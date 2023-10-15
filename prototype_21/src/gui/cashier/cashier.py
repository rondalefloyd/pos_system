
import sqlite3
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import QSSConfig
from src.widget.cashier.cashier import *

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
        self.main_layout.addWidget(self.panel_b_box,0,1)
        self.main_layout.addWidget(self.panel_c_box,1,0,1,2)
        self.setLayout(self.main_layout)
        pass

    def set_panel_a(self):
        self.panel_a_box = MyGroupBox()
        self.panel_a_layout = MyVBoxLayout()

        self.navbar_pos_button = MyPushButton(text='POS')
        self.navbar_transactions_button = MyPushButton(text='Transactions')
        self.navbar_settings_button = MyPushButton(text='Settings')
        self.navbar_box = MyGroupBox()
        self.navbar_layout = MyFormLayout()
        self.navbar_layout.addWidget(self.navbar_pos_button)
        self.navbar_layout.addWidget(self.navbar_transactions_button)
        self.navbar_layout.addWidget(self.navbar_settings_button)
        self.navbar_box.setLayout(self.navbar_layout)
        self.navbar_scra = MyScrollArea()
        self.navbar_scra.setWidget(self.navbar_box)

        self.panel_a_layout.addWidget(self.navbar_scra)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def set_panel_b(self):
        self.panel_b_box = MyGroupBox()
        self.panel_b_layout = MyVBoxLayout()
        
        pos_content = MyGroupBox() # TODO: replace with dedicated content 
        transactions_content = MyGroupBox() # TODO: replace with dedicated content
        settings_content = MyGroupBox() # TODO: replace with dedicated content
        
        self.content_stacked = MyStackedWidget()
        self.content_stacked.addWidget(pos_content)
        self.content_stacked.addWidget(transactions_content)
        self.content_stacked.addWidget(settings_content)

        self.panel_b_layout.addWidget(self.content_stacked)
        self.panel_b_box.setLayout(self.panel_b_layout)
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

    pass

class MyCashierWindow:
    def __init__(self, name, phone):
        self.model = MyCashierModel(name=name, phone=phone)
        self.view = MyCashierView(self.model)
        self.controller = MyCashierController(self.model, self.view)

    def run(self):
        self.view.show()
    pass

# # NOTE: For testing purpsoes only.
# if __name__ == ('__main__'):
#     app = QApplication(sys.argv)
#     cashier_window = MyCashierWindow()

#     cashier_window.run()
#     app.exec()