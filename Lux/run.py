#! python
import logging 
from datetime import datetime
from tqdm import tqdm

GUI = False
N_STEPS = 5000

parameters = {
    "Mercato": {
        "nt0": 10,       # numero technical 
        "nf0": 490,      # numero fundamentalist
        "p0": 10,       # prezzo iniziale
        "beta": 6,      # frequenza di cambio prezzo
        "gamma": 0.01,  # parametro influenza dei fundamentalist sull'ED
        "tc": 0.02,     # azioni scambiate dai chartist
        "deltap": 0.01, # cambio di prezzo
        "sigma": 0.25,  # noise sull'ED
        "pf": 10,       # prezzo del fundamentalist
    },

    "Agenti": {
        "v1": 3,      # frequenza con cui un technical rivaluta la sua opinione
        "v2": 10,      # frequenza con cui un trader cambia strategia
        "a1": 0.6,    # dipendenza dalla maggioranza dei technical, < 1
        "a2": 0.2,    # dipendenza dal mercato dei technical, < 1
        "a3": 2,    # misura della pressione esercitata dai profitti differenziali / inerzia della reazione ai profitti differenziali
        "R" : 0.0004, # ritorno medio dagli altri investimenti
        "r" : 0.004,  # dividendo nominale dell'asset
        "s" : 0.75,   # discount factor
        "pf": 10,     # prezzo del fundamentalist
    }
}

if GUI:
    print('SERVER STARTING')
    from model.server import server

    server.launch()

    print('SERVER STOPPED')

else:
    from model.Market import Mercato
    
    model = Mercato(**parameters)

    print("Launching without GUI")

    model.start()

    for i in tqdm(range(N_STEPS)):
        model.step()

    print("Data collected")

    model_vars_dataframe = model.datacollector.get_model_vars_dataframe()
    model_vars_dataframe.to_pickle(f"Model_vars.pkl")
    agent_vars_dataframe = model.datacollector.get_agent_vars_dataframe()
    agent_vars_dataframe.to_pickle(f"Agent_vars.pkl")

