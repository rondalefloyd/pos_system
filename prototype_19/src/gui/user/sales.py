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
from src.core.receipt_printer import *

from database.user.sales import *
from widget.user.sales import *

class MySalesModel: # IDEA: can't use 'MySalesView' and 'MySalesController' attributes
    def __init__(self, schema: SalesSchema):
        self.schema = schema

        self.page_number = 1
        self.total_page = [
            schema.count_product_list_total_pages(),
            schema.count_product_list_via_promo_total_pages(),
        ]

        self.new_quantity = 0
        self.new_price = 0
        
        self.save_file_path = 'G:' + f"/My Drive/saved_orders/"
        # IDEA: container
        self.set_cust_order_data()


    def set_cust_order_data(self):
        self.cust_order_name_values = []
        self.cust_order_type_values = []

        self.cust_order_tables: List[MyTableWidget] = []

        self.cust_order_subtotal_values = []
        self.cust_order_discount_values = []
        self.cust_order_tax_values = []
        self.cust_order_total_values = []

        self.cust_order_type_labels: List[MyLabel] = []
        self.cust_order_clear_buttons: List[MyPushButton] = []
        self.cust_order_subtotal_labels: List[MyLabel] = []
        self.cust_order_discount_labels: List[MyLabel] = []
        self.cust_order_tax_labels: List[MyLabel] = []
        self.cust_order_total_labels: List[MyLabel] = []
        self.cust_order_discard_buttons: List[MyPushButton] = []
        self.cust_order_restrict_buttons: List[MyPushButton] = []
        self.cust_order_save_buttons: List[MyPushButton] = []
        self.cust_order_pay_buttons: List[MyPushButton] = []

        self.cust_order_item_data = []
        self.cust_order_summary_data = []

        self.cust_info_name = ''
        self.cust_info_points = 0
        self.cust_info_phone = ''
        self.cust_order_amount_tendered_value = 0
        self.cust_order_change_value = 0

    def append_cust_order_data(
        self,
        cust_order_name_value,
        cust_order_type_value,
        cust_order_subtotal_value,
        cust_order_discount_value,
        cust_order_tax_value,
        cust_order_total_value,
        cust_order_table,
        cust_order_type_label,
        cust_order_clear_button,
        cust_order_subtotal_label,
        cust_order_discount_label,
        cust_order_tax_label,
        cust_order_total_label,
        cust_order_discard_button,
        cust_order_restrict_button,
        cust_order_save_button,
        cust_order_pay_button,
    ):
        self.cust_order_name_values.append(cust_order_name_value)
        self.cust_order_type_values.append(cust_order_type_value)
        
        self.cust_order_subtotal_values.append(cust_order_subtotal_value)
        self.cust_order_discount_values.append(cust_order_discount_value)
        self.cust_order_tax_values.append(cust_order_tax_value)
        self.cust_order_total_values.append(cust_order_total_value)

        self.cust_order_tables.append(cust_order_table)
        self.cust_order_type_labels.append(cust_order_type_label)
        self.cust_order_clear_buttons.append(cust_order_clear_button)
        self.cust_order_subtotal_labels.append(cust_order_subtotal_label)
        self.cust_order_discount_labels.append(cust_order_discount_label)
        self.cust_order_tax_labels.append(cust_order_tax_label)
        self.cust_order_total_labels.append(cust_order_total_label)
        self.cust_order_discard_buttons.append(cust_order_discard_button)
        self.cust_order_restrict_buttons.append(cust_order_restrict_button)
        self.cust_order_save_buttons.append(cust_order_save_button)
        self.cust_order_pay_buttons.append(cust_order_pay_button)
        pass
    def append_cust_order_item_data(self, cust_order_item_data):
        self.cust_order_item_data.append(cust_order_item_data)
        pass
    def append_cust_order_summary_data(
        self,
        cust_order_subtotal_value,
        cust_order_discount_value,
        cust_order_tax_value,
        cust_order_total_value,
        cust_order_amount_tendered_value,
        cust_order_change_value,
    ):
        self.cust_order_summary_data.append([
            cust_order_subtotal_value,
            cust_order_discount_value,
            cust_order_tax_value,
            cust_order_total_value,
            cust_order_amount_tendered_value,
            cust_order_change_value,
        ])

    def remove_cust_order_data(self, i):
        self.cust_order_name_values.remove(self.cust_order_name_values[i]),
        self.cust_order_type_values.remove(self.cust_order_type_values[i]),

        self.cust_order_tables.remove(self.cust_order_tables[i]),

        self.cust_order_subtotal_values.remove(self.cust_order_subtotal_values[i]),
        self.cust_order_discount_values.remove(self.cust_order_discount_values[i]),
        self.cust_order_tax_values.remove(self.cust_order_tax_values[i]),
        self.cust_order_total_values.remove(self.cust_order_total_values[i]),

        self.cust_order_type_labels.remove(self.cust_order_type_labels[i]),
        self.cust_order_clear_buttons.remove(self.cust_order_clear_buttons[i]),
        self.cust_order_subtotal_labels.remove(self.cust_order_subtotal_labels[i]),
        self.cust_order_discount_labels.remove(self.cust_order_discount_labels[i]),
        self.cust_order_tax_labels.remove(self.cust_order_tax_labels[i]),
        self.cust_order_total_labels.remove(self.cust_order_total_labels[i]),
        self.cust_order_discard_buttons.remove(self.cust_order_discard_buttons[i]),
        self.cust_order_restrict_buttons.remove(self.cust_order_restrict_buttons[i]),
        self.cust_order_save_buttons.remove(self.cust_order_save_buttons[i]),
        self.cust_order_pay_buttons.remove(self.cust_order_pay_buttons[i]),

    def verify_customer(self, i):
        try:
            self.customer_id = schema.get_customer_id(customer=self.cust_order_name_values[i])
            
            selected_cust = schema.list_customer(customer_id=self.customer_id)

            for cust_i, cust_v in enumerate(selected_cust):
                self.cust_info_name = f"{cust_v[0]}"
                self.cust_info_points = '[unavailable]' # f"{cust_v[1]}"
                self.cust_info_phone = f"{cust_v[2]}"
        except Exception as e:
            self.customer_id = None
            self.cust_info_name = '[unavailable]'
            self.cust_info_points = '[unavailable]'
            self.cust_info_phone = '[unavailable]'

        print('customer_id:', self.customer_id)

