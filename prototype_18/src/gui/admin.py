import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui.promo import PromoWindow
from gui.settings import SettingsWindow

from widget.admin import *

class AdminWindow(MyWidget):
    def __init__(self):
        super().__init__(widget_ref='promo_window')

        self.promo_window = PromoWindow()

        self.show_main_panel()
        self.default_values()


    def default_values(self):
        pass

    # region -- on_push_button_clicked
    def on_product_content_button_clicked(self):
        # self.stacked_content_panel.setCurrentIndex(0)
        pass
    def on_promo_content_button_clicked(self):
        self.stacked_content_panel.setCurrentIndex(0)

        self.promo_window.on_refresh_data_button_clicked()
        pass
    def on_customer_content_button_clicked(self):
        # self.stacked_content_panel.setCurrentIndex(2)
        pass
    def on_user_content_button_clicked(self):
        # self.stacked_content_panel.setCurrentIndex(3)
        pass
    def on_settings_content_button_clicked(self):
        self.stacked_content_panel.setCurrentIndex(1)
        
        pass
    # endregion -- on_push_button_clicked

    def show_stacked_content_panel(self):
        self.stacked_content_panel = MyStackedWidget(stacked_widget_ref='stacked_content_panel')

        self.promo_window = PromoWindow()
        self.settings_window = SettingsWindow()

        self.stacked_content_panel.addWidget(self.promo_window)
        self.stacked_content_panel.addWidget(self.settings_window)

    def show_side_nav_panel(self):
        self.side_nav_panel = MyGroupBox(group_box_ref='side_nav_panel')
        self.side_nav_panel_layout = MyFormLayout(form_layout_ref='side_nav_panel_layout')

        self.product_content_button = MyPushButton(push_button_ref='product_content_button', text='Product')
        self.product_content_button.clicked.connect(self.on_product_content_button_clicked)
        self.promo_content_button = MyPushButton(push_button_ref='promo_content_button', text='Promo')
        self.promo_content_button.clicked.connect(self.on_promo_content_button_clicked)
        self.customer_content_button = MyPushButton(push_button_ref='customer_content_button', text='Customer')
        self.customer_content_button.clicked.connect(self.on_customer_content_button_clicked)
        self.user_content_button = MyPushButton(push_button_ref='user_content_button', text='User')
        self.user_content_button.clicked.connect(self.on_user_content_button_clicked)
        self.settings_content_button = MyPushButton(push_button_ref='settings_content_button', text='Settings')
        self.settings_content_button.clicked.connect(self.on_settings_content_button_clicked)

        self.side_nav_panel_layout.addRow(self.product_content_button)
        self.side_nav_panel_layout.addRow(self.promo_content_button)
        self.side_nav_panel_layout.addRow(self.customer_content_button)
        self.side_nav_panel_layout.addRow(self.user_content_button)
        self.side_nav_panel_layout.addRow(self.settings_content_button)


        self.side_nav_panel.setLayout(self.side_nav_panel_layout)

    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(grid_layout_ref='main_panel_layout')

        self.show_side_nav_panel()
        self.show_stacked_content_panel()

        self.main_panel_layout.addWidget(self.side_nav_panel,0,0)
        self.main_panel_layout.addWidget(self.stacked_content_panel,0,1)
        self.setLayout(self.main_panel_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(pos_app.exec())
