from .experiment import Experiment
import string
import random


class Deployment:
    def generate_code(self, experiment_id: str):
        experiment = Experiment(experiment_id=experiment_id)
        with open("deployment.py", "w") as f:
            f.write("import requests")
            f.write("\nimport os")
            f.write("\nimport pandas as pd")
            f.write("\nfrom pydantic import BaseModel, Field")
            f.write("\nfrom huble import Experiment,Dataset")
            f.write("\nfrom typing import Union")
            f.write("\nimport joblib")
            f.write('\nexperiment_id = os.getenv("EXPERIMENT_ID")')
            f.write(f"\nexperiment = Experiment(experiment_id)")
            f.write("\n")
            f.write("\nclass RequestBody(BaseModel):")
            for column in experiment.input_format["columns"]:
                if column["name"] != "index":
                    f.write(
                        f"\n\t{''.join(random.choices(string.ascii_lowercase,k=7))}: Union[int, float,str] = Field(None,alias=\"{column['name']}\")"
                    )
            f.write("\n")
            f.write(f"\nmodel_url = experiment.modelURL")
            f.write('\nmodel_content = requests.get(f"https://const-bucket.s3.ap-south-1.amazonaws.com/{model_url}")')
            f.write("\nopen('{model_url}.joblib', 'wb').write(model_content.content)")
            f.write("\nmodel = joblib.load('{model_url}.joblib')")
            f.write("\n")
            f.write("\n")
            f.write("\ndef predict(X):")
            f.write("\n\treturn model.predict(X)")
