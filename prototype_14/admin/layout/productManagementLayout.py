import sqlite3
import sys, os
import csv
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from widget.productManagementWidget import *
from util.productManagementSchema import *
from util.salesTableSchema import *

class ProductManagementLayout(CustomGroupBox):
    def __init__(self):
        super().__init__()

        self.sales_table_schema = SalesTableSchema()
        self.sales_table_schema.createSalesTable()
        self.product_management_schema = ProductManagementSchema()
    
        self.createLayout()
        self.refreshUI()
    
    def refreshUI(self):
        self.total_label.setText(f'TOTAL: {self.product_management_schema.countProductG()}')
        self.list_table_data = None
        self.current_edit_button = None
        self.populateComboBox()
        self.populateTable()


        print('Window has been refreshed.')

# -- data handling
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
                        self.product_management_schema.addNewProduct(promo_name, promo_type, discount_percent, description)

            self.refreshUI()

            if self.panel_d.isVisible() == True:
                self.onPushButtonClicked(reference='add')

        QMessageBox.information(self, 'Success', f"All data from '{csv_file_name}' has been imported.")
        print('Successfully imported.')

    def saveNewData(self):
        if self.promo_name_field.currentText() == '' or self.promo_type_field.currentText() == '' or self.discount_percent_field.text() == '':
            QMessageBox.critical(self, 'Invalid', "All required fields must be filled.")
            return
        else:
            if self.discount_percent_field.text().isnumeric() == False:
                print('not numeric')
                QMessageBox.critical(self, 'Invalid', "Invalid discount percent input.")
                return
            
            promo_name = self.promo_name_field.currentText()
            promo_type = self.promo_type_field.currentText()
            discount_percent = self.discount_percent_field.text()
            description = self.description_field.toPlainText()

            self.product_management_schema.addNewProduct(promo_name, promo_type, discount_percent, description)
            
            if self.panel_d.isVisible() == True:
                self.onPushButtonClicked(reference='add')

            self.refreshUI()

            QMessageBox.information(self, 'Success', f"New promo has been added.")

        print('New data has been added.')

    def saveEditData(self):
        if self.promo_name_field.currentText() == '' or self.promo_type_field.currentText() == '' or self.discount_percent_field.text() == '':
            QMessageBox.critical(self, 'Invalid', "All required fields must be filled.")
            return
        else:
            if self.discount_percent_field.text().isnumeric() == False:
                print('not numeric')
                QMessageBox.critical(self, 'Invalid', "Invalid discount percent input.")
                return
            
            promo_name = self.promo_name_field.currentText()
            promo_type = self.promo_type_field.currentText()
            discount_percent = self.discount_percent_field.text()
            description = self.description_field.toPlainText()

            promo_id = self.promo_id
            self.product_management_schema.editSelectedProduct(promo_name, promo_type, discount_percent, description, promo_id)
            
            if self.panel_d.isVisible() == True:
                self.onPushButtonClicked(reference='add')

            self.refreshUI()

            QMessageBox.information(self, 'Success', f"Product has been edited.")

        pass

    def deleteData(self, row_value):
        promo_name = f'{row_value[0]}'
        promo_id = f'{row_value[5]}'

        confirmation = QMessageBox.warning(self, 'Delete', f'Are you sure you want to delete {promo_name}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes:
            self.product_management_schema.deleteSelectedProduct(promo_id)
            # Reset the current_edit_button to None
            
            if self.panel_d.isVisible() == True:
                self.onPushButtonClicked(reference='add')

            self.refreshUI()

        elif confirmation == QMessageBox.StandardButton.No:
            print("wasn't deleted")
            self.filter_by_date_field.setCurrentText(self.filter_by_date_field.currentText())
            pass
        
# -- layout handling
    def updatePanelD(
            self,
            reference='',
            row_value=''
    ):
        if reference == 'edit':
            self.promo_name_field.setCurrentText(f'{row_value[0]}')
            self.promo_type_field.setCurrentText(f'{row_value[1]}')
            self.discount_percent_field.setText(f'{row_value[2]}')
            self.description_field.setPlainText(f'{row_value[3]}')
            self.promo_id = f'{row_value[5]}'

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

            self.save_new_button.show()
            self.save_edit_button.hide()

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

            self.save_edit_button.show()
            self.save_new_button.hide()

            self.updatePanelD(
                reference,
                row_value
            )

        elif reference == 'delete':
            self.deleteData(row_value)

        elif reference == 'save_new':
            self.saveNewData()

        elif reference == 'save_edit':
            self.saveEditData()

    def populateComboBox(self):
        self.item_name_data = self.product_management_schema.fillItemComboBox()
        self.item_type_data = self.product_management_schema.fillItemTypeComboBox()
        self.brand_data = self.product_management_schema.fillBrandComboBox()
        self.supplier_data = self.product_management_schema.fillSupplierComboBox()
        self.promo_name_data = self.product_management_schema.fillPromoComboBox()

        self.item_name_field.clear()
        self.item_type_field.clear()
        self.brand_field.clear()
        self.supplier_field.clear()
        self.promo_name_field.clear()

        self.item_name_field.addItems([data[0] for data in self.item_name_data])
        self.item_type_field.addItems([data[0] for data in self.item_type_data])
        self.brand_field.addItems([data[0] for data in self.brand_data])
        self.supplier_field.addItems([data[0] for data in self.supplier_data])

        self.promo_name_field.addItem('No promo')
        self.promo_name_field.addItems([data[0] for data in self.promo_name_data])

    def populateTable(self, text='', date_filter=''):
        self.list_table.clearContents()

        date_filter = self.filter_by_date_field.currentText()
        
        print(date_filter)

        date_filter_mapping = {
            'Today': 'listProductA',
            'Yesterday': 'listProductB',
            'Last 7 days': 'listProductC',
            'Last 30 days': 'listProductD',
            'This month': 'listProductE',
            'Last month': 'listProductF',
            'All': 'listProductG'
        }

        # Check if date_filter is in the mapping
        if date_filter in date_filter_mapping:
            data_filter_method = date_filter_mapping[date_filter]
            
            self.updatePanelD(reference='add')
            self.list_table_data = getattr(self.product_management_schema, data_filter_method)(text=text)
            
            if self.current_edit_button:
                self.current_edit_button.setDisabled(False)

            self.current_edit_button = None
            
                 
        self.list_table.setRowCount(len(self.list_table_data))

        for row_index, row_value in enumerate(self.list_table_data):
            column_count = row_value[:5]
            for col_index, col_value in enumerate(column_count):

                self.edit_button = CustomPushButton(reference='edit_button', text='E')
                self.delete_button = CustomPushButton(reference='delete_button', text='D')
                self.cell_value = QTableWidgetItem(f'{col_value}')
                self.discount_percent_cell = QTableWidgetItem(f'{row_value[2]}%')

                self.discount_percent_cell.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

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

                self.list_table.setCellWidget(row_index, 0, self.edit_button)
                self.list_table.setCellWidget(row_index, 1, self.delete_button)
                self.list_table.setItem(row_index, col_index + 2, self.cell_value)
                self.list_table.setItem(row_index, 4, self.discount_percent_cell)


        print('Table has been populated.')
        

# -- layouts
    def showPanelD(self):
        self.panel_d = CustomGroupBox(reference='panel_d_box')
        form_layout = QFormLayout()

        required_indicator = "<font color='red'>*</font>"

        self.back_button = CustomPushButton(reference='back_button', text='BACK')
        self.back_button.clicked.connect(lambda: self.onPushButtonClicked(reference='back', bool=False))
        
        self.barcode_field = CustomLineEdit(reference='barcode_field')
        self.item_name_field = CustomComboBox(reference='item_name_field')
        self.expire_dt_field = CustomDateEdit(reference='expire_dt_field')
        self.item_type_field = CustomComboBox(reference='item_type_field')
        self.brand_field = CustomComboBox(reference='brand_field')
        self.sales_group_field = CustomComboBox(reference='sales_group_field')
        self.supplier_field = CustomComboBox(reference='supplier_field')
        self.cost_field = CustomLineEdit(reference='cost_field')
        self.sell_price_field = CustomLineEdit(reference='sell_price_field')
        self.promo_name_field = CustomComboBox(reference='promo_name_field')
        self.promo_type_field = CustomLineEdit(reference='promo_type_field')
        self.discount_percent_field = CustomLineEdit(reference='discount_percent_field')
        self.discount_value_field = CustomLineEdit(reference='discount_value_field')
        self.new_sell_price_field = CustomLineEdit(reference='new_sell_price_field')
        self.start_dt_field = CustomDateEdit(reference='start_dt_field')
        self.end_dt_field = CustomDateEdit(reference='end_dt_field')
        self.effective_dt_field = CustomDateEdit(reference='effective_dt_field')
        self.inventory_status_field = CustomComboBox(reference='inventory_status_field')
        self.available_stock_field = CustomLineEdit(reference='available_stock_field')
        self.on_hand_stock_field = CustomLineEdit(reference='on_hand_stock_field')

        self.label_barcode = CustomLabel(reference='label_barcode', text='barcode')
        self.label_item_name = CustomLabel(reference='label_item_name', text='item_name')
        self.label_expire_dt = CustomLabel(reference='label_expire_dt', text='expire_dt')
        self.label_item_type = CustomLabel(reference='label_item_type', text='item_type')
        self.label_brand = CustomLabel(reference='label_brand', text='brand')
        self.label_sales_group = CustomLabel(reference='label_sales_group', text='sales_group')
        self.label_supplier = CustomLabel(reference='label_supplier', text='supplier')
        self.label_cost = CustomLabel(reference='label_cost', text='cost')
        self.label_sell_price = CustomLabel(reference='label_sell_price', text='sell_price')
        self.label_promo_name = CustomLabel(reference='label_promo_name', text='promo_name')
        self.label_promo_type = CustomLabel(reference='label_promo_type', text='promo_type')
        self.label_discount_percent = CustomLabel(reference='label_discount_percent', text='discount_percent')
        self.label_discount_value = CustomLabel(reference='label_discount_value', text='discount_value')
        self.label_new_sell_price = CustomLabel(reference='label_new_sell_price', text='new_sell_price')
        self.label_start_dt = CustomLabel(reference='label_start_dt', text='start_dt')
        self.label_end_dt = CustomLabel(reference='label_end_dt', text='end_dt')
        self.label_effective_dt = CustomLabel(reference='label_effective_dt', text='effective_dt')
        self.label_inventory_status = CustomLabel(reference='label_inventory_status', text='inventory_status')
        self.label_available_stock = CustomLabel(reference='label_available_stock', text='available_stock')
        self.label_on_hand_stock = CustomLabel(reference='label_on_hand_stock', text='on_hand_stock')

        self.current_barcode_field = CustomLineEdit(reference='current_barcode_field')
        self.current_item_name_field = CustomLineEdit(reference='current_item_name_field')
        self.current_expire_dt_field = CustomLineEdit(reference='current_expire_dt_field')
        self.current_item_type_field = CustomLineEdit(reference='current_item_type_field')
        self.current_brand_field = CustomLineEdit(reference='current_brand_field')
        self.current_sales_group_field = CustomLineEdit(reference='current_sales_group_field')
        self.current_supplier_field = CustomLineEdit(reference='current_supplier_field')
        self.current_cost_field = CustomLineEdit(reference='current_cost_field')
        self.current_sell_price_field = CustomLineEdit(reference='current_sell_price_field')
        self.current_promo_name_field = CustomLineEdit(reference='current_promo_name_field')
        self.current_promo_type_field = CustomLineEdit(reference='current_promo_type_field')
        self.current_discount_percent_field = CustomLineEdit(reference='current_discount_percent_field')
        self.current_discount_value_field = CustomLineEdit(reference='current_discount_value_field')
        self.current_new_sell_price_field = CustomLineEdit(reference='current_new_sell_price_field')
        self.current_start_dt_field = CustomLineEdit(reference='current_start_dt_field')
        self.current_end_dt_field = CustomLineEdit(reference='current_end_dt_field')
        self.current_effective_dt_field = CustomLineEdit(reference='current_effective_dt_field')
        self.current_inventory_status_field = CustomLineEdit(reference='current_inventory_status_field')
        self.current_available_stock_field = CustomLineEdit(reference='current_available_stock_field')
        self.current_on_hand_stock_field = CustomLineEdit(reference='current_on_hand_stock_field')

        self.label_current_barcode = CustomLabel(reference='label_current_barcode', text='current_barcode')
        self.label_current_item_name = CustomLabel(reference='label_current_item_name', text='current_item_name')
        self.label_current_expire_dt = CustomLabel(reference='label_current_expire_dt', text='current_expire_dt')
        self.label_current_item_type = CustomLabel(reference='label_current_item_type', text='current_item_type')
        self.label_current_brand = CustomLabel(reference='label_current_brand', text='current_brand')
        self.label_current_sales_group = CustomLabel(reference='label_current_sales_group', text='current_sales_group')
        self.label_current_supplier = CustomLabel(reference='label_current_supplier', text='current_supplier')
        self.label_current_cost = CustomLabel(reference='label_current_cost', text='current_cost')
        self.label_current_sell_price = CustomLabel(reference='label_current_sell_price', text='current_sell_price')
        self.label_current_promo_name = CustomLabel(reference='label_current_promo_name', text='current_promo_name')
        self.label_current_promo_type = CustomLabel(reference='label_current_promo_type', text='current_promo_type')
        self.label_current_discount_percent = CustomLabel(reference='label_current_discount_percent', text='current_discount_percent')
        self.label_current_discount_value = CustomLabel(reference='label_current_discount_value', text='current_discount_value')
        self.label_current_new_sell_price = CustomLabel(reference='label_current_new_sell_price', text='current_new_sell_price')
        self.label_current_start_dt = CustomLabel(reference='label_current_start_dt', text='current_start_dt')
        self.label_current_end_dt = CustomLabel(reference='label_current_end_dt', text='current_end_dt')
        self.label_current_effective_dt = CustomLabel(reference='label_current_effective_dt', text='current_effective_dt')
        self.label_current_inventory_status = CustomLabel(reference='label_current_inventory_status', text='current_inventory_status')
        self.label_current_available_stock = CustomLabel(reference='label_current_available_stock', text='current_available_stock')
        self.label_current_on_hand_stock = CustomLabel(reference='label_current_on_hand_stock', text='current_on_hand_stock')
        
        self.save_new_button = CustomPushButton(reference='save_new_button', text='SAVE NEW')
        self.save_new_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_new'))
        self.save_edit_button = CustomPushButton(reference='save_edit_button', text='SAVE EDIT')
        self.save_edit_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_edit'))

        form_layout.addRow(self.back_button)

        # form_layout.addRow(f'promo_name {required_indicator}', self.promo_name_field)
        # form_layout.addRow(f'promo_type {required_indicator}', self.promo_type_field)
        # form_layout.addRow(f'discount_percent {required_indicator}', self.discount_percent_field)
        # form_layout.addRow('description', self.description_field)

        form_layout.addRow(self.label_barcode, self.barcode_field)
        form_layout.addRow(self.label_current_barcode, self.current_barcode_field)
        form_layout.addRow(self.label_item_name, self.item_name_field)
        form_layout.addRow(self.label_current_item_name, self.current_item_name_field)
        form_layout.addRow(self.label_expire_dt, self.expire_dt_field)
        form_layout.addRow(self.label_current_expire_dt, self.current_expire_dt_field)
        form_layout.addRow(self.label_item_type, self.item_type_field)
        form_layout.addRow(self.label_current_item_type, self.current_item_type_field)
        form_layout.addRow(self.label_brand, self.brand_field)
        form_layout.addRow(self.label_current_brand, self.current_brand_field)
        form_layout.addRow(self.label_sales_group, self.sales_group_field)
        form_layout.addRow(self.label_current_sales_group, self.current_sales_group_field)
        form_layout.addRow(self.label_supplier, self.supplier_field)
        form_layout.addRow(self.label_current_supplier, self.current_supplier_field)
        form_layout.addRow(self.label_cost, self.cost_field)
        form_layout.addRow(self.label_current_cost, self.current_cost_field)
        form_layout.addRow(self.label_sell_price, self.sell_price_field)
        form_layout.addRow(self.label_current_sell_price, self.current_sell_price_field)
        form_layout.addRow(self.label_promo_name, self.promo_name_field)
        form_layout.addRow(self.label_current_promo_name, self.current_promo_name_field)
        form_layout.addRow(self.label_promo_type, self.promo_type_field)
        form_layout.addRow(self.label_current_promo_type, self.current_promo_type_field)
        form_layout.addRow(self.label_discount_percent, self.discount_percent_field)
        form_layout.addRow(self.label_current_discount_percent, self.current_discount_percent_field)
        form_layout.addRow(self.label_discount_value, self.discount_value_field)
        form_layout.addRow(self.label_current_discount_value, self.current_discount_value_field)
        form_layout.addRow(self.label_new_sell_price, self.new_sell_price_field)
        form_layout.addRow(self.label_current_new_sell_price, self.current_new_sell_price_field)
        form_layout.addRow(self.label_start_dt, self.start_dt_field)
        form_layout.addRow(self.label_current_start_dt, self.current_start_dt_field)
        form_layout.addRow(self.label_end_dt, self.end_dt_field)
        form_layout.addRow(self.label_current_end_dt, self.current_end_dt_field)
        form_layout.addRow(self.label_effective_dt, self.effective_dt_field)
        form_layout.addRow(self.label_current_effective_dt, self.current_effective_dt_field)
        form_layout.addRow(self.label_inventory_status, self.inventory_status_field)
        form_layout.addRow(self.label_current_inventory_status, self.current_inventory_status_field)
        form_layout.addRow(self.label_available_stock, self.available_stock_field)
        form_layout.addRow(self.label_current_available_stock, self.current_available_stock_field)
        form_layout.addRow(self.label_on_hand_stock, self.on_hand_stock_field)
        form_layout.addRow(self.label_current_on_hand_stock, self.current_on_hand_stock_field)



        form_layout.addRow(self.save_new_button)
        form_layout.addRow(self.save_edit_button)

        self.panel_d.setLayout(form_layout)

    def showPanelC(self):
        self.panel_c = CustomGroupBox()
        grid_layout = QGridLayout()

        self.total_label = CustomLabel(reference='total_promo_label', text=f'TOTAL: {self.product_management_schema.countProductG()}')

        grid_layout.addWidget(self.total_label,0,0)

        self.panel_c.setLayout(grid_layout)

    def showPanelB(self):
        self.panel_b = CustomGroupBox()
        grid_layout = QGridLayout()

        self.filter_field = CustomLineEdit(placeholderText='Filter by barcode, product name, item type, brand, sales group, supplier, inventory status')
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

        self.page_label = CustomLabel(text='Product Management')
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
    window = ProductManagementLayout()
    window.show()
    sys.exit(pos_app.exec())
