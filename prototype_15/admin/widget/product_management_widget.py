import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CustomLabel(QLabel):
    def __init__(self, ref='', text=''):
        super().__init__()

        self.setText(text)

        if ref in ['promo_active','inactive_display']:
            self.hide()

        elif ref == 'inventory_tracking_active':
            self.hide()

        pass

class CustomPushButton(QPushButton):
    def __init__(self, ref='', text=''):
        super().__init__()

        self.setText(text)

        if ref in ['filter_button','refresh_button']:
            self.setStyleSheet("QPushButton { height: 25px; }")

class CustomTableWidget(QTableWidget):
    def __init__(self, ref=''):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setDefaultSectionSize(50)
        self.setStyleSheet('''
            QTableWidget { border: 0px; }
            QHeaderView::section { border: 0px; padding: 0px 20px; }
            QTableWidget::item { border: 0px; border-bottom: 1px solid #ccc; padding: 0px 10px }
        ''')
        
        if ref == 'overview_data_list':
            self.setColumnCount(8)
            self.setHorizontalHeaderLabels(['','item_name','brand','sales_group','sell_price','promo','inventory_tracking','time_stamp'])

        elif ref == 'item_data_list':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['','bardcode','item_name','expire_dt','promo','time_stamp'])

        elif ref == 'category_data_list':
            self.setColumnCount(8)
            self.setHorizontalHeaderLabels(['','item_name','item_type','brand','sales_group','supplier','promo','time_stamp'])

        elif ref == 'item_price_data_list':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['','item_name','cost','sell_price','discount_value','promo','time_stamp'])

        elif ref == 'inventory_data_list':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['','item_name','inventory_tracking','available_stock','on_hand_stock','promo','time_stamp'])

        
class CustomLineEdit(QLineEdit):
    def __init__(self, ref='', placeholderText=''):
        super().__init__()

        self.setPlaceholderText(placeholderText)

        if ref == 'filter_field':
            self.setStyleSheet("QLineEdit { height: 30px; padding: 0px 5px; } ")
            pass

        elif ref in ['promo_active','inactive_display']:
            self.hide()
            self.setDisabled(True)

        elif ref == 'inventory_tracking_active':
            self.hide()

class CustomComboBox(QComboBox):
    def __init__(self, ref='', editable=False, disabled=False):
        super().__init__()

        self.setEditable(editable)
        self.setDisabled(disabled)

        if ref == 'ts_sorter':
            self.setStyleSheet("QComboBox { height: 25px; }")

            self.addItem('Today')
            self.addItem('Yesterday')
            self.addItem('Last 7 days')
            self.addItem('Last 30 days')
            self.addItem('This month')
            self.addItem('Last month')
            self.addItem('Custom')

        elif ref == 'sales_group':
            self.addItem('Retail')
            self.addItem('Wholesale')
        
        elif ref == 'promo_name':
            self.addItem('No promo')

        elif ref == 'inventory_tracking':
            self.addItem('Disabled')
            self.addItem('Enabled')

        pass

class CustomDateEdit(QDateEdit):
    def __init__(self, ref=''):
        super().__init__()

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

        if ref == 'promo_active':
            self.hide()

class CustomScrollArea(QScrollArea):
    def __init__(self, ref=''):
        super().__init__()


class CustomGroupBox(QGroupBox):
    def __init__(self, ref=''):
        super().__init__()

        if ref == 'panel_a':
            pass

        elif ref == 'panel_b':
            self.setStyleSheet("QGroupBox { background-color: #fff; }")
            self.setFixedWidth(350)
            pass

        elif ref == 'panel_c':
            pass

        elif ref == 'panel_d':
            pass

class CustomGridLayout(QGridLayout):
    def __init__(self, ref=''):
        super().__init__()

        if ref in ['manage_box_layout','modify_box_layout']:
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

class CustomWidget(QWidget):
    def __init__(self, ref=''):
        super().__init__()

        if ref == 'manage_box':
            self.setFixedWidth(70)

        pass

class CustomTabWidget(QTabWidget):
    def __init__(self, ref=''):
        super().__init__()

        self.setStyleSheet("QTabBar::tab { height: 30px; }")

        pass

class CustomProgressBar(QProgressBar):
    def __init__(self, reference=''):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.setFixedWidth(100)
        self.setTextVisible(False)