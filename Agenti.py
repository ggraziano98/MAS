import numpy as np

import matplotlib.pyplot as plt

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from MasUtils import *



class Vucumpra(Agent):
    '''
    Un venditore.
    
    Attributes
        prezzo
        banane_ieri             (vendute)
        banane_totali           (vendute)
        pos                     
        unique_id
    '''
    id_curr = 0
    agent_type = 'Vucumpra'
    

    def __init__(self, model, prezzo, pos, scorta_banane):
        '''
        Create a venditore.
        Args:
            prezzo: Prezzo iniziale
            pos:    Posizione
        '''
        super().__init__(f'VUC_{Vucumpra.id_curr}', model)
        Vucumpra.id_curr += 1
        self.prezzo = prezzo
        self.scorta_banane = scorta_banane
        self.pos = pos
        self.registro_scorte = []
        self.registro_vendite = []
        self.avg_scorte = 0
        self.avg_vendite = 0

    def step(self):
        
        self.registro_scorte.append(self.scorta_banane)
        self.registro_vendite.append(self.prezzo)
        self.avg_scorte = (sum(self.registro_scorte))/len(self.registro_scorte)
        self.avg_vendite = (sum(self.registro_vendite))/len(self.registro_vendite)


    def vendi(n):
        '''
        n = numero di banane vendute 
        per ogni banana venduta aumento il numero di banane vendute
        e diminuisco la scorta di banane
        '''
        
        for i in range(n):
            self.banane_vendute += 1
            self.scorta_banane -= 1 


    def rifornimento(refill):
    
        '''
        ogni giorno il venditore riceve un rifornimento di banane 

        '''
        
        self.stock_banane = stock_banane + refill


    def prezzoseguente(scorta_banane, banane_vendute, prezzo):
        
        '''
        v_shift = shift del prezzo dovuto alle vendite passate
        s_shifr = shift del prezzo dovuto alla scorta corrente 
        
        '''
        if self.scorta_banane < self.avg_scorte:
            s_shift = 0.1
        else:
            s_shift = - 0.1

        if self.banane_vendute < self.avg_vendite:
            v_shift = - 0.1
        else:
            v_shift = 0.1

        self.prezzo = self.prezzo + v_shift - s_shift
        
        
        

    

        
        

class Umarell(Agent):
    '''
    Un Umarell.
    
    Attributes:
        prezzo              (prezzo a cui vuole comprare)
        banane_ieri         (numero banane comprate ieri)
        banane_totali       (numero banane comprate totale)
        banane_scorta       (numero banane in scorta) 
        bisogno             (bisogno giornaliero)
        unique_id
    '''
    id_curr = 0
    agent_type = 'Umarell'
    def __init__(self, model, prezzo, bisogno, banane_iniziali, pos):
        '''
        Crea un Umarell.
        Args:
            prezzo: prezzo a cui compra
            n:      numero di venditori che incontra
        '''
        super().__init__(f'UMA_{Umarell.id_curr}', model)
        Umarell.id_curr += 1
        self.prezzo = prezzo
        self.banane_ieri = 0
        #self.banane_totali = 0
        self.bisogno_def = bisogno
        self.bisogno = bisogno
        self.banane_scorta = banane_iniziali
        self.pos = pos


    def start_day(self):
        """
        Start day at random position and reset bisogno
        """
        pos = random_cell(self.model.grid)
        self.model.grid.move_agent(self, pos)
        self.bisogno = self.bisogno_def
        
    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=False)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def compra(self, n):
        self.bisogno -= 1    
    
    def step(self):
        '''
        Ogni step si posiziona random nella griglia  e inizia a camminare
        vede i venditori più vicini
        decide se comprare o no 
        restock
        '''
        
        
        
        
        if self.bisogno > 0:
            #si muove in una casella se ha bisogno di banane 
            self.random_move()
            
            #controlla dentro la casella che venditori ci sono
            vicini = self.model.grid.get_cell_list_contents([self.pos])   
            vicini = [v for v in vicini if type(v) == Vucumpra]
             
            # TODO da cambiare che fa casini
            #in vicini ho i venditori di quella cella
            #if len(vicini) ==0:
                #self.random_move()  #se non ho venditori cambia posizione
            
            #nella lista di venditori cerco il venditore con prezzo minore   
             
            
            if len(vicini) != 0:
                vend_min = min(vicini, key=lambda v: v.prezzo)      
                
                # guardo il prezzo minimo e se uno gli sta bene compra una banana
                #if vend_min.prezzo >= self.prezzo :
                    #random.move()    #se il prezzo min non va bene cambia posizione  
                
                
                
                if self.prezzo <= vend_min.prezzo:
                    self.compra(1)
                    self.banane_oggi= self.banane_ieri + 1
                    
            #if self.bisogno  == 0:
            #passa il giorno bo
            
            

            
     
               
            
            




        
            

            
            
            
                



