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

class MySalesModel:
    def __init__(self, schema: SalesSchema):
        self.schema = schema

        self.set_global_values()

    def set_global_values(self):
        self.page_number = 1
        self.total_page_number = schema.count_product_list_total_pages()

        self.current_user_value = '<none>'
        self.pending_order_value = 0
        self.available_product_value = 0

        self.cust_name_data_list = schema.list_customer()
        self.cust_order_name_value = ''
        self.cust_order_type_value = 'Retail'

        self.cust_order_subtotal_value = 0
        self.cust_order_discount_value = 0
        self.cust_order_tax_value = 0
        self.cust_order_total_value = 0

        # region > containers
        self.cust_order_name_values = []
        self.cust_order_type_values = []

        self.cust_order_type_labels: List[MyLabel] = []
        self.cust_order_clear_buttons: List[MyPushButton] = []
        self.cust_order_tables: List[MyTableWidget] = []

        self.cust_order_subtotal_values = []
        self.cust_order_discount_values = []
        self.cust_order_tax_values = []
        self.cust_order_total_values = []

        self.cust_order_subtotal_labels: List[MyLabel] = []
        self.cust_order_discount_labels: List[MyLabel] = []
        self.cust_order_tax_labels: List[MyLabel] = []
        self.cust_order_total_labels: List[MyLabel] = []

        self.cust_order_discard_buttons: List[MyPushButton] = []
        self.cust_order_resctrict_buttons: List[MyPushButton] = []
        self.cust_order_save_buttons: List[MyPushButton] = []
        self.cust_order_pay_buttons: List[MyPushButton] = []
        # endregion > containers

    def set_prod_list_table_data_value(self, text_filter, order_type, page_number):
        self.prod_list_a_table_data = schema.list_product(text_filter, order_type, page_number)
        self.prod_list_b_table_data = schema.list_product_via_promo(text_filter, order_type, page_number)

    def set_main_panel_widgets(self):
        pass
    
    def set_panel_box_a_widgets(self):
        self.text_filter_field = MyLineEdit()
        self.text_filter_button = MyPushButton(text='Filter')

        self.barcode_scan_field = MyLineEdit()
        self.barcode_scan_button: List[MyPushButton] = [
            MyPushButton(text='Turn on'),
            MyPushButton(text='Turn off')
        ]

        self.prod_list_tab = MyTabWidget()
       
        self.prod_list_a_table = MyTableWidget(object_name='prod_list_a_table')
        self.prod_list_a_pag_button: List[MyPushButton] = [
            MyPushButton(text='Prev'),
            MyPushButton(text='Next'),
        ]
        self.prod_list_a_pag_page_label = MyLabel(text=f"Page {self.page_number}/{self.total_page_number}")
        
        self.prod_list_b_table = MyTableWidget(object_name='prod_list_b_table')
        self.prod_list_b_pag_button: List[MyPushButton] = [
            MyPushButton(text='Prev'),
            MyPushButton(text='Next'),
        ]
        self.prod_list_b_pag_page_label = MyLabel()
        pass
    def set_prod_list_act_widgets(self):
        self.prod_list_a_act_button: List[MyPushButton] = [
            MyPushButton(text='Add'),
            MyPushButton(text='View'),
        ]
        self.prod_list_b_act_button: List[MyPushButton] = [
            MyPushButton(),
            MyPushButton(),
        ]
        
    def set_panel_box_b_widgets(self):
        self.add_order_cust_sel_field = MyComboBox()
        self.add_order_type_field = MyComboBox()
        self.add_order_button = MyPushButton(text='Add')
        self.add_order_load_button = MyPushButton(text='Load')

        self.cust_order_tab = MyTabWidget()
        pass
    def set_cust_order_widgets(self):
        # region > widgets
        self.cust_order_type_label = MyLabel(text=f"Order type: {self.cust_order_type_value}")
        self.cust_order_clear_button = MyPushButton(text='Clear')
        self.cust_order_table = MyTableWidget()
        self.cust_order_subtotal_label = MyLabel(text=f"{self.cust_order_subtotal_value:.2f}")
        self.cust_order_discount_label = MyLabel(text=f"{self.cust_order_discount_value:.2f}")
        self.cust_order_tax_label = MyLabel(text=f"{self.cust_order_tax_value:.2f}")
        self.cust_order_total_label = MyLabel(text=f"{self.cust_order_total_value:.2f}")
        self.cust_order_discard_button = MyPushButton(text='Discard')
        self.cust_order_resctrict_button = [
            MyPushButton(text='Lock'),
            MyPushButton(text='Unlock'),
        ]
        self.cust_order_save_button = MyPushButton(text='Save')
        self.cust_order_pay_button = MyPushButton(text=f"Pay {self.cust_order_total_value:.2f}")
        # endregion > widgets
    
    def set_panel_box_c_widgets(self):
        self.current_user_label = MyLabel(text=f"Current user: {self.current_user_value}")
        self.pending_order_label = MyLabel(text=f"Pending order: {self.pending_order_value}")
        self.available_product_label = MyLabel(text=f"Available product: {self.available_product_value}")

    def append_cust_order_data(
        self,
        cust_order_name_value,
        cust_order_type_value,
        cust_order_type_label,
        cust_order_clear_button,
        cust_order_table,
        cust_order_subtotal_value,
        cust_order_discount_value,
        cust_order_tax_value,
        cust_order_total_value,
        cust_order_subtotal_label,
        cust_order_discount_label,
        cust_order_tax_label,
        cust_order_total_label,
        cust_order_discard_button,
        cust_order_resctrict_button,
        cust_order_save_button,
        cust_order_pay_button,
    ):
        self.cust_order_name_values.append(cust_order_name_value)
        self.cust_order_type_values.append(cust_order_type_value)
        
        self.cust_order_type_labels.append(cust_order_type_label)
        self.cust_order_clear_buttons.append(cust_order_clear_button)
        self.cust_order_tables.append(cust_order_table)

        self.cust_order_subtotal_values.append(cust_order_subtotal_value) 
        self.cust_order_discount_values.append(cust_order_discount_value) 
        self.cust_order_tax_values.append(cust_order_tax_value) 
        self.cust_order_total_values.append(cust_order_total_value) 

        self.cust_order_subtotal_labels.append(cust_order_subtotal_label)
        self.cust_order_discount_labels.append(cust_order_discount_label)
        self.cust_order_tax_labels.append(cust_order_tax_label)
        self.cust_order_total_labels.append(cust_order_total_label)
        self.cust_order_discard_buttons.append(cust_order_discard_button)
        self.cust_order_resctrict_buttons.append(cust_order_resctrict_button)
        self.cust_order_save_buttons.append(cust_order_save_button)
        self.cust_order_pay_buttons.append(cust_order_pay_button)

