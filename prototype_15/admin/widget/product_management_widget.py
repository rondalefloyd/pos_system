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
        self.setStyleSheet("QLabel { padding: 5px; }")

        pass

class CustomPushButton(QPushButton):
    def __init__(self, ref='', text=''):
        super().__init__()
        
        self.setText(text)

class CustomTableWidget(QTableWidget):
    def __init__(self, ref=''):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setStyleSheet('''
            QTableWidget { border: 0px; }
            QHeaderView::section { border: 0px; }
            QTableWidget::item { border-bottom: 1px solid black; }
        ''')
        
        if ref == 'item_data_list':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['','bardcode','item_name','expire_dt','time_stamp'])

        elif ref == 'category_data_list':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['','item_name','item_type','brand','sales_group','supplier','time_stamp'])

        elif ref == 'item_price_data_list':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['','item_name','cost','sell_price','effective_dt'])

        elif ref == 'inventory_data_list':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['','item_name','available_stock','on_hand_stock','time_stamp'])

        
class CustomLineEdit(QLineEdit):
    def __init__(self, ref='', placeholderText=''):
        super().__init__()
        
        self.setPlaceholderText(placeholderText)

class CustomComboBox(QComboBox):
    def __init__(self, ref=''):
        super().__init__()
        
        if ref == 'ts_sorter':
            self.setStyleSheet("QComboBox { height: 30px; }")

            self.addItem('Today')
            self.addItem('Yesterday')
            self.addItem('Last 7 days')
            self.addItem('Last 30 days')
            self.addItem('This month')
            self.addItem('Last month')
            self.addItem('Custom')

        pass

class CustomDateEdit(QDateEdit):
    def __init__(self, ref=''):
        super().__init__()

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

class CustomScrollArea(QScrollArea):
    def __init__(self, ref=''):
        super().__init__()
        

class CustomGroupBox(QGroupBox):
    def __init__(self, ref=''):
        super().__init__()

        if ref == 'panel_a':
            pass

        if ref == 'panel_b':
            self.setStyleSheet("QGroupBox { background-color: #fff; }")
            self.setFixedWidth(350)
            pass

        elif ref == 'panel_c':
            pass

        elif ref == 'panel_d':
            pass


class CustomWidget(QWidget):
    def __init__(self, ref=''):
        super().__init__()
        
        pass

class CustomTabWidget(QTabWidget):
    def __init__(self, ref=''):
        super().__init__()
        
        self.setStyleSheet("QTabBar::tab { height: 30px; }")

        pass