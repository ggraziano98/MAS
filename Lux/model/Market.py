from __future__ import annotations

import random
import logging
from typing import List
from enum import Enum

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np

from model.Agenti import Trader, log_agent_step
from model.conf import *

logger = logging.getLogger(__name__)
logger.setLevel(MARKET_LOG_LEVEL)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.WARNING)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(f'Market.log', mode='w')
file_handler.setLevel(MARKET_LOG_LEVEL)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)

datacollector_dict = {
    'model_reporters':{
        'tech_optimists': 'tech_optimists',
        'tech_pessimists': 'tech_pessimists',
        'price': 'price',
        'nf': 'nf',
        'technical_fraction': 'technical_fraction',
        'slope': 'slope',
        'opinion_index': 'opinion_index',
        'edt': 'edt',
        'edf': 'edf',
        'ed': 'ed',
        'ept': 'ept',
        'epf': 'epf',
        'U_strategy': 'U_strategy',
        'p_trans_strategy': 'p_trans_strategy',
    },
    'agent_reporters': {},
    'tables': {}
}

class Strategy(Enum):
    Tech_O = 1
    Tech_P = -1
    Fundam = 0

class PriceSeries(List[float]):
    def __init__(self, *iterable):
        super().__init__(*iterable)

    def slope(self) -> float:
        try:
            x = (self[-1] - self[-20]) / (20 * DT)
        except IndexError as e:
            x = (self[-1] - self[0]) / (len(self) * DT)
        return x


class Mercato(Model):
    def __init__(self):
        # Set up model objects
        self.schedule = RandomActivation(self)

        self.nf = nf0
        self.tech_optimists = nt0 // 2
        self.tech_pessimists = nt0 - self.tech_optimists
        self.nt = nt0

        self.price = p0
        self.priceseries = PriceSeries([p0])
        self.slope = 0
        self.opinion_index = 0

        self.datacollector = DataCollector(**datacollector_dict)

        self._generate_agents()

        self.running = False

    def _generate_agents(self):
        for i in range(N):
            strategy = random.choice([Strategy.Tech_O, Strategy.Tech_P]) if i < nt0 else Strategy.Fundam
            p = Trader(self, unique_id=i, strategy=strategy)
            self.schedule.add(p)

    def start(self):
        self.running = True

    def _update_price(self):
        mu = random.gauss(0, sigma)  # noise term
        U = beta * (self.ed + mu)

        p_trans = abs(U)

        logger.debug(f"EDt: {self.edt:5f} - EDf: {self.edf: 5.2f} - ED: {self.ed:5.2f} - noise: {mu:5.2f} - Transition probability: {p_trans:5.3f}")
        

        if random.random() < p_trans:
            self.price += np.sign(U) * deltap

    def step(self):
        '''
        Advance the model by one step.
        '''
        logger.info(f"\n\n STEP {self.schedule.steps}\n\n")
        log_agent_step(self.schedule.steps)

        self.slope = self.priceseries.slope()

        logger.debug(f'Excess profits: ept: {self.ept:.4f}  -  epf: {self.epf:.4f}')

        self.schedule.step()

        self.priceseries.append(self.price)
        if UPDATE_PRICE:
            self._update_price()

        self.datacollector.collect(self)
        logger.debug(f"NF: {self.nf:5d} - NT+: {self.tech_optimists:5d} - NT-: {self.tech_pessimists:5d} - Price: {self.price:5.2f}")

    def switch(self, old: Strategy, new: Strategy):
        self.add_to_traders(old, -1)
        self.add_to_traders(new, +1)
        self.nt = self.tech_optimists + self.tech_pessimists
        self.opinion_index = ARBITRARY_OPINION_INDEX or (self.tech_optimists - self.tech_pessimists) / self.nt

    def get_n_traders(self, strategy: Strategy):
        return self.nf if strategy == Strategy.Fundam else \
                    self.tech_optimists if strategy == Strategy.Tech_O else \
                        self.tech_pessimists
                    
    def add_to_traders(self, strategy: Strategy, add: int):
        if strategy == Strategy.Fundam:
            self.nf += add
        elif strategy == Strategy.Tech_O:
            self.tech_optimists += add
        else:
            self.tech_pessimists += add

    @property
    def technical_fraction(self):
        return self.nt / N

    @property
    def ept(self):
        return (r + self.slope / v2) / self.price - R

    @property
    def epf(self):
        return s * abs((self.price - pf) / self.price)
    
    @property
    def U_strategy(self):
        return a3 * (self.ept - self.epf)
    
    @property
    def p_trans_strategy(self):
        return Trader.calc_p_transition(v2, self.U_strategy, self.tech_optimists)

    @property
    def edt(self):
        return (self.tech_optimists - self.tech_pessimists) * tc

    @property
    def edf(self):
        return self.nf * gamma * (pf - self.price)

    @property
    def ed(self):
        return self.edt + self.edf