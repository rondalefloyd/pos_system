
import sys, os
import subprocess
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(r'C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22')

from src.gui.cashier.pos import MyPOSWindow
from src.gui.cashier.transaction import MyTXNWindow
from src.gui.widget.my_widget import *

class MyCashierModel:
    def __init__(self, user, phone):
        self.user = user
        self.phone = phone
        pass
class MyCashierView(MyWidget):
    def __init__(self, model: MyCashierModel):
        super().__init__(object_name='MyCashierView', window_title='Cashier')

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
        self.pos_page_button = MyPushButton(object_name='pos_page_button', text='  POS', disabled=True)
        self.transaction_page_button = MyPushButton(object_name='transaction_page_button', text='  Transaction')
        self.logout_button = MyPushButton(object_name='logout_button', text='  Logout')
        self.navbar_box = MyGroupBox(object_name='navbar_box')
        self.navbar_layout = MyVBoxLayout(object_name='navbar_layout')
        self.navbar_layout.addWidget(self.pos_page_button)
        self.navbar_layout.addWidget(self.transaction_page_button)
        self.navbar_layout.addWidget(self.logout_button)
        self.navbar_box.setLayout(self.navbar_layout)
        self.navbar_scra = MyScrollArea(object_name='navbar_scra')
        self.navbar_scra.setWidget(self.navbar_box)
        pass
    
    def set_page_stcw(self):
        self.pos_page_window = MyPOSWindow(self.m.user, self.m.phone)
        self.transaction_page_window = MyTXNWindow(self.m.user, self.m.phone)
        self.settings_page_window = MyGroupBox()
        self.page_stcw = MyStackedWidget()
        self.page_stcw.addWidget(self.pos_page_window)
        self.page_stcw.addWidget(self.transaction_page_window)
        self.page_stcw.addWidget(self.settings_page_window)

    def set_extra_info_box(self):
        self.current_cashier_label = MyLabel(text=f"Cashier: {self.m.user}")
        self.current_phone_label = MyLabel(text=f"Phone: {self.m.phone}")
        self.extra_info_box = MyGroupBox(object_name='extra_info_box')
        self.extra_info_layout = MyHBoxLayout(object_name='extra_info_layout')
        self.extra_info_layout.addWidget(self.current_cashier_label,0,Qt.AlignmentFlag.AlignLeft)
        self.extra_info_layout.addWidget(self.current_phone_label,1,Qt.AlignmentFlag.AlignLeft)
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
        self.v.logout_button.clicked.connect(self.on_logout_button_clicked)

    def on_page_button_clicked(self, index):
        self.v.page_stcw.setCurrentIndex(index)

        self.v.pos_page_window.controller.sync_ui_handler() if index == 0 else None
        self.v.transaction_page_window.controller.sync_ui() if index == 1 else None

        self.v.pos_page_button.setDisabled(index == 0)
        self.v.transaction_page_button.setDisabled(index == 1)
                
        print(index)

    def on_logout_button_clicked(self):
        confirm = QMessageBox.question(self.v, 'Confirm', 'Are you sure you want to logout?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            self.v.close_signal.emit('logout')
            self.v.close()

class MyCashierWindow:
    def __init__(self, user='test', phone='test'):
        self.model = MyCashierModel(user, phone)
        self.view = MyCashierView(self.model)
        self.controller = MyCashierController(self.model, self.view)

    def run(self):
        open('app_running.flag', 'w').close()
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    cashier_window = MyCashierWindow(user=sys.argv[1], phone=sys.argv[2])
    # cashier_window = MyCashierWindow(user='test', phone='test') # for testing only

    cashier_window.run()

    sys.exit(app.exec())