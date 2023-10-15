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
from src.sql.login.login import *
from src.gui.cashier.cashier import *
from src.widget.login.login import *


schema = MyLoginSchema()
qss = QSSConfig()

class MyLoginModel: # IDEA: global variables
    def __init__(self):
        self.csv_path = 'G:' + f"/My Drive/csv/"

class MyLoginView(MyDialog):  # IDEA: groupbox, layouts, dialogs
    def __init__(self, model: MyLoginModel):
        super().__init__(object_name='my_sales_view')

        self.model = model

        self.set_main_panel()

    def set_main_panel(self):
        self.set_panel_a_box()

        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.panel_a_box)
        self.setLayout(self.main_layout)
        pass

    def set_panel_a_box(self):
        self.panel_a_box = MyGroupBox()
        self.panel_a_layout = MyFormLayout()
        
        self.login_label = MyLabel(text='POS')
        self.username_label = MyLabel(text='Username')
        self.username_field = MyLineEdit(object_name='username_field')
        self.password_label = MyLabel(text='Password')
        self.password_field = MyLineEdit(object_name='password_field')
        self.login_button = MyPushButton(text='Login')
        
        self.panel_a_layout.addRow(self.login_label)
        self.panel_a_layout.addRow(self.username_label)
        self.panel_a_layout.addRow(self.username_field)
        self.panel_a_layout.addRow(self.password_label)
        self.panel_a_layout.addRow(self.password_field)
        self.panel_a_layout.addRow(self.login_button)

        self.panel_a_box.setLayout(self.panel_a_layout)
        pass

class MyLoginController: # IDEA: connections, populations, on signals
    def __init__(self, model: MyLoginModel, view: MyLoginView):
        self.model = model
        self.view = view
        self.cashier_model = None
        self.cashier_view = None
        self.cashier_controller = None

        self.set_panel_a_box_conn()

    def set_panel_a_box_conn(self):
        self.view.login_button.clicked.connect(self.on_login_button_clicked)
        pass      
        
    def on_login_button_clicked(self):
        username = self.view.username_field.text()
        password = self.view.password_field.text()
        print('username:', username)
        print('password:', password)

        user_id = schema.get_user_id(username, password)
    

        if user_id > 0:
            # TODO: close the view and open the other view from the other file
            self.view.close()
            self.cashier_app = CashierApplication()

            self.cashier_app.run()
            pass
        else:
            pass
        pass

if __name__ == ('__main__'):
    login_app = QApplication(sys.argv)
    
    model = MyLoginModel()
    view = MyLoginView(model)
    controller = MyLoginController(model, view)
    
    view.show()

    sys.exit(login_app.exec())
