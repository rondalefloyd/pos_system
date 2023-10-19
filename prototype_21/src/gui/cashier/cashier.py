
import sqlite3
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import QSSConfig
from src.gui.cashier.pos import MyPOSWindow
from src.gui.cashier.txn import MyTXNWindow
from src.widget.admin.admin import *


qss = QSSConfig()

class MyCashierModel:
    def __init__(self, name, phone):
        self.gdrive_path = 'G:' + f"/My Drive/"

        self.user_name = name
        self.user_phone = phone

    pass
class MyCashierView(MyWidget):
    def __init__(self, model: MyCashierModel):
        super().__init__()

        self.model = model

        self.set_main_panel()

    def set_main_panel(self):
        self.set_panel_a()
        self.set_panel_b()
        self.set_panel_c()
        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.panel_a_box,0,0)
        self.main_layout.addWidget(self.panel_b_stacked,0,1)
        self.main_layout.addWidget(self.panel_c_box,1,0,1,2)
        self.setLayout(self.main_layout)
        pass

    def set_panel_a(self):
        self.panel_a_box = MyGroupBox(object_name='panel_a_box')
        self.panel_a_layout = MyVBoxLayout(object_name='panel_a_layout')

        self.navbar_pos_button = MyPushButton(text='POS')
        self.navbar_txn_button = MyPushButton(text='Transactions')
        self.navbar_settings_button = MyPushButton(text='Settings')
        self.navbar_box = MyGroupBox()
        self.navbar_layout = MyFormLayout()
        self.navbar_layout.addWidget(self.navbar_pos_button)
        self.navbar_layout.addWidget(self.navbar_txn_button)
        self.navbar_layout.addWidget(self.navbar_settings_button)
        self.navbar_box.setLayout(self.navbar_layout)
        self.navbar_scra = MyScrollArea()
        self.navbar_scra.setWidget(self.navbar_box)

        self.panel_a_layout.addWidget(self.navbar_scra)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def set_panel_b(self):
        self.panel_b_stacked = MyStackedWidget()
        
        self.pos_content = MyPOSWindow(name=self.model.user_name, phone=self.model.user_phone)
        self.txn_content = MyTXNWindow(name=self.model.user_name, phone=self.model.user_phone)
        self.settings_content = QWidget()
        
        self.panel_b_stacked.setCurrentIndex(0)
        self.panel_b_stacked.addWidget(self.pos_content)
        self.panel_b_stacked.addWidget(self.txn_content)
        self.panel_b_stacked.addWidget(self.settings_content)
        pass
        pass

    def set_panel_c(self):
        self.panel_c_box = MyGroupBox()
        self.panel_c_layout = MyVBoxLayout()

        self.extra_info_current_user = MyLabel(text=f"Current user: {self.model.user_name} (Cashier)")
        self.extra_info_total_prodcut = MyLabel(text=f"Total: {'TEST'}")
        self.extra_info_box = MyGroupBox()
        self.extra_info_layout = MyHBoxLayout()
        self.extra_info_layout.addWidget(self.extra_info_current_user)
        self.extra_info_layout.addWidget(self.extra_info_total_prodcut)
        self.extra_info_box.setLayout(self.extra_info_layout)

        self.panel_c_layout.addWidget(self.extra_info_box)
        self.panel_c_box.setLayout(self.panel_c_layout)
    pass

class MyCashierController:
    def __init__(self, model: MyCashierModel, view: MyCashierView):
        self.view = view
        self.model = model

        self.set_panel_a_conn()

    def set_panel_a_conn(self):
        self.view.navbar_pos_button.clicked.connect(lambda: self.on_navbar_button_clicked(stack_index=0))
        self.view.navbar_txn_button.clicked.connect(lambda: self.on_navbar_button_clicked(stack_index=1))
    
    def on_navbar_button_clicked(self, stack_index):
        self.view.panel_b_stacked.setCurrentIndex(stack_index)
        self.view.pos_content.controller.start_sync_ui()
        self.view.txn_content.controller.start_sync_ui()
        print(stack_index)
    pass

class MyCashierWindow:
    def __init__(self, name, phone):
        self.model = MyCashierModel(name=name, phone=phone)
        self.view = MyCashierView(self.model)
        self.controller = MyCashierController(self.model, self.view)

    def run(self):
        self.view.show()
    pass

# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    cashier_window = MyCashierWindow(name='test-name', phone='test-phone')

    cashier_window.run()
    app.exec()