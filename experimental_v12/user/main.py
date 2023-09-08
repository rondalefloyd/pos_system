import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.layouts.sales_management_window import SalesManagementWindow


class MainWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.main_layout = QGridLayout()

        self.navbar = self.showPanelA()
        self.content = self.showPanelB()

        self.main_layout.addWidget(self.navbar,0,0)
        self.main_layout.addWidget(self.content,0,1)

        self.setLayout(self.main_layout)

    def prepareSubWindow(self):
        self.sales_management_window = SalesManagementWindow()


    def onNavbarButtonClicked(self, index):
        self.panel_b.setCurrentIndex(index)

    def showPanelA(self):
        self.panel_a = QGroupBox()
        self.panel_a_layout = QVBoxLayout()

        self.sales_management = QPushButton('Sales Management')
        self.sales_management.clicked.connect(lambda: self.onNavbarButtonClicked(0))
        self.sales_history = QPushButton('Sales History')
        self.sales_history.clicked.connect(lambda: self.onNavbarButtonClicked(1))

        self.panel_a_layout.addWidget(self.sales_management)
        self.panel_a_layout.addWidget(self.sales_history)

        self.panel_a_layout.addWidget(QFrame()) # -- spacer

        self.panel_a.setLayout(self.panel_a_layout)

        return self.panel_a

    def showPanelB(self):
        self.panel_b = QStackedWidget()
        self.panel_b.setCurrentIndex(0)

        self.prepareSubWindow()

        self.panel_b.addWidget(self.sales_management_window)
        # self.panel_b.addWidget(self.sales_history_window)

        return self.panel_b
    
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(pos_app.exec())

