import logging

############
# Parametri mercato
############

PICK_STRATEGY = True
UPDATE_PRICE = True
ARBITRARY_OPINION_INDEX = None


N = 500
nt0 = 30   # numero technical
nf0 = N - nt0   # numero fundamentalist
v1 = 0.5          # frequenza con cui un technical rivaluta la sua opinione
v2 = 1          # frequenza con cui un trader cambia strategia
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

deltap = 0.0001   # cambio di prezzo
sigma = 2    # noise sull'ED
sloperange = 20 # numero di step su cui calcolare la slope

DT = 0.01
MIN_TRADER = 5
RESULT_DIR = "results/merge"

N_STEPS = 1000
N_RUNS = 1

SEED = 42

MARKET_LOG_LEVEL = logging.WARN
AGENTI_LOG_LEVEL = logging.WARN

#############
# Marco 
#############

############
# Parametri mercato
############

#### Market Population parameters
nt0 = 495       # FIXnumero chartist 
nf0 = 5       # FIXtenumero fundamentalist
N = nf0 + nt0
Tc = 3;         tc = Tc/N     # excess demand chartist influence
Tf = 3;         gamma = Tf/N  # excess demand fundamentalist influence 

#### Market regulation parameters
p0 = 12         # initial price
beta = 6        # price change frequency
deltap = 0.0001 # FIXprice change
sigma = 2       # FIXexcess demand noise traders

###############################################################################

############
# Parametri trader 
############

# Parametri cambio strategia
v2 = .05      # frequenza con cui un trader cambia strategia
R  = .04    # ritorno medio dagli altri investimenti 0.0004
r  = .12    # dividendo nominale dell'asset 0.004
s  = 0.75   # discount factor

# Parametri logica technical
v1 = 1      # frequenza con cui un technical rivaluta la sua opinione
a1 = .8     # peso decisionale dell'opinione media < 1
a2 = .5     # peso decisionale della price slope < 1
sloperange = 20

# Parametri logica fundamentalist
pf = 11     # fundamental price
a3 = .8     # inerzia alla reazione sui profitti differenziali 

DT = .01    # FIX 
MIN_TRADER = 5
