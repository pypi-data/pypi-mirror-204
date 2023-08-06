from typing import List, Union

from nemo_bo.models.base.base_model import Base_Model
from nemo_bo.models.gp import GPModel
from nemo_bo.models.ngb import NGBoostModel
from nemo_bo.models.nn_bayesian import NNBayesianModel
from nemo_bo.models.nn_concrete import NNConcreteDropoutModel
from nemo_bo.models.nn_ensemble import NNEnsembleModel
from nemo_bo.models.rf import RFModel
from nemo_bo.models.xgb import XGBoostModel


def create_predictor_list(predictor_type: List[Union[str, Base_Model]]) -> List[Base_Model]:
    """

    Parameters
    ----------
    predictor_type: List[str | Base_Model]
        List of predictors to use defined by the user. It can contain strings which correspond to particular model
        types that are built-in to NEMO, or can be any model that inherits from the Base_Model class

    Returns
    -------
    List[str | Base_Model]
        List of predictors which are all inherited the Base_Model class

    """
    if predictor_type is not None:
        if isinstance(predictor_type, list):
            predictor_type_list = []
            for predictor in predictor_type:
                if isinstance(predictor, str):
                    if predictor == "gp":
                        predictor_type_list.append(GPModel)
                    elif predictor == "nn_concrete":
                        predictor_type_list.append(NNConcreteDropoutModel)
                    elif predictor == "nn_ensemble":
                        predictor_type_list.append(NNEnsembleModel)
                    elif predictor == "nn_bayesian":
                        predictor_type_list.append(NNBayesianModel)
                    elif predictor == "xgb":
                        predictor_type_list.append(XGBoostModel)
                    elif predictor == "ngb":
                        predictor_type_list.append(NGBoostModel)
                    elif predictor == "rf":
                        predictor_type_list.append(RFModel)
                    else:
                        raise ValueError(
                            f'Predictor type "{predictor}" is not natively supported. Please provide the class of the '
                            f"external predictor that inherits from the Base_Model class"
                        )
                else:
                    if issubclass(predictor, Base_Model):
                        predictor_type_list.append(predictor)
                    else:
                        raise TypeError(f'Predictor type "{predictor}" does not inherit from the Base_Model class')
            return predictor_type_list

        elif isinstance(predictor_type, str):
            if predictor_type == "gp":
                return [GPModel]
            elif predictor_type == "nn_concrete":
                return [NNConcreteDropoutModel]
            elif predictor_type == "nn_ensemble":
                return [NNEnsembleModel]
            elif predictor_type == "nn_bayesian":
                return [NNBayesianModel]
            elif predictor_type == "xgb":
                return [XGBoostModel]
            elif predictor_type == "ngb":
                return [NGBoostModel]
            elif predictor_type == "rf":
                return [RFModel]
            else:
                raise ValueError(
                    f'Predictor type "{predictor_type}" is not natively supported. Please provide the class of the '
                    f"external predictor that inherits from the Base_Model class"
                )
        elif issubclass(predictor_type, Base_Model):
            return [predictor_type]
        else:
            raise TypeError(f'Predictor type "{predictor_type}" does not inherit from the Base_Model class')
    else:
        return [GPModel, NNConcreteDropoutModel, NNEnsembleModel, NNBayesianModel, XGBoostModel, NGBoostModel, RFModel]
