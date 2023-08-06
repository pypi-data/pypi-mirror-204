import os
import pickle
from attrs import define, field
from datetime import datetime
from typing import Optional, Tuple, Union, Dict, List

import numpy as np
import pandas as pd
import torch

from botorch.test_functions.synthetic import (
    SyntheticTestFunction,
    Ackley,
    Griewank,
    Levy,
    Michalewicz,
    Rastrigin,
    Rosenbrock,
    StyblinskiTang,
)

from gpytorch.kernels import AdditiveStructureKernel, Kernel, MaternKernel, ScaleKernel

from pymoo.core.problem import Problem
from pymoo.factory import get_reference_directions, get_termination
from pymoo.optimize import minimize
from pymoo.problems.multi import Kursawe, ZDT1, ZDT2, ZDT3, ZDT4, ZDT6

from nemo_bo.acquisition_functions.nsga_improvement.unsga3 import UNSGA3
import nemo_bo.utils.logger as logging_nemo
from nemo_bo.opt.objectives import CalculableObjective, ObjectivesList, RegressionObjective
from nemo_bo.opt.variables import VariablesList
from nemo_bo.opt.constraints import ConstraintsList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class Benchmark:
    """

    Benchmark functions are typically used to simulate the outcomes of experiments in a closed-loop manner and therefore
    can be helpful to evaluate the quality of an optimisation (inferred from the effectiveness of the utilised ML
    model(s) and/or acquisition function to identify the optimum)

    """

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Returns the corresponding output values and standard deviations using the inputted X array and benchmark method

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be used in the prediction, i.e. The data has not
            yet undergone any transformations related to converted categorical variables to their respective
            descriptors or transformations related to standardisation/normalisation

        """
        pass

    def best_result(self) -> Optional[Union[int, float, np.ndarray]]:
        """

        Returns the best result for the benchmark function

        """
        pass


@define
class SingleObjectiveSyntheticBenchmark(Benchmark):
    """

    Adopts the following synthetic functions from the BoTorch package to use as functions in a benchmark.
    M. Balandat, B. Karrer, D. R. Jiang, S. Daulton, B. Letham, A. G. Wilson, and E. Bakshy. BoTorch: A Framework for
    Efficient Monte-Carlo Bayesian Optimization. Advances in Neural Information Processing Systems 33, 2020.
    http://arxiv.org/abs/1910.06403
    https://github.com/pytorch/botorch
    https://botorch.org/

    All functions are to be minimized. The recommended bounds for each variable is shown below:

    1. Ackley (var_bounds = [-32.768, 32.768], obj_bounds = [0.0, 25.0])
    2. Griewank (var_bounds = [-600.0, 600.0], obj_bounds = [0.0, 100.0 * n_var])
    3. Levy (var_bounds = [-10.0, 10.0], obj_bounds = [0.0, 50.0 * n_var])
    4. Michalewicz (var_bounds = [0.0, math.pi], n_var = 2, 5, or 10, obj_bounds = [-1.9, 0.0], [-4.8, 0.0], [-9.8, 0.0])
    5. Rastrigin (var_bounds = [-5.12, 5.12], obj_bounds = [0.0, 50.0 * n_var])
    6. Rosenbrock (var_bounds = [-5.0, 10.0], obj_bounds = [0.0, 810081.0 * (n_var - 1)])
    7. StyblinskiTang (var_bounds = [-5.0, 5.0], obj_bounds = [-40.0 * n_var, 25.0])

    Parameters
    ----------
    function_name: str
        The name of the synthetic function to use ('ackley', 'griewank', 'levy', 'michalewicz',
        'rastrigin', 'rosenbrock', or 'styblinski-tang')
    dim: int
        The number of input dimensions
    noise_std: float = None
        Standard deviation of the observation noise

    """

    function_name: str
    dim: int
    noise_std: Optional[float] = None
    fitted: bool = field(init=False)
    synthetic_function: SyntheticTestFunction = field(init=False)

    def __attrs_post_init__(self):
        if self.function_name == "ackley":
            self.synthetic_function = Ackley(dim=self.dim, noise_std=self.noise_std)
        elif self.function_name == "griewank":
            self.synthetic_function = Griewank(dim=self.dim, noise_std=self.noise_std)
        elif self.function_name == "levy":
            self.synthetic_function = Levy(dim=self.dim, noise_std=self.noise_std)
        elif self.function_name == "michalewicz":
            if self.dim not in [2, 5, 10]:
                raise ValueError(
                    f"The input of input dimensions has been set as {self.dim}. Please use 2, 5, or 10 "
                    f"input dimensions for the Michalewicz function"
                )
            self.synthetic_function = Michalewicz(dim=self.dim, noise_std=self.noise_std)
        elif self.function_name == "rastrigin":
            self.synthetic_function = Rastrigin(dim=self.dim, noise_std=self.noise_std)
        elif self.function_name == "rosenbrock":
            self.synthetic_function = Rosenbrock(dim=self.dim, noise_std=self.noise_std)
        elif self.function_name == "styblinski-tang":
            self.synthetic_function = StyblinskiTang(dim=self.dim, noise_std=self.noise_std)

        self.fitted = True

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Calculate the corresponding output values using the desired synthetic function and the inputted X array

        Parameters
        ----------
        X: np.ndarray
            X array that contains only numerical data

        """
        Y = self.synthetic_function.evaluate_true(torch.tensor(X)).cpu().detach().numpy()

        return Y, np.zeros_like(Y)

    def best_result(self) -> float:
        """

        Returns the best result for the benchmark function

        """
        if self.function_name == "ackley":
            return 0.0
        elif self.function_name == "griewank":
            return 0.0
        elif self.function_name == "levy":
            return 0.0
        elif self.function_name == "michalewicz":
            if self.dim == 2:
                return -1.8013
            elif self.dim == 5:
                return -4.687658
            elif self.dim == 10:
                return -9.66015
        elif self.function_name == "rastrigin":
            return 0.0
        elif self.function_name == "rosenbrock":
            return 0.0
        elif self.function_name == "styblinski-tang":
            return -39.16599 * self.dim


