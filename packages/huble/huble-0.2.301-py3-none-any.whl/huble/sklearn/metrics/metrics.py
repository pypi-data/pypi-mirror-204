from sklearn import metrics
import evalml
import pandas as pd
from evalml.problem_types import detect_problem_type
import numpy as np

def regression_metrics(y_true, y_pred):
    explained_variance_score=metrics.explained_variance_score(y_true, y_pred)
    max_error = metrics.max_error(y_true, y_pred)
    mean_absolute_error = metrics.mean_absolute_error(y_true, y_pred)
    mean_squared_error = metrics.mean_squared_error(y_true, y_pred)
    mean_squared_log_error = metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error = metrics.median_absolute_error(y_true, y_pred)
    r2_score = metrics.r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error)
    rmsle = np.sqrt(mean_squared_log_error)
   
    
    # create dictionary of metrics
    metrics_dict = {
        "ExpVariance":explained_variance_score,
        "MaxError": max_error,
        "MedianAE": median_absolute_error,
        "MAE": mean_absolute_error,
        "MSE": mean_squared_error,
        "R2": r2_score,
        "Mean Squared Log Error": mean_squared_log_error,
        "Root Mean Squared Log Error": rmsle,
        "Root Mean Squared Error": rmse, 
    }
    return metrics_dict


def classification_metrics(y_true, y_pred):
    accuracy_score = metrics.accuracy_score(y_true, y_pred)
    balanced_accuracy_score = metrics.balanced_accuracy_score(y_true, y_pred)
    f1_score = metrics.f1_score(y_true, y_pred)
    f1_weighted = metrics.f1_score(y_true, y_pred, average="weighted")
    f1_micro = metrics.f1_score(y_true, y_pred, average="micro")
    f1_macro = metrics.f1_score(y_true, y_pred, average="macro")
    log_loss = metrics.log_loss(y_true, y_pred)
    matthews_corrcoef = metrics.matthews_corrcoef(y_true, y_pred)
    precision_score = metrics.precision_score(y_true, y_pred)
    precision_weighted = metrics.precision_score(y_true, y_pred, average="weighted")
    precision_micro = metrics.precision_score(y_true, y_pred, average="micro")
    precision_macro = metrics.precision_score(y_true, y_pred, average="macro")
    recall_score = metrics.recall_score(y_true, y_pred)
    recall_weighted = metrics.recall_score(y_true, y_pred, average="weighted")
    recall_micro = metrics.recall_score(y_true, y_pred, average="micro")
    recall_macro = metrics.recall_score(y_true, y_pred, average="macro")
    roc_auc_score = metrics.roc_auc_score(y_true, y_pred)
    roc_auc_weighted = metrics.roc_auc_score(y_true, y_pred, average="weighted")
    roc_auc_micro = metrics.roc_auc_score(y_true, y_pred, average="micro")
    roc_auc_macro = metrics.roc_auc_score(y_true, y_pred, average='macro')
    
    metrics_dict={}
    y_task = pd.Series(y_true)
    task=(detect_problem_type(y_task))
    task_str = str(task)
    if task_str == 'binary':
        metrics_dict = {
            "MCC Binary": matthews_corrcoef,
            "Log Loss Binary": log_loss,
            "AUC": roc_auc_score,
            "Precision": precision_score,
            "Recall": recall_score,
            "F1": f1_score,
            "Accuracy Binary": accuracy_score,
            "Balanced Accuracy Binary": balanced_accuracy_score,      
        }
    elif task == 'multiclass':
        metrics_dict = {
            "MCC Multiclass": matthews_corrcoef,
            "Log Loss Multiclass": log_loss,
            "Accuracy Multiclass": accuracy_score,
            "Balanced Accuracy Multiclass": balanced_accuracy_score,
            "Precision Weighted": precision_weighted,
            "Precision Micro": precision_micro,
            "Precision Macro": precision_macro,
            "Recall Weighted": recall_weighted,
            "Recall Micro": recall_micro,
            "Recall Macro": recall_macro,            
            "F1 Weighted": f1_weighted,   
            "F1 Macro": f1_macro, 
            "F1 Mirco": f1_micro,  
            "AUC Weighted": roc_auc_weighted,
            "AUC Micro": roc_auc_micro,
            "AUC Macro": roc_auc_macro, 
        }
    return metrics_dict


def clustering_metrics(X, labels):
    silhouette_score = metrics.silhouette_score(X, labels)
    calinski_harabasz_score = metrics.calinski_harabasz_score(X, labels)
    davies_bouldin_score = metrics.davies_bouldin_score(X, labels)
    
    # create dictionary of metrics
    metrics_dict = {
        "silhouette_score": silhouette_score,
        "calinski_harabasz_score": calinski_harabasz_score,
        "davies_bouldin_score": davies_bouldin_score,
    }
    return metrics_dict


def log_metrics(y_true, y_pred, task, X, labels):
    if task == "regression":
        metrics_dict = regression_metrics(y_true, y_pred)
        return metrics_dict
    elif task == "classification":
        metrics_dict = classification_metrics(y_true, y_pred)
        return metrics_dict
    elif task == "clustering":
        metrics_dict = clustering_metrics(X, labels)
        return metrics_dict
