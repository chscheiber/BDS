import pandas as pd
import os
import numpy as np
from logzero import logger

"""
    CoronaData stores all information concerning Corona Cases/Deaths per US State     
"""


class CoronaData:
    def __init__(self, base_dir):
        self.file_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
        self.file_name = 'us-counties.csv'
        self.base_dir = base_dir
        self.file_path = f"{self.base_dir}/Data/{self.file_name}"

        # Download files if necessary
        if self.__update_necessary():
            self.data = self.download_data()
        else:
            self.data = self.__read_data()
        self.start_date = "2020-02-01"
        self.end_date = self.__get_end_date()
        self.file_size = os.stat(self.file_path).st_size


    # Download latest corona data from NY-Times GitHub Repo
    def download_data(self):
        logger.info("Downloading latest corona data...")
        df = pd.read_csv(self.file_url)
        df = df.replace(np.nan, 0)
        self.data = df
        self.end_date = df.iloc[-1]["date"]
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        df.to_csv(self.file_path)
        logger.info("Corona data updated!")
        return df

    # Load stored corona data
    def __read_data(self):
        if os.path.isfile(self.file_path):
            df = pd.read_csv(self.file_path, index_col=0)
            df = df.replace(np.nan, 0)
        else:
            df = self.download_data()
        return df

    # Get the latest date for which corona data is stored
    def __get_end_date(self):
        return self.data.iloc[-1]["date"]

    def __update_necessary(self):
        return True

"""
b_dir = "C:/Users/chris/Documents/Studium/6 Semester/Big Data Science/BDS_Project"
cd = CoronaData(b_dir)
print(cd.end_date)"""