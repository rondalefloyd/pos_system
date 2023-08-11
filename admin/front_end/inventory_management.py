import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class InventoryManagement(QWidget):
    def __init__(self):
        super().__init__()

        self.create_body()

    def create_body(self):
        self.grid_layout = QGridLayout()

        self.sample_label = QLabel('INVENTORY')
        self.grid_layout.addWidget(self.sample_label, 0, 0)
        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = InventoryManagement()
    window.show()
    sys.exit(pos_app.exec())