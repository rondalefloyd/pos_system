import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=''):
        super().__init__()


        if reference == 'panel_d_box':
            self.hide()
            self.setFixedWidth(350)

class CustomLabel(QLabel):
    def __init__(self, reference='', text=''):
        super().__init__()
    
        self.setText(text)

        if reference in [
            'label_current_barcode',
            'label_current_item_name',
            'label_current_expire_dt',
            'label_current_item_type',
            'label_current_brand',
            'label_current_sales_group',
            'label_current_supplier',
            'label_current_cost',
            'label_current_sell_price',
            'label_current_promo_name',
            'label_promo_type',
            'label_current_promo_type',
            'label_discount_percent',
            'label_current_discount_percent',
            'label_discount_value',
            'label_current_discount_value',
            'label_new_sell_price',
            'label_current_new_sell_price',
            'label_start_dt',
            'label_current_start_dt',
            'label_end_dt',
            'label_current_end_dt',
            'label_current_effective_dt',
            'label_current_inventory_status',
            'label_available_stock',
            'label_current_available_stock',
            'label_on_hand_stock',
            'label_current_on_hand_stock'
        ]:
            self.hide()

        if reference == 'page_label':
            self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        if reference in ['total_promo_label','total_promo_shown_label']:
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

class CustomLineEdit(QLineEdit):
    def __init__(self, reference='', placeholderText=''):
        super().__init__()

        self.setPlaceholderText(placeholderText)

        if reference in [
            'current_barcode_field',
            'current_item_name_field',
            'current_expire_dt_field',
            'current_item_type_field',
            'current_brand_field',
            'current_sales_group_field',
            'current_supplier_field',
            'current_cost_field',
            'current_sell_price_field',
            'current_promo_name_field',
            'promo_type_field',
            'current_promo_type_field',
            'discount_percent_field',
            'current_discount_percent_field',
            'discount_value_field',
            'current_discount_value_field',
            'new_sell_price_field',
            'current_new_sell_price_field',
            'current_start_dt_field',
            'current_end_dt_field',
            'current_effective_dt_field',
            'current_inventory_status_field',
            'available_stock_field',
            'current_available_stock_field',
            'on_hand_stock_field',
            'current_on_hand_stock_field'
        ]:
            self.hide()
            self.setDisabled(True)



class CustomPushButton(QPushButton):
    def __init__(self, reference='', text=''):
        super().__init__()

        self.setText(text)
        
        if reference in ['add_button','import_button','back_button','refresh_button']:
            self.setFixedWidth(100)

        if reference in ['edit_button','delete_button']:
            self.setFixedWidth(30)


class CustomComboBox(QComboBox):
    def __init__(self, reference=''):
        super().__init__()

        if reference in ['item_name_field','item_type_field','brand_field','supplier_field']:
            self.setEditable(True)

        if reference == 'filter_by_date_field':
            self.addItem('Today')
            self.addItem('Yesterday')
            self.addItem('Last 7 days')
            self.addItem('Last 30 days')
            self.addItem('This month')
            self.addItem('Last month')
            self.addItem('All')

        if reference == 'sales_group_field':
            self.addItem('Retail')
            self.addItem('Wholesale')
            
        if reference == 'promo_name_field':
            self.setDisabled(True)

        if reference == 'inventory_status_field':
            self.addItem('Disable')
            self.addItem('Enable')

class CustomTextEdit(QTextEdit):
    def __init__(self, reference=''):
        super().__init__()

class CustomTableWidget(QTableWidget):
    def __init__(self, reference=''):
        super().__init__()

        if reference == 'list_table':
            self.setShowGrid(False)
            self.setColumnCount(16)
            self.setHorizontalHeaderLabels([
                '','',
                'barcode',
                'item_name',
                'expire_dt',
                'item_type',
                'brand',
                'sales_group',
                'supplier',
                'cost',
                'sell_price',
                'discount_value',
                'effective_dt',
                'promo_name',
                'inventory_status',
                'time_stamp'
            ])

            self.setEditTriggers(QAbstractItemView.EditTrigger(False))

            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

            self.horizontalHeaderItem(9).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.horizontalHeaderItem(10).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.horizontalHeaderItem(11).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

class CustomDateEdit(QDateEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

        if reference in ['start_dt_field','end_dt_field']:
            self.hide()

class CustomProgressBar(QProgressBar):
    def __init__(self, reference=''):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.setFixedHeight(15)
        self.setTextVisible(False)
