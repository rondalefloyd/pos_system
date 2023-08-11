import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from product_management import ProductManagement
from inventory_management import InventoryManagement
from customer_management import CustomerManagement
from user_management import UserManagement

class AdminMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.create_navbar()
        self.create_content()
        self.create_body()
    
    def click_navbar_button(self, index):
        self.content_stacked_widget.setCurrentIndex(index)

    def create_content(self): 
        self.content_stacked_widget = QStackedWidget()
        self.content_stacked_widget.setCurrentIndex(0)
        self.content_hbox_layout = QVBoxLayout()

        product_management_class = ProductManagement()
        inventory_management_class = InventoryManagement()
        customer_management_class = CustomerManagement()
        user_management_class = UserManagement()

        main_content_widget = QWidget()
        main_content_vbox_layout = QVBoxLayout()
        main_content_vbox_layout.addWidget(product_management_class)
        main_content_vbox_layout.addWidget(inventory_management_class)
        main_content_vbox_layout.addWidget(customer_management_class)
        main_content_vbox_layout.addWidget(user_management_class)

        main_content_widget.setLayout(main_content_vbox_layout)

        self.content_stacked_widget.addWidget(product_management_class)
        self.content_stacked_widget.addWidget(inventory_management_class)
        self.content_stacked_widget.addWidget(customer_management_class)
        self.content_stacked_widget.addWidget(user_management_class)
        


    def create_navbar(self):
        self.navbar_group_box = QGroupBox()
        self.navbar_vbox_layout = QVBoxLayout()

        self.product_push_button = QPushButton('Product')
        self.inventory_push_button = QPushButton('Inventory')
        self.customer_push_button = QPushButton('Customer')
        self.user_push_button = QPushButton('User')

        self.product_push_button.clicked.connect(lambda: self.click_navbar_button(0))
        self.inventory_push_button.clicked.connect(lambda: self.click_navbar_button(1))
        self.customer_push_button.clicked.connect(lambda: self.click_navbar_button(2))
        self.user_push_button.clicked.connect(lambda: self.click_navbar_button(3))

        self.navbar_vbox_layout.addWidget(self.product_push_button)
        self.navbar_vbox_layout.addWidget(self.inventory_push_button)
        self.navbar_vbox_layout.addWidget(self.customer_push_button)
        self.navbar_vbox_layout.addWidget(self.user_push_button)

        self.navbar_group_box.setLayout(self.navbar_vbox_layout)

    def create_body(self):
        

        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.navbar_group_box)
        self.hbox_layout.addWidget(self.content_stacked_widget)
        self.setLayout(self.hbox_layout)
        

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AdminMainWindow()
    window.show()
    sys.exit(pos_app.exec())