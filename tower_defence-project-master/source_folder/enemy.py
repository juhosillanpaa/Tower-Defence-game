'''
Created on 27.3.2017

@author: sillanj5
'''
class Enemy(object):
    def __init__(self,current_game, round, x,y, ):
        self.current_game = current_game
        self.round = round
        self.health = self.round.enemy_health
        self.type = self.round.type
        self.x = x
        self.y = y
        self.last_x = None
        self.last_y = None
        
        
        
        
    
    def get_enemy_x(self):
        return self.x
    
    def get_enemy_y(self):
        return self.y
    
    def move(self):
        world = self.current_game.get_all_squares()
        mx = self.current_game.get_size()
        self.jatkuu = True
       
        
        if self.x+1 <mx:
            if world[self.x+1][self.y].is_square_road():
                self.check_is_last(1,0)
                direction = "EAST"
                
        if self.y-1 >= 0 and self.jatkuu:
            if world[self.x][self.y-1].is_square_road():
                self.check_is_last(0, -1)
                direction = "NORTH"
            
                
        if self.y+1 <mx and self.jatkuu:
            if world[self.x][self.y+1].is_square_road():
                self.check_is_last(0,1)
                direction = "SOUTH"
               
        if self.jatkuu:
         
            tempx = self.x
            tempy = self.y
            self.x = self.x-1
            
            self.last_x = tempx
            self.last_y = tempy
            direction = "WEST"
        return direction
        
    def reduce_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        else:
            return False
    
        
    
    def check_is_last(self, nx, ny):
        '''
        Tarkistetaan ettei auto jaa jumiin liikkuessaan alaspain,
        koska auto tarkistaa ensin onko ylapuolella oleva ruutu tyhja, eika
        siis jatkaisi muuten matkaa alaspain
        '''
       
        if (self.x + nx == self.last_x) and (self.y +ny == self.last_y):
            return
        else:
            self.remember_location_for_next_move()
            self.x = self.x + nx
            self.y = self.y + ny
            self.jatkuu= False
            
    def remember_location_for_next_move(self):
        self.last_x = self.x
        self.last_y = self.y
    
    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False
    