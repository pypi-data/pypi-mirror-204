import requests
from boto3.session import Session
import json


class Experiment:
    def __init__(self, experiment_id: str) -> None:
        self.experiment_id = experiment_id
        (
            self.graph,
            self.task_type,
            self.target_column,
            self.modelURL,
            self.input_format,
        ) = self.__get_experiment_details(experiment_id=experiment_id)

    def __get_experiment_details(self, experiment_id: str):
        try:
            response = requests.get(
                f"http://localhost:8000/experiments/{experiment_id}",
            )
            response = response.json()
        except:
            try:
                response = requests.get(
                    f"http://const_server:8000/experiments/{experiment_id}",
                )
                response = response.json()
            except:
                raise Exception("Unable to connect to the server")
        try:
            graph = response["pipelineJSON"]
            project = response["project"]
            target_column = project["targetColumn"]
            task_type = project["taskType"]
            modelURL = response["modelURL"]
            input_format = response["inputFormat"]
        except:
            raise Exception("Invalid Experiment ID")
        return graph, task_type, target_column, modelURL, input_format

    def upload_metrics(self, metrics, input_format, feature_importance_dict):
        requests.put(
            f"http://localhost:8000/experiments/results/{self.experiment_id}",
            data={
                "metrics": json.dumps(metrics),
                "input_format": json.dumps(input_format),
                "feature_importance": json.dumps(feature_importance_dict),
            },
        )

    def upload_model(self, file_name):
        try:
            with open(file_name, "rb") as data:
                print("Uploading model...")
                requests.put(
                    f"http://localhost:8000/experiments/{self.experiment_id}/model/upload", files={"file": data}
                )
            print("Model uploaded successfully")
        except:
            Exception("Unable to upload model")
