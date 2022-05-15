nt0 = 20       # numero technical 
nf0 = 180      # numero fundamentalist
p0 = 10       # prezzo iniziale
beta = 6      # frequenza di cambio prezzo
gamma = 0.01  # parametro influenza dei fundamentalist sull'ED
tc = 0.02     # azioni scambiate dai chartist
deltap = 0.01 # cambio di prezzo
sigma = 0.5  # noise sull'ED
pf = 10       # prezzo del fundamentalist
v1 = 3      # frequenza con cui un technical rivaluta la sua opinione
v2 = 2      # frequenza con cui un trader cambia strategia
a1 = 0.6    # dipendenza dalla maggioranza dei technical < 1
a2 = 0.2    # dipendenza dal mercato dei technical < 1
a3 = 0.5    # misura della pressione esercitata dai profitti differenziali / inerzia della reazione ai profitti differenziali
R  = 0.0004 # ritorno medio dagli altri investimenti
r  = 0.004  # dividendo nominale dell'asset
s  = 0.75   # discount factor

N = nf0 + nt0

DT = 0.01
MIN_TRADER = 10