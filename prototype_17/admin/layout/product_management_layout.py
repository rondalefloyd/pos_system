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
          
    # region: data processing functions
    def refresh_data(self):
        self.populate_table()
        print('refreshed!')
        pass
    def mass_delete_data(self):
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
        print('Import data!')
        pass
    def add_data(self):
        pass
    # endregion: data processing functions
    
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
        # endregion: get fields' input
        pass
    def save_edit_data(self):
        pass
   
    # region: fields and buttons event
    def on_push_button_clicked(self, clicked_ref):
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

            self.populate_table(text_filter=self.filter_field.text(), current_page=self.current_page)
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
            
            self.populate_table(text_filter=self.filter_field.text(), current_page=self.current_page)

        if clicked_ref == 'refresh_button':
            self.refresh_data()
            pass
        if clicked_ref == 'mass_delete_button':
            pass
        if clicked_ref == 'import_button':
            self.import_data()
            pass
        if clicked_ref == 'add_button':
            self.panel_b_box.show()
            self.add_button.setDisabled(True)
            self.add_data()

        if clicked_ref == 'back_button':
            self.panel_b_box.hide()
            self.add_button.setDisabled(False)       
        if clicked_ref == 'save_new_button':
            self.save_new_data()
            pass
        if clicked_ref == 'save_edit_button':
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
        pass
    def on_combo_box_current_text_changed(self, current_text, current_text_changed_ref):
        if current_text_changed_ref == 'promo_name_field':
            if current_text == 'No promo':
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
                # promo_name = self.promo_name_field.currentText()

                # data = self.item_management_schema.get_promo_type_and_discount_percent(promo_name)
                # for row in data:
                #     self.promo_type_field.setText(str(row[0]))
                #     self.discount_percent_field.setText(str(row[1]))

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
            if current_text == 'Disabled':
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
    # endregion: fields and buttons event

    def update_panel_b(self):
        pass

    def populate_combo_box(self, combo_box_ref):
        if combo_box_ref == 'item_type':
            pass
        if combo_box_ref == 'brand':
            pass
        if combo_box_ref == 'supplier':
            pass
        if combo_box_ref == 'promo_name':
            pass
        pass
    def populate_table(self, current_page=1):
        data = self.product_management_schema.list_product(text_filter=self.filter_field.text(), page_number=current_page)

        # region: pagination button
        self.overview_pagination_previous_button.setEnabled(self.current_page > 1)
        self.primary_pagination_previous_button.setEnabled(self.current_page > 1)
        self.category_pagination_previous_button.setEnabled(self.current_page > 1)
        self.price_pagination_previous_button.setEnabled(self.current_page > 1)
        self.inventory_pagination_previous_button.setEnabled(self.current_page > 1)

        self.overview_pagination_next_button.setEnabled(len(data) == 30)
        self.primary_pagination_next_button.setEnabled(len(data) == 30)
        self.category_pagination_next_button.setEnabled(len(data) == 30)
        self.price_pagination_next_button.setEnabled(len(data) == 30)
        self.inventory_pagination_next_button.setEnabled(len(data) == 30)
        # endregion: pagination button

        self.overview_table.setRowCount(len(data))
        self.primary_table.setRowCount(len(data))
        self.category_table.setRowCount(len(data))
        self.price_table.setRowCount(len(data))
        self.inventory_table.setRowCount(len(data))

        for row_index, row_value in enumerate(data):
            # region: action button
            action_box = CustomWidget(ref='action_box')
            action_layout = CustomHBoxLayout(ref='action_layout')
            self.edit_button = CustomPushButton(text='Edit')
            self.view_button = CustomPushButton(text='View')
            self.delete = CustomPushButton(text='Delete')
            action_layout.addWidget(self.edit_button)
            action_layout.addWidget(self.view_button)
            action_layout.addWidget(self.delete)
            action_box.setLayout(action_layout)
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
                CustomTableWidgetItem(text=f'{row_value[5]}'),
                CustomTableWidgetItem(text=f'{row_value[5]}'),
                CustomTableWidgetItem(text=f'{row_value[5]}'),
                CustomTableWidgetItem(text=f'{row_value[5]}'),
                CustomTableWidgetItem(text=f'{row_value[5]}')
            ]
            supplier = CustomTableWidgetItem(text=f'{row_value[6]}')
            cost = CustomTableWidgetItem(text=f'₱{row_value[7]}')
            sell_price = [
                CustomTableWidgetItem(text=f'₱{row_value[8]}'),
                CustomTableWidgetItem(text=f'₱{row_value[8]}'),
                CustomTableWidgetItem(text=f'₱{row_value[8]}'),
                CustomTableWidgetItem(text=f'₱{row_value[8]}'),
                CustomTableWidgetItem(text=f'₱{row_value[8]}')
            ]
            discount_value = CustomTableWidgetItem(text=f'₱{row_value[11]}')
            effective_dt = CustomTableWidgetItem(text=f'{row_value[9]}')
            promo_name = [
                CustomTableWidgetItem(text=f'{row_value[10]}'),
                CustomTableWidgetItem(text=f'{row_value[10]}'),
                CustomTableWidgetItem(text=f'{row_value[10]}'),
                CustomTableWidgetItem(text=f'{row_value[10]}'),
                CustomTableWidgetItem(text=f'{row_value[10]}')
            ]
            inventory_tracking = [
                CustomTableWidgetItem(text=f'{row_value[12]}'),
                CustomTableWidgetItem(text=f'{row_value[12]}'),
                CustomTableWidgetItem(text=f'{row_value[12]}'),
                CustomTableWidgetItem(text=f'{row_value[12]}'),
                CustomTableWidgetItem(text=f'{row_value[12]}')
            ]
            available = CustomTableWidgetItem(text=f'{row_value[13]}')
            on_hand = CustomTableWidgetItem(text=f'{row_value[14]}')
            update_ts = [
                CustomTableWidgetItem(text=f'{row_value[15]}'),
                CustomTableWidgetItem(text=f'{row_value[15]}'),
                CustomTableWidgetItem(text=f'{row_value[15]}'),
                CustomTableWidgetItem(text=f'{row_value[15]}'),
                CustomTableWidgetItem(text=f'{row_value[15]}')
            ]
            # endregion: assign values

            # region: overview list
            self.overview_table.setCellWidget(row_index, 0, action_box)
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
            # region: inventory list
            self.inventory_table.setItem(row_index, 0, item_name[4])
            self.inventory_table.setItem(row_index, 1, inventory_tracking[4])
            self.inventory_table.setItem(row_index, 2, available)
            self.inventory_table.setItem(row_index, 3, on_hand)
            self.inventory_table.setItem(row_index, 4, promo_name[4])
            self.inventory_table.setItem(row_index, 5, update_ts[4])
            # endregion: inventory list

    def call_signal(self, signal_ref=''):
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
            self.mass_delete_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='mass_delete_button'))
            self.add_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='add_button'))
            self.import_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='import_button'))
            # endregion: manage data buttons
            pass
        if signal_ref == 'panel_b_signal':
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
            pass

    def show_panel_b(self):
        self.panel_b_box = CustomGroupBox(ref='panel_b_box')
        self.panel_b_box_layout = CustomFormLayout()

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
        self.available_stock_label = CustomLabel(ref='available_stock_label', text='available_stock')
        self.on_hand_stock_label = CustomLabel(ref='on_hand_stock_label', text='on_hand_stock')

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

        self.panel_b_box_layout.insertRow(1, self.primary_box)
        self.panel_b_box_layout.insertRow(2, self.category_box)
        self.panel_b_box_layout.insertRow(3, self.price_box)
        self.panel_b_box_layout.insertRow(4, self.inventory_box)

        # region: form buttons
        self.back_button = CustomPushButton(text='Back')
        self.save_new_button = CustomPushButton(text='Save Add')
        self.save_edit_button = CustomPushButton(text='Save Edit')

        self.panel_b_box_layout.insertRow(0, self.back_button)
        self.panel_b_box_layout.insertRow(5, self.save_new_button)
        self.panel_b_box_layout.insertRow(6, self.save_edit_button)
        # endregion: form buttons

        self.panel_b_box.setLayout(self.panel_b_box_layout)

        self.call_signal(signal_ref='panel_b_signal')

    def show_panel_a(self):
        self.panel_a_box = CustomGroupBox()
        self.panel_a_box_layout = CustomGridLayout()

        self.filter_field = CustomLineEdit(ref='filter_field')
        self.tab_sort = CustomTabWidget()

        # region: overview pagination table
        self.overview_table = CustomTableWidget(ref='overview_table')
        self.overview_pagination = CustomGroupBox()
        self.overview_pagination_layout = CustomGridLayout()
        self.overview_pagination_previous_button = CustomPushButton(text='Prev')
        self.overview_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.overview_pagination_next_button = CustomPushButton(text='Next')
        self.overview_pagination_layout.addWidget(self.overview_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_layout.addWidget(self.overview_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_layout.addWidget(self.overview_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination.setLayout(self.overview_pagination_layout)
        self.overview_tab_layout = CustomGridLayout() 
        self.overview_tab_layout.addWidget(self.overview_table)
        self.overview_tab_layout.addWidget(self.overview_pagination)
        self.overview_tab = CustomWidget() 
        self.overview_tab.setLayout(self.overview_tab_layout) 
        # endregion: overview pagination table
        # region: primary pagination table
        self.primary_table = CustomTableWidget(ref='primary_table')
        self.primary_pagination = CustomGroupBox()
        self.primary_pagination_layout = CustomGridLayout()
        self.primary_pagination_previous_button = CustomPushButton(text='Prev')
        self.primary_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.primary_pagination_next_button = CustomPushButton(text='Next')
        self.primary_pagination_layout.addWidget(self.primary_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.primary_pagination_layout.addWidget(self.primary_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.primary_pagination_layout.addWidget(self.primary_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.primary_pagination.setLayout(self.primary_pagination_layout)
        self.primary_tab_layout = CustomGridLayout()
        self.primary_tab_layout.addWidget(self.primary_table)
        self.primary_tab_layout.addWidget(self.primary_pagination)
        self.primary_tab = CustomWidget() 
        self.primary_tab.setLayout(self.primary_tab_layout) 
        # endregion: primary pagination table
        # region: category pagination table
        self.category_table = CustomTableWidget(ref='category_table')
        self.category_pagination = CustomGroupBox()
        self.category_pagination_layout = CustomGridLayout()
        self.category_pagination_previous_button = CustomPushButton(text='Prev')
        self.category_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.category_pagination_next_button = CustomPushButton(text='Next')
        self.category_pagination_layout.addWidget(self.category_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.category_pagination_layout.addWidget(self.category_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.category_pagination_layout.addWidget(self.category_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.category_pagination.setLayout(self.category_pagination_layout)
        self.category_tab_layout = CustomGridLayout()
        self.category_tab_layout.addWidget(self.category_table)
        self.category_tab_layout.addWidget(self.category_pagination)
        self.category_tab = CustomWidget() 
        self.category_tab.setLayout(self.category_tab_layout) 
        # endregion: category pagination table
        # region: price pagination table
        self.price_table = CustomTableWidget(ref='price_table')
        self.price_pagination = CustomGroupBox()
        self.price_pagination_layout = CustomGridLayout()
        self.price_pagination_previous_button = CustomPushButton(text='Prev')
        self.price_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.price_pagination_next_button = CustomPushButton(text='Next')
        self.price_pagination_layout.addWidget(self.price_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.price_pagination_layout.addWidget(self.price_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.price_pagination_layout.addWidget(self.price_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.price_pagination.setLayout(self.price_pagination_layout)
        self.price_tab_layout = CustomGridLayout()
        self.price_tab_layout.addWidget(self.price_table)
        self.price_tab_layout.addWidget(self.price_pagination)
        self.price_tab = CustomWidget() 
        self.price_tab.setLayout(self.price_tab_layout) 
        # endregion: price pagination table
        # region: inventory pagination table
        self.inventory_table = CustomTableWidget(ref='inventory_table')
        self.inventory_pagination = CustomGroupBox()
        self.inventory_pagination_layout = CustomGridLayout()
        self.inventory_pagination_previous_button = CustomPushButton(text='Prev')
        self.inventory_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.inventory_pagination_next_button = CustomPushButton(text='Next')
        self.inventory_pagination_layout.addWidget(self.inventory_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_pagination_layout.addWidget(self.inventory_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_pagination_layout.addWidget(self.inventory_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_pagination.setLayout(self.inventory_pagination_layout)
        self.inventory_tab_layout = CustomGridLayout()
        self.inventory_tab_layout.addWidget(self.inventory_table)
        self.inventory_tab_layout.addWidget(self.inventory_pagination)
        self.inventory_tab = CustomWidget() 
        self.inventory_tab.setLayout(self.inventory_tab_layout) 
        # endregion: inventory pagination table
        # region: manage data buttons
        self.manage_data_box = CustomGroupBox()
        self.manage_data_box_layout = CustomHBoxLayout()
        self.refresh_button = CustomPushButton(text='Refresh')
        self.mass_delete_button = CustomPushButton(text='Mass Delete')
        self.import_button = CustomPushButton(text='Import')
        self.add_button = CustomPushButton(text='Add')
        self.manage_data_box_layout.addWidget(self.refresh_button)
        self.manage_data_box_layout.addWidget(self.mass_delete_button)
        self.manage_data_box_layout.addWidget(self.import_button)
        self.manage_data_box_layout.addWidget(self.add_button)
        self.manage_data_box.setLayout(self.manage_data_box_layout)
        # endregion: manage data buttons

        # region: tab setup
        self.tab_sort.addTab(self.overview_tab, 'Overview')
        self.tab_sort.addTab(self.primary_tab, 'Primary')
        self.tab_sort.addTab(self.category_tab, 'Category')
        self.tab_sort.addTab(self.price_tab, 'Price')
        self.tab_sort.addTab(self.inventory_tab, 'Inventory')
        self.tab_sort.setCornerWidget(self.manage_data_box)
        # endregion: setup tab

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
