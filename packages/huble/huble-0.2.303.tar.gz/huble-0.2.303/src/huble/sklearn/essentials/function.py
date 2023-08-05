from sklearn.model_selection import train_test_split as sklearn_tts  # type: ignore
import pandas as pd
from ...error.decorators import function_error_handling
from ...connector import Dataset
import joblib
from ...util.data_types import get_dataframe_types
from ...util.feature_selection import select_features

# @function_error_handling("train_test_split")
def train_test_split(**params):
    data = params["data"]
    target = params["target_column"]
    model = params["model"]
    X = data.drop([target], axis=1)
    data_dict = get_dataframe_types(X)
    data = select_features(data, target)
    train_dataset, test_dataset = sklearn_tts(data, test_size=params["parameters"]["test_size"], random_state=42)
    return train_dataset, test_dataset, data_dict


# @function_error_handling("train_model")
def train_model(**params):
    task_type = params["task_type"]
    data = params["data"]
    model = params["model"]
    if task_type == "clustering":
        Model = model.fit(data)
    else:
        y = data[params["column"]]
        X = data.drop(params["column"], axis=1)

        Model = model.fit(X, y)
    filename = f'model-{params["id"]}.joblib'
    joblib.dump(Model, filename)
    return Model, filename
