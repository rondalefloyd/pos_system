import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_manager import *

from admin.item_management import ItemManagementWindow
from admin.inventory_management import InventoryManagementWindow
from admin.promo_management import PromoManagementWindow
from admin.customer_management import CustomerManagementWindow
from admin.reward_management import RewardManagementWindow
from admin.user_management import UserManagementWindow
 
class CustomPushButton(QPushButton):
    def __init__(self, text=None, reference=None):
        super().__init__()
        
        self.setText(text)

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

        self.setFixedWidth(200)

class CustomStackedWidget(QStackedWidget):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

# ------------------------------------------------------------------------------- #

class AdminMainWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__() 

        self.prepareUtils()
        self.setMainLayout()

    # PANEL B SECTION -------------------------------------------------------- #

    def showPanelB(self): # -- PANEL B
        self.panel_b = CustomStackedWidget(reference='panel_b')
        self.panel_b.setCurrentIndex(0)

        self.panel_b.addWidget(self.item_management)
        self.panel_b.addWidget(self.inventory_management)
        self.panel_b.addWidget(self.promo_management)
        self.panel_b.addWidget(self.customer_management)
        self.panel_b.addWidget(self.reward_management)
        self.panel_b.addWidget(self.user_management)

        return self.panel_b

    # PANEL A SECTION -------------------------------------------------------- #

    def onNavbarButtonClicked(self, index):
        self.panel_b.setCurrentIndex(index)

    def showPanelA(self): # -- PANEL A
        panel = CustomGroupBox(reference='panel_a')
        panel_layout = QVBoxLayout()

        self.item = CustomPushButton(text='item')
        self.item.clicked.connect(lambda: self.onNavbarButtonClicked(0))
        self.inventory = CustomPushButton(text='inventory')
        self.inventory.clicked.connect(lambda: self.onNavbarButtonClicked(1))
        self.promo = CustomPushButton(text='promo')
        self.promo.clicked.connect(lambda: self.onNavbarButtonClicked(2))
        self.customer = CustomPushButton(text='customer')
        self.customer.clicked.connect(lambda: self.onNavbarButtonClicked(3))
        self.reward = CustomPushButton(text='reward')
        self.reward.clicked.connect(lambda: self.onNavbarButtonClicked(4))
        self.user = CustomPushButton(text='user')
        self.user.clicked.connect(lambda: self.onNavbarButtonClicked(5))
        
        panel_layout.addWidget(self.item)
        panel_layout.addWidget(self.inventory)
        panel_layout.addWidget(self.promo)
        panel_layout.addWidget(self.customer)
        panel_layout.addWidget(self.reward)
        panel_layout.addWidget(self.user)
        panel_layout.addWidget(QFrame())

        panel.setLayout(panel_layout)

        return panel
    
    # MAIN SECTION -------------------------------------------------------- #
    def setMainLayout(self):
        self.main_layout = QGridLayout()

        self.panel_a = self.showPanelA()
        self.panel_b = self.showPanelB()

        self.main_layout.addWidget(self.panel_a,0,0)
        self.main_layout.addWidget(self.panel_b,0,1)

        self.setLayout(self.main_layout)

    def prepareUtils(self):
        self.accounts_data_manager = AccountsDataManager()
        self.accounts_data_manager.createAccountsTable() # -- for temporary used while main_admin_window is not yet existing


        self.item_management = ItemManagementWindow()
        self.inventory_management = InventoryManagementWindow()
        self.promo_management = PromoManagementWindow()
        self.customer_management = CustomerManagementWindow()
        self.reward_management = RewardManagementWindow()
        self.user_management = UserManagementWindow()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AdminMainWindow()
    window.show()
    sys.exit(pos_app.exec())
