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

        if scroll_area_ref == 'scrolling_manage_data_panel':
            self.setFixedWidth(500)
            self.setStyleSheet('QScrollArea { border: 0px; border-left: 1px solid #aaa }')
            self.hide()

class MyTabWidget(QTabWidget):
    def __init__(self, widget_ref=''):
        super().__init__()

        
class MyTableWidget(QTableWidget):
    def __init__(self, table_widget_ref=''):
        super().__init__()
        
        self.setWordWrap(False)
        self.setShowGrid(False)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setStyleSheet('''
            QTableWidget { border: 0px; }
            QHeaderView::section { border: 0px; }
            QTableWidget::item { border: 0px; border-bottom: 1px solid #ccc; padding: 0px 20px }
        ''')

        if table_widget_ref == 'overview_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Item name','Brand','Sell price','Applied promo','Inventory tracking'])
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.verticalHeader().setVisible(False)

        pass
class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, table_widget_item_ref='', text=''):
        super().__init__()

        self.setText(text)
        
        if table_widget_item_ref in [
            'cost',
            'sell_price',
            'effective_dt',
            'promo_name',
            'discount_value'
        ]:
            self.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

class MyWidget(QWidget):
    def __init__(self, widget_ref='', parent=None):
        super().__init__()

        if widget_ref == 'product_window':
            self.setWindowTitle('Promo')
            self.setWindowState(Qt.WindowState.WindowMaximized)

        if widget_ref == 'overview_pagination_nav':
            self.setFixedWidth(500)

        pass
class MyGroupBox(QGroupBox):
    def __init__(self, group_box_ref=''):
        super().__init__()

        if group_box_ref == 'operation_status_panel':
            self.setStyleSheet('QGroupBox { border: 0px; border-top: 1px solid #aaa }')

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
    def __init__(self):
        super().__init__()


class MyLabel(QLabel):
    def __init__(self, label_ref='', text=''):
        super().__init__()

        self.setText(text)
        self.setToolTip(text)

        if label_ref in [
            # region -- conditions
            'barcode_label',
            'item_name_label',
            'expire_dt_label',
            
            'item_type_label',
            'brand_label',
            'sales_group_label',
            'supplier_label',

            'cost_label',
            'sell_price_label',
            'effective_dt_label',
            'promo_name_label',
            'promo_type_label',
            'discount_percent_label',
            'discount_value_label',
            'new_sell_price_label',
            'start_dt_label',
            'end_dt_label',

            'inventory_tracking_label',
            'available_stock_label',
            'on_hand_stock_label'
            # endregion -- conditions
        ]:
            self.setFixedWidth(150)

        if label_ref in [
            'promo_type_label',
            'discount_percent_label',
            'discount_value_label',
            'new_sell_price_label',
            'start_dt_label',
            'end_dt_label',

            'available_stock_label',
            'on_hand_stock_label'
            # checkpoint!!!
        ]:
            self.hide()

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

        if line_edit_ref in [
            'promo_type_field',
            'discount_percent_field',
            'discount_value_field',
            'new_sell_price_field'
        ]:
            self.setDisabled(True)

        if line_edit_ref in [
            'promo_type_field',
            'discount_percent_field',
            'discount_value_field',
            'new_sell_price_field',

            'available_stock_field',
            'on_hand_stock_field'
        ]:
            self.hide()

class MyTextEdit(QTextEdit):
    def __init__(self, textedit_ref=''):
        super().__init__()

class MyDateEdit(QDateEdit):
    def __init__(self, date_edit_ref=''):
        super().__init__()

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

        if date_edit_ref in [
            'start_dt_field',
            'end_dt_field'
        ]:
            self.hide()

class MyComboBox(QComboBox):
    def __init__(self, combo_box_ref=''):
        super().__init__()

        if combo_box_ref in [
            'item_type_field',
            'brand_field',
            'supplier_field'
        ]:
            self.setEditable(True)

        if combo_box_ref == 'sales_group_field':
            self.addItem('Retail')
            self.addItem('Wholesale')

        if combo_box_ref == 'promo_name_field':
            self.setCurrentIndex(0)
            self.insertItem(0, 'No promo')

        if combo_box_ref == 'inventory_tracking_field':
            self.addItem('Disabled')
            self.addItem('Enabled')
