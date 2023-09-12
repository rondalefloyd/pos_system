import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class CustomLabel(QLabel):
    def __init__(self, ref=''):
        super().__init__()

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
        self.setStyleSheet('QTableWidget::item { border-bottom: 1px solid black;}')
        
class CustomLineEdit(QLineEdit):
    def __init__(self, ref='', placeholderText=''):
        super().__init__()
        
        self.setPlaceholderText(placeholderText)

class CustomComboBox(QComboBox):
    def __init__(self, ref=''):
        super().__init__()
        
        pass

class CustomDateEdit(QDateEdit):
    def __init__(self, ref=''):
        super().__init__()

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())


class CustomGroupBox(QGroupBox):
    def __init__(self, ref=''):
        super().__init__()

        if ref == 'panel_a':
            pass

        elif ref == 'panel_b':
            pass

        elif ref == 'panel_c':
            pass

        elif ref == 'panel_d':
            pass


class CustomWidget(QWidget):
    def __init__(self, ref=''):
        super().__init__()
        
        pass

