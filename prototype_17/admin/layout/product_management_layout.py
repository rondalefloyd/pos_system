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
        self.sales_table_schema = SalesTableSchema()
        self.sales_table_schema.setup_sales_table()

        self.default_values()
        self.show_main_panel()
        self.refresh_data()

    def default_values(self):
        self.current_page = 1
        self.tab_table_page = 1
        self.required_marker = "<font color='red'><b>!</font>"
        self.selected_item_name = '[no product selected]'
          
    def edit_data(self, row_value):
        # region: hide active fields
        self.item_type_label.hide()
        self.brand_label.hide()
        self.sales_group_label.hide()
        self.supplier_label.hide()

        self.item_type_field.hide()
        self.brand_field.hide()
        self.sales_group_field.hide()
        self.supplier_field.hide()
        # endregion: hide active fields
        # region: hide inactive fields
        self.current_item_type_label.show()
        self.current_brand_label.show()
        self.current_sales_group_label.show()
        self.current_supplier_label.show()

        self.current_item_type_field.show()
        self.current_brand_field.show()
        self.current_sales_group_field.show()
        self.current_supplier_field.show()
        # endregion: hide inactive fields

        self.barcode_field.setText(str(row_value[0]))
        self.item_name_field.setText(str(row_value[1]))
        self.expire_dt_field.setDate(QDate.fromString(row_value[2], Qt.DateFormat.ISODate))

        self.current_item_type_field.setText(str(row_value[3]))
        self.current_brand_field.setText(str(row_value[4]))
        self.current_sales_group_field.setText(str(row_value[5]))
        self.current_supplier_field.setText(str(row_value[6]))
        
        self.cost_field.setText(str(row_value[7]))
        self.sell_price_field.setText(str(row_value[8]))
        self.effective_dt_field.setDate(QDate.fromString(row_value[9], Qt.DateFormat.ISODate))
        self.promo_name_field.setCurrentText(str(row_value[10]))

        self.inventory_tracking_field.setCurrentText(str(row_value[12]))
        self.available_stock_field.setText(str(row_value[13]))
        self.on_hand_stock_field.setText(str(row_value[14]))
        
        self.selected_item_id = row_value[16]
        self.selected_item_price_id = row_value[17]
        self.selected_promo_id = row_value[18]
        self.selected_stock_id = row_value[19]
        pass
    def view_data(self, row_value):
        self.view_data_dialog = CustomDialog(ref='view_data_dialog', parent=self, row_value=row_value)

        pass
    def delete_data(self, row_value):
        item_id = row_value[16]
        item_price_id = row_value[17]
        stock_id = row_value[18]

        confirmation = QMessageBox.warning(self, 'Confirm', 'Are you sure you want to delete this product?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirmation == QMessageBox.StandardButton.Yes:
            self.product_management_schema.delete_selected_product(item_price_id)
        pass

    def refresh_data(self):
        self.populate_combo_box()
        self.populate_table()
        print('refreshed!')
        pass
    def delete_all_data(self):
        confirmation_a = QMessageBox.warning(self, 'Confirm', 'Are you sure you want to delete all product?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation_a == QMessageBox.StandardButton.Yes:
            confirmation_b = QMessageBox.warning(self, 'Confirm', 'This will delete all product in the database. Proceed?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation_b == QMessageBox.StandardButton.Yes:
                while True:
                    confirmation_c, yes = QInputDialog.getText(self, 'Confirm', "Type <b>'delete all'</b> to confirm")

                    if yes:
                        if confirmation_c == 'delete all':
                            self.product_management_schema.delete_all_data()
                            break
                        else:
                            QMessageBox.critical(self, 'Error', 'Invalid input. Please try again.')
                    
                    else:
                        break

        self.delete_all_button.setDisabled(False)
        pass
    def import_data(self):
        self.import_button.setDisabled(True)

        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')

        if csv_file:
            data_frame = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)
            
            self.import_thread = CustomThread(csv_file, import_button=self.import_button)
            self.import_thread.progress_signal.connect(self.import_thread.update_progress)
            self.import_thread.finished_signal.connect(self.import_thread.import_finished)
            self.import_thread.error_signal.connect(self.import_thread.import_error)
            self.import_thread.start()
            print(data_frame)
            pass
        else:
            self.import_button.setDisabled(False)
        pass
    def add_data(self):
        # region: hide active fields
        self.item_type_label.show()
        self.brand_label.show()
        self.sales_group_label.show()
        self.supplier_label.show()
        self.inventory_tracking_label.show()

        self.item_type_field.show()
        self.brand_field.show()
        self.sales_group_field.show()
        self.supplier_field.show()
        self.inventory_tracking_field.show()
        # endregion: hide active fields
        # region: hide inactive fields
        self.current_item_type_label.hide()
        self.current_brand_label.hide()
        self.current_sales_group_label.hide()
        self.current_supplier_label.hide()
        self.current_inventory_tracking_label.hide()

        self.current_item_type_field.hide()
        self.current_brand_field.hide()
        self.current_sales_group_field.hide()
        self.current_supplier_field.hide()
        self.current_inventory_tracking_field.hide()
        # endregion: hide inactive fields
        # region: set default input on form fields (for adding)
        self.barcode_field.setText('')
        self.item_name_field.setText('')
        self.expire_dt_field.setDate(QDate.currentDate())

        self.item_type_field.setCurrentText('') if self.item_type_field.currentText() == '[no data]' else self.item_type_field

        self.cost_field.setText('0')
        self.sell_price_field.setText('0')
        self.effective_dt_field.setDate(QDate.currentDate())
        self.promo_name_field.setCurrentText('No promo')

        self.inventory_tracking_field.setCurrentText('Disabled')
        self.available_stock_field.setText('0')
        self.on_hand_stock_field.setText('0')
        # endregion: set default input on form fields (for adding)
        pass

    def save_new_data(self):
        # region: get fields' input
        barcode = self.barcode_field.text()
        item_name = self.item_name_field.text()
        expire_dt = self.expire_dt_field.date().toString(Qt.DateFormat.ISODate)
        item_type = self.item_type_field.currentText()
        brand = self.brand_field.currentText()
        sales_group = self.sales_group_field.currentText()
        supplier = self.supplier_field.currentText()
        cost = self.cost_field.text()
        sell_price = self.sell_price_field.text()
        effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)
        promo_name = self.promo_name_field.currentText()
        promo_type = self.promo_type_field.text()
        discount_percent = self.discount_percent_field.text()
        discount_value = self.discount_value_field.text()
        new_sell_price = self.new_sell_price_field.text()
        start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
        end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)
        inventory_tracking = self.inventory_tracking_field.currentText()
        available_stock = self.available_stock_field.text()
        on_hand_stock = self.on_hand_stock_field.text()
        # endregion: get fields' input

        # region: assign values if data is an empty string
        barcode = '[no data]' if barcode == '' else barcode
        expire_dt = '9999-12-31' if expire_dt == '' else expire_dt
        item_type = '[no data]' if item_type == '' else item_type
        # endregion: assign values if data is an empty string

        self.product_management_schema.add_new_product(
                # region: params
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
                promo_name=promo_name,
                promo_type=promo_type,
                discount_percent=discount_percent,
                discount_value=discount_value,
                new_sell_price=new_sell_price,
                start_dt=start_dt,
                end_dt=end_dt,
                inventory_tracking=inventory_tracking,
                available_stock=available_stock,
                on_hand_stock=on_hand_stock
                # endregion: params
        )
        pass
    def save_edit_data(self):
        # region: assign input values to variables
        barcode = self.barcode_field.text()
        item_name = self.item_name_field.text()
        expire_dt = self.expire_dt_field.date().toString(Qt.DateFormat.ISODate)
        item_type = self.item_type_field.currentText()
        brand = self.brand_field.currentText()
        sales_group = self.sales_group_field.currentText()
        supplier = self.supplier_field.currentText()
        cost = self.cost_field.text()
        sell_price = self.sell_price_field.text()
        effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)
        promo_name = self.promo_name_field.currentText()
        promo_type = self.promo_type_field.text()
        discount_percent = self.discount_percent_field.text()
        discount_value = self.discount_value_field.text()
        new_sell_price = self.new_sell_price_field.text()
        start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
        end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)
        inventory_tracking = self.inventory_tracking_field.currentText()
        available_stock = self.available_stock_field.text()
        on_hand_stock = self.on_hand_stock_field.text()

        # selected data identifier
        item_id = self.selected_item_id
        item_price_id = self.selected_item_price_id
        promo_id = self.selected_promo_id
        stock_id = self.selected_stock_id
        # endregion: assign input values to variables

        self.product_management_schema.edit_selected_item(
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
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            discount_value=discount_value,
            new_sell_price=new_sell_price,
            start_dt=start_dt,
            end_dt=end_dt,
            inventory_tracking=inventory_tracking,
            available_stock=available_stock,
            on_hand_stock=on_hand_stock,

            item_id=item_id,
            item_price_id=item_price_id,
            promo_id=promo_id,
            stock_id=stock_id
        )

        self.selected_product.setText(f'Selected product: {item_name}')

        QMessageBox.information(self, 'Success', 'Product has been edited!')
        pass

    def on_push_button_clicked(self, row_value='', clicked_ref=''):
        if clicked_ref == 'edit_button':
            self.panel_b_box.show()
            self.add_button.setDisabled(False)
            self.selected_data_box.show()
            self.save_new_button.hide()
            self.save_edit_button.show()

            self.selected_item_name = f'{row_value[1]}'
            self.selected_product.setText(f'Selected product: {self.selected_item_name}')

            self.edit_data(row_value)
            pass
        if clicked_ref == 'view_button':
            self.view_data(row_value)
            pass
        if clicked_ref == 'delete_button':
            self.delete_data(row_value)
            pass

        if clicked_ref == 'previous_button':
            if self.current_page > 1:
                self.current_page -= 1

                # region: pagination page label
                self.overview_pagination_page_label.setText(f'Page {self.current_page}')
                self.primary_pagination_page_label.setText(f'Page {self.current_page}')
                self.category_pagination_page_label.setText(f'Page {self.current_page}')
                self.price_pagination_page_label.setText(f'Page {self.current_page}')
                self.inventory_pagination_page_label.setText(f'Page {self.current_page}')
                # endregion: pagination page label

            self.populate_table(current_page=self.current_page)
            pass
        if clicked_ref == 'next_button':
            self.current_page += 1

            # region: pagination page label
            self.overview_pagination_page_label.setText(f'Page {self.current_page}')
            self.primary_pagination_page_label.setText(f'Page {self.current_page}')
            self.category_pagination_page_label.setText(f'Page {self.current_page}')
            self.price_pagination_page_label.setText(f'Page {self.current_page}')
            self.inventory_pagination_page_label.setText(f'Page {self.current_page}')
            # endregion: pagination page label
            
            self.populate_table(current_page=self.current_page)

        if clicked_ref == 'refresh_button':
            self.refresh_data()
            pass
        if clicked_ref == 'delete_all_button':
            self.delete_all_button.setDisabled(True)
            self.delete_all_data()
            pass
        if clicked_ref == 'import_button':
            self.import_data()
            pass
        if clicked_ref == 'add_button':
            self.panel_b_box.show()
            self.add_button.setDisabled(True)
            self.selected_data_box.hide()
            self.save_new_button.show()
            self.save_edit_button.hide()

            self.selected_item_name = '[no product selected]'
            self.selected_product.setText(f'Selected product: {self.selected_item_name}')
            
            self.add_data()

        if clicked_ref == 'back_button':
            self.panel_b_box.hide()
            self.add_button.setDisabled(False)       
        if clicked_ref == 'save_new_button':
            self.save_new_data()
            pass
        if clicked_ref == 'save_edit_button':
            self.save_edit_data()
            pass
        pass
    def on_line_edit_text_changed(self, text_changed_ref):
        if text_changed_ref == 'filter_field':
            self.current_page = 1

            # region: pagination page label
            self.overview_pagination_page_label.setText(f'Page {self.current_page}')
            self.primary_pagination_page_label.setText(f'Page {self.current_page}')
            self.category_pagination_page_label.setText(f'Page {self.current_page}')
            self.price_pagination_page_label.setText(f'Page {self.current_page}')
            self.inventory_pagination_page_label.setText(f'Page {self.current_page}')
            # endregion: pagination page label

            self.populate_table(current_page=self.current_page)
        
        if text_changed_ref == 'sell_price_field':
            # region: calculate discount amount and new sell price
            promo_name = self.promo_name_field.currentText()

            data = self.product_management_schema.list_promo_type_and_discount_percent(promo_name)
            for row in data:
                self.promo_type_field.setText(str(row[0]))
                self.discount_percent_field.setText(str(row[1]))

            try:
                sell_price = float(self.sell_price_field.text())
                discount_percent = float(self.discount_percent_field.text())

                old_sell_price = sell_price
                discount_amount = old_sell_price * (discount_percent / 100)
                
                new_sell_price = sell_price - discount_amount

                self.discount_value_field.setText(f'{discount_amount:.2f}')
                self.new_sell_price_field.setText(f'{new_sell_price:.2f}')
                pass
            except ValueError:
                pass
            # endregion: calculate discount amount and new sell price
        pass
    def on_combo_box_current_text_changed(self, current_text, current_text_changed_ref):
        if current_text_changed_ref == 'promo_name_field':
            if current_text in ['No promo','']:
                self.effective_dt_label.show()
                self.promo_type_label.hide()
                self.discount_percent_label.hide()
                self.discount_value_label.hide()
                self.new_sell_price_label.hide()
                self.start_dt_label.hide()
                self.end_dt_label.hide()

                self.effective_dt_field.show()
                self.promo_type_field.hide()
                self.discount_percent_field.hide()
                self.discount_value_field.hide()
                self.new_sell_price_field.hide()
                self.start_dt_field.hide()
                self.end_dt_field.hide()
            else:
                self.effective_dt_label.hide()
                self.promo_type_label.show()
                self.discount_percent_label.show()
                self.discount_value_label.show()
                self.new_sell_price_label.show()
                self.start_dt_label.show()
                self.end_dt_label.show()

                self.effective_dt_field.hide()
                self.promo_type_field.show()
                self.discount_percent_field.show()
                self.discount_value_field.show()
                self.new_sell_price_field.show()
                self.start_dt_field.show()
                self.end_dt_field.show()

                # region: calculate discount amount and new sell price
                promo_name = self.promo_name_field.currentText()

                data = self.product_management_schema.list_promo_type_and_discount_percent(promo_name)
                for row in data:
                    self.promo_type_field.setText(str(row[0]))
                    self.discount_percent_field.setText(str(row[1]))

                try:
                    sell_price = float(self.sell_price_field.text())
                    discount_percent = float(self.discount_percent_field.text())

                    old_sell_price = sell_price
                    discount_amount = old_sell_price * (discount_percent / 100)
                    
                    new_sell_price = sell_price - discount_amount

                    self.discount_value_field.setText(f'{discount_amount:.2f}')
                    self.new_sell_price_field.setText(f'{new_sell_price:.2f}')
                    pass
                except ValueError:
                    pass
                # endregion: calculate discount amount and new sell price
                pass
        if current_text_changed_ref == 'inventory_tracking_field':
            if current_text in ['Disabled','']:
                self.available_stock_label.hide()
                self.on_hand_stock_label.hide()

                self.available_stock_field.hide()
                self.on_hand_stock_field.hide()
                pass
            elif current_text == 'Enabled':
                self.available_stock_label.show()
                self.on_hand_stock_label.show()

                self.available_stock_field.show()
                self.on_hand_stock_field.show()
                pass

    def call_signal(
            # region: params
            self,
            edit_button=None,
            view_button=None,
            delete_button=None,
            row_value='',
            signal_ref=''
            # endregion: params
    ):
        if signal_ref == 'panel_a_signal':
            self.filter_field.textChanged.connect(lambda: self.on_line_edit_text_changed(text_changed_ref='filter_field'))

            # region: pagination
            self.overview_pagination_previous_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='previous_button'))
            self.primary_pagination_previous_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='previous_button'))
            self.category_pagination_previous_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='previous_button'))
            self.price_pagination_previous_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='previous_button'))
            self.inventory_pagination_previous_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='previous_button'))

            self.overview_pagination_next_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='next_button'))
            self.primary_pagination_next_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='next_button'))
            self.category_pagination_next_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='next_button'))
            self.price_pagination_next_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='next_button'))
            self.inventory_pagination_next_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='next_button'))
            # endregion: pagination
            # region: manage data buttons
            self.refresh_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='refresh_button'))
            self.delete_all_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='delete_all_button'))
            self.add_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='add_button'))
            self.import_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='import_button'))
            # endregion: manage data buttons
            pass
        if signal_ref == 'populate_table_signal':
            edit_button.clicked.connect(lambda: self.on_push_button_clicked(row_value=row_value, clicked_ref='edit_button'))
            view_button.clicked.connect(lambda: self.on_push_button_clicked(row_value=row_value, clicked_ref='view_button'))
            delete_button.clicked.connect(lambda: self.on_push_button_clicked(row_value=row_value, clicked_ref='delete_button'))
            pass

        if signal_ref == 'panel_b_signal':
            self.sell_price_field.textChanged.connect(lambda: self.on_line_edit_text_changed(text_changed_ref='sell_price_field'))

            self.promo_name_field.currentTextChanged.connect(
                lambda current_text: self.on_combo_box_current_text_changed(
                    current_text=current_text, 
                    current_text_changed_ref='promo_name_field'
                )
            )

            self.inventory_tracking_field.currentTextChanged.connect(
                lambda current_text: self.on_combo_box_current_text_changed(
                    current_text=current_text,
                    current_text_changed_ref='inventory_tracking_field'
                )
            )

            self.back_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='back_button'))
            self.save_new_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='save_new_button'))
            self.save_edit_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='save_edit_button'))
            pass

    def populate_combo_box(self):
        item_type = self.product_management_schema.list_item_type()
        brand = self.product_management_schema.list_brand()
        supplier = self.product_management_schema.list_supplier()
        promo_name = self.product_management_schema.list_promo()

        self.item_type_field.addItems(data[0] for data in item_type)
        self.brand_field.addItems(data[0] for data in brand)
        self.supplier_field.addItems(data[0] for data in supplier)
        self.promo_name_field.addItems(data[0] for data in promo_name)
        pass
    def populate_table(self, current_page=1):
        product_data = self.product_management_schema.list_product(text_filter=self.filter_field.text(), page_number=current_page)
        inventory_data = self.product_management_schema.list_inventory(text_filter=self.filter_field.text(), page_number=current_page)

        # region: table pagination button
        self.overview_pagination_previous_button.setEnabled(self.current_page > 1)
        self.primary_pagination_previous_button.setEnabled(self.current_page > 1)
        self.category_pagination_previous_button.setEnabled(self.current_page > 1)
        self.price_pagination_previous_button.setEnabled(self.current_page > 1)
        self.inventory_pagination_previous_button.setEnabled(self.current_page > 1)

        self.overview_pagination_next_button.setEnabled(len(product_data) == 30)
        self.primary_pagination_next_button.setEnabled(len(product_data) == 30)
        self.category_pagination_next_button.setEnabled(len(product_data) == 30)
        self.price_pagination_next_button.setEnabled(len(product_data) == 30)
        self.inventory_pagination_next_button.setEnabled(len(product_data) == 30)
        # endregion: pagination button
        # region: table row count
        self.overview_table.setRowCount(len(product_data))
        self.primary_table.setRowCount(len(product_data))
        self.category_table.setRowCount(len(product_data))
        self.price_table.setRowCount(len(product_data))

        self.inventory_table.setRowCount(len(inventory_data))
        # endregion: set tables' row count

        for row_index, row_value in enumerate(product_data):
            # region: action button
            table_action_menu = CustomWidget(ref='table_action_menu')
            table_action_menu_layout = CustomHBoxLayout(ref='table_action_menu_layout')
            self.edit_button = CustomPushButton(ref='edit_button')
            self.view_button = CustomPushButton(ref='view_button')
            self.delete_button = CustomPushButton(ref='delete_button')
            table_action_menu_layout.addWidget(self.edit_button)
            table_action_menu_layout.addWidget(self.view_button)
            table_action_menu_layout.addWidget(self.delete_button)
            table_action_menu.setLayout(table_action_menu_layout)

            self.call_signal(
                edit_button=self.edit_button,
                view_button=self.view_button,
                delete_button=self.delete_button,
                row_value=row_value, 
                signal_ref='populate_table_signal'
            )
            pass
            # endregion: action button
            # region: assign values
            item_name = [
                (CustomTableWidgetItem(text=f'{row_value[1]}')),
                (CustomTableWidgetItem(text=f'{row_value[1]}')),
                (CustomTableWidgetItem(text=f'{row_value[1]}')),
                (CustomTableWidgetItem(text=f'{row_value[1]}')),
                (CustomTableWidgetItem(text=f'{row_value[1]}')),
            ]
            barcode = CustomTableWidgetItem(text=f'{row_value[0]}')
            expire_dt = CustomTableWidgetItem(text=f'{row_value[2]}')
            item_type = CustomTableWidgetItem(text=f'{row_value[3]}')
            brand = [
                (CustomTableWidgetItem(text=f'{row_value[4]}')),
                (CustomTableWidgetItem(text=f'{row_value[4]}')),
                (CustomTableWidgetItem(text=f'{row_value[4]}')),
                (CustomTableWidgetItem(text=f'{row_value[4]}')),
                (CustomTableWidgetItem(text=f'{row_value[4]}'))
            ]
            sales_group = [
                CustomTableWidgetItem(ref='sales_group', text=f'{row_value[5]}'),
                CustomTableWidgetItem(ref='sales_group', text=f'{row_value[5]}'),
                CustomTableWidgetItem(ref='sales_group', text=f'{row_value[5]}'),
                CustomTableWidgetItem(ref='sales_group', text=f'{row_value[5]}'),
                CustomTableWidgetItem(ref='sales_group', text=f'{row_value[5]}')
            ]
            supplier = CustomTableWidgetItem(ref='supplier', text=f'{row_value[6]}')
            cost = CustomTableWidgetItem(ref='cost', text=f'₱{row_value[7]}')
            sell_price = [
                CustomTableWidgetItem(ref='sell_price', text=f'₱{row_value[8]}'),
                CustomTableWidgetItem(ref='sell_price', text=f'₱{row_value[8]}'),
                CustomTableWidgetItem(ref='sell_price', text=f'₱{row_value[8]}'),
                CustomTableWidgetItem(ref='sell_price', text=f'₱{row_value[8]}'),
                CustomTableWidgetItem(ref='sell_price', text=f'₱{row_value[8]}')
            ]
            discount_value = CustomTableWidgetItem(ref='discount_value', text=f'₱{row_value[11]}')
            effective_dt = CustomTableWidgetItem(text=f'{row_value[9]}')
            promo_name = [
                CustomTableWidgetItem(ref='promo_name', text=f'{row_value[10]}'),
                CustomTableWidgetItem(ref='promo_name', text=f'{row_value[10]}'),
                CustomTableWidgetItem(ref='promo_name', text=f'{row_value[10]}'),
                CustomTableWidgetItem(ref='promo_name', text=f'{row_value[10]}'),
                CustomTableWidgetItem(ref='promo_name', text=f'{row_value[10]}')
            ]
            inventory_tracking = [
                CustomTableWidgetItem(ref='inventory_tracking', text=f'{row_value[12]}'),
                CustomTableWidgetItem(ref='inventory_tracking', text=f'{row_value[12]}'),
                CustomTableWidgetItem(ref='inventory_tracking', text=f'{row_value[12]}'),
                CustomTableWidgetItem(ref='inventory_tracking', text=f'{row_value[12]}'),
                CustomTableWidgetItem(ref='inventory_tracking', text=f'{row_value[12]}')
            ]
            update_ts = [
                CustomTableWidgetItem(ref='update_ts', text=f'{row_value[15]}'),
                CustomTableWidgetItem(ref='update_ts', text=f'{row_value[15]}'),
                CustomTableWidgetItem(ref='update_ts', text=f'{row_value[15]}'),
                CustomTableWidgetItem(ref='update_ts', text=f'{row_value[15]}'),
                CustomTableWidgetItem(ref='update_ts', text=f'{row_value[15]}')
            ]
            
            promo_id = row_value[18]

            if promo_id != 0:
                barcode.setForeground(QColor(255,0,0))
                expire_dt.setForeground(QColor(255,0,0))
                item_type.setForeground(QColor(255,0,0))
                supplier.setForeground(QColor(255,0,0))
                cost.setForeground(QColor(255,0,0))
                discount_value.setForeground(QColor(255,0,0))
                effective_dt.setForeground(QColor(255,0,0))

                for item_name_data in item_name: item_name_data.setForeground(QColor(255,0,0))
                for brand_data in brand: brand_data.setForeground(QColor(255,0,0))
                for sales_group_data in sales_group: sales_group_data.setForeground(QColor(255,0,0))
                for sell_price_data in sell_price: sell_price_data.setForeground(QColor(255,0,0))
                for promo_name_data in promo_name: promo_name_data.setForeground(QColor(255,0,0))
                for inventory_tracking_data in inventory_tracking: inventory_tracking_data.setForeground(QColor(255,0,0))
                for update_ts_data in update_ts: update_ts_data.setForeground(QColor(255,0,0))

                self.edit_button.hide()

            # endregion: assign values

            # region: overview list
            self.overview_table.setCellWidget(row_index, 0, table_action_menu)
            self.overview_table.setItem(row_index, 1, item_name[0])
            self.overview_table.setItem(row_index, 2, brand[0])
            self.overview_table.setItem(row_index, 3, sales_group[0])
            self.overview_table.setItem(row_index, 4, sell_price[0])
            self.overview_table.setItem(row_index, 5, promo_name[0])
            self.overview_table.setItem(row_index, 6, inventory_tracking[0])
            self.overview_table.setItem(row_index, 7, update_ts[0])
            # endregion: overview list
            # region: primary list
            self.primary_table.setItem(row_index, 0, barcode)
            self.primary_table.setItem(row_index, 1, item_name[1])
            self.primary_table.setItem(row_index, 2, expire_dt)
            self.primary_table.setItem(row_index, 3, promo_name[1])
            self.primary_table.setItem(row_index, 4, update_ts[1])
            # endregion: primary list
            # region: category list
            self.category_table.setItem(row_index, 0, item_name[2])
            self.category_table.setItem(row_index, 1, item_type)
            self.category_table.setItem(row_index, 2, brand[2])
            self.category_table.setItem(row_index, 3, sales_group[2])
            self.category_table.setItem(row_index, 4, supplier)
            self.category_table.setItem(row_index, 5, promo_name[2])
            self.category_table.setItem(row_index, 6, update_ts[2])
            # endregion: category list
            # region: price list
            self.price_table.setItem(row_index, 0, item_name[3])
            self.price_table.setItem(row_index, 1, cost)
            self.price_table.setItem(row_index, 2, sell_price[3])
            self.price_table.setItem(row_index, 3, discount_value)
            self.price_table.setItem(row_index, 4, effective_dt)
            self.price_table.setItem(row_index, 5, promo_name[3])
            self.price_table.setItem(row_index, 6, update_ts[3])
            # endregion: price list

        for row_index, row_value in enumerate(inventory_data):
            item_name = CustomTableWidgetItem(text=f'{row_value[0]}')
            available_stock = CustomTableWidgetItem(ref='available_stock', text=f'{row_value[1]}')
            on_hand_stock = CustomTableWidgetItem(ref='on_hand_stock', text=f'{row_value[2]}')
            update_ts = CustomTableWidgetItem(ref='update_ts', text=f'{row_value[5]}')
            # region: inventory list
            self.inventory_table.setItem(row_index, 0, item_name)
            self.inventory_table.setItem(row_index, 1, available_stock)
            self.inventory_table.setItem(row_index, 2, on_hand_stock)
            self.inventory_table.setItem(row_index, 3, update_ts)
            # endregion: inventory list

    def show_panel_b(self):
        self.panel_b_box = CustomGroupBox(ref='panel_b_box')
        self.panel_b_box_layout = CustomFormLayout()
        
        # region: form fields
        # region: primary fields
        self.primary_box = CustomGroupBox(ref='primary_box')
        self.primary_box_layout = CustomFormLayout()

        self.primary_box_label = CustomLabel(text='Primary Information')
        
        self.barcode_label = CustomLabel(ref='barcode_label', text='barcode')
        self.item_name_label = CustomLabel(ref='item_name_label', text=f'{self.required_marker} item_name')
        self.expire_dt_label = CustomLabel(ref='expire_dt_label', text='expire_dt')

        self.barcode_field = CustomLineEdit(ref='barcode_field')
        self.item_name_field = CustomLineEdit(ref='item_name_field')
        self.expire_dt_field = CustomDateEdit(ref='expire_dt_field')
        
        self.primary_box_layout.insertRow(0, self.primary_box_label)
        self.primary_box_layout.insertRow(1, self.barcode_label, self.barcode_field)
        self.primary_box_layout.insertRow(2, self.item_name_label, self.item_name_field)
        self.primary_box_layout.insertRow(3, self.expire_dt_label, self.expire_dt_field)

        self.current_barcode_label = CustomLabel(ref='inactive_label', text='current_barcode')
        self.current_item_name_label = CustomLabel(ref='inactive_label', text='current_item_name')
        self.current_expire_dt_label = CustomLabel(ref='inactive_label', text='current_expire_dt')

        self.current_barcode_field = CustomLineEdit(ref='inactive_field')
        self.current_item_name_field = CustomLineEdit(ref='inactive_field')
        self.current_expire_dt_field = CustomLineEdit(ref='inactive_field')

        self.primary_box_layout.insertRow(1, self.current_barcode_label, self.current_barcode_field)
        self.primary_box_layout.insertRow(2, self.current_item_name_label, self.current_item_name_field)
        self.primary_box_layout.insertRow(3, self.current_expire_dt_label, self.current_expire_dt_field)

        self.primary_box.setLayout(self.primary_box_layout)
        # endregion: primary fields
        # region: category fields
        self.category_box = CustomGroupBox(ref='category_box')
        self.category_box_layout = CustomFormLayout()

        self.category_box_label = CustomLabel(text='Category')

        self.item_type_label = CustomLabel(ref='item_type_label', text='item_type')
        self.brand_label = CustomLabel(ref='brand_label', text=f'{self.required_marker} brand')
        self.sales_group_label = CustomLabel(ref='sales_group_label', text=f'{self.required_marker} sales_group')
        self.supplier_label = CustomLabel(ref='supplier_label', text=f'{self.required_marker} supplier')

        self.item_type_field = CustomComboBox(ref='item_type_field')
        self.brand_field = CustomComboBox(ref='brand_field')
        self.sales_group_field = CustomComboBox(ref='sales_group_field')
        self.supplier_field = CustomComboBox(ref='supplier_field')

        self.category_box_layout.insertRow(0, self.category_box_label)
        self.category_box_layout.insertRow(1, self.item_type_label, self.item_type_field)
        self.category_box_layout.insertRow(2, self.brand_label, self.brand_field)
        self.category_box_layout.insertRow(3, self.sales_group_label, self.sales_group_field)
        self.category_box_layout.insertRow(4, self.supplier_label, self.supplier_field)

        self.current_item_type_label = CustomLabel(ref='inactive_label', text='current_item_type')
        self.current_brand_label = CustomLabel(ref='inactive_label', text='current_brand')
        self.current_sales_group_label = CustomLabel(ref='inactive_label', text='current_sales_group')
        self.current_supplier_label = CustomLabel(ref='inactive_label', text='current_supplier')

        self.current_item_type_field = CustomLineEdit(ref='inactive_field')
        self.current_brand_field = CustomLineEdit(ref='inactive_field')
        self.current_sales_group_field = CustomLineEdit(ref='inactive_field')
        self.current_supplier_field = CustomLineEdit(ref='inactive_field')

        self.category_box_layout.insertRow(1, self.current_item_type_label, self.current_item_type_field)
        self.category_box_layout.insertRow(2, self.current_brand_label, self.current_brand_field)
        self.category_box_layout.insertRow(3, self.current_sales_group_label, self.current_sales_group_field)
        self.category_box_layout.insertRow(4, self.current_supplier_label, self.current_supplier_field)

        self.category_box.setLayout(self.category_box_layout)
        # endregion: category fields
        # region: price fields
        self.price_box = CustomGroupBox(ref='price_box')
        self.price_box_layout = CustomFormLayout()

        self.price_box_label = CustomLabel(text='Price')

        self.cost_label = CustomLabel(ref='cost_label', text=f'{self.required_marker} cost')
        self.sell_price_label = CustomLabel(ref='sell_price_label', text=f'{self.required_marker} sell_price')
        self.effective_dt_label = CustomLabel(ref='effective_dt_label', text='effective_dt')
        self.promo_name_label = CustomLabel(ref='promo_name_label', text='promo_name')
        self.promo_type_label = CustomLabel(ref='promo_type_label', text='promo_type')
        self.discount_percent_label = CustomLabel(ref='discount_percent_label', text='discount_percent')
        self.discount_value_label = CustomLabel(ref='discount_value_label', text='discount_value')
        self.new_sell_price_label = CustomLabel(ref='new_sell_price_label', text='new_sell_price')
        self.start_dt_label = CustomLabel(ref='start_dt_label', text='start_dt')
        self.end_dt_label = CustomLabel(ref='end_dt_label', text='end_dt')

        self.cost_field = CustomLineEdit(ref='cost_field')
        self.sell_price_field = CustomLineEdit(ref='sell_price_field')
        self.effective_dt_field = CustomDateEdit(ref='effective_dt_field')
        self.promo_name_field = CustomComboBox(ref='promo_name_field')
        self.promo_type_field = CustomLineEdit(ref='promo_type_field')
        self.discount_percent_field = CustomLineEdit(ref='discount_percent_field')
        self.discount_value_field = CustomLineEdit(ref='discount_value_field')
        self.new_sell_price_field = CustomLineEdit(ref='new_sell_price_field')
        self.start_dt_field = CustomDateEdit(ref='start_dt_field')
        self.end_dt_field = CustomDateEdit(ref='end_dt_field')

        self.price_box_layout.insertRow(0, self.price_box_label)
        self.price_box_layout.insertRow(1, self.cost_label, self.cost_field)
        self.price_box_layout.insertRow(2, self.sell_price_label, self.sell_price_field)
        self.price_box_layout.insertRow(3, self.effective_dt_label, self.effective_dt_field)
        self.price_box_layout.insertRow(4, self.promo_name_label, self.promo_name_field)
        self.price_box_layout.insertRow(5, self.promo_type_label, self.promo_type_field)
        self.price_box_layout.insertRow(6, self.discount_percent_label, self.discount_percent_field)
        self.price_box_layout.insertRow(7, self.discount_value_label, self.discount_value_field)
        self.price_box_layout.insertRow(8, self.new_sell_price_label, self.new_sell_price_field)
        self.price_box_layout.insertRow(9, self.start_dt_label, self.start_dt_field)
        self.price_box_layout.insertRow(10, self.end_dt_label, self.end_dt_field)

        self.current_cost_label = CustomLabel(ref='inactive_label', text='current_cost')
        self.current_sell_price_label = CustomLabel(ref='inactive_label', text='current_sell_price')
        self.current_effective_dt_label = CustomLabel(ref='inactive_label', text='current_effective_dt')
        self.current_promo_name_label = CustomLabel(ref='inactive_label', text='current_promo_name')
        self.current_promo_type_label = CustomLabel(ref='inactive_label', text='current_promo_type')
        self.current_discount_percent_label = CustomLabel(ref='inactive_label', text='current_discount_percent')
        self.current_discount_value_label = CustomLabel(ref='inactive_label', text='current_discount_value')
        self.current_new_sell_price_label = CustomLabel(ref='inactive_label', text='current_new_sell_price')

        self.current_cost_field = CustomLineEdit(ref='inactive_field')
        self.current_sell_price_field = CustomLineEdit(ref='inactive_field')
        self.current_effective_dt_field = CustomLineEdit(ref='inactive_field')
        self.current_promo_name_field = CustomLineEdit(ref='inactive_field')
        self.current_promo_type_field = CustomLineEdit(ref='inactive_field')
        self.current_discount_percent_field = CustomLineEdit(ref='inactive_field')
        self.current_discount_value_field = CustomLineEdit(ref='inactive_field')
        self.current_new_sell_price_field = CustomLineEdit(ref='inactive_field')

        self.price_box_layout.insertRow(1, self.current_cost_label, self.current_cost_field)
        self.price_box_layout.insertRow(2, self.current_sell_price_label, self.current_sell_price_field)
        self.price_box_layout.insertRow(3, self.current_effective_dt_label, self.current_effective_dt_field)
        self.price_box_layout.insertRow(4, self.current_promo_name_label, self.current_promo_name_field)
        self.price_box_layout.insertRow(5, self.current_promo_type_label, self.current_promo_type_field)
        self.price_box_layout.insertRow(6, self.current_discount_percent_label, self.current_discount_percent_field)
        self.price_box_layout.insertRow(7, self.current_discount_value_label, self.current_discount_value_field)
        self.price_box_layout.insertRow(8, self.current_new_sell_price_label, self.current_new_sell_price_field)

        self.price_box.setLayout(self.price_box_layout)
        # endregion: price fields
        # region: inventory fields
        self.inventory_box = CustomGroupBox(ref='inventory_box')
        self.inventory_box_layout = CustomFormLayout()

        self.inventory_box_label = CustomLabel(text='Inventory')

        self.inventory_tracking_label = CustomLabel(ref='inventory_tracking_label', text='inventory_tracking')
        self.available_stock_label = CustomLabel(ref='available_stock_label', text=f'{self.required_marker} available_stock')
        self.on_hand_stock_label = CustomLabel(ref='on_hand_stock_label', text=f'{self.required_marker} on_hand_stock')

        self.inventory_tracking_field = CustomComboBox(ref='inventory_tracking_field')
        self.available_stock_field = CustomLineEdit(ref='available_stock_field')
        self.on_hand_stock_field = CustomLineEdit(ref='on_hand_stock_field')

        self.inventory_box_layout.insertRow(0, self.inventory_box_label)
        self.inventory_box_layout.insertRow(1, self.inventory_tracking_label, self.inventory_tracking_field)
        self.inventory_box_layout.insertRow(2, self.available_stock_label, self.available_stock_field)
        self.inventory_box_layout.insertRow(3, self.on_hand_stock_label, self.on_hand_stock_field)

        self.current_inventory_tracking_label = CustomLabel(ref='inactive_label', text='current_inventory_tracking')

        self.current_inventory_tracking_field = CustomLineEdit(ref='inactive_field')

        self.inventory_box_layout.insertRow(1, self.current_inventory_tracking_label, self.current_inventory_tracking_field)

        self.inventory_box.setLayout(self.inventory_box_layout)
        # endregion: inventory fields
        # endregion: form fields
        # region: form buttons
        self.selected_data_box = CustomGroupBox()
        self.selected_data_layout = CustomFormLayout()
        self.selected_product = CustomLabel(text=f'Selected product: {self.selected_item_name}')
        self.selected_data_layout.addRow(self.selected_product)
        self.selected_data_box.setLayout(self.selected_data_layout)

        self.panel_b_action_menu = CustomGroupBox()
        self.panel_b_action_menu_layout = CustomGridLayout()
        self.back_button = CustomPushButton(text='Back')
        self.save_new_button = CustomPushButton(text='Save Add')
        self.save_edit_button = CustomPushButton(text='Save Edit')
        self.panel_b_action_menu_layout.addWidget(self.back_button,0,0)
        self.panel_b_action_menu_layout.addWidget(self.save_new_button,0,1)
        self.panel_b_action_menu_layout.addWidget(self.save_edit_button,0,1)
        self.panel_b_action_menu.setLayout(self.panel_b_action_menu_layout)
        # endregion: form buttons

        self.panel_b_box_layout.insertRow(0, self.selected_data_box)
        self.panel_b_box_layout.insertRow(1, self.primary_box)
        self.panel_b_box_layout.insertRow(2, self.category_box)
        self.panel_b_box_layout.insertRow(3, self.price_box)
        self.panel_b_box_layout.insertRow(4, self.inventory_box)
        self.panel_b_box_layout.insertRow(5, self.panel_b_action_menu)

        self.panel_b_box.setLayout(self.panel_b_box_layout)

        self.call_signal(signal_ref='panel_b_signal')
        pass
    def show_panel_a(self):
        self.panel_a_box = CustomGroupBox()
        self.panel_a_box_layout = CustomGridLayout()

        self.filter_field = CustomLineEdit(ref='filter_field')
        # region: overview pagination table
        self.overview_table = CustomTableWidget(ref='overview_table')
        self.overview_pagination = CustomWidget(ref='overview_pagination')
        self.overview_pagination_layout = CustomGridLayout(ref='overview_pagination_layout')
        self.overview_pagination_previous_button = CustomPushButton(ref='previous_button')
        self.overview_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.overview_pagination_next_button = CustomPushButton(ref='next_button')
        self.overview_pagination_layout.addWidget(self.overview_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_layout.addWidget(self.overview_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_layout.addWidget(self.overview_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination.setLayout(self.overview_pagination_layout)
        self.overview_tab_layout = CustomGridLayout() 
        self.overview_tab_layout.addWidget(self.overview_table,0,0)
        self.overview_tab_layout.addWidget(self.overview_pagination,1,0,Qt.AlignmentFlag.AlignCenter)
        self.overview_tab = CustomWidget() 
        self.overview_tab.setLayout(self.overview_tab_layout) 
        # endregion: overview pagination table
        # region: primary pagination table
        self.primary_table = CustomTableWidget(ref='primary_table')
        self.primary_pagination = CustomWidget(ref='primary_pagination')
        self.primary_pagination_layout = CustomGridLayout(ref='primary_pagination_layout')
        self.primary_pagination_previous_button = CustomPushButton(ref='previous_button')
        self.primary_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.primary_pagination_next_button = CustomPushButton(ref='next_button')
        self.primary_pagination_layout.addWidget(self.primary_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.primary_pagination_layout.addWidget(self.primary_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.primary_pagination_layout.addWidget(self.primary_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.primary_pagination.setLayout(self.primary_pagination_layout)
        self.primary_tab_layout = CustomGridLayout()
        self.primary_tab_layout.addWidget(self.primary_table,0,0)
        self.primary_tab_layout.addWidget(self.primary_pagination,1,0,Qt.AlignmentFlag.AlignCenter)
        self.primary_tab = CustomWidget() 
        self.primary_tab.setLayout(self.primary_tab_layout) 
        # endregion: primary pagination table
        # region: category pagination table
        self.category_table = CustomTableWidget(ref='category_table')
        self.category_pagination = CustomWidget(ref='category_pagination')
        self.category_pagination_layout = CustomGridLayout(ref='category_pagination_layout')
        self.category_pagination_previous_button = CustomPushButton(ref='previous_button')
        self.category_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.category_pagination_next_button = CustomPushButton(ref='next_button')
        self.category_pagination_layout.addWidget(self.category_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.category_pagination_layout.addWidget(self.category_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.category_pagination_layout.addWidget(self.category_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.category_pagination.setLayout(self.category_pagination_layout)
        self.category_tab_layout = CustomGridLayout()
        self.category_tab_layout.addWidget(self.category_table,0,0)
        self.category_tab_layout.addWidget(self.category_pagination,1,0,Qt.AlignmentFlag.AlignCenter)
        self.category_tab = CustomWidget() 
        self.category_tab.setLayout(self.category_tab_layout) 
        # endregion: category pagination table
        # region: price pagination table
        self.price_table = CustomTableWidget(ref='price_table')
        self.price_pagination = CustomWidget(ref='price_pagination')
        self.price_pagination_layout = CustomGridLayout(ref='price_pagination_layout')
        self.price_pagination_previous_button = CustomPushButton(ref='previous_button')
        self.price_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.price_pagination_next_button = CustomPushButton(ref='next_button')
        self.price_pagination_layout.addWidget(self.price_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.price_pagination_layout.addWidget(self.price_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.price_pagination_layout.addWidget(self.price_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.price_pagination.setLayout(self.price_pagination_layout)
        self.price_tab_layout = CustomGridLayout()
        self.price_tab_layout.addWidget(self.price_table,0,0)
        self.price_tab_layout.addWidget(self.price_pagination,1,0,Qt.AlignmentFlag.AlignCenter)
        self.price_tab = CustomWidget() 
        self.price_tab.setLayout(self.price_tab_layout) 
        # endregion: price pagination table
        # region: inventory pagination table
        self.inventory_table = CustomTableWidget(ref='inventory_table')
        self.inventory_pagination = CustomWidget(ref='inventory_pagination')
        self.inventory_pagination_layout = CustomGridLayout(ref='inventory_pagination_layout')
        self.inventory_pagination_previous_button = CustomPushButton(ref='previous_button')
        self.inventory_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.inventory_pagination_next_button = CustomPushButton(ref='next_button')
        self.inventory_pagination_layout.addWidget(self.inventory_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_pagination_layout.addWidget(self.inventory_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_pagination_layout.addWidget(self.inventory_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_pagination.setLayout(self.inventory_pagination_layout)
        self.inventory_tab_layout = CustomGridLayout()
        self.inventory_tab_layout.addWidget(self.inventory_table,0,0)
        self.inventory_tab_layout.addWidget(self.inventory_pagination,1,0,Qt.AlignmentFlag.AlignCenter)
        self.inventory_tab = CustomWidget() 
        self.inventory_tab.setLayout(self.inventory_tab_layout) 
        # endregion: inventory pagination table
        # region: manage data buttons
        self.tab_sort_action_menu = CustomWidget(ref='tab_sort_action_menu')
        self.tab_sort_action_menu_layout = CustomHBoxLayout()
        self.refresh_button = CustomPushButton(ref='refresh_button')
        self.delete_all_button = CustomPushButton(ref='delete_all_button')
        self.import_button = CustomPushButton(ref='import_button')
        self.add_button = CustomPushButton(ref='add_button')
        self.tab_sort_action_menu_layout.addWidget(self.refresh_button)
        self.tab_sort_action_menu_layout.addWidget(self.delete_all_button)
        self.tab_sort_action_menu_layout.addWidget(self.import_button)
        self.tab_sort_action_menu_layout.addWidget(self.add_button)
        self.tab_sort_action_menu.setLayout(self.tab_sort_action_menu_layout)
        # endregion: manage data buttons
        # region: tab layout setup
        self.tab_sort = CustomTabWidget(ref='tab_sort')
        self.tab_sort.addTab(self.overview_tab, 'Overview')
        self.tab_sort.addTab(self.primary_tab, 'Primary')
        self.tab_sort.addTab(self.category_tab, 'Category')
        self.tab_sort.addTab(self.price_tab, 'Price')
        self.tab_sort.addTab(self.inventory_tab, 'Inventory')
        self.tab_sort.setCornerWidget(self.tab_sort_action_menu, Qt.Corner.BottomRightCorner)
        # endregion: tab layout setup

        self.panel_a_box_layout.addWidget(self.filter_field,0,0)
        self.panel_a_box_layout.addWidget(self.tab_sort,1,0)

        self.panel_a_box.setLayout(self.panel_a_box_layout)
        pass
        
        self.call_signal(signal_ref='panel_a_signal')

    def show_main_panel(self):
        self.show_panel_a()
        self.show_panel_b()

        grid_layout = CustomGridLayout()
        grid_layout.addWidget(self.panel_a_box,0,0)
        grid_layout.addWidget(self.panel_b_box,0,1)

        self.setLayout(grid_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagementLayout()
    window.show()
    sys.exit(pos_app.exec())
