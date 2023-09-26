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

        self.setWidgetResizable(True)
        self.setStyleSheet('QScrollArea { border: 0px } ')

class MyTabWidget(QTabWidget):
    def __init__(self, tab_widget_ref=''):
        super().__init__()

        self.setStyleSheet("""
            QTabBar::tab { height: 30px; width: 100px; }
        """)


class MyTabBar(QTabBar):
    def __init__(self, tab_bar_ref=''):
        super().__init__()

        pass
class MyTableWidget(QTableWidget):
    def __init__(self, table_widget_ref=''):
        super().__init__()
        
        self.setWordWrap(False)
        self.setShowGrid(False)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setStyleSheet('''
            QTableWidget { background-color: #fff; border: 0px; }
            QHeaderView::section { border: 0px; }
            QTableWidget::item { border: 0px; border-bottom: 1px solid #ccc; padding: 0px 20px }
        ''')

        if table_widget_ref == 'overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Promo name','Promo type','Discount percent','Description','Date and time created'])
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.verticalHeader().setVisible(False)
        pass
class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, table_widget_item_ref='', text=''):
        super().__init__()

        self.setText(text)
        
        if table_widget_item_ref == 'discount_percent':
            self.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            pass
        if table_widget_item_ref == 'update_ts':
            self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

class MyWidget(QWidget):
    def __init__(self, widget_ref='', parent=None):
        super().__init__()

        if widget_ref == 'promo_window':
            self.setWindowTitle('Promo')
            self.setWindowState(Qt.WindowState.WindowMaximized)

        pass
class MyGroupBox(QGroupBox):
    def __init__(self, group_box_ref=''):
        super().__init__()

        if group_box_ref == 'content_panel':
            self.setStyleSheet('QGroupBox { border: 0px }')
            pass
        if group_box_ref == 'overview_pagination_container':
            self.setStyleSheet('QGroupBox { border-top: 1px solid #ddd }')
            pass
        if group_box_ref == 'overview_pagination_nav':
            self.setStyleSheet('QGroupBox { border: 0px }')
            self.setFixedWidth(500)

        if group_box_ref == 'operation_status_panel':
            self.setStyleSheet('QGroupBox { background-color: #fff; border: 0px; border-top: 1px solid #ddd }')

        if group_box_ref == 'manage_data_panel':
            self.setFixedWidth(400)
            self.setStyleSheet('QGroupBox { border: 0px; border-left: 1px solid #ddd } ')
            self.hide()

        if group_box_ref == 'primary_form':
            self.setStyleSheet('QGroupBox { background-color: #fff; border: 1px solid #ddd } ')

        if group_box_ref == 'form_nav':
            self.setStyleSheet('QGroupBox { border: 0px; border-top: 1px solid #ddd } ')


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
    def __init__(self, vbox_layout_ref=''):
        super().__init__()

        if vbox_layout_ref == 'manage_data_panel_layout':
            self.setSpacing(0)
            self.setContentsMargins(0,0,0,0)

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

        if grid_layout_ref == 'overview_pagination_container_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
            pass
        if grid_layout_ref == 'overview_pagination_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

class MyFormLayout(QFormLayout):
    def __init__(self, form_layout_ref=''):
        super().__init__()

        if form_layout_ref == 'form_container_layout':
            self.setContentsMargins(10,10,10,10)

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
            self.setFixedWidth(125)

class MyPushButton(QPushButton):
    def __init__(self, push_button_ref='', text=''):
        super().__init__()

        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if push_button_ref in [
            'save_new_button',
            'save_edit_button'
        ]:
            pass

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
            self.setPlaceholderText('Filter promo by name, type, discount percent, or description')
            self.setMinimumWidth(100)
            self.setMaximumWidth(500)

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