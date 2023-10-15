import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
from typing import List
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))


from src.core.qss_config import *
from src.widget.cashier.cashier import *

qss = QSSConfig()

class MyCashierModel: # IDEA: global variables and repetitive groupbox, layouts, dialogs
    def __init__(self):
        self.csv_path = 'G:' + f"/My Drive/csv/"

        self.current_user_value = ''

class MyCashierView(MyWidget):  # IDEA: groupbox, layouts, dialogs
    def __init__(self, model: MyCashierModel):
        super().__init__(object_name='my_sales_view')

        self.model = model

        self.set_main_panel()

    def set_main_panel(self):
        self.main_layout = MyGridLayout()
        
        self.set_panel_a()
        self.set_panel_b()
        self.set_panel_c()

        self.main_layout.addWidget(self.panel_a_box,0,0)
        self.main_layout.addWidget(self.panel_b_box,0,1)
        self.main_layout.addWidget(self.panel_c_box,1,0,1,2)
        self.setLayout(self.main_layout)
        pass

    def set_panel_a(self):
        self.panel_a_box = MyGroupBox()
        self.panel_a_layout = MyGridLayout()

        self.navbar_product_button = MyPushButton(text='POS')
        self.navbar_promo_button = MyPushButton(text='Transactions')
        self.navbar_customer_button = MyPushButton(text='Settings')
        self.navbar_box = MyGroupBox()
        self.navbar_layout = MyFormLayout()
        self.navbar_layout.addRow(self.navbar_product_button)
        self.navbar_layout.addRow(self.navbar_promo_button)
        self.navbar_layout.addRow(self.navbar_customer_button)
        self.navbar_box.setLayout(self.navbar_layout)

        self.panel_a_layout.addWidget(self.navbar_box)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def set_panel_b(self):
        self.panel_b_box = MyGroupBox()
        self.panel_b_layout = MyHBoxLayout()

        self.content_widget = MyStackedWidget()

        self.panel_b_layout.addWidget(self.content_widget)
        self.panel_b_box.setLayout(self.panel_b_layout)
        pass
    def set_panel_c(self):
        self.panel_c_box = MyGroupBox()
        self.panel_c_layout = MyHBoxLayout()
        
        self.current_user_label = MyLabel(text=f"Current user: {self.model.current_user_value} (Admin)")
        self.extra_info_box = MyGroupBox()
        self.extra_info_layout = MyHBoxLayout()
        self.extra_info_layout.addWidget(self.current_user_label)
        self.extra_info_box.setLayout(self.extra_info_layout)

        self.panel_c_layout.addWidget(self.extra_info_box)
        self.panel_c_box.setLayout(self.panel_c_layout)
        pass

class MyCashierController: # IDEA: connections, populations, on signals
    def __init__(self, model: MyCashierModel, view: MyCashierView):
        self.model = model
        self.view = view

class CashierApplication:
    def __init__(self):
        self.model = MyCashierModel()
        self.view = MyCashierView(self.model)
        self.controller = MyCashierController(self.model, self.view)

    def run(self):
        self.view.show()
