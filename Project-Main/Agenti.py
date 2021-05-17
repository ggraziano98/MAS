from cmath import exp
import random

from sqlalchemy import null
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
from sklearn.cluster import k_means

#TODO
#Price class(method?) with attributes .t, .series, .slope, .whatever --> inside market?

class technical(Agent):

    class_type = 'tech'

    def __init__(self, status, money, assets, price_t, k, unique_id):
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
        time_range = random.choice(range(50))
        price_slope = pd.Series(np.gradient('price.series'[-time_range:-1])) #to be written later as price.slope attribute
        alpha = random.random(0.5,1)
        U = alpha*(price_slope/k) #k è la frequenza con cui l'agente rivaluta la sua opinione, come la implementiamo?
        shift_probability = stats.expon.cdf(self.status*U)*k #usando sta funzione la shift_probability è già normalizzata come una probabilità 

        #DONE per far funzionare il codice sotto bisogna controllare che shift_probability sia normalizzata tra 0 e 1 
       
        if random.random() < shift_probability: 
            change_of_opinion(self)
        # non so se è la sintassi giusta per scrivere sta roba


        # rettifico: non c'è alcun codice, come cazzo la implemento sta transizione di probabilità? 
        # bisogna normalizzare la shift_probability... com'cazz s normalizz sta probbbabbiliti wagliò

        

        




         

        


pass


