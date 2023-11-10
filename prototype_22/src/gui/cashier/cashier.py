
import sys, os
import subprocess
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from src.gui.cashier.pos import MyPOSWindow
from src.gui.cashier.transaction import MyTXNWindow
from src.gui.admin.product import MyProductWindow
from src.gui.admin.customer import MyCustomerWindow
from src.gui.widget.my_widget import *

class MyCashierModel:
    def __init__(self, user, password, phone, level):
        self.user = user
        self.password = password
        self.phone = phone
        self.level = int(level)
        pass
class MyCashierView(MyWidget):
    def __init__(self, model: MyCashierModel):
        super().__init__(object_name='MyCashierView', window_title='Cashier')
        self.setWindowState(Qt.WindowState.WindowMaximized)

        self.m = model

        self.set_main_window()

    def set_main_window(self):
        self.set_navbar_box()
        self.set_page_stcw()
        self.set_extra_info_box()
        
        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.navbar_box,0,0)
        self.main_layout.addWidget(self.page_stcw,1,0)
        self.main_layout.addWidget(self.extra_info_box,2,0)
        self.setLayout(self.main_layout)

    def set_navbar_box(self):
        self.pos_page_button = MyPushButton(object_name='pos_page_button', text='  POS', disabled=True)
        self.transaction_page_button = MyPushButton(object_name='transaction_page_button', text='  Transaction')
        self.product_page_button = MyPushButton(object_name='product_page_button', text='  Product')
        self.customer_page_button = MyPushButton(object_name='customer_page_button', text='  Customer')
        self.logout_button = MyPushButton(object_name='logout_button', text='  Logout')
        self.navbar_box = MyGroupBox(object_name='navbar_box')
        self.navbar_layout = MyHBoxLayout(object_name='navbar_layout')
        self.navbar_layout.addWidget(self.pos_page_button)
        self.navbar_layout.addWidget(self.transaction_page_button)
        self.navbar_layout.addWidget(self.product_page_button)
        self.navbar_layout.addWidget(self.customer_page_button)
        self.navbar_layout.addWidget(QLabel(),4,Qt.AlignmentFlag.AlignLeft)
        self.navbar_layout.addWidget(self.logout_button,0,Qt.AlignmentFlag.AlignRight)
        self.navbar_box.setLayout(self.navbar_layout)

        print('self.m.level:', type(self.m.level), self.m.level)
        if self.m.level == 1: 
            print('self.m.level:', self.m.level)
            self.product_page_button.hide()
            self.customer_page_button.hide()
        elif self.m.level == 2: 
            print('self.m.level:', self.m.level)
            self.customer_page_button.show()
        elif self.m.level == 3: 
            print('self.m.level:', self.m.level)
            self.customer_page_button.show()

        pass
    
    def set_page_stcw(self):
        self.pos_page_window = MyPOSWindow(self.m.user, self.m.password, self.m.phone)
        self.transaction_page_window = MyTXNWindow(self.m.user, self.m.password, self.m.phone)
        self.product_page_window = MyProductWindow(self.m.user)
        self.customer_page_window = MyCustomerWindow(self.m.user, self.m.level)

        self.page_stcw = MyStackedWidget()
        self.page_stcw.addWidget(self.pos_page_window)
        self.page_stcw.addWidget(self.transaction_page_window)
        self.page_stcw.addWidget(self.product_page_window)
        self.page_stcw.addWidget(self.customer_page_window)

    def set_extra_info_box(self):
        self.current_cashier_label = MyLabel(object_name='current_cashier_label', text=f"Cashier: {self.m.user}")
        self.current_phone_label = MyLabel(object_name='current_phone_label', text=f"Phone: {self.m.phone}")
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
        self.v.product_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=2))
        self.v.customer_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=3))
        self.v.logout_button.clicked.connect(self.on_logout_button_clicked)

    def on_page_button_clicked(self, index):
        self.v.page_stcw.setCurrentIndex(index)

        self.v.pos_page_window.controller.sync_ui_handler() if index == 0 else None
        self.v.transaction_page_window.controller.sync_ui() if index == 1 else None
        self.v.product_page_window.controller.sync_ui() if index == 2 else None
        self.v.customer_page_window.controller.sync_ui() if index == 3 else None

        self.v.pos_page_button.setDisabled(index == 0)
        self.v.transaction_page_button.setDisabled(index == 1)
        self.v.product_page_button.setDisabled(index == 2)
        self.v.customer_page_button.setDisabled(index == 3)

    def on_logout_button_clicked(self):
        confirm = QMessageBox.question(self.v, 'Confirm', 'Are you sure you want to logout?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            self.v.close_signal.emit('logout')
            self.v.close()

class MyCashierWindow:
    def __init__(self, user='test', password='test', phone='test', level=0):
        self.model = MyCashierModel(user, password, phone, level)
        self.view = MyCashierView(self.model)
        self.controller = MyCashierController(self.model, self.view)

    def run(self):
        open('app_running.flag', 'w').close()
        self.view.showFullScreen()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    cashier_window = MyCashierWindow(user=sys.argv[1], password=sys.argv[2], phone=sys.argv[3], level=sys.argv[4])
    # cashier_window = MyCashierWindow(user='test', phone='test') # for testing only

    cashier_window.run()

    sys.exit(app.exec())