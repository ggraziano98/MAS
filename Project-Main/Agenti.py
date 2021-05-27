from __future__ import annotations
import random
import math
from typing import List

from mesa import Agent

import Market as mk

#TODO sono placeholders, da implementare in modo che le azioni siano in numero costante
def starting_money():
    return random.random()*10000
#TODO sono placeholders, da implementare in modo che le azioni siano in numero costante
def starting_assets():
    return random.randint(0, 40)

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

        
class Trader(Agent):
    def __init__(self, model: mk.Mercato, unique_id: int, money: float, assets: int, *args, **kwargs):
        super().__init__(unique_id, model)
        self.model = model
        self.priceseries = model.priceseries
        self.money = money
        self.assets = assets
        self.orders: List[mk.Order] = []
        self.opinion = 0

    def does_its_thing(self):
        ''' Logica dell'agente, implementata da ciascun tipo '''
        pass

    def buy(self, n, price):
        ''' place a buy order for n assets at price '''
        order = self.model.place_order(mk.Order(price, n, self, 'buy', self.model.schedule.steps))
        self.orders.append(order)
        self.money -= n * price

    def sell(self, n, price):
        ''' place a sell order for n assets at price '''
        order = self.model.place_order(mk.Order(price, n, self, 'sell', self.model.schedule.steps))
        self.orders.append(order)
        self.assets -= n

    def step(self, *args, **kwargs):
        self.does_its_thing()
        if self.opinion > 0:
            self._random_buy()
        elif self.opinion < 0:
            self._random_sell()

    def complete_order(self, order: mk.Order, n: int, price: float):
        if order not in self.orders:
            print('MISSING ORDER', order, self.orders)
        assert order in self.orders
        order.n -= n
        if order.n == 0:
            self.orders.remove(order)
        if order.order_t == 'buy':
            self.money  += n * order.price
            self.money  -= n * price
            self.assets += n
        else:
            self.money += n * price

    def _random_buy(self):
        inv = random.random() * self.money
        prezzo = self.model.bid + random.gauss(0, self.model.ask - self.model.bid)
        n = int(inv / prezzo)
        if n > 0:
            self.buy(n, prezzo)
        
    def _random_sell(self):
        prezzo = self.model.ask + random.gauss(0, self.model.ask - self.model.bid)
        self.sell(self.assets, prezzo) 

    @property
    def wealth(self):
        return self.money + self.assets * self.priceseries.t.close


class Technical(Trader):
    agent_type = 'tech'
    def __init__(self, model, unique_id, money, assets, k):
        super().__init__(model, unique_id, money, assets)
        self.k = k                                                              # k è la frequenza con cui l'agente rivaluta la sua opinione, come la implementiamo? 

    def does_its_thing(self):
        # TODO rivedere con i numeri, k non è mai usata
        time_range = random.randint(2, 3)                                      # ogni agente calcola la slope col suo range temporale 
        price_slope = self.priceseries.slope(-time_range, -1)

        shift_probability = sigmoid(price_slope)

        if random.random() > shift_probability:
            self.opinion = 1
        else: 
            self.opinion = -1
       

# si differenziano dai fundamental perchè l'operazione buy o sell è casuale
class Noise(Trader):
    agent_type = 'noise'
    def __init__(self, model, unique_id, money, assets):                        # il costo_azione dipenderà dalla compra-vendita
        super().__init__(model, unique_id, money, assets)
        
    def does_its_thing(self):            
        self.opinion = random.choice([-1, 0, 1])


class Fundamental(Trader):
    agent_type = 'fund'
    def __init__(self, model, unique_id, money, assets, pi):
        super().__init__(model, unique_id, money, assets)
    
        self.valutazione = 0
        self.riskfree = 0.03
        self.pi = pi                                                            # random.random()*1e-1 + 0.10
            
    def does_its_thing(self):
        self.valutazione = self.priceseries.t.close + 0.2* self.priceseries.t.close * (-1 + 2*random.random())
        if self.valutazione > self.priceseries.t.close + (self.riskfree + self.pi)*self.priceseries.t.close:
            self.opinion = 1
        elif self.valutazione < self.priceseries.t.close + (self.riskfree)*self.priceseries.t.close:
            self.opinion = -1
        else:
            self.opinion = 0
            

