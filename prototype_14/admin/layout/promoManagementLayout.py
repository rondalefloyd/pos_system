import sqlite3
import sys, os
import csv
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from widget.promoManagementWidget import *
from util.promoManagementSchema import *
from util.salesTableSchema import *

class PromoManagementLayout(CustomGroupBox):
    def __init__(self):
        super().__init__()

        self.sales_table_schema = SalesTableSchema()
        self.sales_table_schema.createSalesTable()
        self.promo_management_schema = PromoManagementSchema()
    
        self.createLayout()
        self.refreshUI()
    
    def refreshUI(self):
        self.total_label.setText(f'TOTAL: {self.promo_management_schema.countTotalPromo()}')
        self.data_list = None
        self.current_edit_button = None
        self.populateTable()


        print('Window has been refreshed.')

    def importData(self):
        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')
        csv_file_name = os.path.basename(csv_file)

        if csv_file:
            # Open the CSV file with 'utf-8-sig' encoding to remove the BOM
            with open(csv_file, 'r', encoding='utf-8-sig', newline='') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    promo_name, promo_type, discount_percent, description = row
                    if promo_name == '' or promo_type == '' or discount_percent == '':
                        QMessageBox.critical(self, 'Error', f'Unable to import {csv_file_name} due to missing values.')
                        print('Failed to import')
                        return
                    else:
                        self.promo_management_schema.addNewPromo(promo_name, promo_type, discount_percent, description)

            self.refreshUI()

        QMessageBox.information(self, 'Success', f"All data from '{csv_file_name}' has been imported.")
        print('Successfully imported.')

    def saveData(self, reference):
        if self.promo_name_field.currentText() == '' or self.promo_type_field.currentText() == '' or self.discount_percent_field.text() == '':
            QMessageBox.critical(self, 'Invalid', "All required fields must be filled.")
        else:
            promo_name = self.promo_name_field.currentText()
            promo_type = self.promo_type_field.currentText()
            discount_percent = self.discount_percent_field.text()
            description = self.description_field.toPlainText()

            if reference == 'save_new':
                self.promo_management_schema.addNewPromo(promo_name, promo_type, discount_percent, description)
            if reference == 'save_edit':
                promo_id = self.promo_id
                self.promo_management_schema.editSelectedPromo(promo_name, promo_type, discount_percent, description, promo_id)
            
            self.refreshUI()

            QMessageBox.information(self, 'Success', f"New promo has been added.")

        print('New data has been added.')

    def deleteData(self, row_value):
        promo_name = f'{row_value[0]}'
        promo_id = f'{row_value[4]}'

        confirmation = QMessageBox.warning(self, 'Delete', f'Are you sure you want to delete {promo_name}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes:
            self.promo_management_schema.deleteSelectedPromo(promo_id)
            # Reset the current_edit_button to None
            
            if self.panel_d.isVisible() == True:
                self.onPushButtonClicked(reference='add')

            self.refreshUI()

        elif confirmation == QMessageBox.StandardButton.No:
            print("wasn't deleted")
            self.filter_by_date_field.setCurrentText(self.filter_by_date_field.currentText())
            pass
        

    def updatePanelD(
            self,
            reference='',
            row_value=''
    ):
        if reference == 'add':
            self.promo_name_field.setCurrentText(row_value)
            self.promo_type_field.setCurrentText(row_value)
            self.discount_percent_field.setText(row_value)
            self.description_field.setPlainText(row_value)

        elif reference == 'edit':
            self.promo_name_field.setCurrentText(f'{row_value[0]}')
            self.promo_type_field.setCurrentText(f'{row_value[1]}')
            self.discount_percent_field.setText(f'{row_value[2]}')
            self.description_field.setPlainText(f'{row_value[3]}')
            self.promo_id = f'{row_value[4]}'

        print('Panel D has been updated.')

    def onPushButtonClicked(
        self,
        reference='',
        bool=True,
        row_edit_button='',
        row_value=''
    ):

        if reference == 'refresh':
            self.refreshUI()

        elif reference == 'import':
            self.importData()
        
        elif reference == 'add':
            self.panel_d.show() if bool == True else self.panel_d.hide()
            # Re-enable the previously disabled edit button (if any)
            if self.current_edit_button:
                self.current_edit_button.setDisabled(False)
            
            # Reset the current_edit_button to None
            self.current_edit_button = None
            self.add_button.setDisabled(True)

            self.updatePanelD(reference, '')

        elif reference == 'back':
            self.panel_d.hide() if bool == False else self.panel_d.show()
            # Re-enable the previously disabled edit button (if any)
            if self.current_edit_button:
                self.current_edit_button.setDisabled(False)
            
            # Reset the current_edit_button to None
            self.current_edit_button = None
            self.add_button.setDisabled(False)
        
        elif reference == 'edit':
            self.panel_d.show() if bool == True else self.panel_d.hide()
            # Re-enable the previously disabled edit button (if any)
            if self.current_edit_button:
                self.current_edit_button.setDisabled(False)

            # Disable the clicked edit_button
            row_edit_button.setDisabled(True)
            self.add_button.setDisabled(False)

            # Set the currently disabled edit button to the clicked button
            self.current_edit_button = row_edit_button

            self.updatePanelD(
                reference,
                row_value
            )

        elif reference == 'delete':
            self.deleteData(row_value)

        elif reference == 'save_new':
            self.saveData(reference)

        elif reference == 'save_edit':
            self.saveData(reference)

    def populateTable(self, text='', date_filter=''):
        self.list_table.clearContents()

        date_filter = self.filter_by_date_field.currentText()
        
        print(date_filter)

        date_filter_mapping = {
            'Today': 'listPromoA',
            'Yesterday': 'listPromoB',
            'Last 7 days': 'listPromoC',
            'Last 30 days': 'listPromoD',
            'This month': 'listPromoE',
            'Last month': 'listPromoF',
            'All': 'listPromoG'
        }

        # Check if date_filter is in the mapping
        if date_filter in date_filter_mapping:
            data_filter_method = date_filter_mapping[date_filter]
            
            self.updatePanelD(reference='add')
            self.data_list = getattr(self.promo_management_schema, data_filter_method)(text=text)
            
            if self.current_edit_button:
                self.current_edit_button.setDisabled(False)

            self.current_edit_button = None
            
            
            
        self.list_table.setRowCount(len(self.data_list))

        for row_index, row_value in enumerate(self.data_list):
            column_count = row_value[:4]
            for col_index, col_value in enumerate(column_count):

                self.cell_value = QTableWidgetItem(str(col_value))
                self.edit_button = CustomPushButton(text='EDIT')
                self.delete_button = CustomPushButton(text='DELETE')

                self.edit_button.clicked.connect(
                    lambda 
                    row_index=row_index, 
                    row_edit_button=self.edit_button,
                    row_value=row_value: 
                    self.onPushButtonClicked(
                        reference='edit',
                        row_edit_button=row_edit_button,
                        row_value=row_value
                    )
                )
                self.delete_button.clicked.connect(
                    lambda 
                    row_index=row_index, 
                    row_value=row_value: 
                    self.onPushButtonClicked(
                        reference='delete', 
                        row_value=row_value
                    )
                )

                self.list_table.setItem(row_index, col_index + 2, self.cell_value)
                self.list_table.setCellWidget(row_index, 0, self.edit_button)
                self.list_table.setCellWidget(row_index, 1, self.delete_button)


        print('Table has been populated.')
        

    def showPanelD(self):
        self.panel_d = CustomGroupBox(reference='panel_d_box')
        form_layout = QFormLayout()

        required_indicator = "<font color='red'>*</font>"

        self.back_button = CustomPushButton(reference='back_button', text='BACK')
        self.back_button.clicked.connect(lambda: self.onPushButtonClicked(reference='back', bool=False))
        self.promo_name_field = CustomComboBox(reference='promo_name_field')
        self.promo_type_field = CustomComboBox(reference='promo_type_field')
        self.discount_percent_field = CustomLineEdit()
        self.description_field = CustomTextEdit()
        self.save_button = CustomPushButton(reference='save_button', text='SAVE')
        self.save_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_new'))

        form_layout.addRow(self.back_button)
        form_layout.addRow(f'promo_name {required_indicator}', self.promo_name_field)
        form_layout.addRow(f'promo_type {required_indicator}', self.promo_type_field)
        form_layout.addRow(f'discount_percent {required_indicator}', self.discount_percent_field)
        form_layout.addRow('description', self.description_field)
        form_layout.addRow(self.save_button)

        self.panel_d.setLayout(form_layout)

    def showPanelC(self):
        self.panel_c = CustomGroupBox()
        grid_layout = QGridLayout()

        self.total_label = CustomLabel(reference='total_promo_label', text=f'TOTAL: {self.promo_management_schema.countTotalPromo()}')

        grid_layout.addWidget(self.total_label,0,0)

        self.panel_c.setLayout(grid_layout)

    def showPanelB(self):
        self.panel_b = CustomGroupBox()
        grid_layout = QGridLayout()

        self.filter_field = CustomLineEdit(placeholderText='Filter by barcode, product name, item type, brand, sales group, supplier, inventory_status')
        self.filter_field.textChanged.connect(lambda text: self.populateTable(text=text))
        self.filter_by_date_field = CustomComboBox(reference='filter_by_date_field')
        self.filter_by_date_field.currentTextChanged.connect(lambda date_filter: self.populateTable(date_filter=date_filter))
        self.list_table = CustomTableWidget(reference='list_table')

        grid_layout.addWidget(self.filter_by_date_field,0,0)
        grid_layout.addWidget(self.filter_field,0,1)
        grid_layout.addWidget(self.list_table,1,0,1,2)

        self.panel_b.setLayout(grid_layout)

    def showPanelA(self):
        self.panel_a = CustomGroupBox()
        hbox_layout = QHBoxLayout()

        self.page_label = CustomLabel(text='Promo Management')
        self.refresh_button = CustomPushButton(reference='refresh_button', text='REFRESH')
        self.refresh_button.clicked.connect(lambda: self.onPushButtonClicked(reference='refresh'))
        self.import_button = CustomPushButton(reference='import_button', text='IMPORT')
        self.import_button.clicked.connect(lambda: self.onPushButtonClicked(reference='import'))
        self.add_button = CustomPushButton(reference='add_button', text='ADD')
        self.add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='add', bool=True))

        hbox_layout.addWidget(self.page_label)
        hbox_layout.addWidget(self.refresh_button)
        hbox_layout.addWidget(self.import_button)
        hbox_layout.addWidget(self.add_button)

        self.panel_a.setLayout(hbox_layout)

    def createLayout(self):
        grid_layout = QGridLayout()

        self.showPanelA()
        self.showPanelB()
        self.showPanelC()
        self.showPanelD()

        grid_layout.addWidget(self.panel_a,0,0)
        grid_layout.addWidget(self.panel_b,1,0)
        grid_layout.addWidget(self.panel_c,2,0)
        grid_layout.addWidget(self.panel_d,0,1,0,3)

        self.setLayout(grid_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoManagementLayout()
    window.show()
    sys.exit(pos_app.exec())