class MySalesView(MyWidget): # IDEA: can only use 'MySalesModel' attributes
    def __init__(self, model: MySalesModel):
        super().__init__(object_name='my_sales_view')

        self.model = model
        
        self.show_main_panel()

    def show_main_panel(self):
        self.show_panel_box_a()
        self.show_panel_box_b()
        self.show_panel_box_c()

        main_panel_layout = MyGridLayout()

        main_panel_layout.addWidget(self.panel_a_box,0,0)
        main_panel_layout.addWidget(self.panel_b_box,0,1,2,1)
        main_panel_layout.addWidget(self.panel_c_box,1,0)
        self.setLayout(main_panel_layout)
        pass

    def show_panel_box_a(self):
        self.panel_a_box = MyGroupBox()
        self.panel_a_layout = MyGridLayout()

        self.text_filter_field = MyLineEdit()
        self.text_filter_button = MyPushButton(text='Filter')
        self.text_filter_box = MyGroupBox()
        self.text_filter_layout = MyHBoxLayout()
        self.text_filter_layout.addWidget(self.text_filter_field)
        self.text_filter_layout.addWidget(self.text_filter_button)
        self.text_filter_box.setLayout(self.text_filter_layout)

        self.barcode_scan_field = MyLineEdit(object_name='barcode_scan_field')
        self.barcode_scan_button = [
            MyPushButton(object_name='barcode_scan_button_toggle', text='Turn on'),
            MyPushButton(object_name='barcode_scan_button_untoggle', text='Turn off'),
        ]
        self.barcode_scan_box = MyGroupBox()
        self.barcode_scan_layout = MyHBoxLayout()
        self.barcode_scan_layout.addWidget(self.barcode_scan_field)
        self.barcode_scan_layout.addWidget(self.barcode_scan_button[0])
        self.barcode_scan_layout.addWidget(self.barcode_scan_button[1])
        self.barcode_scan_box.setLayout(self.barcode_scan_layout)

        self.prod_list_tab = MyTabWidget()
        self.prod_list_table = [
            MyTableWidget(object_name='prod_list_table_a'),
            MyTableWidget(object_name='prod_list_table_b'),
        ]
        self.prod_list_pag_prev_button = [
            MyPushButton(text='Prev'),
            MyPushButton(text='Prev'),
        ]
        self.prod_list_pag_page_label = [
            MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page[0]}"),
            MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page[1]}"),
        ]
        self.prod_list_pag_next_button = [
            MyPushButton(text='Next'),
            MyPushButton(text='Next'),
        ]

        self.prod_list_pag_box = [
            MyGroupBox(),
            MyGroupBox(),
        ]
        self.prod_list_pag_layout = [
            MyHBoxLayout(),
            MyHBoxLayout(),
        ]
        self.prod_list_box = [
            MyGroupBox(),
            MyGroupBox(),
        ]
        self.prod_list_layout = [
            MyVBoxLayout(),
            MyVBoxLayout(),
        ]

        self.prod_list_pag_layout[0].addWidget(self.prod_list_pag_prev_button[0])
        self.prod_list_pag_layout[0].addWidget(self.prod_list_pag_page_label[0])
        self.prod_list_pag_layout[0].addWidget(self.prod_list_pag_next_button[0])
        self.prod_list_pag_box[0].setLayout(self.prod_list_pag_layout[0])

        self.prod_list_layout[0].addWidget(self.prod_list_table[0])
        self.prod_list_layout[0].addWidget(self.prod_list_pag_box[0])
        self.prod_list_box[0].setLayout(self.prod_list_layout[0])
        
        self.prod_list_pag_layout[1].addWidget(self.prod_list_pag_prev_button[1])
        self.prod_list_pag_layout[1].addWidget(self.prod_list_pag_page_label[1])
        self.prod_list_pag_layout[1].addWidget(self.prod_list_pag_next_button[1])
        self.prod_list_pag_box[1].setLayout(self.prod_list_pag_layout[1])

        self.prod_list_layout[1].addWidget(self.prod_list_table[1])
        self.prod_list_layout[1].addWidget(self.prod_list_pag_box[1])
        self.prod_list_box[1].setLayout(self.prod_list_layout[1])

        self.prod_list_tab.addTab(self.prod_list_box[0], 'Overview')
        self.prod_list_tab.addTab(self.prod_list_box[1], 'On sale')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.barcode_scan_box,0,1)
        self.panel_a_layout.addWidget(self.prod_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def show_panel_box_b(self):
        self.panel_b_box = MyGroupBox()
        self.panel_b_layout = MyVBoxLayout()

        self.add_cust_name_sel_field = MyComboBox()
        self.add_cust_order_type_field = MyComboBox()
        self.add_cust_new_tab_button = MyPushButton(text='Add')
        self.add_cust_load_button = MyPushButton(object_name='add_cust_load_button', text='Load')
        self.add_cust_box = MyGroupBox()
        self.add_cust_layout = MyHBoxLayout()
        self.add_cust_layout.addWidget(self.add_cust_name_sel_field)
        self.add_cust_layout.addWidget(self.add_cust_order_type_field)
        self.add_cust_layout.addWidget(self.add_cust_new_tab_button)
        self.add_cust_layout.addWidget(self.add_cust_load_button)
        self.add_cust_box.setLayout(self.add_cust_layout)

        self.cust_order_tab = MyTabWidget()

        # IDEA

        self.panel_b_layout.addWidget(self.add_cust_box)
        self.panel_b_layout.addWidget(self.cust_order_tab)
        self.panel_b_box.setLayout(self.panel_b_layout)
        pass
    def show_panel_box_c(self):
        self.panel_c_box = MyGroupBox()
        self.panel_c_layout = MyHBoxLayout()

        self.current_user_label = MyLabel(text=f"Current user: ?")
        self.pending_order_label = MyLabel(text=f"Pending order: {self.cust_order_tab.count()}")
        self.available_prod_label = MyLabel(text=f"Available product: {schema.count_product()}")
        self.panel_c_layout.addWidget(self.current_user_label)
        self.panel_c_layout.addWidget(self.pending_order_label)
        self.panel_c_layout.addWidget(self.available_prod_label)
        self.panel_c_box.setLayout(self.panel_c_layout)
        pass

class MySalesController: # IDEA: can use 'MySalesModel' and 'MySalesView' attributes
    def __init__(self, model: MySalesModel, view: MySalesView):
        self.model = model
        self.view = view

        self.populate_prod_list_table()
        self.populate_cust_order_field()
        self.populate_cust_order_tab() if self.view.cust_order_tab.count() == 0 else None

        self.set_panel_box_a_conn()
        self.set_panel_box_b_conn()
        self.set_panel_box_c_conn()

    def populate_prod_list_table(self, text_filter='', order_type='Retail', page_number=1):
        if self.view.cust_order_tab.count() > 0:
            self.prod_list_data = [
                schema.list_product(text_filter, order_type, page_number),
                schema.list_product_via_promo(text_filter, order_type, page_number)
            ]

            self.view.prod_list_pag_page_label[0].setText(f"Page {self.model.page_number}/{self.model.total_page[0]}")
            self.view.prod_list_pag_page_label[1].setText(f"Page {self.model.page_number}/{self.model.total_page[1]}")

            self.view.prod_list_pag_prev_button[0].setEnabled(self.model.page_number > 1)
            self.view.prod_list_pag_next_button[0].setEnabled(len(self.prod_list_data[0]) == 30)

            self.view.prod_list_pag_prev_button[1].setEnabled(self.model.page_number > 1)
            self.view.prod_list_pag_next_button[1].setEnabled(len(self.prod_list_data[1]) == 30)

            self.view.prod_list_table[0].setRowCount(len(self.prod_list_data[0]))
            self.view.prod_list_table[1].setRowCount(len(self.prod_list_data[1]))
        
            for ai, av in enumerate(self.prod_list_data[0]):
                self.prod_list_add_button = MyPushButton(text='Add')
                self.prod_list_view_button = MyPushButton(text='View')
                prod_list_table_act_box = MyGroupBox()
                prod_list_table_act_layout = MyHBoxLayout()
                prod_list_table_act_layout.addWidget(self.prod_list_add_button)
                prod_list_table_act_layout.addWidget(self.prod_list_view_button)
                prod_list_table_act_box.setLayout(prod_list_table_act_layout)

                product = QTableWidgetItem(f"{av[1]}")
                brand = QTableWidgetItem(f"{av[4]}")
                sales_group = QTableWidgetItem(f"{av[5]}")
                price = QTableWidgetItem(f"{av[8]}")
                promo = QTableWidgetItem(f"{av[10]}")
                discount = QTableWidgetItem(f"{av[11]}")

                self.view.prod_list_table[0].setCellWidget(ai, 0, prod_list_table_act_box)
                self.view.prod_list_table[0].setItem(ai, 1, product)
                self.view.prod_list_table[0].setItem(ai, 2, brand)
                self.view.prod_list_table[0].setItem(ai, 3, sales_group)
                self.view.prod_list_table[0].setItem(ai, 4, price)
                self.view.prod_list_table[0].setItem(ai, 5, promo)
                self.view.prod_list_table[0].setItem(ai, 6, discount)

                self.prod_list_add_button.clicked.connect(lambda _, av=av: self.on_prod_list_add_button_clicked(row_v=av))
                self.prod_list_view_button.clicked.connect(lambda _, av=av: self.on_prod_list_view_button_clicked(row_v=av))
                pass
            for bi, bv in enumerate(self.prod_list_data[1]):
                
                self.prod_list_add_button = MyPushButton(text='Add')
                self.prod_list_view_button = MyPushButton(text='View')
                prod_list_table_act_box = MyGroupBox()
                prod_list_table_act_layout = MyHBoxLayout()
                prod_list_table_act_layout.addWidget(self.prod_list_add_button)
                prod_list_table_act_layout.addWidget(self.prod_list_view_button)
                prod_list_table_act_box.setLayout(prod_list_table_act_layout)

                product = QTableWidgetItem(f"{bv[1]}")
                brand = QTableWidgetItem(f"{bv[4]}")
                sales_group = QTableWidgetItem(f"{bv[5]}")
                price = QTableWidgetItem(f"{bv[8]}")
                promo = QTableWidgetItem(f"{bv[10]}")
                discount = QTableWidgetItem(f"{bv[11]}")

                self.view.prod_list_table[1].setCellWidget(bi, 0, prod_list_table_act_box)
                self.view.prod_list_table[1].setItem(bi, 1, product)
                self.view.prod_list_table[1].setItem(bi, 2, brand)
                self.view.prod_list_table[1].setItem(bi, 3, sales_group)
                self.view.prod_list_table[1].setItem(bi, 4, price)
                self.view.prod_list_table[1].setItem(bi, 5, promo)
                self.view.prod_list_table[1].setItem(bi, 6, discount)

                self.prod_list_add_button.clicked.connect(lambda _, bv=bv: self.on_prod_list_add_button_clicked(row_v=bv))
                self.prod_list_view_button.clicked.connect(lambda _, bv=bv: self.on_prod_list_view_button_clicked(row_v=bv))
                pass
        else: 
            self.view.prod_list_pag_prev_button[0].setDisabled(True)
            self.view.prod_list_pag_next_button[0].setDisabled(True)
            
            self.view.prod_list_pag_prev_button[1].setDisabled(True)
            self.view.prod_list_pag_next_button[1].setDisabled(True)

            self.view.prod_list_pag_page_label[0].setText(f"Page 0/0")
            self.view.prod_list_pag_page_label[1].setText(f"Page 0/0")

            self.view.prod_list_table[0].setRowCount(0)
            self.view.prod_list_table[1].setRowCount(0)
        pass
    def populate_cust_order_field(self):
        self.cust_list_data = schema.list_customer()

        self.view.add_cust_name_sel_field.clear()
        self.view.add_cust_order_type_field.clear()

        self.view.add_cust_name_sel_field.addItem('Order')
        for cust in self.cust_list_data:
            self.view.add_cust_name_sel_field.addItem(cust[0])

        self.view.add_cust_order_type_field.addItem('Retail')
        self.view.add_cust_order_type_field.addItem('Wholesale')
        pass
    def populate_cust_order_tab(self):
        # FIXME: SHOULD BE IN A DIFFERENT FUNCTION
        self.cust_order_type_label = MyLabel(text=f"Order type: {self.view.add_cust_order_type_field.currentText()}")
        self.cust_order_clear_button = MyPushButton(text='Clear')
        self.cust_order_act_a_box = MyGroupBox()
        self.cust_order_act_a_layout = MyHBoxLayout()
        self.cust_order_act_a_layout.addWidget(self.cust_order_type_label)
        self.cust_order_act_a_layout.addWidget(self.cust_order_clear_button)
        self.cust_order_act_a_box.setLayout(self.cust_order_act_a_layout)

        self.cust_order_table = MyTableWidget(object_name='cust_order_table')
        
        self.cust_order_subtotal_value = 0
        self.cust_order_discount_value = 0
        self.cust_order_tax_value = 0
        self.cust_order_total_value = 0

        self.cust_order_subtotal_label = MyLabel(text=f"₱{self.cust_order_subtotal_value}")
        self.cust_order_discount_label = MyLabel(text=f"₱{self.cust_order_discount_value}")
        self.cust_order_tax_label = MyLabel(text=f"₱{self.cust_order_tax_value}")
        self.cust_order_total_label = MyLabel(text=f"₱{self.cust_order_total_value}")
        self.cust_order_summary_box = MyGroupBox()
        self.cust_order_summary_layout = MyFormLayout()
        self.cust_order_summary_layout.addRow('Subtotal:', self.cust_order_subtotal_label)
        self.cust_order_summary_layout.addRow('Discount:', self.cust_order_discount_label)
        self.cust_order_summary_layout.addRow('Tax:', self.cust_order_tax_label)
        self.cust_order_summary_layout.addRow('Total:', self.cust_order_total_label)
        self.cust_order_summary_box.setLayout(self.cust_order_summary_layout)

        self.cust_order_discard_button = MyPushButton(text='Discard')
        self.cust_order_restrict_button = [
            MyPushButton(object_name='cust_order_restrict_button_toggle', text='Lock'),
            MyPushButton(object_name='cust_order_restrict_button_untoggle', text='Unlock'),
        ]
        self.cust_order_save_button = MyPushButton(object_name='cust_order_save_button', text='Save')
        self.cust_order_pay_button = MyPushButton(text=f"Pay ₱{self.cust_order_total_value:.2f}")
        self.cust_order_act_b_box = MyGroupBox()
        self.cust_order_act_b_layout: List[MyVBoxLayout, MyHBoxLayout] = [
            MyVBoxLayout(),
            MyHBoxLayout(),
        ]
        self.cust_order_act_b_layout[1].addWidget(self.cust_order_discard_button)
        self.cust_order_act_b_layout[1].addWidget(self.cust_order_restrict_button[0])
        self.cust_order_act_b_layout[1].addWidget(self.cust_order_restrict_button[1])
        self.cust_order_act_b_layout[1].addWidget(self.cust_order_save_button)
        self.cust_order_act_b_layout[0].addLayout(self.cust_order_act_b_layout[1])
        self.cust_order_act_b_layout[0].addWidget(self.cust_order_pay_button)
        self.cust_order_act_b_box.setLayout(self.cust_order_act_b_layout[0])

        self.cust_order_box = MyGroupBox()
        self.cust_order_layout = MyVBoxLayout()
        self.cust_order_layout.addWidget(self.cust_order_act_a_box)
        self.cust_order_layout.addWidget(self.cust_order_table)
        self.cust_order_layout.addWidget(self.cust_order_summary_box)
        self.cust_order_layout.addWidget(self.cust_order_act_b_box)
        self.cust_order_box.setLayout(self.cust_order_layout)

        self.model.append_cust_order_data(
            self.view.add_cust_name_sel_field.currentText(),
            self.view.add_cust_order_type_field.currentText(),

            self.cust_order_subtotal_value,
            self.cust_order_discount_value,
            self.cust_order_tax_value,
            self.cust_order_total_value,

            self.cust_order_table,
            self.cust_order_type_label,
            self.cust_order_clear_button,
            self.cust_order_subtotal_label,
            self.cust_order_discount_label,
            self.cust_order_tax_label,
            self.cust_order_total_label,
            self.cust_order_discard_button,
            self.cust_order_restrict_button,
            self.cust_order_save_button,
            self.cust_order_pay_button,
        )

        new_i = self.view.cust_order_tab.addTab(self.cust_order_box, self.view.add_cust_name_sel_field.currentText())
        
        self.view.cust_order_tab.setCurrentIndex(new_i)
        self.view.add_cust_name_sel_field.setCurrentText('Order')
        self.view.pending_order_label.setText(f"Pending order: {self.view.cust_order_tab.count()}")
        
        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[new_i], page_number=self.model.page_number)

        self.cust_order_clear_button.clicked.connect(self.on_cust_order_clear_button_clicked)
        self.cust_order_discard_button.clicked.connect(self.on_cust_order_discard_button_clicked)

        self.cust_order_restrict_button[0].clicked.connect(lambda: self.on_cust_order_restrict_button_clicked(action='toggle'))
        self.cust_order_restrict_button[1].clicked.connect(lambda: self.on_cust_order_restrict_button_clicked(action='untoggle'))

        self.cust_order_save_button.clicked.connect(self.on_cust_order_save_button_clicked)
        self.cust_order_pay_button.clicked.connect(self.on_cust_order_pay_button_clicked)
        pass
    def populate_cash_drawer_dialog(self):
        i = self.view.cust_order_tab.currentIndex()
        self.model.verify_customer(i)
        
        self.cash_drawer_dialog = MyDialog(parent=self.view)
        self.cash_drawer_layout = MyGridLayout()

        self.numpad_keys_button: List[MyPushButton] = [
            [3,1, MyPushButton(text='0')],
            [0,0, MyPushButton(text='1')],
            [0,1, MyPushButton(text='2')],
            [0,2, MyPushButton(text='3')],
            [1,0, MyPushButton(text='4')],
            [1,1, MyPushButton(text='5')],
            [1,2, MyPushButton(text='6')],
            [2,0, MyPushButton(text='7')],
            [2,1, MyPushButton(text='8')],
            [2,2, MyPushButton(text='9')],
            [3,0, MyPushButton(text='Delete')],
            [3,2, MyPushButton(text='Clear')],
        ]
        self.numpad_box = MyGroupBox(object_name='numpad_box')
        self.numpad_layout = MyGridLayout()
        for row, col, numpad in self.numpad_keys_button:
            self.numpad_layout.addWidget(numpad,row,col)
        self.numpad_box.setLayout(self.numpad_layout)
        
        self.amount_tendered_label = MyLabel(text='Amount tendered:')
        self.amount_tendered_field = MyLineEdit()
        self.numpad_button = [
            MyPushButton(object_name='numpad_button_toggle', text='Turn on'),
            MyPushButton(object_name='numpad_button_untoggle', text='Turn off'),
        ]
        self.amount_tendered_box = MyGroupBox()
        self.amount_tendered_layout = MyGridLayout()
        self.amount_tendered_layout.addWidget(self.amount_tendered_label,0,0)
        self.amount_tendered_layout.addWidget(self.amount_tendered_field,1,0)
        self.amount_tendered_layout.addWidget(self.numpad_button[0],1,1)
        self.amount_tendered_layout.addWidget(self.numpad_button[1],1,1)
        self.amount_tendered_layout.addWidget(self.numpad_box,2,0,1,2)
        self.amount_tendered_box.setLayout(self.amount_tendered_layout)

        self.payment_cash_button = MyPushButton(text='Cash')
        self.payment_points_button = MyPushButton(text='Points')
        self.payment_type_box = MyGroupBox()
        self.payment_type_box.setParent(self.numpad_button[1])
        self.payment_type_layout = MyHBoxLayout()
        self.payment_type_layout.addWidget(self.payment_cash_button)
        self.payment_type_layout.addWidget(self.payment_points_button)
        self.payment_type_box.setLayout(self.payment_type_layout)

        self.cust_info_name = MyLabel(text=f"{self.model.cust_info_name}")
        self.cust_info_points = MyLabel(text=f"{self.model.cust_info_points}")
        self.cust_info_phone = MyLabel(text=f"{self.model.cust_info_phone}")
        self.cust_info_box = MyGroupBox()
        self.cust_info_layout = MyFormLayout()
        self.cust_info_layout.addRow('Name:', self.cust_info_name)
        self.cust_info_layout.addRow('Points:', self.cust_info_points)
        self.cust_info_layout.addRow('Phone:', self.cust_info_phone)
        self.cust_info_box.setLayout(self.cust_info_layout)

        self.payment_box = MyGroupBox()
        self.payment_layout = MyFormLayout()
        self.payment_layout.addRow(self.amount_tendered_box)
        self.payment_layout.addRow(self.payment_type_box)
        self.payment_layout.addRow(self.cust_info_box) if self.model.customer_id else None
        self.payment_box.setLayout(self.payment_layout)

        self.cust_order_final_table = MyTableWidget(object_name='cust_order_final_table')
        self.cust_order_final_subtotal_label = MyLabel(text=f"{self.model.cust_order_subtotal_values[i]:.2f}")
        self.cust_order_final_discount_label = MyLabel(text=f"{self.model.cust_order_discount_values[i]:.2f}")
        self.cust_order_final_tax_label = MyLabel(text=f"{self.model.cust_order_tax_values[i]:.2f}")
        self.cust_order_final_total_label = MyLabel(text=f"{self.model.cust_order_total_values[i]:.2f}")
        self.cust_order_final_summary_box = MyGroupBox()
        self.cust_order_final_summary_layout = MyFormLayout()
        self.cust_order_final_summary_layout.addRow('Subtotal:', self.cust_order_final_subtotal_label)
        self.cust_order_final_summary_layout.addRow('Discount:', self.cust_order_final_discount_label)
        self.cust_order_final_summary_layout.addRow('Tax:', self.cust_order_final_tax_label)
        self.cust_order_final_summary_layout.addRow('Total:', self.cust_order_final_total_label)
        self.cust_order_final_summary_box.setLayout(self.cust_order_final_summary_layout)
        self.cust_order_final_box = MyGroupBox()
        self.cust_order_final_layout = MyVBoxLayout()
        self.cust_order_final_layout.addWidget(self.cust_order_final_table)
        self.cust_order_final_layout.addWidget(self.cust_order_final_summary_box)
        self.cust_order_final_box.setLayout(self.cust_order_final_layout)

        self.cash_drawer_layout.addWidget(self.payment_box,0,0)
        self.cash_drawer_layout.addWidget(self.cust_order_final_box,0,1)
        self.cash_drawer_dialog.setLayout(self.cash_drawer_layout)

        self.amount_tendered_field.returnPressed.connect(lambda: self.on_payment_button_clicked(action='cash_payment'))

        self.numpad_button[0].clicked.connect(lambda: self.on_numpad_button_clicked(action='toggle'))
        self.numpad_button[1].clicked.connect(lambda: self.on_numpad_button_clicked(action='untoggle'))
        
        self.numpad_keys_button[0][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=0))
        self.numpad_keys_button[1][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=1))
        self.numpad_keys_button[2][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=2))
        self.numpad_keys_button[3][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=3))
        self.numpad_keys_button[4][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=4))
        self.numpad_keys_button[5][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=5))
        self.numpad_keys_button[6][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=6))
        self.numpad_keys_button[7][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=7))
        self.numpad_keys_button[8][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=8))
        self.numpad_keys_button[9][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(value=9))
        self.numpad_keys_button[10][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(action='delete'))
        self.numpad_keys_button[11][2].clicked.connect(lambda: self.on_numpad_keys_button_clicked(action='clear'))

        self.payment_cash_button.clicked.connect(lambda: self.on_payment_button_clicked(action='cash_payment'))
        self.payment_points_button.clicked.connect(lambda: self.on_payment_button_clicked(action='points_payment'))
   
        # for numpad_keys_i in range(10):
        #     print(numpad_keys_i)
        #     self.numpad_keys_button[numpad_keys_i][2].clicked.connect(lambda value=numpad_keys_i: self.on_numpad_keys_button_clicked(value=value))

        self.populate_cust_order_final_table()

        self.cash_drawer_dialog.exec() # dialog stays open until here
        
        self.model.cust_order_item_data = []

        pass
    def populate_cust_order_final_table(self):
        self.cust_order_final_table.setRowCount(len(self.model.cust_order_item_data))
        for item_i, item_v in enumerate(self.model.cust_order_item_data):
            final_quantity = QTableWidgetItem(f"{item_v[2]}")
            final_item_name = QTableWidgetItem(f"{item_v[3]}")
            final_price = QTableWidgetItem(f"{item_v[4]}")

            self.cust_order_final_table.setItem(item_i, 0, final_quantity)
            self.cust_order_final_table.setItem(item_i, 1, final_item_name)
            self.cust_order_final_table.setItem(item_i, 2, final_price)
    def populate_payment_dialog(self):
        i = self.view.cust_order_tab.currentIndex()

        self.payment_dialog = MyDialog(parent=self.cash_drawer_dialog)
        self.payment_layout = MyVBoxLayout()

        self.print_opt_label = QLabel(text='Select option:')

        self.print_receipt_button = MyPushButton(text='Receipt')
        self.print_invoice_button = MyPushButton(text='Invoice')
        self.print_opt_layout = MyHBoxLayout()
        self.print_opt_layout.addWidget(self.print_receipt_button)
        self.print_opt_layout.addWidget(self.print_invoice_button)

        self.payment_layout.addWidget(self.print_opt_label)
        self.payment_layout.addLayout(self.print_opt_layout)
        self.payment_dialog.setLayout(self.payment_layout)

        self.print_receipt_button.clicked.connect(lambda: self.on_print_button_clicked(action='print_receipt'))
        self.print_invoice_button.clicked.connect(lambda: self.on_print_button_clicked(action='print_invoice'))

    def set_panel_box_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)

        self.view.barcode_scan_field.returnPressed.connect(self.on_barcode_scan_field_return_pressed)
        self.view.barcode_scan_button[0].clicked.connect(lambda: self.on_barcode_scan_button_clicked(action='toggle'))
        self.view.barcode_scan_button[1].clicked.connect(lambda: self.on_barcode_scan_button_clicked(action='untoggle'))

        self.view.prod_list_tab.currentChanged.connect(self.on_prod_list_tab_current_changed)
        self.view.prod_list_pag_prev_button[0].clicked.connect(self.on_prod_list_pag_prev_button_clicked)
        self.view.prod_list_pag_next_button[0].clicked.connect(self.on_prod_list_pag_next_button_clicked)
        self.view.prod_list_pag_prev_button[1].clicked.connect(self.on_prod_list_pag_prev_button_clicked)
        self.view.prod_list_pag_next_button[1].clicked.connect(self.on_prod_list_pag_next_button_clicked)
        pass
    def set_panel_box_b_conn(self):
        # self.view.add_cust_name_sel_field.currentTextChanged.connect()
        # self.view.add_cust_order_type_field.currentTextChanged.connect()
        self.view.add_cust_new_tab_button.clicked.connect(self.on_add_cust_new_tab_button_clicked)
        self.view.add_cust_load_button.clicked.connect(self.on_add_cust_load_button_clicked)
        self.view.cust_order_tab.currentChanged.connect(self.on_cust_order_tab_current_changed)

        pass
    def set_panel_box_c_conn(self):
        pass

    def on_text_filter_button_clicked(self):
        i = self.view.cust_order_tab.currentIndex()

        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    
    def on_barcode_scan_field_return_pressed(self):
        if self.view.cust_order_tab.count() > 0:
            i = self.view.cust_order_tab.currentIndex()

            prod_list_data = schema.list_product_via_barcode(barcode=self.view.barcode_scan_field.text(), order_type=self.model.cust_order_type_values[i])

            if self.view.cust_order_tab.count() > 0:
                try: 
                    for _, row_v in enumerate(prod_list_data):
                        cust_order_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name
                        
                        if cust_order_list: # if order list exist
                            for item_v in cust_order_list:
                                item_i = item_v.row()  # get row index
                                current_quantity = int(self.model.cust_order_tables[i].item(item_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                                current_price = float(self.model.cust_order_tables[i].item(item_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                                current_discount = float(self.model.cust_order_tables[i].item(item_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                                self.model.new_quantity = int(current_quantity + 1)
                                self.model.new_price = current_price + (float(row_v[8]) * 1)
                                self.model.new_discount = current_discount + (float(row_v[11]) * 1)

                                quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                                price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")  # Create a new 
                                discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")  # Create a new 

                                self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                                self.model.cust_order_tables[i].setItem(item_i, 3, price)
                                self.model.cust_order_tables[i].setItem(item_i, 4, discount)
                            pass
                        else:
                            item_i = self.model.cust_order_tables[i].rowCount()

                            self.model.cust_order_tables[i].insertRow(item_i)
                            
                            self.model.new_quantity = 1
                            self.model.new_price = float(row_v[8]) * 1
                            self.model.new_discount = float(row_v[11]) * 1

                            self.drop_all_quantity_button = MyPushButton(text='Drop all')
                            self.drop_quantity_button = MyPushButton(text='Drop')
                            self.add_quantity_button = MyPushButton(text='Add')
                            self.edit_quantity_button = MyPushButton(text='Edit')
                            cust_order_table_act_box = MyGroupBox()
                            cust_order_table_act_box_layout = MyHBoxLayout()
                            cust_order_table_act_box_layout.addWidget(self.drop_all_quantity_button)
                            cust_order_table_act_box_layout.addWidget(self.drop_quantity_button)
                            cust_order_table_act_box_layout.addWidget(self.add_quantity_button)
                            cust_order_table_act_box_layout.addWidget(self.edit_quantity_button)
                            cust_order_table_act_box.setLayout(cust_order_table_act_box_layout)

                            quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                            item_name = QTableWidgetItem(str(row_v[1]))
                            price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")
                            discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")

                            self.model.cust_order_tables[i].setCellWidget(item_i, 0, cust_order_table_act_box)
                            self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                            self.model.cust_order_tables[i].setItem(item_i, 2, item_name)
                            self.model.cust_order_tables[i].setItem(item_i, 3, price)
                            self.model.cust_order_tables[i].setItem(item_i, 4, discount)

                            self.drop_all_quantity_button.clicked.connect(lambda: self.on_drop_all_quantity_button_clicked(row_v))
                            self.drop_quantity_button.clicked.connect(lambda: self.on_drop_quantity_button_clicked(row_v))
                            self.add_quantity_button.clicked.connect(lambda: self.on_add_quantity_button_clicked(row_v))
                            self.edit_quantity_button.clicked.connect(lambda: self.on_edit_quantity_button_clicked(row_v))

                        self.model.cust_order_subtotal_values[i] += (float(row_v[8]) * 1)
                        self.model.cust_order_discount_values[i] += (float(row_v[11]) * 1)
                        self.model.cust_order_tax_values[i] += (0 * 1)
                        self.model.cust_order_total_values[i] = (self.model.cust_order_subtotal_values[i] - self.model.cust_order_discount_values[i]) + self.model.cust_order_tax_values[i]

                        self.model.cust_order_subtotal_labels[i].setText(f"₱{self.model.cust_order_subtotal_values[i]:.2f}")
                        self.model.cust_order_discount_labels[i].setText(f"₱{self.model.cust_order_discount_values[i]:.2f}")
                        self.model.cust_order_tax_labels[i].setText(f"₱{self.model.cust_order_tax_values[i]:.2f}")
                        self.model.cust_order_total_labels[i].setText(f"₱{self.model.cust_order_total_values[i]:.2f}")

                        self.model.cust_order_pay_buttons[i].setText(f"Pay ₱{self.model.cust_order_total_values[i]:.2f}")

                        self.view.barcode_scan_field.clear()
                    pass

                except ValueError as e:
                    QMessageBox.critical(self.view, 'Error', 'Invalid input.')
                pass
            else:
                QMessageBox.critical(self.view, 'Error', 'Must add order first.')

            self.view.barcode_scan_field.clear()

            self.new_quantity = 0
            self.new_price = 0

        pass
    def on_barcode_scan_button_clicked(self, action):
        if action == 'toggle':
            self.view.barcode_scan_button[0].hide()
            self.view.barcode_scan_button[1].show()
            condition = False
            pass
        elif action == 'untoggle':
            self.view.barcode_scan_button[0].show()
            self.view.barcode_scan_button[1].hide()
            condition = True

        self.view.barcode_scan_field.setHidden(condition)
        pass

    def on_prod_list_tab_current_changed(self):
        if self.view.cust_order_tab.count() > 0:
            i = self.view.cust_order_tab.currentIndex()

            self.model.page_number = 1

            self.view.prod_list_pag_page_label[0].setText(f"Page {self.model.page_number}/{self.model.total_page[0]}")
            self.view.prod_list_pag_page_label[1].setText(f"Page {self.model.page_number}/{self.model.total_page[1]}")

            self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    def on_prod_list_add_button_clicked(self, row_v):
        print(row_v)
        # DONE: add_button
        i = self.view.cust_order_tab.currentIndex()

        if self.view.cust_order_tab.count() > 0:
            while True:
                prop_quantity, confirm = QInputDialog.getText(self.view, 'Add', 'Input quantity:')

                if confirm == True:
                    try: 
                        if int(prop_quantity) > 0:
                            cust_order_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name
                            
                            if cust_order_list: # if order list exist
                                for item_v in cust_order_list:
                                    item_i = item_v.row()  # get row index
                                    current_quantity = int(self.model.cust_order_tables[i].item(item_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                                    current_price = float(self.model.cust_order_tables[i].item(item_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                                    current_discount = float(self.model.cust_order_tables[i].item(item_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                                    self.model.new_quantity = int(current_quantity + int(prop_quantity))
                                    self.model.new_price = current_price + (float(row_v[8]) * int(prop_quantity))
                                    self.model.new_discount = current_discount + (float(row_v[11]) * int(prop_quantity))

                                    quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                                    price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")  # Create a new 
                                    discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")  # Create a new 

                                    self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                                    self.model.cust_order_tables[i].setItem(item_i, 3, price)
                                    self.model.cust_order_tables[i].setItem(item_i, 4, discount)
                                pass
                            else:
                                item_i = self.model.cust_order_tables[i].rowCount()

                                self.model.cust_order_tables[i].insertRow(item_i)
                                
                                self.model.new_quantity = int(prop_quantity)
                                self.model.new_price = float(row_v[8]) * int(prop_quantity)
                                self.model.new_discount = float(row_v[11]) * int(prop_quantity)

                                self.drop_all_quantity_button = MyPushButton(text='Drop all')
                                self.drop_quantity_button = MyPushButton(text='Drop')
                                self.add_quantity_button = MyPushButton(text='Add')
                                self.edit_quantity_button = MyPushButton(text='Edit')
                                cust_order_table_act_box = MyGroupBox()
                                cust_order_table_act_box_layout = MyHBoxLayout()
                                cust_order_table_act_box_layout.addWidget(self.drop_all_quantity_button)
                                cust_order_table_act_box_layout.addWidget(self.drop_quantity_button)
                                cust_order_table_act_box_layout.addWidget(self.add_quantity_button)
                                cust_order_table_act_box_layout.addWidget(self.edit_quantity_button)
                                cust_order_table_act_box.setLayout(cust_order_table_act_box_layout)

                                quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                                item_name = QTableWidgetItem(str(row_v[1]))
                                price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")
                                discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")
                    
                                self.model.cust_order_tables[i].setCellWidget(item_i, 0, cust_order_table_act_box)
                                self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                                self.model.cust_order_tables[i].setItem(item_i, 2, item_name)
                                self.model.cust_order_tables[i].setItem(item_i, 3, price)
                                self.model.cust_order_tables[i].setItem(item_i, 4, discount)

                                self.drop_all_quantity_button.clicked.connect(lambda: self.on_drop_all_quantity_button_clicked(row_v))
                                self.drop_quantity_button.clicked.connect(lambda: self.on_drop_quantity_button_clicked(row_v))
                                self.add_quantity_button.clicked.connect(lambda: self.on_add_quantity_button_clicked(row_v))
                                self.edit_quantity_button.clicked.connect(lambda: self.on_edit_quantity_button_clicked(row_v))


                            self.model.cust_order_subtotal_values[i] += (float(row_v[8]) * int(prop_quantity))
                            self.model.cust_order_discount_values[i] += (float(row_v[11]) * int(prop_quantity))
                            self.model.cust_order_tax_values[i] += (0 * int(prop_quantity))
                            self.model.cust_order_total_values[i] = (self.model.cust_order_subtotal_values[i] - self.model.cust_order_discount_values[i]) + self.model.cust_order_tax_values[i]

                            self.model.cust_order_subtotal_labels[i].setText(f"₱{self.model.cust_order_subtotal_values[i]:.2f}")
                            self.model.cust_order_discount_labels[i].setText(f"₱{self.model.cust_order_discount_values[i]:.2f}")
                            self.model.cust_order_tax_labels[i].setText(f"₱{self.model.cust_order_tax_values[i]:.2f}")
                            self.model.cust_order_total_labels[i].setText(f"₱{self.model.cust_order_total_values[i]:.2f}")

                            self.model.cust_order_pay_buttons[i].setText(f"Pay ₱{self.model.cust_order_total_values[i]:.2f}")

                            break
                            pass
                        else:
                            QMessageBox.critical(self.view, 'Error', 'Must be greater than 0.')
                            pass
                    except ValueError as e:
                        QMessageBox.critical(self.view, 'Error', 'Invalid input.')
                else:
                    break
        else:
            QMessageBox.critical(self.view, 'Error', 'Must add order first.')

        self.new_quantity = 0
        self.new_price = 0
        pass
    def on_prod_list_view_button_clicked(self, row_v):
        print(row_v)
        # TODO: view_button
        self.view_dialog = MyDialog(parent=self.view)
        self.view_layout = MyFormLayout()

        item_data = [
            ['Barcode:', MyLabel(text=f"{row_v[0]}")],
            ['Item name:', MyLabel(text=f"{row_v[1]}")],
            ['Expire dt:', MyLabel(text=f"{row_v[2]}")],
            [None, MyLabel(text='<hr>')],
            ['Item type:', MyLabel(text=f"{row_v[3]}")],
            ['Brand:', MyLabel(text=f"{row_v[4]}")],
            ['Sales group:', MyLabel(text=f"{row_v[5]}")],
            ['Supplier:', MyLabel(text=f"{row_v[6]}")],
            [None, MyLabel(text='<hr>')],
            ['Cost:', MyLabel(text=f"{row_v[7]}")],
            ['Sell price:', MyLabel(text=f"{row_v[8]}")],
            ['Effective dt:', MyLabel(text=f"{row_v[9]}")],
            ['Promo name:', MyLabel(text=f"{row_v[10]}")],
            ['Discount value:', MyLabel(text=f"{row_v[11]}")],
            [None, MyLabel(text='<hr>')],
            ['Inventory tracking:', MyLabel(text=f"{row_v[12]}")],
            ['Available stock:', MyLabel(text=f"{row_v[13]}")],
            ['On hand stock:', MyLabel(text=f"{row_v[14]}")],
        ]

        for label, data in item_data:
            if label:
                self.view_layout.addRow(label, data)
            else:
                self.view_layout.addRow(data)

        self.view_dialog.setLayout(self.view_layout)

        self.view_dialog.exec()
        pass
    def on_prod_list_pag_prev_button_clicked(self):
        i = self.view.cust_order_tab.currentIndex()
        
        if self.model.page_number > 1:
            self.model.page_number -= 1
            self.view.prod_list_pag_page_label[0].setText(f"Page {self.model.page_number}/{self.model.total_page[0]}")
            self.view.prod_list_pag_page_label[1].setText(f"Page {self.model.page_number}/{self.model.total_page[1]}")

        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    def on_prod_list_pag_next_button_clicked(self):
        i = self.view.cust_order_tab.currentIndex()
        
        self.model.page_number += 1
        self.view.prod_list_pag_page_label[0].setText(f"Page {self.model.page_number}/{self.model.total_page[0]}")
        self.view.prod_list_pag_page_label[1].setText(f"Page {self.model.page_number}/{self.model.total_page[1]}")
        
        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass

    def on_add_cust_new_tab_button_clicked(self):
        self.populate_cust_order_tab()
        pass
    def on_add_cust_load_button_clicked(self):
        # TODO: finish this
        
        filename, _ = QFileDialog.getOpenFileName(self.view, 'Load', '', "Text Files (*.txt);;All Files (*)")

        with open(filename, 'r') as file:
            loaded_data = []

            for line in file:
                # Split the line by a comma and strip whitespace
                items = [item.strip() for item in line.split(',')]
                loaded_data.append(items)

        # Update self.model.cust_order_item_data with the loaded data
        self.model.cust_order_item_data = loaded_data

        print('data:', self.model.cust_order_item_data)
        pass

    def on_cust_order_tab_current_changed(self):
        i = self.view.cust_order_tab.currentIndex()
        
        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    def on_cust_order_clear_button_clicked(self):
        # DONE: order_clear_button
        i = self.view.cust_order_tab.currentIndex()
            
        if self.model.cust_order_tables[i].rowCount() > 0:
            confirm = QMessageBox.warning(self.view, 'Clear', 'Are you sure you want to clear this order?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.model.cust_order_tables[i].setRowCount(0)

                self.model.cust_order_subtotal_values[i] = 0
                self.model.cust_order_discount_values[i] = 0
                self.model.cust_order_tax_values[i] = 0
                self.model.cust_order_total_values[i] = 0

                self.model.cust_order_subtotal_labels[i].setText(f"₱{self.model.cust_order_subtotal_values[i]:.2f}")
                self.model.cust_order_discount_labels[i].setText(f"₱{self.model.cust_order_discount_values[i]:.2f}")
                self.model.cust_order_tax_labels[i].setText(f"₱{self.model.cust_order_tax_values[i]:.2f}")
                self.model.cust_order_total_labels[i].setText(f"₱{self.model.cust_order_total_values[i]:.2f}")

                self.model.cust_order_pay_buttons[i].setText(f"Pay ₱{self.model.cust_order_total_values[i]:.2f}")

            self.new_quantity = 0
            self.new_price = 0
        else:
            QMessageBox.critical(self.view, 'Error', 'Nothing to clear in this table.')
        pass

    def on_drop_all_quantity_button_clicked(self, row_v):
        # DONE: drop_all
        i = self.view.cust_order_tab.currentIndex()

        confirm = QMessageBox.warning(self.view, 'Drop', 'Are you sure you want to drop all this item?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            cust_order_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name

            if cust_order_list:
                for item_v in cust_order_list:
                    item_i = item_v.row()  # Get the row of the item
                    current_quantity = int(self.model.cust_order_tables[i].item(item_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                    current_price = float(self.model.cust_order_tables[i].item(item_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                    current_discount = float(self.model.cust_order_tables[i].item(item_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                    self.model.new_quantity = int(current_quantity - current_quantity)
                    self.model.new_price = current_price - current_price
                    self.model.new_discount = current_discount - current_discount

                    quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                    price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")  # Create a new 
                    discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")  # Create a new 

                    self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                    self.model.cust_order_tables[i].setItem(item_i, 3, price)
                    self.model.cust_order_tables[i].setItem(item_i, 4, discount)

                    self.model.cust_order_tables[i].removeRow(item_i)

                    self.model.cust_order_subtotal_values[i] = max(0, self.model.cust_order_subtotal_values[i] - current_price)
                    self.model.cust_order_discount_values[i] = max(0, self.model.cust_order_discount_values[i] - current_discount)
                    self.model.cust_order_tax_values[i] = max(0, self.model.cust_order_tax_values[i] - 0)
                    self.model.cust_order_total_values[i] = max(0, (self.model.cust_order_subtotal_values[i] - self.model.cust_order_discount_values[i]) - self.model.cust_order_tax_values[i])

            self.model.cust_order_subtotal_labels[i].setText(f"₱{self.model.cust_order_subtotal_values[i]:.2f}")
            self.model.cust_order_discount_labels[i].setText(f"₱{self.model.cust_order_discount_values[i]:.2f}")
            self.model.cust_order_tax_labels[i].setText(f"₱{self.model.cust_order_tax_values[i]:.2f}")
            self.model.cust_order_total_labels[i].setText(f"₱{self.model.cust_order_total_values[i]:.2f}")

            self.model.cust_order_pay_buttons[i].setText(f"Pay ₱{self.model.cust_order_total_values[i]:.2f}")

        self.new_quantity = 0
        self.new_price = 0
        pass
    def on_drop_quantity_button_clicked(self, row_v):
        # DONE: drop
        i = self.view.cust_order_tab.currentIndex()

        cust_order_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name
        
        if cust_order_list: # if item already exist in table, update row of item
            for item_v in cust_order_list:
                item_i = item_v.row()  # Get the row of the item
                current_quantity = int(self.model.cust_order_tables[i].item(item_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                current_price = float(self.model.cust_order_tables[i].item(item_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                current_discount = float(self.model.cust_order_tables[i].item(item_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                if current_quantity > 1:
                    self.model.new_quantity = int(current_quantity - 1)
                    self.model.new_price = current_price - float(row_v[8])
                    self.model.new_discount = current_discount - float(row_v[11])

                    quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                    price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")  # Create a new 
                    discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")  # Create a new 

                    self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                    self.model.cust_order_tables[i].setItem(item_i, 3, price)
                    self.model.cust_order_tables[i].setItem(item_i, 4, discount)
                    pass
                else:
                    self.model.cust_order_tables[i].removeRow(item_i)
                pass

        self.model.cust_order_subtotal_values[i] = max(0, self.model.cust_order_subtotal_values[i] - float(row_v[8]))
        self.model.cust_order_discount_values[i] = max(0, self.model.cust_order_discount_values[i] - float(row_v[11]))
        self.model.cust_order_tax_values[i] = max(0, self.model.cust_order_tax_values[i])
        self.model.cust_order_total_values[i] = max(0, (self.model.cust_order_subtotal_values[i] - self.model.cust_order_discount_values[i]) - self.model.cust_order_tax_values[i])

        self.model.cust_order_subtotal_labels[i].setText(f"₱{self.model.cust_order_subtotal_values[i]:.2f}")
        self.model.cust_order_discount_labels[i].setText(f"₱{self.model.cust_order_discount_values[i]:.2f}")
        self.model.cust_order_tax_labels[i].setText(f"₱{self.model.cust_order_tax_values[i]:.2f}")
        self.model.cust_order_total_labels[i].setText(f"₱{self.model.cust_order_total_values[i]:.2f}")

        self.model.cust_order_pay_buttons[i].setText(f"Pay ₱{self.model.cust_order_total_values[i]:.2f}")

        self.new_quantity = 0
        self.new_price = 0
        pass
    def on_add_quantity_button_clicked(self, row_v):
        # DONE: add
        i = self.view.cust_order_tab.currentIndex()

        cust_order_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name
        
        if cust_order_list: # if item already exist in table, update row of item
            for item_v in cust_order_list:
                item_i = item_v.row()  # Get the row of the item
                current_quantity = int(self.model.cust_order_tables[i].item(item_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                current_price = float(self.model.cust_order_tables[i].item(item_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                current_discount = float(self.model.cust_order_tables[i].item(item_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                self.model.new_quantity = int(current_quantity + 1)
                self.model.new_price = current_price + float(row_v[8])
                self.model.new_discount = current_discount + float(row_v[11])

                quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")  # Create a new 
                discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")  # Create a new 

                self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                self.model.cust_order_tables[i].setItem(item_i, 3, price)
                self.model.cust_order_tables[i].setItem(item_i, 4, discount)
                pass

        self.model.cust_order_subtotal_values[i] += (float(row_v[8]) * 1)
        self.model.cust_order_discount_values[i] += (float(row_v[11]) * 1)
        self.model.cust_order_tax_values[i] += (0 * 1)
        self.model.cust_order_total_values[i] = (self.model.cust_order_subtotal_values[i] - self.model.cust_order_discount_values[i]) + self.model.cust_order_tax_values[i]

        self.model.cust_order_subtotal_labels[i].setText(f"₱{self.model.cust_order_subtotal_values[i]:.2f}")
        self.model.cust_order_discount_labels[i].setText(f"₱{self.model.cust_order_discount_values[i]:.2f}")
        self.model.cust_order_tax_labels[i].setText(f"₱{self.model.cust_order_tax_values[i]:.2f}")
        self.model.cust_order_total_labels[i].setText(f"₱{self.model.cust_order_total_values[i]:.2f}")

        self.model.cust_order_pay_buttons[i].setText(f"Pay ₱{self.model.cust_order_total_values[i]:.2f}")

        self.new_quantity = 0
        self.new_price = 0
        pass
    def on_edit_quantity_button_clicked(self, row_v):
        # DONE: edit
        i = self.view.cust_order_tab.currentIndex()

        i = self.view.cust_order_tab.currentIndex()

        if self.view.cust_order_tab.count() > 0:
            while True:
                prop_quantity, confirm = QInputDialog.getText(self.view, 'Add', 'Input quantity:')

                if confirm == True:
                    try: 
                        if int(prop_quantity) > 0:
                            cust_order_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name

                            if cust_order_list:
                                for item_v in cust_order_list:
                                    item_i = item_v.row()  # Get the row of the item

                                    self.model.new_quantity = int(prop_quantity)
                                    self.model.new_price = float(row_v[8]) * int(prop_quantity)
                                    self.model.new_discount = float(row_v[11]) * int(prop_quantity)

                                    quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                                    price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")  # Create a new 
                                    discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")  # Create a new 

                                    self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                                    self.model.cust_order_tables[i].setItem(item_i, 3, price)
                                    self.model.cust_order_tables[i].setItem(item_i, 4, discount)

                            self.model.cust_order_subtotal_values[i] = float(row_v[8]) * int(prop_quantity)
                            self.model.cust_order_discount_values[i] = float(row_v[11]) * int(prop_quantity)
                            self.model.cust_order_tax_values[i] = 0
                            self.model.cust_order_total_values[i] = (self.model.cust_order_subtotal_values[i] - self.model.cust_order_discount_values[i]) + self.model.cust_order_tax_values[i]

                            self.model.cust_order_subtotal_labels[i].setText(f"₱{self.model.cust_order_subtotal_values[i]:.2f}")
                            self.model.cust_order_discount_labels[i].setText(f"₱{self.model.cust_order_discount_values[i]:.2f}")
                            self.model.cust_order_tax_labels[i].setText(f"₱{self.model.cust_order_tax_values[i]:.2f}")
                            self.model.cust_order_total_labels[i].setText(f"₱{self.model.cust_order_total_values[i]:.2f}")

                            self.model.cust_order_pay_buttons[i].setText(f"Pay ₱{self.model.cust_order_total_values[i]:.2f}")

                            break
                            pass
                        else:
                            QMessageBox.critical(self.view, 'Error', 'Must be greater than 0.')
                            pass
                    except ValueError as e:
                        QMessageBox.critical(self.view, 'Error', 'Invalid input.')
                else:
                    break

        self.new_quantity = 0
        self.new_price = 0
        pass

    def on_cust_order_discard_button_clicked(self):
        # DONE: order_discard_button
        i = self.view.cust_order_tab.currentIndex()
        
        confirm = QMessageBox.warning(self.view, 'Clear', 'Are you sure you want to discard this order?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.view.cust_order_tab.removeTab(i)
            self.model.remove_cust_order_data(i)

            self.view.pending_order_label.setText(f"Pending order: {self.view.cust_order_tab.count()}")

        self.populate_cust_order_tab() if self.view.cust_order_tab.count() == 0 else None
        pass
    def on_cust_order_restrict_button_clicked(self, action):
        i = self.view.cust_order_tab.currentIndex()
        
        if action == 'toggle':
            self.model.cust_order_restrict_buttons[i][0].hide()
            self.model.cust_order_restrict_buttons[i][1].show()
            condition = True
            pass
        elif action == 'untoggle':
            self.model.cust_order_restrict_buttons[i][0].show()
            self.model.cust_order_restrict_buttons[i][1].hide()
            condition = False
            pass

        self.model.cust_order_tables[i].setDisabled(condition)

        self.model.cust_order_type_labels[i].setDisabled(condition)
        self.model.cust_order_clear_buttons[i].setDisabled(condition)
        self.model.cust_order_subtotal_labels[i].setDisabled(condition)
        self.model.cust_order_discount_labels[i].setDisabled(condition)
        self.model.cust_order_tax_labels[i].setDisabled(condition)
        self.model.cust_order_total_labels[i].setDisabled(condition)
        self.model.cust_order_discard_buttons[i].setDisabled(condition)

        self.model.cust_order_pay_buttons[i].setDisabled(condition)
        pass
    def on_cust_order_save_button_clicked(self):
        # TODO: order_save_button
        i = self.view.cust_order_tab.currentIndex()

        for row in range(self.model.cust_order_tables[i].rowCount()):
            item_row_data = [self.model.cust_order_type_values[i]]

            for col in range(self.model.cust_order_tables[i].columnCount()):
                item = self.model.cust_order_tables[i].item(row, col)
                if item is not None:
                    item_row_data.append(item.text().replace('₱', ''))

            self.model.append_cust_order_item_data(item_row_data)

        print('data:', self.model.cust_order_item_data)

        confirm = QMessageBox.warning(self.view, 'Save', 'Save this order?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        file_name = f"{self.model.cust_order_type_values[i]}-{self.model.cust_order_name_values[i]}-{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

        if confirm == QMessageBox.StandardButton.Yes:
            with open(os.path.abspath(self.model.save_file_path + file_name), 'w') as file:   
                for item in self.model.cust_order_item_data:
                    line = ', '.join(item) 
                    file.write(line + '\n')  
                    # REVIEW: needs to be reviewed

        self.model.cust_order_item_data = []

        pass
    def on_cust_order_pay_button_clicked(self):
        # TODO: order_pay_button
        i = self.view.cust_order_tab.currentIndex()

        if self.model.cust_order_tables[i].rowCount() > 0:
            for row in range(self.model.cust_order_tables[i].rowCount()):
                item_row_data = [self.model.cust_order_name_values[i], self.model.cust_order_type_values[i]]

                for col in range(self.model.cust_order_tables[i].columnCount()):
                    item = self.model.cust_order_tables[i].item(row, col)
                    if item is not None:
                        item_row_data.append(item.text().replace('₱', ''))

                self.model.append_cust_order_item_data(item_row_data)
                
            self.populate_cash_drawer_dialog()
            pass
        else:
            QMessageBox.critical(self.view, 'Error', 'Must add an item first.')
        pass

    def on_numpad_button_clicked(self, action):
        if action == 'toggle':
            condition = False
            self.numpad_button[0].hide()
            self.numpad_button[1].show()
            pass
        elif action == 'untoggle':
            condition = True
            self.numpad_button[0].show()
            self.numpad_button[1].hide()
            pass

        self.numpad_box.setHidden(condition)
    def on_numpad_keys_button_clicked(self, value=0, action=''):
        current_value = self.amount_tendered_field.text()

        if value >= 0:
            current_value = current_value + str(value)
            self.amount_tendered_field.setText(current_value)
            pass
        if action == 'delete':
            current_value = current_value[:-2]
            self.amount_tendered_field.setText(current_value)
            pass
        elif action == 'clear':
            self.amount_tendered_field.setText('')
            pass
        pass

    def on_payment_button_clicked(self, action):
        i = self.view.cust_order_tab.currentIndex()

        try:
            self.populate_payment_dialog()

            self.model.cust_order_amount_tendered_value = float(self.amount_tendered_field.text())
            self.model.cust_order_change_value = self.model.cust_order_amount_tendered_value - self.model.cust_order_total_values[i]

            print('amount_tendered:', self.model.cust_order_amount_tendered_value)
            print('change:', self.model.cust_order_change_value)

            if self.model.cust_order_amount_tendered_value >= self.model.cust_order_total_values[i]:
                if action == 'cash_payment':
                    self.payment_dialog.close()

                    self.model.append_cust_order_summary_data(
                        cust_order_subtotal_value=self.model.cust_order_subtotal_values[i],
                        cust_order_discount_value=self.model.cust_order_discount_values[i],
                        cust_order_tax_value=self.model.cust_order_tax_values[i],
                        cust_order_total_value=self.model.cust_order_total_values[i],
                        cust_order_amount_tendered_value=self.model.cust_order_amount_tendered_value,
                        cust_order_change_value=self.model.cust_order_change_value,
                    )
                    
                    self.payment_dialog.exec()
                    pass
                if action == 'points_payment':
                    print('points')
                    pass

            else:
                QMessageBox.critical(self.payment_dialog, 'Error', 'Insufficient amount.')
                pass
        except ValueError as e:
            QMessageBox.critical(self.payment_dialog, 'Error', 'Invalid input.')
        pass
    def on_print_button_clicked(self, action):
        self.payment_dialog.close()
        
        self.wait_label = QLabel('Processing order...')
        self.wait_dialog = MyDialog(parent=self.cash_drawer_dialog)
        self.wait_layout = MyHBoxLayout()
        self.wait_layout.addWidget(self.wait_label)
        self.wait_dialog.setLayout(self.wait_layout)

        print('cust_order_item_data:', self.model.cust_order_item_data)
        print('cust_order_summary_data:', self.model.cust_order_summary_data)
        print('customer_id:', self.model.customer_id)

        if action == 'print_receipt':
            self.receipt_printer = ReceiptGenerator(
                cust_order_item_data=self.model.cust_order_item_data,
                cust_order_summary_data=self.model.cust_order_summary_data,
                customer_id=self.model.customer_id,
                current_user='test',
                action=action,
            )


            self.receipt_printer.start()
            self.receipt_printer.finished.connect(self.on_receipt_printer_finished)

        elif action == 'print_invoice':
            self.receipt_printer = ReceiptGenerator(
                cust_order_item_data=self.model.cust_order_item_data,
                cust_order_summary_data=self.model.cust_order_summary_data,
                customer_id=self.model.customer_id,
                current_user='test',
                action=action,
            )

            self.receipt_printer.start()
            self.receipt_printer.finished.connect(self.on_receipt_printer_finished)
        
        self.model.cust_order_summary_data = [] # REVIEW: THIS IS A CHECKPOINT!!!
        
        self.wait_dialog.exec()
        
        pass

    def on_receipt_printer_finished(self):
        self.wait_dialog.close()
        i = self.view.cust_order_tab.currentIndex()

        self.payment_dialog.close()
        self.cash_drawer_dialog.close()
        
        self.view.cust_order_tab.removeTab(i)
        self.model.remove_cust_order_data(i)
        
        QMessageBox.information(self.view, 'Success', 'Item has been sold.')

        
        self.populate_cust_order_tab()

if __name__ == ('__main__'):
    app = QApplication(sys.argv)

    schema = SalesSchema()

    model = MySalesModel(schema)
    view = MySalesView(model)
    controller = MySalesController(model, view)

    view.show()
    sys.exit(app.exec())
