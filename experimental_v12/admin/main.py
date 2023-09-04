import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.layouts.item_management_window import ItemManagementWindow
from utils.layouts.inventory_management_window import InventoryManagementWindow
from utils.layouts.promo_management_window import PromoManagementWindow
from utils.layouts.customer_management_window import CustomerManagementWindow
from utils.layouts.reward_management_window import RewardManagementWindow
from utils.layouts.user_management_window import UserManagementWindow


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
        self.item_management = ItemManagementWindow()
        self.inventory_management = InventoryManagementWindow()
        self.promo_management = PromoManagementWindow()
        self.customer_management = CustomerManagementWindow()
        self.reward_management = RewardManagementWindow()
        self.user_management = UserManagementWindow()

    def onNavbarButtonClicked(self, index):
        self.panel_b.setCurrentIndex(index)

    def showPanelA(self):
        self.panel_a = QGroupBox()
        self.panel_a_layout = QVBoxLayout()

        self.item = QPushButton('Item')
        self.item.clicked.connect(lambda: self.onNavbarButtonClicked(0))
        self.inventory = QPushButton('Inventory')
        self.inventory.clicked.connect(lambda: self.onNavbarButtonClicked(1))
        self.promo = QPushButton('Promo')
        self.promo.clicked.connect(lambda: self.onNavbarButtonClicked(2))
        self.customer = QPushButton('Customer')
        self.customer.clicked.connect(lambda: self.onNavbarButtonClicked(3))
        self.reward = QPushButton('Reward')
        self.reward.clicked.connect(lambda: self.onNavbarButtonClicked(4))
        self.user = QPushButton('User')
        self.user.clicked.connect(lambda: self.onNavbarButtonClicked(5))

        self.panel_a_layout.addWidget(self.item)
        self.panel_a_layout.addWidget(self.inventory)
        self.panel_a_layout.addWidget(self.promo)
        self.panel_a_layout.addWidget(self.customer)
        self.panel_a_layout.addWidget(self.reward)
        self.panel_a_layout.addWidget(self.user)
        self.panel_a_layout.addWidget(QFrame()) # -- spacer

        self.panel_a.setLayout(self.panel_a_layout)

        return self.panel_a

    def showPanelB(self):
        self.panel_b = QStackedWidget()
        self.panel_b.setCurrentIndex(0)

        self.prepareSubWindow()

        self.panel_b.addWidget(self.item_management)
        self.panel_b.addWidget(self.inventory_management)
        self.panel_b.addWidget(self.promo_management)
        self.panel_b.addWidget(self.customer_management)
        self.panel_b.addWidget(self.reward_management)
        self.panel_b.addWidget(self.user_management)

        return self.panel_b
    
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(pos_app.exec())

