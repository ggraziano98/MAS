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
from model.conf import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.WARNING)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(f'{RESULT_DIR}/Market.log', mode='w')
file_handler.setLevel(MARKET_LOG_LEVEL)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)

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

        self.datacollector = DataCollector(
            model_reporters={
                'tech_optimists' : 'tech_optimists',
                'tech_pessimists': 'tech_pessimists',
                'price'          : 'price',
                'nf'             : 'nf',
                'technical_fraction': 'technical_fraction',
                'slope': 'slope',
                'opinion_index': 'opinion_index',
            },
        )
            
        self._generate_agents()

        self.running = False

    def _generate_agents(self):
        for i in range(N):
            strategy = Strategies.Technical if i < nt0 else Strategies.Fundamentalist
            opinion = -1 if i < self.tech_pessimists else 1
            p = Trader(self, unique_id=i, strategy=strategy, opinion=opinion)
            self.schedule.add(p)
    
    def start(self):
        self.running = True

    def _update_price(self):
        edt = (self.tech_optimists - self.tech_pessimists) * tc  # excess technical demand
        edf = self.nf * gamma * (pf - self.price)
        ed = edt + edf
        mu = random.gauss(0, sigma)  # noise term
        U = beta * (ed + mu)

        p_trans = abs(U) 

        logger.debug(f"EDt: {edt:5f} - EDf: {edf: 5.2f} - ED: {ed:5.2f} - noise: {mu:5.2f} - Transition probability: {p_trans:5.3f}")

        if random.random() < p_trans:
            self.price += sign(U) * deltap

    def step(self):
        '''
        Advance the model by one step.
        '''
        logger.info(f"\n\n STEP {self.schedule.steps}\n\n")
        log_agent_step(self.schedule.steps)

        self.schedule.step()

        self.priceseries.append(self.price)
        self._update_price()

        self.datacollector.collect(self)
        logger.debug(f"NF: {self.nf:5d} - NT+: {self.tech_optimists:5d} - NT-: {self.tech_pessimists:5d} - Price: {self.price:5.2f}")

    def calculate_traders(self):
        self.tech_optimists = sum((1 for a in self.schedule.agents if a.strategy == Strategies.Technical and a.opinion == 1))
        self.tech_pessimists = sum((1 for a in self.schedule.agents if a.strategy == Strategies.Technical and a.opinion == -1))
        self.nt = self.tech_optimists + self.tech_pessimists
        self.nf = sum((1 for a in self.schedule.agents if a.strategy == Strategies.Fundamentalist))

    @property
    def technical_fraction(self):
        return self.nt / N

    @property
    def slope(self):
        return self.priceseries.slope()

    @property
    def opinion_index(self):
        return (self.tech_optimists - self.tech_pessimists) / self.nt
