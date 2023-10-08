import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))

from src.core.color_scheme import *
from src.database.login.login import *
from src.widget.login.login import *

class LoginWindow(MyWidget):
    def __init__(self):
        super().__init__(object_name='login_window')

        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):
        pass
    def sync_ui(self):
        self.signup_form_panel.hide()
        self.login_form_replacement.hide()
        pass

    def on_signup_form_login_button_clicked(self):
        self.login_form_replacement.hide()
        self.signup_form_replacement.show()
        self.signup_form_panel.hide()
        self.login_form_panel.show()
        self.signup_form_panel.setDisabled(True)
        self.login_form_panel.setDisabled(False)
        pass
    def on_login_form_signup_button_clicked(self):
        self.login_form_replacement.show()
        self.signup_form_replacement.hide()
        self.signup_form_panel.show()
        self.login_form_panel.hide()
        self.signup_form_panel.setDisabled(False)
        self.login_form_panel.setDisabled(True)
        pass

    def show_signup_form_panel(self):
        self.signup_form_replacement = MyGroupBox(object_name='signup_form_replacement')
        self.signup_form_replacement_layout = MyGridLayout(object_name='signup_form_replacement_layout')
        self.signup_form_replacement_label = MyLabel(object_name='signup_form_replacement_label')
        self.signup_form_replacement_layout.addWidget(self.signup_form_replacement_label)
        self.signup_form_replacement.setLayout(self.signup_form_replacement_layout)

        self.signup_form_panel = MyGroupBox(object_name='signup_form_panel')
        self.signup_form_panel_layout = MyFormLayout(object_name='signup_form_panel_layout')

        self.signup_form_username_label = MyLabel(object_name='signup_form_username_label', text='Username')
        self.signup_form_phone_label = MyLabel(object_name='signup_form_phone_label', text='Phone')
        self.signup_form_password_label = MyLabel(object_name='signup_form_password_label', text='Password')

        self.signup_form_username_field = MyLineEdit(object_name='signup_form_username_field')
        self.signup_form_phone_field = MyLineEdit(object_name='signup_form_phone_field')
        self.signup_form_password_field = MyLineEdit(object_name='signup_form_password_field')

        self.signup_form_submit_button = MyPushButton(object_name='signup_form_submit_button', text='Signup')
        self.signup_form_login_button = MyPushButton(object_name='signup_form_login_button', text='Login')
        self.signup_form_login_button.clicked.connect(self.on_signup_form_login_button_clicked)

        self.signup_form_panel_layout.insertRow(0, MyLabel(object_name='signup_form_title', text='Sign up'))
        self.signup_form_panel_layout.insertRow(1, self.signup_form_username_label)
        self.signup_form_panel_layout.insertRow(3, self.signup_form_phone_label)
        self.signup_form_panel_layout.insertRow(5, self.signup_form_password_label)

        self.signup_form_panel_layout.insertRow(2, self.signup_form_username_field)
        self.signup_form_panel_layout.insertRow(4, self.signup_form_phone_field)
        self.signup_form_panel_layout.insertRow(6,self.signup_form_password_field)

        self.signup_form_panel_layout.insertRow(7, self.signup_form_submit_button)
        self.signup_form_panel_layout.insertRow(8, self.signup_form_login_button)
        self.signup_form_panel.setLayout(self.signup_form_panel_layout)
        pass
    def show_login_form_panel(self):
        self.login_form_replacement = MyGroupBox(object_name='login_form_replacement')
        self.login_form_replacement_layout = MyGridLayout(object_name='login_form_replacement_layout')
        self.login_form_replacement_label = MyLabel(object_name='login_form_replacement_label')
        self.login_form_replacement_layout.addWidget(self.login_form_replacement_label)
        self.login_form_replacement.setLayout(self.login_form_replacement_layout)

        self.login_form_panel = MyGroupBox(object_name='login_form_panel')
        self.login_form_panel_layout = MyFormLayout(object_name='login_form_panel_layout')

        self.login_form_username_label = MyLabel(object_name='login_form_username_label', text='Username')
        self.login_form_password_label = MyLabel(object_name='login_form_password_label', text='Password')

        self.login_form_username_field = MyLineEdit(object_name='login_form_username_field')
        self.login_form_password_field = MyLineEdit(object_name='login_form_password_field')

        self.login_form_submit_button = MyPushButton(object_name='login_form_submit_button', text='Login')
        self.login_form_signup_button = MyPushButton(object_name='login_form_signup_button', text='Sign up')
        self.login_form_signup_button.clicked.connect(self.on_login_form_signup_button_clicked)

        self.login_form_panel_layout.insertRow(0, MyLabel(object_name='login_form_title', text='Login'))
        self.login_form_panel_layout.insertRow(1, self.login_form_username_label)
        self.login_form_panel_layout.insertRow(3, self.login_form_password_label)

        self.login_form_panel_layout.insertRow(2, self.login_form_username_field)
        self.login_form_panel_layout.insertRow(4, self.login_form_password_field)

        self.login_form_panel_layout.insertRow(5, self.login_form_submit_button)
        self.login_form_panel_layout.insertRow(6, self.login_form_signup_button)
        self.login_form_panel.setLayout(self.login_form_panel_layout)
        pass


    def show_content_panel(self):
        self.content_panel = MyGroupBox(object_name='content_panel')
        self.content_panel_layout = MyGridLayout(object_name='content_panel_layout')

        self.show_login_form_panel()
        self.show_signup_form_panel()

        self.content_panel_layout.addWidget(self.login_form_panel,0,0)
        self.content_panel_layout.addWidget(self.login_form_replacement,0,0)
        self.content_panel_layout.addWidget(self.signup_form_panel,0,1)
        self.content_panel_layout.addWidget(self.signup_form_replacement,0,1)
        self.content_panel.setLayout(self.content_panel_layout)
        pass

    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(object_name='main_panel_layout')

        self.show_content_panel()

        self.main_panel_layout.addWidget(self.content_panel,0,0)
        self.setLayout(self.main_panel_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(pos_app.exec())
