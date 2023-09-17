import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from other.csv_importer import *    
from schema.sales_table_schema import *
from schema.product_management_schema import *
from widget.product_management_widget import *

class ProductManagementLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.product_management_schema = ProductManagementSchema()
        # for temporary use --
        self.sales_table_schema = SalesTableSchema()
        self.sales_table_schema.setup_sales_table()
        # --
        self.current_page = 1
        self.createLayout()
        self.refresh_data()

# under construction...
    def import_data(self):
        self.import_button.setDisabled(True)

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

                for row in df.itertuples(index=False):
                    barcode, item_name, expire_dt, item_type, brand, sales_group, supplier, cost, sell_price, available_stock = row[:10]
                    effective_dt = date.today()
                    inventory_tracking = 'Disabled'
                    print('this is available_stock: ', available_stock)

                    # set default value if empty string
                    barcode = '<unknown>' if barcode == '' else barcode
                    expire_dt = '9999-12-31' if expire_dt == '' else expire_dt
                    item_type = '<unknown>' if item_type == '' else item_type

                    if available_stock == '0' or available_stock == '' or available_stock == None:
                        inventory_tracking = 'Disabled'
                    else: 
                        inventory_tracking = 'Enabled' 
                    
                    print('this is inventory tracking: ', inventory_tracking)

                    if '' in (item_name, brand, sales_group, supplier, cost, sell_price):
                        QMessageBox.critical(self, 'Error', f'Unable to import {csv_file_name} due to missing values.')
                        self.import_button.setDisabled(False)
                        return

                    else:
                        # print('Inventory tracking: ', inventory_tracking)
                        self.product_management_schema.add_new_product(
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
                            inventory_tracking=inventory_tracking,
                            available_stock=available_stock
                        )

                    progress_min_range += 1
                    current_row = progress_min_range - 1
                    progress_dialog.setLabelText(f'Importing data from {csv_file_name}: ({current_row} out of {total_rows})')
                    progress_dialog.setValue(progress_min_range)
                    print(f'Imported data: {progress_min_range} out of {total_rows}')
                    print('\n')

                    # Process events to keep the UI responsive
                    QCoreApplication.processEvents()

                    # Check if the cancel button was pressed
                    if progress_dialog.wasCanceled():
                        QMessageBox.warning(self, 'Canceled', 'Import process was canceled.')
                        self.import_button.setDisabled(False)
                        return  # Terminate the import process

                QMessageBox.information(self, 'Success', f"All data from '{csv_file_name}' has been imported.")
                self.import_button.setDisabled(False)
                print('Successfully imported.')

            except Exception as error_message:
                QMessageBox.critical(self, 'Error', f'Error importing data from {csv_file_name}: {str(error_message)}')

        # if self.panel_d.isVisible() == True:
        #     self.onPushButtonClicked(reference='add')
