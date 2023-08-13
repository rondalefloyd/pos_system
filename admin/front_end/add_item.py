import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from salesdb import SalesDBFunctions

class AddItem(QDialog):
    data_saved = pyqtSignal()

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
        self.brand.setEditable(True)
        self.supplier = QComboBox()
        self.supplier.setEditable(True)

        # pricing
        self.sales_group = QComboBox()
        self.sales_group.addItem('Retail')
        self.sales_group.addItem('Wholesale')

        self.cost = QLineEdit()
        self.cost.setPlaceholderText('Cost')
        self.discount = QLineEdit()
        self.discount.setPlaceholderText('Discount')
        self.sell_price = QLineEdit()
        self.sell_price.setPlaceholderText('Sell price')


        # validity
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate())

        self.effective_date = QDateEdit()
        self.effective_date.setCalendarPopup(True)
        self.effective_date.setDate(QDate.currentDate())

        self.track_inventory = QLabel('Track inventory?')
        self.option_y_radio_button = QRadioButton('Yes')
        self.option_y_radio_button.setChecked(True)
        self.option_y_radio_button.clicked.connect(lambda: self.inventory_option('Yes'))
        self.option_n_radio_button = QRadioButton('No')
        self.option_n_radio_button.clicked.connect(lambda: self.inventory_option('No'))

        self.on_hand = QLineEdit()
        self.on_hand.setPlaceholderText('On hand')
        self.available = QLineEdit()
        self.available.setPlaceholderText('Available')

        self.save_item_push_button = QPushButton('SAVE ITEM')
        self.save_item_push_button.clicked.connect(lambda: self.store_data(
            self.item_name, self.barcode, self.item_type, self.brand, self.supplier,
            self.sales_group, self.cost, self.discount, self.sell_price, self.expiry_date, self.effective_date))

        self.grid_layout.addWidget(self.item_name, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.barcode, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.item_type, 2, 0, 1, 2)
        self.grid_layout.addWidget(self.brand, 3, 0, 1, 2)
        self.grid_layout.addWidget(self.supplier, 4, 0, 1, 2)
        self.grid_layout.addWidget(self.sales_group, 5, 0, 1, 2)

        self.grid_layout.addWidget(self.cost, 6, 0, 1, 2)
        self.grid_layout.addWidget(self.discount, 7, 0, 1, 2)
        self.grid_layout.addWidget(self.sell_price, 8, 0, 1, 2)

        self.grid_layout.addWidget(self.expiry_date, 9, 0, 1, 2)
        self.grid_layout.addWidget(self.effective_date, 10, 0, 1, 2)
        self.grid_layout.addWidget(self.track_inventory, 11, 0, 1, 2)
        self.grid_layout.addWidget(self.option_y_radio_button, 12, 0)
        self.grid_layout.addWidget(self.option_n_radio_button, 12, 1)
        self.grid_layout.addWidget(self.on_hand, 13, 0, 1, 2)
        self.grid_layout.addWidget(self.available, 14, 0, 1, 2)
        self.grid_layout.addWidget(self.save_item_push_button, 15, 0, 1, 2)

        self.setLayout(self.grid_layout)

    def inventory_option(self, option):
        if option == 'No':
            self.on_hand.setEnabled(False)
            self.available.setEnabled(False)
        elif option == 'Yes':
            self.on_hand.setEnabled(True)
            self.available.setEnabled(True)

    def store_data(self, item_name, barcode, item_type, brand, supplier, sales_group, cost, discount, sell_price, expiry_date, effective_date):
        self.salesdb_functions = SalesDBFunctions()

        item_name = self.item_name.text()
        barcode = self.barcode.text()
        item_type = self.item_type.currentText()
        brand = self.brand.currentText()
        supplier = self.supplier.currentText()
        sales_group = self.sales_group.currentText()

        # Extract the input first
        cost_text = self.cost.text()
        discount_text = self.discount.text()
        sell_price_text = self.sell_price.text()

        # Convert the input to float or default to 0.00 if the input is empty
        cost = float(cost_text) if cost_text else 0.00
        discount = float(discount_text) if discount_text else 0.00
        sell_price = float(sell_price_text) if sell_price_text else 0.00
        

        expiry_date = self.expiry_date.date().toString(Qt.DateFormat.ISODate)
        effective_date = self.effective_date.date().toString(Qt.DateFormat.ISODate)
 
        self.salesdb_functions.insert_item_table(item_name, barcode, expiry_date)
        self.salesdb_functions.insert_item_type_table(item_type)
        self.salesdb_functions.insert_item_brand_table(brand)
        self.salesdb_functions.insert_supplier_table(supplier)
        self.salesdb_functions.insert_sales_group_table(sales_group)
        self.salesdb_functions.insert_item_price_table(cost, discount, sell_price, effective_date)

        # Emit the signal after data is saved
        self.data_saved.emit()

        self.accept()
        


if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AddItem()
    window.show()
    sys.exit(pos_app.exec())