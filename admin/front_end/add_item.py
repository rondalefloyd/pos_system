import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class AddItem(QDialog):
    def __init__(self):
        super().__init__()

        self.create_content()

    def create_content(self):
        self.grid_layout = QGridLayout()

        self.sample_label = QLabel('PRODUCT')
        
        # primary information
        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText('Item name')
        self.barcode = QLineEdit()
        self.barcode.setPlaceholderText('Barcode')

        # categorize
        self.item_type = QComboBox()
        self.item_type.setEditable(True)
        self.brand = QComboBox()
        self.supplier = QComboBox()

        # pricing
        self.sales_group = QComboBox()
        self.sales_group.addItem('Retail')
        self.sales_group.addItem('Wholesale')

        self.item_price = QLineEdit()
        self.item_price.setPlaceholderText('Price')

        # validity
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate())

        self.effective_date = QDateEdit()
        self.effective_date.setCalendarPopup(True)
        self.effective_date.setDate(QDate.currentDate())

        self.save_item_push_button = QPushButton('SAVE ITEM')

        self.grid_layout.addWidget(self.item_name, 0, 0)
        self.grid_layout.addWidget(self.barcode, 1, 0)
        self.grid_layout.addWidget(self.item_type, 2, 0)
        self.grid_layout.addWidget(self.brand, 3, 0)
        self.grid_layout.addWidget(self.supplier, 4, 0)
        self.grid_layout.addWidget(self.sales_group, 5, 0)
        self.grid_layout.addWidget(self.item_price, 6, 0)
        self.grid_layout.addWidget(self.expiry_date, 7, 0)
        self.grid_layout.addWidget(self.effective_date, 8, 0)
        self.grid_layout.addWidget(self.save_item_push_button, 9, 0)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AddItem()
    window.show()
    sys.exit(pos_app.exec())