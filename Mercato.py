import numpy as np


from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
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


    def __init__(self, height, width, N, M):
        '''
        Create a new forest fire model.
        
        Args:
            height, width: The size of the grid to model
            N: numero Vucumpra
            M: numero Umarell
        '''
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)
        self.N = N 
        self.M = M

        # TODO datacollector
        # self.dc = DataCollector({"Fine": lambda m: self.count_type(m, "Fine"),
        #                         "On Fire": lambda m: self.count_type(m, "On Fire"),
        #                         "Burned Out": lambda m: self.count_type(m, "Burned Out")})
        
        # Place down Vucumpras

        #TODO questo codice fa cagare non sempre ne spawna N
        for i in range(self.N):
            x, y = random_cell(self.grid)
            v = self.grid.get_cell_list_contents([(x, y)])
            if len(v) == 0:
                prezzo = np.random.rand()*10
                new_vucumpra = Vucumpra(self, prezzo, (x, y), 25)
                self.grid.place_agent(new_vucumpra, (x, y))
                self.schedule.add(new_vucumpra)

        for i in range(self.M):
            pos = random_cell(self.grid)
            new_umarell = Umarell(self, prezzo, 1, 10, pos)
            self.grid.place_agent(new_umarell, pos)

            self.schedule.add(new_umarell)

            
        self.running = True
        
    def step(self):
        '''
        Advance the model by one step.
        '''
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