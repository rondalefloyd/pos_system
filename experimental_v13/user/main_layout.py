import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_widget import *
from utils.layout.transact_layout import TransactWindow

class MainWindow(CustomGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMainLayout()

    def showPanelB(self):
        self.panel_b = CustomStackedWidget()

        self.transact_window = TransactWindow()
        
        self.panel_b.addWidget(self.transact_window)

    def showPanelA(self):
        self.panel_a = CustomGroupBox(reference='panel_a')
        self.panel_a_layout = QVBoxLayout()

        self.transact_button = CustomPushButton(text='Transact')
        self.history_button = CustomPushButton(text='History')

        self.panel_a_layout.addWidget(self.transact_button)
        self.panel_a_layout.addWidget(self.history_button)
        self.panel_a_layout.addWidget(QFrame()) # -- serves as spacer

        self.panel_a.setLayout(self.panel_a_layout)

    def setMainLayout(self):
        self.setWindowState(Qt.WindowState.WindowMaximized)
    
        self.main_layout = QGridLayout()

        self.showPanelA()
        self.showPanelB()

        self.main_layout.addWidget(self.panel_a,0,0)
        self.main_layout.addWidget(self.panel_b,0,1)

        self.setLayout(self.main_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(pos_app.exec())

