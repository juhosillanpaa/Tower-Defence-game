'''
Created on 27.3.2017

@author: sillanj5
'''
import sys



from enemy import Enemy

class Round(object):
    def __init__(self,current_game, amount_of_enemys, type,enemy_health):
        super().__init__()
        
        self.current_game = current_game
        self.type = type
        self.enemy_health = enemy_health
        self.enemys = []
        self.amount_of_enemys = amount_of_enemys
        self.findStartingPoint()
        
        
    

    def findStartingPoint(self):
        
        for y in range(self.current_game.get_size()):
            if self.current_game.get_square(0,y).is_square_road():
                self.starting_point_y = y
            
     
    def get_amount_of_enemys(self):
        return self.amount_of_enemys
    
    def add_enemy_to_list(self,enemy):
        self.enemys.append(enemy)
    
    def reduce_enemy_amount(self):
        self.amount_of_enemys -=1
    
    def get_starting_point_y(self):
        return self.starting_point_y
    
        

        
        
        
        
        
        
        
        
        
        
        
    
    