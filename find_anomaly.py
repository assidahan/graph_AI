import random

from conf_bi_anomaly import Conf


import pandas as pd
import pickle, gzip
import time
import numpy as np

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import seaborn as sns
import random

if Conf.local_mode:
    import matplotlib.pyplot as plt

import warnings

class findAnomaly():
    # data_file_path = Conf.data_file_path

    def init(self, FE):
        self.time_series = FE.time_series

    def find(self):
        self.run_on_graphs(flag_exist=False)

    def run_on_graphs(self, flag_exist=False,flag_plot=False):
        print(f"   -------       running in anomaly on graphs .    ---------      ")
        start_time = time.time()
        if flag_exist:
            with open(Conf.data_features_path, 'rb') as handle:
                self.all_features = pickle.load(handle)
        else:

            time_series = self.time_series

            names = time_series.index.names
            indexes = time_series.index
            # ind = range(5000,8000)
            ind = range(len(time_series))
            flag_inset_anomaly = True

            for col in time_series.columns[0:4]:
                original_vec = time_series[col].values[ind]
                vec = original_vec.copy()

                if flag_inset_anomaly:
                    num_anomalies = int(random.random()*5)+1
                    for i in range(num_anomalies):
                        ind_anomaly_start = int(random.random()*len(ind))
                        len_anomaly = int(random.random()*10)
                        indexes_anomaly = range(ind_anomaly_start,min(ind_anomaly_start+len_anomaly,len(ind)))
                        size_anomaly = (2*random.random()-1)*time_series[col]['mean']*5
                        vec[indexes_anomaly] = vec[indexes_anomaly]+size_anomaly

                if flag_plot:
                    plt.figure()
                    plt.plot(vec)
                    plt.title(col)
                    # plt.grid()
                    # plt.xticks(rotation=60)
                    plt.show(block=False)

                plt.rc('figure', figsize=(12, 8))
                plt.rc('font', size=15)
                result = seasonal_decompose(vec, period=1000, model='additive')
                resudial = result.resid
                anomaly_ind = np.where(resudial > 2*np.std(time_series[col]))

                fig = result.plot()
                fig = plt.gcf()
                fig.set_size_inches(18.5, 10.5)

                plt.figure()
                plt.subplot(3,1,1)
                plt.plot(vec)
                plt.plot(original_vec)
                plt.title('')
                plt.grid()

                plt.subplot(3,1,2)
                plt.plot(vec- original_vec)
                plt.title('')
                plt.grid()

                plt.subplot(3,1,3)
                plt.plot(resudial)
                plt.plot(anomaly_ind,0,'*r')
                plt.title('')
                plt.grid()
                fig = plt.gcf()
                fig.set_size_inches(18.5, 10.5)
                plt.show(block=False)


                # define model configuration
                my_order = (1, 1, 1)
                my_seasonal_order = (1, 1, 1, 12)
                # define model
                # model = SARIMAX(vec, order=my_order, seasonal_order=my_seasonal_order, ...)



            if Conf.local_mode:
                with open(Conf.data_features_path, 'wb') as handle:
                    pickle.dump(self.features, handle)

        print(f'time for feature extractor-  : {time.time() - start_time}, ')
