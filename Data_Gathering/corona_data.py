import pandas as pd
import numpy as np

"""
    CoronaData stores all information concerning Corona Cases/Deaths
    Returns:
        {
        Infections: {
            total_data_usa: Total Data for USA,
            east_data_usa: Data for USA WEST,
            west_data_usa: Data for USA EAST,
            }
            
        Deaths: {
            total_deaths_usa: Total Deaths USA,
            east_deaths_usa: Deaths USA WEST,
            west_deaths_usa: Deaths USA EAST,
            }
        }              
"""


class CoronaData:
    def __init__(self):
        self.filename_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
                               'csse_covid_19_time_series/time_series_covid19_deaths_US.csv '
        self.filename_infections = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master' \
                                   '/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv '

        # TODO: Change *_deaths_* to *_data_*
        self.infections = {
            "total_data_usa": None,
            "east_data_usa": None,
            "west_data_usa": None,
        }
        self.deaths = {
            "total_deaths_usa": None,
            "east_deaths_usa": None,
            "west_deaths_usa": None,
        }

        self.__read_data()

    def __read_data(self):
        # read the data
        timeseriesUSA = pd.read_csv(self.filename_deaths)
        timeseriesUSA = timeseriesUSA.drop(timeseriesUSA.columns[[i for i in range(12)]], axis=1)
        self.deaths['east_deaths_usa'] = timeseriesUSA[:int(timeseriesUSA.shape[0] / 2)].sum().transpose().to_frame()
        self.deaths['west_deaths_usa'] = timeseriesUSA[int(timeseriesUSA.shape[0] / 2):].sum().transpose().to_frame()
        self.deaths['total_deaths_usa'] = timeseriesUSA.sum().transpose().to_frame()
        self.deaths['total_deaths_usa'].columns = ['deaths']
        self.deaths['east_deaths_usa'].columns = ['deaths']
        self.deaths['west_deaths_usa'].columns = ['deaths']

        timeseriesUSA = pd.read_csv(self.filename_infections)
        timeseriesUSA = timeseriesUSA.drop(timeseriesUSA.columns[[i for i in range(11)]], axis=1)
        east_infections_usa = timeseriesUSA[:int(timeseriesUSA.shape[0] / 2)].sum().transpose().to_frame()
        west_infections_usa = timeseriesUSA[int(timeseriesUSA.shape[0] / 2):].sum().transpose().to_frame()
        total_infections_usa = timeseriesUSA.sum().transpose().to_frame()
        total_infections_usa.columns = ['infections']
        east_infections_usa.columns = ['infections']
        west_infections_usa.columns = ['infections']

        self.infections['total_data_usa'] = pd.concat([total_infections_usa, self.deaths['total_deaths_usa']], axis=1)
        self.infections['east_data_usa'] = pd.concat([east_infections_usa, self.deaths['east_deaths_usa']], axis=1)
        self.infections['west_data_usa'] = pd.concat([west_infections_usa, self.deaths['west_deaths_usa']], axis=1)

        self.infections['total_data_usa']['sentiment'] = pd.Series(np.zeros(self.infections['total_data_usa'].shape[0]),
                                                                   index=self.infections['total_data_usa'].index)
        self.infections['east_data_usa']['sentiment'] = pd.Series(np.zeros(self.infections['east_data_usa'].shape[0]),
                                                                  index=self.infections['east_data_usa'].index)
        self.infections['west_data_usa']['sentiment'] = pd.Series(np.zeros(self.infections['west_data_usa'].shape[0]),
                                                                  index=self.infections['west_data_usa'].index)
        # dates = self.infections.total_data_usa.index.values.tolist()

    def get_corona_data(self):
        return {
            "infections": self.infections,
            "deaths": self.deaths
        }


tmp = {}
cd = CoronaData().get_corona_data()
for key, df in cd["deaths"].items():
    tmp_row = {}
    for index, row in df.iterrows():
        tmp_row[index] = dict(row)
    tmp[key] = tmp_row
response = tmp

