import copy
import os
import time
from dataclasses import dataclass
from itertools import combinations
from joblib import Parallel, delayed
from typing import Optional, Tuple, Union

import numpy as np
import random
import torch
from botorch.acquisition.multi_objective.monte_carlo import qNoisyExpectedHypervolumeImprovement
from botorch.acquisition.monte_carlo import qNoisyExpectedImprovement
from botorch.sampling.samplers import SobolQMCNormalSampler
from botorch.models.model_list_gp_regression import ModelListGP
from botorch.optim.optimize import optimize_acqf
from gpytorch.mlls.sum_marginal_log_likelihood import SumMarginalLogLikelihood
from scipy import spatial
from scipy.optimize import Bounds
from scipy.optimize import minimize as scipy_minimize
from scipy.stats import norm

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.acquisition_functions.base_acq_function import AcquisitionFunction
from nemo_bo.acquisition_functions.expected_improvement.ehvi import ExpectedHypervolumeImprovement
from nemo_bo.opt.constraints import ConstraintsList, LinearConstraint
from nemo_bo.opt.objectives import ObjectivesList, RegressionObjective
from nemo_bo.opt.samplers import PoolBased, SampleGenerator, PolytopeSampling
from nemo_bo.opt.variables import VariablesList
from nemo_bo.utils.data_proc import remove_all_nan_rows, remove_nan

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@dataclass
class ExpectedImprovement(AcquisitionFunction):
    """

    Class to instantiate to use the acquisition functions expected improvement for single-objective problems or
    expected hypervolume improvement for multi-objective problems

    Parameters
    ----------
    num_candidates: int
        The number of sets of X arrays to be suggested by the acquisition function
    num_restarts: int, Default = 4
        The number of times to restart the acquisition function. The result from every restart is saved, and the one
        with best improvement is selected
    exploration_factor: int, Default = None
        Determines the amount of exploration during optimisation by controlling the size of the effect of the standard
        deviation of a prediction on exploitation/exploration trade-off. Higher exploration_factor values lead to
        more exploration. Default for single objective optimisation is 1 and multi-objectivve optimisation is 3
    force_botorch_ei_methods: bool, Default = False
        Whether to force the expected improvement type methods to use the BoTorch-based ones, as long as the following
        conditions are met:
        1. All objectives are modelled with GPs
        2. All constraints, if used, are LinearConstraint objects
        3. The sampler chosen is not a PoolBased sampler

    """

    num_candidates: int
    num_restarts: Optional[int] = 4
    exploration_factor: Optional[int] = None
    force_botorch_ei_methods: bool = False
    sample_size: Optional = 500000

    def generate_candidates(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        sampler: Union[SampleGenerator, PoolBased],
        constraints: Optional[ConstraintsList] = None,
        **kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that is called to generate the best candidates using the expected improvement or expected
        hypervolume acquisition functions. This selection is made automatically based on the number of objectives

        Parameters
        ----------
        X: np.ndarray
            An array containing X-values for all variables
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        sampler: SampleGenerator | PoolBased
            Used during the ei or ehvi functions to generate samples (SampleGenerator) or provide the samples defined
            by the user (PoolBased)
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest expected improvement or expected
            hypervolume improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest expected improvement or expected
            hypervolume improvement

        """
        self.sampler = sampler

        X, Y = remove_nan(X, Y)

        if constraints is not None:
            if all([isinstance(constr, LinearConstraint) for constr in constraints.constraints]):
                none_or_linear_constraints_bool = True
            else:
                none_or_linear_constraints_bool = False
        else:
            none_or_linear_constraints_bool = True

        if all([isinstance(obj, RegressionObjective) for obj in objectives.objectives]):
            all_gp_bool = all([obj == "gp" for obj in [obj.obj_function.name for obj in objectives.objectives]])
        else:
            all_gp_bool = False

        if self.force_botorch_ei_methods:
            if not all_gp_bool:
                logger.warning(
                    f"The model(s) for the optimisation are not all GP models therefore NEMO-based expected improvement"
                    f"methods will be used instead of the desired BoTorch methods"
                )
            if not none_or_linear_constraints_bool:
                logger.warning(
                    f"Only linear constraints are currently supported with the BoTorch methods within the NEMO "
                    f"framework therefore NEMO-based expected improvement methods will be used instead of the desired "
                    f"BoTorch methods"
                )
            if isinstance(self.sampler, PoolBased):
                logger.warning(
                    f"Pool-based samplers for benchmarking is not supported with the BoTorch methods within the NEMO "
                    f"framework therefore NEMO-based expected improvement methods will be used instead of the desired "
                    f"BoTorch methods"
                )

        if (
            self.force_botorch_ei_methods
            and all_gp_bool
            and none_or_linear_constraints_bool
            and not isinstance(self.sampler, PoolBased)
        ):
            # Use BoTorch based acquisition functions
            if objectives.n_obj > 1:
                selected_X, selected_Y = self.qnehvi_botorch(X, Y, variables, objectives, constraints)

            elif objectives.n_obj == 1:
                selected_X, selected_Y = self.qnei_botorch(X, Y, variables, objectives, constraints)

        else:
            # Use NEMO based acquisition functions
            if isinstance(self.sampler, PoolBased):
                if self.num_candidates > 4:
                    logger.warning(
                        f"The number of suggested candidates is 5 or greater, which is not recommended for pool-based "
                        f"samples with more than 60 samples due to long run times"
                    )

            if objectives.n_obj > 1:
                if isinstance(self.sampler, SampleGenerator):
                    if self.num_candidates > 1:
                        self.sampler.num_new_points = self.sample_size
                    logger.info(
                        f"Setting the number of candidates to be generated by the sampler to "
                        f"{self.sampler.num_new_points} for more memory-efficient EHVI calculations"
                    )

                if self.exploration_factor is None:
                    self.exploration_factor = 3

                selected_X, selected_Y = self.ehvi(Y, variables, objectives, constraints)

            elif objectives.n_obj == 1:
                if isinstance(self.sampler, SampleGenerator):
                    if self.sampler.num_new_points is None:
                        if isinstance(self.sampler, PolytopeSampling):
                            self.sampler.num_new_points = 1024
                        else:
                            self.sampler.num_new_points = 262144
                    logger.info(
                        f"Setting the number of candidates to be generated by the sampler to "
                        f"{self.sampler.num_new_points} for more efficient EI calculations"
                    )

                if self.exploration_factor is None:
                    self.exploration_factor = 1

                selected_X, selected_Y = self.ei(Y, variables, objectives, constraints)

        return selected_X, selected_Y

    def ei(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: Optional[ConstraintsList] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that determines the candidates with the best expected improvement

        Parameters
        ----------
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest expected improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest expected improvement

        """
        logger.info(f"Identifying conditions with the highest expected improvement")

        success_res_fun_list = []
        success_selected_X_list = []
        success_selected_Y_list = []
        fail_res_fun_list = []
        fail_selected_X_list = []
        fail_selected_Y_list = []
        for iteration in range(self.num_restarts):
            start_time = time.perf_counter()

            if isinstance(self.sampler, PoolBased):
                logger.info(f"Returning X values from the provided sample pool")
                X_new_points = self.sampler.X_pool
            elif isinstance(self.sampler, SampleGenerator):
                X_new_points = self.sampler.generate_samples(variables, constraints)

            Y_new_points, Y_new_points_stddev = objectives.evaluate(X_new_points)

            Y_norm = (Y - objectives.bounds[0, 0]) / (objectives.bounds[0, 1] - objectives.bounds[0, 0])
            Y_new_points_norm = (Y_new_points - objectives.bounds[0, 0]) / (
                objectives.bounds[0, 1] - objectives.bounds[0, 0]
            )
            # Min_max normalisation of Y standard deviation
            # I think this should be fine to minmax normalise like this
            Y_new_points_stddev_norm = Y_new_points_stddev / (objectives.bounds[0, 1] - objectives.bounds[0, 0])

            Y_best = np.max(Y_norm) if objectives.max_bool_dict[objectives.names[0]] else np.min(Y_norm)

            logger.info(f"Identifying approximate conditions with the highest expected improvement")
            with np.errstate(divide="warn"):
                sigma = Y_new_points_stddev_norm * self.exploration_factor
                if objectives.max_bool_dict[objectives.names[0]]:
                    Z = (Y_new_points_norm - Y_best) / sigma
                else:
                    Z = (Y_best - Y_new_points_norm) / sigma

                ei = sigma * (norm.pdf(Z) + (Z * norm.cdf(Z)))
                ei[sigma == 0.0] = 0.0

            sorting_indices = ei[:, -1].argsort()
            index_array = np.arange(X_new_points.shape[0]).reshape(-1, 1)
            concat = np.hstack((X_new_points, Y_new_points, ei))
            concat_sorted = concat[sorting_indices][::-1]
            index_array_sorted = index_array[sorting_indices][::-1]

            X_ei = concat_sorted[:, :-2]
            Y_ei = concat_sorted[:, -2].flatten()

            X_ei_norm = ((X_ei - np.array(variables.lower_bounds))) / (
                np.array(variables.upper_bounds) - np.array(variables.lower_bounds)
            )

            # 0 index for the ei one at the top of the array
            chosen_indices = [0]
            # cosine similarity index of 1.0 for the ei one at the top of the array
            cosine_simularity_list = [1.0]
            # Comparing the X_values for the ei with every other entry down the sorted X_array
            for index, x in enumerate(X_ei_norm):
                cosine_simularity_index = 1 - spatial.distance.cosine(X_ei_norm[0], x)
                # Only passes if the cosine similarity index of a given x row is greater than 0.1 different from all of
                # the x's in the list
                if all((((cs - cosine_simularity_index) ** 2) ** 0.5) > 0.1 for cs in cosine_simularity_list):
                    cosine_simularity_list.append(cosine_simularity_index)
                    chosen_indices.append(index)

                if len(chosen_indices) == self.num_candidates:
                    break

            X_ei = X_ei[chosen_indices]
            Y_ei = Y_ei[chosen_indices].astype(np.float64)

            # Writes the indexes of the selected candidates in the sample pool
            if isinstance(self.sampler, PoolBased):
                self.sampler.index = index_array_sorted[: self.num_candidates].flatten().tolist()

                logger.info("Conditions were successfully selected using expected improvement")
                return X_ei, Y_ei

            elif isinstance(self.sampler, SampleGenerator):

                def fun(X_norm):
                    X_norm_reshape = X_norm.astype(np.float64).reshape(X_ei.shape)
                    X = (
                        X_norm_reshape * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
                    ) + np.array(variables.lower_bounds)

                    if variables.num_cat_descriptor_var > 0:
                        X = variables.descriptor_to_name(X)

                    Y, Y_stddev = objectives.evaluate(X)

                    Y_norm = (Y - objectives.bounds[0, 0]) / (objectives.bounds[0, 1] - objectives.bounds[0, 0])
                    # I think this should be fine to minmax normalise like this
                    Y_stddev_norm = Y_stddev / (objectives.bounds[0, 1] - objectives.bounds[0, 0])

                    with np.errstate(divide="warn"):
                        sigma = Y_stddev_norm * self.exploration_factor
                        if objectives.max_bool_dict[objectives.names[0]]:
                            Z = (Y_norm - Y_best) / sigma
                        else:
                            Z = (Y_best - Y_norm) / sigma

                        ei = sigma * (norm.pdf(Z) + (Z * norm.cdf(Z)))
                        ei[sigma == 0.0] = 0.0

                    ei_sum = np.sum(ei)

                    return -1 * ei_sum

                # Convert the names of categorical variables to their descriptor values
                if variables.num_cat_descriptor_var > 0:
                    X_ei = variables.categorical_transform(X_ei)

                # Normalise all variable values against the bounds
                X_ei_norm = (X_ei - np.array(variables.lower_bounds)) / (
                    np.array(variables.upper_bounds) - np.array(variables.lower_bounds)
                )

                logger.info(f"Optimising the variable location that provides the highest expected improvement")
                if constraints is None:
                    method = "L-BFGS-B"
                    consts = ()
                    options = {
                        # "iprint": 99,
                        "maxiter": 1000,
                        "maxfun": 1000000,
                    }
                else:
                    method = "SLSQP"
                    consts = constraints.create_scipy_constraints(self.num_candidates)
                    options = {
                        # "disp": True,
                        "maxiter": 1000
                    }

                np.random.seed(random.randint(0, 9999999))
                res = scipy_minimize(
                    fun,
                    X_ei_norm.flatten(),
                    method=method,
                    jac="3-point",
                    bounds=Bounds(
                        lb=np.zeros_like(X_ei_norm).flatten(),
                        ub=np.ones_like(X_ei_norm).flatten(),
                        keep_feasible=True,
                    ),
                    constraints=consts,
                    options=options,
                )

                if res.success == True:
                    res_X = res.x.astype(np.float64).reshape(X_ei.shape)

                    # Removes samples that are very similar and replaces them with the original values before
                    # optimization
                    selected_X = copy.copy(res_X)
                    for index_a, candidate_a in enumerate(selected_X):
                        for index_b, candidate_b in enumerate(res_X):
                            if index_a != index_b:
                                if np.all((np.isclose(candidate_a, candidate_b, rtol=1e-2))):
                                    selected_X[index_b] = X_ei_norm[index_b]

                    true_fun = fun(selected_X.flatten())

                    selected_X = (
                        selected_X * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
                    ) + np.array(variables.lower_bounds)

                    if variables.num_cat_var > 0:
                        selected_X = variables.categorical_values_euc(selected_X)
                    if variables.num_cat_descriptor_var > 0:
                        selected_X = variables.descriptor_to_name(selected_X)

                    selected_Y, Y_new_stddev = objectives.evaluate(selected_X)

                    success_res_fun_list.append(true_fun)
                    success_selected_X_list.append(selected_X)
                    success_selected_Y_list.append(selected_Y)

                else:
                    true_fun = res.fun

                    if variables.num_cat_var > 0:
                        X_ei = variables.categorical_values_euc(X_ei)
                    if variables.num_cat_descriptor_var > 0:
                        X_ei = variables.descriptor_to_name(X_ei)

                    fail_res_fun_list.append(true_fun)
                    fail_selected_X_list.append(X_ei)
                    fail_selected_Y_list.append(Y_ei.reshape(-1, 1) if Y_ei.ndim == 1 else Y_ei)

                print(
                    f'{iteration + 1}/{self.num_restarts}, EI optimisation: {"Success" if res.success else "Fail"}, '
                    f"iteration time (s) = {time.perf_counter() - start_time:>4.2f}, current function value: {true_fun}"
                    f", best function value: {min(success_res_fun_list + fail_res_fun_list)}"
                )

        if len(success_res_fun_list) > 0:
            logger.info("Successfully optimised the variable location that provides the highest expected improvement")
            best_fun_index = success_res_fun_list.index(min(success_res_fun_list))

            return success_selected_X_list[best_fun_index], success_selected_Y_list[best_fun_index]

        else:
            logger.warning(
                "Optimisation of the variable location that provides the highest expected improvement failed. Will use "
                "the best failed X-values"
            )
            best_fun_index = fail_res_fun_list.index(min(fail_res_fun_list))

            return fail_selected_X_list[best_fun_index], fail_selected_Y_list[best_fun_index]

    def ehvi(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: Optional[ConstraintsList] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that determines the candidates with the best expected hypervolume improvement

        Parameters
        ----------
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest expected hypervolume improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest expected hypervolume improvement

        """
        logger.info(f"Identifying conditions with the highest expected hypervolume improvement")

        # Construct hypervolume reference point
        ref_point = self.build_ref_point(objectives.max_bool_dict)

        success_res_fun_list = []
        success_selected_X_list = []
        success_selected_Y_list = []
        fail_res_fun_list = []
        fail_selected_X_list = []
        fail_selected_Y_list = []
        for iteration in range(self.num_restarts):
            start_time = time.perf_counter()

            if isinstance(self.sampler, PoolBased):
                logger.info(f"Returning X values from the provided sample pool")
                X_new_points = self.sampler.X_pool
                index_combos = list(combinations(np.arange(X_new_points.shape[0]), self.num_candidates))
            elif isinstance(self.sampler, SampleGenerator):
                X_new_points = self.sampler.generate_samples(variables, constraints)

            Y_new_points, Y_new_points_stddev = objectives.evaluate(X_new_points)

            sign_adjusted_Y = self.Y_norm_minmax_transform(Y, objectives.bounds, objectives.max_bool_dict)
            sign_adjusted_Y_new_points = self.Y_norm_minmax_transform(
                Y_new_points, objectives.bounds, objectives.max_bool_dict
            )

            # Min_max normalisation of Y standard deviation
            # I think this should be fine to minmax normalise like this
            for obj_index, _ in enumerate(objectives.bounds):
                Y_new_points_stddev[:, obj_index] = Y_new_points_stddev[:, obj_index] / (
                    objectives.bounds[obj_index, 1] - objectives.bounds[obj_index, 0]
                )

            # Creates a list of expected hypervolume improvements for all combinations of the new Y points
            logger.info(f"Identifying approximate conditions with the highest expected hypervolume improvement")
            ehvi = ExpectedHypervolumeImprovement(
                ref_point=torch.tensor(ref_point, dtype=torch.double),
                Y=torch.tensor(sign_adjusted_Y, dtype=torch.double),
            )

            # Create a list of indices to randomly select candidate solutions from each input set
            idx_list = list(range(len(X_new_points)))
            random.shuffle(idx_list)

            start_time_ehvi= time.time()

            # Generate multiple sets of candidate solutions and compute EHVI for each set
            ehvi_list = []
            num_sets = int(self.sample_size/5)  # specify the number of sets to generate

            for i in range(num_sets):
                # randomly select `self.num_candidates` items from each input set using the shuffled index list
                X_candidates = [X_new_points[j] for j in idx_list[:self.num_candidates]]
                Y_candidates = [Y_new_points[j] for j in idx_list[:self.num_candidates]]
                Y_stddev_candidates = [Y_new_points_stddev[j] for j in idx_list[:self.num_candidates]]
                sign_adjusted_Y_candidates = [sign_adjusted_Y_new_points[j] for j in idx_list[:self.num_candidates]]

                # evaluate EHVI for the set of candidate solutions
                ehvi_val = ehvi.ehvi_calc(
                    Y_new=torch.tensor(np.array(sign_adjusted_Y_candidates), dtype=torch.double),
                    Y_new_stddev=torch.tensor(np.array(Y_stddev_candidates), dtype=torch.double),
                    exploration_factor=self.exploration_factor,
                )
                ehvi_list.append((ehvi_val, X_candidates, Y_candidates))

            print('Runtime:', time.time() - start_time_ehvi, 'seconds')

            # Select the set of candidate solutions with the highest EHVI value
            ehvi_list.sort(key=lambda x: x[0], reverse=True)
            best_set = ehvi_list[0][1:]
            X_ehvi = np.array(best_set[0])
            Y_ehvi = np.array(best_set[1])

            start_time_comb = time.time()

            # Writes the indexes of the selected candidates in the sample pool
            if isinstance(self.sampler, PoolBased):
                self.sampler.index = list(index_combos[max_idx])

                logger.info("Conditions were successfully selected using expected hypervolume improvement")
                return X_ehvi, Y_ehvi

            elif isinstance(self.sampler, SampleGenerator):
                # The objective function to be minimized for the scipy optimize minimize method
                def fun(X_norm):
                    X_norm_reshape = X_norm.astype(np.float64).reshape(X_ehvi.shape)
                    X = (
                        X_norm_reshape * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
                    ) + np.array(variables.lower_bounds)

                    if variables.num_cat_descriptor_var > 0:
                        X = variables.descriptor_to_name(X)

                    Y, Y_stddev = objectives.evaluate(X)

                    sign_adjusted_Y = self.Y_norm_minmax_transform(Y, objectives.bounds, objectives.max_bool_dict)
                    # Min_max normalisation of Y standard deviation
                    # I think this should be fine to minmax normalise like this
                    for obj_index, _ in enumerate(objectives.bounds):
                        Y_stddev[:, obj_index] = Y_stddev[:, obj_index] / (
                            objectives.bounds[obj_index, 1] - objectives.bounds[obj_index, 0]
                        )

                    try:
                        fun_val = -1 * ehvi.ehvi_calc(
                            Y_new=torch.tensor(sign_adjusted_Y, dtype=torch.double),
                            Y_new_stddev=torch.tensor(Y_stddev, dtype=torch.double),
                            exploration_factor=self.exploration_factor,
                        )
                    except ValueError:
                        fun_val = -1 * torch.tensor(1e-8, dtype=torch.double)

                    return fun_val.item()

                # Convert the names of categorical variables with their descriptor values
                if variables.num_cat_descriptor_var > 0:
                    X_ehvi = variables.categorical_transform(X_ehvi)

                # Normalise all variable values against the bounds
                X_ehvi_norm = (X_ehvi - np.array(variables.lower_bounds)) / (
                    np.array(variables.upper_bounds) - np.array(variables.lower_bounds)
                )

                # Performs the scipy optimize minimize method
                logger.info(
                    f"Optimising the variable location that provides the highest expected hypervolume improvement"
                )
                if constraints is None:
                    method = "L-BFGS-B"
                    consts = ()
                    options = {
                        # "iprint": 99,
                        "maxiter": 1000,
                        "maxfun": 1000000,
                    }
                else:
                    method = "SLSQP"
                    consts = constraints.create_scipy_constraints(self.num_candidates)
                    options = {
                        # "disp": True,
                        "maxiter": 1000
                    }

                np.random.seed(random.randint(0, 9999999))
                res = scipy_minimize(
                    fun,
                    X_ehvi_norm.flatten(),
                    method=method,
                    jac="3-point",
                    bounds=Bounds(
                        lb=np.zeros_like(X_ehvi_norm).flatten(),
                        ub=np.ones_like(X_ehvi_norm).flatten(),
                        keep_feasible=True,
                    ),
                    constraints=consts,
                    options=options,
                )

                if -1*res.fun > -1*max([item[0] for item in ehvi_list]):
                    if not res.success == True:
                        logger.warning(
                            f"Attempts to optimise the variable location that provides the highest expected "
                            f"hypervolume improvement failed to converge but still improved and so will use the new X "
                            f"values"
                        )

                    # Transform the optimised X value and calculate the corresponding objective Y values
                    res_X = res.x.astype(np.float64).reshape(X_ehvi.shape)

                    # Removes samples that are very similar and replaces them with the original values before
                    # optimization
                    selected_X = copy.copy(res_X)
                    for index_a, candidate_a in enumerate(selected_X):
                        for index_b, candidate_b in enumerate(res_X):
                            if index_a != index_b:
                                if np.all((np.isclose(candidate_a, candidate_b, rtol=1e-2))):
                                    selected_X[index_b] = X_ehvi_norm[index_b]

                    true_fun = fun(selected_X.flatten())

                    selected_X = (
                        selected_X * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
                    ) + np.array(variables.lower_bounds)

                    if variables.num_cat_var > 0:
                        selected_X = variables.categorical_values_euc(selected_X)
                    if variables.num_cat_descriptor_var > 0:
                        selected_X = variables.descriptor_to_name(selected_X)

                    selected_Y, selected_Y_stddev = objectives.evaluate(selected_X)

                    success_res_fun_list.append(true_fun)
                    success_selected_X_list.append(selected_X)
                    success_selected_Y_list.append(selected_Y)

                else:
                    true_fun = res.fun

                    if variables.num_cat_var > 0:
                        X_ehvi = variables.categorical_values_euc(X_ehvi)
                    if variables.num_cat_descriptor_var > 0:
                        X_ehvi = variables.descriptor_to_name(X_ehvi)

                    fail_res_fun_list.append(true_fun)
                    fail_selected_X_list.append(X_ehvi)
                    fail_selected_Y_list.append(Y_ehvi)

                print(
                    f'{iteration + 1}/{self.num_restarts}, EHVI optimisation: {"Success" if res.success else "Fail"}, '
                    f"iteration time (s) = {time.perf_counter() - start_time:>4.2f}, current function value: {true_fun}"
                    f", best function value: {min(success_res_fun_list + fail_res_fun_list)}"
                )

        if len(success_res_fun_list) > 0:
            logger.info("Successfully optimised the variable location that provides the highest expected improvement")
            best_fun_index = success_res_fun_list.index(min(success_res_fun_list))

            return success_selected_X_list[best_fun_index], success_selected_Y_list[best_fun_index]

        else:
            logger.warning(
                "Optimisation of the variable location that provides the highest expected improvement failed. Will "
                "use the best failed X-values"
            )
            best_fun_index = fail_res_fun_list.index(min(fail_res_fun_list))

            return fail_selected_X_list[best_fun_index], fail_selected_Y_list[best_fun_index]

    def qnei_botorch(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: Optional[ConstraintsList] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that determines the candidates with the best expected improvement using the qNoisyExpectedImprovement
        acquisition function from the BoTorch package

        Parameters
        ----------
        X: np.ndarray
            An array containing X-values for all variables
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest expected improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest expected improvement

        """
        logger.info(f"Identifying conditions with the highest expected improvement")

        # BoTorch acquisition functions require the GP models for minimising objectives to be fitted using values that
        # have been multiplied by -1. This will re-fit the GP models with Y-values that have the correct sign
        temp_objectves = copy.copy(objectives)
        temp_objectves.objectives[0].fit_regressor(X, Y if objectives.objectives[0].obj_max_bool else -Y, variables)

        # Convert the names of categorical variables with their descriptor values
        if variables.num_cat_descriptor_var > 0:
            X = variables.categorical_transform(X)

        # Instantiate the single objective qNoisyExpectedImprovement acquisition function
        # This acquisition function is not using min-max normalised X-values
        acq_func = qNoisyExpectedImprovement(
            model=temp_objectves.objectives[0].obj_function.model,
            X_baseline=torch.tensor(X),
            sampler=SobolQMCNormalSampler(num_samples=1024),
        )

        # Optimises the acquisition function and returns the suggested candidates
        selected_X, _ = optimize_acqf(
            acq_function=acq_func,
            bounds=torch.stack((torch.tensor(variables.lower_bounds), torch.tensor(variables.upper_bounds))),
            q=self.num_candidates,
            num_restarts=self.num_restarts,
            raw_samples=1024,
            equality_constraints=constraints.create_botorch_constraints("eq") if constraints is not None else None,
            inequality_constraints=constraints.create_botorch_constraints("ineq") if constraints is not None else None,
            options={"batch_limit": 5, "maxiter": 1000},
            sequential=True,
        )
        selected_X = selected_X.detach().cpu().numpy()

        if variables.num_cat_descriptor_var > 0:
            selected_X = variables.descriptor_to_name(selected_X.detach().cpu().numpy())

        selected_Y, _ = temp_objectves.evaluate(selected_X)

        return selected_X, selected_Y if objectives.objectives[0].obj_max_bool else -selected_Y

    def qnehvi_botorch(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: Optional[ConstraintsList] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that determines the candidates with the best expected improvement using the
        qNoisyExpectedHypervolumeImprovement acquisition function from the BoTorch package

        Parameters
        ----------
        X: np.ndarray
            An array containing X-values for all variables
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest expected improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest expected improvement

        """
        logger.info(f"Identifying conditions with the highest expected hypervolume improvement")

        # BoTorch acquisition functions require the GP models for minimising objectives to be fitted using values that
        # have been multiplied by -1. This will re-fit the GP models with Y-values that have the correct sign
        temp_objectves = copy.copy(objectives)
        for obj_index, obj in enumerate(temp_objectves.objectives):
            obj.fit_regressor(X, Y[:, obj_index] if obj.obj_max_bool else -Y[:, obj_index], variables)

        # Create the ModelListGP object for convenience
        model = ModelListGP(*[obj.obj_function.model for obj in temp_objectves.objectives])
        mll = SumMarginalLogLikelihood(model.likelihood, model)
        model.eval()
        mll.eval()

        # Convert the names of categorical variables with their descriptor values
        if variables.num_cat_descriptor_var > 0:
            X = variables.categorical_transform(X)

        # Normalise all variable values against the bounds
        X_norm = (X - np.array(variables.lower_bounds)) / (
            np.array(variables.upper_bounds) - np.array(variables.lower_bounds)
        )

        # Instantiate the multi-objective qNoisyExpectedHypervolumeImprovement acquisition function
        acq_func = qNoisyExpectedHypervolumeImprovement(
            model=model,
            ref_point=self.build_ref_point(temp_objectves.max_bool_dict),  # use known reference point
            X_baseline=torch.tensor(X_norm),
            prune_baseline=True,
            sampler=SobolQMCNormalSampler(num_samples=1024),
        )

        # Optimises the acquisition function and returns the suggested candidates
        selected_X_norm, _ = optimize_acqf(
            acq_function=acq_func,
            bounds=torch.stack((torch.zeros(X_norm.shape[1]), torch.ones(X_norm.shape[1]))),
            q=self.num_candidates,
            num_restarts=self.num_restarts,
            raw_samples=1024,
            equality_constraints=constraints.create_botorch_constraints("eq") if constraints is not None else None,
            inequality_constraints=constraints.create_botorch_constraints("ineq") if constraints is not None else None,
            options={"batch_limit": 5, "maxiter": 1000},
            sequential=True,
        )

        # Un-min-max normalises the suggested candidates
        selected_X = (
            selected_X_norm.detach().cpu().numpy()
            * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
        ) + np.array(variables.lower_bounds)

        if variables.num_cat_descriptor_var > 0:
            selected_X = variables.descriptor_to_name(selected_X)

        selected_Y, _ = temp_objectves.evaluate(selected_X)

        for obj_index, obj in enumerate(temp_objectves.objectives):
            if not obj.obj_max_bool:
                selected_Y[:, obj_index] = -selected_Y[:, obj_index]

        return selected_X, selected_Y
