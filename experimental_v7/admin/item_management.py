import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.item_management_sql import *
from utils.inventory_management_sql import *

class AddItemWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')

        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.manage_item = ItemManagementSQL()
        self.manage_inventory = InventoryManagementSQL()

    def fillComboBox(self):
        item_name = self.manage_item.selectItemData()
        for row in item_name:
            self.item_name.addItem(row)

        item_type = self.manage_item.selectItemTypeData()
        for row in item_type:
            self.item_type.addItem(row)

        brand = self.manage_item.selectBrandData()
        for row in brand:
            self.brand.addItem(row)

        supplier = self.manage_item.selectSupplierData()
        for row in supplier:
            self.supplier.addItem(row)

    def onToggledTrack(self, flag):
        if flag == 'Yes':
            self.on_hand_stock.setText('0')
            self.on_hand_stock.setDisabled(False)
            self.available_stock.setText('0')
            self.available_stock.setDisabled(False)

        elif flag == 'No':
            self.on_hand_stock.setText('0')
            self.on_hand_stock.setDisabled(True)
            self.available_stock.setText('0')
            self.available_stock.setDisabled(True)

    def setNumericInputValidator(self):
        self.item_price_input_validator = QDoubleValidator()
        self.item_price_input_validator.setDecimals(2)  # Set the number of decimal places
        self.item_price_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.item_price_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

        self.stock_input_validator = QDoubleValidator()
        self.stock_input_validator.setDecimals(0)  # Set the number of decimal places
        self.stock_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.stock_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

    def saveItem(self):
        # convert input
        converted_barcode = str(self.barcode.text())
        converted_item_name = str(self.item_name.currentText())
        converted_expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)
        converted_item_type = str(self.item_type.currentText())
        converted_brand = str(self.brand.currentText())
        converted_sales_group = str(self.sales_group.currentText())
        converted_supplier = str(self.supplier.currentText())
        converted_cost = '{:.2f}'.format(float(self.cost.text()))
        converted_discount = '{:.2f}'.format(float(self.discount.text()))
        converted_sell_price = '{:.2f}'.format(float(self.sell_price.text()))
        converted_effective_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate)
        converted_on_hand_stock = int(self.on_hand_stock.text())
        converted_available_stock = int(self.available_stock.text())

        # Perform input validation here
        if (converted_item_type == '' or converted_brand == '' or converted_sales_group == '' or converted_supplier == '' or converted_item_name == '' or converted_barcode == '' or converted_cost == 0.00 or converted_discount == 0.00 or converted_sell_price == 0.00):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
            
        else:
            if self.track_y.isChecked() and (converted_on_hand_stock == 0 or converted_available_stock == 0):
                 QMessageBox.critical(self, "Error", "All fields must be filled.")
            else:
                self.manage_item.insertItemTypeData(converted_item_type)
                self.manage_item.insertBrandData(converted_brand)
                self.manage_item.insertSalesGroupData(converted_sales_group)
                self.manage_item.insertSupplierData(converted_supplier)

                print('STEP A -- DONE')

                converted_item_type_id = self.manage_item.selectItemTypeId(converted_item_type)
                converted_brand_id = self.manage_item.selectBrandId(converted_brand)
                converted_sales_group_id = self.manage_item.selectSalesGroupId(converted_sales_group)
                converted_supplier_id = self.manage_item.selectSupplierId(converted_supplier)

                self.manage_item.insertItemData(converted_barcode, converted_item_name, converted_expire_dt, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id)

                print('STEP B -- DONE')

                converted_item_id = self.manage_item.selectItemId(converted_barcode, converted_item_name, converted_expire_dt, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id)

                self.manage_item.insertItemPriceData(converted_item_id, converted_cost, converted_discount, converted_sell_price, converted_effective_dt)
                
                if self.track_y.isChecked():
                    self.manage_inventory.insertStockData(converted_supplier_id, converted_item_id, converted_on_hand_stock, converted_available_stock)

                    print('ITEM TRACKED!')
                    self.accept()
                else:
                    print('ITEM NOT TRACKED!!')
                    self.accept()

                print('STEP C -- DONE')

                self.data_saved.emit()

                print('NEW ITEM ADDED!')

    def setWidgetsAttributes(self):
        self.setNumericInputValidator()

        self.item_name.setEditable(True)
        self.item_type.setEditable(True)
        self.brand.setEditable(True)
        self.supplier.setEditable(True)
        
        self.sales_group.addItem('Retail')
        self.sales_group.addItem('Wholesale')

        self.barcode.setPlaceholderText('Barcode')
        self.cost.setPlaceholderText('Cost')
        self.discount.setPlaceholderText('Discount')
        self.sell_price.setPlaceholderText('Sell price')

        self.cost.setValidator(self.item_price_input_validator)     
        self.discount.setValidator(self.item_price_input_validator)  
        self.sell_price.setValidator(self.item_price_input_validator)

        self.expire_dt.setMinimumDate(QDate.currentDate())
        self.effective_dt.setMinimumDate(QDate.currentDate())

        self.expire_dt.setCalendarPopup(True)
        self.effective_dt.setCalendarPopup(True)

        self.cost.setText('0')
        self.discount.setText('0')
        self.sell_price.setText('0')
        self.inventory_track_prompt.setText('Track inventory for this item?')
        self.track_y.setText('Yes')
        self.track_y.toggled.connect(lambda: self.onToggledTrack('Yes'))
        self.track_n.setText('No')
        self.track_n.toggled.connect(lambda: self.onToggledTrack('No'))
        self.track_n.setChecked(True)

        self.on_hand_stock.setPlaceholderText('On hand stock')
        self.on_hand_stock.setValidator(self.stock_input_validator)
        self.available_stock.setPlaceholderText('Available stock')
        self.available_stock.setValidator(self.stock_input_validator)

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(self.saveItem)

    def createLayout(self):
        self.grid_layout = QGridLayout()

        self.barcode = QLineEdit()
        self.item_name = QComboBox()
        self.expire_dt = QDateEdit()
        self.item_type = QComboBox()
        self.brand = QComboBox()
        self.sales_group = QComboBox()
        self.supplier = QComboBox()
        self.cost = QLineEdit()
        self.discount = QLineEdit()
        self.sell_price = QLineEdit()
        self.effective_dt = QDateEdit()
        self.inventory_track_prompt = QLabel() 
        self.track_y = QRadioButton() 
        self.track_n = QRadioButton()
        self.on_hand_stock = QLineEdit()
        self.available_stock = QLineEdit()
        self.save_button = QPushButton()
        
        self.fillComboBox()
        self.setWidgetsAttributes()

        self.grid_layout.addWidget(self.barcode, 0, 0) # -- barcode (widget[0])
        self.grid_layout.addWidget(self.item_name, 1, 0) # -- item_name (widget[1])
        self.grid_layout.addWidget(self.expire_dt, 2, 0) # -- expire_dt (widget[2])
        self.grid_layout.addWidget(self.item_type, 3, 0) # -- item_type (widget[3])
        self.grid_layout.addWidget(self.brand, 4, 0) # -- brand (widget[4])
        self.grid_layout.addWidget(self.sales_group, 5, 0) # -- sales_group (widget[5])
        self.grid_layout.addWidget(self.supplier, 6, 0) # -- supplier (widget[6])
        self.grid_layout.addWidget(self.cost, 7, 0) # -- cost (widget[7])
        self.grid_layout.addWidget(self.discount, 8, 0) # -- discount (widget[8])
        self.grid_layout.addWidget(self.sell_price, 9, 0) # -- sell_price (widget[9])
        self.grid_layout.addWidget(self.effective_dt, 10, 0) # -- effective_dt (widget[10])
        self.grid_layout.addWidget(self.inventory_track_prompt, 11, 0) # -- inventory_track_prompt (widget[11]) x
        self.grid_layout.addWidget(self.track_y, 12, 0) # -- track_y (widget[12]) x
        self.grid_layout.addWidget(self.track_n, 13, 0) # -- track_n (widget[13]) x
        self.grid_layout.addWidget(self.on_hand_stock, 14, 0) # -- on_hand_stock (widget[14])
        self.grid_layout.addWidget(self.available_stock, 15, 0) # -- available_stock (widget[15])
        self.grid_layout.addWidget(self.save_button, 16, 0) # -- save_button (widget[16]) x

        self.setLayout(self.grid_layout)

class EditItemWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self, row_index, row_value):
        super().__init__()

        self.setWindowTitle('Edit Item')

        self.callSQLUtils()
        self.createLayout(row_index, row_value)

    def callSQLUtils(self):
        self.manage_item = ItemManagementSQL()
        self.manage_inventory = InventoryManagementSQL()

    def fillComboBox(self):
        item_name = self.manage_item.selectItemData()
        for row in item_name:
            self.item_name.addItem(row)

        item_type = self.manage_item.selectItemTypeData()
        for row in item_type:
            self.item_type.addItem(row)

        brand = self.manage_item.selectBrandData()
        for row in brand:
            self.brand.addItem(row)

        supplier = self.manage_item.selectSupplierData()
        for row in supplier:
            self.supplier.addItem(row)

    def onToggledTrack(self, flag):
        if flag == 'Yes':
            self.on_hand_stock.setText('0')
            self.on_hand_stock.setDisabled(False)
            self.available_stock.setText('0')
            self.available_stock.setDisabled(False)

        elif flag == 'No':
            self.on_hand_stock.setText('0')
            self.on_hand_stock.setDisabled(True)
            self.available_stock.setText('0')
            self.available_stock.setDisabled(True)

    def setNumericInputValidator(self):
        self.item_price_input_validator = QDoubleValidator()
        self.item_price_input_validator.setDecimals(2)  # Set the number of decimal places
        self.item_price_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.item_price_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

        self.stock_input_validator = QDoubleValidator()
        self.stock_input_validator.setDecimals(0)  # Set the number of decimal places
        self.stock_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.stock_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

    def saveItem(self, row_value):
        # convert input
        converted_barcode = str(self.barcode.text())
        converted_item_name = str(self.item_name.currentText())
        converted_expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)

        # Perform input validation here
        if (converted_barcode == '' or converted_item_name == ''):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
          
        else:
            converted_item_id = int(row_value[11])
            converted_item_type_id = int(row_value[12]) 
            converted_brand_id = int(row_value[13]) 
            converted_sales_group_id = int(row_value[14]) 
            converted_supplier_id = int(row_value[15]) 

            self.manage_item.updateItemData(converted_barcode, converted_item_name, converted_expire_dt, converted_item_id, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id)

            print('STEP A -- DONE')

            self.data_saved.emit()

            print('ITEM HAS BEEN EDITED!')

            self.accept()

    def setWidgetsAttributes(self, row_index, row_value):
        self.setNumericInputValidator()

        self.item_name.setEditable(True)
        self.item_type.setEditable(True)
        self.brand.setEditable(True)
        self.supplier.setEditable(True)
    
        self.sales_group.addItem('Retail')
        self.sales_group.addItem('Wholesale')

        self.barcode.setPlaceholderText('Barcode')
        self.cost.setPlaceholderText('Cost')
        self.discount.setPlaceholderText('Discount')
        self.sell_price.setPlaceholderText('Sell price')

        self.cost.setValidator(self.item_price_input_validator)     
        self.discount.setValidator(self.item_price_input_validator)  
        self.sell_price.setValidator(self.item_price_input_validator)

        self.expire_dt.setMinimumDate(QDate.currentDate())
        self.effective_dt.setMinimumDate(QDate.currentDate())

        self.expire_dt.setCalendarPopup(True)
        self.effective_dt.setCalendarPopup(True)

        self.barcode.setText(row_value[0])
        self.item_name.setCurrentText(row_value[1])
        self.expire_dt.setDate(QDate.fromString(row_value[2], Qt.DateFormat.ISODate))
        self.item_type.setCurrentText(row_value[3])
        self.brand.setCurrentText(row_value[4])
        self.sales_group.setCurrentText(row_value[5])
        self.supplier.setCurrentText(row_value[6])
        self.cost.setText(str(row_value[7]))
        self.discount.setText(str(row_value[8]))
        self.sell_price.setText(str(row_value[9]))
        self.effective_dt.setDate(QDate.fromString(row_value[10], Qt.DateFormat.ISODate))

        self.item_type.setDisabled(True)
        self.brand.setDisabled(True)
        self.sales_group.setDisabled(True)
        self.supplier.setDisabled(True)
        self.cost.setDisabled(True)
        self.discount.setDisabled(True)
        self.sell_price.setDisabled(True)
        self.effective_dt.setDisabled(True)

        # self.inventory_track_prompt.setText('Track inventory for this item?')
        # self.track_y.setText('Yes')
        # self.track_y.toggled.connect(lambda: self.onToggledTrack('Yes'))
        # self.track_n.setText('No')
        # self.track_n.toggled.connect(lambda: self.onToggledTrack('No'))
        # self.track_n.setChecked(True)

        # self.on_hand_stock.setPlaceholderText('On hand stock')
        # self.on_hand_stock.setValidator(self.stock_input_validator)
        # self.available_stock.setPlaceholderText('Available stock')
        # self.available_stock.setValidator(self.stock_input_validator)

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(lambda: self.saveItem(row_value))

    def createLayout(self, row_index, row_value):
        self.grid_layout = QGridLayout()

        self.barcode = QLineEdit()
        self.item_name = QComboBox()
        self.expire_dt = QDateEdit()
        self.item_type = QComboBox()
        self.brand = QComboBox()
        self.sales_group = QComboBox()
        self.supplier = QComboBox()
        self.cost = QLineEdit()
        self.discount = QLineEdit()
        self.sell_price = QLineEdit()
        self.effective_dt = QDateEdit()
        # self.inventory_track_prompt = QLabel() 
        # self.track_y = QRadioButton() 
        # self.track_n = QRadioButton()
        # self.on_hand_stock = QLineEdit()
        # self.available_stock = QLineEdit()
        self.save_button = QPushButton()
        
        self.fillComboBox()
        self.setWidgetsAttributes(row_index, row_value)

        self.grid_layout.addWidget(self.barcode, 0, 0) # -- barcode (widget[0])
        self.grid_layout.addWidget(self.item_name, 1, 0) # -- item_name (widget[1])
        self.grid_layout.addWidget(self.expire_dt, 2, 0) # -- expire_dt (widget[2])
        self.grid_layout.addWidget(self.item_type, 3, 0) # -- item_type (widget[3])
        self.grid_layout.addWidget(self.brand, 4, 0) # -- brand (widget[4])
        self.grid_layout.addWidget(self.sales_group, 5, 0) # -- sales_group (widget[5])
        self.grid_layout.addWidget(self.supplier, 6, 0) # -- supplier (widget[6])
        self.grid_layout.addWidget(self.cost, 7, 0) # -- cost (widget[7])
        self.grid_layout.addWidget(self.discount, 8, 0) # -- discount (widget[8])
        self.grid_layout.addWidget(self.sell_price, 9, 0) # -- sell_price (widget[9])
        self.grid_layout.addWidget(self.effective_dt, 10, 0) # -- effective_dt (widget[10])
        # self.grid_layout.addWidget(self.inventory_track_prompt, 11, 0) # -- inventory_track_prompt (widget[11]) x
        # self.grid_layout.addWidget(self.track_y, 12, 0) # -- track_y (widget[12]) x
        # self.grid_layout.addWidget(self.track_n, 13, 0) # -- track_n (widget[13]) x
        # self.grid_layout.addWidget(self.on_hand_stock, 14, 0) # -- on_hand_stock (widget[14])
        # self.grid_layout.addWidget(self.available_stock, 15, 0) # -- available_stock (widget[15])
        self.grid_layout.addWidget(self.save_button, 16, 0) # -- save_button (widget[16]) x

        self.setLayout(self.grid_layout)

class ItemListTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.callSQLUtils()
        self.setAttributes()

    def callSQLUtils(self):
        self.manage_item = ItemManagementSQL()

    def openEditItemWindow(self, row_index, row_value):
        edit_item_window = EditItemWindow(row_index, row_value)
        edit_item_window.data_saved.connect(lambda: self.displayItemList(''))
        edit_item_window.exec()

    def displayFilteredItemList(self, text_filter):
        all_item_data = self.manage_item.selectAllItemData(text_filter)

        self.setRowCount(len(all_item_data))

        for row_index, row_value in enumerate(all_item_data):
            total_cell = row_value[:11] # limits the data shown in the table
            
            for col_index, col_value in enumerate(total_cell):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def displayItemList(self, text):
        all_item_data = self.manage_item.selectAllItemData(text)

        self.setRowCount(50)

        for row_index, row_value in enumerate(all_item_data):
            total_cell = row_value[:11] # limits the data shown in the table

            for col_index, col_value in enumerate(total_cell):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.openEditItemWindow(row_index, row_value))
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def setAttributes(self):
        self.setColumnCount(12) # counts starting from 1 to n
        self.setHorizontalHeaderLabels(['','Barcode','Item name','Expire date','Item type','Brand','Sales group','Supplier','Cost','Discount','Sell price','Effective date'])
        
        self.displayItemList('')

# main layout
class ItemManagement(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')
        
        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.manage_item = ItemManagementSQL()

    def fillItemListTable(self):
        filter_text = self.filter_bar.text()

        if filter_text == '':
            self.item_list.displayItemList('')
        else:
            self.item_list.displayFilteredItemList(filter_text)

    def openAddItemWindow(self):
        add_item_window = AddItemWindow()
        add_item_window.data_saved.connect(lambda: self.item_list.displayItemList(''))
        add_item_window.exec()

    def setWidgetsAttributes(self):
        self.filter_bar.setPlaceholderText('Filter item by...')
        self.filter_bar.textChanged.connect(self.fillItemListTable)
        self.add_button.setText('ADD')
        self.add_button.clicked.connect(self.openAddItemWindow)

    def createLayout(self):
        self.manage_item.createAllItemTable()

        self.grid_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.add_button = QPushButton()
        self.item_list = ItemListTable()

        self.setWidgetsAttributes()
        self.fillItemListTable()

        self.grid_layout.addWidget(self.filter_bar,0,0)
        self.grid_layout.addWidget(self.add_button,0,1)
        self.grid_layout.addWidget(self.item_list,1,0,1,2)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagement()
    window.show()
    sys.exit(pos_app.exec())




