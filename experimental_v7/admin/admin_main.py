import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from item_management import ItemManagement
from inventory_management import InventoryManagement
from customer_management import CustomerManagement
from promo_management import PromoManagement
from user_management import UserManagement

class AdminMain(QWidget):
    def __init__(self):
        super().__init__()

        self.createLayout()

    def onClickNavBar(self, index):
        self.content_container.setCurrentIndex(index)

    def setWidgetsAttributes(self):
        self.item.setText('Item')
        self.inventory.setText('Inventory')
        self.customer.setText('Customer')
        self.promo.setText('Promo')
        self.user.setText('User')

        self.item.clicked.connect(lambda: self.onClickNavBar(0))
        self.inventory.clicked.connect(lambda: self.onClickNavBar(1))
        self.customer.clicked.connect(lambda: self.onClickNavBar(2))
        self.promo.clicked.connect(lambda: self.onClickNavBar(3))
        self.user.clicked.connect(lambda: self.onClickNavBar(4))

    def navBarLayout(self):
        self.nav_bar_container = QGroupBox()
        self.nav_bar_layout = QVBoxLayout()

        self.item = QPushButton()
        self.inventory = QPushButton()
        self.customer = QPushButton()
        self.promo = QPushButton()
        self.user = QPushButton()
        self.spacer = QFrame()

        self.nav_bar_layout.addWidget(self.item)
        self.nav_bar_layout.addWidget(self.inventory)
        self.nav_bar_layout.addWidget(self.customer)
        self.nav_bar_layout.addWidget(self.promo)
        self.nav_bar_layout.addWidget(self.user)
        self.nav_bar_layout.addWidget(self.spacer)

        self.nav_bar_container.setLayout(self.nav_bar_layout)

        return self.nav_bar_container

    def contentLayout(self):
        self.content_container = QStackedWidget()
        self.content_container.setCurrentIndex(0)

        item_management = ItemManagement()
        inventory_management = InventoryManagement()
        customer_management = CustomerManagement()
        promo_management = PromoManagement()
        user_management = UserManagement()

        self.content_container.addWidget(item_management)
        self.content_container.addWidget(inventory_management)
        self.content_container.addWidget(customer_management)
        self.content_container.addWidget(promo_management)
        self.content_container.addWidget(user_management)

        return self.content_container

    def createLayout(self):
        self.grid_layout = QGridLayout()

        nav_bar_layout = self.navBarLayout()
        content_layout = self.contentLayout()

        self.setWidgetsAttributes()

        self.grid_layout.addWidget(nav_bar_layout,0,0)
        self.grid_layout.addWidget(content_layout,0,1)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AdminMain()
    window.show()
    sys.exit(pos_app.exec())
