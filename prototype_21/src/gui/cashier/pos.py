# IDEA: THIS CODE IS IN PYQT6 MVC (MODEL, VIEW, CONTROLLER) FORMAT
# NOTE: FOR MODEL FORMATIING
# init_(purpose name)_entry
# assign_(purpose name)_entry
# setup_(widget type)

# NOTE: FOR VIEW FORMATTING
# setup_main_panel
# setup_panel_a
# setup_panel_b
# and so on...

# NOTE: FOR CONTROLLER FORMATTING
# on_(widget name)_(connection type)
# populate_(widget name or specific widget group)
# setup_(widget name)_conn
# set_label_required_field_indicator
# start_(purpose name)

import sqlite3
import sys, os
import pandas as pd
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.core.user.receipt_printer import ReceiptGenerator
from src.core.user.csv_to_db_importer import MyDataImportThread
from src.sql.cashier.pos import *
from src.widget.admin.admin import *
from templates.qss.qss_config import QSSConfig

schema = MyPOSSchema()
qss = QSSConfig()

class MyPOSModel: # NOTE: entries
    def __init__(self, name, phone):
        # NOTE: global variables
        self.gdrive_path = 'G:' + f"/My Drive/"
        self.user_name = name # IDEA: will be used for receipt
        self.user_phone = phone # IDEA: will be used for receipt

        self.init_pos_list_page_val()
        self.init_order_tab_val()
        self.init_sel_prod_val()
        self.init_order_tab_ctr()

        self.init_final_order_ctr()


    def init_order_clear_entry(self, i):
        self.init_order_tab_val()
        self.init_sel_prod_val()

        self.order_subtotal_val_ctr[i] = 0
        self.order_discount_val_ctr[i] = 0
        self.order_tax_val_ctr[i] = 0
        self.order_total_val_ctr[i] = 0

        self.init_order_summary_update(i)

    def init_pos_list_page_val(self):
        self.pos_page_number = 1
        self.pos_total_page_number = 1
        pass
    def setup_pos_list_panel(self):
        self.pos_list_table = MyTableWidget(object_name='pos_list_table')
        self.pos_list_prev_button = MyPushButton(text='Prev')
        self.pos_list_page_label = MyLabel(text=f"Page {self.pos_page_number}/{self.pos_total_page_number}")
        self.pos_list_next_button = MyPushButton(text='Next')
        self.pos_list_pag_box = MyGroupBox()
        self.pos_list_pag_layout = MyHBoxLayout(object_name='pos_list_pag_layout')
        self.pos_list_pag_layout.addWidget(self.pos_list_prev_button)
        self.pos_list_pag_layout.addWidget(self.pos_list_page_label)
        self.pos_list_pag_layout.addWidget(self.pos_list_next_button)
        self.pos_list_pag_box.setLayout(self.pos_list_pag_layout)
        self.pos_list_box = MyGroupBox()
        self.pos_list_layout = MyGridLayout()
        self.pos_list_layout.addWidget(self.pos_list_table,0,0)
        self.pos_list_layout.addWidget(self.pos_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.pos_list_box.setLayout(self.pos_list_layout)
    def init_sel_prod_val(self):
        self.sel_qty_val = 0
        self.sel_prod_name_val = ''
        self.sel_prod_price_val = 0
        self.sel_prod_discount_val = 0
        pass
    def init_order_tab_val(self):
        self.order_cust_name_value = ''
        self.order_cust_phone_value = '09-XXXXXXXXX'
        self.order_cust_points_value = 0
        self.order_order_type_value = ''

        self.order_subtotal_value = 0
        self.order_discount_value = 0
        self.order_tax_value = 0
        self.order_total_value = 0
        pass
    def init_order_tab_ctr(self):
        self.order_cust_name_value_ctr = []
        self.order_cust_phone_value_ctr = []
        self.order_cust_points_value_ctr = []
        self.order_order_type_value_ctr = []

        self.order_subtotal_val_ctr = []
        self.order_discount_val_ctr = []
        self.order_tax_val_ctr = []
        self.order_total_val_ctr = []

        self.order_type_label_ctr: List[MyPushButton] = []
        self.order_clear_button_ctr: List[MyPushButton] = []
        self.order_table_ctr: List[MyTableWidget] = []
        self.order_subtotal_label_ctr: List[MyLabel] = []
        self.order_discount_label_ctr: List[MyLabel] = []
        self.order_tax_label_ctr: List[MyLabel] = []
        self.order_total_label_ctr: List[MyLabel] = []
        self.order_discard_button_ctr: List[MyPushButton] = []
        self.order_lock_toggle_button_ctr: List[MyPushButton] = []
        self.order_save_button_ctr: List[MyPushButton] = []
        self.order_pay_button_ctr: List[MyPushButton] = []
        pass

    def setup_order_tab_panel(self, tab_name='Order'):
        self.order_type_label = MyLabel(text=f"Order type: {self.order_order_type_value}")
        self.order_clear_button = MyPushButton(text='Clear')
        self.order_act_a_box = MyGroupBox()
        self.order_act_a_layout = MyHBoxLayout()
        self.order_act_a_layout.addWidget(self.order_type_label)
        self.order_act_a_layout.addWidget(self.order_clear_button)
        self.order_act_a_box.setLayout(self.order_act_a_layout)

        self.order_table = MyTableWidget(object_name='order_table')

        self.order_subtotal_label = MyLabel(object_name='order_subtotal', text=f"{self.order_subtotal_value:.2f}")
        self.order_discount_label = MyLabel(object_name='order_discount', text=f"{self.order_discount_value:.2f}")
        self.order_tax_label = MyLabel(object_name='order_tax', text=f"{self.order_tax_value:.2f}")
        self.order_total_label = MyLabel(object_name='order_total', text=f"{self.order_total_value:.2f}")
        self.order_summary_box = MyGroupBox()
        self.order_summary_layout = MyFormLayout()
        self.order_summary_layout.addRow('Subtotal:', self.order_subtotal_label)
        self.order_summary_layout.addRow('Discount:', self.order_discount_label)
        self.order_summary_layout.addRow('Tax:', self.order_tax_label)
        self.order_summary_layout.addRow('Total:', self.order_total_label)
        self.order_summary_box.setLayout(self.order_summary_layout)

        self.order_discard_button = MyPushButton(text='Discard')
        self.order_lock_toggle_button = [
            MyPushButton(text='Lock'),
            MyPushButton(text='Unlock'),
        ]
        self.order_save_button = MyPushButton(text='Save')
        self.order_act_b_box = MyGroupBox()
        self.order_act_b_layout = MyHBoxLayout()        
        self.order_act_b_layout.addWidget(self.order_discard_button)        
        self.order_act_b_layout.addWidget(self.order_lock_toggle_button[0])        
        self.order_act_b_layout.addWidget(self.order_lock_toggle_button[1])        
        self.order_act_b_layout.addWidget(self.order_save_button)        
        self.order_act_b_box.setLayout(self.order_act_b_layout)

        self.order_pay_button = MyPushButton(text=f"Pay {self.order_total_value:.2f}")
        self.order_act_c_box = MyGroupBox()
        self.order_act_c_layout = MyHBoxLayout()
        self.order_act_c_layout.addWidget(self.order_pay_button)
        self.order_act_c_box.setLayout(self.order_act_c_layout)

        self.order_box = MyGroupBox()
        self.order_layout = MyGridLayout()
        self.order_layout.addWidget(self.order_act_a_box,0,0)
        self.order_layout.addWidget(self.order_table,1,0)
        self.order_layout.addWidget(self.order_summary_box,2,0)
        self.order_layout.addWidget(self.order_act_b_box,3,0,Qt.AlignmentFlag.AlignLeft)
        self.order_layout.addWidget(self.order_act_c_box,4,0)
        self.order_box.setLayout(self.order_layout)
        pass
    def append_order_tab_ctr(self):
        try:
            self.order_cust_name_value_ctr.append(self.order_cust_name_value)
            self.order_cust_phone_value_ctr.append(self.order_cust_phone_value)
            self.order_cust_points_value_ctr.append(self.order_cust_points_value)
            self.order_order_type_value_ctr.append(self.order_order_type_value)

            self.order_subtotal_val_ctr.append(self.order_subtotal_value)
            self.order_discount_val_ctr.append(self.order_discount_value)
            self.order_tax_val_ctr.append(self.order_tax_value)
            self.order_total_val_ctr.append(self.order_total_value)

            self.order_type_label_ctr.append(self.order_type_label)
            self.order_clear_button_ctr.append(self.order_clear_button)
            self.order_table_ctr.append(self.order_table)
            self.order_subtotal_label_ctr.append(self.order_subtotal_label)
            self.order_discount_label_ctr.append(self.order_discount_label)
            self.order_tax_label_ctr.append(self.order_tax_label)
            self.order_total_label_ctr.append(self.order_total_label)
            self.order_discard_button_ctr.append(self.order_discard_button)
            self.order_lock_toggle_button_ctr.append(self.order_lock_toggle_button)
            self.order_save_button_ctr.append(self.order_save_button)
            self.order_pay_button_ctr.append(self.order_pay_button)
            pass
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")
        pass  
    def remove_order_tab_ctr(self, i: int):
        try:
            self.order_cust_name_value_ctr.remove(self.order_cust_name_value_ctr[i])
            self.order_cust_phone_value_ctr.remove(self.order_cust_phone_value_ctr[i])
            self.order_cust_points_value_ctr.remove(self.order_cust_points_value_ctr[i])
            self.order_order_type_value_ctr.remove(self.order_order_type_value_ctr[i])

            self.order_subtotal_val_ctr.remove(self.order_subtotal_val_ctr[i])
            self.order_discount_val_ctr.remove(self.order_discount_val_ctr[i])
            self.order_tax_val_ctr.remove(self.order_tax_val_ctr[i])
            self.order_total_val_ctr.remove(self.order_total_val_ctr[i])

            self.order_type_label_ctr.remove(self.order_type_label_ctr[i])
            self.order_clear_button_ctr.remove(self.order_clear_button_ctr[i])
            self.order_table_ctr.remove(self.order_table_ctr[i])
            self.order_subtotal_label_ctr.remove(self.order_subtotal_label_ctr[i])
            self.order_discount_label_ctr.remove(self.order_discount_label_ctr[i])
            self.order_tax_label_ctr.remove(self.order_tax_label_ctr[i])
            self.order_total_label_ctr.remove(self.order_total_label_ctr[i])
            self.order_discard_button_ctr.remove(self.order_discard_button_ctr[i])
            self.order_lock_toggle_button_ctr.remove(self.order_lock_toggle_button_ctr[i])
            self.order_save_button_ctr.remove(self.order_save_button_ctr[i])
            self.order_pay_button_ctr.remove(self.order_pay_button_ctr[i])
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")

    # region > order_box
    def assign_cust_order_val_entry(self, i: int, value):
        sel_prod_name = str(value[1])
        sel_prod_price = float(value[3])
        sel_prod_discount = float(value[6]) if value[5] != 'No promo' else 0
        cust_order_prod_name = self.order_table_ctr[i].findItems(sel_prod_name, Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name

        return sel_prod_name,sel_prod_price,sel_prod_discount, cust_order_prod_name
        pass

    def init_add_prod_update_entry(self, i: int, cust_order_prod_name, sel_qty, sel_prod_price, sel_prod_discount):
        for row_v in cust_order_prod_name:
            row_i = row_v.row()

            current_qty = int(self.order_table_ctr[i].item(row_i, 1).text())
            current_price = float(self.order_table_ctr[i].item(row_i, 3).text())
            current_discount = float(self.order_table_ctr[i].item(row_i, 4).text())

            self.sel_qty_val = current_qty + sel_qty
            self.sel_prod_price_val = current_price + (sel_prod_price * sel_qty)
            self.sel_prod_discount_val = current_discount + (sel_prod_discount * sel_qty)
            
            self.order_table_ctr[i].item(row_i, 1).setText(f"{self.sel_qty_val}")
            self.order_table_ctr[i].item(row_i, 3).setText(f"{self.sel_prod_price_val:.2f}")
            self.order_table_ctr[i].item(row_i, 4).setText(f"{self.sel_prod_discount_val:.2f}")
        pass
    def init_add_prod_compute_entry(self, i: int, sel_qty, sel_prod_price, sel_prod_discount):
        self.order_subtotal_val_ctr[i] = max(0, self.order_subtotal_val_ctr[i] + (sel_prod_price * sel_qty))
        self.order_discount_val_ctr[i] = max(0, self.order_discount_val_ctr[i] + (sel_prod_discount * sel_qty))
        self.order_tax_val_ctr[i] = max(0, self.order_tax_val_ctr[i] + (0)) # NOTE: ALWAYS SET TO 0 FOR NOW
        self.order_total_val_ctr[i] = max(0, (self.order_subtotal_val_ctr[i] - self.order_discount_val_ctr[i]) + self.order_tax_val_ctr[i])

    def init_drop_all_qty_update_entry(self, i: int, cust_order_prod_name):
        for row_v in cust_order_prod_name:
            row_i = row_v.row()

            current_qty = int(self.order_table_ctr[i].item(row_i, 1).text())
            current_price = float(self.order_table_ctr[i].item(row_i, 3).text())
            current_discount = float(self.order_table_ctr[i].item(row_i, 4).text())

            self.sel_qty_val = current_qty - current_qty
            self.sel_prod_price_val = current_price - current_price
            self.sel_prod_discount_val = current_discount - current_discount
                        
            self.order_table_ctr[i].item(row_i, 1).setText(f"{self.sel_qty_val}")
            self.order_table_ctr[i].item(row_i, 3).setText(f"{self.sel_prod_price_val:.2f}")
            self.order_table_ctr[i].item(row_i, 4).setText(f"{self.sel_prod_discount_val:.2f}")

            self.init_drop_all_qty_compute_entry(i, current_price, current_discount)

            self.order_table_ctr[i].removeRow(row_i)
        pass
    def init_drop_all_qty_compute_entry(self, i: int, current_price, current_discount):
        self.order_subtotal_val_ctr[i] = max(0, self.order_subtotal_val_ctr[i] - current_price)
        self.order_discount_val_ctr[i] = max(0, self.order_discount_val_ctr[i] - current_discount)
        self.order_tax_val_ctr[i] = max(0, self.order_tax_val_ctr[i] - (0)) # NOTE: ALWAYS SET TO 0 FOR NOW
        self.order_total_val_ctr[i] = max(0, (self.order_subtotal_val_ctr[i] - self.order_discount_val_ctr[i]) - self.order_tax_val_ctr[i])

    def init_drop_qty_update_entry(self, i: int, cust_order_prod_name, sel_prod_price, sel_prod_discount):
        for row_v in cust_order_prod_name:
            row_i = row_v.row()

            current_qty = int(self.order_table_ctr[i].item(row_i, 1).text())
            current_price = float(self.order_table_ctr[i].item(row_i, 3).text())
            current_discount = float(self.order_table_ctr[i].item(row_i, 4).text())

            if current_qty > 1:
                self.sel_qty_val = current_qty - 1
                self.sel_prod_price_val = current_price - sel_prod_price
                self.sel_prod_discount_val = current_discount - sel_prod_discount
                
                self.order_table_ctr[i].item(row_i, 1).setText(f"{self.sel_qty_val}")
                self.order_table_ctr[i].item(row_i, 3).setText(f"{self.sel_prod_price_val:.2f}")
                self.order_table_ctr[i].item(row_i, 4).setText(f"{self.sel_prod_discount_val:.2f}")
                pass
            else:
                self.order_table_ctr[i].removeRow(row_i)

            self.init_drop_qty_compute_entry(i, sel_prod_price, sel_prod_discount)
        pass
    def init_drop_qty_compute_entry(self, i: int, sel_prod_price, sel_prod_discount):
        self.order_subtotal_val_ctr[i] = max(0, self.order_subtotal_val_ctr[i] - sel_prod_price)
        self.order_discount_val_ctr[i] = max(0, self.order_discount_val_ctr[i] - sel_prod_discount)
        self.order_tax_val_ctr[i] = max(0, self.order_tax_val_ctr[i] + (0)) # NOTE: ALWAYS SET TO 0 FOR NOW
        self.order_total_val_ctr[i] = max(0, (self.order_subtotal_val_ctr[i] - self.order_discount_val_ctr[i]) + self.order_tax_val_ctr[i])

    def init_add_qty_update_entry(self, i: int, cust_order_prod_name, sel_prod_price, sel_prod_discount):
        for row_v in cust_order_prod_name:
            row_i = row_v.row()

            current_qty = int(self.order_table_ctr[i].item(row_i, 1).text())
            current_price = float(self.order_table_ctr[i].item(row_i, 3).text())
            current_discount = float(self.order_table_ctr[i].item(row_i, 4).text())

            self.sel_qty_val = current_qty + 1
            self.sel_prod_price_val = current_price + sel_prod_price
            self.sel_prod_discount_val = current_discount + sel_prod_discount
            
            self.order_table_ctr[i].item(row_i, 1).setText(f"{self.sel_qty_val}")
            self.order_table_ctr[i].item(row_i, 3).setText(f"{self.sel_prod_price_val:.2f}")
            self.order_table_ctr[i].item(row_i, 4).setText(f"{self.sel_prod_discount_val:.2f}")

            self.init_add_qty_compute_entry(i, sel_prod_price, sel_prod_discount)
        pass
    def init_add_qty_compute_entry(self, i: int, sel_prod_price, sel_prod_discount):
        self.order_subtotal_val_ctr[i] = max(0, self.order_subtotal_val_ctr[i] + sel_prod_price)
        self.order_discount_val_ctr[i] = max(0, self.order_discount_val_ctr[i] + sel_prod_discount)
        self.order_tax_val_ctr[i] = max(0, self.order_tax_val_ctr[i] + (0)) # NOTE: ALWAYS SET TO 0 FOR NOW
        self.order_total_val_ctr[i] = max(0, (self.order_subtotal_val_ctr[i] - self.order_discount_val_ctr[i]) + self.order_tax_val_ctr[i])

    def init_edit_qty_update_entry(self, i: int, cust_order_prod_name, sel_qty, sel_prod_price, sel_prod_discount):
        for row_v in cust_order_prod_name:
            row_i = row_v.row()

            self.sel_qty_val = sel_qty
            self.sel_prod_price_val = sel_prod_price
            self.sel_prod_discount_val = sel_prod_discount
            
            self.order_table_ctr[i].item(row_i, 1).setText(f"{self.sel_qty_val}")
            self.order_table_ctr[i].item(row_i, 3).setText(f"{self.sel_prod_price_val:.2f}")
            self.order_table_ctr[i].item(row_i, 4).setText(f"{self.sel_prod_discount_val:.2f}")

            self.init_edit_qty_compute_entry(i, sel_qty, sel_prod_price, sel_prod_discount)
        pass
    def init_edit_qty_compute_entry(self, i: int, sel_qty, sel_prod_price, sel_prod_discount):
        self.order_subtotal_val_ctr[i] = sel_prod_price * sel_qty
        self.order_discount_val_ctr[i] = sel_prod_discount * sel_qty
        self.order_tax_val_ctr[i] = 0 # NOTE: ALWAYS SET TO 0 FOR NOW
        self.order_total_val_ctr[i] = max(0, (self.order_subtotal_val_ctr[i] - self.order_discount_val_ctr[i]) + self.order_tax_val_ctr[i])

    def init_order_summary_update(self, i: int):
        self.order_subtotal_label_ctr[i].setText(f"{self.order_subtotal_val_ctr[i]:.2f}")
        self.order_discount_label_ctr[i].setText(f"{self.order_discount_val_ctr[i]:.2f}")
        self.order_tax_label_ctr[i].setText(f"{self.order_tax_val_ctr[i]:.2f}")
        self.order_total_label_ctr[i].setText(f"{self.order_total_val_ctr[i]:.2f}")
        self.order_pay_button_ctr[i].setText(f"Pay {self.order_total_val_ctr[i]:.2f}")
    # endregion > order_box
    
    def init_final_order_val(self):
        self.final_order_cust_name_value = ''
        self.final_order_cust_phone_value = ''
        self.final_order_cust_points_value = ''
        self.final_order_order_type_value = ''

        self.final_order_subtotal_value = 0
        self.final_order_discount_value = 0
        self.final_order_tax_value = 0
        self.final_order_total_value = 0
        pass
    def assign_final_order_val_entry(self, value):
        self.final_order_cust_name_value = value[0]
        self.final_order_cust_phone_value = value[0]
        self.final_order_cust_points_value = value[0]
        self.final_order_order_type_value = value[0]

        self.final_order_subtotal_value = value[0]
        self.final_order_discount_value = value[0]
        self.final_order_tax_value = value[0]
        self.final_order_total_value = value[0]
    def init_final_order_ctr(self): # NOTE: this is for the printing thread
        self.cashier_info_ctr = []
        self.cust_info_ctr = []
        self.final_order_table_ctr = []
        self.final_order_summary_ctr = []
        pass
        
    def init_ref_id_generator_entry(self, sales_group_id, cust_id):
        sales_group_id = f'{sales_group_id:02}'
        cust_id = f'{cust_id:05}'
        update_ts = f"{datetime.today().strftime('%y%m%d%H%M%S')}"

        self.ref_id = f"{sales_group_id}-{cust_id}-{update_ts}"

        return self.ref_id

    pass
class MyPOSView(MyGroupBox): # NOTE: layout
    def __init__(self, model: MyPOSModel):
        super().__init__()

        self.model = model

        self.setup_main_panel()

    def setup_main_panel(self):
        self.setup_panel_a()
        self.setup_panel_b()
        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.panel_a_box,0,0)
        self.main_layout.addWidget(self.panel_b_box,0,1)
        self.setLayout(self.main_layout)
        pass

    def setup_panel_a(self):
        self.panel_a_box = MyGroupBox()
        self.panel_a_layout = MyGridLayout()

        self.text_filter_button = MyPushButton(text='Filter')
        self.text_filter_field = MyLineEdit(object_name='text_filter_field', push_button=self.text_filter_button)
        self.text_filter_box = MyGroupBox()
        self.text_filter_layout = MyHBoxLayout()
        self.text_filter_layout.addWidget(self.text_filter_field)
        self.text_filter_box.setLayout(self.text_filter_layout)

        self.sync_ui_button = MyPushButton(text='Sync')
        self.barcode_scan_field = MyLineEdit(object_name='barcode_scan_field')
        self.barcode_scan_toggle_button = [
            MyPushButton(text='On'),
            MyPushButton(text='Off'),
        ]
        self.interactive_act_box = MyGroupBox()
        self.interactive_act_layout = MyHBoxLayout()
        self.interactive_act_layout.addWidget(self.sync_ui_button)
        self.interactive_act_layout.addWidget(self.barcode_scan_field)
        self.interactive_act_layout.addWidget(self.barcode_scan_toggle_button[0])
        self.interactive_act_layout.addWidget(self.barcode_scan_toggle_button[1])
        self.interactive_act_box.setLayout(self.interactive_act_layout)

        self.model.setup_pos_list_panel()
        self.pos_list_tab = MyTabWidget()
        self.pos_list_tab.addTab(self.model.pos_list_box, 'Overview')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.interactive_act_box,0,1)
        self.panel_a_layout.addWidget(self.pos_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def setup_panel_b(self):
        self.panel_b_box = MyGroupBox(object_name='panel_b_box')
        self.panel_b_layout = MyGridLayout(object_name='panel_b_layout')

        self.sel_cust_field = MyComboBox()
        self.sel_order_type_field = MyComboBox()
        self.add_order_button = MyPushButton(text='Add')
        self.load_order_button = MyPushButton(text='Load')
        self.add_order_act_box = MyGroupBox()
        self.add_order_act_layout = MyHBoxLayout()
        self.add_order_act_layout.addWidget(self.sel_cust_field)
        self.add_order_act_layout.addWidget(self.sel_order_type_field)
        self.add_order_act_layout.addWidget(self.add_order_button)
        self.add_order_act_layout.addWidget(self.load_order_button)
        self.add_order_act_box.setLayout(self.add_order_act_layout)
        
        self.order_tab = MyTabWidget()

        self.panel_b_layout.addWidget(self.add_order_act_box)
        self.panel_b_layout.addWidget(self.order_tab)
        self.panel_b_box.setLayout(self.panel_b_layout)

    def setup_payment_dialog(self):
        self.payment_dialog = MyDialog()
        self.payment_layout = MyGridLayout()

        self.final_order_table = MyTableWidget(object_name='final_order_table')
        # TODO: init table populating entry
        self.final_order_subtotal_label = MyLabel(text=f"{'test'}")
        self.final_order_discount_label = MyLabel(text=f"{'test'}")
        self.final_order_tax_label = MyLabel(text=f"{'test'}")
        self.final_order_total_label = MyLabel(text=f"{'test'}")
        self.final_order_summary_box = MyGroupBox()
        self.final_order_summary_layout = MyFormLayout()
        self.final_order_summary_layout.addRow('Subtotal', self.final_order_subtotal_label)
        self.final_order_summary_layout.addRow('Discount', self.final_order_discount_label)
        self.final_order_summary_layout.addRow('Tax', self.final_order_tax_label)
        self.final_order_summary_layout.addRow('Total', self.final_order_total_label)
        self.final_order_summary_box.setLayout(self.final_order_summary_layout)
        self.payment_a_box = MyGroupBox()
        self.payment_a_layout = MyVBoxLayout()
        self.payment_a_layout.addWidget(self.final_order_table)
        self.payment_a_layout.addWidget(self.final_order_summary_box)
        self.payment_a_box.setLayout(self.payment_a_layout)

        self.tender_amount_label = MyLabel(text='Amount tendered')
        self.tender_amount_field = MyLineEdit(object_name='tender_amount_field')
        self.numpad_key_toggle_button = [
            MyPushButton(object_name='numpad_key_toggle_button', text='Toggle'),
            MyPushButton(object_name='numpad_key_untoggle_button', text='Untoggle'),
        ]
        self.numpad_key_button = [
            MyPushButton(text='1'),
            MyPushButton(text='2'),
            MyPushButton(text='3'),
            MyPushButton(text='4'),
            MyPushButton(text='5'),
            MyPushButton(text='6'),
            MyPushButton(text='7'),
            MyPushButton(text='8'),
            MyPushButton(text='9'),
            MyPushButton(text='Delete'),
            MyPushButton(text='0'),
            MyPushButton(text='.'),
        ]
        self.numpad_key_box = MyGroupBox(object_name='numpad_key_box')
        self.numpad_key_layout = MyGridLayout(object_name='numpad_key_layout')
        self.numpad_key_layout.addWidget(self.numpad_key_button[0],0,0)
        self.numpad_key_layout.addWidget(self.numpad_key_button[1],0,1)
        self.numpad_key_layout.addWidget(self.numpad_key_button[2],0,2)
        self.numpad_key_layout.addWidget(self.numpad_key_button[3],1,0)
        self.numpad_key_layout.addWidget(self.numpad_key_button[4],1,1)
        self.numpad_key_layout.addWidget(self.numpad_key_button[5],1,2)
        self.numpad_key_layout.addWidget(self.numpad_key_button[6],2,0)
        self.numpad_key_layout.addWidget(self.numpad_key_button[7],2,1)
        self.numpad_key_layout.addWidget(self.numpad_key_button[8],2,2)
        self.numpad_key_layout.addWidget(self.numpad_key_button[9],3,0)
        self.numpad_key_layout.addWidget(self.numpad_key_button[10],3,1)
        self.numpad_key_layout.addWidget(self.numpad_key_button[11],3,2)
        self.numpad_key_box.setLayout(self.numpad_key_layout)
        self.payment_b_box = MyGroupBox()
        self.payment_b_layout = MyGridLayout()
        self.payment_b_layout.addWidget(self.tender_amount_label,0,0)
        self.payment_b_layout.addWidget(self.tender_amount_field,1,0)
        self.payment_b_layout.addWidget(self.numpad_key_toggle_button[0],1,1)
        self.payment_b_layout.addWidget(self.numpad_key_toggle_button[1],1,1)
        self.payment_b_layout.addWidget(self.numpad_key_box,2,0,1,2)
        self.payment_b_box.setLayout(self.payment_b_layout)
        
        self.reg_cust_name_label = MyLabel(text=f"Name: {'test'}")
        self.reg_cust_phone_label = MyLabel(text=f"Phone: {'test'}")
        self.reg_cust_points_label = MyLabel(text=f"Points: {'test'}")
        self.reg_cust_info_box = MyGroupBox()
        self.reg_cust_info_layout = MyHBoxLayout()
        self.reg_cust_info_layout.addWidget(self.reg_cust_name_label)
        self.reg_cust_info_layout.addWidget(self.reg_cust_phone_label)
        self.reg_cust_info_layout.addWidget(self.reg_cust_points_label)
        self.reg_cust_info_box.setLayout(self.reg_cust_info_layout)
        self.pay_cash_button = MyPushButton(text=f"Pay cash")
        self.pay_points_button = MyPushButton(text=f"Pay points")
        self.payment_act_box = MyGroupBox()
        self.payment_act_layout = MyHBoxLayout()
        self.payment_act_layout.addWidget(self.reg_cust_info_box,1,Qt.AlignmentFlag.AlignLeft)
        self.payment_act_layout.addWidget(self.pay_cash_button)
        self.payment_act_layout.addWidget(self.pay_points_button)
        self.payment_act_box.setLayout(self.payment_act_layout)

        self.payment_layout.addWidget(self.payment_a_box,0,0)
        self.payment_layout.addWidget(self.payment_b_box,0,1,Qt.AlignmentFlag.AlignTop)
        self.payment_layout.addWidget(self.payment_act_box,1,0,1,2)
        self.payment_dialog.setLayout(self.payment_layout)
    
    def setup_txn_complete_dialog(self):
        self.txn_complete_dialog = MyDialog()
        self.txn_complete_layout = MyGridLayout()

        self.txn_amount_tendered_label = MyLabel(text='Amount tendered')
        self.txn_amount_tendered_field = MyLabel(text=f"{'100.00'}")
        self.txn_order_change_label = MyLabel(text='Change')
        self.txn_order_change_field = MyLabel(text=f"{'100.00'}")
        self.txn_info_box = MyGroupBox()
        self.txn_info_layout = MyVBoxLayout()
        self.txn_info_layout.addWidget(self.txn_amount_tendered_label,1,Qt.AlignmentFlag.AlignCenter)
        self.txn_info_layout.addWidget(self.txn_amount_tendered_field,1,Qt.AlignmentFlag.AlignCenter)
        self.txn_info_layout.addWidget(self.txn_order_change_label,1,Qt.AlignmentFlag.AlignCenter)
        self.txn_info_layout.addWidget(self.txn_order_change_field,1,Qt.AlignmentFlag.AlignCenter)
        self.txn_info_box.setLayout(self.txn_info_layout)

        self.print_receipt_button = MyPushButton(text='Print')
        self.save_receipt_button = MyPushButton(text='Save')
        self.txn_complete_act_a_box = MyGroupBox()
        self.txn_complete_act_a_layout = MyHBoxLayout()
        self.txn_complete_act_a_layout.addWidget(self.print_receipt_button)
        self.txn_complete_act_a_layout.addWidget(self.save_receipt_button)
        self.txn_complete_act_a_box.setLayout(self.txn_complete_act_a_layout)

        self.txn_complete_summary_box = MyGroupBox(object_name='txn_complete_summary_box')
        self.txn_complete_summary_layout = MyVBoxLayout(object_name='txn_complete_summary_layout')
        self.txn_complete_summary_layout.addWidget(self.txn_info_box,1,Qt.AlignmentFlag.AlignCenter)
        self.txn_complete_summary_layout.addWidget(self.txn_complete_act_a_box,1,Qt.AlignmentFlag.AlignCenter)
        self.txn_complete_summary_box.setLayout(self.txn_complete_summary_layout)

        self.add_new_order_button = MyPushButton(text='Add new order')
        self.txn_complete_close_button = MyPushButton(text='Close')
        self.txn_complete_act_b_box = MyGroupBox()
        self.txn_complete_act_b_layout = MyHBoxLayout()
        self.txn_complete_act_b_layout.addWidget(self.add_new_order_button)
        self.txn_complete_act_b_layout.addWidget(self.txn_complete_close_button)
        self.txn_complete_act_b_box.setLayout(self.txn_complete_act_b_layout)
        
        self.txn_complete_layout.addWidget(self.txn_complete_summary_box,0,0)
        self.txn_complete_layout.addWidget(self.txn_complete_act_b_box,1,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.txn_complete_dialog.setLayout(self.txn_complete_layout)
    pass 
class MyPOSController: # NOTE: connections, setting attributes
    def __init__(self, model: MyPOSModel, view: MyPOSView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_pos_list_table()
        
        self.setup_panel_b_conn()
        self.populate_add_order_act_box()

    # NOTE: THIS IS PANEL A SECTION
    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.view.barcode_scan_field.returnPressed.connect(self.on_barcode_scan_field_return_pressed)
        self.view.barcode_scan_toggle_button[0].clicked.connect(lambda: self.on_barcode_scan_toggle_button_clicked(action='toggle'))
        self.view.barcode_scan_toggle_button[1].clicked.connect(lambda: self.on_barcode_scan_toggle_button_clicked(action='untoggle'))
        self.model.pos_list_prev_button.clicked.connect(lambda: self.on_pos_list_pag_button_clicked(action='go_prev'))
        self.model.pos_list_next_button.clicked.connect(lambda: self.on_pos_list_pag_button_clicked(action='go_next'))
        pass
    def populate_pos_list_table(self, text_filter='', prod_type='', page_number=1):
        prod_list = schema.list_all_prod_col(text_filter=text_filter, prod_type=prod_type, page_number=page_number)

        self.model.pos_total_page_number = schema.count_prod_list_total_pages(text_filter, prod_type)
        self.model.pos_page_number = 0 if self.model.pos_total_page_number <= 0 else self.model.pos_page_number
        self.model.pos_list_page_label.setText(f"Page {self.model.pos_page_number}/{self.model.pos_total_page_number}")

        self.model.pos_list_prev_button.setEnabled(page_number > 1)
        self.model.pos_list_next_button.setEnabled(len(prod_list) == 30)

        self.model.pos_list_table.setRowCount(len(prod_list))

        for pos_list_i, pos_list_v in enumerate(prod_list):
            self.add_item_button = MyPushButton(text='Add')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.add_item_button)
            table_act_panel.setLayout(table_act_laoyut)

            self.highlight = False
            self.highlight = True if pos_list_v[11] != 0 else self.highlight
                
            prod_barcode = MyTableWidgetItem(text=f"{pos_list_v[0]}", has_promo=self.highlight)
            prod_name = MyTableWidgetItem(text=f"{pos_list_v[1]}", has_promo=self.highlight)
            prod_brand = MyTableWidgetItem(text=f"{pos_list_v[2]}", has_promo=self.highlight)
            prod_price = MyTableWidgetItem(text=f"{pos_list_v[3]}", has_promo=self.highlight)
            prod_effective_dt = MyTableWidgetItem(text=f"{pos_list_v[4]}", has_promo=self.highlight)
            promo_name = MyTableWidgetItem(text=f"{pos_list_v[5]}", has_promo=self.highlight) # REVIEW: set icon or text??
            promo_value = MyTableWidgetItem(text=f"{pos_list_v[6]}", has_promo=self.highlight) # REVIEW: set value or percent??
            stock_on_hand = MyTableWidgetItem(text=f"{pos_list_v[7]}", has_promo=self.highlight)

            self.model.pos_list_table.setCellWidget(pos_list_i, 0, table_act_panel)
            self.model.pos_list_table.setItem(pos_list_i, 1, prod_barcode)
            self.model.pos_list_table.setItem(pos_list_i, 2, prod_name)
            self.model.pos_list_table.setItem(pos_list_i, 3, prod_brand)
            self.model.pos_list_table.setItem(pos_list_i, 4, prod_price)
            self.model.pos_list_table.setItem(pos_list_i, 5, prod_effective_dt)
            self.model.pos_list_table.setItem(pos_list_i, 6, promo_name)
            self.model.pos_list_table.setItem(pos_list_i, 7, promo_value)
            self.model.pos_list_table.setItem(pos_list_i, 8, stock_on_hand)


            self.setup_pos_list_table_act_panel_conn(value=pos_list_v)
            pass
        pass
    def setup_pos_list_table_act_panel_conn(self, value):
        self.add_item_button.clicked.connect(lambda _, value=value: self.on_add_prod_button_clicked(value))
        pass
    def on_add_prod_button_clicked(self, value):
        print('on_add_pos_button_clicked')
        self.on_add_prod_button_clicked(value)

        pass

    def on_text_filter_button_clicked(self):
        self.model.pos_page_number = 1

        self.start_sync_ui()
        pass
    def on_sync_ui_button_clicked(self):
        self.model.pos_page_number = 1

        self.start_sync_ui()
        
        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass
    def start_sync_ui(self):
        try:
            text_filter = ''
            prod_type = ''

            if self.view.order_tab.count() > 0:
                i = self.view.order_tab.currentIndex()
                
                text_filter = self.view.text_filter_field.text()
                prod_type = self.model.order_order_type_value_ctr[i]

            self.populate_pos_list_table(text_filter=text_filter, prod_type=prod_type, page_number=self.model.pos_page_number)
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")

        pass
    def on_barcode_scan_toggle_button_clicked(self, action):
        if action == 'toggle':
            self.view.barcode_scan_toggle_button[0].hide()
            self.view.barcode_scan_toggle_button[1].show()
            self.view.barcode_scan_field.show()
            pass
        elif action == 'untoggle':
            self.view.barcode_scan_toggle_button[0].show()
            self.view.barcode_scan_toggle_button[1].hide()
            self.view.barcode_scan_field.hide()
            pass
        pass
     
    def on_pos_list_pag_button_clicked(self, action):
        i = self.view.order_tab.currentIndex()

        if action == 'go_prev':
            if self.model.pos_page_number > 1:
                self.model.pos_page_number -= 1
            pass
        elif action == 'go_next':
            self.model.pos_page_number += 1
            pass
        self.start_sync_ui()
        pass

    # NOTE: THIS IS PANEL B SECTION
    def setup_panel_b_conn(self):
        self.view.add_order_button.clicked.connect(self.on_add_order_button_clicked)
        self.view.order_tab.currentChanged.connect(self.on_order_tab_current_changed)
        pass
    def populate_add_order_act_box(self):
        cust_list = schema.list_cust_name_col()
        
        self.view.sel_cust_field.addItem('Guest order')
        for cust_name in cust_list: self.view.sel_cust_field.addItems(cust_name)

        self.view.sel_order_type_field.addItem('Retail')
        self.view.sel_order_type_field.addItem('Wholesale')

        pass
    def on_add_order_button_clicked(self):
        try:
            sel_cust = self.view.sel_cust_field.currentText()

            sel_cust_id = schema.list_cust_id(self.view.sel_cust_field.currentText()) # REVIEW: NEEDS TO HAVE A PROPER IMPLEMENTATION

            if sel_cust_id != 0:
                sel_cust_data = schema.list_all_cust_col_via_cust_id(sel_cust_id) # REVIEW: NEEDS TO HAVE A PROPER IMPLEMENTATION

                for cust_name, cust_phone, cust_points in sel_cust_data: # REVIEW: NEEDS TO HAVE A PROPER IMPLEMENTATION
                    order_name = cust_name
                    order_phone = cust_phone
                    order_points = cust_points

                    self.model.order_cust_name_value = order_name
                    self.model.order_cust_phone_value = order_phone
                    self.model.order_cust_points_value = order_points

            else:
                self.model.order_cust_name_value = sel_cust
    
            print('cust_name:', self.model.order_cust_name_value)
            print('cust_phone:', self.model.order_cust_phone_value)
            print('cust_points:', self.model.order_cust_points_value)

            order_type = self.view.sel_order_type_field.currentText()

            self.model.order_order_type_value = order_type

            self.model.setup_order_tab_panel()

            self.model.append_order_tab_ctr()

            curr_i = self.view.order_tab.addTab(self.model.order_box, sel_cust)
            self.view.order_tab.setCurrentIndex(curr_i)

            self.setup_order_tab_conn()
        except Exception as e:
            print(e)
        pass
    def on_order_tab_current_changed(self):
        i = self.view.order_tab.currentIndex()
        
        self.model.pos_page_number = 1

        self.start_sync_ui()
        pass
    def setup_order_tab_conn(self):
        i = self.view.order_tab.currentIndex()
        
        self.model.order_clear_button_ctr[i].clicked.connect(self.on_order_clear_button_clicked)
        self.model.order_discard_button_ctr[i].clicked.connect(self.on_order_discard_button_clicked)
        self.model.order_lock_toggle_button[0].clicked.connect(lambda: self.order_lock_toggle_button(action='toggle'))
        self.model.order_lock_toggle_button[1].clicked.connect(lambda: self.order_lock_toggle_button(action='untoggle'))
        self.model.order_save_button_ctr[i].clicked.connect(self.on_order_save_button_clicked)

        self.model.order_pay_button_ctr[i].clicked.connect(self.on_order_pay_button_clicked)
        pass

    def on_order_clear_button_clicked(self):
        i = self.view.order_tab.currentIndex()

        if self.model.order_table_ctr[i].rowCount() > 0:
            confirm = QMessageBox.warning(self.view, 'Clear', 'Clear this table?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if confirm is QMessageBox.StandardButton.Yes:

                self.model.order_table_ctr[i].setRowCount(0)

                self.model.init_order_clear_entry(i)

                pass
        else:
            QMessageBox.critical(self.view, 'Error', 'This table is already empty.')

    # region > add prod manip
    def on_barcode_scan_field_return_pressed(self):
        try:
            barcode = self.view.barcode_scan_field.text()

            sel_prod_data = schema.list_all_prod_col_via_barcode(barcode=barcode)

            i = self.view.order_tab.currentIndex()
            
            for _, value in enumerate(sel_prod_data):
                sel_prod_name, sel_prod_price, sel_prod_discount, cust_order_prod_name = self.model.assign_cust_order_val_entry(i, value)

                if cust_order_prod_name:
                    self.model.init_add_prod_update_entry(i, cust_order_prod_name, 1, sel_prod_price, sel_prod_discount) # param for sel qty is set to 1
                    pass
                else:
                    self.populate_order_table(i, value, sel_prod_name, sel_prod_price, sel_prod_discount, 1) # param for sel qty is set to 1

                self.model.init_add_prod_compute_entry(i, 1, sel_prod_price, sel_prod_discount) # param for sel qty is set to 1
                self.model.init_order_summary_update(i)

                self.model.init_sel_prod_val()
            pass
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")

    def on_add_prod_button_clicked(self, value):
        try:
            i = self.view.order_tab.currentIndex()

            sel_prod_name, sel_prod_price, sel_prod_discount, cust_order_prod_name = self.model.assign_cust_order_val_entry(i, value)
            
            print(sel_prod_name)

            sel_qty, confirm = QInputDialog.getInt(self.view, sel_prod_name, 'Input quantity:', 0, 1, 9999999)

            if confirm:
                if cust_order_prod_name:
                    self.model.init_add_prod_update_entry(i, cust_order_prod_name, sel_qty, sel_prod_price, sel_prod_discount)
                    pass
                else:
                    self.populate_order_table(i, value, sel_prod_name, sel_prod_price, sel_prod_discount, sel_qty)

                self.model.init_add_prod_compute_entry(i, sel_qty, sel_prod_price, sel_prod_discount)
                self.model.init_order_summary_update(i)

                self.model.init_sel_prod_val()
            pass
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")
            pass
    def populate_order_table(self, i: int, value, sel_prod_name, sel_prod_price, sel_prod_discount, sel_qty):
        print('THIS INDEX!!!: ', i)
        row_i = self.model.order_table_ctr[i].rowCount() 
                    
        self.model.order_table_ctr[i].insertRow(row_i)

        self.model.sel_qty_val = sel_qty
        self.model.sel_prod_name_val = sel_prod_name
        self.model.sel_prod_price_val = sel_prod_price * sel_qty
        self.model.sel_prod_discount_val = sel_prod_discount * sel_qty

        self.drop_all_qty_button = MyPushButton(text='Drop all')
        self.drop_qty_button = MyPushButton(text='Drop')
        self.add_qty_button = MyPushButton(text='Add')
        self.edit_qty_button = MyPushButton(text='Edit')
        self.cust_order_act_box = MyGroupBox(object_name='cust_order_act_box')
        self.cust_order_act_layout = MyHBoxLayout(object_name='cust_order_act_layout')
        self.cust_order_act_layout.addWidget(self.drop_all_qty_button)
        self.cust_order_act_layout.addWidget(self.drop_qty_button)
        self.cust_order_act_layout.addWidget(self.add_qty_button)
        self.cust_order_act_layout.addWidget(self.edit_qty_button)
        self.cust_order_act_box.setLayout(self.cust_order_act_layout)

        prod_qty = MyTableWidgetItem(str(self.model.sel_qty_val))
        prod_name = MyTableWidgetItem(str(self.model.sel_prod_name_val))
        prod_price = MyTableWidgetItem(str(self.model.sel_prod_price_val))
        prod_discount = MyTableWidgetItem(str(self.model.sel_prod_discount_val))

        self.model.order_table_ctr[i].setCellWidget(row_i, 0, self.cust_order_act_box)
        self.model.order_table_ctr[i].setItem(row_i, 1, prod_qty)
        self.model.order_table_ctr[i].setItem(row_i, 2, prod_name)
        self.model.order_table_ctr[i].setItem(row_i, 3, prod_price)
        self.model.order_table_ctr[i].setItem(row_i, 4, prod_discount)

        self.setup_order_table_conn(value)
        pass
    def setup_order_table_conn(self, value):
        self.drop_all_qty_button.clicked.connect(lambda: self.on_drop_all_qty_button_clicked(value))
        self.drop_qty_button.clicked.connect(lambda: self.on_drop_qty_button_clicked(value))
        self.add_qty_button.clicked.connect(lambda: self.on_add_qty_button_clicked(value))
        self.edit_qty_button.clicked.connect(lambda: self.on_edit_qty_button_clicked(value))
        pass
    
    def on_drop_all_qty_button_clicked(self, value):
        try: 
            i = self.view.order_tab.currentIndex()

            sel_prod_name, _, _, cust_order_prod_name = self.model.assign_cust_order_val_entry(i, value)
            
            print(sel_prod_name)

            if cust_order_prod_name: # NOTE: if item name already exist in the order tab
                self.model.init_drop_all_qty_update_entry(i, cust_order_prod_name)

            self.model.init_order_summary_update(i)
            self.model.init_sel_prod_val()
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")

        pass
    def on_drop_qty_button_clicked(self, value):
        try:
            i = self.view.order_tab.currentIndex()

            _, sel_prod_price, sel_prod_discount, cust_order_prod_name = self.model.assign_cust_order_val_entry(i, value)

            if cust_order_prod_name: # NOTE: if item name already exist in the order tab
                self.model.init_drop_qty_update_entry(i, cust_order_prod_name, sel_prod_price, sel_prod_discount)
                
            self.model.init_order_summary_update(i)
            self.model.init_sel_prod_val()
            pass
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")
        pass
    def on_add_qty_button_clicked(self, value):
        try:
            i = self.view.order_tab.currentIndex()

            _, sel_prod_price, sel_prod_discount, cust_order_prod_name = self.model.assign_cust_order_val_entry(i, value)

            if cust_order_prod_name: # NOTE: if item name already exist in the order tab
                self.model.init_add_qty_update_entry(i, cust_order_prod_name, sel_prod_price, sel_prod_discount)
                
            self.model.init_order_summary_update(i)
            self.model.init_sel_prod_val()
            pass
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")
        pass
    def on_edit_qty_button_clicked(self, value):
        try:
            i = self.view.order_tab.currentIndex()

            sel_prod_name, sel_prod_price, sel_prod_discount, cust_order_prod_name = self.model.assign_cust_order_val_entry(i, value)
            
            print(sel_prod_name)

            sel_qty, confirm = QInputDialog.getInt(self.view, sel_prod_name, 'Input quantity:', 0, 1, 9999999)

            if confirm:
                if cust_order_prod_name: # NOTE: if item name already exist in the order tab
                    self.model.init_edit_qty_update_entry(i, cust_order_prod_name, sel_qty, sel_prod_price, sel_prod_discount)
                    
                self.model.init_order_summary_update(i)
                self.model.init_sel_prod_val()
            pass
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")
        pass
    # endregion > add prod manip

    def on_order_discard_button_clicked(self):
        confirm = QMessageBox.warning(self.view, 'Discard', 'Discard this order?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            i = self.view.order_tab.currentIndex()

            self.view.order_tab.removeTab(i)

            self.model.remove_order_tab_ctr(i)

            self.start_sync_ui()
        pass
    def order_lock_toggle_button(self, action):
        i = self.view.order_tab.currentIndex()
        
        if action == 'toggle':
            flag = True

            self.model.order_lock_toggle_button_ctr[i][0].hide()
            self.model.order_lock_toggle_button_ctr[i][1].show()
            pass
        elif action == 'untoggle':
            flag = False

            self.model.order_lock_toggle_button_ctr[i][0].show()
            self.model.order_lock_toggle_button_ctr[i][1].hide()
            pass

        self.model.order_type_label_ctr[i].setDisabled(flag)
        self.model.order_clear_button_ctr[i].setDisabled(flag)
        self.model.order_table_ctr[i].setDisabled(flag)
        self.model.order_subtotal_label_ctr[i].setDisabled(flag)
        self.model.order_discount_label_ctr[i].setDisabled(flag)
        self.model.order_tax_label_ctr[i].setDisabled(flag)
        self.model.order_total_label_ctr[i].setDisabled(flag)
        self.model.order_discard_button_ctr[i].setDisabled(flag)
        self.model.order_save_button_ctr[i].setDisabled(flag)
        self.model.order_pay_button_ctr[i].setDisabled(flag)
        
        pass
    def on_order_save_button_clicked(self):
        pass

    def on_order_pay_button_clicked(self):
        i = self.view.order_tab.currentIndex()

        self.view.setup_payment_dialog()

        if self.model.order_table_ctr[i].rowCount() > 0:
            row_i = self.view.final_order_table.rowCount()             
            for col_i in range(self.model.order_table_ctr[i].rowCount()):
                sel_prod_qty = int(self.model.order_table_ctr[i].item(col_i, 1).text())
                sel_prod_name = str(self.model.order_table_ctr[i].item(col_i, 2).text())
                sel_prod_price = float(self.model.order_table_ctr[i].item(col_i, 3).text())

                self.populate_final_order_table(row_i, sel_prod_qty, sel_prod_name, sel_prod_price)

                self.model.final_order_table_ctr.append([sel_prod_qty, sel_prod_name, sel_prod_price])
                pass
            self.model.cust_info_ctr.append([
                self.model.order_cust_name_value_ctr[i],
                self.model.order_cust_phone_value_ctr[i],
                self.model.order_cust_points_value_ctr[i],
            ])
            self.model.cashier_info_ctr.append([self.model.user_name, self.model.user_phone])
            self.model.final_order_summary_ctr.append([
                self.model.order_subtotal_val_ctr[i],
                self.model.order_discount_val_ctr[i],
                self.model.order_tax_val_ctr[i],
                self.model.order_total_val_ctr[i],
            ])
            
            self.update_reg_cust_box(i)

            self.setup_payment_dialog_conn()
            self.on_close_button_clicked(self.view.payment_dialog)
           
            self.view.payment_dialog.exec()

            if self.view.payment_dialog.close():
                self.model.init_final_order_ctr()
        else:
            QMessageBox.critical(self.view, 'Error', 'Please add a product first.')
        pass
    def populate_final_order_table(self, row_i, sel_prod_qty, sel_prod_name, sel_prod_price):
        prod_qty = MyTableWidgetItem(f"{sel_prod_qty}")
        prod_name = MyTableWidgetItem(f"{sel_prod_name}")
        prod_price = MyTableWidgetItem(f"{sel_prod_price:.2f}")

        self.view.final_order_table.insertRow(row_i)

        self.view.final_order_table.setItem(row_i, 0, prod_qty)
        self.view.final_order_table.setItem(row_i, 1, prod_name)
        self.view.final_order_table.setItem(row_i, 2, prod_price)
        pass
    def update_reg_cust_box(self, i):
        self.view.final_order_subtotal_label.setText(f"{self.model.order_subtotal_val_ctr[i]:.2f}")
        self.view.final_order_discount_label.setText(f"{self.model.order_discount_val_ctr[i]:.2f}")
        self.view.final_order_tax_label.setText(f"{self.model.order_tax_val_ctr[i]:.2f}")
        self.view.final_order_total_label.setText(f"{self.model.order_total_val_ctr[i]:.2f}")

        if self.model.order_cust_name_value_ctr[i] != 'Guest order':
            self.view.reg_cust_name_label.setText(f"Name: {self.model.order_cust_name_value_ctr[i]}")
            self.view.reg_cust_phone_label.setText(f"Phone: {self.model.order_cust_phone_value_ctr[i]}")
            self.view.reg_cust_points_label.setText(f"Points: {self.model.order_cust_points_value_ctr[i]}")
        else:
            self.view.reg_cust_name_label.setText(f"{self.model.order_cust_name_value_ctr[i]}")
            self.view.reg_cust_phone_label.hide()
            self.view.reg_cust_points_label.hide()
        pass

    # NOTE: THIS IS PAYMENT DIALOG SECTION
    def setup_payment_dialog_conn(self):
        self.view.numpad_key_toggle_button[0].clicked.connect(lambda: self.on_numpad_key_toggle_button_clicked(action='toggle'))
        self.view.numpad_key_toggle_button[1].clicked.connect(lambda: self.on_numpad_key_toggle_button_clicked(action='untoggle'))
        self.view.numpad_key_button[0].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='1'))
        self.view.numpad_key_button[1].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='2'))
        self.view.numpad_key_button[2].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='3'))
        self.view.numpad_key_button[3].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='4'))
        self.view.numpad_key_button[4].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='5'))
        self.view.numpad_key_button[5].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='6'))
        self.view.numpad_key_button[6].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='7'))
        self.view.numpad_key_button[7].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='8'))
        self.view.numpad_key_button[8].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='9'))
        self.view.numpad_key_button[9].clicked.connect(lambda: self.on_numpad_key_button_clicked())
        self.view.numpad_key_button[10].clicked.connect(lambda: self.on_numpad_key_button_clicked(value='0'))
        self.view.numpad_key_button[11].clicked.connect(lambda: self.on_numpad_key_button_clicked())
        self.view.pay_cash_button.clicked.connect(self.on_pay_cash_button_clicked)
        self.view.pay_points_button.clicked.connect(self.on_pay_points_button_clicked)
        pass
    def on_numpad_key_toggle_button_clicked(self, action):
        if action == 'toggle':
            self.view.numpad_key_toggle_button[0].hide()
            self.view.numpad_key_toggle_button[1].show()
            self.view.numpad_key_box.show()
            pass
        elif action == 'untoggle':
            self.view.numpad_key_toggle_button[0].show()
            self.view.numpad_key_toggle_button[1].hide()
            self.view.numpad_key_box.hide()
            pass
        pass
    def on_numpad_key_button_clicked(self, value=''):
        pass
    def on_pay_cash_button_clicked(self):
        try:
            i = self.view.order_tab.currentIndex()
            amount_tendered = float(self.view.tender_amount_field.text())
            order_total = float(self.model.order_total_val_ctr[i])


            if amount_tendered >= order_total:
                confirm = QMessageBox.warning(self.view.payment_dialog, 'Confirm', f"Pay {amount_tendered} for this order?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if confirm is QMessageBox.StandardButton.Yes:

                    order_prod_list_data = self.model.final_order_table_ctr

                    for list_i, list_v in enumerate(order_prod_list_data):
                        user_name = self.model.user_name
                        cust_name = self.model.order_cust_name_value_ctr[i]
                        order_type = self.model.order_order_type_value_ctr[i]

                        prod_qty = int(list_v[0])
                        prod_name = str(list_v[1])
                        prod_price = float(list_v[2])

                        item_id = schema.get_item_id(prod_name)
                        item_price_id = schema.get_item_price_id(item_id)
                        sales_group_id = schema.get_sales_group_id(order_type)
                        cust_id = schema.get_cust_id(cust_name)
                        stock_id = schema.get_stock_id(item_id)
                        user_id = schema.get_user_id(user_name)

                        ref_id = self.model.init_ref_id_generator_entry(sales_group_id, cust_id)

                        schema.add_new_txn(item_price_id, cust_id, stock_id, user_id, prod_qty, prod_price, ref_id)

                        schema.update_stock(item_id, stock_id, prod_qty)

                    order_change = float(amount_tendered - order_total)

                    schema.update_cust_reward(cust_id, order_total, ref_id) # FIX

                    self.model.remove_order_tab_ctr(i)
                    self.view.order_tab.removeTab(i)
                    self.view.payment_dialog.close()

                    self.view.setup_txn_complete_dialog()

                    self.view.txn_amount_tendered_field.setText(f"<b>{amount_tendered:.2f}</b>")
                    self.view.txn_order_change_field.setText(f"<b>{order_change:.2f}</b>")

                    self.set_txn_complete_dialog_conn()

                    self.view.txn_complete_dialog.exec()
                pass
            else:
                QMessageBox.critical(self.view.payment_dialog, 'Error', 'Insufficient fund.')
        except Exception as e:
            QMessageBox.critical(self.view.payment_dialog, 'Error', 'Invalid numerical input.')

        pass
    def on_pay_points_button_clicked(self):
        self.view.setup_print_dialog()

        #  TODO: add methods here

        self.set_print_dialog_conn(payment_type='points')
        self.view.print_dialog.exec()
        pass

    def on_add_new_order_button_clicked(self):
        self.view.txn_complete_dialog.close()    
        self.on_add_order_button_clicked()
        pass

    def set_txn_complete_dialog_conn(self, payment_type=''):
        self.view.add_new_order_button.clicked.connect(self.on_add_new_order_button_clicked)
        self.view.txn_complete_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.view.txn_complete_dialog))
        self.view.print_receipt_button.clicked.connect(lambda: self.on_print_button_clicked(action='print_receipt', payment_type=payment_type))
        self.view.save_receipt_button.clicked.connect(lambda: self.on_print_button_clicked(action='save_receipt', payment_type=payment_type))

    def on_print_button_clicked(self, action, payment_type):
        if action == 'print_receipt':
            # self.print_thread = ReceiptGenerator()
            print(action)
            pass
        elif action == 'save_receipt':
            print(action)
            pass
        pass
    def on_close_button_clicked(self, widget: QWidget):
        try:
            widget.close()
            pass
        except Exception as e:
            print(e)
        pass
    pass


class MyPOSWindow(MyGroupBox):
    def __init__(self, name, phone): # NOTE: 'name' param is for the current user (cashier, cashier, dev) name
        super().__init__(object_name='MyPOSWindow')

        self.model = MyPOSModel(name=name, phone=phone)
        self.view = MyPOSView(self.model)
        self.controller = MyPOSController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.show()


# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    pos_window = MyPOSWindow(name='test-name', phone='test-phone')

    pos_window.run()
    app.exec()