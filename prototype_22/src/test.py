
import sys, os
import subprocess
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MyCashierModel:
    def __init__(self, user, phone):
        self.user = user
        self.phone = phone
        pass
class MyCashierView(QWidget):
    def __init__(self, model: MyCashierModel):
        super().__init__()

        self.m = model

        self.set_main_window()

    def set_main_window(self):
        self.set_navbar_box()
        self.set_extra_info_box()
        
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.navbar_scra,0,0)
        self.main_layout.addWidget(self.extra_info_box,1,0,1,2)
        self.setLayout(self.main_layout)

    def set_navbar_box(self):
        self.hide_navbar_toggle_button = [
            QPushButton(),
            QPushButton(),
        ]
        self.pos_page_button = QPushButton()
        self.transaction_page_button = QPushButton()
        self.logout_button = QPushButton()
        self.navbar_box = QGroupBox()
        self.navbar_layout = QVBoxLayout()
        self.navbar_layout.addWidget(self.hide_navbar_toggle_button[0],0,Qt.AlignmentFlag.AlignRight)
        self.navbar_layout.addWidget(self.hide_navbar_toggle_button[1],0,Qt.AlignmentFlag.AlignRight)
        self.navbar_layout.addWidget(self.pos_page_button)
        self.navbar_layout.addWidget(self.transaction_page_button)
        self.navbar_layout.addWidget(self.logout_button)
        self.navbar_box.setLayout(self.navbar_layout)
        self.navbar_scra = QScrollArea()
        self.navbar_scra.setWidget(self.navbar_box)
        pass
    
    def set_extra_info_box(self):
        self.current_cashier_label = QLabel()
        self.current_phone_label = QLabel()
        self.extra_info_box = QGroupBox()
        self.extra_info_layout = QHBoxLayout()
        self.extra_info_layout.addWidget(self.current_cashier_label)
        self.extra_info_layout.addWidget(self.current_phone_label)
        self.extra_info_box.setLayout(self.extra_info_layout)
        pass
class MyCashierController:
    def __init__(self, model: MyCashierModel, view: MyCashierView):
        self.v = view
        self.m = model


class MyCashierWindow:
    def __init__(self, user='test', phone='test'):
        self.model = MyCashierModel(user, phone)
        self.view = MyCashierView(self.model)
        self.controller = MyCashierController(self.model, self.view)

    def run(self):
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    cashier_window = MyCashierWindow(user='test', phone='test') # for testing only

    cashier_window.run()

    sys.exit(app.exec())