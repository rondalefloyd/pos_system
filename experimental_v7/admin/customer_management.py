import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.sales_database_table_setup import *
from utils.customer_management_sql import *

class AddCustomerWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')

        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.manage_customer = CustomerManagementSQL()

    # def fillComboBox(self):
    #     item_name = self.manage_item.selectItemData()
    #     for row in item_name:
    #         self.item_name.addItem(row)

    #     item_type = self.manage_item.selectItemTypeData()
    #     for row in item_type:
    #         self.item_type.addItem(row)

    #     brand = self.manage_item.selectBrandData()
    #     for row in brand:
    #         self.brand.addItem(row)

    #     supplier = self.manage_item.selectSupplierData()
    #     for row in supplier:
    #         self.supplier.addItem(row)

    def saveItem(self):
        # convert input
        converted_customer_name = str(self.customer_name.currentText())
        converted_address = str(self.address.text())
        converted_barrio = str(self.barrio.currentText())
        converted_town = str(self.town.currentText())
        converted_phone = str(self.phone.text())
        converted_age = str(self.age.text())
        converted_gender = str(self.gender.currentText())
        converted_martial_status = str(self.martial_status.currentText())

        # Perform input validation here
        if (converted_customer_name == '' or converted_address == '' or converted_barrio == '' or converted_town == '' or converted_phone == '' or converted_age == '' or converted_gender == '' or converted_martial_status == ''):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
            
        else:
            self.manage_customer.insertCustomerData(converted_customer_name, converted_address, converted_barrio, converted_town, converted_phone, converted_age, converted_gender, converted_martial_status)

            print('STEP A -- DONE')

            self.data_saved.emit()

            print('NEW CUSTOMER ADDED!')
            
            self.accept()

    def setWidgetsAttributes(self):
        self.customer_name.setEditable(True)
        self.barrio.setEditable(True)
        self.town.setEditable(True)

        self.address.setPlaceholderText('Address')
        self.phone.setPlaceholderText('Phone')
        self.age.setPlaceholderText('Age')

        self.gender.addItem('Male')
        self.gender.addItem('Female')
        self.martial_status.addItem('Single')
        self.martial_status.addItem('Married')
        self.martial_status.addItem('Separated')
        self.martial_status.addItem('Widowed')

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(self.saveItem)

    def createLayout(self):
        self.grid_layout = QGridLayout()

        self.customer_name = QComboBox()
        self.address = QLineEdit()
        self.barrio = QComboBox()
        self.town = QComboBox()
        self.phone = QLineEdit()
        self.age = QLineEdit()
        self.gender = QComboBox()
        self.martial_status = QComboBox()
        self.save_button = QPushButton()
        
        # self.fillComboBox()
        self.setWidgetsAttributes()

        self.grid_layout.addWidget(self.customer_name, 0, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.address, 1, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.barrio, 2, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.town, 3, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.phone, 4, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.age, 5, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.gender, 6, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.martial_status, 7, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.save_button, 8, 0) # -- save_button (widget[3]) x

        self.setLayout(self.grid_layout)

class EditCustomerWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self, row_index, row_value):
        super().__init__()

        self.setWindowTitle('Edit Item')

        self.callSQLUtils()
        self.createLayout(row_index, row_value)

    def callSQLUtils(self):
        self.manage_customer = CustomerManagementSQL()

    # def fillComboBox(self):
    #     item_name = self.manage_item.selectItemData()
    #     for row in item_name:
    #         self.item_name.addItem(row)

    #     item_type = self.manage_item.selectItemTypeData()
    #     for row in item_type:
    #         self.item_type.addItem(row)

    #     brand = self.manage_item.selectBrandData()
    #     for row in brand:
    #         self.brand.addItem(row)

    #     supplier = self.manage_item.selectSupplierData()
    #     for row in supplier:
    #         self.supplier.addItem(row)

    def saveCustomer(self, row_value):
        # convert input
        converted_customer_name = str(self.customer_name.currentText())
        converted_address = str(self.address.text())
        converted_barrio = str(self.barrio.currentText())
        converted_town = str(self.town.currentText())
        converted_phone = str(self.phone.text())
        converted_age = int(self.age.text())
        converted_gender = str(self.gender.currentText())
        converted_martial_status = str(self.martial_status.currentText())

        # Perform input validation here
        if (converted_customer_name == '' or converted_address == '' or converted_barrio == '' or converted_town == '' or converted_phone == '' or converted_age == '' or converted_gender == '' or converted_martial_status == ''):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
            
        else:
            self.manage_customer.updateCustomerData(converted_customer_name, converted_address, converted_barrio, converted_town, converted_phone, converted_age, converted_gender, converted_martial_status)

            print('STEP A -- DONE')

            self.data_saved.emit()

            print('CUSTOMER HAS BEEN EDITED!')
            
            self.accept()
            
    def setWidgetsAttributes(self, row_index, row_value):
        self.customer_name.setEditable(True)
        self.barrio.setEditable(True)
        self.town.setEditable(True)

        self.address.setPlaceholderText('Address')
        self.phone.setPlaceholderText('Phone')
        self.age.setPlaceholderText('Age')

        self.gender.addItem('Male')
        self.gender.addItem('Female')
        self.martial_status.addItem('Single')
        self.martial_status.addItem('Married')
        self.martial_status.addItem('Separated')
        self.martial_status.addItem('Widowed')

        self.customer_name.setCurrentText(row_value[0])
        self.address.setText(row_value[1])
        self.barrio.setCurrentText(row_value[2])
        self.town.setCurrentText(row_value[3])
        self.phone.setText(row_value[4])
        self.age.setText(str(row_value[5]))
        self.gender.setCurrentText(row_value[6])
        self.martial_status.setCurrentText(row_value[7])

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(self.saveCustomer)

    def createLayout(self, row_index, row_value):
        self.grid_layout = QGridLayout()

        self.customer_name = QComboBox()
        self.address = QLineEdit()
        self.barrio = QComboBox()
        self.town = QComboBox()
        self.phone = QLineEdit()
        self.age = QLineEdit()
        self.gender = QComboBox()
        self.martial_status = QComboBox()
        self.save_button = QPushButton()
        
        # self.fillComboBox()
        self.setWidgetsAttributes(row_index, row_value)

        self.grid_layout.addWidget(self.customer_name, 0, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.address, 1, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.barrio, 2, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.town, 3, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.phone, 4, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.age, 5, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.gender, 6, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.martial_status, 7, 0) # -- customer_name (widget[0])
        self.grid_layout.addWidget(self.save_button, 8, 0) # -- save_button (widget[3]) x

        self.setLayout(self.grid_layout)

class CustomerListTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.callSQLUtils()
        self.setAttributes()

    def callSQLUtils(self):
        self.manage_customer = CustomerManagementSQL()

    def openEditCustomerWindow(self, row_index, row_value):
        edit_customer_window = EditCustomerWindow(row_index, row_value)
        edit_customer_window.data_saved.connect(lambda: self.displayCustomerList(''))
        edit_customer_window.exec()

    def displayFilteredCustomerList(self, text_filter):
        all_customer_data = self.manage_customer.selectAllFilteredCustomerData(text_filter)

        self.setRowCount(len(all_customer_data))

        for row_index, row_value in enumerate(all_customer_data):
            for col_index, col_value in enumerate(row_value):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def displayCustomerList(self, text):
        all_customer_data = self.manage_customer.selectAllCustomerData(text)

        self.setRowCount(50)

        for row_index, row_value in enumerate(all_customer_data):
            for col_index, col_value in enumerate(row_value):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.openEditCustomerWindow(row_index, row_value))
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def setAttributes(self):
        self.setColumnCount(9) # counts starting from 1 to n
        self.setHorizontalHeaderLabels(['', 'Name', 'Address', 'Barrio', 'Town', 'Phone', 'Age', 'Gender', 'Martial status'])
        
        self.displayCustomerList('')

# main layout
class CustomerManagement(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Customer')
        
        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.sales_database_table_setup = SalesDatabaseSetup()
        self.manage_customer = CustomerManagementSQL()

    def fillCustomerListTable(self):
        filter_text = self.filter_bar.text()

        if filter_text == '':
            self.customer_list.displayCustomerList('')
        else:
            self.customer_list.displayFilteredCustomerList(filter_text)

    def openAddCustomerWindow(self):
        add_item_window = AddCustomerWindow()
        add_item_window.data_saved.connect(lambda: self.customer_list.displayCustomerList(''))
        add_item_window.exec()

    def setWidgetsAttributes(self):
        self.filter_bar.setPlaceholderText('Filter customer by...')
        self.filter_bar.textChanged.connect(self.fillCustomerListTable)
        self.add_button.setText('ADD')
        self.add_button.clicked.connect(self.openAddCustomerWindow)

    def createLayout(self):
        self.sales_database_table_setup.createDatabaseTable()

        self.grid_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.add_button = QPushButton()
        self.customer_list = CustomerListTable()

        self.setWidgetsAttributes()
        self.fillCustomerListTable()

        self.grid_layout.addWidget(self.filter_bar,0,0)
        self.grid_layout.addWidget(self.add_button,0,1)
        self.grid_layout.addWidget(self.customer_list,1,0,1,2)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = CustomerManagement()
    window.show()
    sys.exit(pos_app.exec())




