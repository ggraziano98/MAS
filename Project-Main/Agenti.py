import random

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

#TODO
#Price class(method?) with attributes .t, .series, .slope, .whatever --> inside market?

class technical(Agent):

    class_type = 'tech'

    def __init__(self, status, money, assets, price_t, k, unique_id):
        super().__init__(status, money, assets, price_t, k, unique_id)
        self.status = random.choice([-1,1]) #random initialization of opinion
        self.money = random.randrange(100,5000,1) #random initialization of avb money from 100 to 5000 and step 1
        self.assets = assets
        self.k = k 
        self.unique_id = unique_id

    def change_of_opinion(self):
        if self.status == 1:
            self.status = -1
        else:
            self.status = 1

    def does_its_thing(self):
        #calculate slope
        time_range = random.choice(range(50)) # ogni agente calcola la slope col suo range temporale 
        price_slope = np.gradient('price.series'[-time_range:-1]) #to be written later as price.slope attribute
        alpha = random.randrange(5000,10000,1)*float(1e-4)
        U = alpha*(price_slope/k) #k è la frequenza con cui l'agente rivaluta la sua opinione, come la implementiamo?
        shift_probability = stats.expon.cdf(self.status*U)*k #usando sta funzione la shift_probability è già normalizzata come una probabilità (a quanto pare)
        if random.random() < shift_probability: 
            self.change_of_opinion()
        # è la sintassi giusta per scrivere sta roba?

    def step(self):
        if self.status == 1:
            #self.buy_order(amount) - c'è ancora da definire il metodo buy
            pass
        else:
            #self.sell_order(amount) - c'è ancora da definire il metodo sell 
            pass

        n = 0
        while n != self.k:
            n += 1
            if n == self.k: 
                self.does_its_thing()
                # non so se è la sintassi giusta per scrivere sta roba
                n = 0
          


        # rettifico: non c'è alcun codice, come cazzo la implemento sta transizione di probabilità? 
        # bisogna normalizzare la shift_probability... com'cazz s normalizz sta probbbabbiliti wagliò

        

        




         

        


pass