# under construction...
    def refresh_data(self):
        self.total_product = self.product_management_schema.count_total_product()
        self.populate_table_widget()

        print('UI has been refreshed.')

    def save_data(self, clicked_ref):
        if clicked_ref == 'save_new_data':
            if '' in (
                self.item_name_field.text(),
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
                    QMessageBox.critical(self, 'Invalid', "Invalid numerical input.")
                    return
                
                barcode = self.barcode_field.text()
                item_name = self.item_name_field.text()
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
                inventory_tracking = self.inventory_tracking_field.currentText()
                available_stock = self.available_stock_field.text()
                on_hand_stock = self.on_hand_stock_field.text()

                # assign default values to optional field
                barcode = 'Unassigned' if barcode == '' else barcode
                item_type = 'Unassigned' if item_type == '' else item_type

                if promo_name != 'No promo':
                    promo_type = self.promo_type_field.text()
                    discount_percent = self.discount_percent_field.text()
                    discount_value = self.discount_value_field.text()
                    new_sell_price = self.new_sell_price_field.text()
                    start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
                    end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)

                if inventory_tracking == 'Enabled':
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
                    inventory_tracking=inventory_tracking,
                    # stored if inventory status == 'Enbaled'
                    available_stock=available_stock,
                    on_hand_stock=on_hand_stock
                )
                
                if self.panel_d.isVisible() == True:
                    self.onPushButtonClicked(reference='add')

                self.refreshUI()

                QMessageBox.information(self, 'Success', f"New promo has been added.")

            print('testing')
            pass
        
        elif clicked_ref == 'save_edit_data':
            if '' in (
                self.item_name_field.text(),
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
                item_name = self.item_name_field.text()
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

    def edit_data(self, clicked_ref=''):
        pass
    def view_data(self, clicked_ref=''):
        pass
    def delete_data(self, clicked_ref=''):
        if clicked_ref == 'delete_all_data':
            # First confirmation
            confirm_delete_a = QMessageBox.warning(self, 'Confirm', 'Are you sure you want to delete all product?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm_delete_a == QMessageBox.StandardButton.Yes:

                # Second confirmation
                confirm_delete_b = QMessageBox.warning(
                    self, 'Confirm', """
                    <p>Do you want to proceed?</p>
                    <p>Proceeding will delete all product and will not be recovered.</p>
                    """, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if confirm_delete_b == QMessageBox.StandardButton.Yes:
                    while True:
                        # Custom input dialog for final confirmation
                        confirm_delete_c, ok = QInputDialog.getText(self, 'Confirm', "Type <b>'delete all'</b> to confirm")
                        if ok:
                            if confirm_delete_c == 'delete all':
                                # Delete all data
                                self.product_management_schema.delete_all_data()
                                QMessageBox.information(self, "Deleted", "All data has been deleted.")
                                break  # Exit the loop on successful input
                            else:
                                QMessageBox.critical(self, "Error", "Invalid input. Try again.")
                        else:
                            print('Deletion canceled')
                            break  # Exit the loop if input is canceled
                else:
                    print('Deletion canceled')
            elif confirm_delete_a == QMessageBox.StandardButton.No:
                print('Deletion canceled')

    def previous_data(self):
        print(self.current_page)
        if self.current_page > 1:
            self.current_page -= 1
        self.overview_data_page_number.setText(f'Page {self.current_page}')
        self.item_data_page_number.setText(f'Page {self.current_page}')
        self.category_data_page_number.setText(f'Page {self.current_page}')
        self.item_price_data_page_number.setText(f'Page {self.current_page}')
        self.inventory_data_page_number.setText(f'Page {self.current_page}')
        self.populate_table_widget(current_page=self.current_page)
        print('pressed previous')
        pass
    def next_data(self):
        self.current_page += 1
        print(self.current_page)
        self.overview_data_page_number.setText(f'Page {self.current_page}')
        self.item_data_page_number.setText(f'Page {self.current_page}')
        self.category_data_page_number.setText(f'Page {self.current_page}')
        self.item_price_data_page_number.setText(f'Page {self.current_page}')
        self.inventory_data_page_number.setText(f'Page {self.current_page}')
        self.populate_table_widget(current_page=self.current_page)
        print('pressed next')

    def on_push_button_clicked(self, clicked_ref=''):
        if clicked_ref == 'delete_all_data' or clicked_ref == 'import_data' or clicked_ref == 'add_data' or clicked_ref == 'refresh_data':
            if clicked_ref == 'import_data':
                self.import_data()
                pass
            elif clicked_ref == 'add_data':
                pass
            elif clicked_ref == 'delete_all_data':
                self.delete_data(clicked_ref)
                pass
        elif clicked_ref == 'edit_data' or clicked_ref == 'view_data' or clicked_ref == 'delete_data':
            if clicked_ref == 'edit_data':
                pass
            elif clicked_ref == 'view_data':
                pass
            elif clicked_ref == 'delete_data':
                pass
        elif clicked_ref == 'save_new_data' or clicked_ref == 'save_edit_data':
            if clicked_ref == 'save_new_data':
                self.save_data(clicked_ref)
                pass
            elif clicked_ref == 'save_edit_data':
                self.save_data(clicked_ref)
                pass
        elif clicked_ref == 'previous_data' or clicked_ref == 'next_data':
            if clicked_ref == 'previous_data':
                self.previous_data()
                pass
            elif clicked_ref == 'next_data':
                self.next_data()
                pass

    def on_line_edit_text_changed(self, text_changed_ref='', text=''):
        if text == '':
            self.promo_name_field.setDisabled(True)
        else:
            self.promo_name_field.setDisabled(False)

    def on_combo_box_current_text_changed(self, current_text_changed_ref='', currentText=''):
        if current_text_changed_ref == 'promo_name_field':
            if currentText == 'No promo':
                self.effective_dt_label.show()
                self.effective_dt_field.show()

                self.promo_type_label.hide()
                self.promo_type_field.hide()
                self.discount_percent_label.hide()
                self.discount_percent_field.hide()
                self.discount_value_label.hide()
                self.discount_value_field.hide()
                self.new_sell_price_label.hide()
                self.new_sell_price_field.hide()
                self.start_dt_label.hide()
                self.start_dt_field.hide()
                self.end_dt_label.hide()
                self.end_dt_field.hide()
            else:
                self.effective_dt_label.hide()
                self.effective_dt_field.hide()

                self.promo_type_label.show()
                self.promo_type_field.show()
                self.discount_percent_label.show()
                self.discount_percent_field.show()
                self.discount_value_label.show()
                self.discount_value_field.show()
                self.new_sell_price_label.show()
                self.new_sell_price_field.show()
                self.start_dt_label.show()
                self.start_dt_field.show()
                self.end_dt_label.show()
                self.end_dt_field.show()
                pass

        elif current_text_changed_ref == 'inventory_tracking_field':
            if currentText == 'Disabled':
                self.available_stock_label.hide()
                self.available_stock_field.hide()
                self.on_hand_stock_label.hide()
                self.on_hand_stock_field.hide()
            elif currentText == 'Enabled':
                self.available_stock_label.show()
                self.available_stock_field.show()
                self.on_hand_stock_label.show()      
                self.on_hand_stock_field.show()


    def update_panel_b(self):
        pass

    def populate_table_widget(self, current_page=1):
        data = self.product_management_schema.list_product(page_number=current_page)
        tables = [
            self.overview_data_list,
            self.item_data_list,
            self.category_data_list,
            self.item_price_data_list,
            self.inventory_data_list,
        ]
        buttons = [
            self.overview_data_previous_button,
            self.overview_data_next_button,
            self.item_data_previous_button,
            self.item_data_next_button,
            self.category_data_previous_button,
            self.category_data_next_button,
            self.item_price_data_previous_button,
            self.item_price_data_next_button,
            self.inventory_data_previous_button,
            self.inventory_data_next_button,
        ]

        for table in tables:
            table.setRowCount(len(data))

        for row_index, row_value in enumerate(data):
            for table in tables:
                modify_box = CustomWidget(ref='modify_box')
                modify_box_layout = CustomGridLayout(ref='modify_box_layout')
                view_button = CustomPushButton(text='View')
                edit_button = CustomPushButton(text='Edit')
                delete_button = CustomPushButton(text='Delete')
                modify_box_layout.addWidget(view_button, 0, 0)
                modify_box_layout.addWidget(edit_button, 0, 1)
                modify_box_layout.addWidget(delete_button, 0, 2)
                modify_box.setLayout(modify_box_layout)

                if table is self.overview_data_list:
                    item_name = QTableWidgetItem(f'{row_value[1]}')
                    brand = QTableWidgetItem(f'{row_value[4]}')
                    sales_group = QTableWidgetItem(f'{row_value[5]}')
                    sell_price = QTableWidgetItem(f'{row_value[8]}')
                    promo_name = QTableWidgetItem(f'{row_value[10]}')
                    inventory_tracking = QTableWidgetItem(f'{row_value[12]}')
                    update_ts = QTableWidgetItem(f'{row_value[15]}')
                    table.setCellWidget(row_index, 0, modify_box)
                    table.setItem(row_index, 1, item_name)
                    table.setItem(row_index, 2, brand)
                    table.setItem(row_index, 3, sales_group)
                    table.setItem(row_index, 4, sell_price)
                    table.setItem(row_index, 5, promo_name)
                    table.setItem(row_index, 6, inventory_tracking)
                    table.setItem(row_index, 7, update_ts)
                elif table is self.item_data_list:
                    barcode = QTableWidgetItem(f'{row_value[0]}')
                    item_data = QTableWidgetItem(f'{row_value[1]}')
                    expire_dt = QTableWidgetItem(f'{row_value[2]}')
                    promo_name = QTableWidgetItem(f'{row_value[10]}')
                    update_ts = QTableWidgetItem(f'{row_value[15]}')
                    table.setCellWidget(row_index, 0, modify_box)
                    table.setItem(row_index, 1, barcode)
                    table.setItem(row_index, 2, item_data)
                    table.setItem(row_index, 3, expire_dt)
                    table.setItem(row_index, 4, promo_name)
                    table.setItem(row_index, 5, update_ts)
                elif table is self.category_data_list:
                    item_name = QTableWidgetItem(f'{row_value[1]}')
                    item_type = QTableWidgetItem(f'{row_value[3]}')
                    brand = QTableWidgetItem(f'{row_value[4]}')
                    sales_group = QTableWidgetItem(f'{row_value[5]}')
                    supplier = QTableWidgetItem(f'{row_value[6]}')
                    promo_name = QTableWidgetItem(f'{row_value[10]}')
                    update_ts = QTableWidgetItem(f'{row_value[15]}')
                    table.setCellWidget(row_index, 0, modify_box)
                    table.setItem(row_index, 1, item_name)
                    table.setItem(row_index, 2, item_type)
                    table.setItem(row_index, 3, brand)
                    table.setItem(row_index, 4, sales_group)
                    table.setItem(row_index, 5, supplier)
                    table.setItem(row_index, 6, promo_name)
                    table.setItem(row_index, 7, update_ts)
                elif table is self.item_price_data_list:
                    item_name = QTableWidgetItem(f'{row_value[1]}')
                    cost = QTableWidgetItem(f'₱{row_value[7]}')
                    sell_price = QTableWidgetItem(f'₱{row_value[8]}')
                    discount_value = QTableWidgetItem(f'₱{row_value[11]}')
                    promo_name = QTableWidgetItem(f'{row_value[10]}')
                    update_ts = QTableWidgetItem(f'{row_value[15]}')
                    table.setCellWidget(row_index, 0, modify_box)
                    table.setItem(row_index, 1, item_name)
                    table.setItem(row_index, 2, cost)
                    table.setItem(row_index, 3, sell_price)
                    table.setItem(row_index, 4, discount_value)
                    table.setItem(row_index, 5, promo_name)
                    table.setItem(row_index, 6, update_ts)
                elif table is self.inventory_data_list:
                    item_name = QTableWidgetItem(f'{row_value[1]}')
                    inventory_tracking = QTableWidgetItem(f'{row_value[12]}')
                    available = QTableWidgetItem(f'{row_value[13]}')
                    on_hand = QTableWidgetItem(f'{row_value[14]}')
                    promo_name = QTableWidgetItem(f'{row_value[10]}')
                    update_ts = QTableWidgetItem(f'{row_value[15]}')
                    table.setCellWidget(row_index, 0, modify_box)
                    table.setItem(row_index, 1, item_name)
                    table.setItem(row_index, 2, inventory_tracking)
                    table.setItem(row_index, 3, available)
                    table.setItem(row_index, 4, on_hand)
                    table.setItem(row_index, 5, promo_name)
                    table.setItem(row_index, 6, update_ts)


    def show_panel_b(self):
        self.panel_b = CustomGroupBox(ref='panel_b')
        form_layout = QFormLayout()

        self.back_button = CustomPushButton(text='Back')

        # can be changed from here..
        # ---- primary information
        self.barcode_label = CustomLabel(text='barcode')
        self.item_name_label = CustomLabel(text='item_name')
        self.expire_dt_label = CustomLabel(text='expire_dt')
        # ---- category
        self.item_type_label = CustomLabel(text='item_type')
        self.brand_label = CustomLabel(text='brand')
        self.sales_group_label = CustomLabel(text='sales_group')
        self.supplier_label = CustomLabel(text='supplier')
        # ---- price
        self.cost_label = CustomLabel(text='cost')
        self.sell_price_label = CustomLabel(text='sell_price')
        self.effective_dt_label = CustomLabel(text='effective_dt')
        self.promo_name_label = CustomLabel(text='promo_name')
        self.promo_type_label = CustomLabel(ref='promo_active', text='promo_type')
        self.discount_percent_label = CustomLabel(ref='promo_active', text='discount_percent')
        self.discount_value_label = CustomLabel(ref='promo_active', text='discount_value')
        self.new_sell_price_label = CustomLabel(ref='promo_active', text='new_sell_price')
        self.start_dt_label = CustomLabel(ref='promo_active', text='start_dt')
        self.end_dt_label = CustomLabel(ref='promo_active', text='end_dt')
        # ---- inventory
        self.inventory_tracking_label = CustomLabel(text='inventory_tracking')
        self.available_stock_label = CustomLabel(ref='inventory_tracking_active', text='available_stock')
        self.on_hand_stock_label = CustomLabel(ref='inventory_tracking_active', text='on_hand_stock')
        # ..until here.

        # can be changed from here..
        # ---- primary information
        self.barcode_field = CustomLineEdit()
        self.item_name_field = CustomLineEdit()
        self.expire_dt_field = CustomDateEdit()
        # ---- category
        self.item_type_field = CustomComboBox(editable=True)
        self.brand_field = CustomComboBox(editable=True)
        self.sales_group_field = CustomComboBox(ref='sales_group')
        self.supplier_field = CustomComboBox(editable=True)
        # ---- price
        self.cost_field = CustomLineEdit()
        self.sell_price_field = CustomLineEdit()
        self.sell_price_field.textChanged.connect(lambda text: self.on_line_edit_text_changed(text=text))
        self.effective_dt_field = CustomDateEdit()
        self.promo_name_field = CustomComboBox(ref='promo_name', editable=True, disabled=True)
        self.promo_name_field.currentTextChanged.connect(lambda currentText: self.on_combo_box_current_text_changed(current_text_changed_ref='promo_name_field', currentText=currentText))
        self.promo_type_field = CustomLineEdit(ref='promo_active')
        self.discount_percent_field = CustomLineEdit(ref='promo_active')
        self.discount_value_field = CustomLineEdit(ref='promo_active')
        self.new_sell_price_field = CustomLineEdit(ref='promo_active')
        self.start_dt_field = CustomDateEdit(ref='promo_active')
        self.end_dt_field = CustomDateEdit(ref='promo_active')
        # ---- inventory
        self.inventory_tracking_field = CustomComboBox(ref='inventory_tracking')
        self.inventory_tracking_field.currentTextChanged.connect(lambda currentText: self.on_combo_box_current_text_changed(current_text_changed_ref='inventory_tracking_field', currentText=currentText))
        self.available_stock_field = CustomLineEdit(ref='inventory_tracking_active')
        self.on_hand_stock_field = CustomLineEdit(ref='inventory_tracking_active')
        # ..until here.

        # can be changed from here..
        # ---- current primary information
        self.current_barcode_label = CustomLabel(ref='inactive_display', text='current_barcode')
        self.current_item_name_label = CustomLabel(ref='inactive_display', text='current_item_name')
        self.current_expire_dt_label = CustomLabel(ref='inactive_display', text='current_expire_dt')
        # ---- current category
        self.current_item_type_label = CustomLabel(ref='inactive_display', text='current_item_type')
        self.current_brand_label = CustomLabel(ref='inactive_display', text='current_brand')
        self.current_sales_group_label = CustomLabel(ref='inactive_display', text='current_sales_group')
        self.current_supplier_label = CustomLabel(ref='inactive_display', text='current_supplier')
        # ---- current price
        self.current_cost_label = CustomLabel(ref='inactive_display', text='current_cost')
        self.current_sell_price_label = CustomLabel(ref='inactive_display', text='current_sell_price')
        self.current_effective_dt_label = CustomLabel(ref='inactive_display', text='current_effective_dt')
        self.current_promo_name_label = CustomLabel(ref='inactive_display', text='current_promo_name')
        self.current_promo_type_label = CustomLabel(ref='inactive_display', text='current_promo_type')
        self.current_discount_percent_label = CustomLabel(ref='inactive_display', text='current_discount_percent')
        self.current_discount_value_label = CustomLabel(ref='inactive_display', text='current_discount_value')
        self.current_new_sell_price_label = CustomLabel(ref='inactive_display', text='current_new_sell_price')
        # ---- current inventory
        self.current_inventory_tracking_label = CustomLabel(ref='inactive_display', text='current_inventory_tracking')
        # ..until here.

        # can be changed from here..
        # ---- current primary information
        self.current_barcode_field = CustomLineEdit(ref='inactive_display')
        self.current_item_name_field = CustomLineEdit(ref='inactive_display')
        self.current_expire_dt_field = CustomLineEdit(ref='inactive_display')
        # ---- current category
        self.current_item_type_field = CustomLineEdit(ref='inactive_display')
        self.current_brand_field = CustomLineEdit(ref='inactive_display')
        self.current_sales_group_field = CustomLineEdit(ref='inactive_display')
        self.current_supplier_field = CustomLineEdit(ref='inactive_display')
        # ---- current price
        self.current_cost_field = CustomLineEdit(ref='inactive_display')
        self.current_sell_price_field = CustomLineEdit(ref='inactive_display')
        self.current_effective_dt_field = CustomLineEdit(ref='inactive_display')
        self.current_promo_name_field = CustomLineEdit(ref='inactive_display')
        self.current_promo_type_field = CustomLineEdit(ref='inactive_display')
        self.current_discount_percent_field = CustomLineEdit(ref='inactive_display')
        self.current_discount_value_field = CustomLineEdit(ref='inactive_display')
        self.current_new_sell_price_field = CustomLineEdit(ref='inactive_display')
        # ---- current inventory
        self.current_inventory_tracking_field = CustomLineEdit(ref='inactive_display')
        # ..until here.

        self.save_new_button = CustomPushButton(text='Save new')
        self.save_new_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='save_new_data'))
        self.save_edit_button = CustomPushButton(text='Save edit')
        self.save_edit_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='save_edit_data'))
        form_layout.addRow(self.back_button)

        # can be changed from here..
        # ---- primary information
        form_layout.addRow(self.barcode_label, self.barcode_field)
        form_layout.addRow(self.item_name_label, self.item_name_field)
        form_layout.addRow(self.expire_dt_label, self.expire_dt_field)
        # ---- category
        form_layout.addRow(self.item_type_label, self.item_type_field)
        form_layout.addRow(self.brand_label, self.brand_field)
        form_layout.addRow(self.sales_group_label, self.sales_group_field)
        form_layout.addRow(self.supplier_label, self.supplier_field)
        # ---- price
        form_layout.addRow(self.cost_label, self.cost_field)
        form_layout.addRow(self.sell_price_label, self.sell_price_field)
        form_layout.addRow(self.effective_dt_label, self.effective_dt_field)
        form_layout.addRow(self.promo_name_label, self.promo_name_field)
        form_layout.addRow(self.promo_type_label, self.promo_type_field)
        form_layout.addRow(self.discount_percent_label, self.discount_percent_field)
        form_layout.addRow(self.discount_value_label, self.discount_value_field)
        form_layout.addRow(self.new_sell_price_label, self.new_sell_price_field)
        form_layout.addRow(self.start_dt_label, self.start_dt_field)
        form_layout.addRow(self.end_dt_label, self.end_dt_field)
        # ---- inventory
        form_layout.addRow(self.inventory_tracking_label, self.inventory_tracking_field)
        form_layout.addRow(self.available_stock_label, self.available_stock_field)
        form_layout.addRow(self.on_hand_stock_label, self.on_hand_stock_field)
        # ..until here.

        form_layout.addRow(self.save_new_button)
        form_layout.addRow(self.save_edit_button)

        self.panel_b.setLayout(form_layout)

    def show_panel_a(self):
        self.panel_a = CustomGroupBox(ref='panel_a')
        grid_layout = CustomGridLayout()

        self.filter_field = CustomLineEdit(ref='filter_field', placeholderText='Filter by barcode, item name, item type, brand, sales group, supplier, inventory status, or promo name')
        self.filter_button = CustomPushButton(ref='filter_button', text='Filter')

        self.tab_sort = CustomTabWidget()
        
        # Define a helper function for creating data widgets with pagination
        def create_data_widget(data_list):
            data_box = CustomWidget()
            data_box_layout = CustomGridLayout()
            data_list_widget = CustomTableWidget(ref=f'{data_list}_list')
            previous_button = CustomPushButton(text='Previous')
            previous_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='previous_data'))
            page_number_label = CustomLabel(ref='page_number', text=f'Page {self.current_page}')
            next_button = CustomPushButton(text='Next')
            next_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='next_data'))

            data_box_layout.addWidget(data_list_widget, 0, 0,1,3)
            data_box_layout.addWidget(previous_button, 1, 0)
            data_box_layout.addWidget(page_number_label, 1, 1, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
            data_box_layout.addWidget(next_button, 1, 2)

            data_box.setLayout(data_box_layout)
            return data_box, data_list_widget, previous_button, page_number_label, next_button

        # Create data widgets with pagination
        self.overview_data_box, self.overview_data_list, self.overview_data_previous_button, self.overview_data_page_number, self.overview_data_next_button = create_data_widget('overview_data')
        self.item_data_box, self.item_data_list, self.item_data_previous_button, self.item_data_page_number, self.item_data_next_button = create_data_widget('item_data')
        self.category_data_box, self.category_data_list, self.category_data_previous_button, self.category_data_page_number, self.category_data_next_button = create_data_widget('category_data')
        self.item_price_data_box, self.item_price_data_list, self.item_price_data_previous_button, self.item_price_data_page_number, self.item_price_data_next_button = create_data_widget('item_price_data')
        self.inventory_data_box, self.inventory_data_list, self.inventory_data_previous_button, self.inventory_data_page_number, self.inventory_data_next_button = create_data_widget('inventory_data')

        self.manage_box = CustomGroupBox(ref='manage_box')
        manage_box_layout = CustomGridLayout(ref='manage_box_layout')
        self.delete_all_button = CustomPushButton(text='Delete All')
        self.delete_all_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='delete_all_data'))
        self.import_button = CustomPushButton(text='Import')
        self.import_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='import_data'))
        self.add_button = CustomPushButton(text='Add')
        self.refresh_button = CustomPushButton(text='Refresh')
        self.refresh_button.clicked.connect(self.refresh_data)
        manage_box_layout.addWidget(self.delete_all_button, 0, 0)
        manage_box_layout.addWidget(self.import_button, 0, 1)
        manage_box_layout.addWidget(self.add_button, 0, 2)
        manage_box_layout.addWidget(self.refresh_button, 0, 3)
        self.manage_box.setLayout(manage_box_layout)

        # can be changed from here..
        self.tab_sort.addTab(self.overview_data_box, 'Overview')
        self.tab_sort.addTab(self.item_data_box, 'By item')
        self.tab_sort.addTab(self.category_data_box, 'By category')
        self.tab_sort.addTab(self.item_price_data_box, 'By item price')
        self.tab_sort.addTab(self.inventory_data_box, 'By inventory')
        # until here..
        self.tab_sort.setCornerWidget(self.manage_box, Qt.Corner.TopRightCorner)

        self.total_product = self.product_management_schema.count_total_product()
        self.total_data = CustomLabel(ref='total_data', text=f'Total: {self.total_product}')
        grid_layout.addWidget(self.filter_field, 0, 0)
        grid_layout.addWidget(self.filter_button, 0, 1)
        grid_layout.addWidget(self.tab_sort, 1, 0, 1, 2)
        grid_layout.addWidget(self.total_data, 2, 0, 1, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.panel_a.setLayout(grid_layout)


    def createLayout(self):
        # ---- self.setWindowState(Qt.WindowState.WindowMaximized)

        grid_layout = CustomGridLayout()

        self.show_panel_a()
        self.show_panel_b()

        grid_layout.addWidget(self.panel_a,0,0)
        grid_layout.addWidget(self.panel_b,0,1)

        self.setLayout(grid_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagementLayout()
    window.show()
    sys.exit(pos_app.exec())
