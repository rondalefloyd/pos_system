import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.manual_csv_importer import *
from database.product import *
from widget.product import *

class ProductWindow(MyWidget):
    def __init__(self):
        super().__init__(widget_ref='product_window')

        self.product_schema = ProductSchema()

        self.show_main_panel()
        self.default_values()
        self.on_refresh_data_button_clicked()


    def default_values(self):

        self.current_page = 1

        self.clicked_edit_button = None
        self.clicked_view_button = None
        self.clicked_delete_button = None

        # checkpoint!!!
        
        pass

    # region -- on_push_button_clicked functions
    def on_edit_button_clicked(self, row_value, edit_button):
        self.scrolling_manage_data_panel.show()
        self.add_data_button.setDisabled(False)
        self.save_edit_button.show()
        self.save_new_button.hide()

        self.category_form.setDisabled(True)

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        edit_button.setDisabled(True)

        # region -- assign values to fields
        self.barcode_field.setText(str(row_value[0]))
        self.item_name_field.setText(str(row_value[1]))
        self.expire_dt_field.setDate(QDate.fromString(row_value[2], Qt.DateFormat.ISODate))

        self.item_type_field.setCurrentText(str(row_value[3]))
        self.brand_field.setCurrentText(str(row_value[4]))
        self.sales_group_field.setCurrentText(str(row_value[5]))
        self.supplier_field.setCurrentText(str(row_value[6]))

        self.cost_field.setText(str(row_value[7]))
        self.sell_price_field.setText(str(row_value[8]))
        self.effective_dt_field.setDate(QDate.fromString(row_value[9], Qt.DateFormat.ISODate))
        self.promo_name_field.setCurrentText(str(row_value[10]))

        self.inventory_tracking_field.setCurrentText(str(row_value[12]))
        self.available_stock_field.setText(str(row_value[13]))
        self.on_hand_stock_field.setText(str(row_value[14]))

        # WILL BE REVIEWED !!!!
        # region -- selected ids
        self.selected_item_id = int(row_value[16])
        self.selected_item_price_id = int(row_value[17])
        self.selected_promo_id = int(row_value[18])
        self.selected_stock_id = int(row_value[19])
        # endregion -- selected ids
        # endregion -- assign values to fields

        self.clicked_edit_button = edit_button
        pass
    def on_view_button_clicked(self, row_value, view_button):
        self.clicked_view_button.setDisabled(False) if self.clicked_view_button else None
        view_button.setDisabled(True)
        self.clicked_view_button = view_button

        # region -- view_panel_dialog = MyDialog()
        view_panel_dialog = MyDialog(dialog_ref='view_panel_dialog', parent=self)
        view_panel_layout = MyFormLayout()
        
        # region -- change display labels
        barcode_value = MyLabel(label_ref=f'{row_value[0]}')
        item_name_value = MyLabel(label_ref=f'{row_value[1]}')
        expire_dt_value = MyLabel(label_ref=f'{row_value[2]}')

        item_type_value = MyLabel(label_ref=f'{row_value[3]}')
        brand_value = MyLabel(label_ref=f'{row_value[4]}')
        sales_group_value = MyLabel(label_ref=f'{row_value[5]}')
        supplier_value = MyLabel(label_ref=f'{row_value[6]}')

        cost_value = MyLabel(label_ref=f'{row_value[7]}')
        sell_price_value = MyLabel(label_ref=f'{row_value[8]}')
        effective_dt_value = MyLabel(label_ref=f'{row_value[9]}')
        promo_name_value = MyLabel(label_ref=f'{row_value[10]}')

        inventory_tracking_value = MyLabel(label_ref=f'{row_value[12]}')
        available_stock_value = MyLabel(label_ref=f'{row_value[13]}')
        on_hand_stock_value = MyLabel(label_ref=f'{row_value[14]}')
        # endregion -- change display labels

        # region -- add label as rows
        view_panel_layout.addRow('Barcode', barcode_value)
        view_panel_layout.addRow('Item_name', item_name_value)
        view_panel_layout.addRow('Expire date', expire_dt_value)

        view_panel_layout.addRow('Item type', item_type_value)
        view_panel_layout.addRow('Brand', brand_value)
        view_panel_layout.addRow('Sales group', sales_group_value)
        view_panel_layout.addRow('Supplier', supplier_value)

        view_panel_layout.addRow('Cost', cost_value)
        view_panel_layout.addRow('Sell price', sell_price_value)
        view_panel_layout.addRow('Effective date', effective_dt_value)
        view_panel_layout.addRow('Promo name', promo_name_value)

        view_panel_layout.addRow('Inventory tracking', inventory_tracking_value)
        view_panel_layout.addRow('Available stock', available_stock_value)
        view_panel_layout.addRow('On hand stock', on_hand_stock_value)
        # endregion -- add label as rows

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
            selected_promo_id = str(row_value[5])
            selected_stock_id = str(row_value[5])
            selected_item_id = str(row_value[5])
            self.product_schema.delete_selected_product(selected_promo_id, selected_stock_id, selected_item_id)
        # endregion -- confirmation_a = QMessageBox.warning()

        self.clicked_delete_button.setDisabled(False) if self.clicked_delete_button else None
        self.clicked_delete_button = None

        pass

    def on_discard_button_clicked(self):
        self.add_data_button.setDisabled(False)
        self.scrolling_manage_data_panel.hide()

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None

        self.clicked_edit_button = None
        pass
    def on_save_new_button_clicked(self):
        try:
            # region -- get fields input
            barcode = str(self.barcode_field.text())
            item_name = str(self.item_name_field.text())
            expire_dt = self.expire_dt_field.date().toString(Qt.DateFormat.ISODate)

            item_type = str(self.item_type_field.currentText())
            brand = str(self.brand_field.currentText())
            sales_group = str(self.sales_group_field.currentText())
            supplier = str(self.supplier_field.currentText())

            cost = float(self.cost_field.text())
            sell_price = float(self.sell_price_field.text())
            effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)
            promo_name = str(self.promo_name_field.currentText())
            promo_type = str(self.promo_type_field.text())
            discount_percent = float(self.discount_percent_field.text())
            discount_value = float(self.discount_value_field.text())
            new_sell_price = float(self.new_sell_price_field.text())
            start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
            end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)

            inventory_tracking = str(self.inventory_tracking_field.currentText())
            available_stock = int(self.available_stock_field.text())
            on_hand_stock = int(self.on_hand_stock_field.text())
            # endregion -- get fields input

            if '' in [
                # region -- conditions
                item_name,
                brand,
                sales_group,
                supplier,
                cost,
                sell_price
                # endregion -- conditions
            ]:
                QMessageBox.critical(self, 'Error', 'Must fill all required fields.')
                pass
            else:
                self.product_schema.add_new_product(
                    # region -- params
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
                    # endregion -- params
                )

                QMessageBox.information(self, 'Success', 'New product added.')
            pass
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid numerical input.')
            pass
    def on_save_edit_button_clicked(self):
        try:
            # region -- get fields input
            barcode = str(self.barcode_field.text())
            item_name = str(self.item_name_field.text())
            expire_dt = self.expire_dt_field.date().toString(Qt.DateFormat.ISODate)

            item_type = str(self.item_type_field.currentText())
            brand = str(self.brand_field.currentText())
            sales_group = str(self.sales_group_field.currentText())
            supplier = str(self.supplier_field.currentText())

            cost = float(self.cost_field.text())
            sell_price = float(self.sell_price_field.text())
            effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)
            promo_name = str(self.promo_name_field.currentText())
            promo_type = str(self.promo_type_field.text())
            discount_percent = float(self.discount_percent_field.text())
            discount_value = float(self.discount_value_field.text())
            new_sell_price = float(self.new_sell_price_field.text())
            start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
            end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)

            inventory_tracking = str(self.inventory_tracking_field.currentText())
            available_stock = float(self.available_stock_field.text())
            on_hand_stock = float(self.on_hand_stock_field.text())

            item_id = int(self.selected_item_id)
            item_price_id = int(self.selected_item_price_id)
            promo_id = int(self.selected_promo_id)
            stock_id = int(self.selected_stock_id)
            # endregion -- get fields input

            if '' in [
                # region -- conditions
                item_name,
                brand,
                sales_group,
                supplier,
                cost,
                sell_price
                # endregion -- conditions
            ]:
                QMessageBox.critical(self, 'Error', 'Must fill all required fields.')
                pass
            else:
                self.product_schema.edit_selected_product(
                    # region -- params
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
                    # endregion -- params
                )

            QMessageBox.information(self, 'Success', 'New product added.')
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid numerical input.')
        pass

    def on_overview_pagination_prev_button_clicked(self):
        self.on_add_data_button_clicked() if self.scrolling_manage_data_panel.isVisible() == True else None
        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        
        # region -- if self.current_page > 1:
        if self.current_page > 1:
            self.current_page -= 1
            self.overview_pagination_page.setText(f'Page {self.current_page}')

        self.populate_table(current_page=self.current_page)
        # endregion -- if self.current_page > 1:

        self.clicked_edit_button = None
        pass
    def on_overview_pagination_next_button_clicked(self):
        self.on_add_data_button_clicked() if self.scrolling_manage_data_panel.isVisible() == True else None
        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        
        # region -- self.current_page += 1
        self.current_page += 1
        self.overview_pagination_page.setText(f'Page {self.current_page}')
        
        self.populate_table(current_page=self.current_page)
        # endregion -- self.current_page += 1
        
        self.clicked_edit_button = None
        pass

    def on_refresh_data_button_clicked(self):
        self.current_page = 1
        self.clicked_edit_button = None
        self.clicked_view_button = None
        self.clicked_delete_button = None

        self.populate_table()
        self.populate_combo_box()

        self.on_add_data_button_clicked() if self.scrolling_manage_data_panel.isVisible() == True else None

        self.total_product_count.setText(f'Total product: {self.product_schema.count_product()}')
        self.overview_pagination_page.setText(f'Page {self.current_page}')

            
        pass
    def on_delete_all_data_button_clicked(self):
        pass
    def on_import_data_button_clicked(self):
        self.import_data_button.setDisabled(True)

        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')

        print(csv_file)
        if csv_file:
            data_frame = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)
            
            self.import_thread = ManualPromoImport(
                csv_file=csv_file,
                import_data_button=self.import_data_button
            )
            self.import_thread.progress_signal.connect(self.import_thread.update_progress)
            self.import_thread.finished_signal.connect(self.import_thread.import_finished)
            self.import_thread.error_signal.connect(self.import_thread.import_error)
            self.import_thread.start()
            # print(data_frame)
            pass
        else:
            self.import_data_button.setDisabled(False)
        pass
    def on_add_data_button_clicked(self):
        self.add_data_button.setDisabled(True)
        self.scrolling_manage_data_panel.show()
        self.save_edit_button.hide()
        self.save_new_button.show()

        self.category_form.setDisabled(False)

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None

        # region -- assign values to fields
        self.barcode_field.setText('')
        self.item_name_field.setText('')
        self.expire_dt_field.setDate(QDate.currentDate())

        self.item_type_field.setCurrentText('')
        self.brand_field.setCurrentText('')
        self.sales_group_field.setCurrentText('')
        self.supplier_field.setCurrentText('')

        self.cost_field.setText(str(0))
        self.sell_price_field.setText(str(0))
        self.effective_dt_field.setDate(QDate.currentDate())
        self.promo_name_field.setCurrentText('No promo')
        self.promo_type_field.setText('')
        self.discount_percent_field.setText(str(0))
        self.discount_value_field.setText(str(0))
        self.new_sell_price_field.setText(str(0))
        self.start_dt_field.setDate(QDate.currentDate())
        self.end_dt_field.setDate(QDate.currentDate())

        self.inventory_tracking_field.setCurrentText('Disabled')
        self.available_stock_field.setText(str(0))
        self.on_hand_stock_field.setText(str(0))
        # endregion -- assign values to fields

        self.clicked_edit_button = None
        pass
    # endregion -- on_push_button_clicked functions
    # region -- on_combo_box_current_text_changed functions
    def on_promo_name_field_current_text_changed(self):
        if self.promo_name_field.currentText() == 'No promo':
            # region -- hide form labels and fields
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
            # endregion -- hide form labels and fields
        elif self.promo_name_field.currentText() != 'No promo':
            # region -- show form labels and fields
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
            # endregion -- show form labels and fields

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
    def on_inventory_tracking_field_current_text_changed(self):
        if self.inventory_tracking_field.currentText() == 'Disabled':
            # region -- hide form labels and fields
            self.available_stock_label.hide()
            self.on_hand_stock_label.hide()

            self.available_stock_field.hide()
            self.on_hand_stock_field.hide()
            # endregion -- hide form labels and fields
            pass
        elif self.inventory_tracking_field.currentText() == 'Enabled':
            # region -- hide form labels and fields
            self.available_stock_label.show()
            self.on_hand_stock_label.show()

            self.available_stock_field.show()
            self.on_hand_stock_field.show()
            # endregion -- hide form labels and fields
            pass
        pass
    # endregion -- on_combo_box_current_text_changed functions
    # region -- on_line_edit_text_changed functions
    def sell_price_field_text_changed(self):
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
            pass
        # endregion -- compute new sell price and discount value
    # endregion -- on_line_edit_text_changed functions

    def populate_combo_box(self):
        item_type_data = self.product_schema.list_item_type()
        brand_data = self.product_schema.list_brand()
        supplier_data = self.product_schema.list_supplier()
        promo_name_data = self.product_schema.list_promo()

        for item_type in item_type_data: self.item_type_field.addItem(item_type[0])
        for brand in brand_data: self.brand_field.addItem(brand[0])
        for supplier in supplier_data: self.supplier_field.addItem(supplier[0])
        for promo_name in promo_name_data: self.promo_name_field.addItem(promo_name[0])
        pass
    # checkpoint vvv
    def populate_table(self, current_page=1):
        product_data = self.product_schema.list_product(page_number=current_page)
        
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
            
            barcode = MyTableWidgetItem(table_widget_item_ref='barcode', text=f"{row_value[0]}")
            item_name = MyTableWidgetItem(table_widget_item_ref='item_name', text=f"{row_value[1]}")
            expire_dt = MyTableWidgetItem(table_widget_item_ref='expire_dt', text=f"{row_value[2]}")

            item_type = MyTableWidgetItem(table_widget_item_ref='item_type', text=f"{row_value[3]}")
            brand = MyTableWidgetItem(table_widget_item_ref='brand', text=f"{row_value[4]}")
            sales_group = MyTableWidgetItem(table_widget_item_ref='sales_group', text=f"{row_value[5]}")
            supplier = MyTableWidgetItem(table_widget_item_ref='supplier', text=f"{row_value[6]}")

            cost = MyTableWidgetItem(table_widget_item_ref='cost', text=f"₱{row_value[7]}")
            sell_price = MyTableWidgetItem(table_widget_item_ref='sell_price', text=f"₱{row_value[8]}")
            effective_dt = MyTableWidgetItem(table_widget_item_ref='effective_dt', text=f"{row_value[9]}")
            promo_name = MyTableWidgetItem(table_widget_item_ref='promo_name', text=f"{row_value[10]}")
            discount_value = MyTableWidgetItem(table_widget_item_ref='discount_value', text=f"₱{row_value[11]}")

            inventory_tracking = MyTableWidgetItem(table_widget_item_ref='inventory_tracking', text=f"{row_value[12]}")
            available_stock = MyTableWidgetItem(table_widget_item_ref='available_stock', text=f"{row_value[13]}")
            on_hand_stock = MyTableWidgetItem(table_widget_item_ref='on_hand_stock', text=f"{row_value[14]}")

            # endregion -- assign values

            self.overview_table.setCellWidget(row_index, 0, action_nav)
            self.overview_table.setItem(row_index, 1, item_name)
            self.overview_table.setItem(row_index, 2, brand)
            self.overview_table.setItem(row_index, 3, sell_price)
            self.overview_table.setItem(row_index, 4, promo_name)
            self.overview_table.setItem(row_index, 5, inventory_tracking)
        pass

    def show_operation_panel(self):
        self.operation_status_panel = MyGroupBox(group_box_ref='operation_status_panel')
        self.operation_status_layout = MyHBoxLayout(hbox_layout_ref='operation_status_layout')

        self.total_product_count = MyLabel(text=f'Total product: {self.product_schema.count_product()}')
        self.operation_status_layout.addWidget(self.total_product_count)
        self.operation_status_panel.setLayout(self.operation_status_layout)
        pass
    def show_manage_data_panel(self):
        self.scrolling_manage_data_panel = MyScrollArea(scroll_area_ref='scrolling_manage_data_panel')
        self.manage_data_panel = MyWidget(widget_ref='manage_data_panel')
        self.manage_data_panel_layout = MyFormLayout()
        
        # region -- form title labels
        self.primary_title_label = MyLabel(text='<b>Primary</b>')
        self.category_title_label = MyLabel(text='<b>Category</b>')
        self.price_title_label = MyLabel(text='<b>Price</b>')
        self.inventory_title_label = MyLabel(text='<b>Inventory</b>')
        # endregion -- form title labels

        # region -- form labels
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
        # endregion -- form labels
        # region -- form fields
        self.barcode_field = MyLineEdit(line_edit_ref='barcode_field')
        self.item_name_field = MyLineEdit(line_edit_ref='item_name_field')
        self.expire_dt_field = MyDateEdit(date_edit_ref='expire_dt_field')

        self.item_type_field = MyComboBox(combo_box_ref='item_type_field')
        self.brand_field = MyComboBox(combo_box_ref='brand_field')
        self.sales_group_field = MyComboBox(combo_box_ref='sales_group_field')
        self.supplier_field = MyComboBox(combo_box_ref='supplier_field')

        self.cost_field = MyLineEdit(line_edit_ref='cost_field')
        self.sell_price_field = MyLineEdit(line_edit_ref='sell_price_field')
        self.sell_price_field.textChanged.connect(self.sell_price_field_text_changed)
        self.effective_dt_field = MyDateEdit(date_edit_ref='effective_dt_field')
        self.promo_name_field = MyComboBox(combo_box_ref='promo_name_field')
        self.promo_name_field.currentTextChanged.connect(self.on_promo_name_field_current_text_changed)
        self.promo_type_field = MyLineEdit(line_edit_ref='promo_type_field')
        self.discount_percent_field = MyLineEdit(line_edit_ref='discount_percent_field')
        self.discount_value_field = MyLineEdit(line_edit_ref='discount_value_field')
        self.new_sell_price_field = MyLineEdit(line_edit_ref='new_sell_price_field')
        self.start_dt_field = MyDateEdit(date_edit_ref='start_dt_field')
        self.end_dt_field = MyDateEdit(date_edit_ref='end_dt_field')

        self.inventory_tracking_field = MyComboBox(combo_box_ref='inventory_tracking_field')
        self.inventory_tracking_field.currentTextChanged.connect(self.on_inventory_tracking_field_current_text_changed)
        self.available_stock_field = MyLineEdit(line_edit_ref='available_stock_field')
        self.on_hand_stock_field = MyLineEdit(line_edit_ref='on_hand_stock_field')
        # endregion -- form fields

        # region -- form = MyGroupBox()
        self.primary_form = MyGroupBox()
        self.primary_form_layout = MyFormLayout()
        self.primary_form_layout.addRow(self.primary_title_label)
        self.primary_form_layout.addRow(self.barcode_label, self.barcode_field)
        self.primary_form_layout.addRow(self.item_name_label, self.item_name_field)
        self.primary_form_layout.addRow(self.expire_dt_label, self.expire_dt_field)
        self.primary_form.setLayout(self.primary_form_layout)

        self.category_form = MyGroupBox()
        self.category_form_layout = MyFormLayout()
        self.category_form_layout.addRow(self.category_title_label)
        self.category_form_layout.addRow(self.item_type_label, self.item_type_field)
        self.category_form_layout.addRow(self.brand_label, self.brand_field)
        self.category_form_layout.addRow(self.sales_group_label, self.sales_group_field)
        self.category_form_layout.addRow(self.supplier_label, self.supplier_field)
        self.category_form.setLayout(self.category_form_layout)

        self.price_form = MyGroupBox()
        self.price_form_layout = MyFormLayout()
        self.price_form_layout.addRow(self.price_title_label)
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
        self.price_form.setLayout(self.price_form_layout)

        self.inventory_form = MyGroupBox()
        self.inventory_form_layout = MyFormLayout()
        self.inventory_form_layout.addRow(self.inventory_title_label)
        self.inventory_form_layout.addRow(self.inventory_tracking_label, self.inventory_tracking_field)
        self.inventory_form_layout.addRow(self.available_stock_label, self.available_stock_field)
        self.inventory_form_layout.addRow(self.on_hand_stock_label, self.on_hand_stock_field)
        self.inventory_form.setLayout(self.inventory_form_layout)
        # endregion -- form = MyGroupBox()

        # region -- self.form_nav = MyGroupBox()
        self.form_nav = MyGroupBox()
        self.form_nav_layout = MyGridLayout()
        self.discard_button = MyPushButton(text='Discard')
        self.discard_button.clicked.connect(self.on_discard_button_clicked)
        self.save_new_button = MyPushButton(text='Save New')
        self.save_new_button.clicked.connect(self.on_save_new_button_clicked)
        self.save_edit_button = MyPushButton(text='Save Edit')
        self.save_edit_button.clicked.connect(self.on_save_edit_button_clicked)
        self.form_nav_layout.addWidget(self.discard_button,0,0)
        self.form_nav_layout.addWidget(self.save_new_button,0,1)
        self.form_nav_layout.addWidget(self.save_edit_button,0,1)
        self.form_nav.setLayout(self.form_nav_layout)
        # endregion -- self.form_nav = MyGroupBox()

        self.manage_data_panel_layout.addRow(self.primary_form)
        self.manage_data_panel_layout.addRow(self.category_form)
        self.manage_data_panel_layout.addRow(self.price_form)
        self.manage_data_panel_layout.addRow(self.inventory_form)

        self.manage_data_panel_layout.addRow(self.form_nav)
        self.manage_data_panel.setLayout(self.manage_data_panel_layout)
        self.scrolling_manage_data_panel.setWidget(self.manage_data_panel)
        pass
    def show_content_panel(self):
        self.content_panel = MyWidget()
        self.content_panel_layout = MyGridLayout(grid_layout_ref='content_panel_layout')

        self.filter_field = MyLineEdit(line_edit_ref='filter_field')

        # region -- self.manage_data_nav = MyGroupBox()
        self.manage_data_nav = MyWidget(widget_ref='manage_data_nav')
        self.manage_data_layout = MyHBoxLayout(hbox_layout_ref='manage_data_layout')
        self.refresh_data_button = MyPushButton(push_button_ref='refresh_data_button', text='Refresh')
        self.refresh_data_button.clicked.connect(self.on_refresh_data_button_clicked)
        self.delete_all_data_button = MyPushButton(push_button_ref='delete_all_data_button', text='Delete All')
        self.delete_all_data_button.clicked.connect(self.on_delete_all_data_button_clicked)
        self.import_data_button = MyPushButton(push_button_ref='import_data_button', text='Import')
        self.import_data_button.clicked.connect(self.on_import_data_button_clicked)
        self.add_data_button = MyPushButton(push_button_ref='add_data_button', text='Add')
        self.add_data_button.clicked.connect(self.on_add_data_button_clicked)
        self.manage_data_layout.addWidget(self.refresh_data_button)
        self.manage_data_layout.addWidget(self.delete_all_data_button)
        self.manage_data_layout.addWidget(self.import_data_button)
        self.manage_data_layout.addWidget(self.add_data_button)
        self.manage_data_nav.setLayout(self.manage_data_layout)
        # endregion -- self.manage_data_nav = MyGroupBox()

        self.table_sorter = MyTabWidget()

        # region -- self.overview_pagination
        self.overview_pagination = MyWidget(widget_ref='overview_pagination')
        self.overview_pagination_layout = MyGridLayout(grid_layout_ref='overview_pagination_layout')
        self.overview_table = MyTableWidget(table_widget_ref='overview_table')
        self.overview_pagination_nav = MyWidget(widget_ref='overview_pagination_nav')
        self.overview_pagination_nav_layout = MyGridLayout()
        self.overview_pagination_prev_button = MyPushButton(text='Prev')
        self.overview_pagination_prev_button.clicked.connect(self.on_overview_pagination_prev_button_clicked)
        self.overview_pagination_page = MyLabel('Page 1')
        self.overview_pagination_next_button = MyPushButton(text='Next')
        self.overview_pagination_next_button.clicked.connect(self.on_overview_pagination_next_button_clicked)
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_prev_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_page,0,1,Qt.AlignmentFlag.AlignCenter)
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_nav.setLayout(self.overview_pagination_nav_layout)
        self.overview_pagination_layout.addWidget(self.overview_table,0,0)
        self.overview_pagination_layout.addWidget(self.overview_pagination_nav,1,0,Qt.AlignmentFlag.AlignCenter)
        self.overview_pagination.setLayout(self.overview_pagination_layout)
        # endregion -- self.overview_pagination
        
        # region -- self.table_sorter.addTab
        self.table_sorter.addTab(self.overview_pagination, 'Overview')
        # endregion -- self.table_sorter.addTab

        self.content_panel_layout.addWidget(self.filter_field,0,0)
        self.content_panel_layout.addWidget(self.manage_data_nav,0,1)
        self.content_panel_layout.addWidget(self.table_sorter,1,0,1,2)
        self.content_panel.setLayout(self.content_panel_layout)

    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(grid_layout_ref='main_panel_layout')

        self.show_content_panel()
        self.show_manage_data_panel()
        self.show_operation_panel()

        self.main_panel_layout.addWidget(self.content_panel,0,0)
        self.main_panel_layout.addWidget(self.scrolling_manage_data_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.operation_status_panel,1,0)
        self.setLayout(self.main_panel_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(pos_app.exec())
