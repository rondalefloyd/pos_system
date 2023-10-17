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
        self.init_order_tab_ctr()

    def init_pos_list_page_val(self):
        self.pos_page_number = 0
        self.pos_total_page_number = schema.count_prod_list_total_pages()
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

    def init_order_tab_val(self):
        self.order_cust_name_value = ''
        self.order_order_type_value = ''

        self.order_subtotal_value = 0
        self.order_discount_value = 0
        self.order_tax_value = 0
        self.order_total_value = 0
        pass
    def init_order_tab_ctr(self):
        self.order_cust_name_value_ctr = []
        self.order_order_type_value_ctr = []

        self.order_subtotal_value_ctr = []
        self.order_discount_value_ctr = []
        self.order_tax_value_ctr = []
        self.order_total_value_ctr = []

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
        self.order_type_label = MyLabel(text='Order type: type')
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
        self.order_cust_name_value_ctr.append(self.order_cust_name_value)
        self.order_order_type_value_ctr.append(self.order_order_type_value)

        self.order_subtotal_value_ctr.append(self.order_subtotal_value)
        self.order_discount_value_ctr.append(self.order_discount_value)
        self.order_tax_value_ctr.append(self.order_tax_value)
        self.order_total_value_ctr.append(self.order_total_value)

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

        print('order_cust_name_value',self.order_cust_name_value_ctr)
        print('order_order_type_value',self.order_order_type_value_ctr)
        print('---------------------------------------------------')
        print('order_table_value',self.order_table_ctr)
        print('---------------------------------------------------')
        print('order_subtotal_value',self.order_subtotal_value_ctr)
        print('order_discount_value',self.order_discount_value_ctr)
        print('order_tax_value',self.order_tax_value_ctr)
        print('order_total_value',self.order_total_value_ctr)
        print('---------------------------------------------------')
        print('order_type_label',self.order_type_label_ctr)
        print('order_clear_button',self.order_clear_button_ctr)
        print('---------------------------------------------------')
        print('order_subtotal_label',self.order_subtotal_label_ctr)
        print('order_discount_label',self.order_discount_label_ctr)
        print('order_tax_label',self.order_tax_label_ctr)
        print('order_total_label',self.order_total_label_ctr)
        print('---------------------------------------------------')
        print('order_discard_button',self.order_discard_button_ctr)
        print('order_lock_toggle_button',self.order_lock_toggle_button_ctr)
        print('order_save_button',self.order_save_button_ctr)
        print('order_pay_button',self.order_pay_button_ctr)

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

    pass 
