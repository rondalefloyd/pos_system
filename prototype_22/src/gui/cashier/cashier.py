
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.gui.cashier.pos import MyPOSWindow
from src.gui.cashier.transaction import MyTransactionWindow
from src.gui.widget.my_widget import *

class MyCashierModel:
    def __init__(self, user, phone):
        self.user = user
        self.phone = phone
        pass
class MyCashierView(MyWidget):
    def __init__(self, model: MyCashierModel):
        super().__init__(window_title='Cashier')

        self.m = model

        self.set_main_window()

    def set_main_window(self):
        self.set_navbar_box()
        self.set_page_stcw()
        self.set_extra_info_box()
        
        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.navbar_scra,0,0)
        self.main_layout.addWidget(self.page_stcw,0,1)
        self.main_layout.addWidget(self.extra_info_box,1,0,1,2)
        self.setLayout(self.main_layout)

    def set_navbar_box(self):
        self.pos_page_button = MyPushButton(text='POS')
        self.transaction_page_button = MyPushButton(text='Transaction')
        self.settings_page_button = MyPushButton(text='Settings')
        self.navbar_box = MyGroupBox()
        self.navbar_layout = MyFormLayout()
        self.navbar_layout.addRow(self.pos_page_button)
        self.navbar_layout.addRow(self.transaction_page_button)
        self.navbar_layout.addRow(self.settings_page_button)
        self.navbar_box.setLayout(self.navbar_layout)
        self.navbar_scra = MyScrollArea(object_name='navbar_scra')
        self.navbar_scra.setWidget(self.navbar_box)
        pass
    
    def set_page_stcw(self):
        self.pos_page_window = MyPOSWindow(self.m.user, self.m.phone)
        self.transaction_page_window = MyTransactionWindow(self.m.user, self.m.phone)
        self.settings_page_window = MyGroupBox()
        self.page_stcw = MyStackedWidget()
        self.page_stcw.addWidget(self.pos_page_window)
        self.page_stcw.addWidget(self.transaction_page_window)
        self.page_stcw.addWidget(self.settings_page_window)

    def set_extra_info_box(self):
        self.current_cashier_label = MyLabel(text=f"Cashier: {self.m.user}")
        self.current_phone_label = MyLabel(text=f"Phone: {self.m.phone}")
        self.extra_info_box = MyGroupBox()
        self.extra_info_layout = MyHBoxLayout()
        self.extra_info_layout.addWidget(self.current_cashier_label)
        self.extra_info_layout.addWidget(self.current_phone_label)
        self.extra_info_box.setLayout(self.extra_info_layout)
        pass
class MyCashierController:
    def __init__(self, model: MyCashierModel, view: MyCashierView):
        self.v = view
        self.m = model

        self.set_navbar_box_conn()

    def set_navbar_box_conn(self):
        self.v.pos_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=0))
        self.v.transaction_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=1))
        self.v.settings_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=2))
    def on_page_button_clicked(self, index):
        self.v.page_stcw.setCurrentIndex(index)
        print(index)

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
    cashier_window = MyCashierWindow()

    cashier_window.run()

    app.exec()