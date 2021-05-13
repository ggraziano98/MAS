import numpy as np
import networkx as nx
from networkx.algorithms.bipartite.generators import random_graph

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from MasUtils import *
from Agenti import *

class Mercato(Model):
    '''
    Mercato scemo

    1 oggetto con prezzo 
        il prezzo dovrà poi essere concordato quando faremo un modello migliore


    N agenti che vendono
        decidono prezzo di vendita 



    M agenti che comprano 
        decidono prezzo di acquisto
        stessi soldi/distribuzione di soldi
        incontrano n agenti
        scelgono di comprare da un agente
    '''


    def __init__(self, N, M):
        '''       
        Args:
            height, width: The size of the grid to model
            N: numero Vucumpra
            M: numero Umarell
        '''
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.num_nodes = N + M
        self.N = N 
        self.M = M
    
        self.G = random_graph(N, M, p=0.5)
        self.grid = NetworkGrid(self.G)
      

        # TODO datacollector
        # self.dc = DataCollector({"Fine": lambda m: self.count_type(m, "Fine"),
        #                         "On Fire": lambda m: self.count_type(m, "On Fire"),
        #                         "Burned Out": lambda m: self.count_type(m, "Burned Out")})
        
        # Place down Vucumpras

        #TODO questo codice fa cagare non sempre ne spawna N
        
        list_um_nodes = [n for n, d in self.G.nodes(data=True) if d["bipartite"] == 1]
        list_vu_nodes = [n for n, d in self.G.nodes(data=True) if d["bipartite"] == 0]
        
        print(len(list_um_nodes), len(list_vu_nodes))
        
        
        for i in range(self.N):
            prezzo = np.random.rand()*10
            v = Vucumpra(self, i, prezzo, 25)
            self.grid.place_agent(v, list_vu_nodes[i])
            self.schedule.add(v)
            
        
        for i in range(self.M):
            prezzo = np.random.rand()*10
            v = Umarell(self, self.N + i, prezzo, 1, 10)
            self.grid.place_agent(v, list_um_nodes[i])
            self.schedule.add(v)
            
        self.running = True
        
    def randomize_edges(self):
        new_g = random_graph(self.N, self.M, 0.5)        
        e = new_g.edges
        self.G.clear_edges()
        self.G.add_edges_from(e)
        
        
    def step(self):
        '''
        Advance the model by one step.
        '''
        #TODO
        self.randomize_edges()
        self.schedule.step()
        
        
        # self.dc.collect(self)
        # Halt if no more fire
        # if self.count_type(self, "On Fire") == 0:
        #     self.running = False
    

    # @staticmethod
    # def count_type(model, tree_condition):
    #     '''
    #     Helper method to count trees in a given condition in a given model.
    #     '''
    #     count = 0
    #     for tree in model.schedule.agents:
    #         if tree.condition == tree_condition:
    #             count += 1
    #     return count



#