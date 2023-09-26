import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class MyStackedWidget(QStackedWidget):
    def __init__(self, stacked_widget_ref=''):
        super().__init__()

        if stacked_widget_ref == 'stacked_content_panel':
            self.setCurrentIndex(0)

class MyScrollArea(QScrollArea):
    def __init__(self, scroll_area_ref=''):
        super().__init__()


class MyTabWidget(QTabWidget):
    def __init__(self, widget_ref=''):
        super().__init__()

        
class MyTableWidget(QTableWidget):
    def __init__(self, table_widget_ref=''):
        super().__init__()
    
        pass
class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, table_widget_item_ref='', text=''):
        super().__init__()

        self.setText(text)
        
        if table_widget_item_ref == 'discount_percent':
            self.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

class MyWidget(QWidget):
    def __init__(self, widget_ref='', parent=None):
        super().__init__()


        pass
class MyGroupBox(QGroupBox):
    def __init__(self, group_box_ref=''):
        super().__init__()

        if group_box_ref == 'side_nav_panel':
            self.setStyleSheet('QGroupBox { border: 0px; border-right: 1px solid #aaa } ')
            self.setFixedWidth(170)

        pass
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
    def __init__(self, hbox_layout_ref=''):
        super().__init__()

        if hbox_layout_ref == 'manage_data_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            
        if hbox_layout_ref == 'action_nav_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if hbox_layout_ref == 'operation_status_layout':
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.setSpacing(50)
class MyGridLayout(QGridLayout):
    def __init__(self, grid_layout_ref=''):
        super().__init__()

        if grid_layout_ref == 'main_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        if grid_layout_ref == 'overview_pagination_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

class MyFormLayout(QFormLayout):
    def __init__(self, form_layout_ref=''):
        super().__init__()

        if form_layout_ref == 'side_nav_panel_layout':
            self.setSpacing(0)
            self.setContentsMargins(0,0,0,0)


class MyLabel(QLabel):
    def __init__(self, label_ref='', text=''):
        super().__init__()

        self.setText(text)
        self.setToolTip(text)

        if label_ref in [
            'promo_name_label',
            'promo_type_label',
            'discount_percent_label',
            'description_label'
        ]:
            self.setFixedWidth(100)

class MyPushButton(QPushButton):
    def __init__(self, push_button_ref='', text=''):
        super().__init__()

        self.setText(text)

        if push_button_ref in [
            'product_content_button',
            'promo_content_button',
            'customer_content_button',
            'user_content_button',
            'settings_content_button'
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