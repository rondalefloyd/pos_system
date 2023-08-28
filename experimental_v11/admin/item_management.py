import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.databse_manager import *

class CustomLineEdit(QLineEdit):
    def __init__(self, ref=None):
        super().__init__()
        pass

class CustomComboBox(QComboBox):
    def __init__(self, ref=None):
        super().__init__()

        if ref == 'item_name' or ref == 'item_type' or ref == 'brand' or ref == 'supplier':
            self.setEditable(True)
        pass

class CustomDateEdit(QDateEdit):
    def __init__(self, ref=None):
        super().__init__()
        pass

class CustomPushButton(QPushButton):
    def __init__(self, text=None):
        super().__init__()
        
        self.setText(text)

        pass

class CustomTableWidget(QTableWidget):
    def __init__(self, ref=None):
        super().__init__()
        pass

class CustomGroupBox(QGroupBox):
    def __init__(self, ref=None):
        super().__init__()
    
        if ref == 'panel_b':
            self.setFixedWidth(300)
        pass

# ------------------------------------------------------------------------------- #

class ItemManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setMainLayout()

    def onClickedSaveButton(self):
        converted_barcode = str(self.barcode.text())
        converted_item_name = str(self.item_name.currentText())
        converted_expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)

        converted_item_type = str(self.item_type.currentText())
        converted_brand = str(self.brand.currentText())
        converted_sales_group = str(self.sales_group.currentText())
        converted_supplier = str(self.supplier.currentText())

        converted_cost = str('{:.2f}'.format(float(self.cost.text())))
        converted_sell_price = str('{:.2f}'.format(float(self.sell_price.text())))
        converted_new_sell_price = str('{:.2f}'.format(float(self.new_sell_price.text())))
        converted_promo_name = str(self.promo_name.currentText())
        converted_promo_type = str(self.promo_type.text())
        converted_discount_percent = str('{:.2f}'.format(float(self.discount_percent.text())))
        converted_discount_value = str('{:.2f}'.format(float(self.discount_value.text())))
        converted_start_dt = self.start_dt.date().toString(Qt.DateFormat.ISODate)
        converted_end_dt = self.end_dt.date().toString(Qt.DateFormat.ISODate)
        converted_effective_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate)

        converted_inventory_status = str(self.inventory_status.currentText())
        converted_on_hand_stock = str(int(self.on_hand_stock.text()))
        converted_available_stock = str(int(self.available_stock.text()))

    def onClickedCloseButton(self):
        self.panel_b.hide()
        self.add_button.setDisabled(False)

    def showPanelB(self): # -- PANEL B
        panel = CustomGroupBox(ref='panel_b')
        panel_layout = QFormLayout()

        self.close_button = CustomPushButton(text='BACK')
        self.close_button.setFixedWidth(50)
        self.close_button.clicked.connect(self.onClickedCloseButton)

        self.barcode = CustomLineEdit()
        self.item_name = CustomComboBox()
        self.expire_dt = CustomDateEdit()

        self.item_type = CustomComboBox(ref='item_type')
        self.brand = CustomComboBox(ref='brand')
        self.sales_group = CustomComboBox(ref='sales_group')
        self.supplier = CustomComboBox(ref='supplier')

        self.cost = CustomLineEdit(ref='cost')
        self.sell_price = CustomLineEdit(ref='sell_price')
        self.new_sell_price = CustomLineEdit(ref='new_sell_price')
        self.promo_name = CustomComboBox(ref='promo_name')
        self.promo_type = CustomLineEdit(ref='promo_type')
        self.discount_percent = CustomLineEdit(ref='discount_percent')
        self.discount_value = CustomLineEdit()
        self.start_dt = CustomDateEdit()
        self.end_dt = CustomDateEdit()
        self.effective_dt = CustomDateEdit()

        self.inventory_status = CustomComboBox(ref='inventory_status')
        self.on_hand_stock = CustomLineEdit(ref='on_hand_stock')
        self.available_stock = CustomLineEdit(ref='available_stock')

        self.save_button = CustomPushButton(text='SAVE')
        
        panel_layout.addRow(self.close_button)

        panel_layout.addRow('barcode: ', self.barcode)
        panel_layout.addRow('item_name: ', self.item_name)
        panel_layout.addRow('expire_dt: ', self.expire_dt)

        panel_layout.addRow('item_type: ', self.item_type)
        panel_layout.addRow('brand: ', self.brand)
        panel_layout.addRow('sales_group: ', self.sales_group)
        panel_layout.addRow('supplier: ', self.supplier)

        panel_layout.addRow('cost: ', self.cost)
        panel_layout.addRow('sell_price: ', self.sell_price)
        panel_layout.addRow('new_sell_price: ', self.new_sell_price)
        panel_layout.addRow('promo_name: ', self.promo_name)
        panel_layout.addRow('promo_type: ', self.promo_type)
        panel_layout.addRow('discount_percent: ', self.discount_percent)
        panel_layout.addRow('discount_value: ', self.discount_value)
        panel_layout.addRow('start_dt: ', self.start_dt)
        panel_layout.addRow('end_dt: ', self.end_dt)
        panel_layout.addRow('effective_dt: ', self.effective_dt)

        panel_layout.addRow('inventory_status: ', self.inventory_status)
        panel_layout.addRow('on_hand_stock: ', self.on_hand_stock)
        panel_layout.addRow('available_stock: ', self.available_stock)


        panel_layout.addRow(self.save_button)

        panel.setLayout(panel_layout)

        return panel

    # -------------------------------------------------------- #

    def onClickedAddButton(self):
        self.panel_b.show()
        self.add_button.setDisabled(True)

    def showPanelA(self): # -- PANEL A
        panel = CustomGroupBox()
        panel_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.add_button = CustomPushButton(text='ADD')
        self.add_button.clicked.connect(self.onClickedAddButton)
        self.item_list_table = CustomTableWidget()

        panel_layout.addWidget(self.filter_bar,0,0)
        panel_layout.addWidget(self.add_button,0,1)
        panel_layout.addWidget(self.item_list_table,1,0,1,2)

        panel.setLayout(panel_layout)

        return panel

    def setMainLayout(self):
        self.main_layout = QGridLayout()

        self.panel_a = self.showPanelA()
        self.panel_b = self.showPanelB()

        self.main_layout.addWidget(self.panel_a,0,0)
        self.main_layout.addWidget(self.panel_b,0,1)

        self.setLayout(self.main_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
