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

        self.prod_table_a_data = schema.list_product()
        self.prod_table_b_data = schema.list_product_via_promo()

        self.text_filter_field = MyLineEdit()
        self.text_filter_button = MyPushButton(text='Filter')

        self.barcode_scan_field = MyLineEdit()
        self.barcode_scan_toggle_button = MyPushButton(text='AATC Off')
        self.barcode_scan_untoggle_button = MyPushButton(text='AATC On')

        self.prod_table_a = MyTableWidget(object_name='prod_table_a')
        self.prod_table_b = MyTableWidget(object_name='prod_table_b')

        self.prod_table_a_pag_next_button = MyPushButton(text='Next')
        self.prod_table_a_pag_page_label = MyLabel(text=f"99/99")
        self.prod_table_a_pag_prev_button = MyPushButton(text='Prev')
        self.prod_table_b_pag_next_button = MyPushButton(text='Next')
        self.prod_table_b_pag_page_label = MyLabel(text=f"99/99")
        self.prod_table_b_pag_prev_button = MyPushButton(text='Prev')

        self.curr_user_label = MyLabel(text=f"Current user:")
        self.pending_order_count_label = MyLabel(text=f"Pending order:")
        self.available_prod_count_label = MyLabel(text=f"Available product:")

        self.cust_order_tab = MyTabWidget()

        # region > cust_order_tab
        self.order_type_labels = []
        self.clr_order_buttons = []

        self.cust_order_tables = []

        # self.drop_all_item_button = MyPushButton(text='Drop all')
        # self.drop_item_button = MyPushButton(text='Drop')
        # self.add_item_button = MyPushButton(text='Add')
        # self.edit_item_button = MyPushButton(text='Edit')

        self.order_sub_total_labels = []
        self.order_discount_labels = []
        self.order_tax_labels = []
        self.order_total_labels = []

        self.discard_order_buttons = []
        self.lock_order_toggle_buttons = []
        self.lock_order_untoggle_buttons = []
        self.save_order_buttons = []

        self.pay_order_buttons = []
        # endregion > cust_order_tab

    def set_prod_tab_table_act_panel_widgets(self):
        self.prod_table_a_add_item_button = MyPushButton(text='Add')
        self.prod_table_a_view_item_button = MyPushButton(text='View')
        self.prod_table_b_add_item_button = MyPushButton(text='Add')
        self.prod_table_b_view_item_button = MyPushButton(text='View')

    def set_cust_order_act_panel_widgets(self):
        self.cust_sel_field = MyComboBox()
        self.order_type_sel_field = MyComboBox()
        self.add_cust_order_button = MyPushButton(text='Add')
        self.load_cust_order_button = MyPushButton(text='Load')

    def set_cust_order_tab_widgets(self):
        self.order_type_label = MyLabel(text=f"Order type:")
        self.clr_order_button = MyPushButton(text='Clear')
        self.cust_order_table = MyTableWidget(object_name='cust_order_table')
        self.order_sub_total_label = MyLabel(text=f"999")
        self.order_discount_label = MyLabel(text=f"999")
        self.order_tax_label = MyLabel(text=f"999")
        self.order_total_label = MyLabel(text=f"999")
        self.discard_order_button = MyPushButton(text='Discard')
        self.lock_order_toggle_button = MyPushButton(text='Lock')
        self.lock_order_untoggle_button = MyPushButton(text='Unlock')
        self.save_order_button = MyPushButton(text='Save')
        self.pay_order_button = MyPushButton(text=f"Pay")
        pass
    def append_cust_order_tab_data(
        self,
        order_type_label,
        clr_order_button,
        cust_order_table,
        order_sub_total_label,
        order_discount_label,
        order_tax_label,
        order_total_label,
        discard_order_button,
        lock_order_toggle_button,
        lock_order_untoggle_button,
        save_order_button,
        pay_order_button
    ):
        self.order_type_labels.append(order_type_label)
        self.clr_order_buttons.append(clr_order_button)
        self.cust_order_tables.append(cust_order_table)
        self.order_sub_total_labels.append(order_sub_total_label)
        self.order_discount_labels.append(order_discount_label)
        self.order_tax_labels.append(order_tax_label)
        self.order_total_labels.append(order_total_label)
        self.discard_order_buttons.append(discard_order_button)
        self.lock_order_toggle_buttons.append(lock_order_toggle_button)
        self.lock_order_untoggle_buttons.append(lock_order_untoggle_button)
        self.save_order_buttons.append(save_order_button)
        self.pay_order_buttons.append(pay_order_button)

    def set_print_sel_panel_widgets(self):
        self.print_receipt_button = MyPushButton(text='Receipt')
        self.print_invoice_button = MyPushButton(text='Invoice')

    def set_invoice_form_dialog_widgets(self):
        self.invoice_customer_name = MyLineEdit()
        self.invoice_company = MyLineEdit()
        self.invoice_phone = MyLineEdit()
        self.invoice_print_button = MyPushButton(text='Print')

    # TODO: last thing to do
    def set_panel_d_dialog_widgets(self):
        # IDEA: dialogs
        self.amount_tendered_field = MyLineEdit()
        self.numpad_toggle_button = MyPushButton(text='Numpad Off')
        self.numpad_untoggle_button = MyPushButton(text='Numpad On')
        self.numpad_buttons = [
            MyPushButton(text='9'),
            MyPushButton(text='8'),
            MyPushButton(text='7'),
            MyPushButton(text='6'),
            MyPushButton(text='5'),
            MyPushButton(text='4'),
            MyPushButton(text='3'),
            MyPushButton(text='2'),
            MyPushButton(text='1'),
            MyPushButton(text=''),
            MyPushButton(text='0'),
            MyPushButton(text='')

        ]
        
        self.pay_cash_button = MyPushButton(text='Cash')
        self.pay_points_button = MyPushButton(text='Points')

        self.cust_name_label = MyLabel(text=f"Customer Name")
        self.cust_phone_label = MyLabel(text=f"09123456789")
        self.cust_points_label = MyLabel(text=f"99")

        self.order_final_sub_total_label = MyLabel(text=f"999")
        self.order_final_discount_label = MyLabel(text=f"999")
        self.order_final_tax_label = MyLabel(text=f"999")
        self.order_final_total_label = MyLabel(text=f"999")

    def set_panel_e_dialog_widgets(self):
        self.order_change = MyLabel(f"0.00")

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

        # region > prod_tab_panel_a
        prod_tab_panel_a = MyGroupBox()
        prod_tab_panel_a_layout = MyVBoxLayout()
        
        pgtn_act_panel_a = MyGroupBox()
        pgtn_act_panel_a_layout = MyHBoxLayout()
        pgtn_act_panel_a_layout.addWidget(self.model.prod_table_a_pag_next_button)
        pgtn_act_panel_a_layout.addWidget(self.model.prod_table_a_pag_page_label)
        pgtn_act_panel_a_layout.addWidget(self.model.prod_table_a_pag_prev_button)
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
        pgtn_act_panel_b_layout.addWidget(self.model.prod_table_b_pag_next_button)
        pgtn_act_panel_b_layout.addWidget(self.model.prod_table_b_pag_page_label)
        pgtn_act_panel_b_layout.addWidget(self.model.prod_table_b_pag_prev_button)
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
    def show_cust_order_tab_panel(self):
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
        cust_order_act_panel_d_layout.addWidget(self.model.pay_order_button)
        cust_order_act_panel_d.setLayout(cust_order_act_panel_d_layout)

        cust_order_layout.addWidget(cust_order_act_panel_a)
        cust_order_layout.addWidget(self.model.cust_order_table)
        cust_order_layout.addWidget(cust_order_act_panel_b)
        cust_order_layout.addWidget(cust_order_act_panel_c)
        cust_order_layout.addWidget(cust_order_act_panel_d)
        cust_order_panel.setLayout(cust_order_layout)

        curr_index = self.model.cust_order_tab.addTab(cust_order_panel, 'Customer')

        self.model.append_cust_order_tab_data(
            self.model.order_type_label,
            self.model.clr_order_button,
            self.model.cust_order_table,
            self.model.discard_order_button,
            self.model.lock_order_toggle_button,
            self.model.lock_order_untoggle_button,
            self.model.save_order_button,
            self.model.order_sub_total_label,
            self.model.order_discount_label,
            self.model.order_tax_label,
            self.model.order_total_label,
            self.model.pay_order_button
        )

        return curr_index

    def show_panel_c(self):
        self.panel_c = MyGroupBox()
        panel_c_layout = MyHBoxLayout()
        panel_c_layout.addWidget(self.model.curr_user_label)
        panel_c_layout.addWidget(self.model.pending_order_count_label)
        panel_c_layout.addWidget(self.model.available_prod_count_label)
        self.panel_c.setLayout(panel_c_layout)

    # IDEA: dialogs
    def show_panel_d(self):
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
        self.on_add_cust_order_button_clicked()

        self.model.add_cust_order_button.clicked.connect(self.on_add_cust_order_button_clicked)

        self.model.cust_order_tab.currentChanged.connect(self.on_cust_order_tab_current_changed)


    def populate_prod_tab_table_a(self, text_filter='', txn_type='Retail', page_number=1):
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

            self.model.prod_table_a_add_item_button.clicked.connect(lambda _, row_v=row_v: self.on_prod_table_a_add_item_button_clicked(row_v))
            pass
    def populate_prod_tab_table_b(self, text_filter='', txn_type='Retail', page_number=1):
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

    def on_prod_table_a_view_item_button_clicked(self, row_v):
        pass

    def on_add_cust_order_button_clicked(self):
        curr_index = self.view.show_cust_order_tab_panel()
        self.model.cust_order_tab.setCurrentIndex(curr_index)
        self.model.discard_order_button.clicked.connect(self.on_discard_order_button_clicked)
        self.model.lock_order_toggle_button.clicked.connect(self.on_lock_order_toggle_button_clicked)
        self.model.lock_order_untoggle_button.clicked.connect(self.on_lock_order_untoggle_button_clicked)
        self.model.save_order_button.clicked.connect(self.on_save_order_button_clicked)
        self.model.pay_order_button.clicked.connect(self.on_pay_order_button_clicked)
        pass
    def on_cust_order_tab_current_changed(self):
        i = self.model.cust_order_table.currentIndex()     
    
    # TODO: CUST TAB POPULATION !!!!!!!!!!!!!!!!!!!!!!!!!!!
    def on_prod_table_a_add_item_button_clicked(self, row_v):
        print('row_v:', row_v)
        pass
    def on_discard_order_button_clicked(self):
        i = self.model.cust_order_tab.currentIndex()
        self.model.cust_order_tab.removeTab(i)
        pass
    def on_lock_order_toggle_button_clicked(self):
        i = self.model.cust_order_table.currentIndex()     
        pass
    def on_lock_order_untoggle_button_clicked(self):
        i = self.model.cust_order_table.currentIndex()     
        pass
    def on_save_order_button_clicked(self):
        i = self.model.cust_order_table.currentIndex()     
        pass
    def on_pay_order_button_clicked(self):
        self.view.show_panel_d()
        self.model.pay_cash_button.clicked.connect(self.on_pay_cash_button_clicked)
        self.model.pay_points_button.clicked.connect(self.on_pay_points_button_clicked)
        self.view.panel_d.exec()

    def on_pay_cash_button_clicked(self):
        self.view.show_print_sel_dialog()
        self.model.print_receipt_button.clicked.connect(lambda: self.on_print_button_clicked(action='do_print_receipt'))
        self.model.print_invoice_button.clicked.connect(self.on_print_invoice_button_clicked)
        self.view.sel_option_dialog.exec()

        pass
    def on_pay_points_button_clicked(self):
        # TODO: implement pay points ui
        pass

    def on_print_invoice_button_clicked(self):
        self.view.sel_option_dialog.close()
        self.view.show_invoice_form_dialog()
        self.model.invoice_print_button.clicked.connect(lambda: self.on_print_button_clicked(action='do_print_invoice'))
        self.view.invoice_form_dialog.exec()
        pass

    # IDEA: final task
    def on_print_button_clicked(self, action):
        i = self.model.cust_order_tab.currentIndex()

        self.model.set_cust_order_act_panel_widgets()

        self.view.panel_d.close()

        print('action:', action)
        if action == 'do_print_receipt':
            pass
        if action == 'do_print_invoice':
            self.view.invoice_form_dialog.close()
            pass

        self.model.cust_order_tab.removeTab(i)
        self.view.sel_option_dialog.close()

        self.view.show_panel_e()
        self.model.add_cust_order_button.clicked.connect(self.on_add_new_cust_order_button_clicked)
        self.view.panel_e.exec()

    def on_add_new_cust_order_button_clicked(self):
        self.view.panel_e.close()
        self.on_add_cust_order_button_clicked()
        pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)

    schema = SalesSchema()

    model = MySalesModel(schema)
    view = MySalesView(model)
    controller = MySalesController(model, view)

    view.show()
    sys.exit(app.exec())
