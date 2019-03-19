'''
Created on 5.4.2017

@author: sillanj5
'''
import math
from start_window import Start_window
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QApplication, QGraphicsPixmapItem
from game import Game
from square import Square
from tower import Tower
from enemy import Enemy
from round import Round
from tower_graphics_item import TowerGraphicsItem
from enemy_graphics_item import EnemyGraphicsItem
from backgroundgraphicsitem import BackgroundGraphicsItem
from PyQt5.Qt import (QGraphicsItem, QGraphicsRectItem, QBrush,
                      QColor, QHBoxLayout,QVBoxLayout, 
                      QGridLayout, QMessageBox, QApplication)

class GUI(QtWidgets.QMainWindow):
        
    def __init__(self, current_game = Game(10, 50)): 
        super().__init__()
        self.initUI(current_game)
        
    
    def initUI(self,current_game):
        
        self.current_game = current_game
        
        self.square_size = self.current_game.get_square_size()
        self.current_square = self.current_game.get_square(0,0)
        self.road_image ='sand.png'
        self.non_road_image = 'grass.png'
        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
    
        
        self.init_window()
        self.add_game_graphics_items()
        self.add_tower_graphics_items()
        self.init_buttons()
        
        self.timer = QtCore.QBasicTimer()
        self.enemytimer = QtCore.QBasicTimer()
        self.towertimer = QtCore.QBasicTimer()
        self.linetimer = QtCore.QBasicTimer()
        
        self.start_window = Start_window(self.current_game, self)
        
        
    def get_graphic_items(self, type_of_item):
        '''
        Metodi jolla saadaan type_of_item tyyppiset itemit scenesta
        '''
        items = []
        for item in self.scene.items():
            if type(item) is type_of_item:
                items.append(item)
            
        return items
        
    def add_new_tower_graphics_item(self, torni):
        item = TowerGraphicsItem(torni,self.square_size) 
        self.scene.addItem(item)
        
    def add_tower_graphics_items(self):
        '''
        Lisaa esimerkiksi ladatun pelin tornit peliin graafisiksi kuviksi
        '''
        towers_in_game = self.current_game.get_towers() 
        
        for torni in towers_in_game:
            item = TowerGraphicsItem(torni,self.square_size) 
            self.scene.addItem(item)
    def add_game_graphics_items(self):
        '''
        Lisaa pelilaudan graafiset kuvat
        '''
        ss = self.square_size
        size = self.current_game.size
        for x in range(size):
            for y in range(size):
                
                if self.current_game.squares[x][y].road:
                    item = BackgroundGraphicsItem(x,y,ss,self.road_image)
                else:
                    item = BackgroundGraphicsItem(x,y,ss,self.non_road_image)
                self.scene.addItem(item)
    
    def init_buttons(self):
        self.grid = QGridLayout()
        self.buy_tower_btn = QtWidgets.QPushButton("Buy new tower\ncost: 100\n")
        self.buy_tower_btn.clicked.connect(self.prepare_for_buying_tower)
        self.horizontal.addWidget(self.buy_tower_btn)
        
        self.save_quit_btn = QtWidgets.QPushButton("Save and Quit")
        self.save_quit_btn.clicked.connect(self.save_quit)
        self.horizontal.addWidget(self.save_quit_btn)
        
        self.start_round_btn = QtWidgets.QPushButton("\nStart Round\n")
        self.start_round_btn.clicked.connect(self.start_next_round)
        self.horizontal.addWidget(self.start_round_btn)
        
        self.upgarade_tower_btn = QtWidgets.QPushButton("Upgarade tower\ncost:\n150 / 300\n")
        self.upgarade_tower_btn.clicked.connect(self.wants_to_upgarade)
        self.horizontal.addWidget(self.upgarade_tower_btn)
        
        self.statuslabel = QLabel("health: {:d}\nmoney: {:d}\nRound: {:d}".format(self.current_game.health, self.current_game.money, self.current_game.next_round))
        
        self.grid.setSpacing(50)
        
        self.grid.addWidget(self.save_quit_btn,0,0)
        self.grid.addWidget(self.statuslabel,1,0)
        self.grid.addWidget(self.buy_tower_btn, 2 , 0)
        self.grid.addWidget(self.upgarade_tower_btn, 3, 0)
        self.grid.addWidget(self.start_round_btn,4,0)
        self.horizontal.addLayout(self.grid)
     
    def save_quit(self):
        #Taman funktion kautta peli suljetaan ja tallenetaan
        self.current_game.save_quit()
        self.close()   
    def wants_to_upgarade(self):
        self.current_game.wants_to_upgarade_tower()
    def prepare_for_buying_tower(self):
        if self.current_game.buy_tower():
            torni = self.current_game.place_tower( self.current_square.x, self.current_square.y)
            self.add_new_tower_graphics_item(torni)
            self.new_tower = torni
        
    
    def init_window(self):
    
        self.setGeometry(200, 200, 650, 550)
        self.setWindowTitle('Tower defence')
        self.show()
    
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 500, 500)
    
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        
        self.view.adjustSize()
        
        self.view.show()
        self.horizontal.addWidget(self.view)
        
    
    def keyPressEvent(self,e):
        '''
        Metodi, joka hoitaa eri nappainkomentojen kanssa toimimisen
        a,s,d,w - liikuttavat tornia
        q - pura ostos
        e - aseta torni
        esc - sulje ohjelma
        '''
        key = e.key()
            
        if key == Qt.Key_Escape:
            
            self.close()
            
        if not self.current_game.is_tower_waiting(): #Loput komennoista oleellisia vain jos ollaan sijoittamassa tornia
            return
        
        torni = self.new_tower
        
        if key ==Qt.Key_A:
            self.current_square = self.try_move(torni,self.current_square, -1,0)
        elif key == Qt.Key_D:
            self.current_square = self.try_move(torni, self.current_square,1,0)
        elif key == Qt.Key_W:           
            self.current_square = self.try_move(torni, self.current_square,0,-1)
        elif key == Qt.Key_S:
            self.current_square = self.try_move(torni, self.current_square,0,1)
        
        elif key == Qt.Key_E: 
            if self.current_square.is_free():
                self.current_game.tower_is_placed(self.new_tower.x, self.new_tower.y )
                self.new_tower.ready_to_shoot()
                self.new_tower = None
                self.update_info()
              
                
        elif key == Qt.Key_Q:
            self.current_game.cancel_purchase()
            self.new_tower.destroy() 
            self.new_tower = None
            for torni in self.get_graphic_items(TowerGraphicsItem):
                if not torni.is_alive():
                    self.scene.removeItem(torni)
            
    def update_info(self):
        '''
        Kaytetaan kun ostetaan torni, paastaan tason lapi, tai vihollinen paasee lapi puollustuksesta.
        Paivittaa statusLabelin
        '''
        self.statuslabel.setText("health: {:d}\nmoney: {:d}\nLap: {:d}".format(self.current_game.health, self.current_game.money, self.current_game.next_round))        
              
                
    def paint_square_to_normal(self, current_square):   
        x = self.current_square.get_x()
        y = self.current_square.get_y()
        ss = self.square_size
        
    
        if self.current_game.get_square(x,y).is_square_road():
            item = BackgroundGraphicsItem(x,y,ss,self.road_image)
        else:
            item = BackgroundGraphicsItem(x,y,ss,self.non_road_image)
        self.scene.addItem(item) 
        
      
            
    def try_move(self,torni, current_square, x1, y1):
        '''
        Liikuttaa ostettua tornia naytolla.
        '''
        
        x = current_square.get_x()
        y =current_square.get_y()
        ss = self.square_size
        
        mx = self.current_game.get_size()
        if x+x1 >= mx or x+x1 <0 or y+y1 <0 or y+y1 >= mx:
            return self.current_square
        else:
            self.new_square = self.current_game.get_square(x+x1, y+y1)
            torni.move_to(x+x1, y+y1)
            for torni in self.get_graphic_items(TowerGraphicsItem):
                torni.updatePosition()
            
            
      
            
        return self.new_square
    
    def start_next_round(self):
        
        nxt = self.current_game.next_round
        rounds = self.current_game.rounds
        if nxt > (len(rounds)+1):       
            self.close()
            
        self.round = rounds[nxt - 1]
    
        self.timer.start(1500,self)
        
        self.enemytimer.start(2000, self)
        self.towertimer.start(2100, self)
    

    
    def timerEvent(self,e):
        
        self.kierros_loppuu = False
       
        if e.timerId() ==self.timer.timerId():
            self.timer.stop()
          
            if self.round.get_amount_of_enemys() >0:
                aloitus_y = self.round.starting_point_y
                enemy = Enemy(self.current_game, self.round, 0, aloitus_y)
                self.round.add_enemy_to_list(enemy)
                item = EnemyGraphicsItem(enemy, self.square_size,0,aloitus_y)
                self.scene.addItem(item)
                self.round.reduce_enemy_amount()
                self.timer.start(500,self)

        if e.timerId() == self.enemytimer.timerId():
            self.enemytimer.stop()
            
            luku = 0
            for enemyitem in self.get_graphic_items(EnemyGraphicsItem):
                luku +=1
                if enemyitem.enemy_timer_action():
                    
                    #enemy timer action palauttaa True jos vihollinen paasee maaliin
                    self.scene.removeItem(enemyitem)
                    if self.current_game.reduce_health():
                        #reduce_health palauttaa True jos elamat ovat 0 tai alle
                        self.game_over()
                        return
                    self.update_info()
            if luku == 0:
                self.kierros_loppuu = True
            self.enemytimer.start(500, self)
 
 
        if e.timerId() ==self.linetimer.timerId():
            #huolehtii etta ammusten viivat nakyvat vain hetken
            self.linetimer.stop()
            for line in self.get_graphic_items(QtWidgets.QGraphicsLineItem):
                self.scene.removeItem(line)
                
        if e.timerId() == self.towertimer.timerId():
            self.towertimer.stop()
            for tower in self.get_graphic_items(TowerGraphicsItem):
                self.tower_shoot_enemys(tower)
                self.update_info()
            self.towertimer.start(1000, self)
            self.linetimer.start(100,self)
        
        if self.kierros_loppuu and self.round.get_amount_of_enemys() == 0:
            #varmistetaan etta kierros on todella loppu ja suljetaan timerit
            if not self.linetimer.isActive():
                
                if self.timer.isActive():
                    self.timer.stop()
                if self.enemytimer.isActive():
                    self.enemytimer.stop()
                if self.towertimer.isActive():
                    self.towertimer.stop()
                if self.linetimer.isActive():
                    self.linetimer.stop()
                if self.current_game.round_is_over():
                    self.start_window.start_new_map()
                self.update_info() 
         
    def tower_shoot_enemys(self, tower):
        '''
        Etsii tornin vihollisen ja ampuu sita.
        jokainen torni pyrkii ampumaan sita vihollista, jota se on ampunut jo
        '''
        if not tower.is_ready():
            return
        enemys = self.get_graphic_items(EnemyGraphicsItem)
        x = tower.get_x()
        y = tower.get_y()
        
        if tower.last_target != None and tower.last_target.is_alive():
            ex = tower.last_target.get_enemy_x()
            ey = tower.last_target.get_enemy_y()
            
            r = math.sqrt((x-ex)**2 + (y-ey)**2)
            if r<=3:
                tower.updateRotation(ex,ey)
                kuoli = tower.last_target.reduce_health(tower.damage)
                #palauttaa true jos vihollinen kuolee ammukseen
                self.show_ammo(tower, tower.last_target)
                if kuoli:
                    tower.last_target.hide()
                    self.scene.removeItem(tower.last_target)
                    tower.add_last_target(None)
                    self.current_game.add_money(10)
                                          
                return 
            
        for target in enemys:
            ex = target.get_enemy_x()
            ey = target.get_enemy_y()
            
            r = math.sqrt((x-ex)**2 + (y-ey)**2)
            if r<=3:
                tower.updateRotation(ex,ey)
                kuoli = target.reduce_health(tower.damage)
                self.show_ammo(tower,target)
                tower.add_last_target(target)
                if kuoli:
                    self.current_game.add_money(10)
                    tower.last_target.hide()
                    self.scene.removeItem(tower.last_target)
                    tower.add_last_target(None)
                return
    
    def show_ammo(self,tower , enemy):
        '''
        Metodi joka nayttaa tornin ampuman ammuksen viivana tornista viholliseen
        '''
        ss = self.square_size
        x = (tower.get_x() * ss) + (ss/2)
        y = (tower.get_y() * ss) + (ss/2)
        i = (enemy.get_enemy_x() * ss) +(ss/2)
        j = (enemy.get_enemy_y() * ss) + (ss/2)
        line = QtWidgets.QGraphicsLineItem(x,y,i,j)
        pen = QtGui.QPen(Qt.red, 2, Qt.SolidLine)
        line.setPen(pen)
        self.scene.addItem(line)
        
    def game_over(self):
        
        if self.timer.isActive():
            self.timer.stop()
        if self.towertimer.isActive():
            self.towertimer.stop()
        if self.linetimer.isActive():
            self.linetimer.stop()
        if self.enemytimer.isActive():
            self.enemytimer.stop()
        self.centralWidget().close()
        label = QLabel('Game Over', self)
        label.move(300,300)
        label.show()
        
       
        
    
    
                                
    
    
    
    
    
    