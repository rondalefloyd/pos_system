import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CustomLabel(QLabel):
    data_saved = pyqtSignal()

    def __init__(self, reference='', text=''):
        super().__init__()

        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

class CustomPushButton(QPushButton):
    data_saved = pyqtSignal()

    def __init__(self, reference='', text=''):
        super().__init__()

        self.setText(text)

class CustomLineEdit(QLineEdit):
    data_saved = pyqtSignal()

    def __init__(self, reference='', placeholderText=''):
        super().__init__()

        self.setPlaceholderText(placeholderText)

class CustomTableWidget(QTableWidget):
    data_saved = pyqtSignal()

    def __init__(self, reference=''):
        super().__init__()

        if reference == 'cart_table':
            self.setColumnCount(4)
            self.setHorizontalHeaderLabels(['','','item_name','quantity'])

class CustomGroupBox(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self, reference=''):
        super().__init__()

        if reference == 'panel_b':
            self.setFixedWidth(400)

        if reference == 'panel_c':
            self.setFixedWidth(400)


class CustomTabWidget(QTabWidget):
    data_saved = pyqtSignal()

    def __init__(self, reference=''):
        super().__init__()

class CustomWidget(QWidget):
    data_saved = pyqtSignal()

    def __init__(self, reference=''):
        super().__init__()



