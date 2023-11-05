
import sys, os
from datetime import *
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from src.gui.widget.my_widget import *
from src.core.csv_to_db_importer import MyDataImportThread
from src.core.sql.admin.product import MyProductSchema
from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()
schema = MyProductSchema()

class MyProductModel:
    def __init__(self, name, phone):
        self.user_name = name
        self.user_phone = phone

        self.total_product_page_number = schema.select_product_data_total_page_count()
        self.total_stock_page_number = schema.select_stock_data_total_page_count()
        self.page_number = 1 if self.total_product_page_number > 0 or self.total_stock_page_number > 0 else 0

        self.sel_product_id = 0
        self.sel_product_price_id = 0
        self.sel_product_stock_id = 0
        self.sel_product_promo_id = 0

    def set_import_data_entry(self, csv_file_path):
        self.progress_count = 0
        self.progress_percent = 100

        self.data_import_thread = MyDataImportThread(data_name='product', csv_file_path=csv_file_path)

        self.data_import_thread.start()
    
    def init_manage_product_data_entry(
            self, 
            dialog, 
            task, 
            product_name_label, 
            product_brand_label, 
            product_sales_group_label, 
            product_supplier_label, 
            product_cost_label, 
            product_price_label, 
            product_effective_dt_label, 
            
            product_barcode, 
            product_name, 
            product_expire_dt, 

            product_type, 
            product_brand, 
            product_sales_group, 
            product_supplier, 

            product_cost, 
            product_retail_price, # FIXME: HERE
            product_wholesale_price, # FIXME: HERE
            product_price, 
            product_effective_dt, 
            product_promo_name, 
            product_promo_type, 
            product_promo_percent, 
            product_disc_value, 
            product_new_price, 
            product_start_dt, 
            product_end_dt,

            product_stock_tracking=False,
    ):
        if '' not in [
            product_name,
            product_brand,
            product_sales_group,
            product_supplier,
            product_cost,
            product_price,
            product_effective_dt,
        ]:
            if (product_cost.replace('.', '', 1).isdigit() and product_price.replace('.', '', 1).isdigit()):
                product_name_label.setText(f"Name")
                product_brand_label.setText(f"Brand")
                product_sales_group_label.setText(f"Sales group")
                product_supplier_label.setText(f"Supplier")
                product_cost_label.setText(f"Cost")
                product_price_label.setText(f"Price")
                product_effective_dt_label.setText(f"Effective date")

                if task == 'add_data':
                    schema.insert_product_data(
                        product_barcode,
                        product_name,
                        product_expire_dt,

                        product_type,
                        product_brand,
                        product_sales_group,
                        product_supplier,

                        product_cost,
                        product_price,
                        product_effective_dt,
                        product_promo_name,
                        product_promo_type,
                        product_disc_value,
                        product_promo_percent,
                        product_new_price,
                        product_start_dt,
                        product_end_dt,

                        product_stock_tracking,
                    )
                    QMessageBox.information(dialog, 'Success', 'Product added.')
                    dialog.close()
                    pass
                elif task == 'edit_data':
                    schema.update_product_data(
                        product_barcode,
                        product_name,
                        product_expire_dt,

                        product_type,
                        product_brand,
                        product_sales_group,
                        product_supplier,

                        product_cost,
                        product_price,
                        product_effective_dt,
                        product_promo_name,
                        product_promo_type,
                        product_disc_value,
                        product_promo_percent,
                        product_new_price,
                        product_start_dt,
                        product_end_dt,

                        product_stock_tracking,

                        self.sel_product_id,
                        self.sel_product_price_id,
                        self.sel_product_stock_id,
                        self.sel_product_promo_id
                    )
                    QMessageBox.information(dialog, 'Success', 'Product edited.')
                    dialog.close()
                    self.sel_product_id = 0
                    self.sel_product_price_id = 0
                    self.sel_product_stock_id = 0
                    self.sel_product_promo_id = 0
                    pass
                else:
                    QMessageBox.critical(dialog, 'Error', 'Invalid phone number.')
            else:
                product_name_label.setText(f"Name")
                product_brand_label.setText(f"Brand")
                product_sales_group_label.setText(f"Sales group")
                product_supplier_label.setText(f"Supplier")
                product_cost_label.setText(f"Cost {qss.inv_field_indicator}") if product_cost.replace('.', '', 1).isdigit() is False else product_cost_label.setText(f"Cost")
                product_price_label.setText(f"Price {qss.inv_field_indicator}") if product_price.replace('.', '', 1).isdigit() is False else product_price_label.setText(f"Price")
                product_effective_dt_label.setText(f"Effective date")

                QMessageBox.critical(dialog, 'Error', 'Invalid numeric value.')
        else:
            product_name_label.setText(f"Name {qss.req_field_indicator}") if product_name == '' else product_name_label.setText(f"Name")
            product_brand_label.setText(f"Brand {qss.req_field_indicator}") if product_brand == '' else product_brand_label.setText(f"Brand")
            product_sales_group_label.setText(f"Sales group {qss.req_field_indicator}") if product_sales_group == '' else product_sales_group_label.setText(f"Sales group")
            product_supplier_label.setText(f"Supplier {qss.req_field_indicator}") if product_supplier == '' else product_supplier_label.setText(f"Supplier")
            product_cost_label.setText(f"Cost {qss.inv_field_indicator}") if product_cost.replace('.', '', 1).isdigit() is False else product_cost_label.setText(f"Cost")
            product_price_label.setText(f"Price {qss.inv_field_indicator}") if product_price.replace('.', '', 1).isdigit() is False else product_price_label.setText(f"Price")
            product_effective_dt_label.setText(f"Effective date {qss.req_field_indicator}") if product_effective_dt == '' else product_effective_dt_label.setText(f"Effective date")

            QMessageBox.critical(dialog, 'Error', 'Please fill out all required fields.')
    
    def init_manage_stock_data_entry(self, dialog, stock_available, stock_onhand):
        if stock_available.isdigit() and stock_onhand.isdigit():
            schema.update_stock_data(
                stock_available,    
                stock_onhand,
                self.sel_product_stock_id,
                self.sel_product_id
            )

            QMessageBox.information(dialog, 'Success', 'Stock edited.')
            dialog.close()
            self.sel_product_id = 0
            self.sel_product_stock_id = 0
        else:
            QMessageBox.critical(dialog, 'Error', 'Invalid numeric value.')
        pass
    pass
