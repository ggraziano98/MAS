import numpy as np
import networkx as nx
from networkx.algorithms.bipartite.generators import random_graph

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

class Mercato(Model):
    def __init__(self, nf, nt):

        # Set up model objects
        self.schedule = RandomActivation(self)
    
        self.order_book = {'buy':[], 'sell':[]}
        self.price_history = []
        self.nf = nf
        self.nt = nt

        # total number of fundamentalist and technical traders, stays constant
        self.N = nf + nt 
        
        # TODO cambiare tipo di grafo
        self.G = random_graph(nf, nt, p=0.5)
        self.grid = NetworkGrid(self.G)
            
        self.running = False
        
    # TODO
    def generate_agents(self):
        pass
        
    def start(self):
        self.generate_agents()
        self.running = True

    #TODO
    def get_bit_ask(self):
        pass

    #TODO
    def fulfill(self):
        pass

    #TODO
    def calc_volume(self):
        pass

    def step(self):
        '''
        Advance the model by one step.
        '''
        #TODO
        self.get_bid_ask()
        self.schedule.step()
        self.fulfill()
        self.calc_volume()




