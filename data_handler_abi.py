from conf_bi_anomaly import Conf


import time
import pandas as pd
import warnings
from datetime import datetime


class dataHandler():
    queries = None
    data_file_path = Conf.directory + 'data/' + Conf.machine_status + '_data.pkl'

    data_file_path_long = Conf.directory + 'samples_data/p_and_org_long.pkl'
    data_file_path = Conf.directory + 'samples_data/p_and_org.pkl'

    def init_times(self):
        now = datetime.now()
        Conf.now = datetime.now()
        Conf.now_date = now.strftime('%Y-%m-%d %H-%M')
        Conf.now_month = now.strftime('%Y-%m')

    def create_data(self):
        start_time = time.time()
        self.init_times()
        self.create_queries(query_create=['q_data'])
        self.read_data()
        print(f' time took to collect all data- {time.time() - start_time} seconds.')

    def read_table(self, path_file, flag_exist, query, db='analytics', query_source=''):
        if flag_exist:
            data = pd.read_pickle(path_file)
        else:
            print('database call query from: ' + query_source)
            if db == 'analy':
                if Conf.local_mode:
                    print(query)
                else:
                    print(query[0:200] + '.............\n reading data.......')
                data = self.read_data(query)
                data.columns = [x.lower() for x in data.columns]

            if Conf.local_mode:
                data.to_pickle(path_file)
        return data

    def read_data(self):
        if Conf.flag_read_data_exist:
            flag_shorten_data = True
            if flag_shorten_data:
                self.data = pd.read_pickle(self.data_file_path_long)
                self.data = self.data.sort_values('CREATEDAT')
                self.data = self.data[0:1000000]
                self.data.to_pickle(self.data_file_path)
            else:
                self.data = pd.read_pickle(self.data_file_path)

            self.data.columns = [x.lower() for x in self.data.columns]
            self.data['dates'] = pd.to_datetime(self.data.createdat).dt.date
            self.data['dates_hours'] = pd.to_datetime(self.data.createdat).dt.strftime('%m:%d:%Y %H')

        else:
            self.data = self.read_table(path_file=self.data_file_path,
                                                     flag_exist=Conf.flag_read_data_exist,
                                                     query=self.queries['q_datas'],
                                                     query_source='datas')
            self.edit_data()

        if Conf.debug_level >= 1:
            pass


    def edit_data(self):
        if Conf.machine_status == 'prediction':
            pass
        else:
            pass

        if Conf.local_mode:
            self.datas.to_pickle(self.data_file_path)


    def create_queries(self, query_create=None, data_dict=None):
        if self.queries is None:
            self.queries = {}

        if 'q_payments' in query_create:
            if Conf.machine_status == 'learn':
                q_population = '''   

'''
            # q_population = q_population.format()

            if Conf.machine_status == 'prediction':
                q_population = '''

                '''
                q_population = q_population.format(Conf.hours_backward, Conf.limit_amount_payments_checked)

            q_data = '''
             '''
            # q_data = q_data.format(Conf.day_history)

            q_datas = q_population + q_data
            self.queries['q_payments'] = q_datas



