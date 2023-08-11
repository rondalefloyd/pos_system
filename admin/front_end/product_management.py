import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from add_item import AddItem

class ProductManagement(QWidget):
    def __init__(self):
        super().__init__()

        self.create_content()

    def show_add_item(self):
        self.add_item_dialogue = AddItem()
        self.add_item_dialogue.exec()

    def create_content(self):
        
        self.grid_layout = QGridLayout()
        
        # primary information
        self.filter_item = QLineEdit()
        self.add_item_push_button = QPushButton('ADD ITEM')
        self.add_item_push_button.clicked.connect(self.show_add_item)

        self.item_list_table = QTableWidget()
        self.item_list_table.setColumnCount(5)
        

        self.grid_layout.addWidget(self.filter_item, 0, 0)
        self.grid_layout.addWidget(self.add_item_push_button, 0, 1)
        self.grid_layout.addWidget(self.item_list_table, 1, 0, 2, 2)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagement()
    window.show()
    sys.exit(pos_app.exec())