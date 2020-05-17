import pandas as pd
import numpy as np

"""
    CoronaData stores all information concerning Corona Cases/Deaths per US State     
"""


class CoronaData:
    def __init__(self):
        self.file_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'

    def read_data(self):
        df = pd.read_csv(self.file_url)
        return df
