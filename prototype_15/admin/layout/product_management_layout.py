import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema.sales_table_schema import *
from widget.product_management_widget import *

class ProductManagementLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.createLayout()

    def on_push_button_clicked(self, index):
        pass

    def show_panel_b(self):
        self.panel_b = CustomGroupBox(ref='panel_b')
        form_layout = QFormLayout()

        self.back_button = CustomPushButton(text='Back')
        self.barcode = CustomLineEdit()
        self.item_name = CustomLineEdit()
        self.expire_dt = CustomDateEdit()
        self.save_button = CustomPushButton(text='Save')

        form_layout.addRow(self.back_button)
        form_layout.addRow('barcode', self.barcode)
        form_layout.addRow('item_name', self.item_name)
        form_layout.addRow('expire_dt', self.expire_dt)
        form_layout.addRow(self.save_button)

        self.panel_b.setLayout(form_layout)

    def show_panel_a(self):
        self.panel_a = CustomGroupBox(ref='panel_a')
        grid_layout = QGridLayout()
        
        self.filter_bar = CustomLineEdit(placeholderText='Filter by barcode, item name, item type, brand, sales group, supplier, inventory status, or promo name')
        self.filter_button = CustomPushButton(text='Filter')
        self.refresh_list_data = CustomPushButton(text='Refresh list')

        self.tab_sort = CustomTabWidget()
        self.ts_sort = CustomComboBox(ref='ts_sorter')
        self.item_data_list = CustomTableWidget(ref='item_data_list')
        self.category_data_list = CustomTableWidget(ref='category_data_list')
        self.item_price_data_list = CustomTableWidget(ref='item_price_data_list')
        self.inventory_data_list = CustomTableWidget(ref='inventory_data_list')

        self.total_data = CustomLabel(text='Total: 0')
        
        self.tab_sort.setCornerWidget(self.ts_sort, Qt.Corner.TopLeftCorner)
        self.tab_sort.addTab(self.item_data_list, 'By item')
        self.tab_sort.addTab(self.category_data_list, 'By category')
        self.tab_sort.addTab(self.item_price_data_list, 'By item price')
        self.tab_sort.addTab(self.inventory_data_list, 'By inventory')
        self.tab_sort.setCornerWidget(self.total_data, Qt.Corner.TopRightCorner)

        grid_layout.addWidget(self.filter_bar,0,1)
        grid_layout.addWidget(self.filter_button,0,2)
        grid_layout.addWidget(self.refresh_list_data,0,3)
        grid_layout.addWidget(self.tab_sort,2,0,1,4)


        self.panel_a.setLayout(grid_layout)

    def createLayout(self):
        # self.setWindowState(Qt.WindowState.WindowMaximized)

        grid_layout = QGridLayout()

        self.show_panel_a()
        self.show_panel_b()

        grid_layout.addWidget(self.panel_a,0,0)
        grid_layout.addWidget(self.panel_b,0,1)

        self.setLayout(grid_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagementLayout()
    window.show()
    sys.exit(pos_app.exec())
