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
        self.money = money #random initialization of avb money from 100 to 5000 and step 1
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

        # ogni agente calcola la slope col suo range temporale 
        time_range = random.randint(2, 50) 
        price_slope = np.gradient('price.series'[-time_range:-1]) #to be written later as price.slope attribute
        alpha = 0.5 + random.random() * 0.5
        #k è la frequenza con cui l'agente rivaluta la sua opinione, come la implementiamo?
        U = alpha*(price_slope/self.k) 
        shift_probability = stats.expon.cdf(self.status*U) * self.k #usando sta funzione la shift_probability è già normalizzata come una probabilità (a quanto pare)
        if self.status == +1 and random.random() < shift_probability: 
            self.change_of_opinion()
        if self.status == -1 and random.random() > shift_probability:
            self.change_of_opinion()
        # è la sintassi giusta per scrivere sta roba?

    n_step = 0

    def step(self, n_step):
        if self.status == +1:
            #self.buy_order(amount) - c'è ancora da definire il metodo buy
            pass
        else:
            #self.sell_order(amount) - c'è ancora da definire il metodo sell 
            pass

        while True:
            n_step += 1
            if n_step%self.k == 0: 
                self.does_its_thing()
            # in questo modo solo ogni k passi l'agente rivaluta la propria opinione 


       

# si differenziano dai fundamental perchè l'operazione buy o sell è casuale
class Noise(Agent):
    
    agent_type = 'Noise'
    
    def __init__(self, prezzo_t, reddito, n_azioni, unique_id):  #il costo_azione dipenderà dalla compra-vendita
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

        
class Trader(Agent):
    def __init__(self, model, unique_id, money, assets, args):
        super().__init__(self, model, unique_id)
        self.money = money
        self.assets = assets

    def does_its_thing(self):
        # Each class implements this
        pass

    def buy(self, n, price):
        self.model.place_order('buy', n, price)

    def sell(self, n, price):
        self.model.place_order('sell', n, price)








class fundamental(Trader):
    
    agent_type = 'fund'
    def __init__(self, model, unique_id, money, assets, args):
        super().__init__(self, model, unique_id)
    
        
        '''
    FOUNDAMENTAL
    
    Attributes:
        
        valutazione secondo lui dell'azione
        reddito
        '''
        self.valutazione=0
        self.reddito  = random.random()*int(1e4)
        self.n_azioni = n_azioni
        self.riskfree = 0.03
        self.pi =  random.random()*1e-1 + 0.10
            
    def does_its_thing(self):
            
        #valutazione
        self.valutazione = prezzo_t + 0.2* prezzo_t*(-1 + 2*random.random())
            
        


    def step(self):
        if self.reddito > prezzo_t && self.valutazione > prezzo_t + (self.riskfree + self.pi)*prezzo_t:
            #compra
            self.buy
        
        if self.valutazione < prezzo_t + (self.riskfree)*prezzo_t && n_azioni >0:
            #vende
            self.sell
              