from __future__ import annotations
from datetime import datetime

import random
import logging
import math
from typing import List, NamedTuple

from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from model.Agenti import Trader, Strategies, log_step

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)            

file_handler = logging.FileHandler('Market.log', mode='w')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.info(datetime.now().strftime('%H:%M - %d/%m/%Y'))

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
	
    def slope(self, initial: int, final: int) -> float:
        ''' rapporto incrementale fra prezzo al momento final e initial '''
        try:
            x = (self[final].p - self[initial].p) / (final - initial)
        except IndexError as e:
            x = 0
        return x


class Mercato(Model):
    def __init__(self, nt: int, nf: int, p0: float = 10, beta: float = 1/6, gamma: float = 0.01, deltap: float = 1):

        # Set up model objects
        self.schedule = RandomActivation(self)

        self.N = nt + nf

        self.ts_buy, self.ts_sell = 0, 0
        self.current_price = p0
        self.pf = p0

        self.beta = beta
        self.gamma = gamma
        self.deltap = deltap

        self.priceseries = PriceSeries([Price(p=p0, bid=0, ask = 0)])

        self.datacollector = DataCollector(
            model_reporters={
                'ask'            : 'ask',
                'bid'            : 'bid',
                'tech_optimists' : 'tech_optimists',
                'tech_pessimists': 'tech_pessimists',
                'price'          : 'price',
                'nf'             : 'nf',
                'technical_fraction': 'technical_fraction'
            },
        )
            
        self._generate_agents(nt=nt, nf=nf)

        self.running = False

    def _generate_agents(self, nt, nf):
        for i in range(self.N):
            strategy = Strategies.Technical if i < nt else Strategies.Fundamentalist
            p = Trader(self, unique_id=i, strategy=strategy)
            self.schedule.add(p)
    
    def start(self):
        self.running = True

    def _update_price_history(self):
        bid     = self.ts_sell
        ask     = self.ts_buy
        p       = self.current_price

        self.priceseries.append(Price(bid=bid, ask=ask, p=p))

    def _update_price(self):
        edt = self.tech_optimists - self.tech_pessimists  # excess technical demand
        edf = self.nf * self.gamma * (self.pf - self.price)
        ed = edt + edf
        mu = random.gauss(0, 5)  # noise term
        U = self.beta * (ed + mu)

        p_trans = max(0, abs(U))

        logger.debug(f"EDt: {edt:5d} - EDf: {edf: 5.2f} - ED: {ed:5.2f} - noise: {mu:5.2f} - Transition probability: {p_trans:5.3f}")

        if random.random() < p_trans:
            self.current_price += U / abs(U) * self.deltap


    def buy(self):
        self.ts_buy += 1

    def sell(self):
        self.ts_sell += 1

    def step(self):
        '''
        Advance the model by one step.
        '''
        log_step()
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
        self.tech_optimists = sum((1 for a in self.schedule.agents if a.strategy == Strategies.Technical and a.opinion == 1))
        self.tech_pessimists = sum((1 for a in self.schedule.agents if a.strategy == Strategies.Technical and a.opinion == -1))
        self.nt = sum((1 for a in self.schedule.agents if a.strategy == Strategies.Technical))
        self.nf = sum((1 for a in self.schedule.agents if a.strategy == Strategies.Fundamentalist))
        self.technical_fraction = self.nt / self.N

    @property
    def price(self):
        return self.current_price

