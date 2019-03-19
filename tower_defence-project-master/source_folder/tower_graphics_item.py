'''
Created on 4.5.2017

@author: sillanj5
'''
from PyQt5 import QtWidgets, QtGui, QtCore
from math import degrees, atan2

from tower import Tower

from PyQt5.QtWidgets import QGraphicsScene
class TowerGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    '''
    kuvaa tornin graafista esitysta, eli kolmiota.
    Tanne tulee esim mousepressevent jos otetaan mukaan, 
    seka tornin kaantyminen.
    
    '''
    def __init__(self, tower, square_size):
        super(TowerGraphicsItem, self).__init__()
        self.initUI(tower, square_size)
    def initUI(self, tower, square_size):
        self.tower = tower
        self.damage = self.tower.get_damage()
        self.last_target = None
        self.square_size = square_size
      
        self.constructPixmap('cannon_blue.png')
        self.updatePosition()
        self.updateColor()
        
        
        
    def is_ready(self):
        return self.tower.ready
    def add_last_target(self, enemy):
        self.last_target = enemy
    def get_x(self):
        return self.tower.get_x()
    def get_y(self):
        return self.tower.get_y()
        
    def constructPixmap(self, name):
        '''
        Luo kolmion, viimeinen rivi helpottaa kolmion kaantamisessa, mikali
        tallainen ominaisuus otetaan mukaan
        '''
        ss = self.square_size
        
        tower_image = QtGui.QPixmap(name)
        
        self.tower_image = tower_image.scaled(ss , ss )
        
        self.setPixmap(self.tower_image)
    
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)
      

    def updatePosition(self):
        #asetetaan torni oikealle paikalle:
        
        x = self.tower.get_x()
        y = self.tower.get_y()
        self.setPos((x*self.square_size), y*self.square_size )
        
    def updateRotation(self,ex,ey):
        '''
        Laittaa tornin osoittamaan kohti vihollista jota se aikoo ampua,
        parametrina vihollisen koordinaatit
        '''
        ex =ex + self.square_size/2
        ey = ey +self.square_size/2
        x = self.tower.x + self.square_size / 2
        
        y = self.tower.y + self.square_size / 2
        
        xDiff = x- ex
        yDiff = y - ey
        a = degrees(atan2(yDiff, xDiff))
        self.setRotation(a)
        
    def is_alive(self):
        return self.tower.alive
    
    def updateColor(self):
        lvl = self.tower.get_level()
        if lvl ==1:
            name = 'cannon_blue.png'
            
        elif lvl ==2:
            name = 'cannon_red.png'
        elif lvl == 3:
            name = 'cannon_black.png'
        self.constructPixmap(name)
        self.updatePosition()
        self.damage = self.tower.get_damage()
    
    def mousePressEvent(self, *args, **kwargs):
        if self.tower.get_current_game().get_upgarade(self.tower.get_cost()):
            self.tower.upgarade()
            self.updateColor()
        
        
            
        
        
        
        
        
        
        
        
        
        
        
        
        