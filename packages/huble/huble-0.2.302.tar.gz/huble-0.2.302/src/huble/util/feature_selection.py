import pandas as pd
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from evalml.problem_types import detect_problem_type

def select_features(data: pd.DataFrame, target_column: str) -> pd.DataFrame:
    
    label_encoder = LabelEncoder()
    for col in data.select_dtypes(include='object'):
        data[col] = label_encoder.fit_transform(data[col].astype(str))

    X = data.drop(target_column, axis=1)
    y = data[target_column]
    task_type = str(detect_problem_type(y))
    if task_type=="regression":
      estimator = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
      estimator = RandomForestClassifier(n_estimators=100, random_state=42)
    sfm = SelectFromModel(estimator)

    sfm.fit(X, y)
    selected_features_mask = sfm.get_support()
    selected_features_names = X.columns[selected_features_mask]

    selected_data = data[selected_features_names.union([target_column])]

    return selected_data
