import sqlite3
import sys, os
import csv
import pandas as pd
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

    # import data
    def importData(self):
        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')
        csv_file_name = os.path.basename(csv_file)

        if csv_file:
            try:
                # Load the CSV file into a Pandas DataFrame
                df = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

                total_rows = len(df)
                progress_min_range = 0

                progress_dialog = QProgressDialog(f'Importing Data...', 'Cancel', progress_min_range, total_rows, self)
                progress_dialog.setWindowTitle('Import Progress')

                for index, row in df.iterrows():
                    barcode, item_name, expire_dt, item_type, brand, sales_group, supplier, cost, sell_price, available_stock = row[:10]
                    effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)
                    inventory_status = 'Enabled'

                    # set default value if empty string
                    barcode = 'Unassigned' if barcode == '' else barcode
                    expire_dt = '9999-12-31' if expire_dt == '' else expire_dt
                    item_type = 'Unassigned' if item_type == '' else item_type
                    inventory_status = 'Disabled' if available_stock == 0 else inventory_status

                    if '' in (item_name, brand, sales_group, supplier, cost, sell_price):
                        QMessageBox.critical(self, 'Error', f'Unable to import {csv_file_name} due to missing values.')
                        print('Failed to import')
                        return

                    else:
                        self.product_management_schema.addNewProduct(
                            barcode=barcode,
                            item_name=item_name,
                            expire_dt=expire_dt,
                            item_type=item_type,
                            brand=brand,
                            sales_group=sales_group,
                            supplier=supplier,
                            cost=cost,
                            sell_price=sell_price,
                            effective_dt=effective_dt,
                            inventory_status=inventory_status,
                            available_stock=available_stock
                        )

                    progress_min_range += 1
                    progress_dialog.setLabelText(f'Importing data from {csv_file_name}: ({progress_min_range} out of {total_rows})')
                    os.system('cls')
                    print(f'Imported data: {progress_min_range} out of {total_rows}')
                    progress_dialog.setValue(progress_min_range)

                    # Process events to keep the UI responsive
                    QCoreApplication.processEvents()

                    # Check if the cancel button was pressed
                    if progress_dialog.wasCanceled():
                        QMessageBox.warning(self, 'Canceled', 'Import process was canceled.')
                        self.refreshUI()
                        return  # Terminate the import process

                QMessageBox.information(self, 'Success', f"All data from '{csv_file_name}' has been imported.")
                self.refreshUI()
                print('Successfully imported.')

            except Exception as error_message:
                QMessageBox.critical(self, 'Error', f'Error importing data from {csv_file_name}: {str(error_message)}')

        if self.panel_d.isVisible() == True:
            self.onPushButtonClicked(reference='add')

    # -- save new data
    def saveNewData(self):
        if '' in (
            self.item_name_field.currentText(),
            self.brand_field.currentText(),
            self.sales_group_field.currentText(),
            self.supplier_field.currentText(),
            self.cost_field.text(),
            self.sell_price_field.text()
        ):
            QMessageBox.critical(self, 'Invalid', "All required fields must be filled.")
            return
        else:
            if False in (
                self.cost_field.text().isnumeric(),
                self.sell_price_field.text().isnumeric()
            ):
                print('went here')
                print('not numeric')
                QMessageBox.critical(self, 'Invalid', "Invalid numerical input.")
                return
            
            barcode = self.barcode_field.text()
            item_name = self.item_name_field.currentText()
            expire_dt = self.expire_dt_field.date().toString(Qt.DateFormat.ISODate)
            item_type = self.item_type_field.currentText()
            brand = self.brand_field.currentText()
            sales_group = self.sales_group_field.currentText()
            supplier = self.supplier_field.currentText()
            cost = self.cost_field.text()
            sell_price = self.sell_price_field.text()
            promo_name = self.promo_name_field.currentText()
            promo_type = self.promo_type_field.text()
            discount_percent = self.discount_percent_field.text()
            discount_value = self.discount_value_field.text()
            new_sell_price = self.new_sell_price_field.text()
            start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
            end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)
            effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)
            inventory_status = self.inventory_status_field.currentText()
            available_stock = self.available_stock_field.text()
            on_hand_stock = self.on_hand_stock_field.text()

            # assign default values to optional field
            barcode = 'Unassigned' if barcode == '' else barcode
            item_type = 'Unassigned' if item_type == '' else item_type
            promo_type = 'Unassigned' if promo_type == '' else promo_type

            if promo_name != 'No promo':
                promo_type = self.promo_type_field.text()
                discount_percent = self.discount_percent_field.text()
                discount_value = self.discount_value_field.text()
                new_sell_price = self.new_sell_price_field.text()
                start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
                end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)
            

            if inventory_status == 'Enabled':
                available_stock = self.available_stock_field.text()
                on_hand_stock = self.on_hand_stock_field.text()

            self.product_management_schema.addNewProduct(
                barcode=barcode,
                item_name=item_name,
                expire_dt=expire_dt,
                item_type=item_type,
                brand=brand,
                sales_group=sales_group,
                supplier=supplier,
                cost=cost,
                sell_price=sell_price,
                promo_name=promo_name,
                # stored if promo name != 'No promo'
                promo_type=promo_type,
                discount_percent=discount_percent,
                discount_value=discount_value,
                new_sell_price=new_sell_price,
                start_dt=start_dt,
                end_dt=end_dt,
                effective_dt=effective_dt,
                inventory_status=inventory_status,
                # stored if inventory status == 'Enbaled'
                available_stock=available_stock,
                on_hand_stock=on_hand_stock
            )
            
            if self.panel_d.isVisible() == True:
                self.onPushButtonClicked(reference='add')

            self.refreshUI()

            QMessageBox.information(self, 'Success', f"New promo has been added.")

        print('New data has been added.')

    def saveEditData(self):
        if '' in (
            self.item_name_field.currentText(),
            self.cost_field.text(),
            self.sell_price_field.text()
        ):
            QMessageBox.critical(self, 'Invalid', "All required fields must be filled.")
            return
        else:
            if False in (
                self.cost_field.text().isnumeric(),
                self.sell_price_field.text().isnumeric()
            ):
                print('went here')
                print('not numeric')
                QMessageBox.critical(self, 'Invalid', "Invalid numerical input.")
                return
            
            barcode = self.barcode_field.text()
            item_name = self.item_name_field.currentText()
            expire_dt = self.expire_dt_field.date().toString(Qt.DateFormat.ISODate)

            item_type = self.current_item_type_field.text()
            brand = self.current_brand_field.text()
            sales_group = self.current_sales_group_field.text()
            supplier = self.current_supplier_field.text()

            cost = self.cost_field.text()
            sell_price = self.sell_price_field.text()
            promo_name = self.promo_name_field.currentText()
            promo_type = self.promo_type_field.text()
            discount_percent = self.discount_percent_field.text()
            discount_value = self.discount_value_field.text()
            new_sell_price = self.new_sell_price_field.text()
            start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
            end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)
            effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)

            

            if promo_name != 'No promo':
                promo_type = self.promo_type_field.text()
                discount_percent = self.discount_percent_field.text()
                discount_value = self.discount_value_field.text()
                new_sell_price = self.new_sell_price_field.text()
                start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
                end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)

            # assign default values to optional field
            barcode = 'Unassigned' if barcode == '' else barcode
            item_type = 'Unassigned' if item_type == '' else item_type

            self.product_management_schema.editSelectedProduct(
                barcode=barcode,
                item_name=item_name,
                expire_dt=expire_dt,
                item_type=item_type,
                brand=brand,
                sales_group=sales_group,
                supplier=supplier,
                cost=cost,
                sell_price=sell_price,
                promo_name=promo_name,
                promo_type=promo_type,
                discount_percent=discount_percent,
                discount_value=discount_value,
                new_sell_price=new_sell_price,
                start_dt=start_dt,
                end_dt=end_dt,
                effective_dt=effective_dt,
                item_id=self.item_id,
                item_price_id=self.item_price_id,
                promo_id=self.promo_id
            )
            
            if self.panel_d.isVisible() == True:
                self.onPushButtonClicked(reference='add')

            self.refreshUI()

            QMessageBox.information(self, 'Success', f"New promo has been added.")

        print('New data has been added.')

    def deleteData(self, row_value):
        item_name = f'{row_value[1]}'
        item_price_id = f'{row_value[17]}'

        confirmation = QMessageBox.warning(self, 'Delete', f'Are you sure you want to delete {item_name}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes:
            self.product_management_schema.deleteSelectedProduct(item_price_id)
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
        if reference == 'add':
            self.label_item_type.show()
            self.label_brand.show()
            self.label_sales_group.show()
            self.label_supplier.show()

            self.item_type_field.show()
            self.brand_field.show()
            self.sales_group_field.show()
            self.supplier_field.show()

            self.label_current_item_type.hide()
            self.label_current_brand.hide()
            self.label_current_sales_group.hide()
            self.label_current_supplier.hide()

            self.current_item_type_field.hide()
            self.current_brand_field.hide()
            self.current_sales_group_field.hide()
            self.current_supplier_field.hide()

        if reference == 'edit':
            self.label_item_type.hide()
            self.label_brand.hide()
            self.label_sales_group.hide()
            self.label_supplier.hide()
            self.label_inventory_status.hide()
            self.item_type_field.hide()
            self.brand_field.hide()
            self.sales_group_field.hide()
            self.supplier_field.hide()
            self.inventory_status_field.hide()

            self.label_current_item_type.show()
            self.label_current_brand.show()
            self.label_current_sales_group.show()
            self.label_current_supplier.show()
            self.label_current_inventory_status.show()
            self.current_item_type_field.show()
            self.current_brand_field.show()
            self.current_sales_group_field.show()
            self.current_supplier_field.show()
            self.current_inventory_status_field.show()

            # default
            self.barcode_field.setText(f'{row_value[0]}')
            self.item_name_field.setCurrentText(f'{row_value[1]}')
            self.expire_dt_field.setDate(QDate.fromString(row_value[2], Qt.DateFormat.ISODate))
            self.cost_field.setText(f'{row_value[7]}')
            self.sell_price_field.setText(f'{row_value[8]}')
            self.promo_name_field.setCurrentText(f'{row_value[11]}')
            self.effective_dt_field.setDate(QDate.fromString(row_value[10], Qt.DateFormat.ISODate))
            self.item_id = row_value[16]
            self.item_price_id = row_value[17]
            self.promo_id = row_value[18]

            # current
            self.current_barcode_field.setText(f'{row_value[0]}')
            self.current_item_name_field.setText(f'{row_value[1]}')
            self.current_expire_dt_field.setText(f'{row_value[2]}')
            self.current_item_type_field.setText(f'{row_value[3]}')
            self.current_brand_field.setText(f'{row_value[4]}')
            self.current_sales_group_field.setText(f'{row_value[5]}')
            self.current_supplier_field.setText(f'{row_value[6]}')
            self.current_cost_field.setText(f'{row_value[7]}')
            self.current_sell_price_field.setText(f'{row_value[8]}')
            self.current_promo_name_field.setText(f'{row_value[11]}')
            self.current_effective_dt_field.setText(f'{row_value[10]}')
            self.current_inventory_status_field.setText(f'{row_value[12]}')
            
            if self.promo_id == 0:
                # # hide default
                self.label_barcode.show()
                self.label_item_name.show()
                self.label_expire_dt.show()
                self.label_cost.show()
                self.label_sell_price.show()
                self.label_promo_name.show()

                self.barcode_field.show()
                self.item_name_field.show()
                self.expire_dt_field.show()
                self.cost_field.show()
                self.sell_price_field.show()
                self.promo_name_field.show()
                
                # current
                self.label_current_barcode.hide()
                self.label_current_item_name.hide()
                self.label_current_expire_dt.hide()
                self.label_current_cost.hide()
                self.label_current_sell_price.hide()
                self.label_current_promo_name.hide()
                self.label_current_promo_type.hide()
                self.label_current_discount_percent.hide()
                self.label_current_discount_value.hide()
                self.label_current_new_sell_price.hide()

                self.current_barcode_field.hide()
                self.current_item_name_field.hide()
                self.current_expire_dt_field.hide()
                self.current_cost_field.hide()
                self.current_sell_price_field.hide()
                self.current_promo_name_field.hide()
                self.current_promo_type_field.hide()
                self.current_discount_percent_field.hide()
                self.current_discount_value_field.hide()
                self.current_new_sell_price_field.hide()

            else:
                # # show current
                self.label_barcode.hide()
                self.label_item_name.hide()
                self.label_expire_dt.hide()
                self.label_item_type.hide()
                self.label_brand.hide()
                self.label_sales_group.hide()
                self.label_supplier.hide()
                self.label_cost.hide()
                self.label_sell_price.hide()
                self.label_promo_name.hide()
                self.label_promo_type.hide()
                self.label_discount_percent.hide()
                self.label_discount_value.hide()
                self.label_new_sell_price.hide()
                self.label_start_dt.hide()
                self.label_end_dt.hide()

                self.barcode_field.hide()
                self.item_name_field.hide()
                self.expire_dt_field.hide()
                self.item_type_field.hide()
                self.brand_field.hide()
                self.sales_group_field.hide()
                self.supplier_field.hide()
                self.cost_field.hide()
                self.sell_price_field.hide()
                self.promo_name_field.hide()
                self.promo_type_field.hide()
                self.discount_percent_field.hide()
                self.discount_value_field.hide()
                self.new_sell_price_field.hide()
                self.start_dt_field.hide()
                self.end_dt_field.hide()


                # current
                self.label_current_barcode.show()
                self.label_current_item_name.show()
                self.label_current_expire_dt.show()
                self.label_current_cost.show()
                self.label_current_promo_name.show()
                self.label_current_promo_type.show()
                self.label_current_discount_percent.show()
                self.label_current_discount_value.show()
                self.label_current_new_sell_price.show()
                self.label_current_effective_dt.show()

                self.current_barcode_field.show()
                self.current_item_name_field.show()
                self.current_expire_dt_field.show()
                self.current_cost_field.show()
                self.current_promo_name_field.show()
                self.current_promo_type_field.show()
                self.current_discount_percent_field.show()
                self.current_discount_value_field.show()
                self.current_new_sell_price_field.show()
                self.current_effective_dt_field.show()

            print('this promo id', self.promo_id)
                
        print('Panel D has been updated.')

    def onPushButtonClicked(
        self,
        reference='',
        show_panel=True,
        row_edit_button='',
        row_value=''
    ):

        if reference == 'refresh':
            self.refreshUI()

        elif reference == 'import':
            self.importData()
        
        elif reference == 'add':
            self.panel_d.show() if show_panel == True else self.panel_d.hide()
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
            self.panel_d.hide() if show_panel == False else self.panel_d.show()
            # Re-enable the previously disabled edit button (if any)
            if self.current_edit_button:
                self.current_edit_button.setDisabled(False)
            
            # Reset the current_edit_button to None
            self.current_edit_button = None
            self.add_button.setDisabled(False)
        
        elif reference == 'edit':
            self.panel_d.show() if show_panel == True else self.panel_d.hide()
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

    def onLineEditTextChanged(self, reference='', text=''
    ):
        if text == '':
            self.promo_name_field.setDisabled(True)

        else:
            self.promo_name_field.setDisabled(False)

            promo_data = self.product_management_schema.getPromoTypeAndDiscountPercent(self.promo_name_field.currentText())
            
            for row in promo_data:
                self.promo_type_field.setText(f'{row[0]}')
                self.discount_percent_field.setText(f'{row[1]}')
                self.current_promo_type_field.setText(f'{row[0]}')
                self.current_discount_percent_field.setText(f'{row[1]}')

            try:
                float(self.sell_price_field.text())
                float(self.discount_percent_field.text())

                old_sell_price = float(self.sell_price_field.text())
                discount_amount = old_sell_price * (float(self.discount_percent_field.text()) / 100)
                
                new_sell_price = float(self.sell_price_field.text()) - discount_amount

                self.discount_value_field.setText(f'{discount_amount:.2f}')
                self.new_sell_price_field.setText(f'{new_sell_price:.2f}')
                self.current_discount_value_field.setText(f'{discount_amount:.2f}')
                self.current_new_sell_price_field.setText(f'{new_sell_price:.2f}')
                pass

            except ValueError:
                pass
        
    def onComboBoxCurrentTextChanged(self, reference='', text=''
    ):
        if text == 'No promo':
            self.label_promo_type.hide()
            self.label_discount_percent.hide()
            self.label_discount_value.hide()
            self.label_new_sell_price.hide()
            self.label_start_dt.hide()
            self.label_end_dt.hide()
            self.label_effective_dt.show()

            self.promo_type_field.hide()
            self.discount_percent_field.hide()
            self.discount_value_field.hide()
            self.new_sell_price_field.hide()
            self.start_dt_field.hide()
            self.end_dt_field.hide()
            self.effective_dt_field.show()
            
        else:
            self.label_promo_type.show()
            self.label_discount_percent.show()
            self.label_discount_value.show()
            self.label_new_sell_price.show()
            self.label_start_dt.show()
            self.label_end_dt.show()
            self.label_effective_dt.hide()

            self.promo_type_field.show()
            self.discount_percent_field.show()
            self.discount_value_field.show()
            self.new_sell_price_field.show()
            self.start_dt_field.show()
            self.end_dt_field.show()
            self.effective_dt_field.hide()

            promo_data = self.product_management_schema.getPromoTypeAndDiscountPercent(self.promo_name_field.currentText())
            for row in promo_data:
                self.promo_type_field.setText(f'{row[0]}')
                self.discount_percent_field.setText(f'{row[1]}')

            try:
                float(self.sell_price_field.text())
                float(self.discount_percent_field.text())

                old_sell_price = float(self.sell_price_field.text())
                discount_amount = old_sell_price * (float(self.discount_percent_field.text()) / 100)
                
                new_sell_price = float(self.sell_price_field.text()) - discount_amount

                self.discount_value_field.setText(f'{discount_amount:.2f}')
                self.new_sell_price_field.setText(f'{new_sell_price:.2f}')
                pass
            except ValueError:
                pass

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

                self.cost_cell = QTableWidgetItem(f'₱{row_value[7]}')
                self.sell_price_cell = QTableWidgetItem(f'₱{row_value[8]}')
                self.discount_value_cell = QTableWidgetItem(f'₱{row_value[9]}')

                self.cost_cell.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.sell_price_cell.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.discount_value_cell.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

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

                if row_value[11] != 'No promo':
                    self.cell_value.setForeground(QColor(255,0,255))
                    self.cost_cell.setForeground(QColor(255,0,255))
                    self.sell_price_cell.setForeground(QColor(255,0,255))
                    self.discount_value_cell.setForeground(QColor(255,0,255))

                self.list_table.setCellWidget(row_index, 0, self.edit_button)
                self.list_table.setCellWidget(row_index, 1, self.delete_button)
                self.list_table.setItem(row_index, col_index + 2, self.cell_value)
                self.list_table.setItem(row_index, 9, self.cost_cell)
                self.list_table.setItem(row_index, 10, self.sell_price_cell)
                self.list_table.setItem(row_index, 11, self.discount_value_cell)
                

        print('Table has been populated.')
        

# -- layouts
    def showPanelD(self):
        self.panel_d = CustomGroupBox(reference='panel_d_box')
        form_layout = QFormLayout()

        required_indicator = "<font color='red'><b>!</b></font>"

        self.back_button = CustomPushButton(reference='back_button', text='BACK')
        self.back_button.clicked.connect(lambda: self.onPushButtonClicked(reference='back', show_panel=False))
        
        self.barcode_field = CustomLineEdit(reference='barcode_field')
        self.item_name_field = CustomComboBox(reference='item_name_field')
        self.expire_dt_field = CustomDateEdit(reference='expire_dt_field')
        self.item_type_field = CustomComboBox(reference='item_type_field')
        self.brand_field = CustomComboBox(reference='brand_field')
        self.sales_group_field = CustomComboBox(reference='sales_group_field')
        self.supplier_field = CustomComboBox(reference='supplier_field')
        self.cost_field = CustomLineEdit(reference='cost_field')
        self.sell_price_field = CustomLineEdit(reference='sell_price_field')
        self.sell_price_field.textChanged.connect(lambda text: self.onLineEditTextChanged(text=text))
        self.promo_name_field = CustomComboBox(reference='promo_name_field')
        self.promo_name_field.currentTextChanged.connect(lambda text: self.onComboBoxCurrentTextChanged(text=text))
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
        self.label_item_name = CustomLabel(reference='label_item_name', text=f'{required_indicator} item_name')
        self.label_expire_dt = CustomLabel(reference='label_expire_dt', text='expire_dt')
        self.label_item_type = CustomLabel(reference='label_item_type', text=f'{required_indicator} item_type')
        self.label_brand = CustomLabel(reference='label_brand', text=f'{required_indicator} brand')
        self.label_sales_group = CustomLabel(reference='label_sales_group', text=f'{required_indicator} sales_group')
        self.label_supplier = CustomLabel(reference='label_supplier', text=f'{required_indicator} supplier')
        self.label_cost = CustomLabel(reference='label_cost', text=f'{required_indicator} cost')
        self.label_sell_price = CustomLabel(reference='label_sell_price', text=f'{required_indicator} sell_price')
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
        self.current_promo_name_field.textChanged.connect(lambda text: self.onLineEditTextChanged(text=text))
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
        self.add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='add', show_panel=True))

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
