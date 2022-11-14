from __future__ import annotations

import logging
import math
import random
from datetime import datetime
from enum import Enum

import model.Market as mk
from mesa import Agent
from model.conf import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.WARNING)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(f'{RESULT_DIR}/Agenti.log', mode='w')
file_handler.setLevel(AGENTI_LOG_LEVEL)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)

def log_agent_step(i):
    logger.info(f"\n\nSTEP {i}\n\n")

class Strategies(Enum):
    Technical = 1
    Fundamentalist = 2

class Trader(Agent):
    def __init__(self, model: mk.Mercato, unique_id: int, strategy: int, opinion: int = 1):
        super().__init__(unique_id, model)

        self.model = model
        self.strategy = strategy
        self.opinion = opinion


    def step(self):
        self.pick_strategy()
        self.trader_logic()


    def pick_strategy(self):
        price_slope = self.model.priceseries.slope()

        # excess profits per unit by technical
        ept = ((r + price_slope / v2) / self.model.price) - R
        epf = s * abs((pf - self.model.price) / self.model.price)

        if self.strategy == Strategies.Fundamentalist and self.model.nf > MIN_TRADER:
            trader_encoutered = 1 if random.random() < self.model.tech_optimists / self.model.nt else -1
            # n = self.model.tech_optimists if trader_encoutered == 1 else self.model.tech_pessimists

            U = a3 * (trader_encoutered * ept - epf)
            p_transition = (self.model.nt / N) * v2 * math.exp(-U/v2) * DT

            # logger.debug(f"{'Picking strategy (F)':15s} - U = {U} - p_trans = {p_transition}")

            if random.random() < p_transition:
                self.switch(Strategies.Technical, trader_encoutered, self.strategy, self.opinion)

        elif self.strategy == Strategies.Technical:
            if self.model.nt < MIN_TRADER:
                return

            U = a3 * (self.opinion * ept - epf)
           
            p_transition = (self.model.nt / N) * (v2 * math.exp(U/v2)) * DT
            # logger.debug(f"{'Picking strategy (T)':15s} - U = {U} - p_trans = {p_transition}")

            if random.random() < p_transition:
                self.switch(Strategies.Fundamentalist, None, self.strategy, self.opinion)
        

    def trader_logic(self):
        # logica technical
        if self.strategy == Strategies.Technical:
            price_slope = self.model.priceseries.slope()
            x = (self.model.tech_optimists - self.model.tech_pessimists) / self.model.nt #OPINION INDEX
            U1 = a1 * x + a2 * price_slope #/ v1
            p_transition = (self.model.nt / N) * (v1 * math.exp(- self.opinion * U1 / v1)) * DT

            n = self.model.tech_optimists if self.opinion == 1 else self.model.tech_pessimists
            if random.random() < p_transition and n > MIN_TRADER/2:
                self.switch(Strategies.Technical, -self.opinion, self.strategy, self.opinion)

            # logger.debug(f"{'Technical':15s} - Slope: {price_slope:4.2f} - x: {x:4.2f} - Transition probability: {p_transition:4.3f} - Opinion: {self.opinion}")


    def switch(self, new_strategy, new_opinion, old_strategy, old_opinion):
        self.strategy = new_strategy
        self.opinion = new_opinion
        self.model.update_traders_count(new_strategy, new_opinion, old_strategy, old_opinion)

