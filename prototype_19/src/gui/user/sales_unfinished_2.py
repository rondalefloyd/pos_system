import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
from typing import List
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))

from src.core.manual_csv_importer import *
from src.core.qss_config import *

from database.user.sales import *
from widget.user.sales_unfinished_2 import *

class MySalesModel:
    def __init__(self, schema: SalesSchema):

        self.schema = schema

        self.set_icons()
        self.set_a_panel_container()
        self.set_b_panel_container()
        self.set_c_panel_container()
        self.set_populate_cust_tab_container()
        self.set_order_list_container()
        self.set_pymt_panel_container()

    def set_icons(self):
        self.verified_cust_icon = MyIcon(icon_name='verified_cust_icon')
    def set_a_panel_container(self):
        self.curr_tab = ''
        self.curr_page = 1
        self.total_page = self.schema.count_product_list_total_pages(txn_type='Retail')
    def set_b_panel_container(self):
        self.a_prod_list = self.schema.list_product()
        self.b_prod_list = self.schema.list_product_via_promo()
        self.cust_name_list = self.schema.list_customer()
        self.i = 0
        pass
    def set_c_panel_container(self):
        self.curr_user = '[no user]'
        self.total_cust_order = 0
        self.total_prod = self.schema.count_product()
    def set_populate_cust_tab_container(self):
        self.cust_name = []
        self.txn_type = []

        self.order_list_table: List[QTableWidget] = []
        self.order_txn_type_label: List[QLabel] = []
        self.order_clr_list_button: List[QPushButton] = []

        self.item_name = []
        self.qty = []
        self.total_price = []
        self.total_discount = []

        self.order_subtotal = []
        self.order_discount = []
        self.order_tax = []
        self.order_total = []

        self.order_subtotal_label: List[QLabel] = []
        self.order_discount_label: List[QLabel] = []
        self.order_tax_label: List[QLabel] = []
        self.order_total_label: List[QLabel] = []

        self.order_discard_button: List[QPushButton] = []
        self.order_unlocked_button: List[QPushButton] = []
        self.order_locked_button: List[QPushButton] = []
        self.order_save_button: List[QPushButton] = []

        self.order_pay_button: List[QPushButton] = []
        pass
    def set_order_list_container(self):
        self.new_qty = 1
        self.new_total_price = 0
        self.new_discount = 0
        pass
    def set_pymt_panel_container(self):
        self.change_value = 0
        pass
    def verify_customer(self, cust_name):
        try:
            self.customer_id = self.schema.get_customer_id(customer=cust_name)
        except Exception as e:
            self.customer_id = '0'
    def append_cust_tab_cont_var(
        self,
        cust_name,
        txn_type,
        order_list_table,
        order_txn_type_label,
        order_clr_list_button,
        order_subtotal_value,
        order_discount_value,
        order_tax_value,
        order_total_value,
        order_subtotal_label,
        order_discount_label,
        order_tax_label,
        order_total_label,
        order_discard_button,
        order_unlocked_button,
        order_locked_button,
        order_save_button,
        order_pay_button
    ):
        self.cust_name.append(cust_name)
        self.txn_type.append(txn_type)
        self.order_list_table.append(order_list_table)
        self.order_txn_type_label.append(order_txn_type_label)
        self.order_clr_list_button.append(order_clr_list_button)
        self.order_subtotal.append(order_subtotal_value)
        self.order_discount.append(order_discount_value)
        self.order_tax.append(order_tax_value)
        self.order_total.append(order_total_value)
        self.order_subtotal_label.append(order_subtotal_label)
        self.order_discount_label.append(order_discount_label)
        self.order_tax_label.append(order_tax_label)
        self.order_total_label.append(order_total_label)
        self.order_discard_button.append(order_discard_button)
        self.order_unlocked_button.append(order_unlocked_button)
        self.order_locked_button.append(order_locked_button)
        self.order_save_button.append(order_save_button)
        self.order_pay_button.append(order_pay_button)
        pass
    def compute_order_summary(
        self,
        subtotal=0,
        discount=0,
        tax=0,
        total=0,
        change=0

    ):
        subtotal = 0 # TODO: add computation
        discount = 0 # TODO: add computation
        tax = 0 # TODO: add computation
        total = 0 # TODO: add computation
        change = 0 # TODO: add computation
        pass

