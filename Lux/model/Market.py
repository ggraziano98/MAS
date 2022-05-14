from __future__ import annotations
from datetime import datetime

import random
import logging
from typing import List, NamedTuple

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from numpy import sign

from model.Agenti import Trader, Strategies, log_agent_step

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.WARNING)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('Market.log', mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)

DT = 0.01
MIN_TRADER = 5

class Price(NamedTuple):                                                        # namedtuple per facilitare la price history
    p   : float = 10
    bid : int = 0
    ask : ask = 0
    

class PriceSeries(List[Price]):
    def __init__(self, *iterable):
        super().__init__(*iterable)
    
    @property
    def t(self):
        return self[-1]
	
    def slope(self) -> float:
        ''' rapporto incrementale fra prezzo al momento final e initial '''
        try:
            x = (self[-1].p - self[-20].p) / (20 * DT)
        except IndexError as e:
            x = (self[-1].p - self[0].p) / (len(self) * DT)
        return x


class Mercato(Model):
    def __init__(self, *args, **kwargs):
        prop_defaults = {
            "Mercato": {
                "nt0": 10,       # numero technical 
                "nf0": 490,      # numero fundamentalist
                "p0": 10,       # prezzo iniziale
                "beta": 6,      # frequenza di cambio prezzo
                "gamma": 0.01,  # parametro influenza dei fundamentalist sull'ED
                "tc": 0.02,     # azioni scambiate dai chartist
                "deltap": 0.01, # cambio di prezzo
                "sigma": 0.75,  # noise sull'ED
                "pf": 10,       # prezzo del fundamentalist
            },

            "Agenti": {
                "v1": 3,      # frequenza con cui un technical rivaluta la sua opinione
                "v2": 10,      # frequenza con cui un trader cambia strategia
                "a1": 0.6,    # dipendenza dalla maggioranza dei technical, < 1
                "a2": 0.2,    # dipendenza dal mercato dei technical, < 1
                "a3": 0.5,    # misura della pressione esercitata dai profitti differenziali / inerzia della reazione ai profitti differenziali
                "R" : 0.0004, # ritorno medio dagli altri investimenti
                "r" : 0.004,  # dividendo nominale dell'asset
                "s" : 0.75,   # discount factor
                "pf": 10,     # prezzo del fundamentalist
            }
        }
        for (prop, default) in prop_defaults["Mercato"].items():
            setattr(self, prop, kwargs["Mercato"].get(prop, default))

        self.setting_agenti = kwargs.get("Agenti", prop_defaults["Agenti"])

        # Set up model objects
        self.schedule = RandomActivation(self)

        self.N = self.nt0 + self.nf0

        self.ts_buy, self.ts_sell = 0, 0
        self.price = self.p0

        self.priceseries = PriceSeries([Price(p=self.p0, bid=1, ask = 1)])

        self.datacollector = DataCollector(
            model_reporters={
                'ask'            : 'ask',
                'bid'            : 'bid',
                'tech_optimists' : 'tech_optimists',
                'tech_pessimists': 'tech_pessimists',
                'price'          : 'price',
                'nf'             : 'nf',
                'technical_fraction': 'technical_fraction',
                'slope': 'slope'
            },
        )
            
        self._generate_agents()

        self.running = False

    def _generate_agents(self):
        for i in range(self.N):
            strategy = Strategies.Technical if i < self.nt0 else Strategies.Fundamentalist
            p = Trader(self, unique_id=i, strategy=strategy, **self.setting_agenti)
            self.schedule.add(p)
    
    def start(self):
        self.running = True

    def _update_price_history(self):
        bid     = self.ts_sell
        ask     = self.ts_buy
        p       = self.price

        self.priceseries.append(Price(bid=bid, ask=ask, p=p))

    def _update_price(self):
        edt = (self.tech_optimists - self.tech_pessimists) * self.tc  # excess technical demand
        edf = self.nf * self.gamma * (self.pf - self.price)
        ed = edt + edf
        mu = random.gauss(0, self.sigma)  # noise term
        U = self.beta * (ed + mu)

        p_trans = abs(U) 

        logger.debug(f"EDt: {edt:5f} - EDf: {edf: 5.2f} - ED: {ed:5.2f} - noise: {mu:5.2f} - Transition probability: {p_trans:5.3f}")

        if random.random() < p_trans:
            self.price += sign(U) * self.deltap


    def buy(self):
        self.ts_buy += 1

    def sell(self):
        self.ts_sell += 1

    def step(self):
        '''
        Advance the model by one step.
        '''
        logger.info(f"\n\n STEP {self.schedule.steps}\n\n")
        log_agent_step(self.schedule.steps)
        self._calculate_properties()

        self.ts_buy, self.ts_sell = 0, 0
        self.schedule.step()

        self._update_price_history()
        self._update_price()

        self.datacollector.collect(self)
        logger.debug(f"NF: {self.nf:5d} - NT+: {self.tech_optimists:5d} - NT-: {self.tech_pessimists:5d} - Price: {self.price:5.2f}")

    def _calculate_properties(self):
        self.ask = self.priceseries.t.ask
        self.bid = self.priceseries.t.bid

    @property
    def tech_optimists(self):
        return sum((1 for a in self.schedule.agents if a.strategy == Strategies.Technical and a.opinion == 1))

    @property
    def tech_pessimists(self):
        return sum((1 for a in self.schedule.agents if a.strategy == Strategies.Technical and a.opinion == -1))
    
    @property
    def nt(self):
        return sum((1 for a in self.schedule.agents if a.strategy == Strategies.Technical))

    @property
    def nf(self):
        return sum((1 for a in self.schedule.agents if a.strategy == Strategies.Fundamentalist))

    @property
    def technical_fraction(self):
        return self.nt / self.N

    @property
    def slope(self):
        return self.priceseries.slope()

