import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_manager import *

class CustomLineEdit(QLineEdit):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref == 'access_level':
            self.setText('0')
            self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        if self.ref in ['age', 'phone']:
            if event.text().isdigit() or event.key() == 16777219:  # Digit or Backspace key
                if self.text() == '0' and event.key() == 16777219:  # Backspace key
                    return
                if self.text() == '0' and event.text().isdigit():
                    self.setText(event.text())
                else:
                    super().keyPressEvent(event)

        # does nothing
        else:
            super().keyPressEvent(event)
        pass

class CustomComboBox(QComboBox):
    data_saved = pyqtSignal()

    def __init__(self, reference=None):
        super().__init__()

        self.prepareDataManagement()    

        self.ref = reference

        if self.ref in ['customer_name', 'barrio', 'town']:
            self.setEditable(True)

        if self.ref == 'gender':
            self.addItem('Male')
            self.addItem('Female')

        if self.ref == 'marital_status':
            self.addItem('Single')
            self.addItem('Married')
            self.addItem('Separated')
            self.addItem('Widowed')

        self.updateComboBox()
        
    def updateComboBox(self):
        data = self.sales_data_manager.fillCustomerComboBox()
        

        if self.ref == 'customer_name': 
            self.clear()
            for row in data:
                self.addItem(row[0])

        if self.ref == 'barrio': 
            self.clear()
            for row in data:
                self.addItem(row[1])

        if self.ref == 'town': 
            self.clear()
            for row in data:
                self.addItem(row[2])

        self.data_saved.emit()

    def prepareDataManagement(self):
        self.sales_data_manager = SalesDataManager()
    
class CustomTextEdit(QTextEdit):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

class CustomPushButton(QPushButton):
    def __init__(self, text=None, reference=None):
        super().__init__()
        
        self.setText(text)
    
class CustomTableWidget(QTableWidget):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref == 'list_table':
            self.setRowCount(50)
            self.setColumnCount(10)
            self.setHorizontalHeaderLabels(['','',
                'customer_name',
                'address',
                'barrio',
                'town',
                'phone',
                'age',
                'gender',
                'marital_status'
            ])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

        if self.ref == 'panel_b':
            self.setFixedWidth(300)
            self.hide()
        pass

# ------------------------------------------------------------------------------- #

class CustomerManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__() 

        self.prepareDataManagement()
        self.setMainLayout()

    # PANEL B SECTION -------------------------------------------------------- #
    def refreshComboBox(self):
        self.customer_name.updateComboBox()
        self.barrio.updateComboBox()
        self.town.updateComboBox()
    
    def updateEditPanelB(self, row_index, row_data):
        self.save_add_button.hide()
        self.save_edit_button.show()

        data = row_data

        self.customer_name.setCurrentText(str(data[0]))
        self.address.setPlainText(str(data[1]))
        self.barrio.setCurrentText(str(data[2]))
        self.town.setCurrentText(str(data[3]))
        self.phone.setText(str(data[4]))
        self.age.setText(str(data[5]))
        self.gender.setCurrentText(str(data[6]))
        self.marital_status.setCurrentText(str(data[7]))
        self.customer_id = str(data[8])

    def updateAddPanelB(self):
        self.save_add_button.show()
        self.save_edit_button.hide()

    def onSaveButtonClicked(self, reference):
        converted_customer_name = str(self.customer_name.currentText())
        converted_address = str(self.address.toPlainText())
        converted_barrio = str(self.barrio.currentText())
        converted_town = str(self.town.currentText())
        converted_phone = str(self.phone.text())
        converted_age = str(self.age.text())
        converted_gender = str(self.gender.currentText())
        converted_marital_status = str(self.marital_status.currentText())


        if reference == 'add':
            print(reference)
            self.sales_data_manager.addNewCustomer(
                converted_customer_name,
                converted_address,
                converted_barrio,
                converted_town,
                converted_phone,
                converted_age,
                converted_gender,
                converted_marital_status
            )
            QMessageBox.information(self, "Success", "New customer has been added!")
            

        elif reference == 'edit':
            print(reference)
            self.sales_data_manager.editSelectedCustomer(
                converted_customer_name,
                converted_address,
                converted_barrio,
                converted_town,
                converted_phone,
                converted_age,
                converted_gender,
                converted_marital_status,
                self.customer_id
            )
            QMessageBox.information(self, "Success", "customer has been edited!")
            

        self.data_saved.emit()
        

    def handleTextChanged(self, text, reference=None):
        if reference == 'filter_bar':
            self.populateTable(text)
            print(text)

    def onCloseButtonClicked(self):
        self.panel_b.hide()
        self.add_button.setDisabled(False)

    def showPanelB(self): # -- PANEL B
        panel = CustomGroupBox(reference='panel_b')
        panel_layout = QFormLayout()

        self.close_button = CustomPushButton(text='BACK')
        self.close_button.setFixedWidth(50)
        self.close_button.clicked.connect(self.onCloseButtonClicked)

        self.customer_name = CustomComboBox(reference='customer_name')
        self.address = CustomTextEdit(reference='address')
        self.barrio = CustomComboBox(reference='barrio')
        self.town = CustomComboBox(reference='town')
        self.phone = CustomLineEdit(reference='phone')
        self.age = CustomLineEdit(reference='age')
        self.gender = CustomComboBox(reference='gender')
        self.marital_status = CustomComboBox(reference='marital_status')

        self.save_add_button = CustomPushButton(text='SAVE ADD', reference='save_button')
        self.save_add_button.clicked.connect(lambda: self.onSaveButtonClicked('add'))

        self.save_edit_button = CustomPushButton(text='SAVE EDIT', reference='save_button')
        self.save_edit_button.clicked.connect(lambda: self.onSaveButtonClicked('edit'))
        
        panel_layout.addRow(self.close_button)

        panel_layout.addRow('customer_name: ', self.customer_name)
        panel_layout.addRow('address: ', self.address)
        panel_layout.addRow('barrio: ', self.barrio)
        panel_layout.addRow('town: ', self.town)
        panel_layout.addRow('phone: ', self.phone)
        panel_layout.addRow('age: ', self.age)
        panel_layout.addRow('gender: ', self.gender)
        panel_layout.addRow('marital_status: ', self.marital_status)


        panel_layout.addRow(self.save_add_button)
        panel_layout.addRow(self.save_edit_button)

        panel.setLayout(panel_layout)

        return panel

    # PANEL A SECTION -------------------------------------------------------- #
    def showRemoveConfirmationDialog(self, row_index, row_data):
        data = row_data
        customer_name = str(data[0])
        customer_id = str(data[8])

        confirmation = QMessageBox.question(self, "Remove", f"Are you sure you want to remove {customer_name}", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            self.sales_data_manager.removeSelectedCustomer(customer_id)
            self.data_saved.emit()
        else:
            pass

    def onRemoveButtonClicked(self, row_index, row_data):
        self.showRemoveConfirmationDialog(row_index, row_data)
    
    def onEditButtonClicked(self, row_index, row_data):
        self.updateEditPanelB(row_index, row_data)
        self.panel_b.show()
        self.add_button.setDisabled(True)

    def onAddButtonClicked(self):
        self.updateAddPanelB()
        self.panel_b.show()
        self.add_button.setDisabled(True)

    def populateTable(self, text):
        self.list_table.clearContents()
        if text == '':
            data = self.sales_data_manager.listCustomer('')
        else:
            data = self.sales_data_manager.listCustomer(text)

        for row_index, row_data in enumerate(data):
            total_cell = row_data[:8]

            for col_index, col_data in enumerate(total_cell):
                cell = QTableWidgetItem(str(col_data))

                self.list_table.setItem(row_index, col_index + 2, cell)

            self.edit_button = CustomPushButton(text='EDIT')
            self.edit_button.clicked.connect(lambda row_index=row_index, row_data=row_data: self.onEditButtonClicked(row_index, row_data))
            self.list_table.setCellWidget(row_index, 0, self.edit_button)
            
            self.remove_button = CustomPushButton(text='REMOVE')
            self.remove_button.clicked.connect(lambda row_index=row_index, row_data=row_data: self.onRemoveButtonClicked(row_index, row_data))
            self.list_table.setCellWidget(row_index, 1, self.remove_button)


    def showPanelA(self): # -- PANEL A
        panel = CustomGroupBox()
        panel_layout = QGridLayout()

        self.filter_bar = CustomLineEdit(reference='filter_bar')
        self.filter_bar.textChanged.connect(lambda text: self.handleTextChanged(text, reference='filter_bar'))
        self.add_button = CustomPushButton(text='ADD')
        self.add_button.clicked.connect(self.onAddButtonClicked)
        self.list_table = CustomTableWidget(reference='list_table')
        self.populateTable('')
        self.data_saved.connect(lambda: self.populateTable(''))
        self.data_saved.connect(self.refreshComboBox)


        panel_layout.addWidget(self.filter_bar,0,0)
        panel_layout.addWidget(self.add_button,0,1)
        panel_layout.addWidget(self.list_table,1,0,1,2)

        panel.setLayout(panel_layout)

        return panel
    
    # MAIN SECTION -------------------------------------------------------- #
    def setMainLayout(self):
        self.main_layout = QGridLayout()

        self.panel_a = self.showPanelA()
        self.panel_b = self.showPanelB()

        self.main_layout.addWidget(self.panel_a,0,0)
        self.main_layout.addWidget(self.panel_b,0,1)

        self.setLayout(self.main_layout)

    def prepareDataManagement(self):
        self.sales_data_manager = SalesDataManager()
        self.sales_data_manager.createSalesTable() # -- for temporary used while main_admin_window is not yet existing

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = CustomerManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
