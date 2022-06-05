from conf_bi_anomaly import Conf
from data_handler_abi import dataHandler
from feature_extractor import featureExtractor
from find_anomaly import findAnomaly

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import warnings


def main():
    start_time = time.time()
    print(f"  ------   running in {Conf.machine_status} mode.   ------  \n  ")

    if Conf.run_quicky:
        warnings.warn('----   notice that you are running on quicky mode   ----')

    DH = dataHandler()
    DH.create_data()

    FE = featureExtractor()
    FE.init(DH)
    FE.extract()

    FA = findAnomaly()
    FA.init(FE)
    FA.find()




if __name__ == '__main__':
    main()