from __future__ import annotations
from datetime import datetime

import random
import math
import logging

import numpy as np
from mesa import Agent
from prometheus_client import Enum

import model.Market as mk

        
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('Agenti.log', mode='w')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.info(datetime.now().strftime('%H:%M - %d/%m/%Y'))

def log_step():
    logger.debug("\n\nNEXT STEP\n\n")


class Strategies(Enum):
    Technical = 1
    Fundamentalist = 2


class Trader(Agent):
    def __init__(self, model: mk.Mercato, unique_id: int, strategy: int, *args, **kwargs):
        super().__init__(unique_id, model)
        prop_defaults = {
            "v1": 3,    # frequenza con cui un technical rivaluta la sua opinione
            "v2": 2,    # frequenza con cui un trader cambia strategia
            "a1": 0.6,    # dipendenza dalla maggioranza dei technical, < 1
            "a2": 0.2,    # dipendenza dal mercato dei technical, < 1
            "a3": 0.5,    # misura della pressione esercitata dai profitti differenziali / inerzia della reazione ai profitti differenziali
            "R" : 0.0004,  # ritorno medio dagli altri investimenti
            "r" : 0.004,  # dividendo nominale dell'asset
            "s" : 0.75,   # discount factor
            "pf": 10,     # prezzo del fundamentalist
        }
        
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.model = model
        self.opinion = random.choice([-1, +1])
        self.strategy = strategy

    def _buy(self):
        ''' place a buy order for n assets at price '''
        self.model.buy()

    def _sell(self):
        ''' place a sell order for n assets at price '''
        self.model.sell()

    def step(self):
        self.trader_logic()
        self.pick_strategy()
        if self.opinion > 0:
            self._buy()
        elif self.opinion < 0:
            self._sell()

    def pick_strategy(self):
        price_slope = self.model.priceseries.slope()

        # excess profits per unit by technical
        ept = (self.r + price_slope / self.v2) / self.model.price - self.R
        epf = self.s * abs((self.model.price - self.pf) / self.model.price)

        if self.strategy == Strategies.Fundamentalist and self.model.nf > mk.MIN_TRADER:
            trader_encoutered = 1 if random.random() < self.model.tech_optimists / self.model.nt else -1
            U = self.a3 * (trader_encoutered * ept - epf)

            p_transition = self.v2 * self.model.nf / self.model.N * math.exp(-U) * mk.DT

            if random.random() < p_transition:
                self.strategy = Strategies.Technical
                self.opinion = trader_encoutered

        elif self.strategy == Strategies.Technical and self.model.nf > mk.MIN_TRADER:
            U = self.a3 * (self.opinion * ept - epf)

            n = self.model.tech_optimists / self.model.N if self.opinion == 1 else self.model.tech_pessimists / self.model.N
            p_transition = self.v2 * n * math.exp(U) * mk.DT

            if random.random() < p_transition:
                self.strategy = Strategies.Fundamentalist
                self.trader_logic()
        
    def trader_logic(self):
        # logica technical
        if self.strategy == Strategies.Technical:
            price_slope = self.model.priceseries.slope()
            x = (self.model.tech_optimists - self.model.tech_pessimists) / self.model.nt
            U1 = self.a1 * x + self.a2 * price_slope / self.v1
            p_transition = self.v1 * (self.model.nt / self.model.N * math.exp(self.opinion * U1)) * mk.DT

            if random.random() < p_transition:
                self.opinion = self.opinion * -1

            logger.debug(f"{'Technical':15s} - ID: {self.unique_id : 4d} - Slope: {price_slope:4.2f} - x: {x:4.2f} - Transition probability: {p_transition:4.3f} - Opinion: {self.opinion}")
            
        # logica fundamentalist
        elif self.strategy == Strategies.Fundamentalist:
            self.opinion = 1 if self.pf > self.model.price else - 1
            if self.pf == self.model.price:
                self.opinion = random.choice([-1,1])
            logger.debug(f"{'Fundamentalist':15s} - ID: {self.unique_id: 4d} - Market price: {self.model.price: 4.2f} - Opinion: {self.opinion}")
        
        
