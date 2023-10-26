
import sys, os
import subprocess
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

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
        self.hide_navbar_toggle_button = [
            MyPushButton(object_name='toggle'),
            MyPushButton(object_name='untoggle'),
        ]
        self.pos_page_button = MyPushButton(text='POS')
        self.transaction_page_button = MyPushButton(text='Transaction')
        self.logout_button = MyPushButton(text='Logout')
        self.navbar_box = MyGroupBox()
        self.navbar_layout = MyVBoxLayout()
        self.navbar_layout.addWidget(self.hide_navbar_toggle_button[0],0,Qt.AlignmentFlag.AlignRight)
        self.navbar_layout.addWidget(self.hide_navbar_toggle_button[1],0,Qt.AlignmentFlag.AlignRight)
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
        self.v.hide_navbar_toggle_button[0].clicked.connect(lambda: self.on_hide_navbar_button_clicked(hide=True))
        self.v.hide_navbar_toggle_button[1].clicked.connect(lambda: self.on_hide_navbar_button_clicked(hide=False))
        self.v.pos_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=0))
        self.v.transaction_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=1))
        self.v.logout_button.clicked.connect(self.on_logout_button_clicked)

    def on_hide_navbar_button_clicked(self, hide=False):
        if hide is True:
            self.v.hide_navbar_toggle_button[0].hide()
            self.v.hide_navbar_toggle_button[1].show()
            self.v.navbar_scra.setFixedWidth(60)
        if hide is False:
            self.v.hide_navbar_toggle_button[0].show()
            self.v.hide_navbar_toggle_button[1].hide()
            self.v.navbar_scra.setFixedWidth(150)
        
        self.v.pos_page_button.setHidden(hide)
        self.v.transaction_page_button.setHidden(hide)
        self.v.logout_button.setHidden(hide)        

    def on_page_button_clicked(self, index):
        self.v.page_stcw.setCurrentIndex(index)

        self.v.pos_page_window.controller.sync_ui() if index == 0 else None
        self.v.transaction_page_window.controller.sync_ui() if index == 1 else None
        
        print(index)

    def on_logout_button_clicked(self):
        confirm = QMessageBox.question(self.v, 'Confirm', 'Are you sure you want to logout?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            self.v.close_signal.emit('logout')
            self.v.close()
            subprocess.run(['python', '-Xfrozen_modules=off', 'src/gui/login/login.py'])


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
    cashier_window = MyCashierWindow(user=sys.argv[1], phone=sys.argv[2])

    cashier_window.run()

    sys.exit(app.exec())