class MySalesView(MyWidget):
    def __init__(self, model: MySalesModel):
        super().__init__(object_name='my_sales_view')

        self.model = model

        self.show_main_panel()

        
        self.default_layout()
        self.sync_layout()

    def default_layout(self):
        pass
    def sync_layout(self):
        self.total_cust_order_label.setText(f"Pending order: {self.cust_order_tab.count()}")
        self.populate_prod_list_table()
        pass
    
    def populate_via_edit(self):
        i = self.cust_order_tab.currentIndex()
        pass
    def populate_via_drop(self):
        i = self.cust_order_tab.currentIndex()
        pass
    def populate_via_add(self):
        i = self.cust_order_tab.currentIndex()
        pass
    def populate_via_drop_all(self):
        i = self.cust_order_tab.currentIndex()
        pass
    def populate_via_clear(self):
        i = self.cust_order_tab.currentIndex()
        pass
    def populate_via_atc(self, row_value):
        i = self.cust_order_tab.currentIndex()


        proposed_qty, confirm = QInputDialog.getText(self, 'Add quantity', 'Enter quantity:')

        if confirm == True:
            item_list = self.model.order_list_table[i].findItems(row_value[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name
            
            if item_list:
                for item in item_list:
                    row = item.row()  # Get the row of the item

                    curr_qty = int(self.model.order_list_table[i].item(row, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                    curr_price = float(self.model.order_list_table[i].item(row, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                    curr_discount = float(self.model.order_list_table[i].item(row, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                    self.new_qty = int(proposed_qty) + curr_qty
                    self.new_total_price = (float(row_value[8]) * int(proposed_qty)) + curr_price
                    self.new_discount = (float(row_value[11]) * int(proposed_qty)) + curr_discount

                    qty = QTableWidgetItem(f'{self.new_qty}x')  # Create a new 
                    price = QTableWidgetItem(f'₱{self.new_total_price:,.2f}')  # Create a new 
                    discount = QTableWidgetItem(f'₱{self.new_discount:,.2f}')  # Create a new 

                    self.model.order_list_table[i].setItem(row, 1, qty)
                    self.model.order_list_table[i].setItem(row, 3, price)
                    self.model.order_list_table[i].setItem(row, 4, discount)
                pass
            else:
                row_index = self.model.order_list_table[i].rowCount()

                self.model.order_list_table[i].insertRow(row_index)
                
                self.model.new_qty = proposed_qty
                self.model.new_total_price = float(row_value[8]) * int(proposed_qty)

                action_panel = MyGroupBox(object_name='action_panel')
                action_panel_layout = MyHBoxLayout(object_name='action_panel_layout')
                drop_all_qty_button = MyPushButton(object_name='drop_all_qty_button')
                drop_qty_button = MyPushButton(object_name='drop_qty_button')
                add_qty_button = MyPushButton(object_name='add_qty_button')
                edit_qty_button = MyPushButton(object_name='edit_qty_button')
                action_panel_layout.addWidget(drop_all_qty_button)
                action_panel_layout.addWidget(drop_qty_button)
                action_panel_layout.addWidget(add_qty_button)
                action_panel_layout.addWidget(edit_qty_button)
                action_panel.setLayout(action_panel_layout)

                qty = QTableWidgetItem(f'{self.model.new_qty}x')  # Create a new 
                item_name = QTableWidgetItem(str(row_value[1]))
                price = QTableWidgetItem(f'₱{self.model.new_total_price:,.2f}')
                discount = QTableWidgetItem(f'₱{self.model.new_discount:,.2f}')
      

                self.model.order_list_table[i].setCellWidget(row_index, 0, action_panel)
                self.model.order_list_table[i].setItem(row_index, 1, qty)
                self.model.order_list_table[i].setItem(row_index, 2, item_name)
                self.model.order_list_table[i].setItem(row_index, 3, price)
                self.model.order_list_table[i].setItem(row_index, 4, discount)


            self.model.order_subtotal[i] = float(self.model.order_subtotal[i]) + (float(row_value[8]) * int(proposed_qty))
            self.model.order_discount[i] = float(self.model.order_discount[i]) + (float(row_value[11]) * int(proposed_qty))
            self.model.order_tax[i] = float(self.model.order_tax[i]) + (0 * int(proposed_qty))
            self.model.order_total[i] = (self.model.order_subtotal[i] - self.model.order_discount[i]) + self.model.order_tax[i]

            self.model.order_subtotal_label[i].setText(f'₱{self.model.order_subtotal[i]:,.2f}')
            self.model.order_discount_label[i].setText(f'₱{self.model.order_discount[i]:,.2f}')
            self.model.order_tax_label[i].setText(f'₱{self.model.order_tax[i]:,.2f}')
            self.model.order_total_label[i].setText(f'₱{self.model.order_total[i]:,.2f}')

            self.model.order_pay_button[i].setText(f'₱{self.model.order_total[i]:,.2f}')

            self.model.set_order_list_container()
        pass
    def populate_via_barcode(self):
        i = self.cust_order_tab.currentIndex()
        pass

    def populate_cust_tab(self):
        cust_name = self.add_order_cust_name_field.currentText()
        txn_type = self.add_order_txn_type_field.currentText()

        self.model.verify_customer(cust_name=cust_name)
        
        cust_tab_cont_panel = MyGroupBox(object_name='cust_tab_cont_panel')
        cust_tab_cont_panel_panel = MyGridLayout(object_name='cust_tab_cont_panel_panel')

        order_a_act_panel = MyGroupBox(object_name='order_a_act_panel')
        order_a_act_panel_layout = MyHBoxLayout(object_name='order_a_act_panel_layout')
        order_a_txn_type_label = MyLabel(object_name='order_a_txn_type_label', text=f'{txn_type}')
        order_a_clr_list_button = MyPushButton(object_name='order_a_clr_list_button', text='Clear')
        order_a_act_panel_layout.addWidget(order_a_txn_type_label)
        order_a_act_panel_layout.addWidget(order_a_clr_list_button)
        order_a_act_panel.setLayout(order_a_act_panel_layout)
        
        order_list_table = MyTableWidget(object_name='order_list_table')

        order_summ_panel = MyGroupBox(object_name='order_summ_panel')
        order_summ_panel_layout = MyFormLayout(object_name='order_summ_panel_layout')
        order_subtotal_label = MyLabel(object_name='order_subtotal', text=f"₱0")
        order_discount_label = MyLabel(object_name='order_discount', text=f"₱0")
        order_tax_label = MyLabel(object_name='order_tax', text=f"₱0")
        order_total_label = MyLabel(object_name='order_total', text=f"₱0")
        order_summ_panel_layout.addRow('Subtotal:', order_subtotal_label)
        order_summ_panel_layout.addRow('Discount:', order_discount_label)
        order_summ_panel_layout.addRow('Tax:', order_tax_label)
        order_summ_panel_layout.addRow('Total:', order_total_label)
        order_summ_panel.setLayout(order_summ_panel_layout)

        order_b_act_panel = MyGroupBox(object_name='order_b_act_panel')
        order_b_act_panel_layout = MyVBoxLayout(object_name='order_b_act_panel_layout')

        order_ba_sub_act_panel = MyGroupBox(object_name='order_ba_sub_act_panel')
        order_ba_sub_act_panel_layout = MyHBoxLayout(object_name='order_ba_sub_act_panel_layout')
        order_discard_button = MyPushButton(object_name='order_discard_button', text='Discard')
        order_unlocked_button = MyPushButton(object_name='order_unlocked_button', text='Unlocked')
        order_locked_button = MyPushButton(object_name='order_locked_button', text='Locked')
        order_save_button = MyPushButton(object_name='order_save_button', text='Save') 

        order_ba_sub_act_panel_layout.addWidget(order_discard_button)
        order_ba_sub_act_panel_layout.addWidget(order_unlocked_button)
        order_ba_sub_act_panel_layout.addWidget(order_locked_button)
        order_ba_sub_act_panel_layout.addWidget(order_save_button)
        order_ba_sub_act_panel.setLayout(order_ba_sub_act_panel_layout)

        order_bb_sub_act_panel = MyGroupBox(object_name='order_bb_sub_act_panel')
        order_bb_sub_act_panel_layout = MyHBoxLayout(object_name='order_bb_sub_act_panel_layout')
        order_pay_button = MyPushButton(object_name='order_pay_button', text='Pay')
        order_bb_sub_act_panel_layout.addWidget(order_pay_button)
        order_bb_sub_act_panel.setLayout(order_bb_sub_act_panel_layout)

        order_b_act_panel_layout.addWidget(order_ba_sub_act_panel)
        order_b_act_panel_layout.addWidget(order_bb_sub_act_panel)
        order_b_act_panel.setLayout(order_b_act_panel_layout)

        cust_tab_cont_panel_panel.addWidget(order_a_act_panel,0,0)
        cust_tab_cont_panel_panel.addWidget(order_list_table,1,0)
        cust_tab_cont_panel_panel.addWidget(order_summ_panel,2,0)
        cust_tab_cont_panel_panel.addWidget(order_b_act_panel,3,0)
        cust_tab_cont_panel.setLayout(cust_tab_cont_panel_panel)

        if self.model.customer_id == '0':
            curr_index = self.cust_order_tab.addTab(cust_tab_cont_panel, cust_name)
        else:
            curr_index = self.cust_order_tab.addTab(cust_tab_cont_panel, self.model.verified_cust_icon, cust_name)


        self.model.append_cust_tab_cont_var(
            cust_name=cust_name,
            txn_type=txn_type,
            order_list_table=order_list_table,
            order_txn_type_label=order_a_txn_type_label,
            order_clr_list_button=order_a_clr_list_button,
            order_subtotal_value=order_subtotal_label.text().replace('₱',''),
            order_discount_value=order_discount_label.text().replace('₱',''),
            order_tax_value=order_tax_label.text().replace('₱',''),
            order_total_value=order_total_label.text().replace('₱',''),
            order_subtotal_label=order_subtotal_label,
            order_discount_label=order_discount_label,
            order_tax_label=order_tax_label,
            order_total_label=order_total_label,
            order_discard_button=order_discard_button,
            order_unlocked_button=order_unlocked_button,
            order_locked_button=order_locked_button,
            order_save_button=order_save_button,
            order_pay_button=order_pay_button
        )
        
        self.cust_order_tab.setCurrentIndex(curr_index)
        self.model.i = self.cust_order_tab.currentIndex()


        print('cust_name:', self.model.cust_name)
        print('txn_type:', self.model.txn_type)
        print('order_list_table:', self.model.order_list_table)
        print('order_txn_type_label:', self.model.order_txn_type_label)
        print('order_clr_list_button:', self.model.order_clr_list_button)
        print('order_subtotal:', self.model.order_subtotal)
        print('order_discount:', self.model.order_discount)
        print('order_tax:', self.model.order_tax)
        print('order_total:', self.model.order_total)
        print('order_subtotal_label:', self.model.order_subtotal_label)
        print('order_discount_label:', self.model.order_discount_label)
        print('order_tax_label:', self.model.order_tax_label)
        print('order_total_label:', self.model.order_total_label)
        print('order_discard_button:', self.model.order_discard_button)
        print('order_unlocked_button:', self.model.order_unlocked_button)
        print('order_locked_button:', self.model.order_locked_button)
        print('order_save_button:', self.model.order_save_button)
        print('order_pay_button:', self.model.order_pay_button)
        pass
    def populate_b_panel_combo_box(self):
        self.add_order_cust_name_field.clear()
        self.add_order_txn_type_field.clear()

        self.add_order_cust_name_field.addItem('New customer')
        for cust_name in self.model.cust_name_list:
            self.add_order_cust_name_field.addItems(cust_name)
        
        self.add_order_txn_type_field.addItem('Retail')
        self.add_order_txn_type_field.addItem('Wholesale')
        pass
    def populate_prod_list_table(self, text_filter='', txn_type='Retail', curr_page=1):
        self.model.a_prod_list = self.model.schema.list_product(text_filter=text_filter, txn_type=txn_type, page_number=curr_page)
        self.model.b_prod_list = self.model.schema.list_product_via_promo(text_filter=text_filter, txn_type=txn_type, page_number=curr_page)

        self.a_prod_list_prev_button.setEnabled(self.model.curr_page > 1)
        self.b_prod_list_prev_button.setEnabled(self.model.curr_page > 1)
        
        self.a_prod_list_next_button.setEnabled(len(self.model.a_prod_list) == 30)
        self.b_prod_list_next_button.setEnabled(len(self.model.b_prod_list) == 30)

        self.a_prod_list_table.setRowCount(len(self.model.a_prod_list))
        self.b_prod_list_table.setRowCount(len(self.model.b_prod_list))

        for row_index, row_value in enumerate(self.model.a_prod_list):
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_panel_layout = MyHBoxLayout(object_name='table_act_panel_layout')
            self.table_atc_button = MyPushButton(object_name='table_atc_button', text='Add')
            self.table_view_button = MyPushButton(object_name='table_view_button', text='View')
            table_act_panel_layout.addWidget(self.table_atc_button)
            table_act_panel_layout.addWidget(self.table_view_button)
            table_act_panel.setLayout(table_act_panel_layout)

            self.table_atc_button.clicked.connect(lambda _, row_value=row_value: self.populate_via_atc(row_value=row_value))


            item_name = QTableWidgetItem(f"{row_value[1]}")
            brand = QTableWidgetItem(f"{row_value[4]}")
            sales_group = QTableWidgetItem(f"{row_value[5]}")
            price = QTableWidgetItem(f"{row_value[8]}")
            discount = QTableWidgetItem(f"{row_value[11]}")
                
            self.a_prod_list_table.setCellWidget(row_index, 0, table_act_panel)
            self.a_prod_list_table.setItem(row_index, 1, item_name)
            self.a_prod_list_table.setItem(row_index, 2, brand)
            self.a_prod_list_table.setItem(row_index, 3, sales_group)
            self.a_prod_list_table.setItem(row_index, 4, price)
            self.a_prod_list_table.setItem(row_index, 5, discount)
            pass
        for row_index, row_value in enumerate(self.model.b_prod_list):
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_panel_layout = MyHBoxLayout(object_name='table_act_panel_layout')
            self.table_atc_button = MyPushButton(object_name='table_atc_button', text='Add')
            self.table_view_button = MyPushButton(object_name='table_view_button', text='View')
            table_act_panel_layout.addWidget(self.table_atc_button)
            table_act_panel_layout.addWidget(self.table_view_button)
            table_act_panel.setLayout(table_act_panel_layout)

            item_name = QTableWidgetItem(f"{row_value[1]}")
            brand = QTableWidgetItem(f"{row_value[4]}")
            sales_group = QTableWidgetItem(f"{row_value[5]}")
            price = QTableWidgetItem(f"{row_value[8]}")
            discount = QTableWidgetItem(f"{row_value[11]}")
            promo = QTableWidgetItem(f"{row_value[10]}")
                
            self.b_prod_list_table.setCellWidget(row_index, 0, table_act_panel)
            self.b_prod_list_table.setItem(row_index, 1, item_name)
            self.b_prod_list_table.setItem(row_index, 2, brand)
            self.b_prod_list_table.setItem(row_index, 3, sales_group)
            self.b_prod_list_table.setItem(row_index, 4, price)
            self.b_prod_list_table.setItem(row_index, 5, discount)
            self.b_prod_list_table.setItem(row_index, 6, promo)
        pass

    def show_after_pymnt_panel(self): # REVIEW                   
        i = self.view.cust_order_tab.currentIndex()

        self.pymt_panel = MyDialog()
        self.pymt_panel_layout = MyGridLayout()
        self.pymt_panel.setLayout(self.pymt_panel_layout)
        
        print('test')
        pass
    def show_pymt_panel(self):
        i = self.cust_order_tab.currentIndex()

        self.pymt_panel = MyDialog()
        self.pymt_panel_layout = MyGridLayout()

        self.pymt_panel_head = MyGroupBox()
        self.pymt_panel_head_layout = MyHBoxLayout()
        self.pymt_back_button = MyPushButton(text='Back')
        self.pymt_panel_head_layout.addWidget(self.pymt_back_button)
        self.pymt_panel_head.setLayout(self.pymt_panel_head_layout)

        self.cash_drawer_panel = MyGroupBox()
        self.cash_drawer_panel_layout = MyVBoxLayout()

        self.amount_tendered_panel = MyGroupBox()
        self.amount_tendered_panel_layout = MyGridLayout()
        self.amount_tendered_label = MyLabel(text='Amount tendered')
        self.amount_tendered_field = MyLineEdit()
        self.show_numpad_button = MyPushButton(object_name='show_numpad_button', text='Show')
        self.hide_numpad_button = MyPushButton(object_name='hide_numpad_button', text='Hide')
        self.amount_tendered_panel_layout.addWidget(self.amount_tendered_label,0,0,1,2)
        self.amount_tendered_panel_layout.addWidget(self.amount_tendered_field,1,0)
        self.amount_tendered_panel_layout.addWidget(self.show_numpad_button,1,2)
        self.amount_tendered_panel_layout.addWidget(self.hide_numpad_button,1,2)
        self.amount_tendered_panel.setLayout(self.amount_tendered_panel_layout)

        self.numpad_panel = MyGroupBox(object_name='numpad_panel') # TODO                     
        self.numpad_panel_layout = MyGridLayout()
        self.numpad_button: List[QPushButton] = [
            MyPushButton(text='1'),
            MyPushButton(text='2'),
            MyPushButton(text='3'),
            MyPushButton(text='4'),
            MyPushButton(text='5'),
            MyPushButton(text='6'),
            MyPushButton(text='7'),
            MyPushButton(text='8'),
            MyPushButton(text='9'),
            MyPushButton(text=''),
            MyPushButton(text='0'),
            MyPushButton(text='')
        ]
        self.numpad_panel_layout.addWidget(self.numpad_button[0],0,0)
        self.numpad_panel_layout.addWidget(self.numpad_button[1],0,1)
        self.numpad_panel_layout.addWidget(self.numpad_button[2],0,2)
        self.numpad_panel_layout.addWidget(self.numpad_button[3],1,0)
        self.numpad_panel_layout.addWidget(self.numpad_button[4],1,1)
        self.numpad_panel_layout.addWidget(self.numpad_button[5],1,2)
        self.numpad_panel_layout.addWidget(self.numpad_button[6],2,0)
        self.numpad_panel_layout.addWidget(self.numpad_button[7],2,1)
        self.numpad_panel_layout.addWidget(self.numpad_button[8],2,2)
        self.numpad_panel_layout.addWidget(self.numpad_button[9],3,0)
        self.numpad_panel_layout.addWidget(self.numpad_button[10],3,1)
        self.numpad_panel_layout.addWidget(self.numpad_button[11],3,2)
        self.numpad_panel.setLayout(self.numpad_panel_layout)

        self.cash_drawer_act_panel = MyGroupBox()
        self.cash_drawer_act_panel_layout = MyHBoxLayout()
        self.pay_cash_button = MyPushButton(text='Cash')
        self.pay_points_button = MyPushButton(text='Points') 
        self.cash_drawer_act_panel_layout.addWidget(self.pay_cash_button)
        self.cash_drawer_act_panel_layout.addWidget(self.pay_points_button)
        self.cash_drawer_act_panel.setLayout(self.cash_drawer_act_panel_layout)

        self.cash_drawer_panel_layout.addWidget(self.amount_tendered_panel)
        self.cash_drawer_panel_layout.addWidget(self.numpad_panel)
        self.cash_drawer_panel_layout.addWidget(self.cash_drawer_act_panel)
        self.cash_drawer_panel.setLayout(self.cash_drawer_panel_layout)

        self.cust_info_panel = MyGroupBox()
        self.cust_info_panel_layout = MyFormLayout()
        self.cust_info_name_label = MyLabel(text=f"test")
        self.cust_info_phone_label = MyLabel(text=f"test")
        self.cust_info_loy_points_label = MyLabel(text=f"test")
        self.cust_info_panel_layout.addRow('Customer Name:', self.cust_info_name_label)
        self.cust_info_panel_layout.addRow('Phone:', self.cust_info_phone_label)
        self.cust_info_panel_layout.addRow('Loyalty points:', self.cust_info_loy_points_label)
        self.cust_info_panel.setLayout(self.cust_info_panel_layout)


        self.fin_cust_order_panel = MyGroupBox()
        self.fin_cust_order_panel_layout = MyVBoxLayout()

        self.fin_order_summ_panel = MyGroupBox()
        self.fin_order_summ_panel_layout = MyFormLayout()

        self.fin_subtotal_label = MyLabel(object_name='fin_subtotal_label', text=f"₱{self.model.order_subtotal[i]}")
        self.fin_discount_label = MyLabel(object_name='fin_discount_label', text=f"₱{self.model.order_discount[i]}")
        self.fin_tax_label = MyLabel(object_name='fin_tax_label', text=f"₱{self.model.order_tax[i]}")
        self.fin_total_label = MyLabel(object_name='fin_total_label', text=f"₱{self.model.order_total[i]}")

        self.fin_order_summ_panel_layout.addRow('Subtotal:', self.fin_subtotal_label)
        self.fin_order_summ_panel_layout.addRow('Discount:', self.fin_discount_label)
        self.fin_order_summ_panel_layout.addRow('Tax:', self.fin_tax_label)
        self.fin_order_summ_panel_layout.addRow('Total:', self.fin_total_label)
        self.fin_order_summ_panel.setLayout(self.fin_order_summ_panel_layout)

        self.fin_cust_order_panel_layout.addWidget(self.fin_order_summ_panel)
        self.fin_cust_order_panel.setLayout(self.fin_cust_order_panel_layout)


        self.pymt_panel_layout.addWidget(self.pymt_panel_head,0,0,1,4)
        self.pymt_panel_layout.addWidget(self.cash_drawer_panel,1,0)
        self.pymt_panel_layout.addWidget(self.fin_cust_order_panel,1,1,2,3)
        self.pymt_panel_layout.addWidget(self.cust_info_panel,2,0)
        self.pymt_panel.setLayout(self.pymt_panel_layout)
        pass
    def show_c_panel(self):
        self.c_panel = MyGroupBox(object_name='c_panel')
        self.c_panel_layout = MyHBoxLayout(object_name='c_panel_layout')

        self.curr_user_label = MyLabel(object_name='curr_user_label', text=f"Current user: {self.model.curr_user}")
        self.total_cust_order_label = MyLabel(object_name='total_cust_order_label', text=f"Pending order: {self.cust_order_tab.count()}")
        self.total_prod_label = MyLabel(object_name='total_prod_label', text=f"Total product: {self.model.total_prod}")
        self.c_panel_layout.addWidget(self.curr_user_label)
        self.c_panel_layout.addWidget(self.total_cust_order_label)
        self.c_panel_layout.addWidget(self.total_prod_label)
        
        self.c_panel.setLayout(self.c_panel_layout)
        pass
    def show_b_panel(self):
        # info: shows b panel (panel on the right side) 
        self.b_panel = MyGroupBox(object_name='b_panel')
        self.b_panel_layout = MyGridLayout(object_name='b_panel_layout')

        self.add_order_act_panel = MyGroupBox(object_name='add_order_act_panel')
        self.add_order_act_panel_layout = MyHBoxLayout(object_name='add_order_act_panel_layout')
        self.add_order_cust_name_field = MyComboBox(object_name='add_order_cust_name_field')
        self.add_order_txn_type_field = MyComboBox(object_name='add_order_txn_type_field')
        self.add_order_button = MyPushButton(object_name='add_order_button', text='Add')
        self.load_order_button = MyPushButton(object_name='load_order_button', text='Load')
        self.add_order_act_panel_layout.addWidget(self.add_order_cust_name_field)
        self.add_order_act_panel_layout.addWidget(self.add_order_txn_type_field)
        self.add_order_act_panel_layout.addWidget(self.add_order_button)
        self.add_order_act_panel_layout.addWidget(self.load_order_button)
        self.add_order_act_panel.setLayout(self.add_order_act_panel_layout)

        self.cust_order_tab = MyTabWidget(object_name='cust_order_tab')

        self.b_panel_layout.addWidget(self.add_order_act_panel)
        self.b_panel_layout.addWidget(self.cust_order_tab)
        self.b_panel.setLayout(self.b_panel_layout)

        self.populate_b_panel_combo_box()
        self.populate_cust_tab()
        pass
    def show_a_panel(self):
        self.a_panel = MyGroupBox(object_name='a_panel')
        self.a_panel_layout = MyGridLayout(object_name='a_panel_layout')
        
        self.text_filter_panel = MyGroupBox(object_name='text_filter_panel')
        self.text_filter_panel_layout = MyHBoxLayout(object_name='text_filter_panel_layout')
        self.text_filter_field = MyLineEdit(object_name='text_filter_field')
        self.text_filter_button = MyPushButton(object_name='text_filter_button', text='Filter')
        self.text_filter_panel_layout.addWidget(self.text_filter_field)
        self.text_filter_panel_layout.addWidget(self.text_filter_button)
        self.text_filter_panel.setLayout(self.text_filter_panel_layout)
        self.barcode_scan_panel = MyGroupBox(object_name='barcode_scan_panel')
        self.barcode_scan_panel_layout = MyHBoxLayout(object_name='barcode_scan_panel_layout')
        self.barcode_scan_field = MyLineEdit(object_name='barcode_scan_field')
        self.barcode_scan_untoggled_button = MyPushButton(object_name='barcode_scan_untoggled_button', text='Untoggled')
        self.barcode_scan_toggled_button = MyPushButton(object_name='barcode_scan_toggled_button', text='Toggled')
        self.barcode_scan_panel_layout.addWidget(self.barcode_scan_field)
        self.barcode_scan_panel_layout.addWidget(self.barcode_scan_untoggled_button)
        self.barcode_scan_panel_layout.addWidget(self.barcode_scan_toggled_button)
        self.barcode_scan_panel.setLayout(self.barcode_scan_panel_layout)
        
        self.prod_list_tab = MyTabWidget(object_name='prod_list_tab')
        
        self.a_prod_list_panel = MyGroupBox(object_name='a_prod_list_panel')
        self.a_prod_list_panel_layout = MyVBoxLayout(object_name='a_prod_list_panel_layout')
        self.a_prod_list_table = MyTableWidget(object_name='a_prod_list_table')
        self.a_prod_list_act_panel = MyGroupBox(object_name='a_prod_list_act_panel')
        self.a_prod_list_act_panel_layout = MyHBoxLayout(object_name='a_prod_list_act_panel_layout')
        self.a_prod_list_prev_button = MyPushButton(object_name='a_prod_list_prev_button', text='Prev')
        self.a_prod_list_curr_count_label = MyLabel(object_name='a_prod_list_curr_count_label', text=f"{self.model.curr_page}/{self.model.total_page}")
        self.a_prod_list_next_button = MyPushButton(object_name='a_prod_list_next_button', text='Next')
        self.a_prod_list_act_panel_layout.addWidget(self.a_prod_list_prev_button)
        self.a_prod_list_act_panel_layout.addWidget(self.a_prod_list_curr_count_label)
        self.a_prod_list_act_panel_layout.addWidget(self.a_prod_list_next_button)
        self.a_prod_list_act_panel.setLayout(self.a_prod_list_act_panel_layout)
        self.a_prod_list_panel_layout.addWidget(self.a_prod_list_table)
        self.a_prod_list_panel_layout.addWidget(self.a_prod_list_act_panel)
        self.a_prod_list_panel.setLayout(self.a_prod_list_panel_layout)
        self.b_prod_list_panel = MyGroupBox(object_name='b_prod_list_panel')
        self.b_prod_list_panel_layout = MyVBoxLayout(object_name='b_prod_list_panel_layout')
        self.b_prod_list_table = MyTableWidget(object_name='b_prod_list_table')
        self.b_prod_list_act_panel = MyGroupBox(object_name='b_prod_list_act_panel')
        self.b_prod_list_act_panel_layout = MyHBoxLayout(object_name='b_prod_list_act_panel_layout')
        self.b_prod_list_prev_button = MyPushButton(object_name='b_prod_list_prev_button', text='Prev')
        self.b_prod_list_curr_count_label = MyLabel(object_name='b_prod_list_curr_count_label', text=f"{self.model.curr_page}/{self.model.total_page}")
        self.b_prod_list_next_button = MyPushButton(object_name='b_prod_list_next_button', text='Next')
        self.b_prod_list_act_panel_layout.addWidget(self.b_prod_list_prev_button)
        self.b_prod_list_act_panel_layout.addWidget(self.b_prod_list_curr_count_label)
        self.b_prod_list_act_panel_layout.addWidget(self.b_prod_list_next_button)
        self.b_prod_list_act_panel.setLayout(self.b_prod_list_act_panel_layout)
        self.b_prod_list_panel_layout.addWidget(self.b_prod_list_table)
        self.b_prod_list_panel_layout.addWidget(self.b_prod_list_act_panel)
        self.b_prod_list_panel.setLayout(self.b_prod_list_panel_layout)
        
        self.prod_list_tab.addTab(self.a_prod_list_panel, 'Overview')
        self.prod_list_tab.addTab(self.b_prod_list_panel, 'On sale')

        self.a_panel_layout.addWidget(self.text_filter_panel,0,0)
        self.a_panel_layout.addWidget(self.barcode_scan_panel,0,1)
        self.a_panel_layout.addWidget(self.prod_list_tab,1,0,1,2)
        self.a_panel.setLayout(self.a_panel_layout)
        pass

    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(object_name='main_panel_layout')

        self.show_a_panel()
        self.show_b_panel()
        self.show_c_panel()
        self.show_pymt_panel()
        
        self.main_panel_layout.addWidget(self.a_panel,0,0)
        self.main_panel_layout.addWidget(self.b_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.c_panel,1,0)
        self.setLayout(self.main_panel_layout)

class MySalesController:
    def __init__(self, model: MySalesModel, view: MySalesView):
        self.model = model
        self.view = view

        self.set_connections()

    def set_connections(self):
        i = self.view.cust_order_tab.currentIndex()

        self.view.text_filter_field.textChanged.connect(self.on_text_filter_field_text_changed)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        
        self.view.barcode_scan_untoggled_button.clicked.connect(lambda: self.on_barcode_scan_toggle_button_clicked(action='Toggle'))
        self.view.barcode_scan_toggled_button.clicked.connect(lambda: self.on_barcode_scan_toggle_button_clicked(action='Untoggle'))

        for row_index, row_value in enumerate(self.model.b_prod_list):
            self.view.table_atc_button.clicked.connect(lambda _, row_value=row_value: self.view.populate_via_atc(row_value=row_value))

        self.view.a_prod_list_prev_button.clicked.connect(lambda: self.on_prod_list_pgtn_button_clicked(action='prev'))
        self.view.a_prod_list_next_button.clicked.connect(lambda: self.on_prod_list_pgtn_button_clicked(action='next'))
        self.view.b_prod_list_prev_button.clicked.connect(lambda: self.on_prod_list_pgtn_button_clicked(action='prev'))
        self.view.b_prod_list_next_button.clicked.connect(lambda: self.on_prod_list_pgtn_button_clicked(action='next'))

        self.view.prod_list_tab.currentChanged.connect(self.on_prod_list_tab_current_changed)

        self.view.add_order_button.clicked.connect(self.view.populate_cust_tab)
        self.view.add_order_button.clicked.connect(self.on_add_order_button_clicked)
        self.view.cust_order_tab.currentChanged.connect(self.on_cust_order_tab_current_changed)


        self.model.order_unlocked_button[i].clicked.connect(lambda: self.on_order_lock_button_clicked(action='unlocked'))
        self.model.order_locked_button[i].clicked.connect(lambda: self.on_order_lock_button_clicked(action='locked'))
        
        self.view.show_numpad_button.clicked.connect(lambda: self.on_numpad_button_clicked(action='show'))
        self.view.hide_numpad_button.clicked.connect(lambda: self.on_numpad_button_clicked(action='hide'))

        pass

    def on_text_filter_button_clicked(self):
        pass
    def on_text_filter_field_text_changed(self):
        pass
    def on_prod_list_pgtn_button_clicked(self, action):
        i = self.view.cust_order_tab.currentIndex()
        
        if action == 'prev':
            if self.model.curr_page > 1:
                self.model.curr_page -= 1
                self.view.a_prod_list_curr_count_label.setText(f"{self.model.curr_page}/{self.model.total_page}")
                self.view.b_prod_list_curr_count_label.setText(f"{self.model.curr_page}/{self.model.total_page}")

            self.view.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), txn_type=self.model.txn_type[i], curr_page=self.model.curr_page)
            pass
        elif action == 'next':
            self.model.curr_page += 1
            self.view.a_prod_list_curr_count_label.setText(f"{self.model.curr_page}/{self.model.total_page}")
            self.view.b_prod_list_curr_count_label.setText(f"{self.model.curr_page}/{self.model.total_page}")
            
            self.view.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), txn_type=self.model.txn_type[i], curr_page=self.model.curr_page)
            pass
    def on_prod_list_tab_current_changed(self):
        i = self.view.cust_order_tab.currentIndex()
        
        self.model.curr_page = 1
        self.view.a_prod_list_curr_count_label.setText(f"{self.model.curr_page}/{self.model.total_page}")
        self.view.b_prod_list_curr_count_label.setText(f"{self.model.curr_page}/{self.model.total_page}")

        self.view.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), txn_type=self.model.txn_type[i], curr_page=self.model.curr_page)

    def on_add_order_button_clicked(self):
        self.view.total_cust_order_label.setText(f"Pending order: {self.view.cust_order_tab.count()+1}")
        pass
    def on_cust_order_tab_current_changed(self):
        i = self.view.cust_order_tab.currentIndex()

        self.view.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), txn_type=self.model.txn_type[i], curr_page=self.model.curr_page)
        print('cust order index:', i)
        print('self.model.order_pay_button[i]:', self.model.order_pay_button[i])

    def on_barcode_scan_toggle_button_clicked(self, action):
        if action == 'Toggle':
            self.view.barcode_scan_untoggled_button.hide()
            self.view.barcode_scan_toggled_button.show()

            self.view.barcode_scan_field.show()
            pass
        elif action == 'Untoggle':
            self.view.barcode_scan_untoggled_button.show()
            self.view.barcode_scan_toggled_button.hide()

            self.view.barcode_scan_field.hide()
            pass
    
    def on_order_lock_button_clicked(self, action):
        i = self.view.cust_order_tab.currentIndex()

        if action == 'unlocked':
            self.model.order_unlocked_button[i].hide()
            self.model.order_locked_button[i].show()

            self.model.order_list_table[i].setDisabled(True)
            self.model.order_clr_list_button[i].setDisabled(True)
            self.model.order_subtotal_label[i].setDisabled(True)
            self.model.order_discount_label[i].setDisabled(True)
            self.model.order_tax_label[i].setDisabled(True)
            self.model.order_total_label[i].setDisabled(True)
            self.model.order_discard_button[i].setDisabled(True)
            self.model.order_save_button[i].setDisabled(True)
            self.model.order_pay_button[i].setDisabled(True)
            pass
        elif action == 'locked':
            self.model.order_unlocked_button[i].show()
            self.model.order_locked_button[i].hide()

            self.model.order_list_table[i].setDisabled(False)
            self.model.order_clr_list_button[i].setDisabled(False)
            self.model.order_subtotal_label[i].setDisabled(False)
            self.model.order_discount_label[i].setDisabled(False)
            self.model.order_tax_label[i].setDisabled(False)
            self.model.order_total_label[i].setDisabled(False)
            self.model.order_discard_button[i].setDisabled(False)
            self.model.order_save_button[i].setDisabled(False)
            self.model.order_pay_button[i].setDisabled(False)

    def on_order_pay_button_clicked(self):
        print('test pay')
        self.view.pymt_panel.exec()
        pass

    def on_numpad_button_clicked(self, action):
        if action == 'show':
            self.view.numpad_panel.show()
            self.view.show_numpad_button.hide()
            self.view.hide_numpad_button.show()
            pass
        if action == 'hide':
            self.view.numpad_panel.hide()
            self.view.show_numpad_button.show()
            self.view.hide_numpad_button.hide()
            pass


if __name__ == ('__main__'):
    app = QApplication(sys.argv)

    schema = SalesSchema()

    model = MySalesModel(schema)
    view = MySalesView(model)
    controller = MySalesController(model, view)

    view.show()
    sys.exit(app.exec())
