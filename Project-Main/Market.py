from typing import List, NamedTuple
from __future__ import annotations
from warnings import simplefilter
from matplotlib.pyplot import close

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from .Agenti import Trader, Technical, Fundamental, Noise

class Order(NamedTuple):                                                        # namedtuple per gestire più facilmente la struttura degli ordini
    price   : float
    n       : int
    agent   : Trader
    order_t : str
    time    : int
    def __lt__(self, other: Order):
        return self.price < other.price


class Price(NamedTuple):                                                        # namedtuple per facilitare la price history
    close   : float
    open    : float
    high    : float
    low     : float
    avg     : float
    volume  : float
    bid     : float
    ask     : float
    

class CompletedOrder(NamedTuple):                                               # just a wrapper for easier readability
    buy     : Order
    sell    : Order
    price   : float
    n       : int
    time    : int


class PriceSeries(List [Price]):
    def __init__(self, *iterable):
        super().__init__(iterable)
    
    @property
    def t(self):
        return self[-1]
	
    def slope(self, initial: int, final: int) -> float:
        ''' rapporto incrementale fra prezzo al momento final e initial '''
        return (self[final].close - self[initial].close) / (final - initial)


class Mercato(Model):
    def __init__(self, nf: int, nt: int, nn: int):
        # Set up model objects
        self.schedule = RandomActivation(self)

        self.nf = nf
        self.nt = nt
        self.nn = nn
        # total number of noise, fundamentalist and technical traders, stays constant
        self.N = nf + nt + nn

        # TODO definire bene questi
        self.priceseries = PriceSeries()
    
        self.sell_book          : List[Order] = []
        self.buy_book           : List[Order] = []
        self.fulfilled_orders   : List[CompletedOrder] = []                     # lista di ordini completati

        self.datacollector = DataCollector(
            {
                # ask
                # bid
                # close
                # volume
                # optimists
                # pessimists
            }
        )
            
        self.running = False
        
    # TODO
    def _generate_agents(self):
        pass
        
    def start(self):
        self._generate_agents()
        self.running = True

    #TODO
    def _update_price_history(self):
        bid     = max(self.buy_book).price
        ask     = min(self.sell_book).price
        high    = max(self.fulfilled_orders, key=lambda x: x.price).price
        low     = min(self.fulfilled_orders, key=lambda x: x.price).price
        open    = min(self.fulfilled_orders, key=lambda x: x.time).price
        close   = max(self.fulfilled_orders, key=lambda x: x.time).price

        # TODO @Marco
        volume  = 0
        avg = 0

        self.priceseries.append(Price(close, open, high, low, avg, volume, bid, ask))

    def _complete_order(self, buy: Order, sell: Order):
        n = min(buy.n, sell.n)
        # TODO vedere se cambiare questo price quando avremo il market maker
        price = (buy.price + sell.price)/2

        buy.agent.complete_order(buy, n, price)
        sell.agent.complete_order(sell, n, price)

        t = max(buy.time, sell.time)                                            # time a cui avviene l'ordine

        self.fulfilled_orders.append(CompletedOrder(buy, sell, price, n, t))

    def _fulfill(self):
        # Rifare in modo che possa sputare un price e un numero di azioni
        buy  = max(self.buy_book)
        sell = min(self.sell_book)
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
        self.fulfilled_orders = []
        self.schedule.step()

        self._fulfill()
        self.buy_book   = [x for x in self.buy_book if x.n > 0 ]
        self.sell_book  = [x for x in self.sell_book if x.n > 0]
        self._update_price_history()

        self._calc_volume()

    def place_order(self, order: Order):
        order_book = self.buy_book if order.order_t == 'buy' else self.sell_book
        order_book.append(order)


