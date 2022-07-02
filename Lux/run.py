#! python
import logging 
from datetime import datetime
from tqdm import tqdm

from model.conf import LOG_NAME_SUFFIX

GUI = False
N_STEPS = 500

if GUI:
    print('SERVER STARTING')
    from model.server import server

    server.launch()

    print('SERVER STOPPED')

else:
    from model.Market import Mercato
    
    model = Mercato()

    print("Launching without GUI")

    model.start()

    for i in tqdm(range(N_STEPS)):
        model.step()

    print("Data collected")

    model_vars_dataframe = model.datacollector.get_model_vars_dataframe()
    model_vars_dataframe.to_pickle(f"./results/Model_vars{LOG_NAME_SUFFIX}.pkl")
    agent_vars_dataframe = model.datacollector.get_agent_vars_dataframe()
    agent_vars_dataframe.to_pickle(f"./results/Agent_vars{LOG_NAME_SUFFIX}.pkl")

