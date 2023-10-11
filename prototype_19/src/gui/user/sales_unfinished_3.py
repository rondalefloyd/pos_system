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

        self.prod_table_b_data = schema.list_product_via_promo()
        self.cust_data = schema.list_customer()

        self.text_filter_field = MyLineEdit()
        self.text_filter_button = MyPushButton(text='Filter')

        self.barcode_scan_field = MyLineEdit()
        self.barcode_scan_toggle_button = MyPushButton(text='AATC Off')
        self.barcode_scan_untoggle_button = MyPushButton(text='AATC On')

        self.prod_table_a = MyTableWidget(object_name='prod_table_a')
        self.prod_table_b = MyTableWidget(object_name='prod_table_b')

        self.current_page = 1
        self.total_page = schema.count_product_list_total_pages()

        self.cust_order_tab = MyTabWidget()

        self.current_user_value = '<Empty>'
        self.available_prod_count_value = schema.count_product()

        # region > cust_order_tab
        self.new_quantity = int(0)
        self.new_price = float(0)
        self.new_discount = float(0)

        self.cust_name_values = []
        self.order_type_values = []
        self.order_type_labels: List[QLabel] = []
        self.clr_order_buttons: List[QPushButton] = []

        self.cust_order_tables: List[QTableWidget] = []

        self.order_sub_total_values = []
        self.order_discount_values = []
        self.order_tax_values = []
        self.order_total_values = []

        self.order_sub_total_labels: List[QLabel] = []
        self.order_discount_labels: List[QLabel] = []
        self.order_tax_labels: List[QLabel] = []
        self.order_total_labels: List[QLabel] = []

        self.discard_order_buttons: List[QPushButton] = []
        self.lock_order_toggle_buttons: List[QPushButton] = []
        self.lock_order_untoggle_buttons: List[QPushButton] = []
        self.save_order_buttons: List[QPushButton] = []

        self.order_pay_buttons: List[QPushButton] = []
        # endregion > cust_order_tab
        
        self.cust_order_list_data = []
        self.invoice_info_data = []

    def set_prod_tab_table_act_panel_widgets(self):
        self.prod_table_a_add_item_button = MyPushButton(text='Add')
        self.prod_table_a_view_item_button = MyPushButton(text='View')
        self.prod_table_b_add_item_button = MyPushButton(text='Add')
        self.prod_table_b_view_item_button = MyPushButton(text='View')
    def set_prod_table_pag_panel_widgets(self):
        self.prod_table_a_pag_prev_button = MyPushButton(text='Prev')
        self.prod_table_a_pag_page_label = MyLabel(text=f"{self.current_page}/{self.total_page}")
        self.prod_table_a_pag_next_button = MyPushButton(text='Next')

        self.prod_table_b_pag_prev_button = MyPushButton(text='Prev')
        self.prod_table_b_pag_page_label = MyLabel(text=f"{self.current_page}/{self.total_page}")
        self.prod_table_b_pag_next_button = MyPushButton(text='Next')
        pass
    def set_cust_order_act_panel_widgets(self):
        self.cust_sel_field = MyComboBox()
        self.order_type_sel_field = MyComboBox()
        self.add_cust_order_button = MyPushButton(text='Add')
        self.load_cust_order_button = MyPushButton(text='Load')
    def set_cust_order_table_act_panel_widgets(self):
        self.drop_all_quantity_button = MyPushButton(text='Drop all')
        self.drop_quantity_button = MyPushButton(text='Drop')
        self.add_quantity_button = MyPushButton(text='Add')
        self.edit_quantity_button = MyPushButton(text='Edit')
    def set_cust_order_tab_widgets(self):
        self.cust_name_value = str(self.cust_sel_field.currentText())
        self.order_type_value = str(self.order_type_sel_field.currentText())
        self.order_type_label = MyLabel(text=f"Order type: {self.order_type_value}")
        self.clr_order_button = MyPushButton(text='Clear')
        self.cust_order_table = MyTableWidget(object_name='cust_order_table')

        self.order_sub_total_value = float(0)
        self.order_discount_value = float(0)
        self.order_tax_value = float(0)
        self.order_total_value = float(0)

        self.order_sub_total_label = MyLabel(text=f"₱{self.order_sub_total_value:.2f}")
        self.order_discount_label = MyLabel(text=f"₱{self.order_discount_value:.2f}")
        self.order_tax_label = MyLabel(text=f"₱{self.order_tax_value:.2f}")
        self.order_total_label = MyLabel(text=f"₱{self.order_total_value:.2f}")
        self.discard_order_button = MyPushButton(text='Discard')
        self.lock_order_toggle_button = MyPushButton(text='Lock')
        self.lock_order_untoggle_button = MyPushButton(text='Unlock')
        self.save_order_button = MyPushButton(text='Save')
        self.order_pay_button = MyPushButton(text=f"Pay ₱{self.order_total_value}")
        pass
    def set_panel_c_widgets(self):
        self.current_user_label = MyLabel(text=f"Current user: {self.current_user_value}")
        self.pending_order_count_label = MyLabel(text=f"Pending order: {self.cust_order_tab.count()}")
        self.available_prod_count_label = MyLabel(text=f"Available product: {self.available_prod_count_value}")
    
    def set_print_sel_panel_widgets(self):
        self.print_receipt_button = MyPushButton(text='Receipt')
        self.print_invoice_button = MyPushButton(text='Invoice')
        pass
    def set_invoice_form_dialog_widgets(self):
        self.invoice_customer_name = MyLineEdit()
        self.invoice_company = MyLineEdit()
        self.invoice_phone = MyLineEdit()
        self.invoice_print_button = MyPushButton(text='Print')
    # TODO: last thing to do
    def set_panel_d_dialog_widgets(self):
        # IDEA: dialogs
        i = self.cust_order_tab.currentIndex()
        
        self.amount_tendered_field = MyLineEdit()
        self.numpad_toggle_button = MyPushButton(text='Numpad Off')
        self.numpad_untoggle_button = MyPushButton(text='Numpad On')
        self.numpad_buttons = [
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
        
        self.pay_cash_button = MyPushButton(text='Cash')
        self.pay_points_button = MyPushButton(text='Points')

        self.cust_name_label = MyLabel(text=f"{self.cust_name_values[i]}")
        self.cust_phone_label = MyLabel(text=f"") # TODO: leave blank temporarily
        self.cust_points_label = MyLabel(text=f"") # TODO: leave blank temporarily

        self.order_final_type_label = MyLabel(text=f"{self.order_type_values[i]}")
        self.order_final_sub_total_label = MyLabel(text=f"{self.order_sub_total_values[i]:.2f}")
        self.order_final_discount_label = MyLabel(text=f"{self.order_discount_values[i]:.2f}")
        self.order_final_tax_label = MyLabel(text=f"{self.order_tax_values[i]:.2f}")
        self.order_final_total_label = MyLabel(text=f"{self.order_total_values[i]:.2f}")
    def set_panel_e_dialog_widgets(self):
        self.order_change = MyLabel(f"0.00")

    def append_cust_order_tab_data(
        self,
        cust_name_value,
        order_type_value,
        order_type_label,
        clr_order_button,
        cust_order_table,

        order_sub_total_value,
        order_discount_value,
        order_tax_value,
        order_total_value,

        order_sub_total_label,
        order_discount_label,
        order_tax_label,
        order_total_label,
        discard_order_button,
        lock_order_toggle_button,
        lock_order_untoggle_button,
        save_order_button,
        order_pay_button
    ):
        self.cust_name_values.append(cust_name_value)
        self.order_type_values.append(order_type_value)
        self.order_type_labels.append(order_type_label)
        self.clr_order_buttons.append(clr_order_button)
        self.cust_order_tables.append(cust_order_table)

        self.order_sub_total_values.append(order_sub_total_value)
        self.order_discount_values.append(order_discount_value)
        self.order_tax_values.append(order_tax_value)
        self.order_total_values.append(order_total_value)

        self.order_sub_total_labels.append(order_sub_total_label)
        self.order_discount_labels.append(order_discount_label)
        self.order_tax_labels.append(order_tax_label)
        self.order_total_labels.append(order_total_label)
        self.discard_order_buttons.append(discard_order_button)
        self.lock_order_toggle_buttons.append(lock_order_toggle_button)
        self.lock_order_untoggle_buttons.append(lock_order_untoggle_button)
        self.save_order_buttons.append(save_order_button)
        self.order_pay_buttons.append(order_pay_button)
        pass
    def append_cust_order_list_data(self, item_row_data):
        self.cust_order_list_data.append(item_row_data)
    def append_invoice_info_data(self, item_row_data):
        self.invoice_info_data.append(item_row_data)

    def remove_cust_order_tab_data(self, i):
        self.cust_name_values.remove(self.cust_name_values[i])
        self.order_type_values.remove(self.order_type_values[i])
        self.order_type_labels.remove(self.order_type_labels[i])
        self.clr_order_buttons.remove(self.clr_order_buttons[i])
        self.cust_order_tables.remove(self.cust_order_tables[i])
        self.order_sub_total_values.remove(self.order_sub_total_values[i])
        self.order_discount_values.remove(self.order_discount_values[i])
        self.order_tax_values.remove(self.order_tax_values[i])
        self.order_total_values.remove(self.order_total_values[i])
        self.order_sub_total_labels.remove(self.order_sub_total_labels[i])
        self.order_discount_labels.remove(self.order_discount_labels[i])
        self.order_tax_labels.remove(self.order_tax_labels[i])
        self.order_total_labels.remove(self.order_total_labels[i])
        self.discard_order_buttons.remove(self.discard_order_buttons[i])
        self.lock_order_toggle_buttons.remove(self.lock_order_toggle_buttons[i])
        self.lock_order_untoggle_buttons.remove(self.lock_order_untoggle_buttons[i])
        self.save_order_buttons.remove(self.save_order_buttons[i])
        self.order_pay_buttons.remove(self.order_pay_buttons[i])
        pass
    def remove_cust_order_list_data(self, i):
        self.cust_order_list_data.remove(self.cust_order_list_data[i])
    def remove_invoice_info_data(self, i):
        self.invoice_info_data.remove(self.invoice_info_data[i])

class MySalesView(MyWidget):
    def __init__(self, model: MySalesModel):
        super().__init__(object_name='my_sales_view')

        self.model = model
        
        self.show_main_panel()

    def show_main_panel(self):
        main_panel_layout = MyGridLayout()

        self.show_panel_a()
        self.show_panel_b()
        self.show_panel_c()

        main_panel_layout.addWidget(self.panel_a,0,0)
        main_panel_layout.addWidget(self.panel_b,0,1,2,1)
        main_panel_layout.addWidget(self.panel_c,1,0)
        self.setLayout(main_panel_layout)
        pass

    def show_panel_a(self):
        self.panel_a = MyGroupBox()
        panel_a_layout = MyVBoxLayout()

        # region > act_a_layout
        act_a_panel = MyGroupBox()
        act_a_panel_layout = MyHBoxLayout()

        text_filter_act_panel = MyGroupBox()
        text_filter_act_panel_layout = MyHBoxLayout()
        text_filter_act_panel_layout.addWidget(self.model.text_filter_field)
        text_filter_act_panel_layout.addWidget(self.model.text_filter_button)
        text_filter_act_panel.setLayout(text_filter_act_panel_layout)

        barcode_scan_act_panel = MyGroupBox()
        barcode_scan_act_panel_layout = MyHBoxLayout()
        barcode_scan_act_panel_layout.addWidget(self.model.barcode_scan_field)
        barcode_scan_act_panel_layout.addWidget(self.model.barcode_scan_toggle_button)
        barcode_scan_act_panel_layout.addWidget(self.model.barcode_scan_untoggle_button)
        barcode_scan_act_panel.setLayout(barcode_scan_act_panel_layout)

        act_a_panel_layout.addWidget(text_filter_act_panel)
        act_a_panel_layout.addWidget(barcode_scan_act_panel)
        act_a_panel.setLayout(act_a_panel_layout)
        # endregion > act_a_layout
        
        # region > prod_tab
        prod_tab = MyTabWidget()

        self.model.set_prod_table_pag_panel_widgets()
        # region > prod_tab_panel_a
        prod_tab_panel_a = MyGroupBox()
        prod_tab_panel_a_layout = MyVBoxLayout()
        
        pgtn_act_panel_a = MyGroupBox()
        pgtn_act_panel_a_layout = MyHBoxLayout()
        pgtn_act_panel_a_layout.addWidget(self.model.prod_table_a_pag_prev_button)
        pgtn_act_panel_a_layout.addWidget(self.model.prod_table_a_pag_page_label)
        pgtn_act_panel_a_layout.addWidget(self.model.prod_table_a_pag_next_button)
        pgtn_act_panel_a.setLayout(pgtn_act_panel_a_layout)
        prod_tab_panel_a_layout.addWidget(self.model.prod_table_a)
        prod_tab_panel_a_layout.addWidget(pgtn_act_panel_a)
        prod_tab_panel_a.setLayout(prod_tab_panel_a_layout)
        # endregion > prod_tab_panel_a
        
        # region > prod_tab_panel_b
        prod_tab_panel_b = MyGroupBox()
        prod_tab_panel_b_layout = MyVBoxLayout()
        
        pgtn_act_panel_b = MyGroupBox()
        pgtn_act_panel_b_layout = MyHBoxLayout()
        pgtn_act_panel_b_layout.addWidget(self.model.prod_table_b_pag_prev_button)
        pgtn_act_panel_b_layout.addWidget(self.model.prod_table_b_pag_page_label)
        pgtn_act_panel_b_layout.addWidget(self.model.prod_table_b_pag_next_button)
        pgtn_act_panel_b.setLayout(pgtn_act_panel_b_layout)
        prod_tab_panel_b_layout.addWidget(self.model.prod_table_b)
        prod_tab_panel_b_layout.addWidget(pgtn_act_panel_b)
        prod_tab_panel_b.setLayout(prod_tab_panel_b_layout)
        # endregion > prod_tab_panel_b

        prod_tab.addTab(prod_tab_panel_a, 'Overview')
        prod_tab.addTab(prod_tab_panel_b, 'On sale')
        # endregion > prod_tab

        panel_a_layout.addWidget(act_a_panel)
        panel_a_layout.addWidget(prod_tab)
        self.panel_a.setLayout(panel_a_layout)
        pass

    def show_panel_b(self):
        self.model.set_cust_order_act_panel_widgets()

        self.panel_b = MyGroupBox()
        panel_b_layout = MyVBoxLayout()
        
        act_a_panel = MyGroupBox()
        act_a_panel_layout = MyHBoxLayout()
        act_a_panel_layout.addWidget(self.model.cust_sel_field)
        act_a_panel_layout.addWidget(self.model.order_type_sel_field)
        act_a_panel_layout.addWidget(self.model.add_cust_order_button)
        act_a_panel_layout.addWidget(self.model.load_cust_order_button)
        act_a_panel.setLayout(act_a_panel_layout)

        panel_b_layout.addWidget(act_a_panel)
        panel_b_layout.addWidget(self.model.cust_order_tab)
        self.panel_b.setLayout(panel_b_layout)
        pass

    def show_panel_c(self):
        self.panel_c = MyGroupBox()
        panel_c_layout = MyHBoxLayout()
        self.model.set_panel_c_widgets()
        panel_c_layout.addWidget(self.model.current_user_label)
        panel_c_layout.addWidget(self.model.pending_order_count_label)
        panel_c_layout.addWidget(self.model.available_prod_count_label)
        self.panel_c.setLayout(panel_c_layout)

    # IDEA: dialogs
    def show_panel_d(self):
        i = self.model.cust_order_tab.currentIndex()

        self.model.set_panel_d_dialog_widgets()

        self.panel_d = MyDialog()
        panel_d_layout = MyGridLayout()

        cash_drawer_panel = MyGroupBox()
        cash_drawer_panel_layout = MyVBoxLayout()

        numpad_act_panel = MyGroupBox()
        numpad_act_panel_layout = MyHBoxLayout()
        numpad_act_panel_layout.addWidget(self.model.amount_tendered_field)
        numpad_act_panel_layout.addWidget(self.model.numpad_toggle_button)
        numpad_act_panel_layout.addWidget(self.model.numpad_untoggle_button)
        numpad_act_panel.setLayout(numpad_act_panel_layout)
        
        numpad_buttons_panel = MyGroupBox()
        numpad_buttons_panel_layout = MyGridLayout()
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[0],0,0)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[1],0,1)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[2],0,2)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[3],1,0)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[4],1,1)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[5],1,2)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[6],2,0)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[7],2,1)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[8],2,2)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[9],3,0)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[10],3,1)
        numpad_buttons_panel_layout.addWidget(self.model.numpad_buttons[11],3,2)
        numpad_buttons_panel.setLayout(numpad_buttons_panel_layout)

        payment_type_panel = MyGroupBox()
        payment_type_panel_layout = MyHBoxLayout()
        payment_type_panel_layout.addWidget(self.model.pay_cash_button)
        payment_type_panel_layout.addWidget(self.model.pay_points_button)
        payment_type_panel.setLayout(payment_type_panel_layout)

        cust_info_panel = MyGroupBox()
        cust_info_panel_layout = MyFormLayout()
        cust_info_panel_layout.addRow('Customer name:', self.model.cust_name_label)
        cust_info_panel_layout.addRow('Phone:', self.model.cust_phone_label)
        cust_info_panel_layout.addRow('Points:', self.model.cust_points_label)
        cust_info_panel.setLayout(cust_info_panel_layout)

        cash_drawer_panel_layout.addWidget(numpad_act_panel)
        cash_drawer_panel_layout.addWidget(numpad_buttons_panel)
        cash_drawer_panel_layout.addWidget(payment_type_panel)
        cash_drawer_panel_layout.addWidget(cust_info_panel)
        cash_drawer_panel.setLayout(cash_drawer_panel_layout)

        order_summary_panel = MyGroupBox()
        order_summary_panel_layout = MyFormLayout()
        order_summary_panel_layout.addRow('Order type:', self.model.order_final_type_label)
        order_summary_panel_layout.addRow('Sub total:', self.model.order_final_sub_total_label)
        order_summary_panel_layout.addRow('Discount:', self.model.order_final_discount_label)
        order_summary_panel_layout.addRow('Tax:', self.model.order_final_tax_label)
        order_summary_panel_layout.addRow('Total:', self.model.order_final_total_label)
        order_summary_panel.setLayout(order_summary_panel_layout)

        panel_d_layout.addWidget(cash_drawer_panel,0,0)
        panel_d_layout.addWidget(order_summary_panel,0,1)
        self.panel_d.setLayout(panel_d_layout)
        pass
    def show_print_sel_dialog(self):
        self.model.set_print_sel_panel_widgets()

        self.sel_option_dialog = MyDialog()
        sel_option_dialog_layout = MyVBoxLayout()

        print_sel_label = MyLabel(text='Select option:')

        confirm_act_panel = MyGroupBox()
        confirm_act_panel_layout = MyHBoxLayout()
        confirm_act_panel_layout.addWidget(self.model.print_receipt_button)
        confirm_act_panel_layout.addWidget(self.model.print_invoice_button)
        confirm_act_panel.setLayout(confirm_act_panel_layout)

        sel_option_dialog_layout.addWidget(print_sel_label)
        sel_option_dialog_layout.addWidget(confirm_act_panel)
        self.sel_option_dialog.setLayout(sel_option_dialog_layout)

        pass
    def show_invoice_form_dialog(self):
        self.model.set_invoice_form_dialog_widgets()

        self.invoice_form_dialog = MyDialog()
        invoice_form_dialog_layout = QFormLayout()

        invoice_act_panel = MyGroupBox()
        invoice_act_panel_layout = MyHBoxLayout()
        invoice_act_panel_layout.addWidget(self.model.invoice_print_button)
        invoice_act_panel.setLayout(invoice_act_panel_layout)

        invoice_form_dialog_layout.addRow('Customer name:', self.model.invoice_customer_name)
        invoice_form_dialog_layout.addRow('Company:', self.model.invoice_company)
        invoice_form_dialog_layout.addRow('Phone:', self.model.invoice_phone)
        invoice_form_dialog_layout.addRow(invoice_act_panel)
        self.invoice_form_dialog.setLayout(invoice_form_dialog_layout)

    # TODO: last thing to do
    def show_panel_e(self):
        self.model.set_panel_e_dialog_widgets()

        self.panel_e = MyDialog()
        panel_e_layout = MyGridLayout()

        order_change_panel = MyGroupBox()
        order_change_panel_layout = MyVBoxLayout()
        order_change_panel_layout.addWidget(MyLabel(text='Change:'))
        order_change_panel_layout.addWidget(self.model.order_change)
        order_change_panel.setLayout(order_change_panel_layout)

        act_a_panel = MyGroupBox()
        act_a_panel_layout = MyHBoxLayout()
        act_a_panel_layout.addWidget(self.model.cust_sel_field)
        act_a_panel_layout.addWidget(self.model.order_type_sel_field)
        act_a_panel_layout.addWidget(self.model.add_cust_order_button)
        act_a_panel.setLayout(act_a_panel_layout)

        panel_e_layout.addWidget(order_change_panel)
        panel_e_layout.addWidget(act_a_panel)
        self.panel_e.setLayout(panel_e_layout)