class MyPOSController: # NOTE: connections, setting attributes
    def __init__(self, model: MyPOSModel, view: MyPOSView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_pos_list_table()
        
        self.setup_panel_b_conn()

    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.model.pos_list_prev_button.clicked.connect(lambda: self.on_pos_list_pag_button_clicked(action='go_prev'))
        self.model.pos_list_next_button.clicked.connect(lambda: self.on_pos_list_pag_button_clicked(action='go_next'))
        pass

    def populate_pos_list_table(self, text_filter='', page_number=1):
        pos_list = schema.list_all_prod_col(text_filter=text_filter, page_number=page_number)

        self.model.pos_list_page_label.setText(f"Page {page_number}/{self.model.pos_total_page_number}")

        self.model.pos_list_prev_button.setEnabled(page_number > 1)
        self.model.pos_list_next_button.setEnabled(len(pos_list) == 30)

        self.model.pos_list_table.setRowCount(len(pos_list))

        for pos_list_i, pos_list_v in enumerate(pos_list):
            self.add_item_button = MyPushButton(text='Add')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.add_item_button)
            table_act_panel.setLayout(table_act_laoyut)

            prod_barcode = QTableWidgetItem(f"{pos_list_v[0]}")
            prod_name = QTableWidgetItem(f"{pos_list_v[1]}")
            prod_brand = QTableWidgetItem(f"{pos_list_v[2]}")
            prod_price = QTableWidgetItem(f"{pos_list_v[3]}")
            prod_effective_dt = QTableWidgetItem(f"{pos_list_v[4]}")
            promo_name = QTableWidgetItem(f"{pos_list_v[5]}")
            stock_on_hand = QTableWidgetItem(f"{pos_list_v[6]}")

            self.model.pos_list_table.setCellWidget(pos_list_i, 0, table_act_panel)
            self.model.pos_list_table.setItem(pos_list_i, 1, prod_barcode)
            self.model.pos_list_table.setItem(pos_list_i, 2, prod_name)
            self.model.pos_list_table.setItem(pos_list_i, 3, prod_brand)
            self.model.pos_list_table.setItem(pos_list_i, 4, prod_price)
            self.model.pos_list_table.setItem(pos_list_i, 5, prod_effective_dt)
            self.model.pos_list_table.setItem(pos_list_i, 6, promo_name)
            self.model.pos_list_table.setItem(pos_list_i, 7, stock_on_hand)


            self.setup_pos_list_table_act_panel_conn(value=pos_list_v)
            pass
        pass
    def setup_pos_list_table_act_panel_conn(self, value):
        self.add_item_button.clicked.connect(lambda _, value=value: self.on_add_pos_button_clicked(value))
        pass
    def on_add_pos_button_clicked(self, value):
        print('on_add_pos_button_clicked')
        i = self.view.order_tab.currentIndex()

        prod_name = str(value[1])

        tendered_qty, confirm = QInputDialog.getInt(self.view, prod_name, 'Input quantity:', 0, 1, 9999999)

        if confirm:
            item_i = self.model.order_table_ctr[i].rowCount() # REVIEW: 
            self.model.order_table_ctr[i].insertRow(item_i) # REVIEW: 

            cust_order_list = self.model.order_table_ctr[i].findItems(prod_name, Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name

            prod_qty = MyTableWidgetItem(str()) # TODO: needs to have proper values
            prod_name = MyTableWidgetItem(str()) # TODO: needs to have proper values
            prod_price = MyTableWidgetItem(str()) # TODO: needs to have proper values
            prod_discount = MyTableWidgetItem(str()) # TODO: needs to have proper values

            self.model.order_table_ctr[i].setItem(item_i, 1, prod_qty)
            self.model.order_table_ctr[i].setItem(item_i, 2, prod_name)
            self.model.order_table_ctr[i].setItem(item_i, 3, prod_price)
            self.model.order_table_ctr[i].setItem(item_i, 4, prod_discount)

            print('cust_order_list:', cust_order_list)
            print('tendered_qty:', tendered_qty)

        pass

    def on_text_filter_button_clicked(self):
        self.model.pos_page_number = 1
        self.model.pos_list_page_label.setText(f"Page {self.model.pos_page_number}/{self.model.pos_total_page_number}")

        self.populate_pos_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.pos_page_number) 
        pass
    def on_sync_ui_button_clicked(self):
        self.start_sync_ui()

        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass
    def start_sync_ui(self):
        self.model.init_pos_list_page_val()
        self.model.pos_list_page_label.setText(f"Page {self.model.pos_page_number}/{self.model.pos_total_page_number}")
        self.populate_pos_list_table()

    def on_pos_list_pag_button_clicked(self, action):
        print('pos_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.pos_page_number > 1:
                self.model.pos_page_number -= 1
                self.model.pos_list_page_label.setText(f"Page {self.model.pos_page_number}/{self.model.pos_total_page_number}")

            self.populate_pos_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.pos_page_number)
            pass
        elif action == 'go_next':
            self.model.pos_page_number += 1
            self.model.pos_list_page_label.setText(f"Page {self.model.pos_page_number}/{self.model.pos_total_page_number}")

            self.populate_pos_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.pos_page_number)
            pass
        pass

    def setup_panel_b_conn(self):
        self.view.add_order_button.clicked.connect(self.on_add_order_button_clicked)
        pass
    def on_add_order_button_clicked(self):
        self.model.setup_order_tab_panel()

        order_name = self.view.sel_cust_field.currentText()
        order_type = self.view.sel_order_type_field.currentText()

        self.view.order_tab.addTab(self.model.order_box, order_name)

        self.model.order_cust_name_value = order_name
        self.model.order_order_type_value = order_type

        self.model.append_order_tab_ctr()

    def on_close_button_clicked(self, widget: QWidget):
        widget.close()
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