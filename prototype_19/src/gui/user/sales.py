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
        self.add_cust_load_button = MyPushButton(text='Load')
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

        self.set_panel_box_a_conn()
        self.set_panel_box_b_conn()
        self.set_panel_box_c_conn()

    def populate_prod_list_table(self, text_filter='', order_type='Retail', page_number=1):
        self.prod_list_data = [
            schema.list_product(text_filter, order_type, page_number),
            schema.list_product_via_promo(text_filter, order_type, page_number)
        ]

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
        self.cust_order_save_button = MyPushButton(text='Save')
        self.cust_order_pay_button = MyPushButton(text=f"Pay ₱{self.cust_order_total_value}")
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
        self.view.pending_order_label.setText(f"Pending order: {self.view.cust_order_tab.count()}")
        # FIXME: SHOULD BE IN A DIFFERENT FUNCTION

        self.cust_order_clear_button.clicked.connect(self.on_cust_order_clear_button_clicked)
        self.cust_order_discard_button.clicked.connect(self.on_cust_order_discard_button_clicked)

        self.cust_order_restrict_button[0].clicked.connect(lambda: self.on_cust_order_restrict_button_clicked(action='toggle'))
        self.cust_order_restrict_button[1].clicked.connect(lambda: self.on_cust_order_restrict_button_clicked(action='untoggle'))

        self.cust_order_save_button.clicked.connect(self.on_cust_order_save_button_clicked)
        self.cust_order_pay_button.clicked.connect(self.on_cust_order_pay_button_clicked)

    def set_panel_box_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_field_return_pressed)
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

    def on_text_filter_field_return_pressed(self):
        i = self.view.cust_order_tab.currentIndex()

        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    def on_text_filter_button_clicked(self):
        i = self.view.cust_order_tab.currentIndex()

        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    def on_barcode_scan_field_return_pressed(self):
        # DONE: add item to cust order table
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

                            self.model.new_quantity = current_quantity + 1
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

                                    self.model.new_quantity = current_quantity + int(prop_quantity)
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
                                
                                self.model.new_quantity = prop_quantity
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

        confirm = QMessageBox.warning(self.view, 'Proceed', 'This will overwrite the current order. Are you sure you want to continue?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Abort)

        if confirm == QMessageBox.StandardButton.Yes:
            self.populate_cust_order_tab()

            i = self.view.cust_order_tab.currentIndex()

            self.model.cust_order_tables[i].setRowCount(len(self.model.cust_order_item_data))

            for item_i, item_v in enumerate(self.model.cust_order_item_data):
                print('item_v', item_v)
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

                quantity = QTableWidgetItem(f"{item_v[0]}")
                item_name = QTableWidgetItem(f"{item_v[1]}")
                price = QTableWidgetItem(f"{item_v[2]}")
                discount = QTableWidgetItem(f"{item_v[3]}")

                self.model.cust_order_tables[i].setCellWidget(item_i, 0, cust_order_table_act_box)
                self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                self.model.cust_order_tables[i].setItem(item_i, 2, item_name)
                self.model.cust_order_tables[i].setItem(item_i, 3, price)
                self.model.cust_order_tables[i].setItem(item_i, 4, discount)

        print('data:', self.model.cust_order_item_data)
        pass

    def on_cust_order_tab_current_changed(self):
        i = self.view.cust_order_tab.currentIndex()
        
        self.model.cust_order_type_labels[i].setText(f"Order type: {self.model.cust_order_type_values[i]}")
        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    def on_cust_order_clear_button_clicked(self):
        # DONE: order_clear_button
        i = self.view.cust_order_tab.currentIndex()
        
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

                    self.model.new_quantity = current_quantity - current_quantity
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
                    self.model.new_quantity = current_quantity - 1
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

                self.model.new_quantity = current_quantity + 1
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
        pass
    def on_cust_order_restrict_button_clicked(self, action):
        i = self.view.cust_order_tab.currentIndex()
        
        if action == 'toggle':
            self.cust_order_restrict_button[0].hide()
            self.cust_order_restrict_button[1].show()
            condition = True
            pass
        elif action == 'untoggle':
            self.cust_order_restrict_button[0].show()
            self.cust_order_restrict_button[1].hide()
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

        self.model.cust_order_save_buttons[i].setDisabled(condition)
        self.model.cust_order_pay_buttons[i].setDisabled(condition)
    def on_cust_order_save_button_clicked(self):
        # TODO: order_save_button
        i = self.view.cust_order_tab.currentIndex()

        for row in range(self.model.cust_order_tables[i].rowCount()):
            item_row_data = []

            for col in range(self.model.cust_order_tables[i].columnCount()):
                item = self.model.cust_order_tables[i].item(row, col)
                if item is not None:
                    item_row_data.append(item.text().replace('x', '').replace('₱', ''))

            self.model.append_cust_order_item_data(item_row_data)

        print('data:', self.model.cust_order_item_data)

        confirm = QMessageBox.warning(self.view, 'Save', 'Save this order?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        file_name = f"{self.model.cust_order_type_values[i]}-{self.model.cust_order_name_values[i]}-{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

        if confirm == QMessageBox.StandardButton.Yes:
            # REVIEW: save data
            # FIXME: needs to be saved in .db file for better security
            with open(os.path.abspath(self.model.save_file_path + file_name), 'w') as file:   
                for item in self.model.cust_order_item_data:
                    line = ', '.join(item) 
                    file.write(line + '\n')  

        self.model.cust_order_item_data = []

        pass
    def on_cust_order_pay_button_clicked(self):
        # TODO: order_pay_button
        pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)

    schema = SalesSchema()

    model = MySalesModel(schema)
    view = MySalesView(model)
    controller = MySalesController(model, view)

    view.show()
    sys.exit(app.exec())
