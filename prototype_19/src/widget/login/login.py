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

color_scheme = ColorScheme()


class MyScrollArea(QScrollArea):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
        pass
class MyWidget(QWidget):
    def __init__(self, object_name='', parent=None):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'login_window':
            # self.setFixedSize(600,400)
            pass


        pass
class MyGroupBox(QGroupBox):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name in [
            'signup_form_panel',
            'login_form_panel'
        ]:
            self.setStyleSheet(f"""
                QGroupBox#signup_form_panel {{ background-color: {color_scheme.hex_main}; border: 0px; }}
                QGroupBox#login_form_panel {{ border: 0px; }}

            """)
            
            self.setFixedSize(300,400)
        
        if object_name in [
            'signup_form_replacement',
            'login_form_replacement'
        ]:
            self.setStyleSheet(f"""
                QGroupBox#signup_form_replacement {{ background-color: {color_scheme.hex_main}; border: 0px; }}
                QGroupBox#login_form_replacement {{ border: 0px; }}
            """)
            
            self.setFixedSize(300,400)
        pass
class MyStackedWidget(QStackedWidget):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
        pass
class MyProgressDialog(QProgressDialog):
    def __init__(self, object_name='', parent=None):
        super().__init__()
        
        self.setObjectName(object_name)
        pass

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
        pass
class MyGridLayout(QGridLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

        pass
class MyFormLayout(QFormLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name in [
            'signup_form_panel_layout',
            'login_form_panel_layout'
        ]:
            self.setContentsMargins(25,25,25,25)
            
        pass

class MyLabel(QLabel):
    def __init__(self, object_name='', parent=None, text=''):
        super().__init__()
        
        self.setObjectName(object_name)
        self.setParent(parent)
        self.setText(text)

        if object_name in [
            'signup_form_title',
            'login_form_title'
        ]:
            self.setStyleSheet(f"""
                QLabel#signup_form_title {{ color: #fff; font-size: 20px; font-weight: bold }}
                QLabel#login_form_title {{ font-size: 20px; font-weight: bold }}
            """)

        if object_name == 'signup_form_replacement_label':
            background_file = os.path.abspath('src/background/static/signup_bg.jpg')

            pixmap = QPixmap(background_file)

            background_label = QLabel(self)
            background_label.setPixmap(pixmap)

        if object_name == 'login_form_replacement_label':
            background_file = os.path.abspath('src/background/static/signup_bg.jpg')

            pixmap = QPixmap(background_file)

            background_label = QLabel(self)
            background_label.setPixmap(pixmap)

        if object_name in [
            'signup_form_username_label',
            'signup_form_phone_label',
            'signup_form_password_label'
        ]:
            self.setStyleSheet(f"""
                QLabel#{object_name} {{ color: #fff }}
            """)
        pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if object_name in [
            'signup_form_submit_button',
            'login_form_submit_button'
        ]:
            self.setFixedHeight(35)
            self.setStyleSheet(f"""
                QPushButton#signup_form_submit_button {{ background-color: {color_scheme.hex_main_light}; border: 0px; border-radius: 2%; color: #fff; padding: 5px }}
                QPushButton#signup_form_submit_button:hover {{ background-color: {color_scheme.hex_main_light_hover} }}

                QPushButton#login_form_submit_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 2%; color: #fff; padding: 5px }}
                QPushButton#login_form_submit_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
            """)
        
        if object_name in [
            'signup_form_login_button',
            'login_form_signup_button'
        ]:
            self.setFixedHeight(35)
            self.setStyleSheet(f"""
                QPushButton#signup_form_login_button {{ background-color: {color_scheme.hex_main_heavy}; border: 0px; border-radius: 2%; color: #fff; padding: 5px }}
                QPushButton#signup_form_login_button:hover {{ background-color: {color_scheme.hex_main_heavy_hover} }}

                QPushButton#login_form_signup_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 2%; color: #222; padding: 5px }}
                QPushButton#login_form_signup_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
            """)
        pass
class MyComboBox(QComboBox):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)
        pass
class MyLineEdit(QLineEdit):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name in [
            'signup_form_username_field',
            'signup_form_phone_field',
            'signup_form_password_field',
            'login_form_username_field',
            'login_form_password_field'
        ]:
            self.setStyleSheet(f"""
                QLineEdit#{object_name} {{ padding: 3px 5px }}
            """)
        pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)
