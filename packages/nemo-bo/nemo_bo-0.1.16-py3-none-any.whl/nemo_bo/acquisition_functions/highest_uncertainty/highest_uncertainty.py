import os
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
from scipy import spatial

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.acquisition_functions.base_acq_function import AcquisitionFunction
from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList
from nemo_bo.opt.samplers import LatinHyperCubeSampling, PoolBased, SampleGenerator
from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@dataclass
class HighestUncertainty(AcquisitionFunction):
    """

    For single-objective and multi-objective problems, this acquisition function is an explorative method that
    identifies the approximate region of the variable space that has the highest uncertainty in the objective
    prediction

    Parameters
    ----------
    num_candidates: int
        The number of sets of X arrays to be suggested by the acquisition function

    """

    num_candidates: int

    def generate_candidates(
        self,
        variables: VariablesList,
        objectives: ObjectivesList,
        sampler: SampleGenerator,
        constraints: Optional[ConstraintsList] = None,
        num_new_points: int = 2**21,
        **acq_func_kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that is called to generate the candidates that has Y-values with the highest uncertainty

        Parameters
        ----------
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        sampler: SampleGenerator
            Used to generate samples (SampleGenerator). PoolBased is not supported
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints
        num_new_points: int, Default: 2 ** 21
            Number of new sets of input variables to generate

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest uncertainty
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest uncertainty

        """
        if isinstance(sampler, PoolBased):
            raise NotImplementedError(
                "The PoolBased sampler is incompatible with the HighestUncertainty acquisition function. Please select "
                "a different sampler if you wish to continue using this acquisition function. Alternatively, you may "
                "use the ExpectedImprovement acquisition function with the PoolBased sampler instead"
            )

        logger.info(f"Identifying conditions with the highest uncertainty")

        if sampler is None:
            sampler = LatinHyperCubeSampling(num_new_points)
        else:
            sampler.num_new_points = num_new_points

        X_new_points = sampler.generate_samples(variables, constraints)

        Y_new_points, Y_new_points_stddev = objectives.evaluate(X_new_points)

        # Min_max normalisation of Y standard deviation
        # I think this should be fine to minmax normalise like this
        for obj_index, _ in enumerate(objectives.bounds):
            Y_new_points_stddev[:, obj_index] = Y_new_points_stddev[:, obj_index] / (
                objectives.bounds[obj_index, 1] - objectives.bounds[obj_index, 0]
            )

        Y_new_points_stddev_sum = np.sum(Y_new_points_stddev, axis=1).reshape(-1, 1)
        sorting_indices = Y_new_points_stddev_sum[:, -1].argsort()

        X_new_points_sorted = X_new_points[sorting_indices][::-1]

        if variables.num_cat_var > 0:
            X_new_points = variables.categorical_transform(X_new_points).astype("float")
        X_new_points_norm_sorted = (
            (X_new_points[sorting_indices][::-1] - np.array(variables.lower_bounds))
            / (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
        )[sorting_indices][::-1]
        Y_new_points_sorted = Y_new_points[sorting_indices][::-1]
        Y_new_points_stddev_sum_sorted = Y_new_points_stddev_sum[sorting_indices][::-1]

        # 0 index for the highest uncertainty one at the top of the array
        chosen_indices = [0]
        # cosine similarity index of 1.0 for the highest uncertainty one at the top of the array
        cosine_simularity_list = [1.0]
        # Comparing the X-values for the highest uncertainty with every other entry down the sorted X array
        for index, x in enumerate(X_new_points_norm_sorted):
            cosine_simularity_index = 1 - spatial.distance.cosine(X_new_points_norm_sorted[0], x)
            # Only passes if the cosine similarity index of a given x row is greater than 0.1 different compared to all
            # of the x's in the list
            if all((((cs - cosine_simularity_index) ** 2) ** 0.5) > 0.1 for cs in cosine_simularity_list):
                cosine_simularity_list.append(cosine_simularity_index)
                chosen_indices.append(index)

            if len(chosen_indices) == self.num_candidates:
                break

        selected_X = X_new_points_sorted[chosen_indices]
        selected_Y = Y_new_points_sorted[chosen_indices].astype(np.float64)
        total_Y_std = Y_new_points_stddev_sum_sorted[chosen_indices].astype(np.float64)

        logger.info(f"Identified variables with the most uncertain output values")

        return selected_X, selected_Y
