import logging

PICK_STRATEGY = True
UPDATE_PRICE = True
ARBITRARY_OPINION_INDEX = None

RESULT_DIR = "results/tests"

N_STEPS = 30000
N_RUNS = 1
SEED = 42

#simulation parameters 
DT = 0.01
MIN_TRADER = 5
deltap = 0.0001     # cambio di prezzo
sloperange = 20     # numero di step su cui calcolare la slope

#market initialization;     fundamental price 
N=500; nt0=450; p0=10;      pf = 10

#excess demand parameters
beta = 6; Tc=3; Tf=3; sigma=2; 

#strategy change parameters
v2=.05; a3=.8; r=0.12; R=0.04; s=0.75

#technical opinion parameters
v1=1; a1=0.8; a2=0.5; 

RESULT_DIR = "results/original/parameter_set_1"


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