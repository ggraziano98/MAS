import numpy as np

import matplotlib.pyplot as plt
%matplotlib inline

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from .Mercato import Mercato



class Venditore(Agent):
    '''
    Un venditore.
    
    Attributes:
        prezzo
        banane_ieri             (vendute)
        banane_totali           (vendute)
        pos                     
        unique_id
    '''
    id_curr = 0
    def __init__(self, model, prezzo, pos):
        '''
        Create a venditore.
        Args:
            prezzo: Prezzo iniziale
            pos:    Posizione
        '''
        super().__init__(class.id_curr, model)
        class.id_curr += 1
        self.prezzo = prezzo
        self.unique_id = pos
        self.banane_vendute = 0
        self.banane_totali = 0
        self.pos = pos

    def vendi(n):
        self.banane_vendute += 1
        
    def step(self):
        '''
        Incontra Umarell e vende
        '''
        if self.condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=False)
            for neighbor in neighbors:
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"


class Umarell(Agent):
    '''
    Un Umarell.
    
    Attributes:
        prezzo              (prezzo a cui vuole comprare)
        banane_ieri         (numero banane comprate ieri)
        banane_totali       (numero banane comprate totale)
        banane_scorta       (numero banane in scorta) 
        n                   (numero di venditori incontrati)
        bisogno             (bisogno giornaliero)
        pos
        unique_id
    '''
    id_curr = 0
    def __init__(self, model: Mercato, prezzo, n, bisogno, banane_iniziali, pos):
        '''
        Crea un Umarell.
        Args:
            prezzo: prezzo a cui compra
            n:      numero di venditori che incontra
        '''
        super().__init__(class.id_curr, model)
        class.id_curr += 1
        self.prezzo = prezzo
        self.unique_id = class.id_curr
        self.banane_ieri = 0
        self.banane_totali = 0
        self.bisogno_def = bisogno
        self.bisogno = bisogno
        self.banane_scorta = banane_iniziali
        self.pos = pos



        self.model = model

    def start_day(self):
        """
        Start day at random position and reset bisogno
        """
        x = np.random.rand() * self.model.grid.width
        y = np.random.rand() * self.model.grid.height
        self.model.grid.move_agent(self, (x, y))
        self.bisogno = self.bisogno_def
        
    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.model.grid, moore=False)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def compra(n):
        self.bisogno -= 1    
    
    def step(self):
        '''
        Ogni step si posiziona random nella griglia  e inizia a camminare
        vede i venditori più vicini
        decide se comprare o no 
        restock
        '''
        if self.bisogno > 0:
            self.random_move()
            vicini = self.model.grid.get_cell_list_contents([self.pos])
            vicini = [v if type(v) == Venditore for v in vicini]

            v_min = min(vicini, key=lambda v: v.prezzo)
            if v_min.prezzo <= self.prezzo:
                self.compra(1)
                v_min.vendi(1)
                


        if self.condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=False)
            for neighbor in neighbors:
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"



