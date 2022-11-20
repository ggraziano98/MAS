import logging

PICK_STRATEGY = True
UPDATE_PRICE = True
ARBITRARY_OPINION_INDEX = None

RESULT_DIR = "results/tests"

N_STEPS = 30000
N_RUNS = 1
SEED = 42

############
# Parametri mercato
############
DT = 0.01
MIN_TRADER = 5

deltap = 0.01   # cambio di prezzo
sloperange = 20 # numero di step su cui calcolare la slope
N=500; pf=10; r=0.01; R=0.001; nt0=50; p0=10

v1=1; v2=3; beta=4; Tc=1; Tf=10; a1=0.05; a2=0.5; a3=3; sigma=0.05; s=0.8

#Parameter set I:
# v1=3; v2=2; beta=6; Tc=10; Tf=5; a1=0.6; a2=0.2; a3=0.5; sigma=0.05; s=0.75
# RESULT_DIR = "results/original/parameter_set_1"

# Parameter set II:
# v1=4; v2=1; beta=4; Tc=7.5; Tf=5; a1=0.9; a2=0.25; a3=3; sigma=0.1; s=0.75
# RESULT_DIR = "results/original/parameter_set_2"

# Parameter set III:
# v1=0.5; v2=0.5; beta=2; Tc=10; Tf=10; a1=0.75; a2=0.25; a3=0.75; sigma=0.1; s=0.8
# RESULT_DIR = "results/original/parameter_set_3"

# Parameter set IV: 
# v1=2; v2=0.6; beta=4; Tc=5; Tf=5; a1=0.8; a2=0.2; a3=1; sigma=0.05; s=0.75
# RESULT_DIR = "results/original/parameter_set_4"


nf0 = N - nt0   # numero fundamentalist
tc = Tc/N       # azioni scambiate dai technical
gamma = Tf/N    # parametro influenza dei fundamentalist sull'ED

MARKET_LOG_LEVEL = logging.WARN
AGENTI_LOG_LEVEL = logging.WARN