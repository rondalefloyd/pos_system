import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ManageItemDialog(QDialog):
    def __init__(self):
        super().__init__()
    

        self.setDialogLayout()

    # widget functions
    def onClickPromoStatus(self, index):
        if index == 0:
            self.label_promo_start_dt.hide()
            self.label_promo_end_dt.hide()
            self.label_effective_dt.show()
            self.promo_start_dt.hide()
            self.promo_end_dt.hide()
            self.effective_dt.show()
        else:
            self.label_promo_start_dt.show()
            self.label_promo_end_dt.show()
            self.label_effective_dt.hide()
            self.promo_start_dt.show()
            self.promo_end_dt.show()
            self.effective_dt.hide()


    def onClickedInventoryStatus(self, index):
        if index == 0:
            self.label_on_hand_stock.show()
            self.label_available_stock.show()
            self.on_hand_stock.show()
            self.available_stock.show()
        else:
            self.label_on_hand_stock.hide()
            self.label_available_stock.hide()
            self.on_hand_stock.hide()
            self.available_stock.hide()


    # global widgets
    def customPushButton(self, text):
        push_button = QPushButton(text)

        return push_button

    def customLabel(self, text):
        label = QLabel(text)

        label.setFixedHeight(25)

        return label
    
    def customLineEdit(self, ref, placeholder, disabled):
        line_edit = QLineEdit()

        line_edit.setPlaceholderText(placeholder)
        line_edit.setDisabled(disabled)

        return line_edit
    
    def customComboBox(self, ref, editable):
        combo_box = QComboBox()

        combo_box.setEditable(editable)

        if ref == 'inventory_status':
            combo_box.insertItem(0,"Track inventory")
            combo_box.insertItem(1,"Don't track inventory")
            combo_box.setCurrentIndex(0)
            combo_box.currentIndexChanged.connect(self.onClickedInventoryStatus)
        
        elif ref == 'promo_status':
            combo_box.insertItem(0,"No promo")
            combo_box.addItem("Promo 1")
            combo_box.currentIndexChanged.connect(self.onClickPromoStatus)

        return combo_box
    
    def customDateEdit(self, ref):
        date_edit = QDateEdit()

        date_edit.setCalendarPopup(True)

        # exceptions
        if ref == 'expire_dt' or ref == 'promo_start_dt' or ref == 'promo_end_dt' or ref == 'effective_dt':
            date_edit.setMinimumDate(QDate.currentDate())

        return date_edit


    # sections
    def primaryInformationContainer(self):
        group_box = QGroupBox()
        grid_layout = QGridLayout()

        self.label_barcode = self.customLabel('Barcode')
        self.label_item_name = self.customLabel('Item name')
        self.label_expire_dt = self.customLabel('Expire date')
        self.barcode = self.customLineEdit('', 'Barcode', disabled=False) # customLineEdit(self, ref, placeholder, disabled):
        self.item_name = self.customComboBox('', editable=True) # customComboBox(self, ref, editable):
        self.expire_dt = self.customDateEdit('expire_dt') # customDateEdit(self, ref):

        grid_layout.addWidget(self.label_barcode,0,0)
        grid_layout.addWidget(self.barcode,1,0)
        grid_layout.addWidget(self.label_item_name,2,0)
        grid_layout.addWidget(self.item_name,3,0)
        grid_layout.addWidget(self.label_expire_dt,4,0)
        grid_layout.addWidget(self.expire_dt,5,0)
        grid_layout.addWidget(QFrame(),6,0)


        group_box.setLayout(grid_layout)
        return group_box

    def categoryContainer(self):
        group_box = QGroupBox()
        grid_layout = QGridLayout()
        
        self.label_item_type = self.customLabel('Item type')
        self.label_brand = self.customLabel('Brand')
        self.label_sales_group = self.customLabel('Sales group')
        self.label_supplier = self.customLabel('Supplier')
        self.item_type = self.customComboBox('', editable=True) # customComboBox(self, ref, editable):
        self.brand = self.customComboBox('', editable=True) # customComboBox(self, ref, editable):
        self.sales_group = self.customComboBox('', editable=True) # customComboBox(self, ref, editable):
        self.supplier = self.customComboBox('', editable=True) # customComboBox(self, ref, editable):
        
        grid_layout.addWidget(self.label_item_type,0,0)
        grid_layout.addWidget(self.item_type,1,0)
        grid_layout.addWidget(self.label_brand,2,0)
        grid_layout.addWidget(self.brand,3,0)
        grid_layout.addWidget(self.label_sales_group,4,0)
        grid_layout.addWidget(self.sales_group,5,0)
        grid_layout.addWidget(self.label_supplier,6,0)
        grid_layout.addWidget(self.supplier,7,0)
        grid_layout.addWidget(QFrame(),8,0)


        group_box.setLayout(grid_layout)
        return group_box

    def priceContainer(self):
        group_box = QGroupBox()
        grid_layout = QGridLayout()
        
        self.label_cost = self.customLabel('Cost')
        self.label_promo = self.customLabel('Promo')
        self.label_discount = self.customLabel('Discount')
        self.label_sell_price = self.customLabel('Sell price')
        self.label_promo_start_dt = self.customLabel('Start date')
        self.label_promo_end_dt = self.customLabel('End date')
        self.label_effective_dt = self.customLabel('Effective date')
        self.cost = self.customLineEdit('', 'Cost', disabled=False) # customLineEdit(self, ref, placeholder, disabled):
        self.promo = self.customComboBox('promo_status', editable=False) # customComboBox(self, ref, editable):
        self.discount = self.customLineEdit('', 'Discount (%)', disabled=False) # customLineEdit(self, ref, placeholder, disabled):
        self.sell_price = self.customLineEdit('', 'Sell price', disabled=True) # customLineEdit(self, ref, placeholder, disabled):
        self.promo_start_dt = self.customDateEdit('promo_start_dt') # customDateEdit(self, ref):
        self.promo_end_dt = self.customDateEdit('promo_end_dt') # customDateEdit(self, ref):
        self.effective_dt = self.customDateEdit('effective_dt') # customDateEdit(self, ref):

        grid_layout.addWidget(self.label_cost,0,0)
        grid_layout.addWidget(self.cost,1,0)
        grid_layout.addWidget(self.label_promo,2,0)
        grid_layout.addWidget(self.promo,3,0)
        grid_layout.addWidget(self.label_discount,4,0)
        grid_layout.addWidget(self.discount,5,0)
        grid_layout.addWidget(self.label_sell_price,6,0)
        grid_layout.addWidget(self.sell_price,7,0)
        grid_layout.addWidget(self.label_promo_start_dt,8,0)
        grid_layout.addWidget(self.promo_start_dt,9,0)
        grid_layout.addWidget(self.label_promo_end_dt,10,0)
        grid_layout.addWidget(self.promo_end_dt,11,0)
        grid_layout.addWidget(self.label_effective_dt,12,0)
        grid_layout.addWidget(self.effective_dt,13,0)
        grid_layout.addWidget(QFrame(),14,0)

        group_box.setLayout(grid_layout)
        return group_box

    def inventoryStatusContainer(self):
        group_box = QGroupBox()
        grid_layout = QGridLayout()

        self.label_inventory_status = self.customLabel('Inventory status')
        self.label_on_hand_stock = self.customLabel('On hand stock')
        self.label_available_stock = self.customLabel('Available stock')
        self.inventory_status = self.customComboBox('inventory_status', editable=False) # customComboBox(self, ref, editable):
        self.on_hand_stock = self.customLineEdit('', 'On hand stock', disabled=False) # customLineEdit(self, ref, placeholder, disabled):
        self.available_stock = self.customLineEdit('', 'Available stock', disabled=False) # customLineEdit(self, ref, placeholder, disabled):

        grid_layout.addWidget(self.label_inventory_status,0,0)
        grid_layout.addWidget(self.inventory_status,1,0)
        grid_layout.addWidget(self.label_on_hand_stock,2,0)
        grid_layout.addWidget(self.on_hand_stock,3,0)
        grid_layout.addWidget(self.label_available_stock,4,0)
        grid_layout.addWidget(self.available_stock,5,0)
        grid_layout.addWidget(QFrame(),6,0)

        group_box.setLayout(grid_layout)
        return group_box

    # main layout
    def setDialogLayout(self):
        self.grid_layout = QGridLayout()

        self.primary_information_container = self.primaryInformationContainer()
        self.category_container = self.categoryContainer()
        self.price_container = self.priceContainer()
        self.inventory_track_container = self.inventoryStatusContainer()

        self.grid_layout.addWidget(self.primary_information_container,0,0)
        self.grid_layout.addWidget(self.category_container,0,1)
        self.grid_layout.addWidget(self.price_container,0,2)
        self.grid_layout.addWidget(self.inventory_track_container,0,3)

        self.setLayout(self.grid_layout)

class ListItemTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setTableLayout()

    def setTableLayout(self):
        pass

class ItemManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setMainLayout()

    def openManageItemDialog(self):
        self.manage_item_dialog = ManageItemDialog()
        self.manage_item_dialog.exec()

    def setMainLayout(self):
        self.grid_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.add_item = QPushButton('ADD')
        self.add_item.clicked.connect(self.openManageItemDialog)
        self.list_item_table = ListItemTable()

        self.grid_layout.addWidget(self.filter_bar)
        self.grid_layout.addWidget(self.add_item)
        self.grid_layout.addWidget(self.list_item_table)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
