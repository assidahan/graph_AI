import pickle

import os
from datetime import date, timedelta, datetime

class Conf():

    model_version = 'v0'
    # machine_status = 'learn'
    machine_status = 'prediction'

    flag_skip_data = False
    local_mode = True
    start_date = ''

    ml_model_type = 'cat_boost'
    # ml_model_type = 'gradient_boosting'

    ## input params

    hours_backward = None
    default_hours_backward = 36
    day_history = 34

    ## output params
    now = None
    now_date = None
    now_month = None

    flag_prediction_past = True

    run_quicky = True
    quicky_fract = 0.4

    directory = os.getcwd() + "/"

    orgs_accumulate_file_path_learn = directory + 'data/xx.pkl'
    time_series_path_prediction = directory + 'data/time_series_prediction.pkl'

    flag_clean_problematic_account = True and machine_status == 'learn'
    debug_level = 1
    # FLAGS FOR DATA:
    flag_new_data = 1       # or force_new_data
    flag_exist_lon_lat = True
    flag_exist_all_data = (True and not flag_new_data) and local_mode

    flag_learn_read_data = 1 and flag_exist_all_data
    flag_time_series_exists_leran =            1  and flag_exist_all_data and flag_learn_read_data

    flag_predict_read_data = 1 and flag_exist_all_data
    flag_time_series_exists_prediction =    0 and flag_exist_all_data and flag_predict_read_data

    if machine_status == 'learn':
        pass
    else:
        flag_read_data_exist = True
        flag_time_series_exists = flag_time_series_exists_prediction
        time_series_path = time_series_path_prediction

    plots_folder = directory + 'results/plots/'


    ######################


    None_val = -101010
    label_col = ''
    hyper_method = 'biasian'
    num_baisian_points = 1000
    fract_score_recall_prec = 1


    trained_model_biasian_path = directory + "xx"+model_version+"_"+ml_model_type+".pickle.dat"
    trained_param_biasian_path = directory + "x"+model_version+"_"+ml_model_type+".pickle.dat"

    # trained_run_type_biasian_path = directory  + "trained_run_type_biasian_"+model_version+"_"+ml_model_type+".pkl"

    # param_table_file_path = directory +'data/' + ""+model_version+"_"+ml_model_type+".pkl"
    # fall_param_table_file_path = directory +'data/'
    # param_table_CV_file_path = directory +'data/'

    features_columns = ['']



