from __future__ import annotations
from typing import List, NamedTuple
import random

from recordclass import RecordClass

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from model.Agenti import Trader, Technical, Fundamental, Noise, starting_money, starting_assets
                                                       

class Price(NamedTuple):                                                        # namedtuple per facilitare la price history
    close   : float = 0
    open    : float = 0
    high    : float = 0
    low     : float = 0
    volume  : int   = 0
    bid     : float = 0
    ask     : float = 0
    

class Order(RecordClass):                                                       # tipo namedtuple ma mutable per gestire più facilmente la struttura degli ordini
    price   : float
    n       : int                                                               # numero di azioni
    agent   : Trader
    order_t : str                                                               # order type
    time    : int
    def __lt__(self, other: Order):                                             # python lo usa per fare i max e i min in automatico (e anche i sort obv)
        return self.price < other.price
    def __gt__(self, other: Order):                                             # python lo usa per fare i max e i min in automatico (e anche i sort obv)
        return self.price > other.price
    def __eq__(self, other: Order):                                             # python lo usa per fare i max e i min in automatico (e anche i sort obv)
        return self.price == other.price


class CompletedOrder(NamedTuple):                                               # just a wrapper for easier readability
    buy     : Order
    sell    : Order
    price   : float
    n       : int
    time    : int


class PriceSeries(List [Price]):
    def __init__(self, *iterable):
        super().__init__(*iterable)
    
    @property
    def t(self):
        return self[-1]
	
    def slope(self, initial: int, final: int) -> float:
        ''' rapporto incrementale fra prezzo al momento final e initial '''
        return (self[final].close - self[initial].close) / (final - initial)


class Mercato(Model):
    def __init__(self, nf: int, nt: int, nn: int, ask0: float, bid0: float):

        # Set up model objects
        self.schedule = RandomActivation(self)

        self.nf = nf
        self.nt = nt
        self.nn = nn
        # total number of noise, fundamentalist and technical traders, stays constant
        self.N = nf + nt + nn

        # TODO definire bene questi
        self.priceseries = PriceSeries([Price(ask=ask0, bid=bid0)])

        self.sell_book          : List[Order] = []
        self.buy_book           : List[Order] = []
        self.fulfilled_orders   : List[CompletedOrder] = []                     # lista di ordini completati

        self.datacollector = DataCollector(
            model_reporters={
                'ask'       : 'ask',
                'bid'       : 'bid',
                'close'     : 'close',
                'volume'    : 'volume',
                'optimists' : 'optimists',
                'pessimists': 'pessimists'
            },
            agent_reporters={
                'wealth'    : 'wealth'
            }
        )
            
        self.running = False

    def _generate_agents(self):
        for i in range(self.nf):
            p = Fundamental(self, i, starting_money(), starting_assets(), random.random()*1e-1 + 0.10)
            self.schedule.add(p)
        for i in range(self.nt):
            p = Technical(self, i + self.nf, starting_money(), starting_assets(), random.randint(10, 20))
            self.schedule.add(p)
        for i in range(self.nn):
            p = Noise(self, i + self.nf+self.nt, starting_money(), starting_assets())
            self.schedule.add(p)

    # TODO fare in modo che ci siano anche tutti gli altri parametri per price e poi appendere tutto a priceseries
    def _generate_data(self):
        for i in range(self.N):
            self.schedule.add(Noise(self, i, starting_money(), starting_assets()))
        for i in range(3):
            self.step()
        for i in range(self.N):
            self.schedule.remove(self.schedule.agents[0])

    def start(self):
        self._generate_data()
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
        volume  = sum((x.n for x in self.fulfilled_orders))

        self.priceseries.append(Price(close, open, high, low, volume, bid, ask))

    def _complete_order(self, buy: Order, sell: Order):
        n = min(buy.n, sell.n)
        # TODO vedere se cambiare questo price quando avremo il market maker
        price = (buy.price + sell.price)/2

        buy.agent.complete_order(buy, n, price)
        sell.agent.complete_order(sell, n, price)

        t = max(buy.time, sell.time)                                            # time a cui avviene l'ordine

        self.fulfilled_orders.append(CompletedOrder(buy, sell, price, n, t))

        if buy.n == 0:
            self.buy_book.remove(buy)
        if sell.n == 0:
            self.sell_book.remove(sell)

    def _fulfill(self):
        buy  = max(self.buy_book)
        sell = min(self.sell_book)
        if buy.price >= sell.price:
            self._complete_order(buy, sell)
            self._fulfill()


    def step(self):
        '''
        Advance the model by one step.
        '''
        self.fulfilled_orders = []
        self.schedule.step()
        if len(self.buy_book) > 0:
            self._fulfill()

        if len(self.fulfilled_orders) > 0:
            self._update_price_history()
        self.datacollector.collect(self)

    def place_order(self, order: Order):
        order_book = self.buy_book if order.order_t == 'buy' else self.sell_book
        order_book.append(order)
        return order

    @property
    def ask(self):
        return self.priceseries.t.ask

    @property
    def bid(self):
        return self.priceseries.t.bid

    @property
    def close(self):
        return self.priceseries.t.close

    @property
    def volume(self):
        return self.priceseries.t.volume

    @property
    def optimists(self):
        return sum((1 for a in self.schedule.agents if a.opinion == 1))

    @property
    def neutral(self):
        return sum((1 for a in self.schedule.agents if a.opinion == 0))
    
    @property
    def pessimists(self):
        return sum((1 for a in self.schedule.agents if a.opinion == -1))

