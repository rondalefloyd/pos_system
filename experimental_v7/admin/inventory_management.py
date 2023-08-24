import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.item_management_sql import *
from utils.inventory_management_sql import *

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
        self.stock_input_validator = QDoubleValidator()
        self.stock_input_validator.setDecimals(0)  # Set the number of decimal places
        self.stock_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.stock_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

    def saveItem(self, row_value):
        # convert input
        converted_on_hand_stock = int(self.on_hand_stock.text())
        converted_available_stock = int(self.available_stock.text())
        converted_item_id = int(row_value[4])
        converted_supplier_id = int(row_value[5]) 

        print(converted_on_hand_stock, end=', ')
        print(converted_available_stock, end=', ')
        print(converted_item_id, end=', ')
        print(converted_supplier_id, end=', ')

        self.manage_inventory.updateStockData(converted_on_hand_stock, converted_available_stock, converted_item_id, converted_supplier_id)

        print('STEP A -- DONE')

        self.data_saved.emit()

        print('ITEM HAS BEEN EDITED!')

        self.accept()

    def setWidgetsAttributes(self, row_index, row_value):
        self.setNumericInputValidator()

        self.on_hand_stock.setText(str(row_value[2]))
        self.on_hand_stock.setPlaceholderText('On hand stock')
        self.on_hand_stock.setValidator(self.stock_input_validator)
        self.available_stock.setText(str(row_value[3]))
        self.available_stock.setPlaceholderText('Available stock')
        self.available_stock.setValidator(self.stock_input_validator)

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(lambda: self.saveItem(row_value))

    def createLayout(self, row_index, row_value):
        self.grid_layout = QGridLayout()

        self.on_hand_stock = QLineEdit()
        self.available_stock = QLineEdit()
        self.save_button = QPushButton()
        
        self.setWidgetsAttributes(row_index, row_value)

        self.grid_layout.addWidget(self.on_hand_stock, 0, 0) # -- on_hand_stock (widget[14])
        self.grid_layout.addWidget(self.available_stock, 1, 0) # -- available_stock (widget[15])
        self.grid_layout.addWidget(self.save_button, 2, 0) # -- save_button (widget[16]) x

        self.setLayout(self.grid_layout)

class ItemListTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.callSQLUtils()
        self.setAttributes()

    def callSQLUtils(self):
        self.manage_item = ItemManagementSQL()
        self.manage_inventory = InventoryManagementSQL()

    def openEditItemWindow(self, row_index, row_value):
        edit_item_window = EditItemWindow(row_index, row_value)
        edit_item_window.data_saved.connect(lambda: self.displayItemList(''))
        edit_item_window.exec()

    def displayFilteredItemList(self, text_filter):
        all_item_data = self.manage_inventory.selectAllStockData(text_filter)

        self.setRowCount(len(all_item_data))

        for row_index, row_value in enumerate(all_item_data):
            total_cell = row_value[:11] # limits the data shown in the table

            for col_index, col_value in enumerate(total_cell):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def displayItemList(self, text):
        all_item_data = self.manage_inventory.selectAllStockData(text)

        self.setRowCount(50)

        for row_index, row_value in enumerate(all_item_data):
            total_cell = row_value[:4] # limits the data shown in the table

            for col_index, col_value in enumerate(total_cell):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.openEditItemWindow(row_index, row_value))
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def setAttributes(self):
        self.setColumnCount(5) # counts starting from 1 to n
        self.setHorizontalHeaderLabels(['','Supplier','Item name','On hand stock','Available stock'])
        
        self.displayItemList('')

# main layout
class InventoryManagement(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')
        
        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.manage_inventory = InventoryManagementSQL()

    def fillItemListTable(self):
        filter_text = self.filter_bar.text()

        if filter_text == '':
            self.item_list.displayItemList('')
        else:
            self.item_list.displayFilteredItemList(filter_text)

    def setWidgetsAttributes(self):
        self.filter_bar.setPlaceholderText('Filter item by...')
        self.filter_bar.textChanged.connect(self.fillItemListTable)

    def createLayout(self):
        self.manage_inventory.createStockTable()

        self.grid_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.item_list = ItemListTable()

        self.setWidgetsAttributes()
        self.fillItemListTable()

        self.grid_layout.addWidget(self.filter_bar,0,0)
        self.grid_layout.addWidget(self.item_list,1,0)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = InventoryManagement()
    window.show()
    sys.exit(pos_app.exec())




