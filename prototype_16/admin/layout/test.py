import sqlite3
import sys, os
import pandas as pd
import threading
from datetime import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Test(QWidget):
    def __init__(self):
        super().__init__()
        
        self.box = QVBoxLayout()
        # self.icon = QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../import.png')), QSize(50,50))
        self.button = QPushButton()
        self.icon = QIcon()
        self.icon.addFile("C:/Users/Janjan/Documents/GitHub/pos_system/prototype_16/admin/icons/import.png", QSize(100,100))
        print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../admin/icons/import.png')))
        print("C:/Users/Janjan/Documents/GitHub/pos_system/prototype_16/admin/icons/import.png")
        self.button.setIcon(self.icon)
        self.box.addWidget(self.button)

        self.setLayout(self.box)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(pos_app.exec())
