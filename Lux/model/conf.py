import logging

############
# Parametri mercato
############

PICK_STRATEGY = True
UPDATE_PRICE = True
ARBITRARY_OPINION_INDEX = None


N = 500
nt0 = 10   # numero technical
nf0 = N - nt0   # numero fundamentalist
v1 = 2          # frequenza con cui un technical rivaluta la sua opinione
v2 = 3          # frequenza con cui un trader cambia strategia
beta = 6        # frequenza di cambio prezzo
Tc = 3
tc = Tc/N       # azioni scambiate dai technical
Tf = 3
gamma = Tf/N    # parametro influenza dei fundamentalist sull'ED
a1 = 0.8        # dipendenza dalla maggioranza dei technical < 1
a2 = 0.5        # dipendenza dal mercato dei technical < 1
a3 = 0.8        # misura della pressione esercitata dai profitti differenziali / inerzia della reazione ai profitti differenziali
p0 = 10.05         # prezzo iniziale
pf = 10
R = 0.04      # ritorno medio dagli altri investimenti
r = 0.12       # dividendo nominale dell'asset
s = 0.75        # discount factor

deltap = 0.01   # cambio di prezzo
sigma = 0.5    # noise sull'ED
sloperange = 20 # numero di step su cui calcolare la slope

DT = 0.01
MIN_TRADER = 5
RESULT_DIR = "results/merge"

N_STEPS = 30000
N_RUNS = 1

SEED = 42

MARKET_LOG_LEVEL = logging.WARN
AGENTI_LOG_LEVEL = logging.WARN
