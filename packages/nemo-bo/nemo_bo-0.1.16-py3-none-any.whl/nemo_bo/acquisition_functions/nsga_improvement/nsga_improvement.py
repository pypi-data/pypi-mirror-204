import os
from dataclasses import dataclass
from itertools import combinations
from typing import Optional, Tuple

import numpy as np
import torch
from botorch.utils.multi_objective.hypervolume import Hypervolume
from botorch.utils.multi_objective.pareto import is_non_dominated
from pymoo.core.result import Result
from pymoo.factory import get_reference_directions, get_termination
from pymoo.optimize import minimize

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.acquisition_functions.base_acq_function import AcquisitionFunction
from nemo_bo.acquisition_functions.nsga_improvement.problem_wrapper import NSGAProblemWrapper
from nemo_bo.acquisition_functions.nsga_improvement.unsga3 import UNSGA3
from nemo_bo.acquisition_functions.highest_uncertainty.highest_uncertainty import HighestUncertainty
from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList
from nemo_bo.opt.samplers import LatinHyperCubeSampling, PoolBased, SampleGenerator
from nemo_bo.opt.variables import VariablesList
from nemo_bo.utils.data_proc import remove_all_nan_rows

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@dataclass
class NSGAImprovement(AcquisitionFunction):
    """

    For single-objective and multi-objective problems, this acquisition function can select between a method that
    identifies the highest hypervolume improvement using a U-NSGA-III algorithm for selecting candidates, or an
    explorative method that identifies the approximate region of the variable space that has the highest uncertainty
    in the objective prediction

    Parameters
    ----------
    num_candidates: int
        The number of sets of X arrays to be suggested by the acquisition function

    """

    num_candidates: int

    def generate_candidates(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        sampler: Optional[SampleGenerator] = None,
        constraints: Optional[ConstraintsList] = None,
        **acq_func_kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that is called when generate the best candidates using the U-NSGA-III algorithm or the highest
        uncertainty acquisition function

        Parameters
        ----------
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        sampler: SampleGenerator, Default = None
            Used to generate samples (SampleGenerator). PoolBased is not supported
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest hypervolume improvement or highest
            uncertainty
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest hypervolume improvement or highest
            uncertainty

        """
        if isinstance(sampler, PoolBased):
            raise NotImplementedError(
                "The PoolBased sampler is incompatible with the NSGAImprovement acquisition function. Please select a "
                "different sampler if you wish to continue using this acquisition function. Alternatively, you may use "
                "the ExpectedImprovement acquisition function with the PoolBased sampler instead"
            )

        if self.num_candidates > 4:
            logger.warning(
                f"The number of suggested candidates is more than 4, which is not recommended due to the risk of long "
                f"run times"
            )

        self.pop_size = acq_func_kwargs.get("pop_size")
        self.generations = acq_func_kwargs.get("generations")

        Y = remove_all_nan_rows(Y)

        if self.pop_size is None:
            self.pop_size = 200

        if self.generations is None:
            # self.generations = 50
            self.generations = 2

        self.generate_pareto(variables, objectives, constraints)
        selected_X, selected_Y = self.hvi(self.res.X, self.res.F, Y, variables, objectives)

        if not self.hvi_search_pass:
            highest_uncertainty = HighestUncertainty(num_candidates=self.num_candidates)
            selected_X, selected_Y = highest_uncertainty.generate_candidates(
                variables, objectives, sampler=sampler, constraints=constraints
            )

        return selected_X, selected_Y

    def generate_pareto(
        self, variables: VariablesList, objectives: ObjectivesList, constraints: ConstraintsList
    ) -> Result:
        """
        Runs the U-NSGA-III method to generate the samples that have the highest hypervolume

        Parameters
        ----------
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        res: Result
            Contains all of the information and results from the U-NSGA-III method

        """

        xl = 0
        xu = 1

        ref_dirs = get_reference_directions("energy", objectives.n_obj, self.pop_size * 0.9, seed=1)

        logger.info(f"Running the U-NSGA-III algorithm")
        algorithm = UNSGA3(ref_dirs, pop_size=self.pop_size)
        problem = NSGAProblemWrapper(xl, xu, variables, objectives, constraints)
        termination = get_termination("n_gen", self.generations)

        # Runs the U-NSGA-III algorithm
        self.res = minimize(problem, algorithm, termination, verbose=True)

        # Correct by * -1 for maximising objectives from the U-NSGA-III algorithm
        for obj_index, obj in enumerate(objectives.max_bool_dict):
            if objectives.max_bool_dict[obj]:
                if objectives.n_obj > 1:
                    self.res.F[:, obj_index] *= -1
                else:
                    self.res.F[obj_index] *= -1

        # Undo min-max normalisation of X values identified by U-NSGA-III
        self.res.X = (self.res.X * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))) + np.array(
            variables.lower_bounds
        )

        return self.res

    def hvi(
        self,
        X_nsga: np.ndarray,
        Y_nsga: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Identifies the candidate(s) from the solutions from the U-NSGA-III optimisation that will produce the highest
        hypervolume improvement

        Parameters
        ----------
        X_nsga: np.ndarray
            Variable values for the solutions from the U-NSGA-III optimisation
        Y_nsga : np.ndarray
            Objective values for the solutions from the U-NSGA-III optimisation
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest hypervolume improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest hypervolume improvement

        """
        logger.info(f"Identifying conditions with the largest hypervolume")

        # Construct hypervoume reference point
        ref_point = self.build_ref_point(objectives.max_bool_dict)

        # Min-max normalisation of objective values and * -1 for minimising objectives
        sign_adjusted_Y = self.Y_norm_minmax_transform(Y, objectives.bounds, objectives.max_bool_dict)
        sign_adjusted_Y_nsga = self.Y_norm_minmax_transform(Y_nsga, objectives.bounds, objectives.max_bool_dict)

        # Appends all Y_nsga points to the Y array
        Yappy_Ynsga = np.vstack([sign_adjusted_Y, sign_adjusted_Y_nsga])

        # Identifies which data points are non-dominated
        pareto_mask_Yappy_Ynsga = is_non_dominated(torch.tensor(Yappy_Ynsga, dtype=torch.double))

        # Slice out the mask of the Y_nsga points on the pareto front
        pareto_front_Ynsga_mask = pareto_mask_Yappy_Ynsga[Y.shape[0] :].cpu().detach().numpy()

        # If the number of Y_nsga points is greater than or equal to the desired number of candidates
        if pareto_front_Ynsga_mask.sum() >= self.num_candidates:
            # The X_nsga, Y_nsga and sign_adjusted_Y_nsga points that are on the pareto front
            X_nsga = X_nsga[pareto_front_Ynsga_mask]
            Y_nsga = Y_nsga[pareto_front_Ynsga_mask]
            sign_adjusted_Y_nsga = sign_adjusted_Y_nsga[pareto_front_Ynsga_mask]

            # Creates a list of hypervolumes for candidate(s) that successfully improve the hypervolume
            hv_list = []
            candidates_X_list = []
            candidates_Y_list = []
            X_nsga_combos = list(combinations(X_nsga, self.num_candidates))
            Y_nsga_combos = list(combinations(Y_nsga, self.num_candidates))
            sign_adjusted_Y_nsga_combos = list(combinations(sign_adjusted_Y_nsga, self.num_candidates))
            for x, y, candidates_Y in zip(X_nsga_combos, Y_nsga_combos, sign_adjusted_Y_nsga_combos):
                # Adds the candidate objective values to the experimental data set
                YappF = np.vstack([sign_adjusted_Y, np.array(candidates_Y)])
                # Identifies which data points are non-dominated
                pareto_mask_YappF = is_non_dominated(torch.tensor(YappF, dtype=torch.double))
                # Creates an numpy.ndarray containing the non-dominated points
                pareto_front_YappF = YappF[pareto_mask_YappF]

                candidates_X_list.append(x)
                candidates_Y_list.append(y)

                # Calculates the hypervolume
                hv = Hypervolume(ref_point=torch.tensor(ref_point, dtype=torch.double))
                hv_list.append(hv.compute(torch.tensor(pareto_front_YappF, dtype=torch.double)))

            # Selects the variable and objective values of the candidate(s) that produced the largest hypervolume
            max_idx = hv_list.index(max(hv_list))
            selected_X = np.array(candidates_X_list[max_idx])
            selected_Y = np.array(candidates_Y_list[max_idx])

            if variables.num_cat_descriptor_var > 0:
                selected_X = variables.descriptor_to_name(selected_X)

            self.hvi_search_pass = True
            logger.info("Conditions were successfully selected using hypervolume improvement")

        else:
            logger.info(
                "Failed to identify a set of conditions that would improve the hypervolume at the desired batch size"
            )
            selected_X = np.array([0])  # Dummy array
            selected_Y = np.array([0])  # Dummy array
            self.hvi_search_pass = False

        return selected_X, selected_Y
