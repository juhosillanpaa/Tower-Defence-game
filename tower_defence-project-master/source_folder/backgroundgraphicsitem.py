'''
Created on 3.5.2017

@author: sillanj5
'''
from PyQt5 import QtWidgets, QtGui

class BackgroundGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, x,y,square_size, image_name):
        super(BackgroundGraphicsItem, self).__init__()
        self.initUI(x,y,square_size,image_name)
    def initUI(self,x,y,square_size,image_name):
        self.x = x
        self.y = y
        self.square_size = square_size
        self.image_name = image_name
        self.constructPixmap()
    
    def constructPixmap(self):
        self.image = QtGui.QPixmap(self.image_name)
        self.image = self.image.scaled(self.square_size, self.square_size)
        self.setPixmap(self.image)
        self.setPos(self.square_size * self.x, self.square_size * self.y)

        