class MySalesController:
    def __init__(self, model: MySalesModel, view: MySalesView):
        self.model = model
        self.view = view

        self.populate_prod_tab_table_a()
        self.populate_act_panel_fields()

        self.set_prod_tab_panel_connections()
        self.on_add_cust_order_button_clicked()

        self.model.add_cust_order_button.clicked.connect(self.on_add_cust_order_button_clicked)

        self.model.cust_order_tab.currentChanged.connect(self.on_cust_order_tab_current_changed)

    # region > connections
    def set_prod_tab_panel_connections(self):
        self.model.prod_table_a_pag_prev_button.clicked.connect(lambda: self.on_prod_table_a_pag_button_clicked(action='prev'))
        self.model.prod_table_a_pag_next_button.clicked.connect(lambda: self.on_prod_table_a_pag_button_clicked(action='next'))
        pass
    def set_prod_tab_table_a_act_panel_connections(self, row_v):
        self.model.prod_table_a_add_item_button.clicked.connect(lambda _, row_v=row_v: self.on_prod_table_a_add_item_button_clicked(row_v))
        pass
    def set_cust_order_act_panel_connections(self):
        self.model.discard_order_button.clicked.connect(self.on_discard_order_button_clicked)
        self.model.lock_order_toggle_button.clicked.connect(self.on_lock_order_toggle_button_clicked)
        self.model.lock_order_untoggle_button.clicked.connect(self.on_lock_order_untoggle_button_clicked)
        self.model.save_order_button.clicked.connect(self.on_save_order_button_clicked)
        self.model.order_pay_button.clicked.connect(self.on_order_pay_button_clicked)
        pass
    def set_cust_order_table_act_panel_connections(self, row_v):
        self.model.drop_all_quantity_button.clicked.connect(lambda: self.on_drop_all_quantity_button_clicked(row_v))
        self.model.drop_quantity_button.clicked.connect(lambda: self.on_drop_quantity_button_clicked(row_v))
        self.model.add_quantity_button.clicked.connect(lambda: self.on_add_quantity_button_clicked(row_v))
        self.model.edit_quantity_button.clicked.connect(lambda: self.on_edit_quantity_button_clicked(row_v))
        pass
    def set_payment_type_panel_connections(self):
        self.model.pay_cash_button.clicked.connect(self.on_pay_cash_button_clicked)
        self.model.pay_points_button.clicked.connect(self.on_pay_points_button_clicked)
        pass
    def set_confirm_act_panel_connections(self):
        self.model.print_receipt_button.clicked.connect(lambda: self.on_print_button_clicked(action='do_print_receipt'))
        self.model.print_invoice_button.clicked.connect(self.on_print_invoice_button_clicked)
        pass
    def set_invoice_act_panel_connections(self):
        self.model.invoice_print_button.clicked.connect(lambda: self.on_print_button_clicked(action='do_print_invoice'))
        pass
    def set_add_new_cust_order_act_panel_connections(self):
        self.model.add_cust_order_button.clicked.connect(self.on_add_new_cust_order_button_clicked)
        pass
    def set_numpad_button_connections(self):
        self.model.numpad_buttons[0].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='1'))
        self.model.numpad_buttons[1].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='2'))
        self.model.numpad_buttons[2].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='3'))
        self.model.numpad_buttons[3].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='4'))
        self.model.numpad_buttons[4].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='5'))
        self.model.numpad_buttons[5].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='6'))
        self.model.numpad_buttons[6].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='7'))
        self.model.numpad_buttons[7].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='8'))
        self.model.numpad_buttons[8].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='9'))
        self.model.numpad_buttons[9].clicked.connect(lambda: self.on_numpad_buttons_clicked(value=''))
        self.model.numpad_buttons[10].clicked.connect(lambda: self.on_numpad_buttons_clicked(value='0'))
        self.model.numpad_buttons[11].clicked.connect(lambda: self.on_numpad_buttons_clicked(value=''))
    def set_invoice_form_dialog_connections(self):
        self.model.print_invoice_button.clicked.connect(lambda: self.on_print_invoice_button_clicked())
    
    # endregion > connections

    # region > populate
    def populate_prod_tab_table_a(self, text_filter='', order_type='Retail', page_number=1):
        self.model.prod_table_a_data = schema.list_product(text_filter, order_type, page_number)

        self.model.prod_table_a_pag_prev_button.setEnabled(self.model.current_page > 1)
        self.model.prod_table_a_pag_next_button.setEnabled(len(self.model.prod_table_a_data) == 30)
        
        self.model.prod_table_a.setRowCount(len(self.model.prod_table_a_data))

        for row_i, row_v in enumerate(self.model.prod_table_a_data):
            self.model.set_prod_tab_table_act_panel_widgets()
            
            act_panel = MyGroupBox()
            act_panel_layout = MyHBoxLayout()
            act_panel_layout.addWidget(self.model.prod_table_a_add_item_button)
            act_panel_layout.addWidget(self.model.prod_table_a_view_item_button)
            act_panel.setLayout(act_panel_layout)

            product = QTableWidgetItem(f"{row_v[1]}")
            brand = QTableWidgetItem(f"{row_v[4]}")
            sales_group = QTableWidgetItem(f"{row_v[5]}")
            price = QTableWidgetItem(f"{row_v[8]}")
            promo = QTableWidgetItem(f"{row_v[10]}")
            discount = QTableWidgetItem(f"{row_v[11]}")

            self.model.prod_table_a.setCellWidget(row_i, 0, act_panel)
            self.model.prod_table_a.setItem(row_i, 1, product)
            self.model.prod_table_a.setItem(row_i, 2, brand)
            self.model.prod_table_a.setItem(row_i, 3, sales_group)
            self.model.prod_table_a.setItem(row_i, 4, price)
            self.model.prod_table_a.setItem(row_i, 5, promo)
            self.model.prod_table_a.setItem(row_i, 6, discount)

            self.set_prod_tab_table_a_act_panel_connections(row_v)
            pass
        pass
    def populate_prod_tab_table_b(self, text_filter='', order_type='Retail', page_number=1):
        self.model.prod_table_b.setRowCount(len(self.model.prod_table_b_data))

        for row_i, row_v in enumerate(self.model.prod_table_b_data):
            self.model.set_prod_tab_table_act_panel_widgets()
            
            act_panel = MyGroupBox()
            act_panel_layout = MyHBoxLayout()
            act_panel_layout.addWidget(self.model.prod_table_b_add_item_button)
            act_panel_layout.addWidget(self.model.prod_table_b_view_item_button)
            act_panel.setLayout(act_panel_layout)

            product = QTableWidgetItem(f"{row_v[1]}")
            brand = QTableWidgetItem(f"{row_v[4]}")
            sales_group = QTableWidgetItem(f"{row_v[5]}")
            price = QTableWidgetItem(f"{row_v[8]}")
            promo = QTableWidgetItem(f"{row_v[10]}")
            discount = QTableWidgetItem(f"{row_v[11]}")

            self.model.prod_table_b.setCellWidget(row_i, 0, act_panel)
            self.model.prod_table_b.setItem(row_i, 1, product)
            self.model.prod_table_b.setItem(row_i, 2, brand)
            self.model.prod_table_b.setItem(row_i, 3, sales_group)
            self.model.prod_table_b.setItem(row_i, 4, price)
            self.model.prod_table_b.setItem(row_i, 5, promo)
            self.model.prod_table_b.setItem(row_i, 6, discount)
            pass
        # for row_i, row_v in enumerate(self.model.prod_table_b_data):
        #     pass


        pass
    def populate_act_panel_fields(self):
        self.model.cust_sel_field.clear()
        self.model.order_type_sel_field.clear()

        self.model.cust_sel_field.addItem('New order')
        for _, row_v in enumerate(self.model.cust_data):
            self.model.cust_sel_field.addItem(row_v[0])

        self.model.order_type_sel_field.addItem('Retail')
        self.model.order_type_sel_field.addItem('Wholesale')
        pass
    def populate_cust_order_tab_panel(self):
        self.model.set_cust_order_tab_widgets()

        cust_order_panel = MyGroupBox()
        cust_order_layout = MyVBoxLayout()

        cust_order_act_panel_a = MyGroupBox()
        cust_order_act_panel_a_layout = MyHBoxLayout()
        cust_order_act_panel_a_layout.addWidget(self.model.order_type_label)
        cust_order_act_panel_a_layout.addWidget(self.model.clr_order_button)
        cust_order_act_panel_a.setLayout(cust_order_act_panel_a_layout)

        cust_order_act_panel_b = MyGroupBox()
        cust_order_act_panel_b_layout = MyFormLayout()
        cust_order_act_panel_b_layout.addRow('Sub total:', self.model.order_sub_total_label)
        cust_order_act_panel_b_layout.addRow('Discount:', self.model.order_discount_label)
        cust_order_act_panel_b_layout.addRow('Tax:', self.model.order_tax_label)
        cust_order_act_panel_b_layout.addRow('Total:', self.model.order_total_label)
        cust_order_act_panel_b.setLayout(cust_order_act_panel_b_layout)

        cust_order_act_panel_c = MyGroupBox()
        cust_order_act_panel_c_layout = MyHBoxLayout()
        cust_order_act_panel_c_layout.addWidget(self.model.discard_order_button)
        cust_order_act_panel_c_layout.addWidget(self.model.lock_order_untoggle_button)
        cust_order_act_panel_c_layout.addWidget(self.model.lock_order_toggle_button)
        cust_order_act_panel_c_layout.addWidget(self.model.save_order_button)
        cust_order_act_panel_c.setLayout(cust_order_act_panel_c_layout)

        cust_order_act_panel_d = MyGroupBox()
        cust_order_act_panel_d_layout = MyHBoxLayout()
        cust_order_act_panel_d_layout.addWidget(self.model.order_pay_button)
        cust_order_act_panel_d.setLayout(cust_order_act_panel_d_layout)

        cust_order_layout.addWidget(cust_order_act_panel_a)
        cust_order_layout.addWidget(self.model.cust_order_table)
        cust_order_layout.addWidget(cust_order_act_panel_b)
        cust_order_layout.addWidget(cust_order_act_panel_c)
        cust_order_layout.addWidget(cust_order_act_panel_d)
        cust_order_panel.setLayout(cust_order_layout)


        self.model.append_cust_order_tab_data(
            self.model.cust_name_value,
            self.model.order_type_value,
            self.model.order_type_label,
            self.model.clr_order_button,
            self.model.cust_order_table,
            self.model.order_sub_total_value,
            self.model.order_discount_value,
            self.model.order_tax_value,
            self.model.order_total_value,
            self.model.order_sub_total_label,
            self.model.order_discount_label,
            self.model.order_tax_label,
            self.model.order_total_label,
            self.model.discard_order_button,
            self.model.lock_order_toggle_button,
            self.model.lock_order_untoggle_button,
            self.model.save_order_button,
            self.model.order_pay_button
        )

        new_i = self.model.cust_order_tab.addTab(cust_order_panel, self.model.cust_sel_field.currentText())

        self.model.clr_order_button.clicked.connect(self.on_clr_order_button_clicked)

        return new_i
        pass
    # endregion > populate

    # region > actions
    def on_prod_table_a_pag_button_clicked(self, action):
        i = self.model.cust_order_tab.currentIndex()
        
        print('do this func:', action)
        if action == 'prev':
            if self.model.current_page > 1:
                self.model.current_page -= 1
                self.model.prod_table_a_pag_page_label.setText(f"{self.model.current_page}/{self.model.total_page}")

            self.populate_prod_tab_table_a(text_filter=self.model.text_filter_field.text(), order_type=self.model.order_type_values[i], page_number=self.model.current_page)
            pass
        elif action == 'next':
            self.model.current_page += 1
            self.model.prod_table_a_pag_page_label.setText(f"{self.model.current_page}/{self.model.total_page}")
            
            self.populate_prod_tab_table_a(text_filter=self.model.text_filter_field.text(), order_type=self.model.order_type_values[i], page_number=self.model.current_page)
            pass

    def on_prod_table_a_view_item_button_clicked(self, row_v):
        pass

    def on_add_cust_order_button_clicked(self):
        self.populate_prod_tab_table_a()
        new_i = self.populate_cust_order_tab_panel()
        self.model.cust_order_tab.setCurrentIndex(new_i)
        self.set_cust_order_act_panel_connections()
        self.model.pending_order_count_label.setText(f"Pending order count: {self.model.cust_order_tab.count()}")
        pass
    
    def on_cust_order_tab_current_changed(self):
        i = self.model.cust_order_tab.currentIndex()
        
        self.populate_prod_tab_table_a(text_filter='', order_type=self.model.order_type_values[i], page_number=1)       
        
        print('---', self.model.cust_name_values)
        print('---', self.model.order_type_values)
        print('---', self.model.order_type_labels)
        print('---', self.model.clr_order_buttons)
        print('---', self.model.cust_order_tables)
        print('---', self.model.order_sub_total_values)
        print('---', self.model.order_discount_values)
        print('---', self.model.order_tax_values)
        print('---', self.model.order_total_values)
        print('---', self.model.order_sub_total_labels)
        print('---', self.model.order_discount_labels)
        print('---', self.model.order_tax_labels)
        print('---', self.model.order_total_labels)
        print('---', self.model.discard_order_buttons)
        print('---', self.model.lock_order_toggle_buttons)
        print('---', self.model.lock_order_untoggle_buttons)
        print('---', self.model.save_order_buttons)
        print('---', self.model.order_pay_buttons)

    # TODO: CUST TAB POPULATION !!!!!!!!!!!!!!!!!!!!!!!!!!!
    # IDEA: cust tab functions   
    def on_prod_table_a_add_item_button_clicked(self, row_v):
        i = self.model.cust_order_tab.currentIndex()

        selected_item = f"<b>{row_v[1]}</b>"
        proposed_quantity, confirm = QInputDialog.getText(self.view, 'Add', f"{selected_item}<br>Set quantity:")
        
        if confirm == True:
            cust_order_item_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name

            if cust_order_item_list:
                for item in cust_order_item_list:
                    row_i = item.row()  # Get the row of the item
                    current_quantity = int(self.model.cust_order_tables[i].item(row_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                    current_price = float(self.model.cust_order_tables[i].item(row_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                    current_discount = float(self.model.cust_order_tables[i].item(row_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                    self.model.new_quantity = current_quantity + int(proposed_quantity)
                    self.model.new_price = current_price + (float(row_v[8]) * int(proposed_quantity))
                    self.model.new_discount = current_discount + (float(row_v[11]) * int(proposed_quantity))

                    quantity = QTableWidgetItem(f'{self.model.new_quantity}x')  # Create a new 
                    price = QTableWidgetItem(f'₱{self.model.new_price:.2f}')  # Create a new 
                    discount = QTableWidgetItem(f'₱{self.model.new_discount:.2f}')  # Create a new 

                    self.model.cust_order_tables[i].setItem(row_i, 1, quantity)
                    self.model.cust_order_tables[i].setItem(row_i, 3, price)
                    self.model.cust_order_tables[i].setItem(row_i, 4, discount)
            else:
                self.model.set_cust_order_table_act_panel_widgets()

                row_i = self.model.cust_order_tables[i].rowCount()

                self.model.cust_order_tables[i].insertRow(row_i)
                
                self.model.new_quantity = proposed_quantity
                self.model.new_price = float(row_v[8]) * int(proposed_quantity)
                self.model.new_discount = float(row_v[11]) * int(proposed_quantity)

                action_panel = MyGroupBox()
                action_panel_layout = MyHBoxLayout()
                action_panel_layout.addWidget(self.model.drop_all_quantity_button)
                action_panel_layout.addWidget(self.model.drop_quantity_button)
                action_panel_layout.addWidget(self.model.add_quantity_button)
                action_panel_layout.addWidget(self.model.edit_quantity_button)
                action_panel.setLayout(action_panel_layout)

                quantity = QTableWidgetItem(f'{self.model.new_quantity}x')  # Create a new 
                item_name = QTableWidgetItem(str(row_v[1]))
                price = QTableWidgetItem(f'₱{self.model.new_price:.2f}')
                discount = QTableWidgetItem(f'₱{self.model.new_discount:.2f}')
      
                self.model.cust_order_tables[i].setCellWidget(row_i, 0, action_panel)
                self.model.cust_order_tables[i].setItem(row_i, 1, quantity)
                self.model.cust_order_tables[i].setItem(row_i, 2, item_name)
                self.model.cust_order_tables[i].setItem(row_i, 3, price)
                self.model.cust_order_tables[i].setItem(row_i, 4, discount)

                self.set_cust_order_table_act_panel_connections(row_v)

            self.model.order_sub_total_values[i] += (float(row_v[8]) * int(proposed_quantity))
            self.model.order_discount_values[i] += (float(row_v[11]) * int(proposed_quantity))
            self.model.order_tax_values[i] += (0 * int(proposed_quantity))
            self.model.order_total_values[i] = (self.model.order_sub_total_values[i] - self.model.order_discount_values[i]) + self.model.order_tax_values[i]

            self.model.order_sub_total_labels[i].setText(f'₱{self.model.order_sub_total_values[i]:.2f}')
            self.model.order_discount_labels[i].setText(f'₱{self.model.order_discount_values[i]:.2f}')
            self.model.order_tax_labels[i].setText(f'₱{self.model.order_tax_values[i]:.2f}')
            self.model.order_total_labels[i].setText(f'₱{self.model.order_total_values[i]:.2f}')

            self.model.order_pay_buttons[i].setText(f'Pay ₱{self.model.order_total_values[i]:.2f}')

            pass
        self.new_quantity = 0
        self.new_price = 0
        pass
    def on_clr_order_button_clicked(self):
        i = self.model.cust_order_tab.currentIndex()

        self.model.cust_order_tables[i].setRowCount(0)

        self.model.order_sub_total_values[i] = 0
        self.model.order_discount_values[i] = 0
        self.model.order_tax_values[i] = 0
        self.model.order_total_values[i] = 0

        self.model.order_sub_total_labels[i].setText(f'₱{self.model.order_sub_total_values[i]:.2f}')
        self.model.order_discount_labels[i].setText(f'₱{self.model.order_discount_values[i]:.2f}')
        self.model.order_tax_labels[i].setText(f'₱{self.model.order_tax_values[i]:.2f}')
        self.model.order_total_labels[i].setText(f'₱{self.model.order_total_values[i]:.2f}')

        self.model.order_pay_buttons[i].setText(f'Pay ₱{self.model.order_total_values[i]:.2f}')
        print('clr_order')
        pass
    def on_drop_all_quantity_button_clicked(self, row_v):
        i = self.model.cust_order_tab.currentIndex()
        
        cust_order_item_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name

        if cust_order_item_list:
            for item in cust_order_item_list:
                row_i = item.row()  # Get the row of the item
                current_quantity = int(self.model.cust_order_tables[i].item(row_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                current_price = float(self.model.cust_order_tables[i].item(row_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                current_discount = float(self.model.cust_order_tables[i].item(row_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                self.model.new_quantity = current_quantity - current_quantity
                self.model.new_price = current_price - current_price
                self.model.new_discount = current_discount - current_discount

                quantity = QTableWidgetItem(f'{self.model.new_quantity}x')  # Create a new 
                price = QTableWidgetItem(f'₱{self.model.new_price:.2f}')  # Create a new 
                discount = QTableWidgetItem(f'₱{self.model.new_discount:.2f}')  # Create a new 

                self.model.cust_order_tables[i].setItem(row_i, 1, quantity)
                self.model.cust_order_tables[i].setItem(row_i, 3, price)
                self.model.cust_order_tables[i].setItem(row_i, 4, discount)

                self.model.cust_order_tables[i].removeRow(row_i)

                self.model.order_sub_total_values[i] = max(0, self.model.order_sub_total_values[i] - current_price)
                self.model.order_discount_values[i] = max(0, self.model.order_discount_values[i] - current_discount)
                self.model.order_tax_values[i] = max(0, self.model.order_tax_values[i] - 0)
                self.model.order_total_values[i] = max(0, (self.model.order_sub_total_values[i] - self.model.order_discount_values[i]) - self.model.order_tax_values[i])

        self.model.order_sub_total_labels[i].setText(f'₱{self.model.order_sub_total_values[i]:.2f}')
        self.model.order_discount_labels[i].setText(f'₱{self.model.order_discount_values[i]:.2f}')
        self.model.order_tax_labels[i].setText(f'₱{self.model.order_tax_values[i]:.2f}')
        self.model.order_total_labels[i].setText(f'₱{self.model.order_total_values[i]:.2f}')

        self.model.order_pay_buttons[i].setText(f'Pay ₱{self.model.order_total_values[i]:.2f}')


        self.new_quantity = 0
        self.new_price = 0
        print('drop_all_quantity')
        pass
    def on_drop_quantity_button_clicked(self, row_v):
        i = self.model.cust_order_tab.currentIndex()
        print('PASS A!!!!')

        cust_order_item_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name
        
        if cust_order_item_list: # if item already exist in table, update row of item
            for item in cust_order_item_list:
                row_i = item.row()  # Get the row of the item
                current_quantity = int(self.model.cust_order_tables[i].item(row_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                current_price = float(self.model.cust_order_tables[i].item(row_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                current_discount = float(self.model.cust_order_tables[i].item(row_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                if current_quantity > 1:
                    self.model.new_quantity = current_quantity - 1
                    self.model.new_price = current_price - float(row_v[8])
                    self.model.new_discount = current_discount - float(row_v[11])

                    quantity = QTableWidgetItem(f'{self.model.new_quantity}x')  # Create a new 
                    price = QTableWidgetItem(f'₱{self.model.new_price:.2f}')  # Create a new 
                    discount = QTableWidgetItem(f'₱{self.model.new_discount:.2f}')  # Create a new 

                    self.model.cust_order_tables[i].setItem(row_i, 1, quantity)
                    self.model.cust_order_tables[i].setItem(row_i, 3, price)
                    self.model.cust_order_tables[i].setItem(row_i, 4, discount)
                    pass
                else:
                    self.model.cust_order_tables[i].removeRow(row_i)
                pass

        self.model.order_sub_total_values[i] = max(0, self.model.order_sub_total_values[i] - float(row_v[8]))
        self.model.order_discount_values[i] = max(0, self.model.order_discount_values[i] - float(row_v[11]))
        self.model.order_tax_values[i] = max(0, self.model.order_tax_values[i])
        self.model.order_total_values[i] = max(0, (self.model.order_sub_total_values[i] - self.model.order_discount_values[i]) - self.model.order_tax_values[i])

        self.model.order_sub_total_labels[i].setText(f'₱{self.model.order_sub_total_values[i]:.2f}')
        self.model.order_discount_labels[i].setText(f'₱{self.model.order_discount_values[i]:.2f}')
        self.model.order_tax_labels[i].setText(f'₱{self.model.order_tax_values[i]:.2f}')
        self.model.order_total_labels[i].setText(f'₱{self.model.order_total_values[i]:.2f}')

        self.model.order_pay_buttons[i].setText(f'Pay ₱{self.model.order_total_values[i]:.2f}')

        self.new_quantity = 0
        self.new_price = 0
        print('drop_quantity')
        pass
    def on_add_quantity_button_clicked(self, row_v):
        i = self.model.cust_order_tab.currentIndex()
        print('PASS A!!!!')

        cust_order_item_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name
        
        if cust_order_item_list: # if item already exist in table, update row of item
            for item in cust_order_item_list:
                row_i = item.row()  # Get the row of the item
                current_quantity = int(self.model.cust_order_tables[i].item(row_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                current_price = float(self.model.cust_order_tables[i].item(row_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                current_discount = float(self.model.cust_order_tables[i].item(row_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                self.model.new_quantity = current_quantity + 1
                self.model.new_price = current_price + float(row_v[8])
                self.model.new_discount = current_discount + float(row_v[11])

                quantity = QTableWidgetItem(f'{self.model.new_quantity}x')  # Create a new 
                price = QTableWidgetItem(f'₱{self.model.new_price:.2f}')  # Create a new 
                discount = QTableWidgetItem(f'₱{self.model.new_discount:.2f}')  # Create a new 

                self.model.cust_order_tables[i].setItem(row_i, 1, quantity)
                self.model.cust_order_tables[i].setItem(row_i, 3, price)
                self.model.cust_order_tables[i].setItem(row_i, 4, discount)
                pass

        self.model.order_sub_total_values[i] += (float(row_v[8]) * 1)
        self.model.order_discount_values[i] += (float(row_v[11]) * 1)
        self.model.order_tax_values[i] += (0 * 1)
        self.model.order_total_values[i] = (self.model.order_sub_total_values[i] - self.model.order_discount_values[i]) + self.model.order_tax_values[i]

        self.model.order_sub_total_labels[i].setText(f'₱{self.model.order_sub_total_values[i]:.2f}')
        self.model.order_discount_labels[i].setText(f'₱{self.model.order_discount_values[i]:.2f}')
        self.model.order_tax_labels[i].setText(f'₱{self.model.order_tax_values[i]:.2f}')
        self.model.order_total_labels[i].setText(f'₱{self.model.order_total_values[i]:.2f}')

        self.model.order_pay_buttons[i].setText(f'Pay ₱{self.model.order_total_values[i]:.2f}')

        self.new_quantity = 0
        self.new_price = 0
        print('add_quantity')
        pass
    def on_edit_quantity_button_clicked(self, row_v):
        i = self.model.cust_order_tab.currentIndex()

        selected_item = f"<b>{row_v[1]}</b>"
        proposed_quantity, confirm = QInputDialog.getText(self.view, 'Edit', f"{selected_item}<br>Set quantity:")
        
        if confirm == True:
            if int(proposed_quantity) > 0:
                cust_order_item_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name

                if cust_order_item_list:
                    for item in cust_order_item_list:
                        row_i = item.row()  # Get the row of the item

                        self.model.new_quantity = int(proposed_quantity)
                        self.model.new_price = float(row_v[8]) * int(proposed_quantity)
                        self.model.new_discount = float(row_v[11]) * int(proposed_quantity)

                        quantity = QTableWidgetItem(f'{self.model.new_quantity}x')  # Create a new 
                        price = QTableWidgetItem(f'₱{self.model.new_price:.2f}')  # Create a new 
                        discount = QTableWidgetItem(f'₱{self.model.new_discount:.2f}')  # Create a new 

                        self.model.cust_order_tables[i].setItem(row_i, 1, quantity)
                        self.model.cust_order_tables[i].setItem(row_i, 3, price)
                        self.model.cust_order_tables[i].setItem(row_i, 4, discount)

                self.model.order_sub_total_values[i] = float(row_v[8]) * int(proposed_quantity)
                self.model.order_discount_values[i] = float(row_v[11]) * int(proposed_quantity)
                self.model.order_tax_values[i] = 0
                self.model.order_total_values[i] = (self.model.order_sub_total_values[i] - self.model.order_discount_values[i]) + self.model.order_tax_values[i]

                self.model.order_sub_total_labels[i].setText(f'₱{self.model.order_sub_total_values[i]:.2f}')
                self.model.order_discount_labels[i].setText(f'₱{self.model.order_discount_values[i]:.2f}')
                self.model.order_tax_labels[i].setText(f'₱{self.model.order_tax_values[i]:.2f}')
                self.model.order_total_labels[i].setText(f'₱{self.model.order_total_values[i]:.2f}')

                self.model.order_pay_buttons[i].setText(f'Pay ₱{self.model.order_total_values[i]:.2f}')

                pass
            else:
                QMessageBox.critical(self.view, 'Error', 'Must be greater than 0.', QMessageBox.StandardButton.Ok)
                pass
        else:
            pass
        self.new_quantity = 0
        self.new_price = 0
        print('edit_quantity')
        pass
        
    def on_discard_order_button_clicked(self):
        i = self.model.cust_order_tab.currentIndex()
        self.model.cust_order_tab.removeTab(i)

        self.model.remove_cust_order_tab_data(i)

        self.model.pending_order_count_label.setText(f"Pending order count: {self.model.cust_order_tab.count()}")
        pass
    def on_lock_order_toggle_button_clicked(self):
        i = self.model.cust_order_tab.currentIndex()     
        pass
    def on_lock_order_untoggle_button_clicked(self):
        i = self.model.cust_order_tab.currentIndex()     
        pass
    def on_save_order_button_clicked(self):
        i = self.model.cust_order_tab.currentIndex()     
        pass
    def on_order_pay_button_clicked(self):
        i = self.model.cust_order_tab.currentIndex()

        for row in range(self.model.cust_order_tables[i].rowCount()):
            item_row_data = []

            for col in range(self.model.cust_order_tables[i].columnCount()):
                item = self.model.cust_order_tables[i].item(row, col)
                if item is not None:
                    item_row_data.append(item.text().replace('x', '').replace('₱', ''))

            self.model.append_cust_order_list_data(item_row_data)
        print('data:', self.model.cust_order_list_data)

        self.view.show_panel_d()
        self.set_numpad_button_connections()
        self.set_payment_type_panel_connections()
        self.view.panel_d.exec()
        if self.view.panel_d.isVisible() == False:
            self.model.remove_cust_order_list_data(i)
            print('data:', self.model.cust_order_list_data)

    def on_numpad_buttons_clicked(self, value):
        current_text = self.model.amount_tendered_field.text()
        updated_text = current_text + value
        self.model.amount_tendered_field.setText(updated_text)

    def on_pay_cash_button_clicked(self):
        self.view.show_print_sel_dialog()
        self.set_confirm_act_panel_connections()
        self.view.sel_option_dialog.exec()

        pass
    def on_pay_points_button_clicked(self):
        # TODO: implement pay points ui
        pass

    def on_print_invoice_button_clicked(self):
        self.view.sel_option_dialog.close()
        self.view.show_invoice_form_dialog()
        self.set_invoice_act_panel_connections()

        self.view.invoice_form_dialog.exec()
        pass

    # IDEA: final task
    def on_print_button_clicked(self, action):
        i = self.model.cust_order_tab.currentIndex()

        self.model.set_cust_order_act_panel_widgets()
        self.populate_act_panel_fields()
        
        self.set_add_new_cust_order_act_panel_connections()

        self.view.panel_d.close()

        print('action:', action)
        if action == 'do_print_receipt':
            pass
        if action == 'do_print_invoice':
            self.view.invoice_form_dialog.close()

            invoice_customer_name = self.model.invoice_customer_name.text()
            invoice_company = self.model.invoice_company.text()
            invoice_phone = self.model.invoice_phone.text()

            print('invoice_customer_name:', invoice_customer_name)
            print('invoice_company:', invoice_company)
            print('invoice_phone:', invoice_phone)
            pass

        self.model.cust_order_tab.removeTab(i)
        self.view.sel_option_dialog.close()

        self.view.show_panel_e()

        self.model.remove_cust_order_tab_data(i)
        self.model.pending_order_count_label.setText(f"Pending order count: {self.model.cust_order_tab.count()}")
        
        self.view.panel_e.exec()

    def on_add_new_cust_order_button_clicked(self):
        self.view.panel_e.close()
        self.on_add_cust_order_button_clicked()
        pass
    # endregion > actions

if __name__ == ('__main__'):
    app = QApplication(sys.argv)

    schema = SalesSchema()

    model = MySalesModel(schema)
    view = MySalesView(model)
    controller = MySalesController(model, view)

    view.show()
    sys.exit(app.exec())
