import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))
print('sys path: ', os.path.abspath(''))

from src.core.color_scheme import *
from src.core.manual_csv_importer import *
from src.core.receipt_printer import *

from database.user.sales import *
from widget.user.sales import *

class SalesModel:
    def __init__(self, schema: SalesSchema):

        self.schema = schema

        self.set_a_panel_container()
        self.set_b_panel_container()
        self.set_c_panel_container()
        self.set_populate_cust_tab_container()

    def set_a_panel_container(self):
        # region > b_panel
        self.curr_tab = ''
        self.curr_page = 1
        self.total_page = self.schema.count_product_list_total_pages(txn_type='Retail')
        # endregion
    def set_b_panel_container(self):
        self.cust_name_list = self.schema.list_customer()
        pass
    def set_c_panel_container(self):
        # region > c_panel
        self.curr_user = '[no user]'
        self.total_cust_order = 0
        self.total_prod = self.schema.count_product()
        # endregion
        # region > cust_tab_cont
        
    def set_populate_cust_tab_container(self):
        self.cust_name = []

        self.order_list_table = []
        self.order_retail_button = []
        self.order_wholesale_button = []
        self.order_a_clr_list_button = []

        self.order_subtotal = []
        self.order_discount = []
        self.order_tax = []
        self.order_total = []

        self.order_subtotal_label = []
        self.order_discount_label = []
        self.order_tax_label = []
        self.order_total_label = []

        self.order_discard_button = []
        self.order_unlocked_button = []
        self.order_locked_button = []
        self.order_save_button = []

        self.order_pay_button = []
        # endregion

    def append_cust_tab_cont_var(
        self,
        cust_name,
        order_list_table,
        order_a_sub_retail_button,
        order_a_sub_wholesale_button,
        order_a_clr_list_button,
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
        order_pay_button,
    ):
        self.cust_name.append([cust_name])

        self.order_list_table.append([order_list_table])
        self.order_retail_button.append([order_a_sub_retail_button])
        self.order_wholesale_button.append([order_a_sub_wholesale_button])
        self.order_a_clr_list_button.append([order_a_clr_list_button])
        self.order_subtotal.append([order_subtotal_value])
        self.order_discount.append([order_discount_value])
        self.order_tax.append([order_tax_value])
        self.order_total.append([order_total_value])
        self.order_subtotal_label.append([order_subtotal_label])
        self.order_discount_label.append([order_discount_label])
        self.order_tax_label.append([order_tax_label])
        self.order_total_label.append([order_total_label])
        self.order_discard_button.append([order_discard_button])
        self.order_unlocked_button.append([order_unlocked_button])
        self.order_locked_button.append([order_locked_button])
        self.order_save_button.append([order_save_button])
        self.order_pay_button.append([order_pay_button])
        pass

