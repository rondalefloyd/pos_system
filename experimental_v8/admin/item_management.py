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
    

        self.createDialogLayout()

    def onClickPromo(self, index):
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

    def setWidgetAttributes(self):
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
        self.promo.currentIndexChanged.connect(self.onClickPromo)
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

        # stock
        self.track_n.setChecked(True)
        self.on_hand_stock.setPlaceholderText('On hand stock')
        self.available_stock.setPlaceholderText('Available stock')

    # global settings --- x
        # label widgets setFixedHeight
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
        self.on_hand_stock.setFixedHeight(30)
        self.available_stock.setFixedHeight(30)

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
        self.on_hand_stock.setFixedWidth(300)
        self.available_stock.setFixedWidth(300)


    def onStockContainer(self):
        self.stock_container = QGroupBox()
        self.stock_layout = QGridLayout()

        self.track_y = QRadioButton("Track inventory")
        self.track_n = QRadioButton("Don't track inventory")
        self.label_on_hand_stock = QLabel('On hand stock')
        self.on_hand_stock = QLineEdit()
        self.label_available_stock = QLabel('Available stock')
        self.available_stock = QLineEdit()
        self.spacer = QFrame()


        self.stock_layout.addWidget(self.track_y)
        self.stock_layout.addWidget(self.track_n)
        self.stock_layout.addWidget(self.label_on_hand_stock)
        self.stock_layout.addWidget(self.on_hand_stock)
        self.stock_layout.addWidget(self.label_available_stock)
        self.stock_layout.addWidget(self.available_stock)
        self.stock_layout.addWidget(self.spacer)
        self.stock_container.setLayout(self.stock_layout)

        return self.stock_container

    def onPriceContainer(self):
        self.price_container = QGroupBox()
        self.price_layout = QGridLayout()

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

        self.label_item_type = QLabel('Item type')
        self.item_type = QComboBox()
        self.label_brand = QLabel('Brand')
        self.brand = QComboBox()
        self.label_sales_group = QLabel('Sales group')
        self.sales_group = QComboBox()
        self.label_supplier = QLabel('Supplier')
        self.supplier = QComboBox()
        self.spacer = QFrame()

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

        self.label_barcode = QLabel('Barcode')
        self.barcode = QLineEdit()
        self.label_item_name = QLabel('Item name')
        self.item_name = QComboBox()
        self.label_expire_dt = QLabel('Expire date')
        self.expire_dt = QDateEdit()
        self.spacer = QFrame()

        self.primary_information_layout.addWidget(self.label_barcode)
        self.primary_information_layout.addWidget(self.barcode)
        self.primary_information_layout.addWidget(self.label_item_name)
        self.primary_information_layout.addWidget(self.item_name)
        self.primary_information_layout.addWidget(self.label_expire_dt)
        self.primary_information_layout.addWidget(self.expire_dt)
        self.primary_information_layout.addWidget(self.spacer)
        self.primary_information_container.setLayout(self.primary_information_layout)
        
        return self.primary_information_container

    def createDialogLayout(self):
        self.grid_layout = QGridLayout()

        self.primary_information_container = self.onPrimaryInformationContainer()
        self.category_container = self.onCategoryContainer()
        self.price_container = self.onPriceContainer()
        self.stock_container = self.onStockContainer()

        self.setWidgetAttributes()

        self.grid_layout.addWidget(self.primary_information_container,0,0)
        self.grid_layout.addWidget(self.category_container,1,0)
        self.grid_layout.addWidget(self.price_container,0,1,3,1)
        self.grid_layout.addWidget(self.stock_container,2,0)

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

    def openManageItemDialog(self):
        self.manage_item_dialog = ManageItemDialog()
        self.manage_item_dialog.exec()

    def setWidgetAttributes(self):
        self.add_item.clicked.connect(self.openManageItemDialog)

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
