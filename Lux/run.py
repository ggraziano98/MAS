#! python
import os
import pickle
import shutil

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from model.conf import N_RUNS, N_STEPS, RESULT_DIR, vars_to_export
from tqdm import tqdm
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy.stats import kurtosis

if os.path.exists(RESULT_DIR):
    shutil.rmtree(RESULT_DIR)
os.makedirs(RESULT_DIR)

GUI = False
DIRECT_SAVE = True

shutil.copy('Lux\model\conf.py',RESULT_DIR)

if GUI:
    print('SERVER STARTING')
    from model.server import server

    server.launch()

    print('SERVER STOPPED')

else:
    from model.Market import Mercato
    
    print("Launching without GUI")
    print(f"Saving results in {RESULT_DIR}")

    with open(f'{RESULT_DIR}/conf.pkl', 'wb') as f:
        pickle.dump(vars_to_export, f)

    for n_run in range(N_RUNS):
        print("============")
        print(f"RUN = {n_run}")
        print("============")
        model = Mercato()

        model.start()
        
        for i in tqdm(range(N_STEPS)):
            model.step()

        model_vars_dataframe = model.datacollector.get_model_vars_dataframe()
        model_vars_dataframe.to_pickle(f"{RESULT_DIR}/Model_vars_{n_run}.pkl")
        agent_vars_dataframe = model.datacollector.get_agent_vars_dataframe()
        agent_vars_dataframe.to_pickle(f"{RESULT_DIR}/Agent_vars_{n_run}.pkl")

        print("Data collected, printing data...")

        if DIRECT_SAVE:
            
            plt.style.use('ggplot')

            with open(f'{RESULT_DIR}/conf.pkl', 'rb') as f:
                CONST = pickle.load(f)
                
            if not os.path.exists(RESULT_DIR + '/immagini'):
                os.mkdir(f'{RESULT_DIR}/immagini')

            df_list = list([pd.read_pickle(f"{RESULT_DIR}/Model_vars_{n_run}.pkl")])
            pvalues = adfuller(list(df_list[0].loc[:,'price']))[1]
            volclus = acorr_ljungbox(np.array(df_list[0].loc[:,'price'])**2, lags = [20], return_df = True)
            volclusvalues = volclus['lb_pvalue'].values[0]
            kurtosisvalues = [kurtosis(pd.DataFrame(df_list[0]['price'].values[1:] - df_list[0]['price'].values[:-1]).rolling(timeframe, step = 2).sum()[10:])\
                             for timeframe in [20, 60, 3600]]

            fig , ax = plt.subplots(3,1, figsize=(20, 16),dpi=300)
            ax[0].set_xlabel(f'Price time series')
            ax[1].set_xlabel(f'Technical fraction')
            ax[2].set_xlabel(f'Opinion Index')
            ax[0].plot(df_list[0].price, label=f'Run {i}')
            ax[1].plot(df_list[0].technical_fraction, label=f'Run {i}')
            ax[2].plot(df_list[0].opinion_index, label = f'Run {i}')
            title = ['DF-Test pvalue = ', round(pvalues,3), ' \u21FE ','Unit Root:', pvalues>0.05,'\n'
                    'VC-Test pvalue = ', round(volclusvalues,3), ' \u21FE ','Volatility Clustering:', volclusvalues<0.05,'\n' 
                    'Kurtosis = ', kurtosisvalues[0].round(3),' \u21FE ','Leptokurtic:', kurtosisvalues[0]>0,'\n']
                    #'Kurtosis minute = ', kurtosisvalues[1].round(3),' \u21FE ','Leptokurtic:', kurtosisvalues[0]>0,'\n'
                    #'Kurtosis hour = ', kurtosisvalues[2].round(3),' \u21FE ','Leptokurtic:', kurtosisvalues[0]>0,'\n'    ]
            title = ' '.join(str(e) for e in title)
            fig.suptitle(title,fontsize=20,color='black')
            fig.savefig(f'{RESULT_DIR}/immagini/Price and technical fraction over time run={n_run}',facecolor='white', transparent=False)
            plt.close(fig)
        
            print("Data printed")
