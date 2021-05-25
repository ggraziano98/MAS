import random
import math
from typing import List

import scipy.stats as stats
import numpy as np
import pandas as pd 
import mesa
import matplotlib.pyplot as plt

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from .Market import *

#TODO
#Price class(method?) with attributes .t, .series, .slope, .whatever --> inside market?


def sigmoid(x):
  return 2 / (1 + math.exp(-x)) - 1

        
class Trader(Agent):
    def __init__(self, model: Mercato, unique_id: int, money: float, assets: int, *args, **kwargs):
        super().__init__(self, model, unique_id)
        self.model = model
        self.money = money
        self.assets = assets
        self.orders: List[Order] = []

    def does_its_thing(self):
        ''' Logica dell'agente, implementata da ciascun tipo '''
        pass

    def buy(self, n, price):
        ''' place a buy order for n assets at price '''
        order = self.model.place_order(Order(price, n, self, 'buy'))
        self.orders.append(order)

    def sell(self, n, price):
        ''' place a sell order for n assets at price '''
        order = self.model.place_order(Order(price, n, self, 'sell'))
        self.orders.append(order)

    def step(self, *args, **kwargs):
        pass

    def complete_order(self, order: Order, n: int, price: float):
        assert order in self.orders
        order.n -= n
        if order.n == 0:
            self.orders.remove(order)
        m = 1 if order.order_t == 'buy' else -1



class Technical(Trader):

    class_type = 'tech'

    def __init__(self, model, unique_id, money, assets, status, price_t, k):
        super().__init__(model, unique_id, money, assets)
        self.status = random.choice([-1,1])                                     # random initialization of opinion
        self.money = money                                                      # random initialization of avb money from 100 to 5000 and step 1
        self.assets = assets
        self.k = k                                                              # k è la frequenza con cui l'agente rivaluta la sua opinione, come la implementiamo? 
        self.unique_id = unique_id

    def change_of_opinion(self, state=0):
        ''' set state to state or change state if state=0 '''
        if state == 0:
            if self.status == 1:
                self.status = -1
            else:
                self.status = 1
        else:
            self.status = state

    def does_its_thing(self):
        # TODO rivedere con i numeri

        time_range = random.randint(2, 50)                                      # ogni agente calcola la slope col suo range temporale 
        price_slope = self.model.price.slope(-time_range, -1)
        
        shift_probability = sigmoid(price_slope)                                # TODO per ora va bene cosi'

        # è la sintassi giusta per scrivere sta roba?
        if random.random() < abs(shift_probability): 
            self.change_of_opinion(shift_probability / abs(shift_probability))

    def step(self):
        if self.status == +1:
            #self.buy_order(amount) - c'è ancora da definire il metodo buy
            pass
        else:
            #self.sell_order(amount) - c'è ancora da definire il metodo sell 
            pass

        self.does_its_thing()
        # in questo modo solo ogni k passi l'agente rivaluta la propria opinione 
       

# si differenziano dai fundamental perchè l'operazione buy o sell è casuale
class Noise(Trader):
    
    agent_type = 'Noise'
    
    def __init__(self, prezzo_t, reddito, n_azioni, unique_id):                 # il costo_azione dipenderà dalla compra-vendita
        super().__init__(prezzo_t, reddito, n_azioni, unique_id)

        '''
    NOISE TRADER
    
    Attributes:
        
        n_azioni che ha 
        reddito
        
        '''   

        self.n_azioni    = n_azioni
        self.reddito     = random.random()*int(1e4)
        self.unique_id = unique_id
        
        def does_its_thing(self):
                
            r = random.random()

            if r <= 0.5:
                if self.reddito >= prezzo_t:
                    # buy_order(amount)
                    pass
                            
            else:
                if self.n_azioni >= 0:    #ovviamente solo se ha azioni vende
                    # sell_order(amount)
                    pass

    def step(self):
        self.does_its_thing()    

