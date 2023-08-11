import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from add_customer import AddCustomer

class CustomerManagement(QWidget):
    def __init__(self):
        super().__init__()

        self.create_content()

    def show_add_customer(self):
        self.add_customer_dialogue = AddCustomer()
        self.add_customer_dialogue.exec()

    def create_content(self):
        
        self.grid_layout = QGridLayout()
        
        # primary information
        self.filter_customer = QLineEdit()
        self.add_customer_push_button = QPushButton('ADD CUSTOMER')
        self.add_customer_push_button.clicked.connect(self.show_add_customer)

        self.customer_list_table = QTableWidget()
        self.customer_list_table.setColumnCount(5)
        

        self.grid_layout.addWidget(self.filter_customer, 0, 0)
        self.grid_layout.addWidget(self.add_customer_push_button, 0, 1)
        self.grid_layout.addWidget(self.customer_list_table, 1, 0, 2, 2)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = CustomerManagement()
    window.show()
    sys.exit(pos_app.exec())