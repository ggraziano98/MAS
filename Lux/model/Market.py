from __future__ import annotations

import random
import logging
import math
from typing import List, NamedTuple

from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from model.Agenti import Trader, Technical

log = logging.getLogger("MarketLog")
log.setLevel(logging.DEBUG)                                         

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
            x = (self[initial].p - self[final].p) / (final - initial)
        except IndexError as e:
            x = 0
        return x


class Mercato(Model):
    def __init__(self, nt: int, p0: float = 10, beta: float = 1/6, deltap: float = 1):

        # Set up model objects
        self.schedule = RandomActivation(self)

        self.nt = nt
        self.N = nt

        self.ts_buy, self.ts_sell = 0, 0
        self.current_price = p0

        self.beta = beta
        self.deltap = deltap

        self.priceseries = PriceSeries([Price(p=p0, bid=0, ask = 0)])

        self.datacollector = DataCollector(
            model_reporters={
                'ask'            : 'ask',
                'bid'            : 'bid',
                'tech_optimists' : 'tech_optimists',
                'tech_pessimists': 'tech_pessimists',
                'price'          : 'price'
            },
        )
            
        self.running = False

    def _generate_agents(self):
        for i in range(self.nt):
            p = Technical(self, unique_id=i, v1=1/3, a1=0.6, a2=0.2)
            self.schedule.add(p)
    
    def start(self):
        self._generate_agents()
        self.running = True

    def _update_price_history(self):
        bid     = self.ts_sell
        ask     = self.ts_buy
        p       = self.current_price

        self.priceseries.append(Price(bid=bid, ask=ask, p=p))

    def _update_price(self):
        ed = self.ts_buy - self.ts_sell  # excess demand
        mu = random.gauss(0, 5)  # noise term
        U = self.beta * (ed + mu)

        p_trans = max(0, math.exp(-abs(U)))

        log.debug(f"ED: {ed:4d} - noise: {mu:3.2f} - Transition probability: {p_trans:4.3f}")

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
        self.ts_buy, self.ts_sell = 0, 0
        self.schedule.step()

        self._update_price_history()
        self._update_price()

        self.datacollector.collect(self)

    @property
    def ask(self):
        return self.priceseries.t.ask

    @property
    def bid(self):
        return self.priceseries.t.bid
    
    @property
    def tech_optimists(self):
        return sum((1 for a in self.schedule.agents if isinstance(a, Technical) and a.opinion == 1))

    @property
    def tech_pessimists(self):
        return sum((1 for a in self.schedule.agents if isinstance(a, Technical) and a.opinion == -1))

    @property
    def price(self):
        return self.current_price

