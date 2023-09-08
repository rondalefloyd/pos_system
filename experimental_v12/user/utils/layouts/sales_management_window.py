import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

# from utils.layouts.item_management_window import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

# -- changeable
# from utils.schemas.sales_table_schema import *
# from utils.schemas.sales_management_schema import *
from utils.widgets.sales_management_widget import *
# ----

class SalesManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        # self.sales_table_schema = SalesTableSchema()

        # -- changeable
        # self.promo_management_schema = PromoManagementSchema()

        # self.item_management_window = ItemManagementWindow()
        # ----

        # self.sales_table_schema.createSalesTable()

        self.main_layout = QGridLayout()

        self.panel_a_widget = self.showPanelA()
        self.panel_b_widget = self.showPanelB()

        self.main_layout.addWidget(self.panel_a_widget,0,0)
        self.main_layout.addWidget(self.panel_b_widget,0,1)

        self.setLayout(self.main_layout)

    def showPanelA(self):
        self.panel_a = CustomGroupBox(reference='panel_a')
        self.panel_a_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.list_table = CustomTableWidget(reference='list_table')


        self.panel_a_layout.addWidget(self.filter_bar,0,0)
        self.panel_a_layout.addWidget(self.list_table,1,0)

        self.panel_a.setLayout(self.panel_a_layout)

        return self.panel_a

    def showPanelB(self):
        self.panel_b = CustomTabWidget(reference='panel_b')

        self.test = CustomLabel(text='nice')

        return self.panel_b

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = SalesManagementWindow()
    window.show()
    sys.exit(pos_app.exec())

