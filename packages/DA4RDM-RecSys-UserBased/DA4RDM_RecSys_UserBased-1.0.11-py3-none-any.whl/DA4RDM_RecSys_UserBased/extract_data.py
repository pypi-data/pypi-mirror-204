import pandas as pd
import json


def extract_data(data_path):
    df = pd.read_csv(data_path, sep=";")
    res = df.Message.apply(json.loads) \
        .apply(pd.json_normalize) \
        .pipe(lambda x: pd.concat(x.values))
    dataframe = res
    return dataframe
