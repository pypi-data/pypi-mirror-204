import evalml
import json
import numpy as np
import pandas as pd
from evalml.data_checks import DefaultDataChecks
from evalml.automl import AutoMLSearch
from evalml.pipelines.utils import generate_pipeline_code
from ..util.data_types import get_dataframe_types


def convert_to_json(my_dict):
    for key, value in my_dict.items():
        if isinstance(value, dict):
            convert_to_json(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    convert_to_json(item)
                elif isinstance(item, (np.integer, np.floating)):
                    item = item.item()
        elif isinstance(value, (np.integer, np.floating)):
            my_dict[key] = value.item()
    return json.dumps(my_dict)


def automl(data, target_column, task):
    # split into X and y
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    data_dict = get_dataframe_types(X)

    #Predict task type
    if task=="classification":
      n = len(pd.unique(data[target_column]))
    
      if n==2:
        task="binary"
      else:
        task="multiclass"
     

    #train test split
    X_train, X_test, y_train, y_test = evalml.preprocessing.split_data(X, y, problem_type=task)

    # Datachecks
    objective = ""
    if task == "binary":
        objective = objective + "log loss binary"
    elif task == "multiclass":
        objective = objective + "log loss multiclass"
    elif task == "regression":
        objective = objective + "R2"
    data_checks = DefaultDataChecks(task, objective)
    messages = data_checks.validate(X_train, y_train)

    errors = [message for message in messages if message["level"] == "error"]
    warnings = [message for message in messages if message["level"] == "warning"]
    data_issues = []
    for warning in warnings:
        data_issues.append("Warning:" + warning["message"])

    for error in errors:
        data_issues.append("Error:" + error["message"])



    #AutoMl Search
    automl = AutoMLSearch(X_train=X_train, y_train=y_train, problem_type=task)
    automl.search()

    # Pipeline Rankings
    rankings = automl.rankings
    rankings_json = rankings.to_json(orient="table")

    ids = []
    for i in range(6):
        ids.append(rankings["id"].iloc[i])

    pipelines = []

    for i in ids:
        pip={}
        pipeline = automl.get_pipeline(i)
        pip['id']=i
        pip['name']=pipeline.name
        pip['pipeline']=str(pipeline)
        
        pipeline.fit(X_train, y_train) 
        
        #metrics
        objectives=[]
        if task =='binary':
            objectives.extend(['mcc binary',
                                'log loss binary',
                                'gini',
                                'auc',
                                'recall',
                                'precision',
                                'f1',
                                'balanced accuracy binary',
                                'accuracy binary'])
        elif task == 'multiclass':
            objectives.extend(['mcc multiclass',
                                'log loss multiclass',
                                'auc weighted',
                                'auc macro',
                                'auc micro',
                                'recall weighted',
                                'recall macro',
                                'recall micro',
                                'precision weighted',
                                'precision macro',
                                'precision micro',
                                'f1 weighted',
                                'f1 macro',
                                'f1 micro',
                                'balanced accuracy multiclass',
                                'accuracy multiclass'])
        elif task =='regression':
            objectives.extend(['expvariance',
                                'maxerror',
                                'medianae',
                                'mse',
                                'mae',
                                'r2',
                                'mean squared log error',
                                'root mean squared log error',
                                'root mean squared error',])
        pip['metrics'] = dict(pipeline.score(X_test, y_test, objectives)) 
        
        #Feature importance for best pipeline
        feature_imp = pipeline.feature_importance
        feature_imp_json = feature_imp.to_json(orient="table")
        pip['feature_importance']=feature_imp_json

        # generating code for best_pipeline
        pip["code"] = generate_pipeline_code(pipeline)

        pipelines.append(pip)

    automl_result={}
    automl_result['Data Issues']=data_issues
    automl_result['Data Issue Messages']=messages
    automl_result['Task']=task
    automl_result['Pipelines']=pipelines
    automl_result['input_format']=data_dict

    automl_json = convert_to_json(automl_result)
    automl_json = automl_json.replace("\\", "")
    automl_json = automl_json.replace('"{"schema', '{"schema')
    automl_json = automl_json.replace('", "code', ' ,"code')

    return automl_json
