'''
Created on 3.5.2017

@author: sillanj5
'''
from tower import Tower
class Square():
    def __init__(self,x,y,road = False):
        self.x = x
        self.y = y
        self.tower = False
       
        self.road= road #oletuksena pala ei kuulu tiehen
        
        
    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def is_square_road(self):
        return self.road
    
    def change_to_road(self):
        self.road= True
        
    def is_free(self):
        if not self.road:
            return True
        else:
            return False
    
    def square_put_tower(self):
        
        self.tower = True
        
        
    def add_in_range(self,tower):
        self.in_range.append(tower)
        
   
    def remove_tower(self):
        self.tower = False
        
    
       