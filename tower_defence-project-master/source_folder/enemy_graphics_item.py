'''
Created on 4.5.2017

@author: sillanj5
'''
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QGraphicsPixmapItem
from enemy import Enemy

degrees={"EAST" :0, "SOUTH":90, "WEST":180, "NORTH":270}

class EnemyGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, enemy, square_size,x,y):
        super(EnemyGraphicsItem, self).__init__()
        self.initUI(enemy,square_size, x, y)
    def initUI(self,enemy,square_size,x,y):
        
        self.enemy = enemy
        self.square_size = square_size
        self.x = x
        self.y = y
        self.facing = "EAST"
        self.constructPixmap()
        self.updatePosition()
        
        
    def get_enemy_x(self):
        return self.x
    def get_enemy_y(self):
        return self.y
    def reduce_health(self, damage):
        
        return self.enemy.reduce_health(damage)
    
    def constructPixmap(self):
        
        ss = self.square_size
        
        car_image = QtGui.QPixmap(self.enemy.type +'.png')

        self.car_image = car_image.scaled(ss-10, ss-10)

        self.setPixmap(self.car_image)
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)
    def is_alive(self):
        return self.enemy.is_alive()
        
    
    def updatePosition(self):       
        self.x = self.enemy.get_enemy_x()
        self.y = self.enemy.get_enemy_y()
        
        ss = self.square_size
        self.setPos(self.x*ss +5 , self.y * ss +5)
    
    def updateRotation(self,new_direction):
        if new_direction != self.facing:
            self.setRotation(degrees[new_direction])
            self.facing = new_direction
            
        
        

        
    def enemy_timer_action(self):
        if self.x == 9:
            self.hide()
            return 1
        else:
            self.updateRotation(self.enemy.move())
            self.updatePosition()
            return 0
                
        
        
    
    
    
    
    
    
    
    
    
    