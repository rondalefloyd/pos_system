import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.csv_importer import *
from database.product import *
from widget.product import *

class ProductWindow(MyWidget):
    def __init__(self):
        super().__init__(widget_ref='product_window')

        self.product_schema = ProductSchema()

        self.show_main_panel()
        self.default_values()
        self.on_refresh_data_button_clicked()

    # region -- passive functions
    def default_values(self):
        self.current_page = 1

        self.clicked_edit_button = None
        self.clicked_view_button = None
        self.clicked_delete_button = None

        # region -- [editable] -- setStyleSheet for required fields
        self.item_name_field.setStyleSheet('QLineEdit { border: 1px solid orange }')
        self.brand_field.setStyleSheet('QComboBox { border: 1px solid orange }')
        self.supplier_field.setStyleSheet('QComboBox { border: 1px solid orange }')
        self.cost_field.setStyleSheet('QLineEdit { border: 1px solid orange }')
        self.sell_price_field.setStyleSheet('QLineEdit { border: 1px solid orange }')

        self.available_stock_field.setStyleSheet('QLineEdit { border: 1px solid orange }')
        self.on_hand_stock_field.setStyleSheet('QLineEdit { border: 1px solid orange }')
        # endregion -- [editable] -- setStyleSheet for required fields
        pass
    def refresh_ui(self):
        self.current_page = 1

        self.clicked_edit_button = None
        self.clicked_view_button = None
        self.clicked_delete_button = None

        self.total_product_count.setText(f'Total product: {self.product_schema.count_product()}')
        self.overview_pagination_page.setText(f'Page {self.current_page}')

        self.populate_table()
        self.populate_combo_box()
        self.on_add_data_button_clicked() if self.manage_data_panel.isVisible() == True else None
    # endregion -- passive functions
        
    # region -- on_push_button_clicked functions
    def on_edit_button_clicked(self, row_value, edit_button):
        self.manage_data_panel.show()
        self.add_data_button.setDisabled(False)
        self.save_edit_button.show()
        self.save_new_button.hide()

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        edit_button.setDisabled(True)

        # region -- set values
        self.product_name_field.setText(str(row_value[0]))
        self.product_type_field.setCurrentText(str(row_value[1]))
        self.discount_percent_field.setText(str(row_value[2]))
        self.description_field.setPlainText(str(row_value[3]))
        self.selected_product_id = str(row_value[5])
        # endregion -- set values

        self.clicked_edit_button = edit_button
        pass
    def on_view_button_clicked(self, row_value, view_button):
        self.clicked_view_button.setDisabled(False) if self.clicked_view_button else None
        view_button.setDisabled(True)
        self.clicked_view_button = view_button

        # region -- view_panel_dialog = MyDialog()
        view_panel_dialog = MyDialog(dialog_ref='view_panel_dialog', parent=self)
        view_panel_layout = MyFormLayout()
        product_name_value = MyLabel(text=f'{row_value[0]}')
        product_type_value = MyLabel(text=f'{row_value[1]}')
        discount_percent_value = MyLabel(text=f'{row_value[2]}')
        description_value = MyLabel(text=f'{row_value[3]}')
        date_created_value = MyLabel(text=f'{row_value[4]}')

        view_panel_layout.addRow('Product name: ', product_name_value)
        view_panel_layout.addRow('Product type: ', product_type_value)
        view_panel_layout.addRow('Discount percent: ', discount_percent_value)
        view_panel_layout.addRow('Description: ', description_value)
        view_panel_layout.addRow(QLabel('<hr>'))
        view_panel_layout.addRow('Date created: ', date_created_value)
        view_panel_dialog.setLayout(view_panel_layout)
        view_panel_dialog.exec()
        # endregion -- view_panel_dialog = MyDialog()

        self.clicked_view_button.setDisabled(False) if view_panel_dialog.isVisible() == False else None

        pass
    def on_delete_button_clicked(self, row_value, delete_button):
        self.clicked_delete_button.setDisabled(False) if self.clicked_delete_button else None
        delete_button.setDisabled(True)
        self.clicked_delete_button = delete_button

        # region -- confirmation_a = QMessageBox.warning()
        confirmation_a = QMessageBox.warning(self, 'Confirm', f'Are you sure you want to delete {row_value[0]}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation_a == QMessageBox.StandardButton.Yes:
            selected_product_id = str(row_value[5])
            self.product_schema.delete_selected_product(selected_product_id)
            self.refresh_ui()
        # endregion -- confirmation_a = QMessageBox.warning()

        self.clicked_delete_button.setDisabled(False) if self.clicked_delete_button else None
        self.clicked_delete_button = None

        pass

    def on_discard_button_clicked(self):
        self.add_data_button.setDisabled(False)
        self.manage_data_panel.hide()

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None

        self.clicked_edit_button = None
        pass
    def on_save_new_button_clicked(self):
        try:
            if '' in [
                self.item_name_field.text(),
                self.brand_field.currentText(),
                self.sales_group_field.currentText(),
                self.supplier_field.currentText(),
                self.cost_field.text(),
                self.sell_price_field.text(),
            ]:
                QMessageBox.critical(self, 'Error', 'Must fill all required fields.')
                pass
            else:
                barcode = str(self.barcode_field.text())
                item_name = str(self.item_name_field.text())
                expire_dt = self.expire_dt_field.date().toString(Qt.DateFormat.ISODate)

                item_type = str(self.item_type_field.currentText())
                brand = str(self.brand_field.currentText())
                sales_group = str(self.sales_group_field.currentText())
                supplier = str(self.supplier_field.currentText())

                cost = str(self.cost_field.text())
                sell_price = str(self.sell_price_field.text())
                effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)
                promo_name = str(self.promo_name_field.currentText())
                promo_type = str(self.promo_type_field.text())
                discount_percent = str(self.discount_percent_field.text())
                discount_value = str(self.discount_value_field.text())
                new_sell_price = str(self.new_sell_price_field.text())
                start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
                end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)

                inventory_tracking = str(self.inventory_tracking_field.currentText())
                available_stock = str(self.available_stock_field.text())
                on_hand_stock = str(self.on_hand_stock_field.text())

                self.product_schema.add_new_product(
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
                )

                QMessageBox.information(self, 'Success', 'New product added.')
                self.refresh_ui()
            pass
        except Exception as error:
            QMessageBox.critical(self, 'Error', f'{error}')
            pass
        pass
    def on_save_edit_button_clicked(self):
        try:
            if '' in [
                self.product_name_field.text(),
                self.product_type_field.currentText(),
                self.discount_percent_field.text()
            ]:
                QMessageBox.critical(self, 'Error', 'Must fill all required fields.')
                pass
            else:
                product_name = str(self.product_name_field.text())
                product_type = str(self.product_type_field.currentText())
                discount_percent = str(self.discount_percent_field.text())
                description = str(self.description_field.toPlainText())
                product_id = str(self.selected_product_id)

                self.product_schema.edit_selected_product(
                    product_name=product_name,
                    product_type=product_type,
                    discount_percent=discount_percent,
                    description=description,
                    product_id=product_id
                )

                QMessageBox.information(self, 'Success', 'New product added.')
            pass
        except Exception as error:
            QMessageBox.critical(self, 'Error', f'{error}')
            pass
        self.refresh_ui()
        pass

    def on_pagination_prev_button_clicked(self):
        self.on_add_data_button_clicked() if self.manage_data_panel.isVisible() == True else None
        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        
        # region -- if self.current_page > 1:
        if self.current_page > 1:
            self.current_page -= 1
            self.overview_pagination_page.setText(f'Page {self.current_page}')
            self.primary_pagination_page.setText(f'Page {self.current_page}')
            self.category_pagination_page.setText(f'Page {self.current_page}')
            self.price_pagination_page.setText(f'Page {self.current_page}')
            self.inventory_pagination_page.setText(f'Page {self.current_page}')

        self.populate_table(current_page=self.current_page)
        # endregion -- if self.current_page > 1:

        self.clicked_edit_button = None
        pass
    def on_pagination_next_button_clicked(self):
        self.on_add_data_button_clicked() if self.manage_data_panel.isVisible() == True else None
        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        
        # region -- self.current_page += 1
        self.current_page += 1

        self.overview_pagination_page.setText(f'Page {self.current_page}')
        self.primary_pagination_page.setText(f'Page {self.current_page}')
        self.category_pagination_page.setText(f'Page {self.current_page}')
        self.price_pagination_page.setText(f'Page {self.current_page}')
        self.inventory_pagination_page.setText(f'Page {self.current_page}')
        
        self.populate_table(current_page=self.current_page)
        # endregion -- self.current_page += 1
        
        self.clicked_edit_button = None
        pass
    
    def on_refresh_data_button_clicked(self):
        self.refresh_ui()
        pass
    def on_import_data_button_clicked(self):
        self.import_data_button.setDisabled(True)

        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')

        print(csv_file)
        if csv_file:
            data_frame = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)
            
            self.import_thread = ProductCSVImporter(
                csv_file=csv_file,
                refresh_data_button=self.refresh_data_button,
                import_data_button=self.import_data_button
            )
            self.import_thread.progress_signal.connect(self.import_thread.update_progress)
            self.import_thread.finished_signal.connect(self.import_thread.import_finished)
            self.import_thread.finished_signal.connect(self.refresh_ui)
            self.import_thread.error_signal.connect(self.import_thread.import_error)
            self.import_thread.start()

            # print(data_frame)
            pass
        else:
            self.import_data_button.setDisabled(False)
        pass
    def on_add_data_button_clicked(self):
        self.add_data_button.setDisabled(True)
        self.manage_data_panel.show()
        self.save_edit_button.hide()
        self.save_new_button.show()

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None

        # region -- [editable] -- assign default values
        self.barcode_field.setText('')
        self.item_name_field.setText('')
        self.expire_dt_field.setDate(QDate.currentDate())

        self.item_type_field.setCurrentText('')
        self.brand_field.setCurrentText('')
        self.sales_group_field.setCurrentText('')
        self.supplier_field.setCurrentText('')

        self.cost_field.setText('')
        self.sell_price_field.setText('')
        self.effective_dt_field.setDate(QDate.currentDate())
        self.promo_name_field.setCurrentText('')
        self.promo_type_field.setText('')
        self.discount_percent_field.setText('')
        self.discount_value_field.setText('')
        self.new_sell_price_field.setText('')
        self.start_dt_field.setDate(QDate.currentDate())
        self.end_dt_field.setDate(QDate.currentDate())

        self.inventory_tracking_field.setCurrentText('')
        self.available_stock_field.setText('')
        self.on_hand_stock_field.setText('')
        # endregion -- [editable] -- assign default values

        self.clicked_edit_button = None
        pass
    # endregion -- on_push_button_clicked functions
    # region -- [editable] -- form fields functions
    def on_item_name_field_text_changed(self):
        self.item_name_field.setStyleSheet('QLineEdit { border: 1px solid orange }' if self.item_name_field.text() == '' else 'QLineEdit { border: 1px solid green }') # add this if this field is required
        pass
    def on_brand_field_current_text_changed(self):
        self.brand_field.setStyleSheet('QComboBox { border: 1px solid orange }' if self.brand_field.currentText() == '' else 'QComboBox { border: 1px solid green }') # add this if this field is required
        pass
    def on_supplier_field_current_text_changed(self):
        self.supplier_field.setStyleSheet('QComboBox { border: 1px solid orange }' if self.supplier_field.currentText() == '' else 'QComboBox { border: 1px solid green }') # add this if this field is required
        pass
    def on_cost_field_text_changed(self):
        self.cost_field.setStyleSheet('QLineEdit { border: 1px solid orange }' if self.cost_field.text() == '' else 'QLineEdit { border: 1px solid green }') # add this if this field is required
        pass
    def on_sell_price_field_text_changed(self):
        self.sell_price_field.setStyleSheet('QLineEdit { border: 1px solid orange }' if self.sell_price_field.text() == '' else 'QLineEdit { border: 1px solid green }') # add this if this field is required
        
        try:
            sell_price = float(self.sell_price_field.text())
            discount_percent = float(self.discount_percent_field.text())

            old_sell_price = sell_price
            discount_value = old_sell_price * (discount_percent / 100)
            new_sell_price = sell_price - discount_value

            self.discount_value_field.setText(f'{discount_value:.2f}')
            self.new_sell_price_field.setText(f'{new_sell_price:.2f}')
            pass
        except ValueError:
            print('error')
            self.discount_value_field.setText('Error')
            self.new_sell_price_field.setText('Error')
            pass
        pass
    
    def on_promo_name_field_current_text_changed(self):
        if self.promo_name_field.currentText() == 'No promo':
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
            pass
        elif self.promo_name_field.currentText() != 'No promo':
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

            # region -- populate promo_type_field and discount_percent_field
            data = self.product_schema.list_promo_type_and_discount_percent(self.promo_name_field.currentText())

            for row in data:
                self.promo_type_field.setText(str(row[0]))
                self.discount_percent_field.setText(str(row[1]))
            # endregion -- populate promo_type_field and discount_percent_field

        # region -- compute new sell price and discount value
        try:
            sell_price = float(self.sell_price_field.text())
            discount_percent = float(self.discount_percent_field.text())

            old_sell_price = sell_price
            discount_value = old_sell_price * (discount_percent / 100)
            new_sell_price = sell_price - discount_value

            self.discount_value_field.setText(f'{discount_value:.2f}')
            self.new_sell_price_field.setText(f'{new_sell_price:.2f}')
            pass
        except ValueError:
            print('error')
            self.discount_value_field.setText('Error')
            self.new_sell_price_field.setText('Error')
        # endregion -- compute new sell price and discount value
            pass
        pass
    def on_inventory_tracking_field_current_text_changed(self):
        if self.inventory_tracking_field.currentText() == 'Disabled':
            self.available_stock_label.hide()
            self.on_hand_stock_label.hide()
            
            self.available_stock_field.hide()
            self.on_hand_stock_field.hide()

            self.available_stock_field.setText('0')
            self.on_hand_stock_field.setText('0')

        elif self.inventory_tracking_field.currentText() == 'Enabled':
            self.available_stock_label.show()
            self.on_hand_stock_label.show()
            
            self.available_stock_field.show()
            self.on_hand_stock_field.show()

            self.available_stock_field.setText('')
            self.on_hand_stock_field.setText('')
        pass

    def on_available_stock_field_text_changed(self):
        self.available_stock_field.setStyleSheet('QLineEdit { border: 1px solid orange }' if self.available_stock_field.text() == '' else 'QLineEdit { border: 1px solid green }') # add this if this field is required
        pass
    def on_on_hand_stock_field_text_changed(self):
        self.on_hand_stock_field.setStyleSheet('QLineEdit { border: 1px solid orange }' if self.on_hand_stock_field.text() == '' else 'QLineEdit { border: 1px solid green }') # add this if this field is required
        
        pass
    # !!! checkpoint -- !!!!
    # endregion -- [editable] -- form fields functions
    # region -- filter field function
    def on_filter_field_text_changed(self):
        self.populate_table(text_filter=self.filter_field.text())
    # endregion -- filter field function
    
    # region -- populator functions
    def populate_combo_box(self):
        # region -- [editable]
        self.item_type_field.clear()
        self.brand_field.clear()
        self.supplier_field.clear()
        self.promo_name_field.clear()
        
        item_type_data = self.product_schema.list_item_type()
        brand_data = self.product_schema.list_brand()
        supplier_data = self.product_schema.list_supplier()
        promo_name_data = self.product_schema.list_promo()
        
        for item_type in item_type_data: self.item_type_field.addItem(item_type[0])
        for brand in brand_data: self.brand_field.addItem(brand[0])
        for supplier in supplier_data: self.supplier_field.addItem(supplier[0])

        self.promo_name_field.insertItem(0, 'No promo')
        for promo_name in promo_name_data: self.promo_name_field.addItem(promo_name[0])
        # endregion -- [editable]
        pass
    def populate_table(self, text_filter='', current_page=1):
        self.overview_table.clearContents()
        product_data = self.product_schema.list_product(text_filter=text_filter, page_number=current_page)
        
        # region -- pagination_button.setEnabled()
        self.overview_pagination_prev_button.setEnabled(self.current_page > 1)
        self.overview_pagination_next_button.setEnabled(len(product_data) == 30)
        # endregion -- pagination_button.setEnabled()

        # region -- self.clicked_edit_button.setDisabled()
        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        self.clicked_edit_button = None
        # endregion -- self.clicked_edit_button.setDisabled()
        
        self.overview_table.setRowCount(len(product_data))

        for row_index, row_value in enumerate(product_data):
            # region -- assign values

            # region -- action_nav = MyGroupBox()
            action_nav = MyWidget()
            action_nav_layout = MyHBoxLayout(hbox_layout_ref='action_nav_layout')
            self.edit_button = MyPushButton(push_button_ref='edit_button', text='Edit')
            self.edit_button.clicked.connect(lambda _, row_value=row_value, edit_button=self.edit_button: self.on_edit_button_clicked(row_value, edit_button))
            self.view_button = MyPushButton(push_button_ref='view_button', text='View')
            self.view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.view_button: self.on_view_button_clicked(row_value, view_button))
            self.delete_button = MyPushButton(push_button_ref='delete_button', text='Delete')
            self.delete_button.clicked.connect(lambda _, row_value=row_value, delete_button=self.delete_button: self.on_delete_button_clicked(row_value, delete_button))
            action_nav_layout.addWidget(self.edit_button)
            action_nav_layout.addWidget(self.view_button)
            action_nav_layout.addWidget(self.delete_button)
            action_nav.setLayout(action_nav_layout)
            # endregion -- action_nav = MyGroupBox()

            # region -- [editable] -- MyTableWidgetItem
            barcode = MyTableWidgetItem(table_widget_item_ref='barcode', text=str(row_value[0]))
            item_name = MyTableWidgetItem(table_widget_item_ref='item_name', text=str(row_value[1]))
            expire_dt = MyTableWidgetItem(table_widget_item_ref='expire_dt', text=str(row_value[2]))

            item_type = MyTableWidgetItem(table_widget_item_ref='item_type', text=str(row_value[3]))
            brand = MyTableWidgetItem(table_widget_item_ref='brand', text=str(row_value[4]))
            sales_group = MyTableWidgetItem(table_widget_item_ref='sales_group', text=str(row_value[5]))
            supplier = MyTableWidgetItem(table_widget_item_ref='supplier', text=str(row_value[6]))

            cost = MyTableWidgetItem(table_widget_item_ref='cost', text=str(f'₱{row_value[7]}'))
            sell_price = MyTableWidgetItem(table_widget_item_ref='sell_price', text=str(f'₱{row_value[8]}'))
            effective_dt = MyTableWidgetItem(table_widget_item_ref='effective_dt', text=str(row_value[9]))
            promo_name = MyTableWidgetItem(table_widget_item_ref='promo_name', text=str(row_value[10]))
            discount_value = MyTableWidgetItem(table_widget_item_ref='discount_value', text=str(f'₱{row_value[11]}'))

            inventory_tracking = MyTableWidgetItem(table_widget_item_ref='inventory_tracking', text=str(row_value[12]))
            available_stock = MyTableWidgetItem(table_widget_item_ref='available_stock', text=str(row_value[13]))
            on_hand_stock = MyTableWidgetItem(table_widget_item_ref='on_hand_stock', text=str(row_value[14]))

            update_ts = MyTableWidgetItem(table_widget_item_ref='update_ts', text=str(row_value[15]))
            # endregion -- [editable] -- MyTableWidgetItem
           
            # endregion -- assign values
            
            # region -- setItem/setCellWidget

            self.overview_table.setCellWidget(row_index, 0, action_nav)

            # region -- [editable] -- cell items
            self.overview_table.setItem(row_index, 1, item_name)
            self.overview_table.setItem(row_index, 2, update_ts)
            # endregion -- [editable] -- cell items

            # endregion -- setItem/setCellWidget

        pass
    # endregion -- populator functions

    # region -- panel_functions
    def show_operation_panel(self):
        self.operation_status_panel = MyGroupBox(group_box_ref='operation_status_panel')
        self.operation_status_layout = MyHBoxLayout(hbox_layout_ref='operation_status_layout')

        self.total_product_count = MyLabel(text=f'Total product: {self.product_schema.count_product()}')
        self.operation_status_layout.addWidget(self.total_product_count)
        self.operation_status_panel.setLayout(self.operation_status_layout)
        pass
    def show_manage_data_panel(self):
        self.manage_data_panel = MyGroupBox(group_box_ref='manage_data_panel')
        self.manage_data_panel_layout = MyVBoxLayout(vbox_layout_ref='manage_data_panel_layout')
        
        # region -- self.scrolling_manage_data_panel = MyScrollArea()
        self.scrolling_manage_data_panel = MyScrollArea(scroll_area_ref='scrolling_manage_data_panel')
        self.form_container = MyWidget()
        self.form_container_layout = MyFormLayout(form_layout_ref='form_container_layout')
        
        # region -- form = MyGroupBox()
        self.primary_form = MyGroupBox(group_box_ref='primary_form')
        self.category_form = MyGroupBox(group_box_ref='category_form')
        self.price_form = MyGroupBox(group_box_ref='price_form')
        self.inventory_form = MyGroupBox(group_box_ref='inventory_form')

        self.primary_form_layout = MyFormLayout()
        self.category_form_layout = MyFormLayout()
        self.price_form_layout = MyFormLayout()
        self.inventory_form_layout = MyFormLayout()

        # region -- [editable] -- form label
        self.barcode_label = MyLabel(label_ref='barcode_label', text='Barcode:')
        self.item_name_label = MyLabel(label_ref='item_name_label', text='Item name:')
        self.expire_dt_label = MyLabel(label_ref='expire_dt_label', text='Expire date:')

        self.item_type_label = MyLabel(label_ref='item_type_label', text='Item type:')
        self.brand_label = MyLabel(label_ref='brand_label', text='Brand:')
        self.sales_group_label = MyLabel(label_ref='sales_group_label', text='Sales group:')
        self.supplier_label = MyLabel(label_ref='supplier_label', text='Supplier:')

        self.cost_label = MyLabel(label_ref='cost_label', text='Cost:')
        self.sell_price_label = MyLabel(label_ref='sell_price_label', text='Sell price:')
        self.effective_dt_label = MyLabel(label_ref='effective_dt_label', text='Effective date:')
        self.promo_name_label = MyLabel(label_ref='promo_name_label', text='Promo name:')
        self.promo_type_label = MyLabel(label_ref='promo_type_label', text='Promo type:')
        self.discount_percent_label = MyLabel(label_ref='discount_percent_label', text='Discount percent:')
        self.discount_value_label = MyLabel(label_ref='discount_value_label', text='Discount value:')
        self.new_sell_price_label = MyLabel(label_ref='new_sell_price_label', text='New_sell price:')
        self.start_dt_label = MyLabel(label_ref='start_dt_label', text='Start date:')
        self.end_dt_label = MyLabel(label_ref='end_dt_label', text='End date:')

        self.inventory_tracking_label = MyLabel(label_ref='inventory_tracking_label', text='Inventory tracking:')
        self.available_stock_label = MyLabel(label_ref='available_stock_label', text='Available stock:')
        self.on_hand_stock_label = MyLabel(label_ref='on_hand_stock_label', text='On hand stock:')
        # endregion -- [editable] -- form label
        # region -- [editable] -- form field
        self.barcode_field = MyLineEdit(line_edit_ref='barcode_field')
        self.item_name_field = MyLineEdit(line_edit_ref='item_name_field')
        self.expire_dt_field = MyDateEdit(date_edit_ref='expire_dt_field')

        self.item_type_field = MyComboBox(combo_box_ref='item_type_field')
        self.brand_field = MyComboBox(combo_box_ref='brand_field')
        self.sales_group_field = MyComboBox(combo_box_ref='sales_group_field')
        self.supplier_field = MyComboBox(combo_box_ref='supplier_field')

        self.cost_field = MyLineEdit(line_edit_ref='cost_field')
        self.sell_price_field = MyLineEdit(line_edit_ref='sell_price_field')
        self.effective_dt_field = MyDateEdit(date_edit_ref='effective_dt_field')
        self.promo_name_field = MyComboBox(combo_box_ref='promo_name_field')
        self.promo_type_field = MyLineEdit(line_edit_ref='promo_type_field')
        self.discount_percent_field = MyLineEdit(line_edit_ref='discount_percent_field')
        self.discount_value_field = MyLineEdit(line_edit_ref='discount_value_field')
        self.new_sell_price_field = MyLineEdit(line_edit_ref='new_sell_price_field')
        self.start_dt_field = MyDateEdit(date_edit_ref='start_dt_field')
        self.end_dt_field = MyDateEdit(date_edit_ref='end_dt_field')

        self.inventory_tracking_field = MyComboBox(combo_box_ref='inventory_tracking_field')
        self.available_stock_field = MyLineEdit(line_edit_ref='available_stock_field')
        self.on_hand_stock_field = MyLineEdit(line_edit_ref='on_hand_stock_field')
        # endregion -- [editable] -- form field
        # region -- [editable] -- form field signals
        self.item_name_field.textChanged.connect(self.on_item_name_field_text_changed)
 
        self.item_name_field.textChanged.connect(self.on_item_name_field_text_changed)
        self.brand_field.currentTextChanged.connect(self.on_brand_field_current_text_changed)
        self.supplier_field.currentTextChanged.connect(self.on_supplier_field_current_text_changed)

        self.cost_field.textChanged.connect(self.on_cost_field_text_changed)
        self.sell_price_field.textChanged.connect(self.on_sell_price_field_text_changed)

        self.promo_name_field.currentTextChanged.connect(self.on_promo_name_field_current_text_changed)

        self.inventory_tracking_field.currentTextChanged.connect(self.on_inventory_tracking_field_current_text_changed)
        self.available_stock_field.textChanged.connect(self.on_available_stock_field_text_changed)
        self.on_hand_stock_field.textChanged.connect(self.on_on_hand_stock_field_text_changed)
        # endregion -- [editable] -- form field signals

        # region -- [editable] -- form addRow
        self.primary_form_layout.addRow(MyLabel(text='<b>Primary Information</b>'))
        self.primary_form_layout.addRow(MyLabel(text='<hr>'))
        self.primary_form_layout.addRow(self.barcode_label, self.barcode_field)
        self.primary_form_layout.addRow(self.item_name_label, self.item_name_field)
        self.primary_form_layout.addRow(self.expire_dt_label, self.expire_dt_field)

        self.category_form_layout.addRow(MyLabel(text='<b>Category</b>'))
        self.category_form_layout.addRow(MyLabel(text='<hr>'))
        self.category_form_layout.addRow(self.item_type_label, self.item_type_field)
        self.category_form_layout.addRow(self.brand_label, self.brand_field)
        self.category_form_layout.addRow(self.sales_group_label, self.sales_group_field)
        self.category_form_layout.addRow(self.supplier_label, self.supplier_field)

        self.price_form_layout.addRow(MyLabel(text='<b>Price</b>'))
        self.price_form_layout.addRow(MyLabel(text='<hr>'))
        self.price_form_layout.addRow(self.cost_label, self.cost_field)
        self.price_form_layout.addRow(self.sell_price_label, self.sell_price_field)
        self.price_form_layout.addRow(self.effective_dt_label, self.effective_dt_field)
        self.price_form_layout.addRow(self.promo_name_label, self.promo_name_field)
        self.price_form_layout.addRow(self.promo_type_label, self.promo_type_field)
        self.price_form_layout.addRow(self.discount_percent_label, self.discount_percent_field)
        self.price_form_layout.addRow(self.discount_value_label, self.discount_value_field)
        self.price_form_layout.addRow(self.new_sell_price_label, self.new_sell_price_field)
        self.price_form_layout.addRow(self.start_dt_label, self.start_dt_field)
        self.price_form_layout.addRow(self.end_dt_label, self.end_dt_field)

        self.inventory_form_layout.addRow(MyLabel(text='<b>Inventory</b>'))
        self.inventory_form_layout.addRow(MyLabel(text='<hr>'))
        self.inventory_form_layout.addRow(self.inventory_tracking_label, self.inventory_tracking_field)
        self.inventory_form_layout.addRow(self.available_stock_label, self.available_stock_field)
        self.inventory_form_layout.addRow(self.on_hand_stock_label, self.on_hand_stock_field)
        # endregion -- [editable] -- form addRow

        self.primary_form.setLayout(self.primary_form_layout)
        self.category_form.setLayout(self.category_form_layout)
        self.price_form.setLayout(self.price_form_layout)
        self.inventory_form.setLayout(self.inventory_form_layout)
        # endregion -- form = MyGroupBox()
        
        self.form_container_layout.addRow(self.primary_form)
        self.form_container_layout.addRow(self.category_form)
        self.form_container_layout.addRow(self.price_form)
        self.form_container_layout.addRow(self.inventory_form)
        self.form_container.setLayout(self.form_container_layout)
        self.scrolling_manage_data_panel.setWidget(self.form_container)
        # endregion -- self.scrolling_manage_data_panel = MyScrollArea()

        # region -- self.form_nav = MyGroupBox()
        self.form_nav = MyGroupBox(group_box_ref='form_nav')
        self.form_nav_layout = MyGridLayout()
        self.discard_button = MyPushButton(text='Discard')
        self.discard_button.clicked.connect(self.on_discard_button_clicked)
        self.save_new_button = MyPushButton(push_button_ref='save_new_button', text='SAVE')
        self.save_new_button.clicked.connect(self.on_save_new_button_clicked)
        self.save_edit_button = MyPushButton(push_button_ref='save_edit_button', text='SAVE')
        self.save_edit_button.clicked.connect(self.on_save_edit_button_clicked)
        self.form_nav_layout.addWidget(self.discard_button,0,0)
        self.form_nav_layout.addWidget(self.save_new_button,0,1)
        self.form_nav_layout.addWidget(self.save_edit_button,0,1)
        self.form_nav.setLayout(self.form_nav_layout)
        # endregion -- self.form_nav = MyGroupBox()

        self.manage_data_panel_layout.addWidget(self.scrolling_manage_data_panel)
        self.manage_data_panel_layout.addWidget(self.form_nav)
        self.manage_data_panel.setLayout(self.manage_data_panel_layout)
        pass
    def show_content_panel(self):
        self.content_panel = MyGroupBox(group_box_ref='content_panel')
        self.content_panel_layout = MyGridLayout(grid_layout_ref='content_panel_layout')

        self.filter_field = MyLineEdit(line_edit_ref='filter_field')
        self.filter_field.textChanged.connect(self.on_filter_field_text_changed)

        # region -- self.manage_data_nav = MyGroupBox()
        self.manage_data_nav = MyWidget(widget_ref='manage_data_nav')
        self.manage_data_layout = MyHBoxLayout(hbox_layout_ref='manage_data_layout')
        self.refresh_data_button = MyPushButton(push_button_ref='refresh_data_button', text='Refresh')
        self.import_data_button = MyPushButton(push_button_ref='import_data_button', text='Import')
        self.add_data_button = MyPushButton(push_button_ref='add_data_button', text='Add')
        self.manage_data_layout.addWidget(self.refresh_data_button)
        self.manage_data_layout.addWidget(self.import_data_button)
        self.manage_data_layout.addWidget(self.add_data_button)
        self.manage_data_nav.setLayout(self.manage_data_layout)
        # endregion -- self.manage_data_nav = MyGroupBox()

        self.table_sorter = MyTabWidget(tab_widget_ref='table_sorter')

        self.overview_table = MyTableWidget(table_widget_ref='overview_table')
        self.primary_table = MyTableWidget(table_widget_ref='primary_table')
        self.category_table = MyTableWidget(table_widget_ref='category_table')
        self.price_table = MyTableWidget(table_widget_ref='price_table')
        self.inventory_table = MyTableWidget(table_widget_ref='inventory_table')

        self.overview_pagination = MyGroupBox(group_box_ref='overview_pagination')
        self.primary_pagination = MyGroupBox(group_box_ref='primary_pagination')
        self.category_pagination = MyGroupBox(group_box_ref='category_pagination')
        self.price_pagination = MyGroupBox(group_box_ref='price_pagination')
        self.inventory_pagination = MyGroupBox(group_box_ref='inventory_pagination')

        self.overview_pagination_layout = MyGridLayout(grid_layout_ref='overview_pagination_layout')
        self.primary_pagination_layout = MyGridLayout(grid_layout_ref='primary_pagination_layout')
        self.category_pagination_layout = MyGridLayout(grid_layout_ref='category_pagination_layout')
        self.price_pagination_layout = MyGridLayout(grid_layout_ref='price_pagination_layout')
        self.inventory_pagination_layout = MyGridLayout(grid_layout_ref='inventory_pagination_layout')

        self.overview_pagination_container = MyGroupBox(group_box_ref='overview_pagination_container')
        self.primary_pagination_container = MyGroupBox(group_box_ref='primary_pagination_container')
        self.category_pagination_container = MyGroupBox(group_box_ref='category_pagination_container')
        self.price_pagination_container = MyGroupBox(group_box_ref='price_pagination_container')
        self.inventory_pagination_container = MyGroupBox(group_box_ref='inventory_pagination_container')

        self.overview_pagination_container_layout = MyGridLayout(grid_layout_ref='overview_pagination_container_layout')
        self.primary_pagination_container_layout = MyGridLayout(grid_layout_ref='primary_pagination_container_layout')
        self.category_pagination_container_layout = MyGridLayout(grid_layout_ref='category_pagination_container_layout')
        self.price_pagination_container_layout = MyGridLayout(grid_layout_ref='price_pagination_container_layout')
        self.inventory_pagination_container_layout = MyGridLayout(grid_layout_ref='inventory_pagination_container_layout')

        # region -- self.overview_pagination
        self.overview_pagination_nav = MyGroupBox(group_box_ref='overview_pagination_nav')
        self.overview_pagination_nav_layout = MyGridLayout()
        self.overview_pagination_prev_button = MyPushButton(text='Prev')
        self.overview_pagination_page = MyLabel('Page 1')
        self.overview_pagination_next_button = MyPushButton(text='Next')
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_prev_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_page,0,1,Qt.AlignmentFlag.AlignCenter)
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_nav.setLayout(self.overview_pagination_nav_layout)
        self.overview_pagination_container_layout.addWidget(self.overview_pagination_nav)
        self.overview_pagination_container.setLayout(self.overview_pagination_container_layout)

        self.overview_pagination_layout.addWidget(self.overview_table,0,0)
        self.overview_pagination_layout.addWidget(self.overview_pagination_container,1,0)

        self.overview_pagination.setLayout(self.overview_pagination_layout)
        # endregion -- self.overview_pagination
        # region -- self.primary_pagination
        
        self.primary_pagination_nav = MyGroupBox(group_box_ref='primary_pagination_nav')
        self.primary_pagination_nav_layout = MyGridLayout()
        self.primary_pagination_prev_button = MyPushButton(text='Prev')
        self.primary_pagination_page = MyLabel('Page 1')
        self.primary_pagination_next_button = MyPushButton(text='Next')
        self.primary_pagination_nav_layout.addWidget(self.primary_pagination_prev_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.primary_pagination_nav_layout.addWidget(self.primary_pagination_page,0,1,Qt.AlignmentFlag.AlignCenter)
        self.primary_pagination_nav_layout.addWidget(self.primary_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.primary_pagination_nav.setLayout(self.primary_pagination_nav_layout)
        self.primary_pagination_container_layout.addWidget(self.primary_pagination_nav)
        self.primary_pagination_container.setLayout(self.primary_pagination_container_layout)

        self.primary_pagination_layout.addWidget(self.primary_table,0,0)
        self.primary_pagination_layout.addWidget(self.primary_pagination_container,1,0)

        self.primary_pagination.setLayout(self.primary_pagination_layout)
        # endregion -- self.primary_pagination
        # region -- self.category_pagination
        
        self.category_pagination_nav = MyGroupBox(group_box_ref='category_pagination_nav')
        self.category_pagination_nav_layout = MyGridLayout()
        self.category_pagination_prev_button = MyPushButton(text='Prev')
        self.category_pagination_page = MyLabel('Page 1')
        self.category_pagination_next_button = MyPushButton(text='Next')
        self.category_pagination_nav_layout.addWidget(self.category_pagination_prev_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.category_pagination_nav_layout.addWidget(self.category_pagination_page,0,1,Qt.AlignmentFlag.AlignCenter)
        self.category_pagination_nav_layout.addWidget(self.category_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.category_pagination_nav.setLayout(self.category_pagination_nav_layout)
        self.category_pagination_container_layout.addWidget(self.category_pagination_nav)
        self.category_pagination_container.setLayout(self.category_pagination_container_layout)

        self.category_pagination_layout.addWidget(self.category_table,0,0)
        self.category_pagination_layout.addWidget(self.category_pagination_container,1,0)

        self.category_pagination.setLayout(self.category_pagination_layout)
        # endregion -- self.category_pagination
        # region -- self.price_pagination
        
        self.price_pagination_nav = MyGroupBox(group_box_ref='price_pagination_nav')
        self.price_pagination_nav_layout = MyGridLayout()
        self.price_pagination_prev_button = MyPushButton(text='Prev')
        self.price_pagination_page = MyLabel('Page 1')
        self.price_pagination_next_button = MyPushButton(text='Next')
        self.price_pagination_nav_layout.addWidget(self.price_pagination_prev_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.price_pagination_nav_layout.addWidget(self.price_pagination_page,0,1,Qt.AlignmentFlag.AlignCenter)
        self.price_pagination_nav_layout.addWidget(self.price_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.price_pagination_nav.setLayout(self.price_pagination_nav_layout)
        self.price_pagination_container_layout.addWidget(self.price_pagination_nav)
        self.price_pagination_container.setLayout(self.price_pagination_container_layout)

        self.price_pagination_layout.addWidget(self.price_table,0,0)
        self.price_pagination_layout.addWidget(self.price_pagination_container,1,0)

        self.price_pagination.setLayout(self.price_pagination_layout)
        # endregion -- self.price_pagination
        # region -- self.inventory_pagination
        
        self.inventory_pagination_nav = MyGroupBox(group_box_ref='inventory_pagination_nav')
        self.inventory_pagination_nav_layout = MyGridLayout()
        self.inventory_pagination_prev_button = MyPushButton(text='Prev')
        self.inventory_pagination_page = MyLabel('Page 1')
        self.inventory_pagination_next_button = MyPushButton(text='Next')
        self.inventory_pagination_nav_layout.addWidget(self.inventory_pagination_prev_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_pagination_nav_layout.addWidget(self.inventory_pagination_page,0,1,Qt.AlignmentFlag.AlignCenter)
        self.inventory_pagination_nav_layout.addWidget(self.inventory_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_pagination_nav.setLayout(self.inventory_pagination_nav_layout)
        self.inventory_pagination_container_layout.addWidget(self.inventory_pagination_nav)
        self.inventory_pagination_container.setLayout(self.inventory_pagination_container_layout)

        self.inventory_pagination_layout.addWidget(self.inventory_table,0,0)
        self.inventory_pagination_layout.addWidget(self.inventory_pagination_container,1,0)

        self.inventory_pagination.setLayout(self.inventory_pagination_layout)
        # endregion -- self.inventory_pagination
      
        # region -- self.table_sorter.addTab
        self.table_sorter.addTab(self.overview_pagination, 'Overview')
        self.table_sorter.addTab(self.primary_pagination, 'Primary')
        self.table_sorter.addTab(self.category_pagination, 'Category')
        self.table_sorter.addTab(self.price_pagination, 'Price')
        self.table_sorter.addTab(self.inventory_pagination, 'Inventory')
        # endregion -- self.table_sorter.addTab

        self.content_panel_layout.addWidget(self.filter_field,0,0)
        self.content_panel_layout.addWidget(self.manage_data_nav,0,1)
        self.content_panel_layout.addWidget(self.table_sorter,1,0,1,2)
        self.content_panel.setLayout(self.content_panel_layout)

        self.refresh_data_button.clicked.connect(self.on_refresh_data_button_clicked)
        self.import_data_button.clicked.connect(self.on_import_data_button_clicked)
        self.add_data_button.clicked.connect(self.on_add_data_button_clicked)

        self.overview_pagination_prev_button.clicked.connect(self.on_pagination_prev_button_clicked)
        self.overview_pagination_next_button.clicked.connect(self.on_pagination_next_button_clicked)

        self.primary_pagination_prev_button.clicked.connect(self.on_pagination_prev_button_clicked)
        self.primary_pagination_next_button.clicked.connect(self.on_pagination_next_button_clicked)

        self.category_pagination_prev_button.clicked.connect(self.on_pagination_prev_button_clicked)
        self.category_pagination_next_button.clicked.connect(self.on_pagination_next_button_clicked)

        self.price_pagination_prev_button.clicked.connect(self.on_pagination_prev_button_clicked)
        self.price_pagination_next_button.clicked.connect(self.on_pagination_next_button_clicked)

        self.inventory_pagination_prev_button.clicked.connect(self.on_pagination_prev_button_clicked)
        self.inventory_pagination_next_button.clicked.connect(self.on_pagination_next_button_clicked)

    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(grid_layout_ref='main_panel_layout')

        self.show_content_panel()
        self.show_manage_data_panel()
        self.show_operation_panel()

        self.main_panel_layout.addWidget(self.content_panel,0,0)
        self.main_panel_layout.addWidget(self.manage_data_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.operation_status_panel,1,0)
        self.setLayout(self.main_panel_layout)
    # endregion -- panel_functions
    
if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(pos_app.exec())
