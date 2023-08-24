import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.user_management_sql import *

class AddUserWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')

        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.manage_user = UserManagementSQL()

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
        converted_user_name = str(self.user_name.text())
        converted_password = str(self.password.text())
        converted_access_level = int(self.access_level.text())

        # Perform input validation here
        if (converted_user_name == '' or converted_password == '' or converted_access_level == 0):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
            
        else:
            self.manage_user.insertUserData(converted_user_name, converted_password, converted_access_level)

            print('STEP A -- DONE')

            self.data_saved.emit()

            QMessageBox.information(self, 'Success', 'New user has been added!')

            print('NEW CUSTOMER ADDED!')

    def setWidgetsAttributes(self):
        self.user_name.setPlaceholderText('Name')
        self.password.setPlaceholderText('Password')
        self.access_level.setPlaceholderText('Access level')

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(self.saveItem)

    def createLayout(self):
        self.grid_layout = QGridLayout()

        self.user_name = QLineEdit()
        self.password = QLineEdit()
        self.access_level = QLineEdit()
        self.save_button = QPushButton()
        
        # self.fillComboBox()
        self.setWidgetsAttributes()

        self.grid_layout.addWidget(self.user_name, 0, 0) # -- user_name (widget[0])
        self.grid_layout.addWidget(self.password, 1, 0) # -- password (widget[1])
        self.grid_layout.addWidget(self.access_level, 2, 0) # -- access_level (widget[2])
        self.grid_layout.addWidget(self.save_button, 3, 0) # -- save_button (widget[3]) x

        self.setLayout(self.grid_layout)

class EditUserWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self, row_index, row_value):
        super().__init__()

        self.setWindowTitle('Edit Item')

        self.callSQLUtils()
        self.createLayout(row_index, row_value)

    def callSQLUtils(self):
        self.manage_user = UserManagementSQL()

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

    def saveUser(self, row_value):
        # convert input
        converted_user_name = str(self.user_name.text())
        converted_password = str(self.password.text())
        converted_access_level = int(self.access_level.text())

        # Perform input validation here
        if (converted_password == '' or converted_access_level == 0 or converted_user_name == ''):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
          
        else:
            self.manage_user.updateUserData(converted_access_level, converted_password, converted_user_name)

            print('STEP A -- DONE')

            self.data_saved.emit()

            QMessageBox.information(self, 'Success', 'Item has been edited!')

            print('USER HAS BEEN EDITED!')

    def setWidgetsAttributes(self, row_index, row_value):
        self.user_name.setPlaceholderText('Name')
        self.password.setPlaceholderText('Password')
        self.access_level.setPlaceholderText('Access level')

        self.user_name.setText(row_value[0])
        self.access_level.setText(str(row_value[1]))

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(lambda: self.saveUser(row_value))

    def createLayout(self, row_index, row_value):
        self.grid_layout = QGridLayout()

        self.user_name = QLineEdit()
        self.password = QLineEdit()
        self.access_level = QLineEdit()
        self.save_button = QPushButton()
        
        # self.fillComboBox()
        self.setWidgetsAttributes(row_index, row_value)

        self.grid_layout.addWidget(self.user_name, 0, 0) # -- user_name (widget[0])
        self.grid_layout.addWidget(self.password, 1, 0) # -- user_name (widget[0])
        self.grid_layout.addWidget(self.access_level, 2, 0) # -- access_level (widget[2])
        self.grid_layout.addWidget(self.save_button, 3, 0) # -- save_button (widget[3]) x

        self.setLayout(self.grid_layout)

class UserListTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.callSQLUtils()
        self.setAttributes()

    def callSQLUtils(self):
        self.manage_user = UserManagementSQL()

    def openEditUserWindow(self, row_index, row_value):
        edit_user_window = EditUserWindow(row_index, row_value)
        edit_user_window.data_saved.connect(lambda: self.displayUserList(''))
        edit_user_window.exec()

    def displayFilteredUserList(self, text_filter):
        all_user_data = self.manage_user.selectAllUserData(text_filter)

        self.setRowCount(len(all_user_data))

        for row_index, row_value in enumerate(all_user_data):
            for col_index, col_value in enumerate(row_value):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def displayUserList(self, text):
        all_user_data = self.manage_user.selectAllUserData(text)

        self.setRowCount(50)

        for row_index, row_value in enumerate(all_user_data):
            for col_index, col_value in enumerate(row_value):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.openEditUserWindow(row_index, row_value))
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def setAttributes(self):
        self.setColumnCount(3) # counts starting from 1 to n
        self.setHorizontalHeaderLabels(['','Name','Access level'])
        
        self.displayUserList('')

# main layout
class UserManagement(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add User')
        
        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.manage_user = UserManagementSQL()

    def fillUserListTable(self):
        filter_text = self.filter_bar.text()

        if filter_text == '':
            self.user_list.displayUserList('')
        else:
            self.user_list.displayFilteredUserList(filter_text)

    def openAddUserWindow(self):
        add_item_window = AddUserWindow()
        add_item_window.data_saved.connect(lambda: self.user_list.displayUserList(''))
        add_item_window.exec()

    def setWidgetsAttributes(self):
        self.filter_bar.setPlaceholderText('Filter user by...')
        self.filter_bar.textChanged.connect(self.fillUserListTable)
        self.add_button.setText('ADD')
        self.add_button.clicked.connect(self.openAddUserWindow)

    def createLayout(self):
        self.manage_user.createUserDatabaseTable()

        self.grid_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.add_button = QPushButton()
        self.user_list = UserListTable()

        self.setWidgetsAttributes()
        self.fillUserListTable()

        self.grid_layout.addWidget(self.filter_bar,0,0)
        self.grid_layout.addWidget(self.add_button,0,1)
        self.grid_layout.addWidget(self.user_list,1,0,1,2)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = UserManagement()
    window.show()
    sys.exit(pos_app.exec())




