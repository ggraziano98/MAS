#! python
import os
import shutil

import matplotlib.pyplot as plt

plt.style.use('ggplot')

import pandas as pd
import numpy as np
from model.conf import N_RUNS, N_STEPS, RESULT_DIR, vars_to_export
from tqdm import tqdm
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy.stats import kurtosis
from pathlib import Path
import glob

from model.conf import RESULT_DIR, N_STEPS, N_RUNS
n_run = len(glob.glob(f'{RESULT_DIR}/run_*'))
run_dir = f'{RESULT_DIR}/run_{n_run}'
Path(run_dir).mkdir(exist_ok=True, parents=True)
os.chdir(run_dir)

GUI = False
DIRECT_SAVE = True

shutil.copy('Lux\model\conf.py',RESULT_DIR)

if GUI:
    print('SERVER STARTING')
    from model.server import server

    server.launch()

    print('SERVER STOPPED')

else:
    from model.Market import Mercato, datacollector_dict

    print("Launching without GUI")
    print(f"Saving results in {run_dir}")

    import model.conf
    shutil.copyfile(model.conf.__file__, f'conf.py')

    model_vars_df = pd.DataFrame(columns=list(datacollector_dict['model_reporters'].keys()))
    # agent_vars_dataframe = pd.DataFrame(columns=list(datacollector_dict['agent_reporters'].keys()) + ['step', 'run'])
    model_vars_df.index = pd.MultiIndex.from_arrays([[],[]], names=['run', 'step'])
    # agent_vars_dataframe.set_index(['run', 'step'])

    for n_run in range(N_RUNS):
        print("============")
        print(f"RUN = {n_run}")
        print("============")
        model = Mercato()


        model.start()
        for i in tqdm(range(N_STEPS)):
            model.step()

        df = model.datacollector.get_model_vars_dataframe()
        df.index = pd.MultiIndex.from_product([(n_run,), df.index], names=['run', 'step'])
        model_vars_df = pd.concat((model_vars_df, df))
        model_vars_df.to_csv(f"model_vars.csv")
        print("Data collected")

        if DIRECT_SAVE:
            print('Saving plots...')                
            os.mkdir(f'immagini')


            # df_list = list([pd.read_pickle(f"{RESULT_DIR}/Model_vars_{n_run}.pkl")])
            # pvalues = adfuller(list(df_list[0].loc[:,'price']))[1]
            pvalues = adfuller()[1]
            volclus = acorr_ljungbox(df.price.to_numpy() ** 2, lags = [20], return_df = True)
            volclusvalues = volclus['lb_pvalue'].values[0]
            kurtosisvalues = [kurtosis(pd.DataFrame(df.price.values[1:] - df.price.values[:-1]).rolling(timeframe, step = 2).sum()[10:])\
                             for timeframe in [20, 60, 3600]]

            fig , ax = plt.subplots(3,1, figsize=(20, 16),dpi=300)
            
            ax[0].set_title(f'Price time series')
            ax[0].set_xlabel('Step')
            ax[0].set_ylabel('Price')
            
            ax[1].set_title(f'Technical fraction time series')
            ax[1].set_xlabel('Step')
            ax[0].set_ylabel('Technical fraction')

            ax[2].set_title(f'Opinion Index time series')
            ax[2].set_xlabel('Step')
            ax[0].set_ylabel('Opinion Index')
            
            ax[0].plot(df.price, label=f'Run {i}')
            ax[1].plot(df.technical_fraction, label=f'Run {i}')
            ax[2].plot(df.opinion_index, label = f'Run {i}')
            title = f'DF-Test pvalue = {pvalues:.3f} \u21FE Unit Root: {pvalues>0.05}\n' +\
                    f'VC-Test pvalue = {volclusvalues:.3f} \u21FE Volatility Clustering:{volclusvalues<0.05} \n' +\
                    f'Kurtosis = {kurtosisvalues[0]:.3f} \u21FE Leptokurtic: {kurtosisvalues[0]>0}\n'
                    #'Kurtosis minute = ', kurtosisvalues[1].round(3),' \u21FE ','Leptokurtic:', kurtosisvalues[0]>0,'\n'
                    #'Kurtosis hour = ', kurtosisvalues[2].round(3),' \u21FE ','Leptokurtic:', kurtosisvalues[0]>0,'\n'    ]
            fig.suptitle(title,fontsize=20,color='black')
            fig.savefig(f'immagini/Plots run={n_run}.png',facecolor='white', transparent=False)
            plt.close(fig)
            print("Data printed")
    print('All done')
