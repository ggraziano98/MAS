from __future__ import annotations
import random
import math
import numpy as np
from typing import List, Tuple

from mesa import Agent

import model.Market as mk

#TODO sono placeholders, da implementare in modo che le azioni siano in numero costante
def starting_money():
    return random.random()*10000

#TODO sono placeholders, da implementare in modo che le azioni siano in numero costante
def starting_assets():
    return random.randint(0, 400000)

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
        self.internal_time = 0
        self.opinion = random.choice([-1, +1])

    def does_its_thing(self):
        ''' Logica dell'agente, implementata da ciascun tipo '''
        pass

    def _buy(self, n, price):
        ''' place a buy order for n assets at price '''
        order = self.model.place_order(mk.Order(price, n, self, 'buy', self.model.schedule.steps))
        self.orders.append(order)
        self.money -= n * price

    def _sell(self, n, price):
        ''' place a sell order for n assets at price '''
        order = self.model.place_order(mk.Order(price, n, self, 'sell', self.model.schedule.steps))
        self.orders.append(order)
        self.assets -= n

    def step(self, *args, **kwargs):
        self.does_its_thing()
        if self.opinion > 0:
            n, prezzo = self._buy_logic()
            if n > 0:
                self._buy(n, prezzo)
        elif self.opinion < 0:
            n, prezzo = self._sell_logic()
            self._sell(n, prezzo) 


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

    def _buy_logic(self) -> Tuple[int, float]:
        '''
        default logic for determining how much to buy
        '''
        # inv = random.random() * self.money
        prezzo = np.random.normal(self.model.bid, random.random())
        # prezzo = self.model.ask * (random.random()/2 + 1/2)
        n = 1
        return n, prezzo
        
    def _sell_logic(self) -> Tuple[int, float]:
        '''
        default logic for determining how much to sell
        '''
        n = 1
        prezzo = np.random.normal(self.model.ask, random.random())
        # prezzo = self.model.bid * (1 + (random.random() - 0.5) * 0.5)
        return n, prezzo

    @property
    def wealth(self):
        return self.money + self.assets * self.priceseries.t.close


class Technical(Trader):
    agent_type = 'tech'
    def __init__(self, model, unique_id, money, assets, k):
        super().__init__(model, unique_id, money, assets)
        self.k = k  
        self.time_range = 20
                                                                                # k è la frequenza con cui l'agente rivaluta la sua opinione, come la implementiamo? 

    def does_its_thing(self):
        # TODO rivedere con i numeri, k non è mai usata                         # ogni agente calcola la slope col suo range temporale 
        if self.internal_time > self.time_range:
            price_slope = self.priceseries.slope(-self.time_range, -1)
            shift_probability = sigmoid(self.k*price_slope)

            if random.random() > shift_probability:
                self.opinion = 1
            else: 
                self.opinion = -1
        else:
            pass

        self.internal_time += 1
       

# si differenziano dai fundamental perchè l'operazione buy o sell è casuale
class Noise(Trader):
    agent_type = 'noise'
    def __init__(self, model, unique_id, money, assets):                        # il costo_azione dipenderà dalla compra-vendita
        super().__init__(model, unique_id, money, assets)
        
    def does_its_thing(self):            
        self.opinion = random.choice([-1, 0, 1])


class Fundamental(Trader):
    agent_type = 'fund'
    def __init__(self, model, unique_id, money, assets, pi, k=100):
        super().__init__(model, unique_id, money, assets)
    
        self.riskfree = 0.03
        self.pi = pi                     
        self.k = k                                                 
            
    def does_its_thing(self):
        # self.valutazione = self.model.close + 0.2* self.model.close * (-1 + 2*random.random())

        self.internal_time += 1

        if self.model.valutazione() > self.model.close + (self.riskfree + self.pi)*self.model.close:
            self.opinion = 1   
        elif self.model.valutazione() < self.model.close + (self.riskfree)*self.model.close:
            self.opinion = -1
        else:
            self.opinion = 0
                
        if self.internal_time % self.k == 0:
            self.valutazione = self.model.valutazione()
    
        
        
        '''
        t = 0
        while t != self.k:                                                      # the agent doesn't update its valuation each time step.
            t += 1
            if t == self.k:
                self.valutazione = self.model.close + 0.8* self.model.close * (-1 + 2*random.random())
                t = 0
        '''

        # print(self.valutazione, self.model.close + (self.riskfree + self.pi)*self.model.close, self.opinion)
            

