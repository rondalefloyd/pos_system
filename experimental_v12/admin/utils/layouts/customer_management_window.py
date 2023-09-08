import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

# -- changeable
from utils.schemas.sales_table_schema import *
from utils.schemas.customer_management_schema import *
from utils.widgets.customer_management_widget import *
# ----

class CustomerManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.sales_table_schema = SalesTableSchema()

        # -- changeable
        self.customer_management_schema = CustomerManagementSchema()
        # ----

        self.sales_table_schema.createSalesTable()

        self.main_layout = QGridLayout()

        self.panel_a_widget = self.showPanelA()
        self.panel_b_widget = self.showPanelB()

        self.main_layout.addWidget(self.panel_a_widget,0,0)
        self.main_layout.addWidget(self.panel_b_widget,0,1)

        self.setLayout(self.main_layout)

    def showPanelA(self):
        self.panel_a = CustomGroupBox(reference='panel_a')
        self.panel_a_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.filter_bar.textChanged.connect(lambda text: self.populateTable(filter_text=text))
        self.add_button = CustomPushButton(text='ADD')
        self.add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='add_button'))
        self.list_table = CustomTableWidget(reference='list_table')

        self.data_saved.connect(self.populateTable)

        self.populateTable()

        self.panel_a_layout.addWidget(self.filter_bar,0,0)
        self.panel_a_layout.addWidget(self.add_button,0,1)
        self.panel_a_layout.addWidget(self.list_table,1,0,1,2)

        self.panel_a.setLayout(self.panel_a_layout)

        return self.panel_a

    def showPanelB(self):
        self.panel_b = CustomGroupBox(reference='panel_b')
        self.panel_b_layout = QFormLayout()

        self.close_button = CustomPushButton(text='CLOSE')
        self.close_button.clicked.connect(lambda: self.onPushButtonClicked(reference='close_button'))

        # -- changeable
        self.customer_name = CustomComboBox(reference='customer_name')
        self.address = CustomTextEdit(reference='address')
        self.barrio = CustomComboBox(reference='barrio')
        self.town = CustomComboBox(reference='town')
        self.phone = CustomLineEdit(reference='phone')
        self.age = CustomLineEdit(reference='age')
        self.gender = CustomComboBox(reference='gender')
        self.marital_status = CustomComboBox(reference='marital_status')
        # ----
        self.data_saved.connect(self.updateComboBox)

        self.save_add_button = CustomPushButton(text='SAVE NEW')
        self.save_add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_add_button'))
        self.save_edit_button = CustomPushButton(text='SAVE CHANGE')
        self.save_edit_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_edit_button'))

        self.panel_b_layout.addRow(self.close_button)

        # -- changeable
        self.panel_b_layout.addRow('customer_name', self.customer_name)
        self.panel_b_layout.addRow('address', self.address)
        self.panel_b_layout.addRow('barrio', self.barrio)
        self.panel_b_layout.addRow('town', self.town)
        self.panel_b_layout.addRow('phone', self.phone)
        self.panel_b_layout.addRow('age', self.age)
        self.panel_b_layout.addRow('gender', self.gender)
        self.panel_b_layout.addRow('marital_status', self.marital_status)
        # ----

        self.panel_b_layout.addRow(self.save_add_button)
        self.panel_b_layout.addRow(self.save_edit_button)

        self.panel_b.setLayout(self.panel_b_layout)

        return self.panel_b


    def populateTable(self, filter_text=''):
        self.list_table.clearContents()

        # -- changeable
        if filter_text == '':
            all_data = self.customer_management_schema.listCustomer(filter_text)
        else:
            all_data = self.customer_management_schema.listCustomer(filter_text)
        # ----

        for row_index, row_value in enumerate(all_data):
            total_cell = row_value[:8]

            for col_index, col_value in enumerate(total_cell):
                edit_button = CustomPushButton(text='EDIT')
                edit_button.clicked.connect(lambda index=row_index, data=row_value: self.onPushButtonClicked(reference='edit_button', data=data))
                remove_button = CustomPushButton(text='REMOVE')
                remove_button.clicked.connect(lambda index=row_index, data=row_value: self.onPushButtonClicked(reference='remove_button', data=data))
                cell_value = QTableWidgetItem(str(col_value))

                self.list_table.setItem(row_index, col_index + 2, cell_value)
                self.list_table.setCellWidget(row_index, 0, edit_button)
                self.list_table.setCellWidget(row_index, 1, remove_button)

    def onPushButtonClicked(self, reference, data=''):
        if reference == 'close_button':
            self.panel_b.hide()

        elif reference == 'add_button':
            self.updatePanelB(reference)
        elif reference == 'edit_button':
            self.updatePanelB(reference, data)
        elif reference == 'remove_button':
            self.confirmAction(reference, data)
            
        elif reference == 'save_add_button':
            self.saveData(reference)
        elif reference == 'save_edit_button':
            self.saveData(reference)

    def updatePanelB(self, reference, data=''):
        if reference == 'add_button':
            self.panel_b.show()
            self.save_add_button.show()
            self.save_edit_button.hide()
            
            # -- changeable
            self.customer_name.setCurrentText(data)
            self.address.setPlainText(data)
            self.barrio.setCurrentText(data)
            self.town.setCurrentText(data)
            self.phone.setText(data)
            self.age.setText(data)
            self.gender.setCurrentText(data)
            self.marital_status.setCurrentText(data)
            # ----
            
        elif reference == 'edit_button':
            self.panel_b.show()
            self.save_add_button.hide()
            self.save_edit_button.show()

            # -- changeable
            self.customer_name.setCurrentText(str(data[0]))
            self.address.setPlainText(str(data[1]))
            self.barrio.setCurrentText(str(data[2]))
            self.town.setCurrentText(str(data[3]))
            self.phone.setText(str(data[4]))
            self.age.setText(str(data[5]))
            self.gender.setCurrentText(str(data[6]))
            self.marital_status.setCurrentText(str(data[7]))
            self.customer_id = str(data[8])
            # ----

    def confirmAction(self, reference, data=''):
        if reference == 'remove_button':
            customer_name = str(data[0])
            customer_id = str(data[8])

            dialog = QMessageBox.warning(self, 'Remove', f"Are you sure you want to remove '{customer_name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if dialog == QMessageBox.StandardButton.Yes:
                self.customer_management_schema.removeSelectedReward(customer_id)
                self.data_saved.emit()
                
            else:
                pass

    def saveData(self, reference):
        # -- changeable
        customer_name = str(self.customer_name.currentText())
        address = str(self.address.toPlainText())
        barrio = str(self.barrio.currentText())
        town = str(self.town.currentText())
        phone = str(self.phone.text())
        age = str(self.age.text())
        gender = str(self.gender.currentText())
        marital_status = str(self.marital_status.currentText())
        # ----

        if reference == 'save_add_button':
            # -- changeable
            self.customer_management_schema.addNewCustomer(
                customer_name,
                address,
                barrio,
                town,
                phone,
                age,
                gender,
                marital_status
            )
            # ----
            self.data_saved.emit()

        elif reference == 'save_edit_button':
            # -- changeable
            self.customer_management_schema.editSelectedCustomer(
                customer_name,
                address,
                barrio,
                town,
                phone,
                age,
                gender,
                marital_status,
                self.customer_id
            )
            # ----
            self.data_saved.emit()

    def updateComboBox(self):
        self.customer_name.fillComboBox()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = CustomerManagementWindow()
    window.show()
    sys.exit(pos_app.exec())

