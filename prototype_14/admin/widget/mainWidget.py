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

        if reference == 'panel_a':
            self.setFixedWidth(200)

class CustomLabel(QLabel):
    def __init__(self, reference='', text=''):
        super().__init__()

        self.setText(text)

class CustomLineEdit(QLineEdit):
    def __init__(self, reference=''):
        super().__init__()

class CustomPushButton(QPushButton):
    def __init__(self, reference='', text=''):
        super().__init__()

        self.setText(text)

class CustomComboBox(QComboBox):
    def __init__(self, reference=''):
        super().__init__()


