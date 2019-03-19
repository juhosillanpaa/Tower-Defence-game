'''
Created on 27.3.2017

@author: sillanj5
'''
import sys 
from PyQt5.QtWidgets import QApplication

from gui import GUI




def main():
    
    global app
    app = QApplication(sys.argv)
    gui = GUI()
    
    sys.exit(app.exec_())
    
        
if __name__ == '__main__':
    main()

                 
                
        
            
            
        
        
        