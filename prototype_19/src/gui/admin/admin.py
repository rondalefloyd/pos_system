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
from src.gui.admin.product import *
from src.gui.admin.promo import *
from src.widget.admin.admin import *

class AdminWindow(MyWidget):
    def __init__(self):
        super().__init__(object_name='admin_window')


        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):
        self.promo_schema = PromoSchema()
        self.product_schema = ProductSchema()
        self.my_push_button = MyPushButton()

    def sync_ui(self):
        pass

    def style_side_nav_button(self, current_index):
        side_nav_button = [
            self.product_window_button,
            self.promo_window_button,
            self.customer_window_button,
            self.user_window_button,
            self.settings_window_button
        ]
        
        for index, button in enumerate(side_nav_button):
            button.setStyleSheet(self.my_push_button.active_side_nav_button_ss) if index == current_index else button.setStyleSheet(self.my_push_button.inactive_side_nav_button_ss)

    def on_product_window_button_clicked(self):
        self.style_side_nav_button(0)
        self.stacked_panel.setCurrentIndex(0)
        pass
    def on_promo_window_button_clicked(self):
        self.style_side_nav_button(1)
        self.stacked_panel.setCurrentIndex(1)
        pass
    def on_customer_window_button_clicked(self):
        self.style_side_nav_button(2)
        self.stacked_panel.setCurrentIndex(2)
        pass
    def on_user_window_button_clicked(self):
        self.style_side_nav_button(3)
        self.stacked_panel.setCurrentIndex(3)
        pass
    def on_settings_window_button_clicked(self):
        self.style_side_nav_button(4)
        self.stacked_panel.setCurrentIndex(4)
        pass

    def show_stacked_panel(self):
        self.stacked_panel = MyStackedWidget()

        self.product_window = ProductWindow()
        self.promo_window = PromoWindow()

        self.stacked_panel.addWidget(self.product_window)
        self.stacked_panel.addWidget(self.promo_window)

        pass
    def show_side_nav_panel(self):
        self.side_nav_panel = MyGroupBox(object_name='side_nav_panel')
        self.side_nav_panel_layout = MyFormLayout()

        self.product_window_button = MyPushButton(object_name='product_window_button', text='Product')
        self.promo_window_button = MyPushButton(object_name='promo_window_button', text='Promo')
        self.customer_window_button = MyPushButton(object_name='customer_window_button', text='Customer')
        self.user_window_button = MyPushButton(object_name='user_window_button', text='User')
        self.settings_window_button = MyPushButton(object_name='settings_window_button', text='Settings')

        self.product_window_button.clicked.connect(self.on_product_window_button_clicked)
        self.promo_window_button.clicked.connect(self.on_promo_window_button_clicked)
        self.customer_window_button.clicked.connect(self.on_customer_window_button_clicked)
        self.user_window_button.clicked.connect(self.on_user_window_button_clicked)
        self.settings_window_button.clicked.connect(self.on_settings_window_button_clicked)

        self.style_side_nav_button(0)

        self.side_nav_panel_layout.addRow(self.product_window_button)
        self.side_nav_panel_layout.addRow(self.promo_window_button)
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
