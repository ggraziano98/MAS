from __future__ import annotations

import random
import math
import logging

from mesa import Agent

import model.Market as mk
from model.conf import *

from functools import lru_cache

logger = logging.getLogger(__name__)
logger.setLevel(AGENTI_LOG_LEVEL)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.WARNING)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(f'Agenti.log', mode='w')
file_handler.setLevel(AGENTI_LOG_LEVEL)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)


def log_agent_step(i):
    logger.info(f"\n\nSTEP {i}\n\n")

class Trader(Agent):
    def __init__(self, model: mk.Mercato, unique_id: int, strategy: mk.Strategy):
        super().__init__(unique_id, model)
        self.model = model
        self.strategy = strategy

    def step(self):
        self.pick_strategy()

    def _calc_transition_matrix(self, encountered: mk.Strategy):
        '''Calculate transition matrix given the encountered trader'''
        n = self.model.get_n_traders(encountered)
        # basta controllare se uno è zero per vedere se sono di strategie diverse
        if self.strategy.value * encountered.value == 0:
            if not PICK_STRATEGY:
                return 0, 0
            tech_factor_coeff = self.strategy.value or encountered.value # always 1 or -1
            U = Trader.calc_U_strategy(self.model.price, self.model.slope, tech_factor_coeff)
            freq = v2
            U = abs(encountered.value) - abs(self.strategy.value) * U # +- U a seconda di che transizione faccio
        else:
            U = encountered.value * Trader.calc_U_opinion(self.model.opinion_index, self.model.price) # +- U a seconda di che transizione faccio
            freq = v1

        p_transition = Trader.calc_p_transition(freq, n , U)
        return p_transition, U

    @staticmethod
    @lru_cache(maxsize=2000, typed=False)
    def calc_U_opinion(opinion_index, price):
        '''Calculate transition exponent for opinion change probability'''
        return a1 * opinion_index + a2 * price / v1

    @staticmethod
    @lru_cache(maxsize=2000, typed=False)
    def calc_U_strategy(price, slope, tech_factor_coeff):
        '''Calculate transition exponent for strategy change probability'''
        # excess profits per unit by technical
        ept = (r + slope / v2) / price - R
        # excess profits per unit by fundamentalist
        epf = s * abs((price - pf) / price)
        return a3 * (tech_factor_coeff * ept - epf)

    @staticmethod
    @lru_cache(maxsize=2000, typed=False)
    def calc_p_transition(freq, U, n):
        return freq * math.exp(U) * DT

    def _get_random_encounter(self):
        rng = random.random() * N
        return mk.Strategy.Fundam if rng < self.model.nf \
            else mk.Strategy.Tech_O if rng < self.model.tech_optimists \
                else mk.Strategy.Tech_P

    def pick_strategy(self):
        encountered = self._get_random_encounter()

        if self.model.get_n_traders(self.strategy) <= MIN_TRADER:
            logger.debug(f"Cannot change strategy because there are too few {self.strategy.name}")
            return
        elif self.strategy != encountered:
            p_transition, U = self._calc_transition_matrix(encountered)

            logger.debug(f"{self.strategy.name} -> {encountered.name}: U = {U} - p_trans = {p_transition}")

            if random.random() < p_transition:
                self.switch(encountered)

    def switch(self, new: mk.Strategy):
        self.model.switch(self.strategy, new)
        self.strategy = new

    @property
    def opinion(self):
        if self.strategy == mk.Strategy.Fundam:
            raise ValueError('Cannot ask opinion of a fundamentalist')
