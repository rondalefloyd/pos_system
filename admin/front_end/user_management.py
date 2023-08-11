import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from add_user import AddUser

class UserManagement(QWidget):
    def __init__(self):
        super().__init__()

        self.create_content()

    def show_add_user(self):
        self.add_user_dialogue = AddUser()
        self.add_user_dialogue.exec()

    def create_content(self):
        
        self.grid_layout = QGridLayout()
        
        # primary information
        self.filter_user = QLineEdit()
        self.add_user_push_button = QPushButton('ADD USER')
        self.add_user_push_button.clicked.connect(self.show_add_user)

        self.user_list_table = QTableWidget()
        self.user_list_table.setColumnCount(5)
        

        self.grid_layout.addWidget(self.filter_user, 0, 0)
        self.grid_layout.addWidget(self.add_user_push_button, 0, 1)
        self.grid_layout.addWidget(self.user_list_table, 1, 0, 2, 2)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = UserManagement()
    window.show()
    sys.exit(pos_app.exec())