class MyProductView(MyWidget):
    def __init__(self, model: MyProductModel):
        super().__init__()

        self.m = model

        self.set_product_box()

    def set_product_box(self):
        self.filter_field = MyLineEdit(object_name='filter_field')
        self.filter_button = MyPushButton(object_name='filter_button', text='Filter')
        self.filter_box = MyGroupBox(object_name='filter_box')
        self.filter_layout = MyHBoxLayout(object_name='filter_layout')
        self.filter_layout.addWidget(self.filter_field)
        self.filter_layout.addWidget(self.filter_button)
        self.filter_box.setLayout(self.filter_layout)

        self.import_data_button = MyPushButton(object_name='import_data_button', text='Import')
        self.add_data_button = MyPushButton(object_name='add_data_button', text='Add')
        self.manage_data_box = MyGroupBox(object_name='manage_data_box')
        self.manage_data_layout = MyHBoxLayout(object_name='manage_data_layout')
        self.manage_data_layout.addWidget(self.import_data_button)
        self.manage_data_layout.addWidget(self.add_data_button)
        self.manage_data_box.setLayout(self.manage_data_layout)

        self.product_act_box = MyGroupBox(object_name='product_act_box')
        self.product_act_layout = MyHBoxLayout(object_name='product_act_layout')
        self.product_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.product_act_layout.addWidget(self.manage_data_box,1,Qt.AlignmentFlag.AlignRight)
        self.product_act_box.setLayout(self.product_act_layout)

        self.product_overview_table = MyTableWidget(object_name='product_overview_table')
        self.product_overview_prev_button = MyPushButton(object_name='overview_prev_button', text='Prev')
        self.product_overview_page_label = MyLabel(object_name='overview_page_label', text=f"Page {self.m.page_number}/{self.m.total_product_page_number}")
        self.product_overview_next_button = MyPushButton(object_name='overview_next_button', text='Next')
        self.product_overview_act_box = MyGroupBox(object_name='overview_act_box')
        self.product_overview_act_layout = MyHBoxLayout(object_name='overview_act_layout')
        self.product_overview_act_layout.addWidget(self.product_overview_prev_button)
        self.product_overview_act_layout.addWidget(self.product_overview_page_label)
        self.product_overview_act_layout.addWidget(self.product_overview_next_button)
        self.product_overview_act_box.setLayout(self.product_overview_act_layout)
        self.product_overview_box = MyGroupBox()
        self.product_overview_layout = MyVBoxLayout()
        self.product_overview_layout.addWidget(self.product_overview_table)
        self.product_overview_layout.addWidget(self.product_overview_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.product_overview_box.setLayout(self.product_overview_layout)

        self.product_stock_table = MyTableWidget(object_name='product_stock_table')
        self.product_stock_prev_button = MyPushButton(object_name='overview_prev_button', text='Prev')
        self.product_stock_page_label = MyLabel(object_name='overview_page_label', text=f"Page {self.m.page_number}/{self.m.total_stock_page_number}")
        self.product_stock_next_button = MyPushButton(object_name='overview_next_button', text='Next')
        self.product_stock_act_box = MyGroupBox(object_name='overview_act_box')
        self.product_stock_act_layout = MyHBoxLayout(object_name='overview_act_layout')
        self.product_stock_act_layout.addWidget(self.product_stock_prev_button)
        self.product_stock_act_layout.addWidget(self.product_stock_page_label)
        self.product_stock_act_layout.addWidget(self.product_stock_next_button)
        self.product_stock_act_box.setLayout(self.product_stock_act_layout)
        self.product_stock_box = MyGroupBox()
        self.product_stock_layout = MyVBoxLayout()
        self.product_stock_layout.addWidget(self.product_stock_table)
        self.product_stock_layout.addWidget(self.product_stock_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.product_stock_box.setLayout(self.product_stock_layout)
        
        self.product_sort_tab = MyTabWidget()
        self.product_sort_tab.addTab(self.product_overview_box, 'Overview')
        self.product_sort_tab.addTab(self.product_stock_box, 'Inventory')

        self.main_layout = MyVBoxLayout()
        self.main_layout.addWidget(self.product_act_box)
        self.main_layout.addWidget(self.product_sort_tab)
        self.setLayout(self.main_layout)

    def set_manage_product_data_box(self):
        self.product_barcode_label = MyLabel(text='Barcode')
        self.product_name_label = MyLabel(text='Name')
        self.product_expire_dt_label = MyLabel(text='Expire date')
        self.product_barcode_field = MyLineEdit(object_name='product_barcode_field')
        self.product_name_field = MyLineEdit(object_name='product_name_field')
        self.product_expire_dt_field = MyDateEdit(object_name='product_expire_dt_field')
        self.primary_field_box = MyGroupBox(object_name='field_box')
        self.primary_field_layout = MyGridLayout(object_name='sub_field_layout')
        self.primary_field_layout.addWidget(self.product_barcode_label,0,0)
        self.primary_field_layout.addWidget(self.product_barcode_field,1,0)
        self.primary_field_layout.addWidget(self.product_name_label,0,1)
        self.primary_field_layout.addWidget(self.product_name_field,1,1)
        self.primary_field_layout.addWidget(self.product_expire_dt_label,0,2)
        self.primary_field_layout.addWidget(self.product_expire_dt_field,1,2)
        self.primary_field_box.setLayout(self.primary_field_layout)

        self.product_type_label = MyLabel(text='Type')
        self.product_brand_label = MyLabel(text='Brand')
        self.product_sales_group_label = MyLabel(text='Sales group')
        self.product_supplier_label = MyLabel(text='Supplier')
        self.product_type_field = MyComboBox(object_name='product_type_field')
        self.product_brand_field = MyComboBox(object_name='product_brand_field')
        self.product_sales_group_field = MyComboBox(object_name='product_sales_group_field')
        self.product_supplier_field = MyComboBox(object_name='product_supplier_field')
        self.category_field_box = MyGroupBox(object_name='field_box')
        self.category_field_layout = MyGridLayout(object_name='sub_field_layout')
        self.category_field_layout.addWidget(self.product_type_label,0,0)
        self.category_field_layout.addWidget(self.product_type_field,1,0)
        self.category_field_layout.addWidget(self.product_brand_label,2,0)
        self.category_field_layout.addWidget(self.product_brand_field,3,0)
        self.category_field_layout.addWidget(self.product_sales_group_label,0,1)
        self.category_field_layout.addWidget(self.product_sales_group_field,1,1)
        self.category_field_layout.addWidget(self.product_supplier_label,2,1)
        self.category_field_layout.addWidget(self.product_supplier_field,3,1)
        self.category_field_box.setLayout(self.category_field_layout)

        self.product_cost_label = MyLabel(text='Cost')
        self.product_price_label = MyLabel(text='Price')
        self.product_effective_dt_label = MyLabel(text='Effective date')
        self.product_retail_price_label = MyLabel(text='Retail price')
        self.product_wholesale_price_label = MyLabel(text='Wholesale price')

        self.product_cost_field = MyLineEdit(object_name='product_cost_field')
        self.product_effective_dt_field = MyDateEdit(object_name='product_effective_dt_field')
        
        self.product_price_field = MyLineEdit(object_name='product_price_field')
        self.product_retail_price_field = MyLineEdit(object_name='product_price_field')
        self.product_wholesale_price_field = MyLineEdit(object_name='product_price_field')
        
        self.pricing_field_box = MyGroupBox(object_name='field_box')
        self.pricing_field_layout = MyGridLayout(object_name='sub_field_layout')
        self.pricing_field_layout.addWidget(self.product_cost_label,0,0)
        self.pricing_field_layout.addWidget(self.product_cost_field,1,0)
        self.pricing_field_layout.addWidget(self.product_effective_dt_label,0,1)
        self.pricing_field_layout.addWidget(self.product_effective_dt_field,1,1)

        self.pricing_field_layout.addWidget(self.product_retail_price_label,2,0)
        self.pricing_field_layout.addWidget(self.product_retail_price_field,3,0)
        self.pricing_field_layout.addWidget(self.product_wholesale_price_label,2,1)
        self.pricing_field_layout.addWidget(self.product_wholesale_price_field,3,1)
        self.pricing_field_layout.addWidget(self.product_price_label,2,0)
        self.pricing_field_layout.addWidget(self.product_price_field,3,0)
        self.pricing_field_box.setLayout(self.pricing_field_layout)

        self.product_promo_name_label = MyLabel(text='Promo name')
        self.product_promo_type_label = MyLabel(text='Promo type')
        self.product_promo_percent_label = MyLabel(text='Promo percent')
        self.product_disc_value_label = MyLabel(text='Discount value')
        self.product_new_price_label = MyLabel(text='New price')
        self.product_start_dt_label = MyLabel(text='Start date')
        self.product_end_dt_label = MyLabel(text='End date')
        self.product_promo_name_field = MyComboBox(object_name='product_promo_name_field')
        self.product_promo_type_field = MyLineEdit(object_name='product_promo_type_field')
        self.product_promo_percent_field = MyLineEdit(object_name='product_promo_percent_field')
        self.product_disc_value_field = MyLineEdit(object_name='product_disc_value_field')
        self.product_new_price_field = MyLineEdit(object_name='product_new_price_field')
        self.product_start_dt_field = MyDateEdit(object_name='product_start_dt_field')
        self.product_end_dt_field = MyDateEdit(object_name='product_end_dt_field')
        self.promo_field_box = MyGroupBox(object_name='field_box')
        self.promo_field_layout = MyGridLayout(object_name='sub_field_layout')
        self.promo_field_layout.addWidget(self.product_promo_name_label,0,0)
        self.promo_field_layout.addWidget(self.product_promo_name_field,1,0)
        self.promo_field_layout.addWidget(self.product_promo_type_label,2,0)
        self.promo_field_layout.addWidget(self.product_promo_type_field,3,0)
        self.promo_field_layout.addWidget(self.product_promo_percent_label,4,0)
        self.promo_field_layout.addWidget(self.product_promo_percent_field,5,0)
        self.promo_field_layout.addWidget(self.product_disc_value_label,6,0)
        self.promo_field_layout.addWidget(self.product_disc_value_field,7,0)
        self.promo_field_layout.addWidget(self.product_new_price_label,8,0)
        self.promo_field_layout.addWidget(self.product_new_price_field,9,0)
        self.promo_field_layout.addWidget(self.product_start_dt_label,10,0)
        self.promo_field_layout.addWidget(self.product_start_dt_field,11,0)
        self.promo_field_layout.addWidget(self.product_end_dt_label,12,0)
        self.promo_field_layout.addWidget(self.product_end_dt_field,13,0)
        self.promo_field_box.setLayout(self.promo_field_layout)

        self.side_a_field_layout = MyVBoxLayout('sub_field_layout')
        self.side_a_field_layout.addWidget(self.primary_field_box)
        self.side_a_field_layout.addWidget(QLabel('<hr>'))
        self.side_a_field_layout.addWidget(self.category_field_box)
        self.side_a_field_layout.addWidget(QLabel('<hr>'))
        self.side_a_field_layout.addWidget(self.pricing_field_box,4,Qt.AlignmentFlag.AlignTop)

        self.side_b_field_layout = MyVBoxLayout('sub_field_layout')
        self.side_b_field_layout.addWidget(self.promo_field_box,0,Qt.AlignmentFlag.AlignTop)

        self.product_field_box = MyGroupBox(object_name='field_box')
        self.product_field_layout = MyGridLayout(object_name='field_layout')
        self.product_field_layout.addLayout(self.side_a_field_layout,0,0)
        self.product_field_layout.addLayout(self.side_b_field_layout,0,1)
        self.product_field_box.setLayout(self.product_field_layout)
        self.manage_product_data_scra = MyScrollArea()
        self.manage_product_data_scra.setWidget(self.product_field_box)

        self.product_stock_tracking_field = MyCheckBox(object_name='product_stock_tracking_field', text='Track inventory?')
        self.save_product_data_button = MyPushButton(object_name='save_button', text='Save')
        self.manage_product_data_act_close_button = MyPushButton(object_name='close_button', text='Close')
        self.manage_product_data_act_box = MyGroupBox(object_name='manage_data_act_box')
        self.manage_product_data_act_layout = MyHBoxLayout(object_name='manage_data_act_layout')
        self.manage_product_data_act_layout.addWidget(self.product_stock_tracking_field)
        self.manage_product_data_act_layout.addWidget(self.save_product_data_button,1,Qt.AlignmentFlag.AlignRight)
        self.manage_product_data_act_layout.addWidget(self.manage_product_data_act_close_button)
        self.manage_product_data_act_box.setLayout(self.manage_product_data_act_layout)
        
        self.manage_product_data_dialog = MyDialog()
        self.manage_product_data_layout = MyVBoxLayout()
        self.manage_product_data_layout.addWidget(self.manage_product_data_scra)
        self.manage_product_data_layout.addWidget(self.manage_product_data_act_box)
        self.manage_product_data_dialog.setLayout(self.manage_product_data_layout)
    def set_manage_stock_data_box(self):
        self.stock_available_label = MyLabel(text='Available')
        self.stock_available_field = MyLineEdit()
        self.stock_onhand_label = MyLabel(text='On hand')
        self.stock_onhand_field = MyLineEdit()
        self.stock_field_box = MyGroupBox(object_name='field_box')
        self.stock_field_layout = MyFormLayout(object_name='field_layout')
        self.stock_field_layout.addRow(self.stock_available_label)
        self.stock_field_layout.addRow(self.stock_available_field)
        self.stock_field_layout.addRow(self.stock_onhand_label)
        self.stock_field_layout.addRow(self.stock_onhand_field)
        self.stock_field_box.setLayout(self.stock_field_layout)
        self.manage_product_data_scra = MyScrollArea()
        self.manage_product_data_scra.setWidget(self.stock_field_box)

        self.save_stock_data_button = MyPushButton(object_name='save_button', text='Save')
        self.manage_stock_data_act_close_button = MyPushButton(object_name='close_button', text='Close')
        self.manage_stock_data_act_box = MyGroupBox(object_name='manage_data_act_box')
        self.manage_stock_data_act_layout = MyHBoxLayout(object_name='manage_data_act_layout')
        self.manage_stock_data_act_layout.addWidget(self.save_stock_data_button,1,Qt.AlignmentFlag.AlignRight)
        self.manage_stock_data_act_layout.addWidget(self.manage_stock_data_act_close_button)
        self.manage_stock_data_act_box.setLayout(self.manage_stock_data_act_layout)

        self.manage_stock_data_dialog = MyDialog()
        self.manage_stock_data_layout = MyVBoxLayout()
        self.manage_stock_data_layout.addWidget(self.manage_product_data_scra)
        self.manage_stock_data_layout.addWidget(self.manage_stock_data_act_box)
        self.manage_stock_data_dialog.setLayout(self.manage_stock_data_layout)
        pass

    def set_progress_dialog(self):
        self.progress_bar = MyProgressBar()
        self.progress_label = MyLabel(text='Please wait...')
        self.progress_dialog = MyDialog(window_title='99% complete')
        self.progress_layout = MyVBoxLayout(object_name='progress_layout')
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_dialog.setLayout(self.progress_layout)
        pass

    def set_overview_table_act_box(self):
        self.edit_data_button = MyPushButton(object_name='edit_data_button', text='Edit')
        self.view_data_button = MyPushButton(object_name='view_data_button', text='View')
        self.delete_data_button = MyPushButton(object_name='delete_data_button', text='Delete') # unavailable for now
        self.product_overview_data_act_box = MyGroupBox(object_name='product_overview_data_act_box')
        self.product_overview_data_act_layout = MyHBoxLayout(object_name='product_overview_data_act_layout')
        self.product_overview_data_act_layout.addWidget(self.edit_data_button)
        self.product_overview_data_act_layout.addWidget(self.view_data_button)
        self.product_overview_data_act_layout.addWidget(self.delete_data_button)
        self.product_overview_data_act_box.setLayout(self.product_overview_data_act_layout)
    def set_stock_table_act_box(self):
        self.edit_stock_data_button = MyPushButton(object_name='edit_data_button', text='Edit')
        self.delete_stock_data_button = MyPushButton(object_name='void_data_button', text='Stop')
        self.product_stock_act_box = MyGroupBox(object_name='product_stock_data_act_box')
        self.product_stock_act_layout = MyHBoxLayout(object_name='product_stock_data_act_layout')
        self.product_stock_act_layout.addWidget(self.edit_stock_data_button)
        self.product_stock_act_layout.addWidget(self.delete_stock_data_button)
        self.product_stock_act_box.setLayout(self.product_stock_act_layout)

    def set_view_dialog(self):
        self.product_barcode_info = MyLabel(text=f"product_barcode")
        self.product_name_info = MyLabel(text=f"product_name")
        self.product_expire_dt_info = MyLabel(text=f"product_expire_dt")

        self.product_type_info = MyLabel(text=f"product_type")
        self.product_brand_info = MyLabel(text=f"product_brand")
        self.product_sales_group_info = MyLabel(text=f"product_sales_group")
        self.product_supplier_info = MyLabel(text=f"product_supplier")

        self.product_cost_info = MyLabel(text=f"product_cost")
        self.product_price_info = MyLabel(text=f"product_price")
        self.product_effective_dt_info = MyLabel(text=f"product_effective_dt")
        self.product_promo_name_info = MyLabel(text=f"product_promo_name")
        self.product_disc_value_info = MyLabel(text=f"product_disc_value")

        self.product_stock_tracking_info = MyLabel(text=f"product_stock_tracking")

        self.product_datetime_created_info = MyLabel(text=f"product_datetime_created")

        self.info_box = MyGroupBox(object_name='info_box')
        self.info_layout = MyFormLayout(object_name='info_layout')
        self.info_layout.addRow('Barcode:', self.product_barcode_info)
        self.info_layout.addRow('Name:', self.product_name_info)
        self.info_layout.addRow('Expire date:', self.product_expire_dt_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Type:', self.product_type_info)
        self.info_layout.addRow('Brand:', self.product_brand_info)
        self.info_layout.addRow('Sales group:', self.product_sales_group_info)
        self.info_layout.addRow('Supplier:', self.product_supplier_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Cost:', self.product_cost_info)
        self.info_layout.addRow('Price:', self.product_price_info)
        self.info_layout.addRow('Effective date:', self.product_effective_dt_info)
        self.info_layout.addRow('Promo name:', self.product_promo_name_info)
        self.info_layout.addRow('Discount:', self.product_disc_value_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Inventory tracking:', self.product_stock_tracking_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Date/Time created:', self.product_datetime_created_info)

        self.info_box.setLayout(self.info_layout)
        self.view_data_scra = MyScrollArea()
        self.view_data_scra.setWidget(self.info_box)

        self.view_data_act_close_button = MyPushButton(object_name='close_button', text='Close')
        self.view_data_act_box = MyGroupBox(object_name='view_data_act_box')
        self.view_data_act_layout = MyHBoxLayout(object_name='view_data_act_layout')
        self.view_data_act_layout.addWidget(self.view_data_act_close_button,0,Qt.AlignmentFlag.AlignRight)
        self.view_data_act_box.setLayout(self.view_data_act_layout)

        self.view_data_dialog = MyDialog()
        self.view_data_layout = MyVBoxLayout()
        self.view_data_layout.addWidget(self.view_data_scra)
        self.view_data_layout.addWidget(self.view_data_act_box)
        self.view_data_dialog.setLayout(self.view_data_layout)
        pass
class MyProductController:
    def __init__(self, model: MyProductModel, view: MyProductView):
        self.v = view
        self.m = model

        self.set_product_box_conn()
        self.sync_ui()

    def set_product_box_conn(self):
        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)
        self.v.import_data_button.clicked.connect(self.on_import_data_button_clicked)
        self.v.add_data_button.clicked.connect(self.on_add_data_button_clicked)

        self.v.product_sort_tab.currentChanged.connect(self.on_product_sort_tab_current_changed)

        self.v.product_overview_prev_button.clicked.connect(self.on_prev_button_clicked)
        self.v.product_overview_next_button.clicked.connect(self.on_next_button_clicked)
        self.v.product_stock_prev_button.clicked.connect(self.on_prev_button_clicked)
        self.v.product_stock_next_button.clicked.connect(self.on_next_button_clicked)

        pass
    def on_filter_button_clicked(self): # IDEA: src
        text_filter = self.v.filter_field.text()
        
        self.m.total_product_page_number = schema.select_product_data_total_page_count(text=text_filter)
        self.m.total_stock_page_number = schema.select_stock_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_product_page_number > 0 or self.m.total_stock_page_number > 0 else 0

        self.populate_overview_table(text=text_filter, page_number=self.m.page_number)
        self.populate_stock_table(text=text_filter, page_number=self.m.page_number)
        pass
    
    def on_import_data_button_clicked(self): # IDEA: src
        csv_file_path, _ = QFileDialog.getOpenFileName(self.v, 'Open CSV', qss.csv_folder_path, 'CSV File (*csv)')

        if csv_file_path:
            self.v.set_progress_dialog()
            self.m.set_import_data_entry(csv_file_path)
            self.set_data_import_thread_conn()

            self.v.progress_dialog.exec()
            if self.v.progress_dialog.close(): self.m.data_import_thread.stop()
            
            self.sync_ui()
        pass
    def set_data_import_thread_conn(self):
        self.m.data_import_thread.update.connect(self.on_data_import_thread_update)
        self.m.data_import_thread.cancelled.connect(self.on_data_import_thread_cancelled)
        self.m.data_import_thread.finished.connect(self.on_data_import_thread_finished)
        self.m.data_import_thread.invalid.connect(self.on_data_import_thread_invalid)
        pass
    def on_data_import_thread_update(self, total_data_count, current_data):
        self.m.progress_count += 1
        self.m.progress_percent = int((self.m.progress_count * 100) / total_data_count)
        self.v.progress_dialog.setWindowTitle(f"{self.m.progress_percent}% complete")
        self.v.progress_bar.setValue(self.m.progress_percent)
        self.v.progress_label.setText(current_data)
        pass
    def on_data_import_thread_cancelled(self):
        QMessageBox.information(self.v, 'Cancelled', 'Import cancelled.')
        pass
    def on_data_import_thread_finished(self):
        QMessageBox.information(self.v, 'Success', 'Import complete.')
        self.v.progress_dialog.close_signal.emit('finished')
        self.v.progress_dialog.close()
        pass
    def on_data_import_thread_invalid(self):
        QMessageBox.critical(self.v, 'Error', 'An error occurred during import.')
        self.v.progress_dialog.close()
        pass

    def on_add_data_button_clicked(self): # IDEA: src
        self.v.set_manage_product_data_box()
        self.load_combo_box_data()
        self.v.manage_product_data_dialog.setWindowTitle('Add product')

        # self.set_category_field_disabled(False)
        self.v.promo_field_box.hide()
        self.set_price_type_field_hidden(False)
    
        self.set_manage_product_data_box_conn(task='add_data')
        self.v.manage_product_data_dialog.exec()
        pass

    def on_product_sort_tab_current_changed(self):
        self.sync_ui()

    def populate_overview_table(self, text='', page_number=1): # IDEA: src
        self.v.product_overview_prev_button.setEnabled(page_number > 1)
        self.v.product_overview_next_button.setEnabled(page_number < self.m.total_product_page_number)
        self.v.product_overview_page_label.setText(f"Page {page_number}/{self.m.total_product_page_number}")

        product_data = schema.select_product_data_as_display(text=text, page_number=page_number)

        self.v.product_overview_table.setRowCount(len(product_data))

        for i, data in enumerate(product_data):
            self.v.set_overview_table_act_box()

            if datetime.strptime(str(data[9]), "%Y-%m-%d") <= datetime.today(): 
                self.v.edit_data_button.hide()
                self.v.delete_data_button.hide() # NOTE: temporarily unavailable

            flag = True  if data[10] is not None else False # if has promo, set flag (to make the item's foreground red)


            product_barcode = MyTableWidgetItem(text=f"{data[0]}", has_promo=flag)
            product_name = MyTableWidgetItem(text=f"{data[1]}", has_promo=flag)
            product_expire_dt = MyTableWidgetItem(text=f"{data[2]}", has_promo=flag)

            product_type = MyTableWidgetItem(text=f"{data[3]}", has_promo=flag)
            product_brand = MyTableWidgetItem(text=f"{data[4]}", has_promo=flag)
            product_sales_group = MyTableWidgetItem(text=f"{data[5]}", has_promo=flag)
            product_supplier = MyTableWidgetItem(text=f"{data[6]}", has_promo=flag)

            product_cost = MyTableWidgetItem(text=f"{data[7]}", format='bill', has_promo=flag)
            product_price = MyTableWidgetItem(text=f"{data[8]}", format='bill', has_promo=flag)
            product_effective_dt = MyTableWidgetItem(text=f"{data[9]}", has_promo=flag)
            product_promo_name = MyTableWidgetItem(text=f"{data[10]}", has_promo=flag)
            product_disc_value = MyTableWidgetItem(text=f"{data[11]}", format='bill', has_promo=flag)

            product_stock_id = MyTableWidgetItem(text=f"{data[12]}", has_promo=flag)

            datetime_created = MyTableWidgetItem(text=f"{data[13]}", has_promo=flag)

            self.v.product_overview_table.setCellWidget(i, 0, self.v.product_overview_data_act_box)
            self.v.product_overview_table.setItem(i, 1, product_barcode)
            self.v.product_overview_table.setItem(i, 2, product_name)
            self.v.product_overview_table.setItem(i, 3, product_expire_dt)

            self.v.product_overview_table.setItem(i, 4, product_type)
            self.v.product_overview_table.setItem(i, 5, product_brand)
            self.v.product_overview_table.setItem(i, 6, product_sales_group)
            self.v.product_overview_table.setItem(i, 7, product_supplier)

            self.v.product_overview_table.setItem(i, 8, product_cost)
            self.v.product_overview_table.setItem(i, 9, product_price)
            self.v.product_overview_table.setItem(i, 10, product_effective_dt)
            self.v.product_overview_table.setItem(i, 11, product_promo_name)
            self.v.product_overview_table.setItem(i, 12, product_disc_value)

            self.v.product_overview_table.setItem(i, 13, product_stock_id)

            self.v.product_overview_table.setItem(i, 14, datetime_created)

            self.v.edit_data_button.clicked.connect(lambda _, data=data: self.on_edit_data_button_clicked(data))
            self.v.view_data_button.clicked.connect(lambda _, data=data: self.on_view_data_button_clicked(data))
            self.v.delete_data_button.clicked.connect(lambda _, data=data: self.on_delete_data_button_clicked(data))
        pass
    def on_edit_data_button_clicked(self, data):
        self.v.set_manage_product_data_box()
        self.load_combo_box_data()
        self.v.manage_product_data_dialog.setWindowTitle(f"{data[1]}")

        self.v.promo_field_box.show()
        # self.set_category_field_disabled(True)
        self.set_promo_field_hidden(True)
        self.set_price_type_field_hidden(True)
        sel_product_data = schema.select_product_data(data[0], data[1], data[15])

        for i, sel_data in enumerate(sel_product_data):
            self.v.product_barcode_field.setText(str(sel_data[0]))
            self.v.product_name_field.setText(str(sel_data[1]))
            self.v.product_expire_dt_field.setDate(QDate.fromString(str(sel_data[2]), Qt.DateFormat.ISODate))

            self.v.product_type_field.setCurrentText(str(sel_data[3]))
            self.v.product_brand_field.setCurrentText(str(sel_data[4]))
            self.v.product_sales_group_field.setCurrentText(str(sel_data[5]))
            self.v.product_supplier_field.setCurrentText(str(sel_data[6]))

            self.v.product_cost_field.setText(str(sel_data[7]))
            self.v.product_price_field.setText(str(sel_data[8]))
            self.v.product_effective_dt_field.setDate(QDate.fromString(str(sel_data[9]), Qt.DateFormat.ISODate))

            self.v.product_stock_tracking_field.setChecked(True) if sel_data[12] > 0 else self.v.product_stock_tracking_field.setChecked(False)

            self.m.sel_product_id = sel_data[10] # NOTE: becomes 0 if NoneType. Check 'product.py'
            self.m.sel_product_price_id = sel_data[11] # NOTE: becomes 0 if NoneType. Check 'product.py'
            self.m.sel_product_stock_id = sel_data[12] # NOTE: becomes 0 if NoneType. Check 'product.py'
            self.m.sel_product_promo_id = sel_data[13]

            pass
        
        self.set_manage_product_data_box_conn(task='edit_data')
        self.v.manage_product_data_dialog.exec()
        pass

    def set_price_type_field_hidden(self, hidden):
        if hidden is True:
            self.v.product_price_label.show()
            self.v.product_price_field.show()
        else:
            self.v.product_price_label.hide()
            self.v.product_price_field.hide()
        self.v.product_retail_price_label.setHidden(hidden)
        self.v.product_retail_price_field.setHidden(hidden)
        self.v.product_wholesale_price_label.setHidden(hidden)
        self.v.product_wholesale_price_field.setHidden(hidden)

    def on_view_data_button_clicked(self, data):
        self.v.set_view_dialog()
        self.v.view_data_dialog.setWindowTitle(f"{data[1]}")

        self.v.product_barcode_info.setText(str(data[0]))
        self.v.product_name_info.setText(str(data[1]))
        self.v.product_expire_dt_info.setText(str(data[2]))
        self.v.product_type_info.setText(str(data[3]))
        self.v.product_brand_info.setText(str(data[4]))
        self.v.product_sales_group_info.setText(str(data[5]))
        self.v.product_supplier_info.setText(str(data[6]))
        self.v.product_cost_info.setText(str(data[7]))
        self.v.product_price_info.setText(str(data[8]))
        self.v.product_effective_dt_info.setText(str(data[9]))
        self.v.product_promo_name_info.setText(str(data[10]))
        self.v.product_disc_value_info.setText(str(data[11]))

        self.v.product_stock_tracking_info.setText(str(data[12]))
        self.v.product_datetime_created_info.setText(str(data[13]))


        self.set_view_product_data_box_conn()
        self.v.view_data_dialog.exec()
        pass
    def set_view_product_data_box_conn(self):
        self.v.view_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.view_data_dialog))
    def on_delete_data_button_clicked(self, data):
        sel_product_data = schema.select_product_data(data[0], data[1], data[15])

        for i, sel_data in enumerate(sel_product_data):
            product_name = sel_data[1]
            product_effective_dt = sel_data[9]
            product_price_id = data[15]


        confirm = QMessageBox.warning(self.v, 'Confirm', f"Delete {product_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_product_data(product_price_id)

            QMessageBox.information(self.v, 'Success', f"{product_name} has been deleted.")

        self.sync_ui()
        pass

    def populate_stock_table(self, text='', page_number=1): # IDEA: src
        self.v.product_stock_prev_button.setEnabled(page_number > 1)
        self.v.product_stock_next_button.setEnabled(page_number < self.m.total_stock_page_number)
        self.v.product_stock_page_label.setText(f"Page {page_number}/{self.m.total_stock_page_number}")

        stock_data = schema.select_stock_data_as_display(text=text, page_number=page_number)

        self.v.product_stock_table.setRowCount(len(stock_data))

        for i, data in enumerate(stock_data):
            self.v.set_stock_table_act_box()

            product_barcode = MyTableWidgetItem(text=f"{data[0]}")
            product_name = MyTableWidgetItem(text=f"{data[1]}")
            product_stock_available = MyTableWidgetItem(text=f"{data[2]}")
            product_stock_onhand = MyTableWidgetItem(text=f"{data[3]}")
            datetime_created = MyTableWidgetItem(text=f"{data[4]}")

            self.v.product_stock_table.setCellWidget(i, 0, self.v.product_stock_act_box)
            self.v.product_stock_table.setItem(i, 1, product_barcode)
            self.v.product_stock_table.setItem(i, 2, product_name)
            self.v.product_stock_table.setItem(i, 3, product_stock_available)
            self.v.product_stock_table.setItem(i, 4, product_stock_onhand)
            self.v.product_stock_table.setItem(i, 5, datetime_created)

            self.v.edit_stock_data_button.clicked.connect(lambda _, data=data: self.on_edit_stock_data_button_clicked(data))
            self.v.delete_stock_data_button.clicked.connect(lambda _, data=data: self.on_delete_stock_data_button_clicked(data))
        pass
    def on_edit_stock_data_button_clicked(self, data):
        self.v.set_manage_stock_data_box()
        self.v.manage_stock_data_dialog.setWindowTitle(f"{data[1]}")


        self.v.stock_available_field.setText(str(data[2]))
        self.v.stock_onhand_field.setText(str(data[3]))

        self.m.sel_product_stock_id = data[5]
        self.m.sel_product_id = data[6]


        self.set_manage_stock_data_conn()

        self.v.manage_stock_data_dialog.exec()
        pass
    def set_manage_stock_data_conn(self):
        self.v.save_stock_data_button.clicked.connect(self.on_save_stock_data_button_clicked)
        self.v.manage_stock_data_act_close_button.clicked.connect(self.on_manage_stock_data_act_close_button_clicked)
        pass
    def on_save_stock_data_button_clicked(self):
        stock_available = self.v.stock_available_field.text()
        stock_onhand = self.v.stock_onhand_field.text()

        self.m.init_manage_stock_data_entry(
            self.v.manage_stock_data_dialog,
            stock_available, 
            stock_onhand
        )

        self.sync_ui()
        pass
    def on_manage_stock_data_act_close_button_clicked(self):
        self.close_dialog(self.v.manage_stock_data_dialog)
        pass
    def on_delete_stock_data_button_clicked(self, data):
        sel_stock_data = schema.select_stock_data(data[5], data[6])

        for i, sel_data in enumerate(sel_stock_data):
            product_name = sel_data[1]
            stock_id = sel_data[4]
            product_id = sel_data[5]

        confirm = QMessageBox.warning(self.v, 'Confirm', f"Stop tracking {product_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_stock_data(stock_id, product_id)

            QMessageBox.information(self.v, 'Success', f"{product_name} has been deleted.")

        self.sync_ui()
        pass

    def on_prev_button_clicked(self):
        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.product_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_product_page_number}")
            self.v.product_stock_page_label.setText(f"Page {self.m.page_number}/{self.m.total_stock_page_number}")

        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        self.populate_stock_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass
    def on_next_button_clicked(self):
        if self.m.page_number < self.m.total_product_page_number or self.m.page_number < self.m.total_stock_page_number:
            self.m.page_number += 1

            self.v.product_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_product_page_number}")
            self.v.product_stock_page_label.setText(f"Page {self.m.page_number}/{self.m.total_stock_page_number}")
        
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        self.populate_stock_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass

    # IDEA: if the widget uses the same connection
    def set_manage_product_data_box_conn(self, task):
        self.v.product_price_field.textChanged.connect(self.on_product_price_field_text_changed)
        self.v.product_promo_name_field.currentTextChanged.connect(self.on_product_promo_name_field_current_text_changed)

        self.v.save_product_data_button.clicked.connect(lambda: self.on_save_data_button_clicked(task))
        self.v.manage_product_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.manage_product_data_dialog))
        pass
    def load_combo_box_data(self):
        self.v.set_manage_product_data_box()

        self.v.product_type_field.clear()
        self.v.product_brand_field.clear()
        self.v.product_supplier_field.clear()
        self.v.product_promo_name_field.clear()

        product_type_data = schema.select_product_type_for_combo_box()
        product_brand_data = schema.select_product_brand_for_combo_box()
        product_supplier_data = schema.select_product_supplier_for_combo_box()
        product_promo_name_data = schema.select_product_promo_name_for_combo_box()

        for product_type in product_type_data: self.v.product_type_field.addItems(product_type)
        for product_brand in product_brand_data: self.v.product_brand_field.addItems(product_brand)
        for product_supplier in product_supplier_data: self.v.product_supplier_field.addItems(product_supplier)

        self.v.product_sales_group_field.addItem('Retail')
        self.v.product_sales_group_field.addItem('Wholesale')
        
        self.v.product_promo_name_field.addItem('No promo')
        for product_promo_name in product_promo_name_data: self.v.product_promo_name_field.addItems(product_promo_name)
        pass
    
    def on_product_price_field_text_changed(self):
        self.compute_new_product_price_with_promo()
        pass
    def on_product_promo_name_field_current_text_changed(self):
        self.set_promo_field_hidden(True) if self.v.product_promo_name_field.currentText() == 'No promo' else self.set_promo_field_hidden(False)

        promo_name = self.v.product_promo_name_field.currentText()

        promo_type = schema.select_promo_type(promo_name)
        promo_percent = schema.select_promo_percent(promo_name)

        self.v.product_promo_type_field.setText(str(promo_type))
        self.v.product_promo_percent_field.setText(str(promo_percent))

        self.compute_new_product_price_with_promo()
        pass
    def compute_new_product_price_with_promo(self):
        try:
            product_price = float(self.v.product_price_field.text())
            product_promo_percent = float(self.v.product_promo_percent_field.text())

            old_product_price = product_price
            product_disc_value = old_product_price * (product_promo_percent / 100)
            new_product_price = product_price - product_disc_value

            self.v.product_disc_value_field.setText(f'{product_disc_value:.2f}')
            self.v.product_new_price_field.setText(f'{new_product_price:.2f}')
            pass
        except ValueError:
            self.v.product_disc_value_field.setText('Error')
            self.v.product_new_price_field.setText('Error')
            pass
    
    def set_category_field_disabled(self, disabled=True):
        self.v.product_type_field.setDisabled(disabled)
        self.v.product_sales_group_field.setDisabled(disabled)
        self.v.product_supplier_field.setDisabled(disabled)
        self.v.product_brand_field.setDisabled(disabled)
        pass
    def set_promo_field_hidden(self, hidden=True):
        if hidden == True:
            self.v.product_effective_dt_label.show()
            self.v.product_effective_dt_field.show()
        else:
            self.v.product_effective_dt_label.hide()
            self.v.product_effective_dt_field.hide()

        self.v.product_promo_type_label.setHidden(hidden)
        self.v.product_promo_percent_label.setHidden(hidden)
        self.v.product_disc_value_label.setHidden(hidden)
        self.v.product_new_price_label.setHidden(hidden)
        self.v.product_start_dt_label.setHidden(hidden)
        self.v.product_end_dt_label.setHidden(hidden)

        self.v.product_promo_type_field.setHidden(hidden)
        self.v.product_promo_percent_field.setHidden(hidden)
        self.v.product_disc_value_field.setHidden(hidden)
        self.v.product_new_price_field.setHidden(hidden)
        self.v.product_start_dt_field.setHidden(hidden)
        self.v.product_end_dt_field.setHidden(hidden)
        pass
    def on_save_data_button_clicked(self, task):
        product_barcode = self.v.product_barcode_field.text()
        product_name = self.v.product_name_field.text()
        product_expire_dt = self.v.product_expire_dt_field.date().toString(Qt.DateFormat.ISODate)

        product_type = self.v.product_type_field.currentText()
        product_brand = self.v.product_brand_field.currentText()
        product_sales_group = self.v.product_sales_group_field.currentText()
        product_supplier = self.v.product_supplier_field.currentText()

        product_cost = self.v.product_cost_field.text()
        product_retail_price = self.v.product_retail_price_field.text()
        product_wholesale_price = self.v.product_wholesale_price_field.text()
        product_price = self.v.product_price_field.text()
        product_effective_dt = self.v.product_effective_dt_field.date().toString(Qt.DateFormat.ISODate)
        product_promo_name = self.v.product_promo_name_field.currentText()
        product_promo_type = self.v.product_promo_type_field.text() if task == 'edit_data' else ''
        product_promo_percent = self.v.product_promo_percent_field.text() if task == 'edit_data' else '0'
        product_disc_value = self.v.product_disc_value_field.text() if task == 'edit_data' else '0'
        product_new_price = self.v.product_new_price_field.text() if task == 'edit_data' else '0'
        product_start_dt = self.v.product_start_dt_field.date().toString(Qt.DateFormat.ISODate) if task == 'edit_data' else '9999-99-99'
        product_end_dt = self.v.product_end_dt_field.date().toString(Qt.DateFormat.ISODate) if task == 'edit_data' else '9999-99-99'

        product_stock_tracking = self.v.product_stock_tracking_field.isChecked()

        self.m.init_manage_product_data_entry(
            self.v.manage_product_data_dialog,
            task,
            self.v.product_name_label,
            self.v.product_brand_label,
            self.v.product_sales_group_label,
            self.v.product_supplier_label,
            self.v.product_cost_label,
            self.v.product_retail_price_label,
            self.v.product_wholesale_price_label,
            self.v.product_price_label,
            self.v.product_effective_dt_label,

            product_barcode,
            product_name,
            product_expire_dt,

            product_type,
            product_brand,
            product_sales_group,
            product_supplier,

            product_cost,
            product_retail_price,
            product_wholesale_price,
            product_price,
            product_effective_dt,
            product_promo_name,
            product_promo_type,
            product_promo_percent,
            product_disc_value,
            product_new_price,
            product_start_dt,
            product_end_dt,
            
            product_stock_tracking
        )
            

        self.sync_ui()

    def sync_ui(self):
        text_filter = self.v.filter_field.text()
        self.m.total_product_page_number = schema.select_product_data_total_page_count(text=text_filter)
        self.m.total_stock_page_number = schema.select_stock_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_product_page_number > 0 or self.m.total_stock_page_number > 0 else 0
        self.populate_overview_table(text=text_filter, page_number=self.m.page_number)
        self.populate_stock_table(text=text_filter, page_number=self.m.page_number)
        pass
    def close_dialog(self, dialog: QDialog):
        dialog.close()

class MyProductWindow(MyGroupBox):
    def __init__(self, name='test', phone='test'):
        self.model = MyProductModel(name, phone)
        self.view = MyProductView(self.model)
        self.controller = MyProductController(self.model, self.view)

        self.set_box() # NOTE: comment this out if will be tested individually

    def set_box(self):
        super().__init__()

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        
    def run(self):
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    product_window = MyProductWindow()

    product_window.run()

    app.exec()