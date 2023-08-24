import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.promo_management_sql import *

class AddPromoWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')

        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.manage_promo = PromoManagementSQL()

    def fillComboBox(self, text):
        promo_data = self.manage_promo.selectPromoData('')
        promo_type = self.manage_promo.selectPromoTypeData('')
        promo_type_value = self.manage_promo.selectPromoTypeValueData('')

        for row in promo_data:
            self.promo_name.addItem(row)

        for row in promo_type:
            self.promo_type.addItem(row)

        for row in promo_type_value:
            self.promo_type_value.addItem(row)

    def savePromo(self):
        # convert input
        converted_promo_name = str(self.promo_name.currentText())
        converted_description = str(self.description.toPlainText())
        converted_promo_type = str(self.promo_type.currentText())
        converted_promo_type_value = str(self.promo_type_value.currentText())

        # Perform input validation here
        if (converted_promo_name == '' or converted_description == '' or converted_promo_type == '' or converted_promo_type_value == ''):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
            
        else:
            self.manage_promo.insertPromoData(converted_promo_name, converted_description, converted_promo_type, converted_promo_type_value)

            print('STEP A -- DONE')

            self.data_saved.emit()

            QMessageBox.information(self, 'Success', 'New promo has been added!')

            print('NEW PROMO ADDED!')
            
            self.accept()

    def setWidgetsAttributes(self):
        self.promo_name.setEditable(True) 
        self.promo_type.setEditable(True) 
        self.promo_type_value.setEditable(True) 
        
        self.description.setPlaceholderText('Promo description')

        self.promo_name.clearEditText()
        self.promo_type.clearEditText()
        self.promo_type_value.clearEditText()

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(self.savePromo)

    def createLayout(self):
        self.grid_layout = QGridLayout()

        self.promo_name = QComboBox()
        self.description = QTextEdit()
        self.promo_type = QComboBox()
        self.promo_type_value = QComboBox()
        self.save_button = QPushButton()
        
        self.fillComboBox('')
        self.setWidgetsAttributes()

        self.grid_layout.addWidget(self.promo_name, 0, 0) # -- promo_name (widget[0])
        self.grid_layout.addWidget(self.description, 1, 0) # -- promo_name (widget[0])
        self.grid_layout.addWidget(self.promo_type, 2, 0) # -- promo_name (widget[0])
        self.grid_layout.addWidget(self.promo_type_value, 3, 0) # -- promo_name (widget[0])
        self.grid_layout.addWidget(self.save_button, 4, 0) # -- save_button (widget[3]) x

        self.setLayout(self.grid_layout)

class EditPromoWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self, row_index, row_value):
        super().__init__()

        self.setWindowTitle('Edit Item')

        self.callSQLUtils()
        self.createLayout(row_index, row_value)

    def callSQLUtils(self):
        self.manage_promo = PromoManagementSQL()

    def fillComboBox(self, text):
        promo_data = self.manage_promo.selectPromoData('')
        promo_type = self.manage_promo.selectPromoTypeData('')
        promo_type_value = self.manage_promo.selectPromoTypeValueData('')

        for row in promo_data:
            self.promo_name.addItem(row)

        for row in promo_type:
            self.promo_type.addItem(row)

        for row in promo_type_value:
            self.promo_type_value.addItem(row)

    def savePromo(self, row_value):
        # convert input
        converted_promo_name = str(self.promo_name.currentText())
        converted_description = str(self.description.toPlainText())
        converted_promo_type = str(self.promo_type.currentText())
        converted_promo_type_value = str(self.promo_type_value.currentText())
        converted_old_promo_name = str(row_value[0].currentText())

        # Perform input validation here
        if (converted_promo_name == '' or converted_description == '' or converted_promo_type == '' or converted_promo_type_value == ''):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
            
        else:
            self.manage_promo.updatePromoData(converted_promo_name, converted_description, converted_promo_type, converted_promo_type_value, converted_old_promo_name)

            print('STEP A -- DONE')

            self.data_saved.emit()

            print('PROMO HAS BEEN EDITED!')
            
            QMessageBox.information(self, 'Success', 'Promo has been edited!')

            self.accept()
            
    def setWidgetsAttributes(self, row_index, row_value):
        self.promo_name.setEditable(True) 
        self.promo_type.setEditable(True) 
        self.promo_type_value.setEditable(True) 
        
        self.description.setPlaceholderText('Promo description')

        self.promo_name.setCurrentText(row_value[0])
        self.description.setPlainText(row_value[1])
        self.promo_type.setCurrentText(row_value[2])
        self.promo_type_value.setCurrentText(row_value[3])

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(self.savePromo)

    def createLayout(self, row_index, row_value):
        self.grid_layout = QGridLayout()

        self.promo_name = QComboBox()
        self.description = QTextEdit()
        self.promo_type = QComboBox()
        self.promo_type_value = QComboBox()
        self.save_button = QPushButton()
        
        self.fillComboBox('')
        self.setWidgetsAttributes(row_index, row_value)

        self.grid_layout.addWidget(self.promo_name, 0, 0) # -- promo_name (widget[0])
        self.grid_layout.addWidget(self.description, 1, 0) # -- promo_name (widget[0])
        self.grid_layout.addWidget(self.promo_type, 2, 0) # -- promo_name (widget[0])
        self.grid_layout.addWidget(self.promo_type_value, 3, 0) # -- promo_name (widget[0])
        self.grid_layout.addWidget(self.save_button, 4, 0) # -- save_button (widget[3]) x

        self.setLayout(self.grid_layout)

class PromoListTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.callSQLUtils()
        self.setAttributes()

    def callSQLUtils(self):
        self.manage_promo = PromoManagementSQL()

    def openEditPromoWindow(self, row_index, row_value):
        edit_promo_window = EditPromoWindow(row_index, row_value)
        edit_promo_window.data_saved.connect(lambda: self.displayPromoList(''))
        edit_promo_window.exec()

    def displayFilteredPromoList(self, text_filter):
        all_promo_data = self.manage_promo.selectAllFilteredPromoData(text_filter)

        self.setRowCount(len(all_promo_data))

        for row_index, row_value in enumerate(all_promo_data):
            for col_index, col_value in enumerate(row_value):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def displayPromoList(self, text):
        all_promo_data = self.manage_promo.selectAllPromoData(text)

        self.setRowCount(50)

        for row_index, row_value in enumerate(all_promo_data):
            for col_index, col_value in enumerate(row_value):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.openEditPromoWindow(row_index, row_value))
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def setAttributes(self):
        self.setColumnCount(5) # counts starting from 1 to n
        self.setHorizontalHeaderLabels(['','Promo name','Description','Promo type','Promo type value'])
        
        self.displayPromoList('')

# main layout
class PromoManagement(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Promo')
        
        self.callSQLUtils()
        self.createLayout()

    def callSQLUtils(self):
        self.manage_promo = PromoManagementSQL()

    def fillPromoListTable(self):
        filter_text = self.filter_bar.text()

        if filter_text == '':
            self.promo_list.displayPromoList('')
        else:
            self.promo_list.displayFilteredPromoList(filter_text)

    def openAddPromoWindow(self):
        add_item_window = AddPromoWindow()
        add_item_window.data_saved.connect(lambda: self.promo_list.displayPromoList(''))
        add_item_window.exec()

    def setWidgetsAttributes(self):
        self.filter_bar.setPlaceholderText('Filter promo by...')
        self.filter_bar.textChanged.connect(self.fillPromoListTable)
        self.add_button.setText('ADD')
        self.add_button.clicked.connect(self.openAddPromoWindow)

    def createLayout(self):
        self.manage_promo.createPromoTable()

        self.grid_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.add_button = QPushButton()
        self.promo_list = PromoListTable()

        self.setWidgetsAttributes()
        self.fillPromoListTable()

        self.grid_layout.addWidget(self.filter_bar,0,0)
        self.grid_layout.addWidget(self.add_button,0,1)
        self.grid_layout.addWidget(self.promo_list,1,0,1,2)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoManagement()
    window.show()
    sys.exit(pos_app.exec())




