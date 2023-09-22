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
from receipt_generator.receipt_printer import *
from schema.sales_table_schema import *
from schema.product_management_schema import *
from widget.process_sale_widget import *

class ProcessSaleLayout(QWidget):
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
        # Initialize a dictionary to keep track of added products and their quantities
        self.products_on_cart = []

    def add_to_cart(self, product_data):
        print(product_data)
        try:
            # Access the barcode, item_name, and price if they exist
            barcode = product_data[0]
            item_name = product_data[1]
            price = product_data[8]

            # Check if the product already exists in the list
            for index, product in enumerate(self.products_on_cart):
                if product[0] == barcode:
                    # Increment the quantity if the product already exists
                    updated_product = (barcode, product[1], product[2] + 1, product[3])  # Added a quantity field

                    self.products_on_cart[index] = updated_product
                    break
            else:
                # Add the product to the list with a quantity of 1
                new_product = (barcode, item_name, 1, price)
                self.products_on_cart.append(new_product)
                
            self.populate_order_table()

        except Exception as error:
            # Handle the case where product_data doesn't contain the expected values
            print(error)
            QMessageBox.critical(self, 'Error', 'Barcode does not exist.', QMessageBox.StandardButton.Close)

        pass
    def view_data(self, row_value):
        self.view_data_dialog = CustomDialog(ref='view_data_dialog', parent=self, row_value=row_value)

        pass

    def pay_order(self):
        # region -- underconstruction
        self.pay_order_window = CustomWidget(ref='pay_order_window')
        self.pay_order_window_layout = CustomGridLayout()
        
        self.payment_process_box = CustomGroupBox()
        self.payment_process_layout = CustomFormLayout()
        self.amount_tendered_field = CustomLineEdit()

        self.pre_amount_tendered_box = CustomGroupBox()
        self.pre_amount_tendered_layout = CustomGridLayout()
        self.pre_amount_tendered = [
            (CustomPushButton(text='5.00'),0,0),
            (CustomPushButton(text='10.00'),0,1),
            (CustomPushButton(text='20.00'),0,2),
            (CustomPushButton(text='50.00'),0,3),
            (CustomPushButton(text='100.00'),1,0),
            (CustomPushButton(text='200.00'),1,1),
            (CustomPushButton(text='500.00'),1,2),
            (CustomPushButton(text='1000.00'),1,3)
        ]
        print(self.pre_amount_tendered[0][0].text())
        print(self.pre_amount_tendered[1][0].text())
        print(self.pre_amount_tendered[2][0].text())
        print(self.pre_amount_tendered[3][0].text())
        print(self.pre_amount_tendered[4][0].text())
        print(self.pre_amount_tendered[5][0].text())
        print(self.pre_amount_tendered[6][0].text())
        print(self.pre_amount_tendered[7][0].text())

        for pre_amount, row, col in self.pre_amount_tendered:
            self.pre_amount_tendered_layout.addWidget(pre_amount, row, col)
        self.pre_amount_tendered_box.setLayout(self.pre_amount_tendered_layout)

        self.proceed_payment_button = CustomPushButton(ref='proceed_payment_button', text='Proceed Payment')

        self.payment_process_layout.addRow(self.amount_tendered_field)
        self.payment_process_layout.addRow(self.pre_amount_tendered_box)
        self.payment_process_layout.addRow(self.proceed_payment_button)
        self.payment_process_box.setLayout(self.payment_process_layout)

        self.pay_order_window_layout.addWidget(self.payment_process_box,0,0)
        self.pay_order_window.setLayout(self.pay_order_window_layout)

        self.call_signal(signal_ref='pay_order_signal')

        # endregion -- underconstruction
        pass
    def process_payment(self):
        self.receipt_generator = ReceiptGenerator()
        self.after_payment()
        pass
    def after_payment(self):
        self.pay_order_window.close()
        self.after_payment_window = CustomWidget(ref='after_payment_window')
        self.after_payment_window_layout = CustomFormLayout()

        self.process_another_sale_button = CustomLabel(text='DONE!')

        self.after_payment_window_layout.addWidget(self.process_another_sale_button)
        self.after_payment_window.setLayout(self.after_payment_window_layout)
        pass

    def refresh_data(self):
        self.populate_table()
        for data in self.products_on_cart:
            print(data)
        print('refreshed!')
        pass

    def on_push_button_clicked(self, pre_amount_tendered=0, row_value='', clicked_ref=''):
        if clicked_ref == 'add_to_cart_button':

            self.add_to_cart(product_data=row_value)

            self.filter_field.clear()
            pass
        if clicked_ref == 'view_button':
            self.view_data(row_value)
            pass

        if clicked_ref == 'previous_button':
            if self.current_page > 1:
                self.current_page -= 1

                # region: pagination page label
                self.overview_pagination_page_label.setText(f'Page {self.current_page}')
                # endregion: pagination page label

            self.populate_table(current_page=self.current_page)
            pass
        if clicked_ref == 'next_button':
            self.current_page += 1

            # region: pagination page label
            self.overview_pagination_page_label.setText(f'Page {self.current_page}')
            # endregion: pagination page label
            
            self.populate_table(current_page=self.current_page)

        if clicked_ref == 'refresh_button':
            self.refresh_data()
            pass
    
        if clicked_ref == 'pay_order_button':
            self.pay_order()

        # region -- pre_amount clicked_ref
        if clicked_ref == 'pre_amount_a':
            print(pre_amount_tendered)
            pass
        if clicked_ref == 'pre_amount_b':
            print(pre_amount_tendered)
            pass
        if clicked_ref == 'pre_amount_c':
            print(pre_amount_tendered)
            pass
        if clicked_ref == 'pre_amount_d':
            print(pre_amount_tendered)
            pass
        if clicked_ref == 'pre_amount_e':
            print(pre_amount_tendered)
            pass
        if clicked_ref == 'pre_amount_f':
            print(pre_amount_tendered)
            pass
        if clicked_ref == 'pre_amount_g':
            print(pre_amount_tendered)
            pass
        if clicked_ref == 'pre_amount_h':
            print(pre_amount_tendered)
            pass
        # endregion -- pre_amount clicked_ref
        if clicked_ref == 'proceed_payment_button':
            self.process_payment()
            pass

    def on_line_edit_text_changed(self, text_changed_ref):
        if text_changed_ref == 'filter_field':
            self.current_page = 1

            # region: pagination page label
            self.overview_pagination_page_label.setText(f'Page {self.current_page}')
            # endregion: pagination page label

            self.populate_table(current_page=self.current_page)
    def on_line_edit_return_pressed(self, return_pressed_ref):
        if return_pressed_ref == 'filter_field':
            product_data = self.product_management_schema.list_product(text_filter=self.filter_field.text())

            for row_index, row_value in enumerate(product_data):
                self.add_to_cart(product_data=row_value)

            self.filter_field.clear()
        pass

    def call_signal(
            # region: params
            self,
            add_to_cart_button=None,
            view_button=None,
            row_value='',
            signal_ref=''
            # endregion: params
    ):
        if signal_ref == 'panel_a_signal':
            self.filter_field.textChanged.connect(lambda: self.on_line_edit_text_changed(text_changed_ref='filter_field'))
            self.filter_field.returnPressed.connect(lambda: self.on_line_edit_return_pressed(return_pressed_ref='filter_field'))

            self.overview_pagination_previous_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='previous_button'))
            self.overview_pagination_next_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='next_button'))

            self.refresh_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='refresh_button'))
            pass

        if signal_ref == 'panel_b_signal':
            self.pay_order_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='pay_order_button'))
            pass

        if signal_ref == 'populate_table_signal':
            add_to_cart_button.clicked.connect(lambda: self.on_push_button_clicked(row_value=row_value, clicked_ref='add_to_cart_button'))
            view_button.clicked.connect(lambda: self.on_push_button_clicked(row_value=row_value, clicked_ref='view_button'))
            pass

        if signal_ref == 'pay_order_signal':
            # region -- amount tendered buttons
            self.pre_amount_tendered[0][0].clicked.connect(lambda: self.on_push_button_clicked(pre_amount_tendered=5, clicked_ref='pre_amount_a'))
            self.pre_amount_tendered[1][0].clicked.connect(lambda: self.on_push_button_clicked(pre_amount_tendered=10, clicked_ref='pre_amount_b'))
            self.pre_amount_tendered[2][0].clicked.connect(lambda: self.on_push_button_clicked(pre_amount_tendered=20, clicked_ref='pre_amount_c'))
            self.pre_amount_tendered[3][0].clicked.connect(lambda: self.on_push_button_clicked(pre_amount_tendered=50, clicked_ref='pre_amount_d'))
            self.pre_amount_tendered[4][0].clicked.connect(lambda: self.on_push_button_clicked(pre_amount_tendered=100, clicked_ref='pre_amount_e'))
            self.pre_amount_tendered[5][0].clicked.connect(lambda: self.on_push_button_clicked(pre_amount_tendered=200, clicked_ref='pre_amount_f'))
            self.pre_amount_tendered[6][0].clicked.connect(lambda: self.on_push_button_clicked(pre_amount_tendered=500, clicked_ref='pre_amount_g'))
            self.pre_amount_tendered[7][0].clicked.connect(lambda: self.on_push_button_clicked(pre_amount_tendered=1000, clicked_ref='pre_amount_h'))
            # endregion -- amount tendered buttons
            self.proceed_payment_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='proceed_payment_button'))

    def populate_order_table(self):
        # Clear the table
        self.order_table.setRowCount(0)

        # Initialize total price
        total_value = 0.0
        
        # Iterate over the products list and populate the table
        for barcode, item_name, qty, price in self.products_on_cart:
            row_position = self.order_table.rowCount()
            self.order_table.insertRow(row_position)

            # Calculate the subtotal for each product
            subtotal_value = price * qty
            print('total', subtotal_value)
            total_value += subtotal_value

            self.order_table.setItem(row_position, 1, QTableWidgetItem(item_name))
            self.order_table.setItem(row_position, 2, QTableWidgetItem(str(qty)))
            self.order_table.setItem(row_position, 3, QTableWidgetItem(f"₱{price:.2f}"))

        # Update the total price label
        self.subtotal_value.setText(f"{subtotal_value:.2f}")
        self.total_value.setText(f"{total_value:.2f}")
        pass

    def populate_table(self, current_page=1):
        product_data = self.product_management_schema.list_product(text_filter=self.filter_field.text(), page_number=current_page)
        inventory_data = self.product_management_schema.list_inventory(text_filter=self.filter_field.text(), page_number=current_page)

        # region: table pagination button
        self.overview_pagination_previous_button.setEnabled(self.current_page > 1)
        self.overview_pagination_next_button.setEnabled(len(product_data) == 30)
        # endregion: pagination button
        # region: table row count
        self.overview_table.setRowCount(len(product_data))
        # endregion: set tables' row count

        for row_index, row_value in enumerate(product_data):
            # region: action button
            table_action_menu = CustomWidget(ref='table_action_menu')
            table_action_menu_layout = CustomHBoxLayout(ref='table_action_menu_layout')
            self.add_to_cart_button = CustomPushButton(ref='view_button')
            self.view_button = CustomPushButton(ref='view_button')
            table_action_menu_layout.addWidget(self.add_to_cart_button)
            table_action_menu_layout.addWidget(self.view_button)
            table_action_menu.setLayout(table_action_menu_layout)

            self.call_signal(
                add_to_cart_button=self.add_to_cart_button,
                view_button=self.view_button,
                row_value=row_value, 
                signal_ref='populate_table_signal'
            )
            pass
            # endregion: action button
            # region: assign values
            item_name = CustomTableWidgetItem(text=f'{row_value[1]}')
            barcode = CustomTableWidgetItem(text=f'{row_value[0]}')
            expire_dt = CustomTableWidgetItem(text=f'{row_value[2]}')
            item_type = CustomTableWidgetItem(text=f'{row_value[3]}')
            brand = CustomTableWidgetItem(text=f'{row_value[4]}')
            sales_group = CustomTableWidgetItem(ref='sales_group', text=f'{row_value[5]}')
            supplier = CustomTableWidgetItem(ref='supplier', text=f'{row_value[6]}')
            cost = CustomTableWidgetItem(ref='cost', text=f'₱{row_value[7]}')
            sell_price = CustomTableWidgetItem(ref='sell_price', text=f'₱{row_value[8]}')
            discount_value = CustomTableWidgetItem(ref='discount_value', text=f'₱{row_value[11]}')
            effective_dt = CustomTableWidgetItem(text=f'{row_value[9]}')
            promo_name = CustomTableWidgetItem(ref='promo_name', text=f'{row_value[10]}')
            inventory_tracking = CustomTableWidgetItem(ref='inventory_tracking', text=f'{row_value[12]}')
            update_ts = CustomTableWidgetItem(ref='update_ts', text=f'{row_value[15]}')
            # endregion: assign values

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

            # region: overview list
            self.overview_table.setCellWidget(row_index, 0, table_action_menu)
            self.overview_table.setItem(row_index, 1, barcode)
            self.overview_table.setItem(row_index, 2, item_name)
            self.overview_table.setItem(row_index, 3, brand)
            self.overview_table.setItem(row_index, 4, sell_price)
            self.overview_table.setItem(row_index, 5, discount_value)
            self.overview_table.setItem(row_index, 6, promo_name)
            # endregion: overview list

    def show_panel_b(self):
        self.panel_b_box = CustomGroupBox(ref='panel_b_box')
        self.panel_b_box_layout = CustomFormLayout()
        
        # region: under construction
        self.tab_order = CustomTabWidget()
        self.order_table = CustomTableWidget(ref='order_table')
        self.tab_order.addTab(self.order_table, 'Order 1')

        self.order_amount_box = CustomGroupBox()
        self.order_amount_layout = CustomFormLayout()
        self.subtotal_value = CustomLabel(ref='subtotal_value', text='0.00')
        self.discount_value = CustomLabel(ref='discount_value', text='0.00')
        self.tax_value = CustomLabel(ref='tax_value', text='0.00')
        self.total_value = CustomLabel(ref='total_value', text='0.00')
        self.order_amount_layout.addRow('Subtotal:', self.subtotal_value)
        self.order_amount_layout.addRow('Discount:', self.discount_value)
        self.order_amount_layout.addRow('Tax:', self.tax_value)
        self.order_amount_layout.addRow('Total:', self.total_value)
        self.order_amount_box.setLayout(self.order_amount_layout)

        self.panel_b_action_menu = CustomGroupBox()
        self.panel_b_action_menu_layout = CustomGridLayout()
        self.discard_order_button = CustomPushButton(text='Discard')
        self.pay_order_button = CustomPushButton(text=f'Pay {self.total_value.text()}')
        self.panel_b_action_menu_layout.addWidget(self.discard_order_button,0,0)
        self.panel_b_action_menu_layout.addWidget(self.pay_order_button,1,0)
        self.panel_b_action_menu.setLayout(self.panel_b_action_menu_layout)
        # endregion: under construction

        self.panel_b_box_layout.addRow(self.tab_order)
        self.panel_b_box_layout.addRow(self.order_amount_box)
        self.panel_b_box_layout.addRow(self.panel_b_action_menu)
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

        # region: manage data buttons
        self.tab_sort_action_menu = CustomWidget(ref='tab_sort_action_menu')
        self.tab_sort_action_menu_layout = CustomHBoxLayout()
        self.refresh_button = CustomPushButton(ref='refresh_button')
        self.scanner_mode_button = CustomPushButton(ref='scanner_mode_button')
        self.scanner_mode_field = CustomLineEdit(ref='scanner_mode_field')
        self.tab_sort_action_menu_layout.addWidget(self.refresh_button)
        self.tab_sort_action_menu_layout.addWidget(self.scanner_mode_button)
        self.tab_sort_action_menu.setLayout(self.tab_sort_action_menu_layout)
        # endregion: manage data buttons
        # region: tab layout setup
        self.tab_sort = CustomTabWidget(ref='tab_sort')
        self.tab_sort.addTab(self.overview_tab, 'Overview')
        self.tab_sort.setCornerWidget(self.tab_sort_action_menu, Qt.Corner.BottomRightCorner)
        # endregion: tab layout setup

        self.panel_a_box_layout.addWidget(self.filter_field,0,0)
        self.panel_a_box_layout.addWidget(self.tab_sort,1,0)

        self.panel_a_box.setLayout(self.panel_a_box_layout)
        pass
        
        self.call_signal(signal_ref='panel_a_signal')

    def show_main_panel(self):
        self.setWindowTitle('Process Sale')
        self.setWindowState(Qt.WindowState.WindowMaximized)

        self.show_panel_a()
        self.show_panel_b()

        grid_layout = CustomGridLayout()
        grid_layout.addWidget(self.panel_a_box,0,0)
        grid_layout.addWidget(self.panel_b_box,0,1)

        self.setLayout(grid_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProcessSaleLayout()
    window.show()
    sys.exit(pos_app.exec())
