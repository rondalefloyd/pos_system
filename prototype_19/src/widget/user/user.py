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

        pass
class MyGroupBox(QGroupBox):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'side_nav_panel':
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{ background-color: #222; border: 0px }}
            """)
            pass
        if object_name == 'collapse_panel':
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{ border: 0px }}
            """)
        pass
class MyStackedWidget(QStackedWidget):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
        
        self.setCurrentIndex(0)
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

        if object_name == 'main_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        if object_name == 'collapse_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
        pass
class MyFormLayout(QFormLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
        pass

class MyLabel(QLabel):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)
        pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.collapse_button_ss = f"""
            QPushButton#collapse_left_button,
            QPushButton#uncollapse_right_button {{ background-color: #333; border: 0px; border-radius: 3px; padding: 3px }}
        """

        self.active_side_nav_button_ss = f"""
            QPushButton {{ background-color: rgba(225, 225, 225, 25); border: 0px; border-right: 3px solid {color_scheme.hex_main}; text-align: left; padding: 10px; color: #fff }}
        """
        self.inactive_side_nav_button_ss = f"""
            QPushButton {{ background-color: None; border: 0px; border-right: 3px solid #333; text-align: left; padding: 10px; color: #fff }}
            QPushButton:hover {{ background-color: rgba(225, 225, 225, 25); border-right: 3px solid {color_scheme.hex_main} }}
        """

        collapse_left_icon_path = os.path.abspath('src/icons/side_nav_panel/collapse_left.png')
        uncollapse_right_icon_path = os.path.abspath('src/icons/side_nav_panel/uncollapse_right.png')
        sales_icon_path = os.path.abspath('src/icons/side_nav_panel/sales.png')
        transaction_icon_path = os.path.abspath('src/icons/side_nav_panel/transaction.png')
        settings_icon_path = os.path.abspath('src/icons/side_nav_panel/settings.png')

        if object_name == 'collapse_left_button':
            self.setIcon(QIcon(collapse_left_icon_path))
            self.setIconSize(QSize(20,25))
            pass
        if object_name == 'uncollapse_right_button':
            self.setIcon(QIcon(uncollapse_right_icon_path))
            self.setIconSize(QSize(20,25))
            pass

        if object_name in [
            'sales_window_button',
            'transaction_window_button',
            'settings_window_button'
        ]:
            self.setFixedWidth(200)

        if object_name == 'sales_window_button':
            self.setIcon(QIcon(sales_icon_path))
            self.setIconSize(QSize(20,25))
            self.setText('    ' + text)
            pass
        if object_name == 'transaction_window_button':
            self.setIcon(QIcon(transaction_icon_path))
            self.setIconSize(QSize(20,25))
            self.setText('    ' + text)
            pass
        if object_name == 'settings_window_button':
            self.setIcon(QIcon(settings_icon_path))
            self.setIconSize(QSize(20,25))
            self.setText('    ' + text)
            pass

        if object_name in [
            'sales_window_button',
            'transaction_window_button',
            'settings_window_button'
        ]:
            # self.setStyleSheet(f"""
            #     QPushButton#{object_name} {{ border: 0px; text-align: left; padding: 10px; color: #fff }}
            #     QPushButton#{object_name}:hover {{ background-color: rgba(225, 225, 225, 25); }}
            # """)
            pass
        pass
