
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.gui.widget.my_widget import *

class MyAdminModel:
    def __init__(self, user):
        self.user = user
        pass
class MyAdminView(MyWidget):
    def __init__(self, model: MyAdminModel):
        super().__init__(window_title='Admin')

        self.model = model

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
        self.product_page_button = MyPushButton(text='Product')
        self.promo_page_button = MyPushButton(text='Promo')
        self.reward_page_button = MyPushButton(text='Reward')
        self.customer_page_button = MyPushButton(text='Customer')
        self.cashier_page_button = MyPushButton(text='Cashier')
        self.settings_page_button = MyPushButton(text='Settings')
        self.navbar_box = MyGroupBox()
        self.navbar_layout = MyFormLayout()
        self.navbar_layout.addRow(self.product_page_button)
        self.navbar_layout.addRow(self.promo_page_button)
        self.navbar_layout.addRow(self.reward_page_button)
        self.navbar_layout.addRow(self.customer_page_button)
        self.navbar_layout.addRow(self.cashier_page_button)
        self.navbar_layout.addRow(self.settings_page_button)
        self.navbar_box.setLayout(self.navbar_layout)
        self.navbar_scra = MyScrollArea(object_name='navbar_scra')
        self.navbar_scra.setWidget(self.navbar_box)
        pass
    
    def set_page_stcw(self):
        self.product_page_window = MyGroupBox()
        self.promo_page_window = MyGroupBox()
        self.reward_page_window = MyGroupBox()
        self.customer_page_window = MyGroupBox()
        self.cashier_page_window = MyGroupBox()
        self.settings_page_window = MyGroupBox()
        self.page_stcw = MyStackedWidget()
        self.page_stcw.addWidget(self.product_page_window)
        self.page_stcw.addWidget(self.promo_page_window)
        self.page_stcw.addWidget(self.reward_page_window)
        self.page_stcw.addWidget(self.customer_page_window)
        self.page_stcw.addWidget(self.cashier_page_window)
        self.page_stcw.addWidget(self.settings_page_window)

    def set_extra_info_box(self):
        self.current_user_label = MyLabel(text=f"Current user: {self.model.user}")
        self.extra_info_box = MyGroupBox()
        self.extra_info_layout = MyHBoxLayout()
        self.extra_info_layout.addWidget(self.current_user_label)
        self.extra_info_box.setLayout(self.extra_info_layout)
        pass
class MyAdminController:
    def __init__(self, model: MyAdminModel, view: MyAdminView):
        self.view = view
        self.model = model

        self.set_navbar_box_conn()

    def set_navbar_box_conn(self):
        self.view.product_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=0))
        self.view.promo_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=1))
        self.view.reward_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=2))
        self.view.customer_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=3))
        self.view.cashier_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=4))
        self.view.settings_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=5))
    def on_page_button_clicked(self, index):
        print(index)

class MyAdminWindow:
    def __init__(self, user='test'):
        self.model = MyAdminModel(user)
        self.view = MyAdminView(self.model)
        self.controller = MyAdminController(self.model, self.view)

    def run(self):
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    admin_window = MyAdminWindow()

    admin_window.run()

    app.exec()