from huble.sklearn.metrics import log_metrics
from sklearn import inspection
import numpy as np
import pandas as pd

def evaluate_model(model, training_dataset, test_dataset, target_column, task_type):
    X = training_dataset.drop([target_column], axis=1)
    y = training_dataset[target_column]
    if task_type == "clustering":        
        score = model.score(X)
        importances = np.repeat(score, X.shape[1]) 
        labels = model.labels_
        metrics = log_metrics(y_true=None, y_pred=None, task=task_type, X=training_dataset, labels=labels)       
    else:
        y_test = test_dataset[target_column]
        X_test = test_dataset.drop([target_column], axis=1)
        y_pred = model.predict(X_test)
        metrics = log_metrics(y_true=y_test, y_pred=y_pred, task=task_type, X=None, labels=None)
        result = inspection.permutation_importance(model, X, y, n_repeats=10, random_state=42)
        importances = result.importances_mean

    feature_importance = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
    feature_importance = feature_importance.sort_values('Importance', ascending=False).reset_index(drop=True)
    
    
    return metrics, feature_importance.to_json()

