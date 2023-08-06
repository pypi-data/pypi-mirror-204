import pandas as pd
from dateutil.parser import parse

def get_dataframe_types(df):
    data_dict = pd.io.json.build_table_schema(df)  # type: ignore
    cat_cols = [col for col in df.columns if df[col].nunique() < 10]
    date_formats = ['%Y-%m-%d', '%Y/%m/%d', '%m-%d-%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%m-%d-%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S']

    date_cols = []

    for col in df.columns:
        if df.dtypes[col]=='O':
          try:
              if df[col].notnull().any() and any([isinstance(parse(str(val), fuzzy=False), (pd.Timestamp, pd.datetime)) for val in df[col] if not pd.isna(val)] for fmt in date_formats):
                date_cols.append(col)
          except ValueError:
            pass
    for col in date_cols:
      df[col]=pd.to_datetime(df[col], errors = 'coerce')   
    for field in data_dict["fields"]:
        if field["type"] == "integer":
            field["type"] = "number"
        if field["name"] in cat_cols:
            field["type"]="categorical"
    data_dict["columns"] = data_dict.pop("fields")
    data_dict.pop("primaryKey")
    data_dict.pop("pandas_version")
    data_dict['columns'].pop(0)
    return data_dict
