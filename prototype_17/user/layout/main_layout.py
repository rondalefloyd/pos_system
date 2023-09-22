import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user.layout.process_sale_layout import *
from schema.sales_table_schema import *
from widget.main_widget import *

class MainLayout(CustomGroupBox):
    def __init__(self):
        super().__init__()

        self.createLayout()

    def on_push_button_clicked(self, index=0):
        self.panel_b.setCurrentIndex(index)

    def show_panel_b(self):
        self.panel_b = QStackedLayout()
        self.panel_b.setCurrentIndex(0)
        
        self.product_management_layout = ProductManagementLayout()
        # self.inventory_management_layout = InventoryManagementLayout()
        # self.promo_management_layout = PromoManagementLayout()
        # self.reward_management_layout = RewardManagementLayout()
        # self.customer_management_layout = CustomerManagementLayout()
        # self.user_management_layout = UserManagementLayout()

        self.panel_b.addWidget(self.product_management_layout)
        # self.panel_b.addWidget(self.inventory_management_layout)
        # self.panel_b.addWidget(self.promo_management_layout)
        # self.panel_b.addWidget(self.reward_management_layout)
        # self.panel_b.addWidget(self.customer_management_layout)
        # self.panel_b.addWidget(self.user_management_layout)


    def show_panel_a(self):
        self.panel_a = CustomGroupBox(ref='panel_a')
        form_layout = QFormLayout()

        self.product_management_button = CustomPushButton(text='Product')
        self.inventory_management_button = CustomPushButton(text='Inventory')
        self.promo_management_button = CustomPushButton(text='Promo')
        self.reward_management_button = CustomPushButton(text='Reward')
        self.customer_management_button = CustomPushButton(text='Customer')
        self.user_management_button = CustomPushButton(text='User')

        # self.product_management_button.clicked.connect(lambda: self.on_push_button_clicked(0))
        # self.inventory_management_button.clicked.connect(lambda: self.on_push_button_clicked(1))
        # self.promo_management_button.clicked.connect(lambda: self.on_push_button_clicked(2))
        # self.reward_management_button.clicked.connect(lambda: self.on_push_button_clicked(3))
        # self.customer_management_button.clicked.connect(lambda: self.on_push_button_clicked(4))
        # self.user_management_button.clicked.connect(lambda: self.on_push_button_clicked(5))


        form_layout.addRow(self.product_management_button)
        form_layout.addRow(self.inventory_management_button)
        form_layout.addRow(self.promo_management_button)
        form_layout.addRow(self.reward_management_button)
        form_layout.addRow(self.customer_management_button)
        form_layout.addRow(self.user_management_button)
        self.panel_a.setLayout(form_layout)

    def createLayout(self):
        # self.setWindowState(Qt.WindowState.WindowMaximized)

        grid_layout = QGridLayout()

        self.show_panel_a()
        self.show_panel_b()

        grid_layout.addWidget(self.panel_a,0,0)
        grid_layout.addWidget(self.panel_b,0,1)

        self.setLayout(grid_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = MainLayout()
    window.show()
    sys.exit(pos_app.exec())
