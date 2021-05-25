from typing import Any, List, NamedTuple

import numpy as np
import networkx as nx
from networkx.algorithms.bipartite.generators import random_graph

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from .Agenti import *


class Price():
    def __init__(self):
        self.series = []
    
    def t(self):
        ''' prezzo corrente '''
        return self.series[-1]

    def slope(self, initial: int, final: int) -> float:
        ''' rapporto incrementale fra prezzo al momento final e initial '''
        return (self.series[final] - self.series[initial]) / (final - initial)

    def add(self, *args: float):
        ''' aggiungi uno o piu' prezzi alla serie '''
        for p in args:
            self.series.append(p)


class Order(NamedTuple):                                                        # namedtuple per gestire più facilmente la struttura degli ordini
    price   : float
    n       : int
    agent   : Any
    order_t : str


class Mercato(Model):
    def __init__(self, nf: int, nt: int, nn: int):

        # Set up model objects
        self.schedule = RandomActivation(self)
    
        self.sell_book : List[Order] = []
        self.buy_book  : List[Order] = []
        self.price = Price()
        self.nf = nf
        self.nt = nt
        self.nn = nn

        self.bid = -1
        self.ask = -1
        self.spread = -1

        # total number of noise, fundamentalist and technical traders, stays constant
        self.N = nf + nt + nn
        
        # TODO cambiare tipo di grafo
        self.G = random_graph(nf, nt, p=0.5)
        self.grid = NetworkGrid(self.G)
            
        self.running = False
        
    # TODO
    def _generate_agents(self):
        pass
        
    def start(self):
        self._generate_agents()
        self.running = True

    #TODO
    def _get_bid_ask(self):
        self.bid = self.buy_book[-1]
        self.ask = self.sell_book[0]
        self.spread = self.bid - self.ask

    def _complete_order(self, buy: Order, sell: Order):
        n = min(buy.n, sell.n)
        # TODO vedere se cambiare questo price quando avremo il market maker
        price = (buy.price + sell.price)/2

        buy.agent.complete_order(buy, n, price)
        sell.agent.complete_order(sell, n, price)

        if buy.n == 0:
            self.buy_book.remove(buy)
        if sell.n == 0:
            self.sell_book.remove(sell)

    def _fulfill(self):
        buy  = self.buy_book[-1]
        sell = self.sell_book[0]
        if buy.price > sell.price:
            self._complete_order(buy, sell)
            self._fulfill()

    #TODO
    def _calc_volume(self):
        pass

    def step(self):
        '''
        Advance the model by one step.
        '''
        #TODO
        self.sell_book.sort(key=lambda x: x.price)
        self.buy_book.sort(key=lambda x: x.price)

        self.schedule.step()
        self._fulfill()
        self._get_bid_ask()
        self._calc_volume()

    def place_order(self, order: Order):
        order_book = self.buy_book if order.order_t == 'buy' else self.sell_book
        order_book.append(order)


