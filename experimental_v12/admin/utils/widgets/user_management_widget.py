import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.schemas.user_management_schema import *

class CustomLabel(QLabel):
    def __init__(self, text, reference=''):
        super().__init__()

        self.ref = reference
        
class CustomLineEdit(QLineEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

class CustomTextEdit(QTextEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

class CustomComboBox(QComboBox):
    data_saved = pyqtSignal()
    def __init__(self, reference=''):
        super().__init__()

        self.user_management_schema = AccountsManagementSchema()

        self.ref = reference

        if reference == 'user_name':
            self.setEditable(True)

        if reference == 'access_level':
            self.addItem('1')
            self.addItem('2')

        self.fillComboBox()
        
    def fillComboBox(self):
        data = self.user_management_schema.fillUserComboBox()
        
        if self.ref == 'user_name': 
            self.clear()
            for row in data:
                self.addItem(row[0])

        self.data_saved.emit()
        
class CustomDateEdit(QDateEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference
        
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
            self.setColumnCount(5)
            self.setRowCount(50)
            self.setHorizontalHeaderLabels(['','','user_name','password','access_level'])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference
        
        if self.ref == 'panel_b':
            self.hide()
        