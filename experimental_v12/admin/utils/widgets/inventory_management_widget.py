import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.schemas.promo_management_schema import *

class CustomLabel(QLabel):
    def __init__(self, text, reference=''):
        super().__init__()

        self.ref = reference
        
class CustomLineEdit(QLineEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

        if self.ref == 'current_item_name':
            self.setDisabled(True)

        if self.ref in ['available_stock','on_hand_stock']:
            self.setText('0')
            self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        if self.ref in ['available_stock','on_hand_stock']:
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

        if self.ref == 'current_item_name':
            self.setDisabled(True)

class CustomComboBox(QComboBox):
    data_saved = pyqtSignal()
    def __init__(self, reference=''):
        super().__init__()

        self.promo_management_schema = PromoManagementSchema()

        self.ref = reference
        
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
            self.setHorizontalHeaderLabels(['','','item_name','available_stock','on_hand_stock'])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference
        
        if self.ref == 'panel_b':
            self.hide()
        