#! python
import os
import shutil

from tqdm import tqdm
from pathlib import Path
import glob
import pandas as pd

from model.conf import RESULT_DIR, N_STEPS, N_RUNS
n_run = len(glob.glob(f'{RESULT_DIR}/run_*'))
run_dir = f'{RESULT_DIR}/run_{n_run}'
Path(run_dir).mkdir(exist_ok=True, parents=True)
os.chdir(run_dir)

GUI = False

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

    model_vars_dataframe = pd.DataFrame(columns=list(datacollector_dict['model_reporters'].keys()))
    # agent_vars_dataframe = pd.DataFrame(columns=list(datacollector_dict['agent_reporters'].keys()) + ['step', 'run'])
    model_vars_dataframe.index = pd.MultiIndex.from_arrays([[],[]], names=['run', 'step'])
    # agent_vars_dataframe.set_index(['run', 'step'])

    for n_run in range(N_RUNS):
        print("============")
        print(f"RUN = {n_run}")
        print("============")
        model = Mercato()


        model.start()
        for i in tqdm(range(N_STEPS)):
            model.step()

        new_model_data = model.datacollector.get_model_vars_dataframe()
        new_model_data.index = pd.MultiIndex.from_product([(n_run,), new_model_data.index], names=['run', 'step'])
        model_vars_dataframe = pd.concat((model_vars_dataframe, new_model_data))
        model_vars_dataframe.to_csv(f"model_vars.csv")

        # new_agent_data = model.datacollector.get_agent_vars_dataframe()
        # new_agent_data.index = pd.MultiIndex.from_product([(n_run,), new_agent_data.index], names=['run', 'step'])
        # new_agent_data = pd.concat((agent_vars_dataframe, new_agent_data))
        # new_agent_data.to_csv(f"agent_vars.csv")
        print("Data collected")

