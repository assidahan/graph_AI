from conf_bi_anomaly import Conf


import pandas as pd
import pickle, gzip
import numpy as np
import time

if Conf.local_mode:
    import matplotlib.pyplot as plt

import warnings

class featureExtractor():
    # data_file_path = Conf.data_file_path
    break_by_columns = np.array(['col1','col2','col3','col3'])
    target_columns = ['count','sum_amount']
    all_time_axis = ['dates','dates_hours']
    target_function = 'count'

    time_axis = all_time_axis[1]
    group_by = list(break_by_columns[[0,3]])
    group_by.append(time_axis)
    # group_by.reverse()
    target_col = target_columns[0]

    def init(self, DH):
        self.data = DH.data

    def extract(self):
        self.create_time_series(flag_exist=Conf.flag_time_series_exists)


    def create_time_series(self, flag_exist,flag_plot = False):
        print(f"   -------       running in feature extrcatore .    ---------      ")
        start_time = time.time()

        if flag_exist:
            with open(Conf.time_series_path, 'rb') as handle:
                self.all_orgs_features = pickle.load(handle)
        else:
            # self.time_series_path = pd.DataFrame([])

            if self.target_function == 'count':
                data_counted = self.data[self.group_by].value_counts().unstack()
                data_counted['mean'] = data_counted.mean(axis=1)
                data_counted.sort_values(by=['mean'], ascending=False,inplace=True)
                data_counted = data_counted.transpose()
                data_counted.fillna(0,inplace=True)

                names = data_counted.index.names
                indexes = data_counted.index

                if flag_plot:
                    for i in indexes[0:7]:
                        plt.figure()
                        plt.plot(data_counted.loc[i].index,data_counted.loc[i].values,'-')
                        plt.show(block=False)

                self.time_series = data_counted

            else:
                data_summed = self.data.groupby(self.group_by)["amount"].sum().unstack(level=self.time_axis)
                names = data_summed.index.names
                indexes = data_summed.index

                if flag_plot:
                    for i in indexes[0:7]:
                        plt.figure()
                        plt.plot(data_summed.loc[i].index,data_summed.loc[i].values,'-')
                        plt.show(block=False)

                self.time_series = data_summed

                # can_get_data = False
            # if can_get_data:
            #     xx = self.data.groupby(by=self.group_by).size() # where group includes also time axis
            #
            # all_combinations = {}
            # for col in self.group_by:
            #     iter_on = self.data[col].unique()
            #     all_combinations[col] = iter_on

            # for key in all_combinations.keys():
            #     self.data.groupby(by=self.group_by)

            # xx = self.data.groupby(by=self.group_by)
            # count = 0
            # counts = []
            # # counts = pd.DataFrame([],columns=[self.group_by,'counts'])
            # for key, item in xx:
            #     a_group = xx.get_group(key)
            #     vec = list(key)
            #     vec.append(len(a_group[self.group_by]))
            #     print(vec)
            #     counts.append(vec)
            #     count += 1
            #     if count > 10:
            #         break
            # print(counts)
            # counts_frame = pd.DataFrame(counts)
            #
            # col_ = self.group_by.copy()
            # col_.append('counts')
            # counts_frame.column = col_
            # print(counts_frame[np.logical_and(counts_frame[1] == False, counts_frame[2] == 'pay')])

            if Conf.local_mode:
                with open(Conf.time_series_path, 'wb') as handle:
                    pickle.dump(self.time_series, handle)

        print(f'time for feature extractor-  : {time.time() - start_time}, ')

