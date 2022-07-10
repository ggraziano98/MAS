############
# Parametri mercato
############

nt0 = 20       # numero technical 
nf0 = 180      # numero fundamentalist
p0 = 10       # prezzo iniziale
beta = 4      # frequenza di cambio prezzo
gamma = 0.01  # parametro influenza dei fundamentalist sull'ED
deltap = 0.01 # cambio di prezzo
sigma = 0.05  # noise sull'ED

############
# Parametri trader 
############

# Parametri cambio strategia
v2 = 0.6      # frequenza con cui un trader cambia strategia
R  = 0.0004 # ritorno medio dagli altri investimenti
r  = 0.004  # dividendo nominale dell'asset
s  = 0.75   # discount factor

# Parametri logica technical
tc = 0.01     # azioni scambiate dai technical
v1 = 2      # frequenza con cui un technical rivaluta la sua opinione
a1 = 0.8    # dipendenza dalla maggioranza dei technical < 1
a2 = 0.2    # dipendenza dal mercato dei technical < 1

# Parametri logica fundamentalist
pf = 10       # prezzo del fundamentalist
a3 = 1    # misura della pressione esercitata dai profitti differenziali / inerzia della reazione ai profitti differenziali

N = nf0 + nt0

DT = 0.01
MIN_TRADER = 5
RESULT_DIR = "results/parameter set 4"

N_STEPS = 2000
N_RUNS = 15

vars_to_export = {k: v for k, v in locals().items() if not k.startswith('__')}

import logging
MARKET_LOG_LEVEL = logging.INFO
AGENTI_LOG_LEVEL = logging.INFO