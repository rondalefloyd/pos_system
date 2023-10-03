import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))
print('sys path: ', os.path.abspath(''))

from src.database.admin.product import *
from src.database.admin.promo import *
from src.database.admin.reward import *
from src.database.admin.customer import *
from src.database.admin.user import *

from src.gui.admin.product import *
from src.gui.admin.promo import *
from src.gui.admin.reward import *
from src.gui.admin.customer import *
from src.gui.admin.user import *

from src.widget.admin.admin import *

class AdminWindow(MyWidget):
    def __init__(self):
        super().__init__(object_name='admin_window')


        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):
        self.product_schema = ProductSchema()
        self.promo_schema = PromoSchema()
        self.reward_schema = CustomerSchema()
        self.customer_schema = RewardSchema()
        self.user_schema = UserSchema()

        self.my_push_button = MyPushButton()

        self.product_window = ProductWindow()
        self.promo_window = PromoWindow()
        self.reward_window = RewardWindow()
        self.customer_window = CustomerWindow()
        self.user_window = UserWindow()

    def sync_ui(self):
        self.uncollapse_right_button.hide()

        pass

    def style_side_nav_button(self, current_index):
        side_nav_button = [
            self.product_window_button,
            self.promo_window_button,
            self.reward_window_button,
            self.customer_window_button,
            self.user_window_button,
            self.settings_window_button
        ]
        
        for index, button in enumerate(side_nav_button):
            button.setStyleSheet(self.my_push_button.active_side_nav_button_ss) if index == current_index else button.setStyleSheet(self.my_push_button.inactive_side_nav_button_ss)
        
        self.collapse_left_button.setStyleSheet(self.my_push_button.collapse_button_ss)
        self.uncollapse_right_button.setStyleSheet(self.my_push_button.collapse_button_ss)

    def on_collapse_left_button_clicked(self):
        self.collapse_left_button.hide()
        self.uncollapse_right_button.show()

        self.product_window_button.hide()
        self.promo_window_button.hide()
        self.reward_window_button.hide()
        self.customer_window_button.hide()
        self.user_window_button.hide()
        self.settings_window_button.hide()

        self.settings_window_button.hide()
        pass
    def on_uncollapse_right_button_clicked(self):
        self.collapse_left_button.show()
        self.uncollapse_right_button.hide()

        self.product_window_button.show()
        self.promo_window_button.show()
        self.reward_window_button.show()
        self.customer_window_button.show()
        self.user_window_button.show()
        self.settings_window_button.show()

        self.settings_window_button.show()


    def on_product_window_button_clicked(self):
        self.style_side_nav_button(0)
        self.stacked_panel.setCurrentIndex(0)
        self.product_window.sync_ui()
        pass
    def on_promo_window_button_clicked(self):
        self.style_side_nav_button(1)
        self.stacked_panel.setCurrentIndex(1)
        self.promo_window.sync_ui()
        pass
    def on_reward_window_button_clicked(self):
        self.style_side_nav_button(2)
        self.stacked_panel.setCurrentIndex(2)
        self.reward_window.sync_ui()
        pass
    def on_customer_window_button_clicked(self):
        self.style_side_nav_button(3)
        self.customer_window.sync_ui()
        self.stacked_panel.setCurrentIndex(3)
        pass
    def on_user_window_button_clicked(self):
        self.style_side_nav_button(4)
        self.user_window.sync_ui()
        self.stacked_panel.setCurrentIndex(4)
        pass
    def on_settings_window_button_clicked(self):
        self.style_side_nav_button(5)
        self.stacked_panel.setCurrentIndex(5)
        pass

    def show_stacked_panel(self):
        self.stacked_panel = MyStackedWidget()

        self.stacked_panel.addWidget(self.product_window)
        self.stacked_panel.addWidget(self.promo_window)
        self.stacked_panel.addWidget(self.reward_window)
        self.stacked_panel.addWidget(self.customer_window)
        self.stacked_panel.addWidget(self.user_window)

        pass
    def show_side_nav_panel(self):
        self.side_nav_panel = MyGroupBox(object_name='side_nav_panel')
        self.side_nav_panel_layout = MyFormLayout()

        self.collapse_panel = MyGroupBox(object_name='collapse_panel')
        self.collapse_panel_layout = MyGridLayout(object_name='collapse_panel_layout')
        self.collapse_left_button = MyPushButton(object_name='collapse_left_button')
        self.uncollapse_right_button = MyPushButton(object_name='uncollapse_right_button')
        self.collapse_panel_layout.addWidget(self.collapse_left_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.collapse_panel_layout.addWidget(self.uncollapse_right_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.collapse_panel.setLayout(self.collapse_panel_layout)

        self.product_window_button = MyPushButton(object_name='product_window_button', text='Product')
        self.promo_window_button = MyPushButton(object_name='promo_window_button', text='Promo')
        self.reward_window_button = MyPushButton(object_name='reward_window_button', text='Reward')
        self.customer_window_button = MyPushButton(object_name='customer_window_button', text='Customer')
        self.user_window_button = MyPushButton(object_name='user_window_button', text='User')
        self.settings_window_button = MyPushButton(object_name='settings_window_button', text='Settings')

        self.collapse_left_button.clicked.connect(self.on_collapse_left_button_clicked)
        self.uncollapse_right_button.clicked.connect(self.on_uncollapse_right_button_clicked)

        self.product_window_button.clicked.connect(self.on_product_window_button_clicked)
        self.promo_window_button.clicked.connect(self.on_promo_window_button_clicked)
        self.reward_window_button.clicked.connect(self.on_reward_window_button_clicked)
        self.customer_window_button.clicked.connect(self.on_customer_window_button_clicked)
        self.user_window_button.clicked.connect(self.on_user_window_button_clicked)
        self.settings_window_button.clicked.connect(self.on_settings_window_button_clicked)

        self.style_side_nav_button(0)

        self.side_nav_panel_layout.addRow(self.collapse_panel)
        self.side_nav_panel_layout.addRow(self.product_window_button)
        self.side_nav_panel_layout.addRow(self.promo_window_button)
        self.side_nav_panel_layout.addRow(self.reward_window_button)
        self.side_nav_panel_layout.addRow(self.customer_window_button)
        self.side_nav_panel_layout.addRow(self.user_window_button)
        self.side_nav_panel_layout.addRow(self.settings_window_button)
        self.side_nav_panel.setLayout(self.side_nav_panel_layout)
        pass
    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(object_name='main_panel_layout')

        self.show_side_nav_panel()
        self.show_stacked_panel()

        self.main_panel_layout.addWidget(self.side_nav_panel,0,0)
        self.main_panel_layout.addWidget(self.stacked_panel,0,1)
        self.setLayout(self.main_panel_layout)
    
if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(pos_app.exec())
