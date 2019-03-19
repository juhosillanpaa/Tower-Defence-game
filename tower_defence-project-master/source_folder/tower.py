'''
Created on 27.3.2017

@author: sillanj5
'''
class Tower(object):
    '''
    Kuvastaa tornia
    '''
    
    
    def __init__(self,x,y,lvl, game):
        self.level = lvl
       
        self.x = x
        self.y = y
    
        self.damage = 10
        self.range = 80
        self.cost = 150
        self.current_game = game
        self.alive = True
        self.checkLevel()
        self.ready = False
        
    
    
    def checkLevel(self):
        if self.level >1:
            self.cost += 150 * (self.level - 1)
            self.damage += 20 * (self.level - 1)
            
    def ready_to_shoot(self):
        self.ready = True
    
    def get_current_game(self):
        return self.current_game
        
    def get_level(self):
        return self.level
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    def get_damage(self):
        return self.damage
    
    def get_cost(self):
        return self.cost
    
    def move_to(self,x,y):
        self.current_game.squares[self.x][self.y].remove_tower()
        self.x =x
        self.y = y
        self.current_game.squares[self.x][self.y].square_put_tower()
    def destroy(self):
        self.alive = False
    
    def upgarade(self):
        self.level +=1
        self.damage += 20
        self.cost += 150
        self.current_game.upgaraded()
        