class MySalesView(MyWidget):
    def __init__(self, model: MySalesModel):
        super().__init__(object_name='my_sales_view')

        self.model = model
        
        self.show_main_panel()

    def show_main_panel(self):
        self.model.set_main_panel_widgets()
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
        self.model.set_panel_box_a_widgets()

        self.panel_a_box = MyGroupBox()
        panel_a_layout = MyGridLayout()

        text_filter_box = MyGroupBox()
        text_filter_layout = MyHBoxLayout()
        text_filter_layout.addWidget(self.model.text_filter_field)
        text_filter_layout.addWidget(self.model.text_filter_button)
        text_filter_box.setLayout(text_filter_layout)

        barcode_scan_box = MyGroupBox()
        barcode_scan_layout = MyHBoxLayout()
        barcode_scan_layout.addWidget(self.model.barcode_scan_field)
        barcode_scan_layout.addWidget(self.model.barcode_scan_button[0])
        barcode_scan_layout.addWidget(self.model.barcode_scan_button[1])
        barcode_scan_box.setLayout(barcode_scan_layout)

        # region > on_prod_list_tab
        prod_list_a_box = MyGroupBox()
        prod_list_a_layout = MyVBoxLayout()

        prod_list_a_pag_box = MyGroupBox()
        prod_list_a_pag_layout = MyHBoxLayout()
        prod_list_a_pag_layout.addWidget(self.model.prod_list_a_pag_button[0])
        prod_list_a_pag_layout.addWidget(self.model.prod_list_a_pag_page_label)
        prod_list_a_pag_layout.addWidget(self.model.prod_list_a_pag_button[1])
        prod_list_a_pag_box.setLayout(prod_list_a_pag_layout)

        prod_list_a_layout.addWidget(self.model.prod_list_a_table)
        prod_list_a_layout.addWidget(prod_list_a_pag_box)
        prod_list_a_box.setLayout(prod_list_a_layout)

        prod_list_b_box = MyGroupBox()
        prod_list_b_layout = MyVBoxLayout()

        prod_list_b_pag_box = MyGroupBox()
        prod_list_b_pag_layout = MyHBoxLayout()
        prod_list_b_pag_layout.addWidget(self.model.prod_list_b_pag_button[0])
        prod_list_b_pag_layout.addWidget(self.model.prod_list_b_pag_page_label)
        prod_list_b_pag_layout.addWidget(self.model.prod_list_b_pag_button[1])
        prod_list_b_pag_box.setLayout(prod_list_b_pag_layout)

        prod_list_b_layout.addWidget(self.model.prod_list_b_table)
        prod_list_b_layout.addWidget(prod_list_b_pag_box)
        prod_list_b_box.setLayout(prod_list_b_layout)

        self.model.prod_list_tab.addTab(prod_list_a_box, 'Overview')
        self.model.prod_list_tab.addTab(prod_list_b_box, 'On sale')
        # endregion > prod_list_tab

        panel_a_layout.addWidget(text_filter_box,0,0)
        panel_a_layout.addWidget(barcode_scan_box,0,1)
        panel_a_layout.addWidget(self.model.prod_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(panel_a_layout)
        pass
    def show_panel_box_b(self):
        self.model.set_panel_box_b_widgets()

        self.panel_b_box = MyGroupBox()
        panel_b_layout = MyVBoxLayout()

        add_order_box = MyGroupBox()
        add_order_layout = MyHBoxLayout()
        add_order_layout.addWidget(self.model.add_order_cust_sel_field)
        add_order_layout.addWidget(self.model.add_order_type_field)
        add_order_layout.addWidget(self.model.add_order_button)
        add_order_layout.addWidget(self.model.add_order_load_button)
        add_order_box.setLayout(add_order_layout)

        panel_b_layout.addWidget(add_order_box)
        panel_b_layout.addWidget(self.model.cust_order_tab)
        self.panel_b_box.setLayout(panel_b_layout)
        pass
    def show_panel_box_c(self):
        self.model.set_panel_box_c_widgets()

        self.panel_c_box = MyGroupBox()
        panel_c_layout = MyHBoxLayout()
        panel_c_layout.addWidget(self.model.current_user_label)
        panel_c_layout.addWidget(self.model.pending_order_label)
        panel_c_layout.addWidget(self.model.available_product_label)
        self.panel_c_box.setLayout(panel_c_layout)
        pass

        pass

class MySalesController:
    def __init__(self, model: MySalesModel, view: MySalesView):
        self.model = model
        self.view = view

        self.set_add_order_conn()
        self.set_prod_list_a_pag_button_conn()
        self.set_cust_order_tab_conn()

        self.populate_prod_list_table()
        self.populate_cust_order_field()

    def set_add_order_conn(self):
        self.model.add_order_button.clicked.connect(self.populate_cust_order_box)
        self.model.add_order_load_button.clicked.connect(self.on_add_order_load_button_clicked)
    def set_prod_list_a_table_act_button_conn(self):
        self.model.prod_list_a_act_button[0].clicked.connect(lambda: self.on_prod_list_a_act_button_clicked(action='add'))
        self.model.prod_list_a_act_button[1].clicked.connect(lambda: self.on_prod_list_a_act_button_clicked(action='view'))
        pass
    def set_prod_list_a_pag_button_conn(self):
        self.model.prod_list_a_pag_button[0].clicked.connect(lambda: self.on_prod_list_a_pag_button_clicked(action='prev'))
        self.model.prod_list_a_pag_button[1].clicked.connect(lambda: self.on_prod_list_a_pag_button_clicked(action='next'))
    def set_cust_order_tab_conn(self):
        self.model.cust_order_tab.currentChanged.connect(self.on_cust_order_tab_current_changed)

    def populate_prod_list_table(self, text_filter='', order_type='Retail', page_number=1):
        self.model.set_prod_list_table_data_value(text_filter, order_type, page_number)

        self.model.prod_list_a_pag_button[0].setEnabled(self.model.page_number > 1)
        self.model.prod_list_a_pag_button[1].setEnabled(len(self.model.prod_list_a_table_data) == 30)

        self.model.prod_list_a_table.setRowCount(len(self.model.prod_list_a_table_data))
        
        for row_i, row_v in enumerate(self.model.prod_list_a_table_data):
            self.model.set_prod_list_act_widgets()

            prod_list_a_act_box = MyGroupBox()
            prod_list_a_act_layout = MyHBoxLayout(object_name='prod_list_a_act_layout')
            prod_list_a_act_layout.addWidget(self.model.prod_list_a_act_button[0])
            prod_list_a_act_layout.addWidget(self.model.prod_list_a_act_button[1])
            prod_list_a_act_box.setLayout(prod_list_a_act_layout)

            item_name = QTableWidgetItem(f"{row_v[1]}")
            brand = QTableWidgetItem(f"{row_v[4]}")
            sales_group = QTableWidgetItem(f"{row_v[5]}")
            price = QTableWidgetItem(f"{row_v[8]}")
            promo = QTableWidgetItem(f"{row_v[10]}")
            discount = QTableWidgetItem(f"{row_v[11]}")

            self.model.prod_list_a_table.setCellWidget(row_i, 0, prod_list_a_act_box)
            self.model.prod_list_a_table.setItem(row_i, 1, item_name)
            self.model.prod_list_a_table.setItem(row_i, 2, brand)
            self.model.prod_list_a_table.setItem(row_i, 3, sales_group)
            self.model.prod_list_a_table.setItem(row_i, 4, price)
            self.model.prod_list_a_table.setItem(row_i, 5, promo)
            self.model.prod_list_a_table.setItem(row_i, 6, discount)

            self.set_prod_list_a_table_act_button_conn()
            pass
        pass
    def populate_cust_order_field(self):
        self.model.add_order_cust_sel_field.addItem('New order')
        for cust_name in self.model.cust_name_data_list:
            self.model.add_order_cust_sel_field.addItem(cust_name[0])

        self.model.add_order_type_field.addItem('Retail')
        self.model.add_order_type_field.addItem('Wholesale')
        pass
    def populate_cust_order_box(self):
        i = self.model.cust_order_tab.currentIndex()
        
        self.model.set_cust_order_widgets()

        cust_order_box = MyGroupBox()
        cust_order_layout = MyVBoxLayout()

        self.model.cust_order_name_value = self.model.add_order_cust_sel_field.currentText()
        self.model.cust_order_type_value = self.model.add_order_type_field.currentText()

        cust_order_a_act_box = MyGroupBox()
        cust_order_a_act_layout = MyHBoxLayout()
        cust_order_a_act_layout.addWidget(self.model.cust_order_type_label)
        cust_order_a_act_layout.addWidget(self.model.cust_order_clear_button)
        cust_order_a_act_box.setLayout(cust_order_a_act_layout)

        cust_order_summary_box = MyGroupBox()
        cust_order_summary_layout = MyFormLayout()
        cust_order_summary_layout.addRow('Subtotal', self.model.cust_order_subtotal_label)
        cust_order_summary_layout.addRow('Discount', self.model.cust_order_discount_label)
        cust_order_summary_layout.addRow('Tax', self.model.cust_order_tax_label)
        cust_order_summary_layout.addRow('Total', self.model.cust_order_total_label)
        cust_order_summary_box.setLayout(cust_order_summary_layout)

        cust_order_b_act_box = MyGroupBox()
        cust_order_b_act_layout = MyVBoxLayout()
        cust_order_b_sub_act_layout = MyHBoxLayout()
        cust_order_b_sub_act_layout.addWidget(self.model.cust_order_discard_button)
        cust_order_b_sub_act_layout.addWidget(self.model.cust_order_resctrict_button[0])
        cust_order_b_sub_act_layout.addWidget(self.model.cust_order_resctrict_button[1])
        cust_order_b_sub_act_layout.addWidget(self.model.cust_order_save_button)
        cust_order_b_act_layout.addLayout(cust_order_b_sub_act_layout)
        cust_order_b_act_layout.addWidget(self.model.cust_order_pay_button)
        cust_order_b_act_box.setLayout(cust_order_b_act_layout)

        cust_order_layout.addWidget(cust_order_a_act_box)
        cust_order_layout.addWidget(self.model.cust_order_table)
        cust_order_layout.addWidget(cust_order_summary_box)
        cust_order_layout.addWidget(cust_order_b_act_box)
        cust_order_box.setLayout(cust_order_layout)

        self.model.append_cust_order_data(
            cust_order_name_value=self.model.cust_order_name_value,
            cust_order_type_value=self.model.cust_order_type_value,

            cust_order_subtotal_value=self.model.cust_order_subtotal_value,
            cust_order_discount_value=self.model.cust_order_discount_value,
            cust_order_tax_value=self.model.cust_order_tax_value,
            cust_order_total_value=self.model.cust_order_total_value,

            cust_order_type_label=self.model.cust_order_type_label,
            cust_order_clear_button=self.model.cust_order_clear_button,
            cust_order_table=self.model.cust_order_table,

            cust_order_subtotal_label=self.model.cust_order_subtotal_label,
            cust_order_discount_label=self.model.cust_order_discount_label,
            cust_order_tax_label=self.model.cust_order_tax_label,
            cust_order_total_label=self.model.cust_order_total_label,
            cust_order_discard_button=self.model.cust_order_discard_button,
            cust_order_resctrict_button=self.model.cust_order_resctrict_button,
            cust_order_save_button=self.model.cust_order_save_button,
            cust_order_pay_button=self.model.cust_order_pay_button
        )

        new_i = self.model.cust_order_tab.addTab(cust_order_box, self.model.add_order_cust_sel_field.currentText())
        self.model.cust_order_tab.setCurrentIndex(new_i)
        self.model.pending_order_label.setText(f"Pending order: {self.model.cust_order_tab.count()}")


    def on_add_order_button_clicked(self):
        self.populate_cust_order_box()
        pass
    def on_add_order_load_button_clicked(self):
        pass

    def on_prod_list_a_act_button_clicked(self, action):
        if action == 'add':
            print('action:', action)
            pass
        elif action == 'view':
            print('action:', action)
            pass
            pass
    def on_prod_list_a_pag_button_clicked(self, action):
        i = self.model.cust_order_tab.currentIndex()

        if action == 'prev':
            if self.model.page_number > 1:
                self.model.page_number -= 1
                self.model.prod_list_a_pag_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_prod_list_table(text_filter=self.model.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
            pass
        elif action == 'next':
            self.model.page_number += 1
            self.model.prod_list_a_pag_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
            
            self.populate_prod_list_table(text_filter=self.model.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
            pass
        pass

    def on_cust_order_tab_current_changed(self):
        i = self.model.cust_order_tab.currentIndex()

        self.populate_prod_list_table(text_filter=self.model.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        

if __name__ == ('__main__'):
    app = QApplication(sys.argv)

    schema = SalesSchema()

    model = MySalesModel(schema)
    view = MySalesView(model)
    controller = MySalesController(model, view)

    view.show()
    sys.exit(app.exec())
