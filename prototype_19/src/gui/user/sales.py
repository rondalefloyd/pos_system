import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))
print('sys path: ', os.path.abspath(''))

from src.core.color_scheme import *
from src.core.manual_csv_importer import *

from src.database.user.sales import *
from src.widget.user.sales import *

class SalesWindow(MyWidget):
    def __init__(self):
        super().__init__()

        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):
        self.sales_schema = SalesSchema()
        self.my_push_button = MyPushButton()

        self.data_list_curr_page = 1
        self.new_quantity = 1
        self.new_price = 0

        self.required_field_indicator = "<font color='red'>-- required</font>"

        self.total_product_count = self.sales_schema.count_product()

        # region > cart_panel

        self.container_list()
        
        # endregion

        self.txn_type_toggle = 'Retail'
        self.atc_toggle = 'Untoggled'
        pass
    def sync_ui(self):
        self.populate_all_combo_box()
        self.populate_data_list_table(txn_type=self.txn_type_toggle)

        self.data_mgt_scanned_barcode_field.hide()
        self.data_mgt_toggle_wholesale_txn_button.hide()
        self.data_mgt_untoggle_aatc_button.hide()


        self.customer_name_field.setCurrentText('')

        self.total_data.setText(f'Total promo: {self.sales_schema.count_product()}')
        pass

    def container_list(self):
        self.cart_list_table = []

        self.sub_total_value = []
        self.discount_value = []
        self.tax_value = []
        self.total_value = []

        self.sub_total_value_label = []
        self.discount_value_label = []
        self.tax_value_label = []
        self.total_value_label = []

        self.sales_mgt_discard_button = []
        self.sales_mgt_pay_button = []

        self.cart_list_data = []
        pass

    def style_data_list_action_button(self):
        self.data_list_atc_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.data_list_view_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        pass
    def style_data_list_pgn_action_button(self):
        self.data_list_pgn_prev_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.data_list_pgn_next_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        pass
    def style_sales_mgt_action_button(self):
        self.add_cart_tab_button.setStyleSheet(self.my_push_button.add_cart_tab_button_ss)
        pass
    def style_data_mgt_action_button(self):
        self.data_mgt_sync_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)

        self.data_mgt_toggle_retail_txn_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        self.data_mgt_toggle_wholesale_txn_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        
        self.data_mgt_toggle_aatc_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        self.data_mgt_untoggle_aatc_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        pass

    def on_data_list_view_button_clicked(self, row_value, view_button):
        self.data_list_view_dialog = MyDialog(object_name='data_list_view_dialog', parent=self)
        self.data_list_view_dialog_layout = MyFormLayout()

        barcode_info = MyLabel(object_name='barcode_info', text=str(row_value[0]))
        item_name_info = MyLabel(object_name='item_name_info', text=str(row_value[1]))
        expire_dt_info = MyLabel(object_name='expire_dt_info', text=str(row_value[2]))

        item_type_info = MyLabel(object_name='item_type_info', text=str(row_value[3]))
        brand_info = MyLabel(object_name='brand_info', text=str(row_value[4]))
        sales_group_info = MyLabel(object_name='sales_group_info', text=str(row_value[5]))
        supplier_info = MyLabel(object_name='supplier_info', text=str(row_value[6]))

        cost_info = MyLabel(object_name='cost_info', text=f'₱{row_value[7]}')
        sell_price_info = MyLabel(object_name='sell_price_info', text=f'₱{row_value[8]}')
        effective_dt_info = MyLabel(object_name='effective_dt_info', text=str(row_value[9]))
        promo_name_info = MyLabel(object_name='promo_name_info', text=str(row_value[10]))
        discount_value_info = MyLabel(object_name='discount_value_info', text=f'₱{row_value[11]}')

        inventory_tracking_info = MyLabel(object_name='inventory_tracking_info', text=str(row_value[12]))

        date_created_info = MyLabel(object_name='date_created_info', text=str(row_value[15]))

        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Barcode:'), barcode_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Item name:'), item_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Expire date:'), expire_dt_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Item type:'), item_type_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Brand:'), brand_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Sales group:'), sales_group_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Supplier:'), supplier_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Cost:'), cost_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Sell price:'), sell_price_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Effective date:'), effective_dt_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Promo name:'), promo_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Discount value:'), discount_value_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Inventory tracking:'), inventory_tracking_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Date and time created:'), date_created_info)
        self.data_list_view_dialog.setLayout(self.data_list_view_dialog_layout)

        self.data_list_view_dialog.exec()
        pass

    def on_payment_back_button_clicked(self):
        self.payment_dialog.close()
        self.cart_list_data = []
        pass
    def on_process_payment_button_clicked(self):
        pass

    def on_data_mgt_sync_button_clicked(self):
        self.sync_ui()

        pass
    def on_data_mgt_toggle_retail_txn_button_clicked(self):
        self.data_mgt_toggle_retail_txn_button.hide()
        self.data_mgt_toggle_wholesale_txn_button.show()

        self.txn_type_toggle = 'Wholesale'

        self.populate_data_list_table(text_filter=self.text_filter_field.text(), txn_type=self.txn_type_toggle, current_page=1)

        pass
    def on_data_mgt_toggle_wholesale_txn_button_clicked(self):
        self.data_mgt_toggle_retail_txn_button.show()
        self.data_mgt_toggle_wholesale_txn_button.hide()
        

        self.txn_type_toggle = 'Retail'

        self.populate_data_list_table(text_filter=self.text_filter_field.text(), txn_type=self.txn_type_toggle, current_page=1)

        pass
    def on_data_mgt_toggle_aatc_button_clicked(self):
        self.data_mgt_scanned_barcode_field.show()
        self.data_mgt_toggle_aatc_button.hide()
        self.data_mgt_untoggle_aatc_button.show()

        self.atc_toggle = 'Toggled'

        pass
    def on_data_mgt_untoggle_aatc_button_clicked(self):
        self.data_mgt_scanned_barcode_field.hide()
        self.data_mgt_toggle_aatc_button.show()
        self.data_mgt_untoggle_aatc_button.hide()

        self.atc_toggle = 'Untoggled'
        pass

    def on_data_list_pgn_prev_button_clicked(self):
        
        if self.data_list_curr_page > 1:
            self.data_list_curr_page -= 1
            self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')

        self.populate_data_list_table(text_filter=self.text_filter_field.text(), txn_type=self.txn_type_toggle, current_page=self.data_list_curr_page)

        pass
    def on_data_list_pgn_next_button_clicked(self):
        
        self.data_list_curr_page += 1
        self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')
        
        self.populate_data_list_table(text_filter=self.text_filter_field.text(), txn_type=self.txn_type_toggle, current_page=self.data_list_curr_page)
        

        pass

    def on_text_filter_field_text_changed(self):
        self.data_list_curr_page = 1
        self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')
        
        self.populate_data_list_table(text_filter=str(self.text_filter_field.text()), txn_type=self.txn_type_toggle, current_page=self.data_list_curr_page)
        pass

    def on_amt_tendered_opt_button_clicked(self, amt):
        self.amt_tendered_field.setText(str(amt))
        pass
    def on_data_mgt_scanned_barcode_field_return_pressed(self):
        if self.atc_toggle == 'Toggled':
            product_data = self.sales_schema.list_product_via_barcode(barcode=self.data_mgt_scanned_barcode_field.text(), txn_type=self.txn_type_toggle)
            for row_index, row_value in enumerate(product_data): 
                self.update_cart_tab(row_value=row_value)

            self.data_mgt_scanned_barcode_field.clear()

        elif self.atc_toggle == 'Untoggled':
            pass
        pass
    def on_add_cart_tab_button_clicked(self):
        i = self.cart_tab.currentIndex()

        self.populate_cart_tab()
        pass
    def on_cart_tab_current_changed(self):
        i = self.cart_tab.currentIndex()
        print(os.system('cls'))
        print('current_index:', i)

        
        # region > test print
        print('current:', self.cart_list_table)
        print('current:', self.sub_total_value)
        print('current:', self.discount_value)
        print('current:', self.tax_value)
        print('current:', self.total_value)
        print('current:', self.sub_total_value_label)
        print('current:', self.discount_value_label)
        print('current:', self.tax_value_label)
        print('current:', self.total_value_label)
        print('current:', self.sales_mgt_discard_button)
        print('current:', self.sales_mgt_pay_button)
        # endregion


        pass
   
    def on_sales_mgt_pay_button_clicked(self):
        i = self.cart_tab.currentIndex()
        print(os.system('cls'))
        print('current_index:', i)

        
        # region > test print
        print('current:', self.cart_list_table)
        print('current:', self.sub_total_value)
        print('current:', self.discount_value)
        print('current:', self.tax_value)
        print('current:', self.total_value)
        print('current:', self.sub_total_value_label)
        print('current:', self.discount_value_label)
        print('current:', self.tax_value_label)
        print('current:', self.total_value_label)
        print('current:', self.sales_mgt_discard_button)
        print('current:', self.sales_mgt_pay_button)
        # endregion



        for row in range(self.cart_list_table[i].rowCount()):
            row_data = []
            for col in range(self.cart_list_table[i].columnCount()):
                item = self.cart_list_table[i].item(row, col)
                if item is not None:
                    row_data.append(item.text())
            self.cart_list_data.append(row_data)

        # region > convert field input into str
        self.payment_dialog = MyDialog(object_name='payment_dialog')
        self.payment_dialog_layout = MyGridLayout(object_name='payment_dialog_layout')

        self.bill_review_panel = MyGroupBox(object_name='bill_review_panel')
        self.bill_review_panel_layout = MyFormLayout(object_name='bill_review_panel_layout')

        self.bill_review_sub_total = MyLabel(object_name='bill_review_sub_total', text=f'₱{self.sub_total_value[i]:.2f}')
        self.bill_review_discount = MyLabel(object_name='bill_review_discount', text=f'₱{self.discount_value[i]:.2f}')
        self.bill_review_tax = MyLabel(object_name='bill_review_tax', text=f'₱{self.tax_value[i]:.2f}')
        self.bill_review_total = MyLabel(object_name='bill_review_total', text=f'₱{self.total_value[i]:.2f}')
        self.bill_review_customer = MyLabel(object_name='bill_review_total', text=f'Customer 1')
        self.bill_review_reward_pts = MyLabel(object_name='bill_review_total', text=f'Unavailable')

        # region > set_label_alignment
        self.bill_review_sub_total.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.bill_review_discount.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.bill_review_tax.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.bill_review_total.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.bill_review_customer.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.bill_review_reward_pts.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        # endregion

        self.bill_review_panel_layout.addRow('Sub total:', self.bill_review_sub_total)
        self.bill_review_panel_layout.addRow('Discount:', self.bill_review_discount)
        self.bill_review_panel_layout.addRow('Tax:', self.bill_review_tax)
        self.bill_review_panel_layout.addRow('Total:', self.bill_review_total)
        self.bill_review_panel_layout.addRow(QLabel('<hr>'))
        self.bill_review_panel_layout.addRow('Customer:', self.bill_review_customer)
        self.bill_review_panel_layout.addRow('Reward points:', self.bill_review_reward_pts)
        self.bill_review_panel.setLayout(self.bill_review_panel_layout)
    
        self.payment_panel = MyGroupBox(object_name='payment_panel')
        self.payment_panel_layout = MyFormLayout(object_name='payment_panel_layout')

        self.amt_tendered_panel = MyGroupBox(object_name='amt_tendered_panel')
        self.amt_tendered_panel_layout = MyGridLayout(object_name='amt_tendered_panel_layout')
        self.amt_tendered_label = MyLabel(object_name='amt_tendered_label', text='Amount tenedered:')
        self.amt_tendered_field = MyLineEdit(object_name='amt_tendered_field')
        self.amt_tendered_opt_button = [
            MyPushButton(object_name='amt_tendered_opt_button', text='₱5'),
            MyPushButton(object_name='amt_tendered_opt_button', text='₱10'),
            MyPushButton(object_name='amt_tendered_opt_button', text='₱20'),
            MyPushButton(object_name='amt_tendered_opt_button', text='₱50'),
            MyPushButton(object_name='amt_tendered_opt_button', text='₱100'),
            MyPushButton(object_name='amt_tendered_opt_button', text='₱200'),
            MyPushButton(object_name='amt_tendered_opt_button', text='₱500'),
            MyPushButton(object_name='amt_tendered_opt_button', text='₱1000')
        ]
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_label,0,0,1,4)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_field,1,0,1,4)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_opt_button[0],2,0)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_opt_button[1],2,1)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_opt_button[2],2,2)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_opt_button[3],2,3)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_opt_button[4],3,0)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_opt_button[5],3,1)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_opt_button[6],3,2)
        self.amt_tendered_panel_layout.addWidget(self.amt_tendered_opt_button[7],3,3)
        self.amt_tendered_panel.setLayout(self.amt_tendered_panel_layout)

        self.payment_action_button_panel = MyGroupBox(object_name='payment_action_button_panel')
        self.payment_action_button_panel_layout = MyHBoxLayout(object_name='payment_action_button_panel_layout')
        self.payment_back_button = MyPushButton(object_name='payment_back_button', text=f'Back')
        self.process_payment_button = MyPushButton(object_name='process_payment_button', text=f'Proceed Payment')
        self.payment_action_button_panel_layout.addWidget(self.payment_back_button)
        self.payment_action_button_panel_layout.addWidget(self.process_payment_button)
        self.payment_action_button_panel.setLayout(self.payment_action_button_panel_layout)

        # region > connections
        self.payment_back_button.clicked.connect(self.on_payment_back_button_clicked)
        self.process_payment_button.clicked.connect(self.on_process_payment_button_clicked)
        # endregion

        self.payment_panel_layout.addRow(self.amt_tendered_panel)
        self.payment_panel_layout.addRow(self.payment_action_button_panel)
        self.payment_panel.setLayout(self.payment_panel_layout)

        self.payment_dialog_layout.addWidget(self.bill_review_panel,0,0)
        self.payment_dialog_layout.addWidget(self.payment_panel,0,1)
        self.payment_dialog.setLayout(self.payment_dialog_layout)
        
        # region > connections
        self.amt_tendered_opt_button[0].clicked.connect(lambda: self.on_amt_tendered_opt_button_clicked(amt=5))
        self.amt_tendered_opt_button[1].clicked.connect(lambda: self.on_amt_tendered_opt_button_clicked(amt=10))
        self.amt_tendered_opt_button[2].clicked.connect(lambda: self.on_amt_tendered_opt_button_clicked(amt=20))
        self.amt_tendered_opt_button[3].clicked.connect(lambda: self.on_amt_tendered_opt_button_clicked(amt=50))
        self.amt_tendered_opt_button[4].clicked.connect(lambda: self.on_amt_tendered_opt_button_clicked(amt=100))
        self.amt_tendered_opt_button[5].clicked.connect(lambda: self.on_amt_tendered_opt_button_clicked(amt=200))
        self.amt_tendered_opt_button[6].clicked.connect(lambda: self.on_amt_tendered_opt_button_clicked(amt=500))
        self.amt_tendered_opt_button[7].clicked.connect(lambda: self.on_amt_tendered_opt_button_clicked(amt=1000))

        # endregion

        # region > style_buttons
        for amt_tendered_opt_button in self.amt_tendered_opt_button:
            amt_tendered_opt_button.setStyleSheet(self.my_push_button.amt_tendered_opt_button_ss)

        self.payment_back_button.setStyleSheet(self.my_push_button.payment_back_button_ss)
        self.process_payment_button.setStyleSheet(self.my_push_button.process_payment_button_ss)
        # endregion

        self.payment_dialog.exec()

        # endregion

        if self.payment_dialog.isVisible() == False:
            self.cart_list_data = []
        pass
    def on_sales_mgt_discard_button_clicked(self):
        i = self.cart_tab.currentIndex()

        # Close the tab at the current index
        self.cart_tab.removeTab(i)

        self.cart_list_table.remove(self.cart_list_table[i])
        self.sub_total_value.remove(self.sub_total_value[i])
        self.discount_value.remove(self.discount_value[i])
        self.tax_value.remove(self.tax_value[i])
        self.total_value.remove(self.total_value[i])
        self.sub_total_value_label.remove(self.sub_total_value_label[i])
        self.discount_value_label.remove(self.discount_value_label[i])
        self.tax_value_label.remove(self.tax_value_label[i])
        self.total_value_label.remove(self.total_value_label[i])
        self.sales_mgt_discard_button.remove(self.sales_mgt_discard_button[i])
        self.sales_mgt_pay_button.remove(self.sales_mgt_pay_button[i])


        pass
    
    def on_cart_list_drop_all_qty_button_clicked(self, row_value):
        i = self.cart_tab.currentIndex()
        print(os.system('cls'))
        print('current_index:', i)

        # region > test print
        print('current:', self.cart_list_table)
        print('current:', self.sub_total_value)
        print('current:', self.discount_value)
        print('current:', self.tax_value)
        print('current:', self.total_value)
        print('current:', self.sub_total_value_label)
        print('current:', self.discount_value_label)
        print('current:', self.tax_value_label)
        print('current:', self.total_value_label)
        print('current:', self.sales_mgt_discard_button)
        print('current:', self.sales_mgt_pay_button)
        # endregion

        try:
            self.new_quantity = 0
            self.new_price = float(row_value[8]) * self.new_quantity

            item_list = self.cart_list_table[i].findItems(row_value[1], Qt.MatchFlag.MatchExactly)

            if item_list:
                for item in item_list:
                    row = item.row()  # Get the row of the item

                    print('self.new_price:', self.new_price)
                    # !!! CHECKPOINT !!! 
                    # AGENDA: FIX THE RIGHT AMOUNT OF THE FOLLOWING: 
                    #     self.sub_total_value[i]
                    #     self.discount_value[i]
                    #     self.tax_value[i]
                    #     self.total_value[i]

                    current_quantity = int(self.cart_list_table[i].item(row, 2).text().replace('x', ''))  # Get the current value and convert it to an integer
                    current_price = float(self.cart_list_table[i].item(row, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                
                    self.sub_total_value[i] = self.new_price
                    self.discount_value[i] = float(row_value[11]) * self.new_quantity
                    self.tax_value[i] = 0
                    self.total_value[i] = (self.sub_total_value[i] - self.discount_value[i]) + self.tax_value[i]

                    self.sub_total_value_label[i].setText(f'₱{self.sub_total_value[i]:.2f}')
                    self.discount_value_label[i].setText(f'₱{self.discount_value[i]:.2f}')
                    self.tax_value_label[i].setText(f'₱{self.tax_value[i]:.2f}')
                    self.total_value_label[i].setText(f'₱{self.total_value[i]:.2f}')

                    self.sales_mgt_pay_button[i].setText(f'Pay ₱{self.total_value[i]:.2f}')


                    self.cart_list_table[i].removeRow(row)
        except Exception as e:
            print(e)                
        pass
    def on_cart_list_drop_qty_button_clicked(self, row_value):
        i = self.cart_tab.currentIndex()
        print(os.system('cls'))
        print('current_index:', i)

        # region > test print
        print('current:', self.cart_list_table)
        print('current:', self.sub_total_value)
        print('current:', self.discount_value)
        print('current:', self.tax_value)
        print('current:', self.total_value)
        print('current:', self.sub_total_value_label)
        print('current:', self.discount_value_label)
        print('current:', self.tax_value_label)
        print('current:', self.total_value_label)
        print('current:', self.sales_mgt_discard_button)
        print('current:', self.sales_mgt_pay_button)
        # endregion

        try: 
            item_list = self.cart_list_table[i].findItems(row_value[1], Qt.MatchFlag.MatchExactly)

            if item_list:
                for item in item_list:
                    row = item.row()  # Get the row of the item

                    current_quantity = int(self.cart_list_table[i].item(row, 2).text().replace('x', ''))  # Get the current value and convert it to an integer
                    current_price = float(self.cart_list_table[i].item(row, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                    self.new_quantity = current_quantity - 1  # Increment the current value
                    self.new_price = current_price - row_value[8]

                    quantity = QTableWidgetItem(f'x{self.new_quantity}')  # Create a new 
                    price = QTableWidgetItem(f'₱{self.new_price:.2f}')  # Create a new 

                    quantity.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.cart_list_table[i].setItem(row, 2, quantity)
                    self.cart_list_table[i].setItem(row, 3, price)

                    self.sub_total_value[i] -= float(row_value[8])
                    self.discount_value[i] -= float(row_value[11])
                    self.tax_value[i] = 0
                    self.total_value[i] = (self.sub_total_value[i] - self.discount_value[i]) + self.tax_value[i]

                    if self.new_quantity <= 0:
                        self.cart_list_table[i].removeRow(row)

                    self.sub_total_value_label[i].setText(f'₱{self.sub_total_value[i]:.2f}')
                    self.discount_value_label[i].setText(f'₱{self.discount_value[i]:.2f}')
                    self.tax_value_label[i].setText(f'₱{self.tax_value[i]:.2f}')
                    self.total_value_label[i].setText(f'₱{self.total_value[i]:.2f}')

                    self.sales_mgt_pay_button[i].setText(f'Pay ₱{self.total_value[i]:.2f}')
                pass
            else:
                pass
            self.new_quantity = 1
            self.new_price = 0
            pass
        except Exception as e:
            print(e)
        pass
    def on_cart_list_add_qty_button_clicked(self, row_value):
        self.update_cart_tab(row_value=row_value)
        pass
    def on_cart_list_edit_qty_button_clicked(self, row_value):
        proposed_quantity, confirm = QInputDialog.getText(self, 'Quantity', 'Input quantity:')
        
        self.new_quantity = int(proposed_quantity)
        self.new_quantity = 0 if self.new_quantity < 0 else self.new_quantity

        i = self.cart_tab.currentIndex()
        # print(os.system('cls'))
        print('current_index:', i)
        
        # region > test print
        print('current:', self.cart_list_table)
        print('current:', self.sub_total_value)
        print('current:', self.discount_value)
        print('current:', self.tax_value)
        print('current:', self.total_value)
        print('current:', self.sub_total_value_label)
        print('current:', self.discount_value_label)
        print('current:', self.tax_value_label)
        print('current:', self.total_value_label)
        print('current:', self.sales_mgt_discard_button)
        print('current:', self.sales_mgt_pay_button)
        # endregion

        if confirm == True:
            try:
                self.new_price = float(row_value[8]) * self.new_quantity

                print('self.new_price:', self.new_price)
                
                self.sub_total_value[i] = self.new_price
                self.discount_value[i] = float(row_value[11]) * self.new_quantity
                self.tax_value[i] = 0
                self.total_value[i] = (self.sub_total_value[i] - self.discount_value[i]) + self.tax_value[i]

                self.sub_total_value_label[i].setText(f'₱{self.sub_total_value[i]:.2f}')
                self.discount_value_label[i].setText(f'₱{self.discount_value[i]:.2f}')
                self.tax_value_label[i].setText(f'₱{self.tax_value[i]:.2f}')
                self.total_value_label[i].setText(f'₱{self.total_value[i]:.2f}')

                self.sales_mgt_pay_button[i].setText(f'Pay ₱{self.total_value[i]:.2f}')

                item_list = self.cart_list_table[i].findItems(row_value[1], Qt.MatchFlag.MatchExactly)

                if item_list:
                    for item in item_list:
                        row = item.row()  # Get the row of the item

                        if self.new_quantity <= 0:
                            self.cart_list_table[i].removeRow(row)

                        current_quantity = int(self.cart_list_table[i].item(row, 2).text().replace('x', ''))  # Get the current value and convert it to an integer
                        current_price = float(self.cart_list_table[i].item(row, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                        quantity = QTableWidgetItem(f'x{self.new_quantity}')  # Create a new 
                        price = QTableWidgetItem(f'₱{self.new_price:.2f}')  # Create a new 

                        quantity.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                        price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                        self.cart_list_table[i].setItem(row, 2, quantity)
                        self.cart_list_table[i].setItem(row, 3, price)

                else:
                    pass
                self.new_quantity = 1
                self.new_price = 0
                pass
            except Exception as e:
                print(e)
        else:
            pass

    def on_data_list_atc_button_clicked(self, row_value): # cart process
        quantity, confirm = QInputDialog.getText(self, 'Quantity', 'Input quantity:')
        print(quantity)
        print(confirm)

        try:
            if confirm == True:
                self.new_quantity = int(quantity)

                self.update_cart_tab(row_value=row_value)

            else:
                pass
        except Exception as e:
            print(e)

        pass
    def update_cart_tab(self, row_value):
        i = self.cart_tab.currentIndex()
        # print(os.system('cls'))
        print('current_index:', i)
        
        # region > test print
        print('current:', self.cart_list_table)
        print('current:', self.sub_total_value)
        print('current:', self.discount_value)
        print('current:', self.tax_value)
        print('current:', self.total_value)
        print('current:', self.sub_total_value_label)
        print('current:', self.discount_value_label)
        print('current:', self.tax_value_label)
        print('current:', self.total_value_label)
        print('current:', self.sales_mgt_discard_button)
        print('current:', self.sales_mgt_pay_button)
        # endregion

        try:
            self.new_price = float(row_value[8]) * self.new_quantity
            print('self.new_price:', self.new_price)
            
            if self.new_quantity > 1:
                self.sub_total_value[i] += float(self.new_price)
                self.discount_value[i] = float(row_value[11]) * self.new_quantity
            else:
                self.sub_total_value[i] += float(row_value[8])
                self.discount_value[i] += float(row_value[11])

            self.tax_value[i] = 0
            self.total_value[i] = (self.sub_total_value[i] - self.discount_value[i]) + self.tax_value[i]

            self.sub_total_value_label[i].setText(f'₱{self.sub_total_value[i]:.2f}')
            self.discount_value_label[i].setText(f'₱{self.discount_value[i]:.2f}')
            self.tax_value_label[i].setText(f'₱{self.tax_value[i]:.2f}')
            self.total_value_label[i].setText(f'₱{self.total_value[i]:.2f}')

            self.sales_mgt_pay_button[i].setText(f'Pay ₱{self.total_value[i]:.2f}')

            item_list = self.cart_list_table[i].findItems(row_value[1], Qt.MatchFlag.MatchExactly)

            if item_list:
                for item in item_list:
                    row = item.row()  # Get the row of the item

                    current_quantity = int(self.cart_list_table[i].item(row, 2).text().replace('x', ''))  # Get the current value and convert it to an integer
                    current_price = float(self.cart_list_table[i].item(row, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                    if self.new_quantity > 1:
                        print('here a')
                        self.new_quantity = current_quantity + self.new_quantity  # Increment the current value
                    else:
                        print('here b')
                        self.new_quantity = current_quantity + 1  # Increment the current value

                    self.new_price = current_price + self.new_price

                    quantity = QTableWidgetItem(f'x{self.new_quantity}')  # Create a new 
                    price = QTableWidgetItem(f'₱{self.new_price:.2f}')  # Create a new 

                    quantity.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    self.cart_list_table[i].setItem(row, 2, quantity)
                    self.cart_list_table[i].setItem(row, 3, price)

            else:
                row_index = self.cart_list_table[i].rowCount()
                self.cart_list_table[i].insertRow(row_index)
                
                # region > cart_list_action_panel
                cart_list_action_panel = MyGroupBox(object_name='cart_list_action_panel')
                cart_list_action_panel_layout = MyHBoxLayout(object_name='cart_list_action_panel_layout')
                cart_list_drop_all_qty_button = MyPushButton(object_name='cart_list_drop_all_qty_button')
                cart_list_drop_qty_button = MyPushButton(object_name='cart_list_drop_qty_button')
                cart_list_add_qty_button = MyPushButton(object_name='cart_list_add_qty_button')
                cart_list_edit_qty_button = MyPushButton(object_name='cart_list_edit_qty_button')
                cart_list_action_panel_layout.addWidget(cart_list_drop_all_qty_button)
                cart_list_action_panel_layout.addWidget(cart_list_drop_qty_button)
                cart_list_action_panel_layout.addWidget(cart_list_add_qty_button)
                cart_list_action_panel_layout.addWidget(cart_list_edit_qty_button)
                cart_list_action_panel.setLayout(cart_list_action_panel_layout)
                # endregion
                
                item_name = QTableWidgetItem(str(row_value[1]))
                quantity = QTableWidgetItem(f'x{self.new_quantity}')  # Create a new 
                price = QTableWidgetItem(f'₱{self.new_price:.2f}')

                quantity.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                self.cart_list_table[i].setCellWidget(row_index, 0, cart_list_action_panel)
                self.cart_list_table[i].setItem(row_index, 1, item_name)
                self.cart_list_table[i].setItem(row_index, 2, quantity)
                self.cart_list_table[i].setItem(row_index, 3, price)

                # region > connections
                cart_list_drop_all_qty_button.clicked.connect(lambda: self.on_cart_list_drop_all_qty_button_clicked(row_value))
                cart_list_drop_qty_button.clicked.connect(lambda: self.on_cart_list_drop_qty_button_clicked(row_value))
                cart_list_add_qty_button.clicked.connect(lambda: self.on_cart_list_add_qty_button_clicked(row_value))
                cart_list_edit_qty_button.clicked.connect(lambda: self.on_cart_list_edit_qty_button_clicked(row_value))
                # endregion

                # region > style_buttons
                cart_list_drop_all_qty_button.setStyleSheet(self.my_push_button.cart_list_action_panel_ss)
                cart_list_drop_qty_button.setStyleSheet(self.my_push_button.cart_list_action_panel_ss)
                cart_list_add_qty_button.setStyleSheet(self.my_push_button.cart_list_action_panel_ss)
                cart_list_edit_qty_button.setStyleSheet(self.my_push_button.cart_list_action_panel_ss)
                # endregion


            self.new_quantity = 1
            self.new_price = 0
            pass
        except Exception as e:
            print(e)

    def populate_cart_tab(self, cart_tab_name=''): # cart process a
        cart_panel = MyGroupBox(object_name='cart_panel')
        cart_panel_layout = MyGridLayout(object_name='cart_panel_layout')

        # region > cart_list_table
        cart_list_table = MyTableWidget(object_name='cart_list_table')
        # endregion
        # region > cart_list_bill
        cart_list_bill = MyGroupBox(object_name='cart_list_bill')
        cart_list_bill_layout = MyFormLayout(object_name='cart_list_bill_layout')

        item_name = ''
        quantity = 0
        price = 0

        sub_total_value = 0
        discount_value = 0
        tax_value = 0
        total_value = 0

        sub_total_value_label = MyLabel(object_name='bill_value_label', text=f'₱{sub_total_value:.2f}')
        discount_value_label = MyLabel(object_name='bill_value_label', text=f'₱{discount_value:.2f}')
        tax_value_label = MyLabel(object_name='bill_value_label', text=f'₱{tax_value:.2f}')
        total_value_label = MyLabel(object_name='bill_value_label', text=f'₱{total_value:.2f}')

        cart_list_bill_layout.addRow('Sub total', sub_total_value_label)
        cart_list_bill_layout.addRow('Discount', discount_value_label)
        cart_list_bill_layout.addRow('Tax', tax_value_label)
        cart_list_bill_layout.addRow('Total', total_value_label)
        cart_list_bill.setLayout(cart_list_bill_layout)
        # endregion
        # region > sales_mgt_action
        sales_mgt_action_panel = MyGroupBox(object_name='sales_mgt_action_panel') # head.b
        sales_mgt_action_panel_layout = MyHBoxLayout(object_name='sales_mgt_action_panel_layout')
        sales_mgt_discard_button = MyPushButton(object_name='sales_mgt_discard_button', text='Discard')
        sales_mgt_pay_button = MyPushButton(object_name='sales_mgt_pay_button', text=f'PAY ₱{total_value}')
        sales_mgt_action_panel_layout.addWidget(sales_mgt_discard_button)
        sales_mgt_action_panel_layout.addWidget(sales_mgt_pay_button)
        sales_mgt_action_panel.setLayout(sales_mgt_action_panel_layout)
        # endregion

        cart_panel_layout.addWidget(cart_list_table)
        cart_panel_layout.addWidget(cart_list_bill)
        cart_panel_layout.addWidget(sales_mgt_action_panel)
        cart_panel.setLayout(cart_panel_layout)
        
        # region > connections
        sales_mgt_discard_button.clicked.connect(self.on_sales_mgt_discard_button_clicked)
        sales_mgt_pay_button.clicked.connect(self.on_sales_mgt_pay_button_clicked)
        # endregion

        # region > style_buttons
        sales_mgt_discard_button.setStyleSheet(self.my_push_button.sales_mgt_discard_button_ss)
        sales_mgt_pay_button.setStyleSheet(self.my_push_button.sales_mgt_pay_button_ss)

        cart_tab_name = f'New customer' if cart_tab_name == '' else cart_tab_name
        cart_tab_index = self.cart_tab.addTab(cart_panel, f'{cart_tab_name}')

        self.cart_tab.setCurrentIndex(cart_tab_index)
        # endregion
        
        # region > append to list
        self.cart_list_table.append(cart_list_table)

        self.sub_total_value.append(sub_total_value)
        self.discount_value.append(discount_value)
        self.tax_value.append(tax_value)
        self.total_value.append(total_value)

        self.sub_total_value_label.append(sub_total_value_label)
        self.discount_value_label.append(discount_value_label)
        self.tax_value_label.append(tax_value_label)
        self.total_value_label.append(total_value_label)

        self.sales_mgt_discard_button.append(sales_mgt_discard_button)
        self.sales_mgt_pay_button.append(sales_mgt_pay_button)
        # endregion
        pass
    def populate_all_combo_box(self):
        customer_name_list = self.sales_schema.list_customer()

        self.customer_name_field.addItem('Customer')
        for customer_name in customer_name_list:
            self.customer_name_field.addItem(customer_name[0])
        pass
    def populate_data_list_table(self, text_filter='', txn_type='Retail', current_page=1):
        # region > data_list_clear_contents
        self.data_list_table.clearContents()
        # endregion

        # region > data_list
        
        product_data = self.sales_schema.list_product(text_filter=text_filter, txn_type=txn_type, page_number=current_page)
        # endregion

        # region > data_list_pgn_button_set_enabled
        self.data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)
        self.data_list_pgn_next_button.setEnabled(len(product_data) == 30)
        # endregion

        # region > clicked_data_list_set_disabled
        # endregion
        
        # region > data_list_table_set_row_count
        self.data_list_table.setRowCount(len(product_data))
        # endregion

        for row_index, row_value in enumerate(product_data):
            # region > data_list_action
            self.data_list_action_panel = MyGroupBox(object_name='data_list_action_panel') # head.a
            self.data_list_action_panel_layout = MyHBoxLayout(object_name='data_list_action_panel_layout')
            
            # region > set_data_list_action_buttons
            self.data_list_atc_button = MyPushButton(object_name='data_list_atc_button')
            self.data_list_view_button = MyPushButton(object_name='data_list_view_button', text='View')
            # endregion

            # region > data_list_action_button_connections
            self.data_list_atc_button.clicked.connect(lambda _, row_value=row_value: self.on_data_list_atc_button_clicked(row_value))
            self.data_list_view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.data_list_view_button: self.on_data_list_view_button_clicked(row_value, view_button))
            # endregion

            # region > style_data_list_action_buttons
            self.style_data_list_action_button()
            # endregion

            self.data_list_action_panel_layout.addWidget(self.data_list_atc_button)
            self.data_list_action_panel_layout.addWidget(self.data_list_view_button)
            self.data_list_action_panel.setLayout(self.data_list_action_panel_layout)
            # endregion

            # region > set_table_item_values
            barcode = QTableWidgetItem(str(row_value[0]))
            item_name = QTableWidgetItem(str(row_value[1]))
            brand = QTableWidgetItem(str(row_value[4]))
            sales_group = QTableWidgetItem(str(row_value[5]))
            sell_price = QTableWidgetItem(f'₱{row_value[8]:.2f}')
            # endregion

            # region > set_table_item_alignment
            barcode.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            sales_group.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            sell_price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            # endregion
        
            # region > set_data_list_table_cells
            self.data_list_table.setCellWidget(row_index, 0, self.data_list_action_panel)
            self.data_list_table.setItem(row_index, 1, barcode)
            self.data_list_table.setItem(row_index, 2, item_name)
            self.data_list_table.setItem(row_index, 3, brand)
            self.data_list_table.setItem(row_index, 4, sales_group)
            self.data_list_table.setItem(row_index, 5, sell_price)
            # endregion

            # region > colored_rows_if_has_promo
            if row_value[18] != 0:
                barcode.setForeground(QColor(204,49,61))
                item_name.setForeground(QColor(204,49,61))
                brand.setForeground(QColor(204,49,61))
                sales_group.setForeground(QColor(204,49,61))
                sell_price.setForeground(QColor(204,49,61))
            # endregion
        pass

    def show_extra_info_panel(self):
        self.extra_info_panel = MyGroupBox(object_name='extra_info_panel') # head.d
        self.extra_info_panel_layout = MyHBoxLayout(object_name='extra_info_panel_layout')

        # region > extra_info_labels
        self.total_data = MyLabel(object_name='total_data', text=f'Total product: {self.total_product_count}')
        # endregion

        self.extra_info_panel_layout.addWidget(self.total_data,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.extra_info_panel.setLayout(self.extra_info_panel_layout)
        pass
    def show_sales_mgt_panel(self):
        self.sales_mgt_panel = MyGroupBox(object_name='sales_mgt_panel')
        self.sales_mgt_panel_layout = MyVBoxLayout(object_name='sales_mgt_panel_layout')

        # region > add_cart_tab
        self.add_cart_tab_panel = MyGroupBox(object_name='add_cart_tab_panel')
        self.add_cart_tab_panel_layout = MyHBoxLayout(object_name='add_cart_tab_panel_layout')
        self.customer_name_field = MyComboBox(object_name='customer_name_field')
        self.add_cart_tab_button = MyPushButton(object_name='add_cart_tab_button', text='Add')
        self.add_cart_tab_panel_layout.addWidget(self.customer_name_field,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignHCenter)
        self.add_cart_tab_panel_layout.addWidget(self.add_cart_tab_button)
        self.add_cart_tab_panel.setLayout(self.add_cart_tab_panel_layout)
        # endregion
        # region > cart_tab
        self.cart_tab = MyTabWidget(object_name='cart_tab')

        self.populate_cart_tab()

        # endregion

        # region > sales_mgt_connections
        self.add_cart_tab_button.clicked.connect(self.on_add_cart_tab_button_clicked)
        self.cart_tab.currentChanged.connect(self.on_cart_tab_current_changed)
        # endregion
        
        # region > style_sales_mgt_buttons
        self.style_sales_mgt_action_button()
        # endregion

        self.sales_mgt_panel_layout.addWidget(self.add_cart_tab_panel)
        self.sales_mgt_panel_layout.addWidget(self.cart_tab)
        self.sales_mgt_panel.setLayout(self.sales_mgt_panel_layout)
        pass
    def show_content_panel(self):
        self.content_panel = MyGroupBox(object_name='content_panel')
        self.content_panel_layout = MyGridLayout(object_name='content_panel_layout')

        # region > text_filter
        self.text_filter_field = MyLineEdit(object_name='text_filter_field') # head.a

        # region > content_text_filter_connection
        self.text_filter_field.textChanged.connect(self.on_text_filter_field_text_changed)
        # endregion

        # endregion
        # region > data_mgt_action
        self.data_mgt_action_panel = MyGroupBox(object_name='data_mgt_action_panel') # head.b
        self.data_mgt_action_panel_layout = MyHBoxLayout(object_name='data_mgt_action_panel_layout')
        self.data_mgt_sync_button = MyPushButton(object_name='data_mgt_sync_button')

        self.data_mgt_toggle_retail_txn_button = MyPushButton(object_name='data_mgt_toggle_retail_txn_button', text='Retail')
        self.data_mgt_toggle_wholesale_txn_button = MyPushButton(object_name='data_mgt_toggle_wholesale_txn_button', text='Wholesale')

        self.data_mgt_scanned_barcode_field = MyLineEdit(object_name='data_mgt_scanned_barcode_field') # head.a
        self.data_mgt_toggle_aatc_button = MyPushButton(object_name='data_mgt_toggle_aatc_button')
        self.data_mgt_untoggle_aatc_button = MyPushButton(object_name='data_mgt_untoggle_aatc_button')

        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_sync_button)

        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_toggle_retail_txn_button)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_toggle_wholesale_txn_button)

        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_scanned_barcode_field)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_toggle_aatc_button)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_untoggle_aatc_button)
        self.data_mgt_action_panel.setLayout(self.data_mgt_action_panel_layout)
        # endregion
        # region > data_list_sorter
        self.data_list_sorter_tab = MyTabWidget(object_name='data_list_sorter_tab') # head.c
        self.data_list_pgn_panel = MyGroupBox(object_name='data_list_pgn_panel') # head.c.a
        self.data_list_pgn_panel_layout = MyVBoxLayout(object_name='data_list_pgn_panel_layout')
        self.data_list_table = MyTableWidget(object_name='data_list_table')
        self.data_list_pgn_action_panel = MyGroupBox(object_name='data_list_pgn_action_panel')
        self.data_list_pgn_action_panel_layout = MyGridLayout(object_name='data_list_pgn_action_panel_layout')
        self.data_list_pgn_prev_button = MyPushButton(object_name='data_list_pgn_prev_button')
        self.data_list_pgn_page = MyLabel(object_name='data_list_pgn_page', text='Page 1')
        self.data_list_pgn_next_button = MyPushButton(object_name='data_list_pgn_next_button')
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_prev_button,0,0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_page,0,1, Qt.AlignmentFlag.AlignCenter)
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_next_button,0,2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.data_list_pgn_action_panel.setLayout(self.data_list_pgn_action_panel_layout)
        self.data_list_pgn_panel_layout.addWidget(self.data_list_table)
        self.data_list_pgn_panel_layout.addWidget(self.data_list_pgn_action_panel)
        self.data_list_pgn_panel.setLayout(self.data_list_pgn_panel_layout)
        self.data_list_sorter_tab.addTab(self.data_list_pgn_panel, 'Overview')
        # endregion

        # region > connections
        self.data_mgt_sync_button.clicked.connect(self.on_data_mgt_sync_button_clicked)
        
        self.data_mgt_toggle_retail_txn_button.clicked.connect(self.on_data_mgt_toggle_retail_txn_button_clicked)
        self.data_mgt_toggle_wholesale_txn_button.clicked.connect(self.on_data_mgt_toggle_wholesale_txn_button_clicked)

        self.data_mgt_scanned_barcode_field.returnPressed.connect(self.on_data_mgt_scanned_barcode_field_return_pressed)
        self.data_mgt_toggle_aatc_button.clicked.connect(self.on_data_mgt_toggle_aatc_button_clicked)
        self.data_mgt_untoggle_aatc_button.clicked.connect(self.on_data_mgt_untoggle_aatc_button_clicked)

        self.data_list_pgn_prev_button.clicked.connect(self.on_data_list_pgn_prev_button_clicked)
        self.data_list_pgn_next_button.clicked.connect(self.on_data_list_pgn_next_button_clicked)
        # endregion

        # region > style_content_buttons
        self.style_data_mgt_action_button()
        self.style_data_list_pgn_action_button()
        # endregion

        self.content_panel_layout.addWidget(self.text_filter_field,0,0,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.content_panel_layout.addWidget(self.data_mgt_action_panel,0,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.content_panel_layout.addWidget(self.data_list_sorter_tab,1,0,1,2)
        self.content_panel.setLayout(self.content_panel_layout)
        pass
    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(object_name='main_panel_layout')

        self.show_content_panel()
        self.show_sales_mgt_panel()
        self.show_extra_info_panel()

        self.main_panel_layout.addWidget(self.content_panel,0,0)
        self.main_panel_layout.addWidget(self.sales_mgt_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.extra_info_panel,1,0)
        self.setLayout(self.main_panel_layout)
    
if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    color_scheme = ColorScheme()
    window = SalesWindow()
    window.show()
    sys.exit(pos_app.exec())
