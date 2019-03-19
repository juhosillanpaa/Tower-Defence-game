'''
Created on 4.5.2017

@author: sillanj5
'''
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout,
                             QPushButton, QMenu, QLineEdit, QInputDialog)

import filereader
        
class Start_window(QWidget):
    '''
    luokka joka vastaa valiaikaisten ikkunoiden nayttamisesta
    ja pelin alustuksesta.
    '''
    def __init__(self, current_game,gui):
        super().__init__()
        self.iniUI(current_game,gui)
    def iniUI(self, current_game, gui):
        self.gui = gui
        self.current_game = current_game
        self.grid = QGridLayout()
        self.initButtons()
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('Tower defence')
        self.show()
    
    def initButtons(self):
        self.start_new_btn = QPushButton("Start new\ngame")
        self.start_new_btn.clicked.connect(self.start_new_game)
        
        self.load_game_btn = QPushButton("Load old\ngame")
        self.load_game_btn.clicked.connect(self.load_old_game)
        
        
        self.grid.addWidget(self.start_new_btn, 0, 0)
        self.grid.addWidget(self.load_game_btn, 0, 1)
        self.setLayout(self.grid)
        
    def load_old_game(self):
        self.start_new_btn.hide()
        self.load_game_btn.hide()
        found = False
        txt = "enter your name:"
        while not found:
            text, ok = QInputDialog.getText(self, 'Tower defence', txt)
            if ok:
                self.current_game.set_name(str(text))
                vastaus = filereader.load_game(self.current_game, str(text))
                if vastaus == -1:
                    txt = "Name not found, try again:"
                    continue
                else:
                    self.current_game =vastaus
                    found = True
                    self.end_starting() 
    def start_new_game(self):
      
        self.start_new_btn.hide()
        self.load_game_btn.hide()
        
        
        return self.showDialog()
    
    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Tower defence',
                                        'Enter name for game:' )
        if ok:
            self.current_game.set_name(str(text))
            
            self.show_different_maps()
            
            
    def show_different_maps(self):
        '''
        funktio joka luo graafisen valikon, jossa on lueteltu pelin kaikki
        kartat. Karttoja voi luoda lisaa kirjoittamalla niita itse gamefile.txt
        tiedostoon. piirtaa kolme pushbuttonia aina yhdelle riville,
        riveja voi olla kuinka paljon tahansa
        '''
        ''' 
        self.removeWidget(self.typetxt)
        '''
        
        self.kartat = filereader.get_different_maps()
        btn0 = QPushButton(self.kartat[0])
        btn1 = QPushButton(self.kartat[1])
        btn2 = QPushButton(self.kartat[2])
        btn3 = QPushButton(self.kartat[3])
        btn4 = QPushButton(self.kartat[4])
        btn5 = QPushButton(self.kartat[5])
       
        
        btn0.clicked.connect(self.add_map0)
        btn1.clicked.connect(self.add_map1)
        btn2.clicked.connect(self.add_map2)
        btn3.clicked.connect(self.add_map3)
        btn4.clicked.connect(self.add_map4)
        btn5.clicked.connect(self.add_map5)
        
        self.grid.addWidget(btn0,1,0)
        self.grid.addWidget(btn1,1,1)
        self.grid.addWidget(btn2,1,2)
        self.grid.addWidget(btn3,2,0)
        self.grid.addWidget(btn4,2,1)
        self.grid.addWidget(btn5,2,2)
        self.show()
    
    
    def add_map0(self):
        self.current_game.add_map(self.kartat[0])
        self.end_starting()
    def add_map1(self):
        self.current_game.add_map(self.kartat[1])
        self.end_starting()
    def add_map2(self):
        self.current_game.add_map(self.kartat[2])
        self.end_starting()
    def add_map3(self):
        self.current_game.add_map(self.kartat[3])
        self.end_starting()
    def add_map4(self):
        self.current_game.add_map(self.kartat[4])
        self.end_starting()
    def add_map5(self):
        self.current_game.add_map(self.kartat[5])
        self.end_starting()
    def end_starting(self):
        self.current_game = filereader.create_road(self.current_game)
        self.current_game = filereader.read_round_info(self.current_game)
        self.gui.add_game_graphics_items()
        self.gui.add_tower_graphics_items()
        self.close()
    
    def start_new_map(self):
        label = QLineEdit("You won!\n You can choose new map!")
        
        self.grid = QGridLayout()
        self.grid.addWidget(label,0,0)
        self.show_different_maps()
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('Tower defence- Choose new map')
        self.current_game.zero_stats()
        self.remove_old_stuff()

        self.show()  
    
    def remove_old_stuff(self):
        for item in self.gui.scene.items():
            self.gui.scene.removeItem(item)
        self.end_starting()
        
        
        
        
        