@define
class MultiObjectiveSyntheticBenchmark(Benchmark):
    """

    Adopts the following synthetic functions from the Pymoo package to use as functions in a benchmark.
    The NSGA-based methods were copied and adapted from J. Blank and K. Deb, pymoo: Multi-Objective Optimization in
    Python, in IEEE Access, vol. 8, pp. 89497-89509, 2020, doi: 10.1109/ACCESS.2020.2990567
    https://ieeexplore.ieee.org/document/9078759
    https://github.com/anyoptimization/pymoo

    All objectives in every function are to be minimized. The recommended bounds for each dimension, the number of
    variables, and the number of objectives is shown in parentheses:

    1. Kursawe (var_bounds = [-5.0, 5.0], obj_bounds = approx f1: [-20.0, -5.0], f2: [-13.0, 23.0], n_var = 3,
    n_obj = 2)
    2. ZDT1 (var_bounds = [0.0, 1.0], obj_bounds = approx f1: [0.0, 1.0], f2: [0.0, 7.5], n_var = 30, n_obj = 2)
    3. ZDT2 (var_bounds = [0.0, 1.0], obj_bounds = approx f1: [0.0, 1.0], f2: [0.0, 8.0], n_var = 30, n_obj = 2)
    4. ZDT3 (var_bounds = [0.0, 1.0], obj_bounds = approx f1: [0.0, 1.0], f2: [0.0, 7.5], n_var = 30, n_obj = 2)
    5. ZDT4 (var_bounds = var1: [0.0, 1.0], var2 to var10: [-10.0, 10.0], obj_bounds = approx f1: [0.0, 1.0], f2: [0.0, 900.0], n_var = 10, n_obj = 2)
    6. ZDT6 (var_bounds = [0.0, 1.0], obj_bounds = approx f1: [0.0, 1.0], f2: [0.0, 10.0], n_var = 10, n_obj = 2)

    Parameters
    ----------
    function_name: str
        The name of the synthetic function to use ('kursawe', 'zdt1', 'zdt2', 'zdt3', 'zdt4', 'zdt6')

    """

    function_name: str
    fitted: bool = field(init=False)
    synthetic_function: Problem = field(init=False)

    def __attrs_post_init__(self):
        if self.function_name == "kursawe":
            self.synthetic_function = Kursawe()
        elif self.function_name == "zdt1":
            self.synthetic_function = ZDT1()
        elif self.function_name == "zdt2":
            self.synthetic_function = ZDT2()
        elif self.function_name == "zdt3":
            self.synthetic_function = ZDT3()
        elif self.function_name == "zdt4":
            self.synthetic_function = ZDT4()
        elif self.function_name == "zdt6":
            self.synthetic_function = ZDT6()
        else:
            raise ValueError(f"The synthetic function called {self.function_name} is not supported")

        self.fitted = True

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Calculate the corresponding output values using the desired synthetic function and the inputted X array

        Parameters
        ----------
        X: np.ndarray
            X array that contains only numerical data

        """
        if self.function_name == "kursawe":
            if X.shape[1] != 3:
                raise AttributeError(
                    f"The X array contains {X.shape[1]} variables but the Kursawe two objective "
                    f"synthetic function is for 3 variables"
                )
        elif self.function_name in ["zdt1", "zdt2", "zdt3"]:
            if X.shape[1] != 30:
                raise AttributeError(
                    f"The X array contains {X.shape[1]} variables but the ZDT1, ZDT2, and ZDT3 two objective "
                    f"synthetic functions are for 30 variables"
                )
        elif self.function_name in ["zdt4", "zdt6"]:
            if X.shape[1] != 10:
                raise AttributeError(
                    f"The X array contains {X.shape[1]} variables but the ZDT4, and ZDT6 two objective "
                    f"synthetic functions are for 10 variables"
                )

        out = {"F": np.array([0])}  # Dummy array as the value for 'F'
        self.synthetic_function._evaluate(X, out)
        Y = out["F"]

        return Y, np.zeros_like(Y)

    def best_result(self) -> np.ndarray:
        """

        Returns the best result for the benchmark function

        """
        return self.synthetic_function._calc_pareto_front()


@define
class ModelBenchmark(Benchmark):
    """

    This type of benchmark object is used to accurately predict the outcome of optimisation suggestions as they
    typically utilise all available data for regression objectives. This method will also work for the calculable
    objectives in the optimisation problem.

    Parameters
    ----------
    variables: VariablesList
        VariablesList object that contains information about all variables
    objectives: ObjectivesList
        ObjectivesList object that contains information about all objectives
    constraints: ConstraintsList, Default = None
        ConstraintsList object that contains information about all constraints

    """

    variables: VariablesList
    objectives: ObjectivesList
    constraints: Optional[ConstraintsList] = None
    fitted: bool = field(init=False)
    best: np.ndarray = field(init=False)
    X: np.ndarray = field(init=False)
    Y: np.ndarray = field(init=False)

    def __attrs_post_init__(self):
        self.fitted = False

    def fit(self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, **kwargs) -> None:
        """

        Fits ML models for all specified regression objectives to be used a benchmark functions

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data for all calculable and regression objectives, i.e.
            The data has not yet undergone any transformations related to standardisation/normalisation
        test_ratio: float
            The proportion of inputted X and Y arrays to be split for the validation set where applicable

        """
        logger.info(
            "Performing hyperparameter and model search for the best predictor models for use as benchmarkers for the "
            "regression objectives"
        )

        self.X = X
        self.Y = Y

        # Fit the ML regression model(s)
        self.objectives.fit(
            self.X,
            self.Y,
            self.variables,
            model_search_bool=True,
            test_ratio=test_ratio,
            **kwargs,
        )
        self.fitted = True

        logger.info(
            f"Calculating the approx. best result for the benchmark function. This can take several minutes to "
            f"complete"
        )

        # Calculates the best result using the benchmark model(s) with the input constraints provided (if any)
        xl = 0
        xu = 1
        pop_size = 1200
        generations = 100

        ref_dirs = get_reference_directions("energy", self.objectives.n_obj, pop_size * 0.9, seed=1)
        algorithm = UNSGA3(ref_dirs, pop_size=pop_size)
        problem = NSGABenchmarkProblemWrapper(xl, xu, self.variables, self.objectives, self.constraints)
        termination = get_termination("n_gen", generations)

        # Runs the U-NSGA-III algorithm
        res = minimize(problem, algorithm, termination, verbose=False)

        # Correct by * -1 for maximising objectives from the U-NSGA-III algorithm
        for obj_index, obj in enumerate(self.objectives.max_bool_dict):
            if self.objectives.max_bool_dict[obj]:
                if self.objectives.n_obj > 1:
                    res.F[:, obj_index] *= -1
                else:
                    res.F[obj_index] *= -1

        self.best = res.F

        logger.info(
            f"Identified the best predictor models and hyperparameters for the benchmark functions for the regression "
            f"objectives: {self.objectives.predictor_types}"
        )

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Returns the corresponding output values and standard deviations using the inputted X array and benchmark models
        and calculable objectives

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be used in the prediction, i.e. The data has not
            yet undergone any transformations related to converted categorical variables to their respective
            descriptors or transformations related to standardisation/normalisation

        Returns
        ----------
        Y: np.ndarray
            Complete Y array of output values from all calculable and regression objectives using the provided
            X array
        Y_pred_stddev: np.ndarray
            Complete array of corresponding standard deviations for the predicted Y-values of all calculable and
            regression objectives using the provided X array

        """
        Y = np.zeros((X.shape[0], self.objectives.n_obj), dtype=np.float64)
        Y_stddev = np.zeros_like(Y)
        for obj_index, obj in enumerate(self.objectives.objectives):
            if isinstance(obj, RegressionObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.predict(X)
            elif isinstance(obj, CalculableObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.calculate(X)

        return Y.astype("float"), Y_stddev.astype("float")

    def best_result(self) -> np.ndarray:
        """

        Returns the best result for the benchmark function

        """
        return self.best

    def save(self, dir: str) -> None:
        """

        Saves the ModelBenchmark information

        Parameters
        ----------
        dir: str
            Directory to save the pickle and Excel files of the ModelBenchmark information

        """
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Temporarily stored the information in these lists
        model_info_list = []
        model_info_columns = []
        for obj in self.objectives.objectives:
            if isinstance(obj, RegressionObjective):
                if obj.obj_function.include_validation:
                    model_info_list.append(obj.obj_function.performance_metrics["Train RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["Train r2"])
                    model_info_list.append(obj.obj_function.performance_metrics["Validation RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["Validation r2"])
                    model_info_columns.append(f"{obj.name} Model Train RMSE")
                    model_info_columns.append(f"{obj.name} Model Train r2")
                    model_info_columns.append(f"{obj.name} Model Validation RMSE")
                    model_info_columns.append(f"{obj.name} Model Validation r2")
                else:
                    model_info_list.append(obj.obj_function.performance_metrics["RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["r2"])
                    model_info_columns.append(f"{obj.name} Model Train RMSE")
                    model_info_columns.append(f"{obj.name} Model Train r2")
                model_info_list.append(obj.obj_function.name)

                if obj.obj_function.name == "gp":
                    if isinstance(obj.model_params["kernel"], AdditiveStructureKernel):
                        model_info_list.append(
                            f"AdditiveStructureKernel(ScaleKernel(MaternKernel(ard_num_dims={self.variables.n_var}, "
                            f"nu={obj.model_params['kernel'].base_kernel.base_kernel.nu}, "
                            f"lengthscale_prior=GammaPrior(3.0, 6.0)), outputscale_prior=GammaPrior(2.0, 0.15)), "
                            f"num_dims={self.variables.n_var})"
                        )
                    else:
                        model_info_list.append(
                            f"ScaleKernel(MaternKernel(nu={obj.model_params['kernel'].base_kernel.nu}, "
                            f"ard_num_dims={self.variables.n_var}, lengthscale_prior=GammaPrior(3.0, 6.0)), "
                            f"outputscale_prior=GammaPrior(2.0, 0.15))"
                        )
                else:
                    model_info_list.append(obj.model_params)

                model_info_columns.append(f"{obj.name} Model Type")
                model_info_columns.append(f"{obj.name} Model Hyperparameters")

        model_info_list.append(datetime.now().strftime("%d-%m-%Y, %H-%M-%S"))
        model_info_columns.append("Date and Time")
        # Duplicates this information for every XY row
        model_info = np.array([model_info_list] * self.X.shape[0])

        # Creates the DataFrames of the benchmark function information
        # Constructs lists of variables and objectives with their respective units where provided
        X_columns = []
        for name, units in zip(self.variables.names, self.variables.units):
            if units == "":
                X_columns.append(name)
            else:
                X_columns.append(f"{name} ({units})")

        Y_columns = []
        for name, units in zip(self.objectives.names, self.objectives.units):
            if units == "":
                Y_columns.append(name)
            else:
                Y_columns.append(f"{name} ({units})")

        benchmark_df = pd.DataFrame(
            np.hstack((self.X, self.Y, model_info)),
            columns=X_columns + Y_columns + model_info_columns,
        )

        # Writes the optimisation information DataFrames into Excel files
        with pd.ExcelWriter(
            os.path.join(
                dir,
                f'Model Benchmark {datetime.now().strftime("%d-%m-%Y, %H-%M-%S")}.xlsx',
            )
        ) as writer:
            benchmark_df.to_excel(writer, sheet_name="Model Benchmark")
            for obj in self.objectives.objectives:
                if isinstance(obj, RegressionObjective):
                    if obj.obj_function.include_validation:
                        obj.obj_function.performance_metrics["Train Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Train Parity Data"
                        )
                        obj.obj_function.performance_metrics["Val Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Val Parity Data"
                        )
                    else:
                        obj.obj_function.performance_metrics["Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Train Parity Data"
                        )

        # Writes a pickle file containing the model benchmark information
        benchmark_dict = {
            "Date and Time": datetime.now().strftime("%d-%m-%Y, %H-%M-%S"),
            "Benchmark Table": benchmark_df,
            "X": self.X,
            "Y": self.Y,
        }
        for obj in self.objectives.objectives:
            if isinstance(obj, RegressionObjective):
                benchmark_dict[f"{obj.name} Model Type"] = obj.obj_function.name
                if obj.obj_function.name == "gp":
                    if isinstance(obj.model_params["kernel"], AdditiveStructureKernel):
                        benchmark_dict[f"{obj.name} Model Hyperparameters"] = (
                            f"AdditiveStructureKernel(ScaleKernel(MaternKernel(ard_num_dims={self.variables.n_var}, "
                            f"nu={obj.model_params['kernel'].base_kernel.base_kernel.nu}, "
                            f"lengthscale_prior=GammaPrior(3.0, 6.0)), outputscale_prior=GammaPrior(2.0, 0.15)), "
                            f"num_dims={self.variables.n_var})"
                        )
                    else:
                        benchmark_dict[f"{obj.name} Model Hyperparameters"] = (
                            f"ScaleKernel(MaternKernel(nu={obj.model_params['kernel'].base_kernel.nu}, "
                            f"ard_num_dims={self.variables.n_var}, lengthscale_prior=GammaPrior(3.0, 6.0)), "
                            f"outputscale_prior=GammaPrior(2.0, 0.15))"
                        )
                else:
                    benchmark_dict[f"{obj.name} Model Hyperparameters"] = obj.model_params
                benchmark_dict[f"{obj.name} Model Performance Metrics"] = obj.obj_function.performance_metrics

        with open(
            os.path.join(
                dir,
                f"Model Benchmark {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.pickle",
            ),
            "wb",
        ) as file:
            pickle.dump(benchmark_dict, file, protocol=pickle.HIGHEST_PROTOCOL)


class NSGABenchmarkProblemWrapper(Problem):
    """

    Class for defining a problem in the ModelBenchmark class

    Parameters
    ----------
    xl: int | float | List[int | float]
        Lower bounds for the variables for the NSGA algorithm. If integer, all lower bounds are equal to the integer
        value
    xu: int | float | List[int | float]
        Upper bounds for the variables for the NSGA algorithm. If integer, all upper bounds are equal to the integer
        value
    variables: VariablesList
        VariablesList object that contains information about all variables
    objectives: ObjectivesList
        ObjectivesList object that contains information about all objectives
    constraints: ConstraintsList
        ConstraintsList object that contains information about all constraints

    """

    def __init__(
        self,
        xl: Union[int, float, List[Union[int, float]]],
        xu: Union[int, float, List[Union[int, float]]],
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: ConstraintsList,
    ):
        self.variables = variables
        self.objectives = objectives
        self.constraints = constraints

        n_constr = self.constraints.n_constr if constraints is not None else 0

        super().__init__(
            n_var=self.variables.n_var,
            n_obj=self.objectives.n_obj,
            n_constr=n_constr,
            xl=xl,
            xu=xu,
        )

    def _evaluate(self, X: np.ndarray, out: Dict[str, np.ndarray], **kwargs) -> None:
        """

        Function to calculate the objective(s) and constraint(s) (if any) values

        Parameters
        ----------
        X: np.ndarray
            NSGA generated candidates' X-values, which are min-max normalised
        out: Dict[str, np.ndarray]
            Contains the objective(s) and constraint(s) (if any) values for the generated candidates

        """
        # Un-transform the min-max normalised X array
        X = (X * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
            self.variables.lower_bounds
        )

        # Infer the objective values by drawing samples from the distribution at the X-values
        if self.variables.num_cat_descriptor_var > 0:
            F, _ = self.objectives.evaluate(self.variables.descriptor_to_name(X))
        else:
            F, _ = self.objectives.evaluate(X)

        # * -1 for objectives that are maximising
        for obj_index, obj in enumerate(self.objectives.max_bool_dict):
            if self.objectives.max_bool_dict[obj]:
                F[:, obj_index] *= -1
        out["F"] = F

        # Evaluate the pymoo constraints
        if self.n_constr > 0:
            # Min-max normalises the X array
            X = (X - np.array(self.variables.lower_bounds)) / (
                np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds)
            )
            G = np.zeros((X.shape[0], self.n_constr))
            for index, constr in enumerate(self.constraints.constraints):
                G[:, index] = constr.evaluate_pymoo_constraint(X)
            out["G"] = G
