import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.schemas.reward_management_schema import *

class CustomLabel(QLabel):
    def __init__(self, text, reference=''):
        super().__init__()

        self.ref = reference
        
class CustomLineEdit(QLineEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

        if self.ref == 'points_rate':
            self.setText('0')
            self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        if self.ref == 'points_rate':
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

        self.reward_management_schema = RewardManagementSchema()

        self.ref = reference

        if reference == 'reward_name':
            self.setEditable(True)

        self.fillComboBox()
        
    def fillComboBox(self):
        data = self.reward_management_schema.fillRewardComboBox()
        
        if self.ref == 'reward_name': 
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
            self.setHorizontalHeaderLabels(['','','reward_name','description','points_reward'])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference
        
        if self.ref == 'panel_b':
            self.hide()
        