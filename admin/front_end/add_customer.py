import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class AddCustomer(QDialog):
    def __init__(self):
        super().__init__()

        self.create_content()

    def create_content(self):
        self.grid_layout = QGridLayout()

        self.sample_label = QLabel('CUSTOMER')
        
        # primary information
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText('Customer name')
        self.address = QLineEdit()
        self.address.setPlaceholderText('Address')
        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText('Phone number')
        self.customer_type = QLineEdit()
        self.customer_type.setPlaceholderText('Customer type')
        self.status = QLineEdit()
        self.status.setPlaceholderText('Status')

        self.save_customer_push_button = QPushButton('SAVE CUSTOMER')

        self.grid_layout.addWidget(self.customer_name, 0, 0)
        self.grid_layout.addWidget(self.address, 1, 0)
        self.grid_layout.addWidget(self.phone_number, 2, 0)
        self.grid_layout.addWidget(self.customer_type, 3, 0)
        self.grid_layout.addWidget(self.status, 4, 0)
        self.grid_layout.addWidget(self.save_customer_push_button, 5, 0)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AddCustomer()
    window.show()
    sys.exit(pos_app.exec())