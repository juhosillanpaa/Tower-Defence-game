'''
Created on 27.3.2017

@author: sillanj5

'''
from square import Square
from tower import Tower
import filereader

class Game(object):
    
    def __init__(self,size,square_size):
        
        self.square_size= square_size
        self.next_round=1
        self.rounds = []
        self.size = size
        self.squares = [None] * size
        for x in range(size):
            self.squares[x] =[None] * size
            for y in range(size):
                self.squares[x][y] = Square(x,y)
        
        self.towers = [] #lista torneista
        self.health = 10
        self.money = 250
        self.name = ""
        self.current_map = "MAP1" #oletusarvoinen aloitusmappi
        self.tower_waiting = False
        self.upgarade = False
    
    def zero_stats(self):
        self.health = 10
        self.money = 250
        self.towers =[]
        self.rounds = []
        self.next_round=1
        for x in range(self.size):
            self.squares[x] =[None] * self.size
            for y in range(self.size):
                self.squares[x][y] = Square(x,y)
        
    def set_name(self, new_name):
        self.name = new_name
    def add_map(self, new_map):
        self.current_map = new_map
    
    def get_size(self):
        return self.size
    
    def get_square(self,x,y):
        return self.squares[x][y]
    def get_money(self):
        return self.money
    def add_money(self, mon):
        self.money += mon
    def get_health(self):
        return self.health
    def reduce_health(self):
        #palauttaa True jos peli loppui
        self.health -=1
        if self.health <= 0:
            return True
        else:
            return False
   
    def get_square_size(self):
        return self.square_size
        
    def get_map(self):
        return self.current_map
    
    def buy_tower(self):
        if self.get_money() >= 100:        
            self.tower_waiting = True
            return True
            
        else:
            return False
    def implement_loaded_game(self, map, nxt_rnd, hp, money):
        self.current_map = map
        self.next_round = nxt_rnd
        self.health = hp
        self.money = money
        
    def is_tower_waiting(self):
        return self.tower_waiting
    def tower_is_placed(self,x,y):
        self.tower_waiting = False
        self.squares[x][y].square_put_tower()
        self.money -=100
        
    def place_tower(self,x,y):
        
        tower = Tower(x,y,1,self)
        
        self.towers.append(tower)
        return tower
        
    def add_loaded_tower(self,lvl,x,y):
        tower = Tower(x,y,lvl,self)
        self.towers.append(tower)
        self.squares[x][y].square_put_tower()
        
    def cancel_purchase(self):
        self.tower_waiting = False
    
    def get_towers(self):
        return self.towers
    def get_all_squares(self):
        return self.squares
    def add_round(self, round):
        self.rounds.append(round)
    
    def round_is_over(self):
        self.add_money(100)
        if self.next_round +1 < len(self.rounds):
            self.next_round +=1
            return False
        else:
            return True
           
            
    def wants_to_upgarade_tower(self):
        self.upgarade = True
        
    def get_upgarade(self, cost):
        if self.upgarade and self.money >= cost:
            self.money -= cost
            return True
        else:
            return False
    def upgaraded(self):
        self.upgarade = False
    
    def save_quit(self):
        filereader.save_game(self)
    
    
        
        
        
        
        
    
        
        