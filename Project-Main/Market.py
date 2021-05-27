from typing import List, NamedTuple
from __future__ import annotations
import random

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from .Agenti import Trader, Technical, Fundamental, Noise, starting_money, starting_assets
                                                       

class Price(NamedTuple):                                                        # namedtuple per facilitare la price history
    close   : float
    open    : float
    high    : float
    low     : float
    volume  : int
    bid     : float
    ask     : float
    

class Order(NamedTuple):                                                        # namedtuple per gestire più facilmente la struttura degli ordini
    price   : float
    n       : int                                                               # numero di azioni
    agent   : Trader
    order_t : str                                                               # order type
    time    : int
    def __lt__(self, other: Order):                                             # python lo usa per fare i max e i min in automatico (e anche i sort obv)
        return self.price < other.price


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
        for i in range(self.nn):
            p = Noise(self, i + self.nf+self.nt, starting_money, starting_assets())

    # TODO fare in modo che ci siano anche tutti gli altri parametri per price e poi appendere tutto a priceseries
    def _generate_data(self):
        def randomwalk(step, start, lenght):
            pos = start 
            walk = []
            for i in range(lenght):
                k = random.random()
                if k > 1/2:
                    pos += step 
                else:
                    pos -= step 
                walk.append(pos)
            return walk

        rw = randomwalk(1,0,100)
        
    def start(self):
        self._generate_agents()
        self._generate_data()
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

        self._fulfill()
        self.buy_book   = [x for x in self.buy_book if x.n > 0 ]
        self.sell_book  = [x for x in self.sell_book if x.n > 0]
        self._update_price_history()

    def place_order(self, order: Order):
        order_book = self.buy_book if order.order_t == 'buy' else self.sell_book
        order_book.append(order)

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

