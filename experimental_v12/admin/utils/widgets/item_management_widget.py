import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.schemas.item_management_schema import *
from utils.schemas.promo_management_schema import *

class CustomLabel(QLabel):
    def __init__(self, text, reference=''):
        super().__init__()

        self.ref = reference

        self.setText(text)

        if self.ref in [
            'current_barcode',
            'current_item_name',
            'current_expire_dt',
            'current_item_type',
            'current_brand',
            'current_sales_group',
            'current_supplier',
            'current_cost',
            'current_sell_price',
            'current_promo_name',
            'current_promo_type',
            'current_discount_percent',
            'current_discount_value',
            'current_new_sell_price',
            'current_start_dt',
            'current_end_dt',
            'current_effective_dt',
            'current_inventory_status',
            'current_available_stock',
            'current_on_hand_stock'
        ]:
            self.hide()
        
class CustomLineEdit(QLineEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference
        if reference in ['promo_type', 'discount_percent', 'discount_value','new_sell_price']:
            self.setDisabled(True)

        if self.ref in ['cost','discount_value','discount_percent','sell_price','new_sell_price','on_hand_stock','available_stock']:
            self.setText('0')
            self.textChanged.connect(self.handleTextChanged)

        if self.ref in [
            'current_barcode',
            'current_item_name',
            'current_expire_dt',
            'current_item_type',
            'current_brand',
            'current_sales_group',
            'current_supplier',
            'current_cost',
            'current_sell_price',
            'current_promo_name',
            'current_promo_type',
            'current_discount_percent',
            'current_discount_value',
            'current_new_sell_price',
            'current_start_dt',
            'current_end_dt',
            'current_effective_dt',
            'current_inventory_status',
            'current_available_stock',
            'current_on_hand_stock'
        ]:
            self.setDisabled(True)
            self.hide()

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        if self.ref in ['cost','discount_value','discount_percent','sell_price','new_sell_price','on_hand_stock','available_stock']:
            if event.text().isdigit() or event.key() == 16777219:  # Digit or Backspace key
                if self.text() == '0' and event.key() == 16777219:  # Backspace key
                    return
                if self.text() == '0' and event.text().isdigit():
                    self.setText(event.text())
                else:
                    super().keyPressEvent(event)

        # does nothing
        else:
            super().keyPressEvent(event)

class CustomTextEdit(QTextEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

class CustomComboBox(QComboBox):
    data_saved = pyqtSignal()
    def __init__(self, reference=''):
        super().__init__()

        self.item_management_schema = ItemManagementSchema()
        self.promo_management_schema = PromoManagementSchema()

        self.ref = reference

        if reference in ['item_name','item_type','brand','supplier']:
            self.setEditable(True)

        if reference == 'sales_group':
            self.addItem('Retail')
            self.addItem('Wholesale')

        if reference == 'promo_name':
            self.addItem('No promo')

        if reference == 'inventory_status':
            self.addItem('Not tracked')
            self.addItem('Tracked')

        self.fillComboBox()
        
    def fillComboBox(self):
        
        if self.ref == 'item_name': 
            data = self.item_management_schema.fillItemComboBox()
            self.clear()
            for row in data:
                self.addItem(row[0])

        if self.ref == 'item_type':
            data = self.item_management_schema.fillItemComboBox()
            self.clear()
            for row in data:
                self.addItem(row[1])

        if self.ref == 'brand':
            data = self.item_management_schema.fillItemComboBox()
            self.clear()
            for row in data:
                self.addItem(row[2])

        if self.ref == 'supplier':
            data = self.item_management_schema.fillItemComboBox()
            self.clear()
            for row in data:
                self.addItem(row[3])

        if self.ref == 'promo_name':
            data = self.promo_management_schema.fillPromoComboBox()
            self.clear()
            self.addItem('No promo')
            for row in data:
                self.addItem(row[0])

        self.data_saved.emit()
        
class CustomDateEdit(QDateEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

class CustomPushButton(QPushButton):
    def __init__(self, text, reference=''):
        super().__init__()

        self.setText(text)

        self.ref = reference

        if self.ref in ['add_button', 'edit_button']:
            self.hide()
        
class CustomTableWidget(QTableWidget):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference
        
        if reference == 'list_table':
            self.setColumnCount(15)
            self.setRowCount(50)
            self.setHorizontalHeaderLabels([
                '', # -- edit/view button
                '', # -- remove button
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
                'inventory_status'
            ])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference
        
        if self.ref == 'panel_b':
            self.hide()
        