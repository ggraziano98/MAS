############
# Parametri mercato
############

#### Market Population parameters
nt0 = 495       # FIXnumero chartist 
nf0 = 5       # FIXnumero fundamentalist
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
v2 = .05    # frequenza con cui un trader cambia strategia
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

#============================================
TESTNUM = 0
RESULT_DIR = "results/relazione_0"+str(TESTNUM)

N_STEPS = 30000
N_RUNS = 5
#============================================


vars_to_export = {k: v for k, v in locals().items() if not k.startswith('__')}

import logging

MARKET_LOG_LEVEL = logging.INFO
AGENTI_LOG_LEVEL = logging.INFO