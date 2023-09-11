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

        if reference == 'page_label':
            self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        if reference in ['total_promo_label','total_promo_shown_label']:
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

class CustomLineEdit(QLineEdit):
    def __init__(self, reference='', placeholderText=''):
        super().__init__()

        self.setPlaceholderText(placeholderText)

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

        if reference in ['promo_name_field', 'promo_type_field']:
            self.setEditable(True)

        if reference == 'filter_by_date_field':
            self.addItem('Today')
            self.addItem('Yesterday')
            self.addItem('Last 7 days')
            self.addItem('Last 30 days')
            self.addItem('This month')
            self.addItem('Last month')
            self.addItem('All')

class CustomTextEdit(QTextEdit):
    def __init__(self, reference=''):
        super().__init__()

class CustomTableWidget(QTableWidget):
    def __init__(self, reference=''):
        super().__init__()

        if reference == 'list_table':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['','','promo_name','promo_type','discount_value','description','date_modified'])

            self.setEditTriggers(QAbstractItemView.EditTrigger(False))

            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

            for index in range(2, 7):
                self.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeMode.Stretch)
                self.horizontalHeaderItem(index).setTextAlignment(Qt.AlignmentFlag.AlignLeft)

            # self.horizontalHeaderItem(4).setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)




class CustomDateEdit(QDateEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())

class CustomProgressBar(QProgressBar):
    def __init__(self, reference=''):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.setFixedHeight(15)
        self.setTextVisible(False)
