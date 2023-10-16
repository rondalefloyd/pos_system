
import sqlite3
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import QSSConfig
from src.gui.admin.cust import MyCustWindow
from src.gui.admin.promo import MyPromoWindow
from src.gui.admin.reward import MyRewardWindow
from src.gui.admin.user import MyUserWindow
from src.widget.admin.admin import *

qss = QSSConfig()

class MyAdminModel:
    def __init__(self, name):
        self.gdrive_path = 'G:' + f"/My Drive/"

        self.user_name = name

    pass
class MyAdminView(MyWidget):
    def __init__(self, model: MyAdminModel):
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
        self.panel_a_box = MyGroupBox('panel_a_box')
        self.panel_a_layout = MyVBoxLayout('panel_a_layout')

        self.navbar_prod_button = MyPushButton(text='Product')
        self.navbar_promo_button = MyPushButton(text='Promo')
        self.navbar_reward_button = MyPushButton(text='Reward')
        self.navbar_cust_button = MyPushButton(text='Customer')
        self.navbar_user_button = MyPushButton(text='User')
        self.navbar_settings_button = MyPushButton(text='Settings')
        self.navbar_box = MyGroupBox()
        self.navbar_layout = MyFormLayout()
        self.navbar_layout.addWidget(self.navbar_prod_button)
        self.navbar_layout.addWidget(self.navbar_promo_button)
        self.navbar_layout.addWidget(self.navbar_reward_button)
        self.navbar_layout.addWidget(self.navbar_cust_button)
        self.navbar_layout.addWidget(self.navbar_user_button)
        self.navbar_layout.addWidget(self.navbar_settings_button)
        self.navbar_box.setLayout(self.navbar_layout)
        self.navbar_scra = MyScrollArea()
        self.navbar_scra.setWidget(self.navbar_box)

        self.panel_a_layout.addWidget(self.navbar_scra)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def set_panel_b(self):
        self.panel_b_stacked = MyStackedWidget()
        
        product_content = QWidget()
        promo_content = MyPromoWindow(name=self.model.user_name)
        reward_content = MyRewardWindow(name=self.model.user_name)
        cust_content = MyCustWindow(name=self.model.user_name)
        user_content = MyUserWindow(name=self.model.user_name)
        settings_content = QWidget()
        
        self.panel_b_stacked.setCurrentIndex(0)
        self.panel_b_stacked.addWidget(product_content)
        self.panel_b_stacked.addWidget(promo_content)
        self.panel_b_stacked.addWidget(reward_content)
        self.panel_b_stacked.addWidget(cust_content)
        self.panel_b_stacked.addWidget(user_content)
        self.panel_b_stacked.addWidget(settings_content)
        pass

    def set_panel_c(self):
        self.panel_c_box = MyGroupBox()
        self.panel_c_layout = MyVBoxLayout()

        self.extra_info_current_user = MyLabel(text=f"Current user: {self.model.user_name} (Admin)")
        self.extra_info_total_prodcut = MyLabel(text=f"Total: {'TEST'}")
        self.extra_info_box = MyGroupBox()
        self.extra_info_layout = MyHBoxLayout()
        self.extra_info_layout.addWidget(self.extra_info_current_user)
        self.extra_info_layout.addWidget(self.extra_info_total_prodcut)
        self.extra_info_box.setLayout(self.extra_info_layout)

        self.panel_c_layout.addWidget(self.extra_info_box)
        self.panel_c_box.setLayout(self.panel_c_layout)
    pass

class MyAdminController:
    def __init__(self, model: MyAdminModel, view: MyAdminView):
        self.view = view
        self.model = model

        self.set_panel_a_conn()

    def set_panel_a_conn(self):
        self.view.navbar_prod_button.clicked.connect(lambda: self.on_navbar_button_clicked(stack_index=0))
        self.view.navbar_promo_button.clicked.connect(lambda: self.on_navbar_button_clicked(stack_index=1))
        self.view.navbar_reward_button.clicked.connect(lambda: self.on_navbar_button_clicked(stack_index=2))
        self.view.navbar_cust_button.clicked.connect(lambda: self.on_navbar_button_clicked(stack_index=3))
        self.view.navbar_user_button.clicked.connect(lambda: self.on_navbar_button_clicked(stack_index=4))
        self.view.navbar_settings_button.clicked.connect(lambda: self.on_navbar_button_clicked(stack_index=5))
    
    def on_navbar_button_clicked(self, stack_index):
        self.view.panel_b_stacked.setCurrentIndex(stack_index)
        print(stack_index)
    pass

class MyAdminWindow:
    def __init__(self, name):
        self.model = MyAdminModel(name=name)
        self.view = MyAdminView(self.model)
        self.controller = MyAdminController(self.model, self.view)

    def run(self):
        self.view.show()
    pass

# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    admin_window = MyAdminWindow(name='test-name')

    admin_window.run()
    app.exec()