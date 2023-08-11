import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class AddUser(QDialog):
    def __init__(self):
        super().__init__()

        self.create_content()

    def create_content(self):
        self.grid_layout = QGridLayout()

        self.sample_label = QLabel('USER')
        
        # primary information
        self.user_name = QLineEdit()
        self.user_name.setPlaceholderText('Username')

        self.save_user_push_button = QPushButton('SAVE USER')

        self.grid_layout.addWidget(self.user_name, 0, 0)
        self.grid_layout.addWidget(self.save_user_push_button, 5, 0)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AddUser()
    window.show()
    sys.exit(pos_app.exec())