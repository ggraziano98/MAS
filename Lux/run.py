#! python
import os 
import shutil

from tqdm import tqdm
import pickle

from model.conf import RESULT_DIR, N_STEPS, N_RUNS, vars_to_export
if os.path.exists(RESULT_DIR):
    shutil.rmtree(RESULT_DIR)
os.makedirs(RESULT_DIR)

GUI = False

if GUI:
    print('SERVER STARTING')
    from model.server import server

    server.launch()

    print('SERVER STOPPED')

else:
    from model.Market import Mercato
    
    print("Launching without GUI")
    print(f"Saving results in {RESULT_DIR}")


    for n_run in range(N_RUNS):
        print("============")
        print(f"RUN = {n_run}")
        print("============")
        model = Mercato()

        model.start()
        
        for i in tqdm(range(N_STEPS)):
            model.step()

        print("Data collected")

        model_vars_dataframe = model.datacollector.get_model_vars_dataframe()
        model_vars_dataframe.to_pickle(f"{RESULT_DIR}/Model_vars_{n_run}.pkl")
        agent_vars_dataframe = model.datacollector.get_agent_vars_dataframe()
        agent_vars_dataframe.to_pickle(f"{RESULT_DIR}/Agent_vars_{n_run}.pkl")

    with open(f'{RESULT_DIR}/conf.pkl', 'wb') as f:
        pickle.dump(vars_to_export, f)