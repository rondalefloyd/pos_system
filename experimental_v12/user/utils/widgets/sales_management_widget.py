import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CustomLabel(QLabel):
    def __init__(self, text, reference=''):
        super().__init__()

        self.ref = reference

        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        
class CustomLineEdit(QLineEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        # if self.ref == 'discount_percent':
        #     if event.text().isdigit() or event.key() == 16777219:  # Digit or Backspace key
        #         if self.text() == '0' and event.key() == 16777219:  # Backspace key
        #             return
        #         if self.text() == '0' and event.text().isdigit():
        #             self.setText(event.text())
        #         else:
        #             super().keyPressEvent(event)

        # # does nothing
        # else:
        #     super().keyPressEvent(event)

        pass

class CustomTextEdit(QTextEdit):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

class CustomComboBox(QComboBox):
    data_saved = pyqtSignal()
    def __init__(self, reference=''):
        super().__init__()

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
            self.setColumnCount(6)
            self.setRowCount(50)
            self.setHorizontalHeaderLabels(['','','barcode','item_name','discount_value','description'])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

class CustomTabWidget(QTabWidget):
    def __init__(self, reference=''):
        super().__init__()

        self.ref = reference

        self.tab_content = CustomGroupBox()
        
        # self.setTabBar()

        self.setTabsClosable(True)
        self.setTabText(0, 'NICE')
        self.addTab(self.tab_content, 'Tab')




# Assuming CustomPushButton and CustomGroupBox classes are defined elsewhere.
