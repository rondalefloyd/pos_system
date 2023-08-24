import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ManageItemDialog(QDialog):
    def __init__(self, manage_mode_text):
        super().__init__()
        

        self.createDialogLayout(manage_mode_text)

    def onClickTrackInventoryComboBox(self, index):
        index = self.track_inventory.currentText()

        if index != "Don't track inventory for this item":
            self.label_on_hand_stock.show()
            self.on_hand_stock.show()
            self.label_available_stock.show()
            self.available_stock.show()
        else:
            self.label_on_hand_stock.hide()
            self.on_hand_stock.hide()
            self.label_available_stock.hide()
            self.available_stock.hide()

    def onClickApplyPromoComboBox(self, index):
        index = self.promo.currentText()

        if index != 'None':
            self.label_promo_start_dt.show()
            self.promo_start_dt.show()
            self.label_promo_end_dt.show()
            self.promo_end_dt.show()
            self.sell_price.setDisabled(True)
            self.label_effective_dt.hide()
            self.effective_dt.hide()
        else:
            self.label_promo_start_dt.hide()
            self.promo_start_dt.hide()
            self.label_promo_end_dt.hide()
            self.promo_end_dt.hide()
            self.sell_price.setDisabled(False)
            self.label_effective_dt.show()
            self.effective_dt.show()

    # for user interface

    def setWidgetAttributes(self):
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.grid_layout.setSpacing(0)

        # primary information
        self.barcode.setPlaceholderText('Barcode')
        self.item_name.setEditable(True)
        self.expire_dt.setMinimumDate(QDate.currentDate())
        self.expire_dt.setCalendarPopup(True)

        # category
        self.item_type.setEditable(True)
        self.brand.setEditable(True)
        self.sales_group.addItem('Retail')
        self.sales_group.addItem('Wholesale')
        self.supplier.setEditable(True)

        # price
        self.cost.setPlaceholderText('Cost')
        self.promo.currentIndexChanged.connect(self.onClickApplyPromoComboBox)
        self.promo.insertItem(0,'None')
        self.promo.addItem('Item 1')
        self.promo.setCurrentIndex(0)
        self.discount.setPlaceholderText('Discount (%)')
        self.sell_price.setPlaceholderText('Sell Price')
        self.promo_start_dt.setMinimumDate(QDate.currentDate())
        self.promo_start_dt.setCalendarPopup(True)
        self.promo_end_dt.setMinimumDate(QDate.currentDate())
        self.promo_end_dt.setCalendarPopup(True)
        self.effective_dt.setMinimumDate(QDate.currentDate())
        self.effective_dt.setCalendarPopup(True)

        # inventory
        self.track_inventory.currentIndexChanged.connect(self.onClickTrackInventoryComboBox)
        self.track_inventory.insertItem(0,"Track inventory for this item")
        self.track_inventory.insertItem(1,"Don't track inventory for this item")
        self.track_inventory.setCurrentIndex(0)
        self.on_hand_stock.setPlaceholderText('On hand stock')
        self.available_stock.setPlaceholderText('Available stock')

        # header

    # global settings --- x
        # label widgets
        self.label_header.setStyleSheet('font-weight: bold; font-size: 15pt;')

        self.label_primary_information_container.setStyleSheet('font-weight: bold;')
        self.label_category_container.setStyleSheet('font-weight: bold;')
        self.label_price_container.setStyleSheet('font-weight: bold;')
        self.label_inventory_container.setStyleSheet('font-weight: bold;')

        self.header_container.setFixedHeight(50)

        self.label_primary_information_container.setFixedHeight(20)
        self.label_category_container.setFixedHeight(20)
        self.label_price_container.setFixedHeight(20)
        self.label_inventory_container.setFixedHeight(20)

        self.label_barcode.setFixedHeight(20)
        self.label_item_name.setFixedHeight(20)
        self.label_expire_dt.setFixedHeight(20)
        self.label_item_type.setFixedHeight(20)
        self.label_brand.setFixedHeight(20)
        self.label_sales_group.setFixedHeight(20)
        self.label_supplier.setFixedHeight(20)
        self.label_cost.setFixedHeight(20)
        self.label_promo.setFixedHeight(20)
        self.label_discount.setFixedHeight(20)
        self.label_sell_price.setFixedHeight(20)
        self.label_promo_start_dt.setFixedHeight(20)
        self.label_promo_end_dt.setFixedHeight(20)
        self.label_effective_dt.setFixedHeight(20)
        self.label_on_hand_stock.setFixedHeight(20)
        self.label_available_stock.setFixedHeight(20)

        self.barcode.setFixedHeight(30)
        self.item_name.setFixedHeight(30)
        self.expire_dt.setFixedHeight(30)
        self.item_type.setFixedHeight(30)
        self.brand.setFixedHeight(30)
        self.sales_group.setFixedHeight(30)
        self.supplier.setFixedHeight(30)
        self.cost.setFixedHeight(30)
        self.promo.setFixedHeight(30)
        self.discount.setFixedHeight(30)
        self.sell_price.setFixedHeight(30)
        self.promo_start_dt.setFixedHeight(30)
        self.promo_end_dt.setFixedHeight(30)
        self.effective_dt.setFixedHeight(30)
        self.track_inventory.setFixedHeight(30)
        self.on_hand_stock.setFixedHeight(30)
        self.available_stock.setFixedHeight(30)
        self.save_button.setFixedHeight(30)

        self.barcode.setFixedWidth(300)
        self.item_name.setFixedWidth(300)
        self.expire_dt.setFixedWidth(300)
        self.item_type.setFixedWidth(300)
        self.brand.setFixedWidth(300)
        self.sales_group.setFixedWidth(300)
        self.supplier.setFixedWidth(300)
        self.cost.setFixedWidth(300)
        self.promo.setFixedWidth(300)
        self.discount.setFixedWidth(300)
        self.sell_price.setFixedWidth(300)
        self.promo_start_dt.setFixedWidth(300)
        self.promo_end_dt.setFixedWidth(300)
        self.effective_dt.setFixedWidth(300)
        self.track_inventory.setFixedWidth(300)
        self.on_hand_stock.setFixedWidth(300)
        self.available_stock.setFixedWidth(300)
        self.save_button.setFixedWidth(100)

    def onHeaderContainer(self, manage_mode_text):
        self.header_container = QGroupBox()
        self.header_layout = QGridLayout()
        self.label_header = QLabel(manage_mode_text + 'ITEM')
        spacer = QFrame()
        self.save_button = QPushButton('SAVE')

        self.header_layout.addWidget(self.label_header,0,0)
        self.header_layout.addWidget(spacer,0,1)
        self.header_layout.addWidget(self.save_button,0,2)
        self.header_container.setLayout(self.header_layout)

        return self.header_container

    def onInventoryContainer(self):
        self.inventory_container = QGroupBox()
        self.inventory_layout = QGridLayout()

        self.label_inventory_container = QLabel('INVENTORY')
        self.track_inventory = QComboBox()
        self.label_on_hand_stock = QLabel('On hand stock')
        self.on_hand_stock = QLineEdit()
        self.label_available_stock = QLabel('Available stock')
        self.available_stock = QLineEdit()
        self.spacer = QFrame()


        self.inventory_layout.addWidget(self.label_inventory_container)
        self.inventory_layout.addWidget(self.track_inventory)
        self.inventory_layout.addWidget(self.label_on_hand_stock)
        self.inventory_layout.addWidget(self.on_hand_stock)
        self.inventory_layout.addWidget(self.label_available_stock)
        self.inventory_layout.addWidget(self.available_stock)
        self.inventory_layout.addWidget(self.spacer)
        self.inventory_container.setLayout(self.inventory_layout)

        return self.inventory_container

    def onPriceContainer(self):
        self.price_container = QGroupBox()
        self.price_layout = QGridLayout()

        self.label_price_container = QLabel('PRICE')
        self.label_cost = QLabel('Cost')
        self.cost = QLineEdit()
        self.label_promo = QLabel('Promo')
        self.promo = QComboBox()
        self.label_discount = QLabel('Discount')
        self.discount = QLineEdit()
        self.label_sell_price = QLabel('Sell price')
        self.sell_price = QLineEdit()
        self.label_promo_start_dt = QLabel('Start date')
        self.promo_start_dt = QDateEdit()
        self.label_promo_end_dt = QLabel('End date')
        self.promo_end_dt = QDateEdit()
        self.label_effective_dt = QLabel('Effective date')
        self.effective_dt = QDateEdit()
        self.spacer = QFrame()

        self.price_layout.addWidget(self.label_price_container)
        self.price_layout.addWidget(self.label_cost)
        self.price_layout.addWidget(self.cost)
        self.price_layout.addWidget(self.label_promo)
        self.price_layout.addWidget(self.promo)
        self.price_layout.addWidget(self.label_discount)
        self.price_layout.addWidget(self.discount)
        self.price_layout.addWidget(self.label_sell_price)
        self.price_layout.addWidget(self.sell_price)
        self.price_layout.addWidget(self.label_promo_start_dt)
        self.price_layout.addWidget(self.promo_start_dt)
        self.price_layout.addWidget(self.label_promo_end_dt)
        self.price_layout.addWidget(self.promo_end_dt)
        self.price_layout.addWidget(self.label_effective_dt)
        self.price_layout.addWidget(self.effective_dt)
        self.price_layout.addWidget(self.spacer)
        self.price_container.setLayout(self.price_layout)

        return self.price_container

    def onCategoryContainer(self):
        self.category_container = QGroupBox()
        self.category_layout = QGridLayout()

        self.label_category_container = QLabel('CATEGORY')
        self.label_item_type = QLabel('Item type')
        self.item_type = QComboBox()
        self.label_brand = QLabel('Brand')
        self.brand = QComboBox()
        self.label_sales_group = QLabel('Sales group')
        self.sales_group = QComboBox()
        self.label_supplier = QLabel('Supplier')
        self.supplier = QComboBox()
        self.spacer = QFrame()

        self.category_layout.addWidget(self.label_category_container)
        self.category_layout.addWidget(self.label_item_type)
        self.category_layout.addWidget(self.item_type)
        self.category_layout.addWidget(self.label_brand)
        self.category_layout.addWidget(self.brand)
        self.category_layout.addWidget(self.label_sales_group)
        self.category_layout.addWidget(self.sales_group)
        self.category_layout.addWidget(self.label_supplier)
        self.category_layout.addWidget(self.supplier)
        self.category_layout.addWidget(self.spacer)
        self.category_container.setLayout(self.category_layout)

        return self.category_container

    def onPrimaryInformationContainer(self):
        self.primary_information_container = QGroupBox()
        self.primary_information_layout = QGridLayout()

        self.label_primary_information_container = QLabel('PRIMARY INFORMATION')
        self.label_barcode = QLabel('Barcode')
        self.barcode = QLineEdit()
        self.label_item_name = QLabel('Item name')
        self.item_name = QComboBox()
        self.label_expire_dt = QLabel('Expire date')
        self.expire_dt = QDateEdit()
        self.spacer = QFrame()

        self.primary_information_layout.addWidget(self.label_primary_information_container)
        self.primary_information_layout.addWidget(self.label_barcode)
        self.primary_information_layout.addWidget(self.barcode)
        self.primary_information_layout.addWidget(self.label_item_name)
        self.primary_information_layout.addWidget(self.item_name)
        self.primary_information_layout.addWidget(self.label_expire_dt)
        self.primary_information_layout.addWidget(self.expire_dt)
        self.primary_information_layout.addWidget(self.spacer)
        self.primary_information_container.setLayout(self.primary_information_layout)
        
        return self.primary_information_container

    def createDialogLayout(self, manage_mode_text):
        self.grid_layout = QGridLayout()

        self.primary_information_container = self.onPrimaryInformationContainer()
        self.category_container = self.onCategoryContainer()
        self.price_container = self.onPriceContainer()
        self.inventory_container = self.onInventoryContainer()
        self.header_container = self.onHeaderContainer(manage_mode_text)

        self.setWidgetAttributes()

        self.grid_layout.addWidget(self.header_container,0,0,1,2)
        self.grid_layout.addWidget(self.primary_information_container,1,0)
        self.grid_layout.addWidget(self.category_container,2,0)
        self.grid_layout.addWidget(self.price_container,1,1,3,1) # row_index, col_index, row_occupied, col_occupied
        self.grid_layout.addWidget(self.inventory_container,3,0)

        self.setLayout(self.grid_layout)

class ListItemTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.createTableLayout()

    def createTableLayout(self):
        pass

class ItemManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.createMainLayout()
        pass

    def openManageItemDialog(self, manage_mode_text):
        self.manage_item_dialog = ManageItemDialog(manage_mode_text)
        self.manage_item_dialog.exec()

    def setWidgetAttributes(self):
        self.add_item.clicked.connect(lambda: self.openManageItemDialog('ADD'))

    def createMainLayout(self):
        self.grid_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.add_item = QPushButton('ADD')
        self.list_item_table = ListItemTable()

        self.setWidgetAttributes()

        self.grid_layout.addWidget(self.filter_bar)
        self.grid_layout.addWidget(self.add_item)
        self.grid_layout.addWidget(self.list_item_table)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
