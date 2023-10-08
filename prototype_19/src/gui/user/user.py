import sqlite3
import sys, os
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))
print('sys path: ', os.path.abspath(''))

# from src.database.user.user import *

from src.gui.user.sales_unfinished import *

from src.widget.user.user import *

class UserWindow(MyWidget):
    def __init__(self):
        super().__init__(object_name='user_window')


        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):

        self.my_push_button = MyPushButton()

        self.sales_window = SalesWindow()

    def sync_ui(self):
        self.uncollapse_right_button.hide()
        pass

    def style_side_nav_button(self, current_index):
        side_nav_button = [
            self.sales_window_button,
            self.transaction_window_button,
            self.settings_window_button
        ]
        
        for index, button in enumerate(side_nav_button):
            button.setStyleSheet(self.my_push_button.active_side_nav_button_ss) if index == current_index else button.setStyleSheet(self.my_push_button.inactive_side_nav_button_ss)
        
        self.collapse_left_button.setStyleSheet(self.my_push_button.collapse_button_ss)
        self.uncollapse_right_button.setStyleSheet(self.my_push_button.collapse_button_ss)

    def on_collapse_left_button_clicked(self):
        self.collapse_left_button.hide()
        self.uncollapse_right_button.show()
        self.sales_window_button.hide()
        self.transaction_window_button.hide()
        self.settings_window_button.hide()
        pass
    def on_uncollapse_right_button_clicked(self):
        self.collapse_left_button.show()
        self.uncollapse_right_button.hide()
        self.sales_window_button.show()
        self.transaction_window_button.show()
        self.settings_window_button.show()

    def on_sales_window_button_clicked(self):
        self.style_side_nav_button(0)
        self.stacked_panel.setCurrentIndex(0)
        pass
    def on_transaction_window_button_clicked(self):
        self.style_side_nav_button(1)
        self.stacked_panel.setCurrentIndex(1)
        pass
    def on_settings_window_button_clicked(self):
        self.style_side_nav_button(2)
        self.stacked_panel.setCurrentIndex(2)
        pass


    def show_stacked_panel(self):
        self.stacked_panel = MyStackedWidget()

        self.stacked_panel.addWidget(self.sales_window)

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

        self.sales_window_button = MyPushButton(object_name='sales_window_button', text='Sales')
        self.transaction_window_button = MyPushButton(object_name='transaction_window_button', text='Transaction')
        self.settings_window_button = MyPushButton(object_name='settings_window_button', text='Settings')

        self.collapse_left_button.clicked.connect(self.on_collapse_left_button_clicked)
        self.uncollapse_right_button.clicked.connect(self.on_uncollapse_right_button_clicked)

        self.sales_window_button.clicked.connect(self.on_sales_window_button_clicked)
        self.transaction_window_button.clicked.connect(self.on_transaction_window_button_clicked)
        self.settings_window_button.clicked.connect(self.on_settings_window_button_clicked)

        self.style_side_nav_button(0)

        self.side_nav_panel_layout.addRow(self.collapse_panel)
        self.side_nav_panel_layout.addRow(self.sales_window_button)
        self.side_nav_panel_layout.addRow(self.transaction_window_button)
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
    window = UserWindow()
    window.show()
    sys.exit(pos_app.exec())
