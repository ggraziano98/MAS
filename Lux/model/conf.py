import logging
############
# Parametri mercato
############

PICK_STRATEGY = True
UPDATE_PRICE = True
ARBITRARY_OPINION_INDEX = None


N = 500
nt0 = N // 10   # numero technical
nf0 = N - nt0   # numero fundamentalist
v1 = 3          # frequenza con cui un technical rivaluta la sua opinione
v2 = 2          # frequenza con cui un trader cambia strategia
beta = 6        # frequenza di cambio prezzo
Tc = 10
tc = Tc/N       # azioni scambiate dai technical
Tf = 5
gamma = Tf/N    # parametro influenza dei fundamentalist sull'ED
a1 = 0.6        # dipendenza dalla maggioranza dei technical < 1
a2 = 0.2        # dipendenza dal mercato dei technical < 1
a3 = 0.5        # misura della pressione esercitata dai profitti differenziali / inerzia della reazione ai profitti differenziali
p0 = 10         # prezzo iniziale
pf = 10
R = 0.0004      # ritorno medio dagli altri investimenti
r = 0.004       # dividendo nominale dell'asset
s = 0.75        # discount factor

deltap = 0.01  # cambio di prezzo
sigma = 0.05  # noise sull'ED

DT = 0.01
MIN_TRADER = 5
RESULT_DIR = "results/good"

N_STEPS = 2000
N_RUNS = 30

MARKET_LOG_LEVEL = logging.WARN
AGENTI_LOG_LEVEL = logging.WARN