class SalesView(MyWidget):
    def __init__(self, model: SalesModel):
        super().__init__()

        self.model = model

        self.show_main_panel()
        self.default_layout()
        self.sync_layout()

    def default_layout(self):
        self.barcode_scan_untoggled_button
        self.barcode_scan_toggled_button
        pass

    def sync_layout(self):
        self.total_cust_order_label.setText(f"Pending order: {self.cust_order_tab.count()}")
        pass
    
    def populate_add_cust_name_field(self):
        self.add_order_cust_name_field.clear()

        self.add_order_cust_name_field.addItem('New customer')
        for cust_name in self.model.cust_name_list:
            self.add_order_cust_name_field.addItems(cust_name)
        pass

    def populate_cust_tab(self):
        cust_name = self.add_order_cust_name_field.currentText()
        cust_tab_cont_panel = MyGroupBox(object_name='cust_tab_cont_panel')
        cust_tab_cont_panel_panel = MyGridLayout(object_name='cust_tab_cont_panel_panel')

        order_a_act_panel = MyGroupBox(object_name='order_a_act_panel')
        order_a_act_panel_layout = MyHBoxLayout(object_name='order_a_act_panel_layout')
        order_a_sub_retail_button = MyPushButton(object_name='order_retail_button', text='Retail') 
        order_a_sub_wholesale_button = MyPushButton(object_name='order_wholesale_button', text='Wholesale')
        order_a_clr_list_button = MyPushButton(object_name='order_a_clr_list_button', text='Clear')
        order_a_act_panel_layout.addWidget(order_a_sub_retail_button)
        order_a_act_panel_layout.addWidget(order_a_sub_wholesale_button)
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

        order_b_sub_act_panel = MyGroupBox(object_name='order_b_sub_act_panel')
        order_b_sub_act_panel_layout = MyHBoxLayout(object_name='order_b_sub_act_panel_layout')
        order_discard_button = MyPushButton(object_name='order_discard_button', text='Discard')
        order_unlocked_button = MyPushButton(object_name='order_unlocked_button', text='Unlocked')
        order_locked_button = MyPushButton(object_name='order_locked_button', text='Locked')
        order_save_button = MyPushButton(object_name='order_save_button', text='Save') 

        order_b_sub_act_panel_layout.addWidget(order_discard_button)
        order_b_sub_act_panel_layout.addWidget(order_unlocked_button)
        order_b_sub_act_panel_layout.addWidget(order_locked_button)
        order_b_sub_act_panel_layout.addWidget(order_save_button)
        order_b_sub_act_panel.setLayout(order_b_sub_act_panel_layout)

        order_pay_button = MyPushButton(object_name='order_pay_button', text='Pay')

        order_b_act_panel_layout.addWidget(order_b_sub_act_panel)
        order_b_act_panel_layout.addWidget(order_pay_button)
        order_b_act_panel.setLayout(order_b_act_panel_layout)

        cust_tab_cont_panel_panel.addWidget(order_a_act_panel,0,0)
        cust_tab_cont_panel_panel.addWidget(order_list_table,1,0)
        cust_tab_cont_panel_panel.addWidget(order_summ_panel,2,0)
        cust_tab_cont_panel_panel.addWidget(order_b_act_panel,3,0)
        cust_tab_cont_panel.setLayout(cust_tab_cont_panel_panel)

        self.cust_order_tab.addTab(cust_tab_cont_panel, cust_name)

        self.model.append_cust_tab_cont_var(
            cust_name=cust_name,
            order_list_table=order_list_table,
            order_a_sub_retail_button=order_a_sub_retail_button,
            order_a_sub_wholesale_button=order_a_sub_wholesale_button,
            order_a_clr_list_button=order_a_clr_list_button,
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

    def show_b_panel(self):
        self.b_panel = MyGroupBox(object_name='b_panel')
        self.b_panel_layout = MyGridLayout(object_name='b_panel_layout')

        self.add_order_act_panel = MyGroupBox(object_name='add_order_act_panel')
        self.add_order_act_panel_layout = MyHBoxLayout(object_name='add_order_act_panel_layout')
        self.add_order_cust_name_field = MyComboBox(object_name='add_order_cust_name_field')
        self.add_order_button = MyPushButton(object_name='add_order_button', text='Add')
        self.load_order_button = MyPushButton(object_name='load_order_button', text='Load')
        self.add_order_act_panel_layout.addWidget(self.add_order_cust_name_field)
        self.add_order_act_panel_layout.addWidget(self.add_order_button)
        self.add_order_act_panel_layout.addWidget(self.load_order_button)
        self.add_order_act_panel.setLayout(self.add_order_act_panel_layout)

        self.cust_order_tab = MyTabWidget(object_name='cust_order_tab')

        self.b_panel_layout.addWidget(self.add_order_act_panel)
        self.b_panel_layout.addWidget(self.cust_order_tab)
        self.b_panel.setLayout(self.b_panel_layout)

        self.populate_add_cust_name_field()
        self.populate_cust_tab()

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
        
        self.main_panel_layout.addWidget(self.a_panel,0,0)
        self.main_panel_layout.addWidget(self.b_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.c_panel,1,0)
        self.setLayout(self.main_panel_layout)

class SalesController:
    def __init__(self, model: SalesModel, view: SalesView):
        self.model = model
        self.view = view

        self.set_connections()

    def set_connections(self):
        # region > a_panel
        self.view.text_filter_field.textChanged.connect(self.on_text_filter_field_text_changed)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        # endregion
        # region > b_panel
        self.view.add_order_button.clicked.connect(self.on_add_order_button_clicked)
        
        self.view.add_order_button.clicked.connect(self.view.populate_cust_tab)
        # endregion
        pass

    # region > a_panel
    def on_text_filter_button_clicked(self):
        print('on_text_filter_button_clicked')
        pass
    def on_text_filter_field_text_changed(self):
        print('on_text_filter_field_text_changed')
    # endregion

    # region > b_panel
    def on_add_order_button_clicked(self):
        print('on_add_order_button_clicked')
        self.view.total_cust_order_label.setText(f"Pending order: {self.view.cust_order_tab.count()+1}")
        pass
    # endregion

if __name__ == ('__main__'):
    app = QApplication(sys.argv)

    schema = SalesSchema()

    model = SalesModel(schema)
    view = SalesView(model)
    controller = SalesController(model, view)

    view.show()
    sys.exit(app.exec())
