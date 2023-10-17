
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
from src.sql.admin.prod import *
from src.widget.admin.admin import *
from templates.qss.qss_config import QSSConfig

schema = MyProdSchema()
qss = QSSConfig()

class MyProdModel: # NOTE: entries
    def __init__(self, name):
        # NOTE: global variables
        self.gdrive_path = 'G:' + f"/My Drive/"
        self.user_name = name

        self.init_selected_prod_data_entry()
        self.init_progress_data_entry()
        self.init_prod_list_page_entry()
        self.init_stock_list_page_entry()

    # region: prod
    def setup_prod_list_tab_panel(self):
        self.prod_list_table = MyTableWidget(object_name='prod_list_table')
        self.prod_list_prev_button = MyPushButton(text='Prev')
        self.prod_list_page_label = MyLabel(text=f"Page {self.page_number}/{self.total_page_number}")
        self.prod_list_next_button = MyPushButton(text='Next')
        self.prod_list_pag_box = MyGroupBox()
        self.prod_list_pag_layout = MyHBoxLayout(object_name='prod_list_pag_layout')
        self.prod_list_pag_layout.addWidget(self.prod_list_prev_button)
        self.prod_list_pag_layout.addWidget(self.prod_list_page_label)
        self.prod_list_pag_layout.addWidget(self.prod_list_next_button)
        self.prod_list_pag_box.setLayout(self.prod_list_pag_layout)
        self.prod_list_box = MyGroupBox()
        self.prod_list_layout = MyGridLayout()
        self.prod_list_layout.addWidget(self.prod_list_table,0,0)
        self.prod_list_layout.addWidget(self.prod_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.prod_list_box.setLayout(self.prod_list_layout)
        pass
    def init_prod_list_page_entry(self):
        self.page_number = 1
        self.total_page_number = schema.count_prod_list_total_pages()
    def init_selected_prod_data_entry(self):
        self.sel_prod_barcode_value = None
        self.sel_prod_name_value = None
        self.sel_prod_exp_dt_value = None
        self.sel_prod_type_value = None
        self.sel_prod_brand_value = None
        self.sel_prod_sales_group_value = None
        self.sel_prod_supplier_value = None
        self.sel_prod_cost_value = None
        self.sel_prod_sell_price_value = None
        self.sel_prod_effective_dt_value = None
        self.sel_prod_promo_name_value = None
        self.sel_prod_promo_value_value = None
        self.sel_prod_tracking_value = None
        self.sel_prod_tracking_bool_value = False
        pass
    def assign_selected_prod_data_entry(self, value):
        self.sel_prod_barcode_value = str(value[0])
        self.sel_prod_name_value = str(value[1])
        self.sel_prod_exp_dt_value = str(value[2])
        self.sel_prod_type_value = str(value[3])
        self.sel_prod_brand_value = str(value[4])
        self.sel_prod_sales_group_value = str(value[5])
        self.sel_prod_supplier_value = str(value[6])
        self.sel_prod_cost_value = str(value[7])
        self.sel_prod_sell_price_value = str(value[8])
        self.sel_prod_effective_dt_value = str(value[9])
        self.sel_prod_promo_name_value = str(value[10])
        self.sel_prod_promo_value_value = str(value[11])

        self.sel_prod_tracking_value = str(value[12])

        if str(value[12]) == 'Enabled':
            self.sel_prod_tracking_bool_value = True 
        elif str(value[12]) == 'Disabled':
            self.sel_prod_tracking_bool_value = False 

        self.sel_datetime_created_value = str(value[13])
        self.sel_prod_item_id_value = value[14]
        self.sel_prod_price_id_value = value[15]
        self.sel_prod_promo_id_value = value[16]
        self.sel_prod_stock_id_value = value[17]

    def init_progress_data_entry(self):
        self.prog_data_count_value = 0
        self.prog_total_data_value = 0
        self.prog_remaining_data_value = 0
        pass
    def setup_progress_panel(self, window_title, progress_type):
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_label = MyLabel()
        self.progress_dialog = MyDialog()
        self.progress_layout = MyGridLayout()
        self.progress_layout.addWidget(self.progress_bar,0,0)
        self.progress_layout.addWidget(self.progress_label,1,0)
        self.progress_dialog.setLayout(self.progress_layout)

    def import_prod_entry(self, data_frame):
        self.prod_import_thread = MyDataImportThread(data_name='prod', data_frame=data_frame) # NOTE: ths is QThread for data import
        self.prod_import_thread.start()

    def setup_manage_prod_panel(self, window_title):
        self.manage_prod_dialog = MyDialog(window_title=window_title)
        self.manage_prod_layout = MyGridLayout()

        self.pri_field_label = MyLabel(text='Primary Information')
        self.cat_field_label = MyLabel(text='Category')
        self.price_field_label = MyLabel(text='Pricing')
        self.promo_field_label = MyLabel(text='Promo')

        self.prod_barcode_label = MyLabel(text='Barcode')
        self.prod_name_label = MyLabel(text='Product Name')
        self.prod_exp_dt_label = MyLabel(text='Expire date')

        self.prod_type_label = MyLabel(text='Item type')
        self.prod_brand_label = MyLabel(text='Brand')
        self.prod_sales_group_label = MyLabel(text='Sales group')
        self.prod_supplier_label = MyLabel(text='Supplier')

        self.prod_cost_label = MyLabel(text='Cost')
        self.prod_sell_price_label = MyLabel(text='Price')
        self.prod_effective_dt_label = MyLabel(text='Effective date')
        self.prod_promo_name_label = MyLabel(text='Promo Name')
        self.prod_promo_type_label = MyLabel(text='Type')
        self.prod_promo_percent_label = MyLabel(text='Percent')
        self.prod_promo_value_label = MyLabel(text='Value')
        self.prod_promo_sell_price_label = MyLabel(text='Sell price')
        self.prod_promo_start_dt_label = MyLabel(text='Start date')
        self.prod_promo_end_dt_label = MyLabel(text='End date')

        self.prod_barcode_field = MyLineEdit(object_name='prod_barcode_field')
        self.prod_name_field = MyLineEdit(object_name='prod_name_field')
        self.prod_exp_dt_field = MyDateEdit(object_name='prod_exp_dt_field')
        self.pri_field_box = MyGroupBox()
        self.pri_field_layout = MyGridLayout()
        self.pri_field_layout.addWidget(self.pri_field_label,0,0,1,3,Qt.AlignmentFlag.AlignTop)
        self.pri_field_layout.addWidget(self.prod_barcode_label,1,0,Qt.AlignmentFlag.AlignTop)
        self.pri_field_layout.addWidget(self.prod_name_label,1,1,Qt.AlignmentFlag.AlignTop)
        self.pri_field_layout.addWidget(self.prod_exp_dt_label,1,2,Qt.AlignmentFlag.AlignTop)

        self.pri_field_layout.addWidget(self.prod_barcode_field,2,0,Qt.AlignmentFlag.AlignTop)
        self.pri_field_layout.addWidget(self.prod_name_field,2,1,Qt.AlignmentFlag.AlignTop)
        self.pri_field_layout.addWidget(self.prod_exp_dt_field,2,2,Qt.AlignmentFlag.AlignTop)
        self.pri_field_box.setLayout(self.pri_field_layout)

        self.prod_type_field = MyComboBox(object_name='prod_type_field')
        self.prod_brand_field = MyComboBox(object_name='prod_brand_field')
        self.prod_sales_group_field = MyComboBox(object_name='prod_sales_group_field')
        self.prod_supplier_field = MyComboBox(object_name='prod_supplier_field')
        self.cat_field_box = MyGroupBox()
        self.cat_field_layout = MyGridLayout()
        self.cat_field_layout.addWidget(self.cat_field_label,0,0,1,2,Qt.AlignmentFlag.AlignTop)

        self.cat_field_layout.addWidget(self.prod_type_label,1,0)
        self.cat_field_layout.addWidget(self.prod_type_field,2,0)
        self.cat_field_layout.addWidget(self.prod_brand_label,3,0)
        self.cat_field_layout.addWidget(self.prod_brand_field,4,0)

        self.cat_field_layout.addWidget(self.prod_sales_group_label,1,1)
        self.cat_field_layout.addWidget(self.prod_sales_group_field,2,1)
        self.cat_field_layout.addWidget(self.prod_supplier_label,3,1)
        self.cat_field_layout.addWidget(self.prod_supplier_field,4,1)

        self.cat_field_box.setLayout(self.cat_field_layout)

        self.prod_cost_field = MyLineEdit(object_name='prod_cost_field')
        self.prod_sell_price_field = MyLineEdit(object_name='prod_sell_price_field')
        self.prod_effective_dt_field = MyDateEdit(object_name='prod_effective_dt_field')
        self.price_field_box = MyGroupBox()
        self.price_field_layout = MyGridLayout()
        self.price_field_layout.addWidget(self.price_field_label,0,0,1,3,Qt.AlignmentFlag.AlignTop)
        self.price_field_layout.addWidget(self.prod_cost_label,1,0,Qt.AlignmentFlag.AlignTop)
        self.price_field_layout.addWidget(self.prod_sell_price_label,1,1,Qt.AlignmentFlag.AlignTop)
        self.price_field_layout.addWidget(self.prod_effective_dt_label,1,2,Qt.AlignmentFlag.AlignTop)
        
        self.price_field_layout.addWidget(self.prod_cost_field,2,0,Qt.AlignmentFlag.AlignTop)
        self.price_field_layout.addWidget(self.prod_sell_price_field,2,1,Qt.AlignmentFlag.AlignTop)
        self.price_field_layout.addWidget(self.prod_effective_dt_field,2,2,Qt.AlignmentFlag.AlignTop)
        self.price_field_box.setLayout(self.price_field_layout)

        self.default_field_box = MyGroupBox()
        self.default_field_layout = MyVBoxLayout()
        self.default_field_layout.addWidget(self.pri_field_box)
        self.default_field_layout.addWidget(self.cat_field_box)
        self.default_field_layout.addWidget(self.price_field_box)
        self.default_field_box.setLayout(self.default_field_layout)

        self.prod_promo_name_field = MyComboBox(object_name='prod_promo_name_field')
        self.prod_promo_type_field = MyLineEdit(object_name='prod_promo_type_field')
        self.prod_promo_percent_field = MyLineEdit(object_name='prod_promo_percent_field')
        self.prod_promo_value_field = MyLineEdit(object_name='prod_promo_value_field')
        self.prod_promo_sell_price_field = MyLineEdit(object_name='prod_promo_sell_price_field')
        self.prod_promo_start_dt_field = MyDateEdit(object_name='prod_promo_start_dt_field')
        self.prod_promo_end_dt_field = MyDateEdit(object_name='prod_promo_end_dt_field')
        self.promo_field_box = MyGroupBox(object_name='promo_field_box')
        self.promo_field_layout = MyGridLayout(object_name='promo_field_layout')
        self.promo_field_layout.addWidget(self.promo_field_label,0,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_name_label,1,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_name_field,2,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_type_label,3,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_type_field,4,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_percent_label,5,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_percent_field,6,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_value_label,7,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_value_field,8,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_sell_price_label,9,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_sell_price_field,10,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_start_dt_label,11,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_start_dt_field,12,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_end_dt_label,13,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_layout.addWidget(self.prod_promo_end_dt_field,14,0,Qt.AlignmentFlag.AlignTop)
        self.promo_field_box.setLayout(self.promo_field_layout)


        self.prod_form_box = MyGroupBox()
        self.prod_form_layout = MyGridLayout()
        self.prod_form_layout.addWidget(self.default_field_box,0,0,Qt.AlignmentFlag.AlignTop)
        self.prod_form_layout.addWidget(self.promo_field_box,0,1,3,1,Qt.AlignmentFlag.AlignTop)
        self.prod_form_box.setLayout(self.prod_form_layout)
        self.prod_form_scra = MyScrollArea()
        self.prod_form_scra.setWidget(self.prod_form_box)

        self.prod_tracking_field = MyCheckBox(object_name='prod_tracking_field', text='Track product inventory?')
        self.manage_prod_save_button = MyPushButton(text='Save')
        self.manage_prod_close_button = MyPushButton(text='Close')
        self.manage_prod_act_box = MyGroupBox()
        self.manage_prod_act_layout = MyHBoxLayout(object_name='prod_act_layout')
        self.manage_prod_act_layout.addWidget(self.prod_tracking_field,Qt.AlignmentFlag.AlignLeft)
        self.manage_prod_act_layout.addWidget(self.manage_prod_save_button)
        self.manage_prod_act_layout.addWidget(self.manage_prod_close_button)
        self.manage_prod_act_box.setLayout(self.manage_prod_act_layout)

        self.manage_prod_layout.addWidget(self.prod_form_scra,0,0)
        self.manage_prod_layout.addWidget(self.manage_prod_act_box,1,0)
        self.manage_prod_dialog.setLayout(self.manage_prod_layout)

        self.setup_cat_fields_disabled()
        self.setup_prod_promo_fields_hidden(hide_promo_fields=True)
        pass
    def setup_cat_fields_disabled(self, disabled=False):
        self.prod_type_field.setDisabled(disabled)
        self.prod_brand_field.setDisabled(disabled)
        self.prod_sales_group_field.setDisabled(disabled)
        self.prod_supplier_field.setDisabled(disabled)
        pass
    def setup_prod_promo_fields_hidden(self, hide_promo_fields=True, hide_prod_fields=False):
        self.prod_effective_dt_label.setHidden(hide_prod_fields)
        self.prod_effective_dt_field.setHidden(hide_prod_fields)
    
        self.prod_promo_type_label.setHidden(hide_promo_fields)
        self.prod_promo_percent_label.setHidden(hide_promo_fields)
        self.prod_promo_value_label.setHidden(hide_promo_fields)
        self.prod_promo_sell_price_label.setHidden(hide_promo_fields)
        self.prod_promo_start_dt_label.setHidden(hide_promo_fields)
        self.prod_promo_end_dt_label.setHidden(hide_promo_fields)

        self.prod_promo_type_field.setHidden(hide_promo_fields)
        self.prod_promo_percent_field.setHidden(hide_promo_fields)
        self.prod_promo_value_field.setHidden(hide_promo_fields)
        self.prod_promo_sell_price_field.setHidden(hide_promo_fields)
        self.prod_promo_start_dt_field.setHidden(hide_promo_fields)
        self.prod_promo_end_dt_field.setHidden(hide_promo_fields)
        pass
    def compute_prod_promo_price_entry(self):
        try:
            prod_sell_price = float(self.prod_sell_price_field.text())
            prod_promo_percent = float(self.prod_promo_percent_field.text())

            old_prod_sell_price = prod_sell_price
            prod_promo_value = old_prod_sell_price * (prod_promo_percent / 100)
            new_prod_sell_price = prod_sell_price - prod_promo_value

            self.prod_promo_value_field.setText(f'{prod_promo_value:.2f}')
            self.prod_promo_sell_price_field.setText(f'{new_prod_sell_price:.2f}')
            pass
        except ValueError:
            self.prod_promo_value_field.setText('Error')
            self.prod_promo_sell_price_field.setText('Error')
            pass
    def save_new_prod_entry(self):
        prod_barcode, prod_name, prod_exp_dt, prod_type, prod_brand, prod_sales_group, prod_supplier, prod_cost, prod_sell_price, prod_effective_dt, prod_promo_name, prod_promo_type, prod_promo_percent, prod_promo_value, prod_promo_sell_price, prod_promo_start_dt, prod_promo_end_dt, prod_tracking = self.get_prod_input_entry()

        schema.add_new_prod(
                prod_barcode=prod_barcode,
                prod_name=prod_name,
                prod_exp_dt=prod_exp_dt,
                prod_type=prod_type,
                prod_brand=prod_brand,
                prod_sales_group=prod_sales_group,
                prod_supplier=prod_supplier,
                prod_cost=prod_cost,
                prod_sell_price=prod_sell_price,
                prod_effective_dt=prod_effective_dt,
                prod_promo_name=prod_promo_name,

                prod_promo_type=prod_promo_type,
                prod_promo_percent=prod_promo_percent,
                prod_promo_value=prod_promo_value,
                prod_promo_sell_price=prod_promo_sell_price,
                prod_promo_start_dt=prod_promo_start_dt,
                prod_promo_end_dt=prod_promo_end_dt,
                
                prod_tracking=prod_tracking        
            ) # FIX ME

        self.manage_prod_dialog.close()
        pass

    def get_prod_input_entry(self):
        prod_barcode = self.prod_barcode_field.text()
        prod_name = self.prod_name_field.text()
        prod_exp_dt = self.prod_exp_dt_field.date().toString(Qt.DateFormat.ISODate)
        prod_type = self.prod_type_field.currentText()
        prod_brand = self.prod_brand_field.currentText()
        prod_sales_group = self.prod_sales_group_field.currentText()
        prod_supplier = self.prod_supplier_field.currentText()
        prod_cost = self.prod_cost_field.text()
        prod_sell_price = self.prod_sell_price_field.text()
        prod_effective_dt = self.prod_effective_dt_field.date().toString(Qt.DateFormat.ISODate)
        prod_promo_name = self.prod_promo_name_field.currentText()

        prod_promo_type = self.prod_promo_type_field.text()
        prod_promo_percent = self.prod_promo_percent_field.text()
        prod_promo_value = self.prod_promo_value_field.text()
        prod_promo_sell_price = self.prod_promo_sell_price_field.text()
        prod_promo_start_dt = self.prod_promo_start_dt_field.date().toString(Qt.DateFormat.ISODate)
        prod_promo_end_dt = self.prod_promo_end_dt_field.date().toString(Qt.DateFormat.ISODate)
        
        prod_tracking = self.prod_tracking_field.isChecked()
        return prod_barcode,prod_name,prod_exp_dt,prod_type,prod_brand,prod_sales_group,prod_supplier,prod_cost,prod_sell_price,prod_effective_dt,prod_promo_name,prod_promo_type,prod_promo_percent,prod_promo_value,prod_promo_sell_price,prod_promo_start_dt,prod_promo_end_dt,prod_tracking
    def save_edit_prod_entry(self):
        prod_barcode = self.prod_barcode_field.text()
        prod_name = self.prod_name_field.text()
        prod_exp_dt = self.prod_exp_dt_field.date().toString(Qt.DateFormat.ISODate)
        prod_type = self.prod_type_field.currentText()
        prod_brand = self.prod_brand_field.currentText()
        prod_sales_group = self.prod_sales_group_field.currentText()
        prod_supplier = self.prod_supplier_field.currentText()
        prod_cost = self.prod_cost_field.text()
        prod_sell_price = self.prod_sell_price_field.text()
        prod_effective_dt = self.prod_effective_dt_field.date().toString(Qt.DateFormat.ISODate)
        prod_promo_name = self.prod_promo_name_field.currentText()

        prod_promo_type = self.prod_promo_type_field.text()
        prod_promo_percent = self.prod_promo_percent_field.text()
        prod_promo_value = self.prod_promo_value_field.text()
        prod_promo_sell_price = self.prod_promo_sell_price_field.text()
        prod_promo_start_dt = self.prod_promo_start_dt_field.date().toString(Qt.DateFormat.ISODate)
        prod_promo_end_dt = self.prod_promo_end_dt_field.date().toString(Qt.DateFormat.ISODate)
        
        prod_tracking = self.prod_tracking_field.isChecked()

        prod_item_id = self.sel_prod_item_id_value
        prod_price_id = self.sel_prod_price_id_value
        prod_promo_id = self.sel_prod_promo_id_value
        prod_stock_id = self.sel_prod_stock_id_value

        schema.edit_selected_prod(
                prod_barcode=prod_barcode,
                prod_name=prod_name,
                prod_exp_dt=prod_exp_dt,
                prod_type=prod_type,
                prod_brand=prod_brand,
                prod_sales_group=prod_sales_group,
                prod_supplier=prod_supplier,
                prod_cost=prod_cost,
                prod_sell_price=prod_sell_price,
                prod_effective_dt=prod_effective_dt,
                prod_promo_name=prod_promo_name,
                prod_promo_type=prod_promo_type,
                prod_promo_percent=prod_promo_percent,
                prod_promo_value=prod_promo_value,
                prod_promo_sell_price=prod_promo_sell_price,
                prod_promo_start_dt=prod_promo_start_dt,
                prod_promo_end_dt=prod_promo_end_dt,
                prod_tracking=prod_tracking,
                prod_item_id=prod_item_id,
                prod_price_id=prod_price_id,
                prod_promo_id=prod_promo_id,
                prod_stock_id=prod_stock_id
            )

        self.sel_prod_id_value = 0
        self.manage_prod_dialog.close()
        pass
    
    def setup_view_prod_panel(self):
        self.view_dialog = MyDialog(window_title=f"{self.sel_prod_name_value}")
        self.view_layout = MyGridLayout()

        self.prod_barcode_info_label = MyLabel(text=f"{self.sel_prod_barcode_value}")
        self.prod_name_info_label = MyLabel(text=f"{self.sel_prod_name_value}")
        self.prod_exp_dt_info_label = MyLabel(text=f"{self.sel_prod_exp_dt_value}")
        self.prod_type_info_label = MyLabel(text=f"{self.sel_prod_type_value}")
        self.prod_brand_info_label = MyLabel(text=f"{self.sel_prod_brand_value}")
        self.prod_sales_group_info_label = MyLabel(text=f"{self.sel_prod_sales_group_value}")
        self.prod_supplier_info_label = MyLabel(text=f"{self.sel_prod_supplier_value}")
        self.prod_cost_info_label = MyLabel(text=f"{self.sel_prod_cost_value}")
        self.prod_sell_price_info_label = MyLabel(text=f"{self.sel_prod_sell_price_value}")
        self.prod_effective_dt_info_label = MyLabel(text=f"{self.sel_prod_effective_dt_value}")
        self.prod_promo_name_info_label = MyLabel(text=f"{self.sel_prod_promo_name_value}")
        self.prod_promo_value_info_label = MyLabel(text=f"{self.sel_prod_promo_value_value}")
        self.prod_tracking_info_label = MyLabel(text=f"{self.sel_prod_tracking_value}")

        self.datetime_created_info_label = MyLabel(text=f"{self.sel_datetime_created_value}")

        self.view_form_box = MyGroupBox()
        self.view_form_layout = MyFormLayout()
        self.view_form_layout.addRow('Barcode:', self.prod_barcode_info_label)
        self.view_form_layout.addRow('Product Name:', self.prod_name_info_label)
        self.view_form_layout.addRow('Expire date:', self.prod_exp_dt_info_label)
        self.view_form_layout.addRow(MyLabel(text='<hr>'))
        self.view_form_layout.addRow('Item type:', self.prod_type_info_label)
        self.view_form_layout.addRow('Brand:', self.prod_brand_info_label)
        self.view_form_layout.addRow('Sales group:', self.prod_sales_group_info_label)
        self.view_form_layout.addRow(MyLabel(text='<hr>'))
        self.view_form_layout.addRow('Supplier:', self.prod_supplier_info_label)
        self.view_form_layout.addRow('Cost:', self.prod_cost_info_label)
        self.view_form_layout.addRow('Price:', self.prod_sell_price_info_label)
        self.view_form_layout.addRow('Effective date:', self.prod_effective_dt_info_label)
        self.view_form_layout.addRow('Promo Name:', self.prod_promo_name_info_label)
        self.view_form_layout.addRow('Value:', self.prod_promo_value_info_label)
        self.view_form_layout.addRow(MyLabel(text='<hr>'))
        self.view_form_layout.addRow('Inventory tracking:', self.prod_tracking_info_label)
        self.view_form_layout.addRow('Date/Time created:', self.datetime_created_info_label)
        self.view_form_box.setLayout(self.view_form_layout)
        self.view_form_scra = MyScrollArea()
        self.view_form_scra.setWidget(self.view_form_box)

        self.view_form_close_button = MyPushButton(text='Close')

        self.view_layout.addWidget(self.view_form_scra,0,0)
        self.view_layout.addWidget(self.view_form_close_button,1,0,Qt.AlignmentFlag.AlignRight)
        self.view_dialog.setLayout(self.view_layout)
    # endregion: endprod

    # region: stock
    def setup_stock_list_tab_panel(self):
        self.stock_list_table = MyTableWidget(object_name='stock_list_table')
        self.stock_list_prev_button = MyPushButton(text='Prev')
        self.stock_list_page_label = MyLabel(text=f"Page {self.stock_page_number}/{self.stock_total_page_number}")
        self.stock_list_next_button = MyPushButton(text='Next')
        self.stock_list_pag_box = MyGroupBox()
        self.stock_list_pag_layout = MyHBoxLayout(object_name='stock_list_pag_layout')
        self.stock_list_pag_layout.addWidget(self.stock_list_prev_button)
        self.stock_list_pag_layout.addWidget(self.stock_list_page_label)
        self.stock_list_pag_layout.addWidget(self.stock_list_next_button)
        self.stock_list_pag_box.setLayout(self.stock_list_pag_layout)
        self.stock_list_box = MyGroupBox()
        self.stock_list_layout = MyGridLayout()
        self.stock_list_layout.addWidget(self.stock_list_table,0,0)
        self.stock_list_layout.addWidget(self.stock_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.stock_list_box.setLayout(self.stock_list_layout)
        pass
    def init_stock_list_page_entry(self): # TODO: PENDING...
        self.stock_page_number = 1
        self.stock_total_page_number = schema.count_stock_list_total_pages()
    def init_selected_stock_data_entry(self):
        self.sel_stock_name_value = None
        self.sel_stock_available_value = None
        self.sel_stock_on_hand_value = None
        pass
    def assign_selected_stock_data_entry(self, value):
        self.sel_stock_name_value = str(value[0])
        self.sel_stock_available_value = str(value[1])
        self.sel_stock_on_hand_value = str(value[2])
        self.sel_datetime_created_value = str(value[3])
        self.sel_stock_item_id_value = value[4]
        self.sel_stock_id_value = value[5]
        pass
    def setup_manage_stock_panel(self, window_title):
        self.manage_stock_dialog = MyDialog(window_title=window_title)
        self.manage_stock_layout = MyGridLayout()

        self.stock_available_label = MyLabel(text='Available')
        self.stock_on_hand_label = MyLabel(text='On hand')
        self.stock_available_field = MyLineEdit(object_name='Available')
        self.stock_on_hand_field = MyLineEdit(object_name='On hand')
        self.stock_form_box = MyGroupBox()
        self.stock_form_layout = MyFormLayout()
        self.stock_form_layout.addRow(self.stock_available_label)
        self.stock_form_layout.addRow(self.stock_available_field)
        self.stock_form_layout.addRow(self.stock_on_hand_label)
        self.stock_form_layout.addRow(self.stock_on_hand_field)
        self.stock_form_box.setLayout(self.stock_form_layout)
        self.stock_form_scra = MyScrollArea()
        self.stock_form_scra.setWidget(self.stock_form_box)

        self.manage_stock_save_button = MyPushButton(text='Save')
        self.manage_stock_close_button = MyPushButton(text='Close')
        self.manage_stock_act_box = MyGroupBox()
        self.manage_stock_act_layout = MyHBoxLayout(object_name='stock_act_layout')
        self.manage_stock_act_layout.addWidget(self.manage_stock_save_button)
        self.manage_stock_act_layout.addWidget(self.manage_stock_close_button)
        self.manage_stock_act_box.setLayout(self.manage_stock_act_layout)

        self.manage_stock_layout.addWidget(self.stock_form_scra,0,0)
        self.manage_stock_layout.addWidget(self.manage_stock_act_box,1,0,Qt.AlignmentFlag.AlignRight)
        self.manage_stock_dialog.setLayout(self.manage_stock_layout)
        pass
    # endregion: stock


    pass
class MyProdView(MyGroupBox): # NOTE: layout
    def __init__(self, model: MyProdModel):
        super().__init__()

        self.model = model

        self.setup_main_panel()

    def setup_main_panel(self):
        self.setup_panel_a()
        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.panel_a_box,0,0)
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
        self.import_prod_button = MyPushButton(text='Import')
        self.add_prod_button = MyPushButton(text='Add')
        self.interactive_act_box = MyGroupBox()
        self.interactive_act_layout = MyHBoxLayout()
        self.interactive_act_layout.addWidget(self.sync_ui_button)
        self.interactive_act_layout.addWidget(self.import_prod_button)
        self.interactive_act_layout.addWidget(self.add_prod_button)
        self.interactive_act_box.setLayout(self.interactive_act_layout)

        self.model.setup_prod_list_tab_panel()
        self.model.setup_stock_list_tab_panel()
        self.prod_list_tab = MyTabWidget()
        self.prod_list_tab.addTab(self.model.prod_list_box, 'Overview')
        self.prod_list_tab.addTab(self.model.stock_list_box, 'Inventory')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.interactive_act_box,0,1)
        self.panel_a_layout.addWidget(self.prod_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass

    pass 
class MyProdController: # NOTE: connections, setting attributes
    def __init__(self, model: MyProdModel, view: MyProdView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_prod_list_table()
        self.populate_stock_list_table()

    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.view.import_prod_button.clicked.connect(self.on_import_prod_button_clicked)
        self.view.add_prod_button.clicked.connect(self.on_add_prod_button_clicked)
        self.model.prod_list_prev_button.clicked.connect(lambda: self.on_prod_list_pag_button_clicked(action='go_prev'))
        self.model.prod_list_next_button.clicked.connect(lambda: self.on_prod_list_pag_button_clicked(action='go_next'))
        pass

    def on_text_filter_button_clicked(self):
        self.model.page_number = 1
        self.model.stock_page_number = 1
        self.model.prod_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.model.stock_list_page_label.setText(f"Page {self.model.stock_page_number}/{self.model.stock_total_page_number}")

        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number) 
        self.populate_stock_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.stock_page_number)
        pass
    def on_sync_ui_button_clicked(self):
        self.model.init_prod_list_page_entry()
        self.model.prod_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.model.stock_list_page_label.setText(f"Page {self.model.page_number}/{self.model.stock_total_page_number}")

        self.populate_prod_list_table()
        self.populate_stock_list_table()

        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass
    
    def on_import_prod_button_clicked(self):
        print('PASSED')
        try:
            self.prod_csv_file, _ = QFileDialog.getOpenFileName(self.view, 'Open CSV', qss.csv_file_path, 'CSV File (*.csv)')
            self.prod_csv_df = pd.read_csv(self.prod_csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

            if self.prod_csv_file:
                print('PASSED')
                self.model.prog_total_data_value = len(self.prod_csv_df)
                self.model.prog_remaining_data_value = len(self.prod_csv_df)

                self.model.setup_progress_panel(window_title=f"{'percentage'}", progress_type='prod_import')
                self.model.import_prod_entry(data_frame=self.prod_csv_df)
                self.setup_prod_import_thread_conn()
                self.model.progress_dialog.exec()

                if self.model.prog_remaining_data_value > 0 and self.model.progress_dialog.close():
                    self.model.prod_import_thread.stop()

                    print('PASSED')
                    self.model.init_progress_data_entry()

                    QMessageBox.critical(self.view, 'Cancelled', 'Import has been cancelled')
                    self.on_sync_ui_button_clicked()

            pass
        except Exception as e:
            self.prod_csv_file = ''
        pass
    def setup_prod_import_thread_conn(self):
        self.model.prod_import_thread.update_signal.connect(self.on_prod_import_thread_update_signal)
        self.model.prod_import_thread.finished_signal.connect(self.on_prod_import_thread_finished_signal)
        self.model.prod_import_thread.invalid_signal.connect(self.on_prod_import_thread_invalid_signal)
        pass
    def on_prod_import_thread_update_signal(self):
        try:
            self.model.prog_data_count_value += 1
            self.model.prog_remaining_data_value -= 1
            progress_percent_value = int((self.model.prog_data_count_value / self.model.prog_total_data_value) * 100)

            self.model.progress_dialog.setWindowTitle(f"{progress_percent_value}% complete")
            self.model.progress_label.setText(f"Please wait...({self.model.prog_remaining_data_value})")
            self.model.progress_bar.setValue(progress_percent_value)

            print('PASSED')

            pass
        except Exception as e:
            self.model.init_progress_data_entry()
        pass
    def on_prod_import_thread_finished_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.information(self.view, 'Success', 'All prod has been imported')
        self.on_sync_ui_button_clicked()
        pass
    def on_prod_import_thread_invalid_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.critical(self.view, 'Error', 'Invalid CSV file.')
        self.on_sync_ui_button_clicked()
        pass

    def on_add_prod_button_clicked(self):  
        self.model.setup_manage_prod_panel(window_title='Add product')
        self.populate_manage_prod_combo_box_field()
        self.setup_manage_prod_panel_conn(conn_type='add_prod')

        self.model.manage_prod_dialog.exec()
        pass

    # region: prod_list
    def populate_prod_list_table(self, text_filter='', page_number=1):
        prod_list = schema.list_all_prod_col(text_filter=text_filter, page_number=page_number)

        self.model.prod_list_page_label.setText(f"Page {page_number}/{self.model.total_page_number}")

        self.model.prod_list_prev_button.setEnabled(page_number > 1)
        self.model.prod_list_next_button.setEnabled(len(prod_list) == 30)

        self.model.prod_list_table.setRowCount(len(prod_list))

        for prod_list_i, prod_list_v in enumerate(prod_list):
            self.edit_prod_button = MyPushButton(text='Edit')
            self.view_prod_button = MyPushButton(text='View')
            self.delete_prod_button = MyPushButton(text='Delete')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.edit_prod_button)
            table_act_laoyut.addWidget(self.view_prod_button)
            table_act_laoyut.addWidget(self.delete_prod_button)
            table_act_panel.setLayout(table_act_laoyut)

            self.highlight = False
            if prod_list_v[16] != 0:
                self.highlight = True
                self.edit_prod_button.hide()

            if QDate.fromString(prod_list_v[9], Qt.DateFormat.ISODate) <= QDate.currentDate():
                self.delete_prod_button.hide()

            prod_barcode = MyTableWidgetItem(text=f"{prod_list_v[0]}", has_promo=self.highlight)
            prod_name = MyTableWidgetItem(text=f"{prod_list_v[1]}", has_promo=self.highlight)
            prod_exp_dt = MyTableWidgetItem(text=f"{prod_list_v[2]}", has_promo=self.highlight)
            prod_type = MyTableWidgetItem(text=f"{prod_list_v[3]}", has_promo=self.highlight)
            prod_brand = MyTableWidgetItem(text=f"{prod_list_v[4]}", has_promo=self.highlight)
            prod_sales_group = MyTableWidgetItem(text=f"{prod_list_v[5]}", has_promo=self.highlight)
            prod_supplier = MyTableWidgetItem(text=f"{prod_list_v[6]}", has_promo=self.highlight)
            prod_cost = MyTableWidgetItem(text=f"{prod_list_v[7]}", has_promo=self.highlight)
            prod_sell_price = MyTableWidgetItem(text=f"{prod_list_v[8]}", has_promo=self.highlight)
            prod_effective_dt = MyTableWidgetItem(text=f"{prod_list_v[9]}", has_promo=self.highlight)
            prod_promo_name = MyTableWidgetItem(text=f"{prod_list_v[10]}", has_promo=self.highlight)
            prod_promo_value = MyTableWidgetItem(text=f"{prod_list_v[11]}", has_promo=self.highlight)
            prod_tracking = MyTableWidgetItem(text=f"{prod_list_v[12]}", has_promo=self.highlight)
            datetime_created = MyTableWidgetItem(text=f"{prod_list_v[13]}", has_promo=self.highlight)

            self.model.prod_list_table.setCellWidget(prod_list_i, 0, table_act_panel)
            self.model.prod_list_table.setItem(prod_list_i, 1, prod_barcode)
            self.model.prod_list_table.setItem(prod_list_i, 2, prod_name)
            self.model.prod_list_table.setItem(prod_list_i, 3, prod_exp_dt)
            self.model.prod_list_table.setItem(prod_list_i, 4, prod_type)
            self.model.prod_list_table.setItem(prod_list_i, 5, prod_brand)
            self.model.prod_list_table.setItem(prod_list_i, 6, prod_sales_group)
            self.model.prod_list_table.setItem(prod_list_i, 7, prod_supplier)
            self.model.prod_list_table.setItem(prod_list_i, 8, prod_cost)
            self.model.prod_list_table.setItem(prod_list_i, 9, prod_sell_price)
            self.model.prod_list_table.setItem(prod_list_i, 10, prod_effective_dt)
            self.model.prod_list_table.setItem(prod_list_i, 11, prod_promo_name)
            self.model.prod_list_table.setItem(prod_list_i, 12, prod_promo_value)
            self.model.prod_list_table.setItem(prod_list_i, 13, prod_tracking)
            self.model.prod_list_table.setItem(prod_list_i, 14, datetime_created)


            self.setup_prod_list_table_act_panel_conn(value=prod_list_v)
            pass
        pass
    def setup_prod_list_table_act_panel_conn(self, value):
        self.edit_prod_button.clicked.connect(lambda _, value=value: self.on_edit_prod_button_clicked(value))
        self.view_prod_button.clicked.connect(lambda _, value=value: self.on_view_prod_button_clicked(value))
        self.delete_prod_button.clicked.connect(lambda _, value=value: self.on_delete_prod_button_clicked(value))
        pass
    def on_prod_list_pag_button_clicked(self, action):
        print('prod_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.page_number > 1:
                self.model.page_number -= 1
                self.model.prod_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        elif action == 'go_next':
            self.model.page_number += 1
            self.model.prod_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        pass

    def on_edit_prod_button_clicked(self, value):
        self.model.assign_selected_prod_data_entry(value)
        self.model.setup_manage_prod_panel(window_title=f"Edit {self.model.sel_prod_name_value}")
        self.model.setup_cat_fields_disabled(True)
        self.populate_manage_prod_combo_box_field()

        self.model.prod_barcode_field.setText(self.model.sel_prod_barcode_value)
        self.model.prod_name_field.setText(self.model.sel_prod_name_value)
        self.model.prod_exp_dt_field.setDate(QDate.fromString(self.model.sel_prod_exp_dt_value, Qt.DateFormat.ISODate))
        self.model.prod_type_field.setCurrentText(self.model.sel_prod_type_value)
        self.model.prod_brand_field.setCurrentText(self.model.sel_prod_brand_value)
        self.model.prod_sales_group_field.setCurrentText(self.model.sel_prod_sales_group_value)
        self.model.prod_supplier_field.setCurrentText(self.model.sel_prod_supplier_value)
        self.model.prod_cost_field.setText(self.model.sel_prod_cost_value)
        self.model.prod_sell_price_field.setText(self.model.sel_prod_sell_price_value)
        self.model.prod_effective_dt_field.setDate(QDate.fromString(self.model.sel_prod_effective_dt_value, Qt.DateFormat.ISODate))
        self.model.prod_promo_name_field.setCurrentText(self.model.sel_prod_promo_name_value)

        self.model.prod_tracking_field.setChecked(self.model.sel_prod_tracking_bool_value)

        self.setup_manage_prod_panel_conn(conn_type='edit_prod')

        self.model.manage_prod_dialog.exec()
        pass
    def setup_manage_prod_panel_conn(self, conn_type):
        self.model.prod_sell_price_field.textChanged.connect(self.on_prod_sell_price_field_text_changed)
        self.model.prod_promo_name_field.currentIndexChanged.connect(self.on_prod_promo_name_field_current_text_changed)

        self.model.manage_prod_save_button.clicked.connect(lambda: self.on_manage_prod_save_button_clicked(action=conn_type))
        self.model.manage_prod_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.manage_prod_dialog))
        pass
    def populate_manage_prod_combo_box_field(self):
        self.model.prod_type_field.clear()
        self.model.prod_brand_field.clear()
        self.model.prod_supplier_field.clear()
        self.model.prod_promo_name_field.clear()

        item_type_data = schema.list_item_type_col()
        brand_data = schema.list_brand_col()
        supplier_data = schema.list_supplier_col()
        promo_name_data = schema.list_promo_name_col()

        self.model.prod_sales_group_field.addItem('Retail')
        self.model.prod_sales_group_field.addItem('Wholesale')

        for item_type in item_type_data: self.model.prod_type_field.addItems(item_type)
        for brand in brand_data: self.model.prod_brand_field.addItems(brand)
        for supplier in supplier_data: self.model.prod_supplier_field.addItems(supplier)

        self.model.prod_promo_name_field.addItem('No promo')
        for promo_name in promo_name_data: self.model.prod_promo_name_field.addItems(promo_name)

        pass
    def on_prod_promo_name_field_current_text_changed(self):
        self.model.setup_prod_promo_fields_hidden(hide_promo_fields=True, hide_prod_fields=False) if self.model.prod_promo_name_field.currentText() == 'No promo' else self.model.setup_prod_promo_fields_hidden(hide_promo_fields=False, hide_prod_fields=True)
        
        try: 
            promo_type = schema.list_promo_type_col(self.model.prod_promo_name_field.currentText())
            promo_percent = schema.list_promo_percent_col(self.model.prod_promo_name_field.currentText())

            self.model.prod_promo_type_field.setText(str(promo_type))
            self.model.prod_promo_percent_field.setText(str(promo_percent))

            self.model.compute_prod_promo_price_entry()
        except Exception as e:
            promo_type = ''
            promo_percent = 0
        pass
    def on_prod_sell_price_field_text_changed(self):
        print(self.model.prod_sell_price_field.text())
        self.model.compute_prod_promo_price_entry()
            
        print('working')

    def on_view_prod_button_clicked(self, value):
        self.model.assign_selected_prod_data_entry(value)

        self.model.setup_view_prod_panel()

        self.setup_view_prod_conn()

        self.model.view_dialog.exec()
        pass
    def setup_view_prod_conn(self):
        self.model.view_form_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.view_dialog))
    
    def on_delete_prod_button_clicked(self, value):
        self.model.assign_selected_prod_data_entry(value)

        confirm = QMessageBox.warning(self.view, 'Confirm', f"Delete {self.model.sel_prod_name_value}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_prod(prod_price_id=self.model.sel_prod_price_id_value)

            self.model.init_selected_prod_data_entry()

            QMessageBox.information(self.model.manage_prod_dialog, 'Success', 'Product has been deleted.')

            self.on_sync_ui_button_clicked()
            pass
        else:
            self.model.init_selected_prod_data_entry()
            return
        pass
    
    def on_manage_prod_save_button_clicked(self, action):
        prod_barcode, prod_name, prod_exp_dt, prod_type, prod_brand, prod_sales_group, prod_supplier, prod_cost, prod_sell_price, prod_effective_dt, prod_promo_name, prod_promo_type, prod_promo_percent, prod_promo_value, prod_promo_sell_price, prod_promo_start_dt, prod_promo_end_dt, prod_tracking = self.model.get_prod_input_entry()


        if '' not in [prod_name, prod_brand, prod_sales_group, prod_supplier, prod_cost, prod_sell_price, prod_effective_dt]:
            if (prod_cost.replace('.', '', 1).isdigit() and prod_sell_price.replace('.', '', 1).isdigit()):
                if action == 'add_prod':
                    self.model.save_new_prod_entry()
                    self.model.init_selected_prod_data_entry()

                    QMessageBox.information(self.model.manage_prod_dialog, 'Success', 'New prod has been added.')
                    pass
                elif action == 'edit_prod':
                    self.model.save_edit_prod_entry()
                    self.model.init_selected_prod_data_entry()

                    QMessageBox.information(self.model.manage_prod_dialog, 'Success', 'Product has been edited.')
                    pass
                self.on_sync_ui_button_clicked()
                pass
            else:
                QMessageBox.critical(self.model.manage_prod_dialog, 'Error', 'Invalid numerical input.')
                pass
        else:
            self.set_label_required_field_indicator(prod_name, prod_brand, prod_sales_group, prod_supplier, prod_cost, prod_sell_price, prod_effective_dt)

            QMessageBox.critical(self.model.manage_prod_dialog, 'Error', 'Please fill out the required field.')
            pass
        pass
    def set_label_required_field_indicator(
        self,
        prod_name,
        prod_brand,
        prod_sales_group,
        prod_supplier,
        prod_cost,
        prod_sell_price,
        prod_effective_dt,
    ):
        self.model.prod_name_label.setText(f"Name {qss.required_label}") if prod_name == '' else self.model.prod_name_label.setText(f"Name")
        self.model.prod_brand_label.setText(f"Brand {qss.required_label}") if prod_brand == '' else self.model.prod_brand_label.setText(f"Brand")
        self.model.prod_sales_group_label.setText(f"Sales group {qss.required_label}") if prod_sales_group == '' else self.model.prod_sales_group_label.setText(f"Sales group")
        self.model.prod_supplier_label.setText(f"Supplier {qss.required_label}") if prod_supplier == '' else self.model.prod_supplier_label.setText(f"Supplier")
        self.model.prod_cost_label.setText(f"Cost {qss.required_label}") if prod_cost == '' else self.model.prod_cost_label.setText(f"Cost")
        self.model.prod_sell_price_label.setText(f"Sell price {qss.required_label}") if prod_sell_price == '' else self.model.prod_sell_price_label.setText(f"Sell price")
        self.model.prod_effective_dt_label.setText(f"Effective date {qss.required_label}") if prod_effective_dt == '' else self.model.prod_effective_dt_label.setText(f"Effective date")
    # endregion

    # region: stock_list
    def populate_stock_list_table(self, text_filter='', page_number=1):
        stock_list = schema.list_all_stock_col(text_filter=text_filter, page_number=page_number)

        self.model.stock_list_page_label.setText(f"Page {page_number}/{self.model.stock_total_page_number}")

        self.model.stock_list_prev_button.setEnabled(page_number > 1)
        self.model.stock_list_next_button.setEnabled(len(stock_list) == 30)

        self.model.stock_list_table.setRowCount(len(stock_list))

        for stock_list_i, stock_list_v in enumerate(stock_list):
            self.edit_stock_button = MyPushButton(text='Edit')
            self.delete_stock_button = MyPushButton(text='Stop')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.edit_stock_button)
            table_act_laoyut.addWidget(self.delete_stock_button)
            table_act_panel.setLayout(table_act_laoyut)

            stock_name = MyTableWidgetItem(text=f"{stock_list_v[0]}", has_promo=self.highlight)
            stock_available = MyTableWidgetItem(text=f"{stock_list_v[1]}", has_promo=self.highlight)
            stock_on_hand = MyTableWidgetItem(text=f"{stock_list_v[2]}", has_promo=self.highlight)
            datetime_created = MyTableWidgetItem(text=f"{stock_list_v[3]}", has_promo=self.highlight)

            self.model.stock_list_table.setCellWidget(stock_list_i, 0, table_act_panel)
            self.model.stock_list_table.setItem(stock_list_i, 1, stock_name)
            self.model.stock_list_table.setItem(stock_list_i, 2, stock_available)
            self.model.stock_list_table.setItem(stock_list_i, 3, stock_on_hand)
            self.model.stock_list_table.setItem(stock_list_i, 4, datetime_created)

            self.setup_stock_list_table_act_panel_conn(value=stock_list_v)
            pass
        pass
    def setup_stock_list_table_act_panel_conn(self, value):
        self.edit_stock_button.clicked.connect(lambda _, value=value: self.on_edit_stock_button_clicked(value))
        self.delete_stock_button.clicked.connect(lambda _, value=value: self.on_delete_stock_button_clicked(value))
        pass
    def on_stock_list_pag_button_clicked(self, action):
        print('stock_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.stock_page_number > 1:
                self.model.stock_page_number -= 1
                self.model.stock_list_page_label.setText(f"Page {self.model.stock_page_number}/{self.model.stock_total_page_number}")

            self.populate_stock_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.stock_page_number)
            pass
        elif action == 'go_next':
            self.model.stock_page_number += 1
            self.model.stock_list_page_label.setText(f"Page {self.model.stock_page_number}/{self.model.stock_total_page_number}")

            self.populate_stock_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.stock_page_number)
            pass
        pass

    def on_edit_stock_button_clicked(self, value):
        self.model.assign_selected_stock_data_entry(value)
        self.model.setup_manage_stock_panel(window_title=f"Edit {self.model.sel_stock_name_value}")
        
        self.model.stock_available_field.setText(self.model.sel_stock_available_value)
        self.model.stock_on_hand_field.setText(self.model.sel_stock_on_hand_value)

        self.setup_manage_stock_panel_conn(conn_type='edit_stock')

        self.model.manage_stock_dialog.exec()

        pass
    def on_delete_stock_button_clicked(self, value):
        self.model.assign_selected_stock_data_entry(value)

        confirm = QMessageBox.warning(self.view, 'Confirm', f"Stop tracking {self.model.sel_stock_name_value}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_stock(stock_id=self.model.sel_stock_id_value)

            self.model.init_selected_stock_data_entry()

            QMessageBox.information(self.model.manage_stock_dialog, 'Success', 'Stock has been stopped.')

            self.on_sync_ui_button_clicked()
            pass
        else:
            self.model.init_selected_stock_data_entry()
            return
        pass
    def setup_manage_stock_panel_conn(self, conn_type):
        self.model.manage_stock_save_button.clicked.connect(lambda: self.on_manage_stock_save_button_clicked(action=conn_type))
        self.model.manage_stock_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.manage_stock_dialog))
        pass

    def on_manage_stock_save_button_clicked(self, action):
        stock_available = self.model.stock_available_field.text()
        stock_on_hand = self.model.stock_on_hand_field.text()
        stock_id = self.model.sel_stock_id_value

        if '' not in [stock_available, stock_on_hand]:
            if (stock_available.replace('.', '', 1).isdigit() and stock_on_hand.replace('.', '', 1).isdigit()):
                if action == 'edit_stock':
                    schema.edit_selected_stock(stock_available, stock_on_hand, stock_id)
                    self.model.init_selected_stock_data_entry()

                    QMessageBox.information(self.model.manage_prod_dialog, 'Success', 'Product has been edited.')
                    pass
                self.on_sync_ui_button_clicked()
                pass
            else:
                QMessageBox.critical(self.model.manage_stock_dialog, 'Error', 'Invalid numerical input.')
                pass
        else:
            QMessageBox.critical(self.model.manage_stock_dialog, 'Error', 'Please fill out the required field.')
            pass
        pass
    
    # endregion
    
    def on_close_button_clicked(self, widget: QWidget):
        widget.close()

        self.model.init_selected_prod_data_entry()
        pass

    pass

class MyProdWindow(MyGroupBox):
    def __init__(self, name): # NOTE: 'name' param is for the current user (cashier, admin, dev) name
        super().__init__(object_name='MyProdWindow')

        self.model = MyProdModel(name=name)
        self.view = MyProdView(self.model)
        self.controller = MyProdController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.show()


# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    prod_window = MyProdWindow(name='test-name')

    prod_window.run()
    app.exec()