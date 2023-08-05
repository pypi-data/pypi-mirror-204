import pandas as pd
import boto3
from ..util.data_types import get_dataframe_types
import boto3


class Dataset:
    def __init__(self, url) -> None:
        self.file_name = url
        self.dataframe = self.__load_dataset(url)

    def __load_dataset(self, url: str) -> pd.DataFrame:
        print("Loading dataset from S3: ", url)
        return pd.read_csv("https://const-bucket.s3.ap-south-1.amazonaws.com/" + url)

    def parse_dataset(self):
        data_dict = get_dataframe_types(self.dataframe)
        data_dict["rows"] = len(self.dataframe.axes[0])
        return data_dict
