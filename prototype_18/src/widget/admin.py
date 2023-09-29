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
            self.setStyleSheet('QGroupBox { background-color: #1f2024; border: 0px } ')
            self.setFixedWidth(200)

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
            pass


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
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        product_button_icon = MyIcon(icon_ref='product_button_icon')
        promo_button_icon = MyIcon(icon_ref='promo_button_icon')
        customer_button_icon = MyIcon(icon_ref='customer_button_icon')
        user_button_icon = MyIcon(icon_ref='user_button_icon')
        settings_button_icon = MyIcon(icon_ref='settings_button_icon')

        if push_button_ref in [
            'product_content_button',
            'promo_content_button',
            'customer_content_button',
            'user_content_button',
            'settings_content_button'
        ]:
            self.setIconSize(QSize(25,25))
            self.setStyleSheet("""
                QPushButton { background-color: None; border: 0px; border-radius: 5px; text-align: left; color: #fff; padding: 10px }
                QPushButton::icon { margin: 220px; }
                QPushButton:hover { background-color: #303338 }
            """)
            pass
        if push_button_ref == 'product_content_button':
            self.setIcon(product_button_icon)

        if push_button_ref == 'promo_content_button':
            self.setIcon(promo_button_icon)

        if push_button_ref == 'customer_content_button':
            self.setIcon(customer_button_icon)

        if push_button_ref == 'user_content_button':
            self.setIcon(user_button_icon)

        if push_button_ref == 'settings_content_button':
            self.setIcon(settings_button_icon)

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


class MyIcon(QIcon):
    def __init__(self, icon_ref=''):
        super().__init__()

        if icon_ref == 'product_button_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/product.png')))

        if icon_ref == 'promo_button_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/promo.png')))

        if icon_ref == 'customer_button_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/customer.png')))

        if icon_ref == 'user_button_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/user.png')))

        if icon_ref == 'settings_button_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/settings.png')))