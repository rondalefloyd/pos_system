import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class MyScrollArea(QScrollArea):
    def __init__(self, scroll_area_ref=''):
        super().__init__()

        if scroll_area_ref == 'scrolling_edit_panel':
            self.setWidgetResizable(True)
            self.setFixedWidth(500)
            self.setStyleSheet('QScrollArea { border: 0px; border-left: 1px solid #aaa }')
            self.hide()

class MyTabWidget(QTabWidget):
    def __init__(self, widget_ref=''):
        super().__init__()
        
class MyTableWidget(QTableWidget):
    def __init__(self, table_widget_ref=''):
        super().__init__()

        if table_widget_ref == 'overview_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Promo name','Promo type','Discount percent','Description'])
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, table_widget_item_ref='', text=''):
        super().__init__()

        self.setText(text)

class MyWidget(QWidget):
    def __init__(self, widget_ref='', parent=None):
        super().__init__()

        if widget_ref == 'promo_window':
            self.setWindowTitle('Promo')
            self.setWindowState(Qt.WindowState.WindowMaximized)

        if widget_ref == 'overview_pagination_nav':
            self.setFixedWidth(500)

class MyGroupBox(QGroupBox):
    def __init__(self, group_box_ref=''):
        super().__init__()

class MyDialog(QDialog):
    def __init__(self, dialog_ref='', parent=None):
        super().__init__()

        self.setParent(parent)
        self.setWindowFlag(Qt.WindowType.Dialog)

        if dialog_ref == 'view_panel_dialog':
            self.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.setFixedWidth(400)
            self.adjustSize()


class MyVBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

class MyHBoxLayout(QHBoxLayout):
    def __init__(self, hbox_layout=''):
        super().__init__()

        if hbox_layout == 'manage_data_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            
        if hbox_layout == 'action_nav_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class MyGridLayout(QGridLayout):
    def __init__(self, grid_layout_ref=''):
        super().__init__()

        if grid_layout_ref == 'main_panel_layout':
            self.setContentsMargins(0,0,0,0)

        if grid_layout_ref == 'overview_pagination_layout':
            self.setSpacing(0)

class MyFormLayout(QFormLayout):
    def __init__(self):
        super().__init__()


class MyLabel(QLabel):
    def __init__(self, text=''):
        super().__init__()

        self.setText(text)

class MyPushButton(QPushButton):
    def __init__(self, push_button_ref='', text=''):
        super().__init__()

        self.setText(text)

        if push_button_ref in [
            'refresh_data_button',
            'delete_all_data_button',
            'import_data_button',
            'add_data_button'
        ]:
            pass

        if push_button_ref in [
            'edit_button',
            'view_button',
            'delete_button'
        ]:
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass

class MyLineEdit(QLineEdit):
    def __init__(self, line_edit_ref=''):
        super().__init__()

        if line_edit_ref == 'filter_field':
            self.setFixedWidth(500)

class MyTextEdit(QTextEdit):
    def __init__(self, textedit_ref=''):
        super().__init__()

class MyDateEdit(QDateEdit):
    def __init__(self):
        super().__init__()

class MyComboBox(QComboBox):
    def __init__(self, combo_box_ref=''):
        super().__init__()

        if combo_box_ref == 'promo_type_field':
            self.setEditable(True)