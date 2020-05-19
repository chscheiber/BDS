import pandas as pd
import os
import numpy as np

"""
    CoronaData stores all information concerning Corona Cases/Deaths per US State     
"""


class CoronaData:
    def __init__(self, base_dir):
        self.file_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
        self.file_name = 'us-counties.csv'
        self.base_dir = base_dir
        self.data = self.__read_data()
        self.end_date = self.__get_end_date()

    def __read_data(self):
        file_path = f"{self.base_dir}/Data/{self.file_name}"
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path, index_col=0)
            df = df.replace(np.nan, 0)

        else:
            df = pd.read_csv(self.file_url, index_col=0)
            df.to_csv(file_path)
        return df

    def __get_end_date(self):
        return self.data.iloc[-1]["date"]

    def __update_necessary(self):
        pass

    def update_data(self):
        pass

"""
b_dir = "C:/Users/chris/Documents/Studium/6 Semester/Big Data Science/BDS_Project"
cd = CoronaData(b_dir)
print(cd.end_date)"""