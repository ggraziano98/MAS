from __future__ import annotations

import random
import math
import logging
from typing import List, Tuple

import numpy as np
from mesa import Agent

import model.Market as mk

        
log = logging.getLogger("AgentLog")
log.setLevel(logging.INFO)

class Trader(Agent):
    def __init__(self, model: mk.Mercato, unique_id: int, *args, **kwargs):
        super().__init__(unique_id, model)
        self.model = model
        self.opinion = random.choice([-1, +1])
        self.orders = []

    def trader_logic(self):
        ''' Logica dell'agente, implementata da ciascun tipo '''
        pass

    def _buy(self):
        ''' place a buy order for n assets at price '''
        self.orders.append(self.model.current_price)
        self.model.buy()

    def _sell(self):
        ''' place a sell order for n assets at price '''
        self.orders.append(-self.model.current_price)
        self.model.sell()

    def step(self, *args, **kwargs):
        self.trader_logic()
        if self.opinion > 0:
            self._buy()
        elif self.opinion < 0:
            self._sell()


class Technical(Trader):
    def __init__(self, model, unique_id: int, v1: int, a1: float, a2: float):
        super().__init__(model, unique_id)
        self.v1 = v1  # frequenza con cui l'agente rivaluta la sua opinione, intero
        self.a1 = a1  # dipendenza dalla maggioranza, < 1
        self.a2 = a2  # dipendenza dal mercato, < 1
        
    def trader_logic(self):
        price_slope = self.model.priceseries.slope(- int(1 / self.v1), -1)
        x = (self.model.priceseries.t.ask - self.model.priceseries.t.bid) / self.model.nt
        U1 = self.a1 * x + self.a2 * price_slope / self.v1
        p_transition = self.v1 * (self.model.nt / self.model.N * math.exp(self.opinion * U1))

        log.debug(f"Trader id: {self.unique_id : 4d} - Slope: {price_slope:4.2f} - x: {x:4.2f} - Transition probability: {p_transition:4.3f}")

        if random.random() < p_transition:
            self.opinion = self.opinion * -1