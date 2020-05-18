import pandas as pd
import os
import numpy as np

"""
    CoronaData stores all information concerning Corona Cases/Deaths per US State     
"""


class CoronaData:
    def __init__(self):
        self.file_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
        self.file_name = 'us-counties.csv'

    def read_data(self, base_dir='..'):
        file_path = f"{base_dir}/Data/{self.file_name}"
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path, index_col=0)
            df = df.replace(np.nan, 0)

        else:
            df = pd.read_csv(self.file_url, index_col=0)
            df.to_csv(file_path)
        return df
