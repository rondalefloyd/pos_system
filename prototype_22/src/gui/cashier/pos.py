
import sys, os
import machineid
from datetime import *
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from src.gui.widget.my_widget import *
from src.core.sql.cashier.pos import MyPOSSchema
from src.core.sql.admin.product import MyProductSchema
from src.core.receipt_printer import ReceiptGenerator
from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

pos_schema = MyPOSSchema()
product_schema = MyProductSchema()

class MyPOSModel:
    def __init__(self, name, password, phone):
        self.cashier_info = [name, password, phone] # NAME AND PHONE OF CASHIER

        self.total_page_number = 0
        self.page_number = 1 if self.total_page_number > 0 else 0

        self.set_order_tab_content_container()
        
    def set_order_tab_content_container(self):
        self.order_number = 0
        self.sel_product_id = 0

        self.final_customer_name = ''
        self.final_customer_points_value = 0

        self.order_type_displays: List[MyLabel] = []
        self.customer_points_displays: List[MyLabel] = []
        self.customer_name_fields: List[MyComboBox] = []
        self.clear_order_table_buttons: List[MyPushButton] = []

        self.order_tables: List[MyTableWidget] = []

        self.order_subtotal_displays: List[MyLabel] = []
        self.order_discount_displays: List[MyLabel] = []
        self.order_tax_displays: List[MyLabel] = []
        self.order_total_displays: List[MyLabel] = []

        self.discard_order_buttons: List[MyPushButton] = []
        self.lock_order_toggle_buttons: List[MyPushButton] = []
        self.complete_order_buttons: List[MyPushButton] = []

        pass
    def append_order_tab_content_to_container(
            self,
            order_type_display,
            customer_points_display,
            customer_name_field,
            clear_order_table_button,
            order_table,
            order_subtotal_display,
            order_discount_display,
            order_tax_display,
            order_total_display,
            discard_order_button,
            lock_order_toggle_button,
            complete_order_button,
    ):
        self.order_type_displays.append(order_type_display)
        self.customer_points_displays.append(customer_points_display)
        self.customer_name_fields.append(customer_name_field)
        self.clear_order_table_buttons.append(clear_order_table_button)

        self.order_tables.append(order_table)

        self.order_subtotal_displays.append(order_subtotal_display)
        self.order_discount_displays.append(order_discount_display)
        self.order_tax_displays.append(order_tax_display)
        self.order_total_displays.append(order_total_display)

        self.discard_order_buttons.append(discard_order_button)
        self.lock_order_toggle_buttons.append(lock_order_toggle_button)
        self.complete_order_buttons.append(complete_order_button)
        pass
    def remove_order_tab_content_from_container(self, i:int):
        self.order_type_displays.remove(self.order_type_displays[i])
        self.customer_points_displays.remove(self.customer_points_displays[i])
        self.customer_name_fields.remove(self.customer_name_fields[i])
        self.clear_order_table_buttons.remove(self.clear_order_table_buttons[i])

        self.order_tables.remove(self.order_tables[i])

        self.order_subtotal_displays.remove(self.order_subtotal_displays[i])
        self.order_discount_displays.remove(self.order_discount_displays[i])
        self.order_tax_displays.remove(self.order_tax_displays[i])
        self.order_total_displays.remove(self.order_total_displays[i])

        self.discard_order_buttons.remove(self.discard_order_buttons[i])
        self.lock_order_toggle_buttons.remove(self.lock_order_toggle_buttons[i])
        self.complete_order_buttons.remove(self.complete_order_buttons[i])
    
    def append_final_order_info_for_receipt(
            self, 
            sales_group_id, 
            customer_id, 
            order_subtotal, 
            order_discount, 
            order_tax, 
            order_total, 
            payment_amount, 
            order_change, 
            final_order_table: QTableWidget,
            
            payment_type,
            cash_payment_amount,
            points_payment_amount,
            cash_points_payment_amount,
            current_date=QDate.currentDate().toString(Qt.DateFormat.ISODate)
    ):
        self.generate_transaction_info_entry(sales_group_id, customer_id)
        
        self.transaction_info = [self.transaction_date, self.ref, self.tin, self.min] # GENERATE STORE ADDRESS, TRANSACTION DATE, REF, TIN, MIN

        self.payment_type = 0
        self.cash_payment_amount = 0
        self.points_payment_amount = 0
        self.cash_points_payment_amount = [0,0]

        self.payment_type = payment_type
        self.cash_payment_amount = cash_payment_amount
        self.points_payment_amount = points_payment_amount
        self.cash_points_payment_amount = cash_points_payment_amount

        self.final_order_table = []
        
        if final_order_table.rowCount() > 0:
            for row_v in range(final_order_table.rowCount()):

                product_qty = final_order_table.item(row_v, 0).text()
                product_name = final_order_table.item(row_v, 1).text()
                product_amount = final_order_table.item(row_v, 2).text()

                date_id = pos_schema.select_date_id_by_date_value(current_date)
                product_id = pos_schema.select_product_id_by_name(product_name)
                product_price_id = pos_schema.select_product_price_id_by_product_id(product_id)
                product_stock_id = pos_schema.select_stock_id_by_item_id(product_id)
                user_id = pos_schema.select_user_id_by_name(self.cashier_info[0], self.cashier_info[1])

                self.final_order_table.append((product_qty, product_name, product_amount))

                pos_schema.insert_item_sold_data(
                    date_id=date_id,
                    customer_id=customer_id,
                    product_price_id=product_price_id,
                    product_stock_id=product_stock_id,
                    user_id=user_id,
                    product_qty=product_qty,
                    product_amount=product_amount,
                    reference_number=self.ref,
                )

                pos_schema.update_stock_on_hand(product_id, product_stock_id, product_qty)

        pos_schema.update_customer_reward_points_by_increment(customer_id, order_total)

        self.final_order_summary = [order_subtotal, order_discount, order_tax, order_total, payment_amount, order_change] # FOR SUBTOTAL, DISCOUNT, TAX, TOTAL, PAID AMOUNT, CHANGE
        pass
    def generate_transaction_info_entry(self, sales_group_id, customer_id):
        new_sales_group_id = f'{sales_group_id:02}'
        new_customer_id = f'{customer_id:05}'
        update_ts = f"{datetime.today().strftime('%y%m%d%H%M%S')}"
        
        self.transaction_date = f"{datetime.today().strftime('%b-%d-%Y')}"
        self.ref = f"{new_sales_group_id}-{new_customer_id}-{update_ts}"
        self.tin = f'40567264400000'
        self.min = f'{machineid.id()}'

        pass
    pass
class MyPOSView(MyGroupBox):
    def __init__(self, model: MyPOSModel):
        super().__init__(object_name='MyPOSView')

        self.m = model

        self.set_pos_box()

    def set_pos_box(self):
        self.filter_field = MyLineEdit(object_name='filter_field')
        self.filter_button = MyPushButton(object_name='filter_button', text='Filter')
        self.filter_box = MyGroupBox(object_name='filter_box')
        self.filter_layout = MyHBoxLayout(object_name='filter_layout')
        self.filter_layout.addWidget(self.filter_field)
        self.filter_layout.addWidget(self.filter_button)
        self.filter_box.setLayout(self.filter_layout)

        self.sync_ui_button = MyPushButton(object_name='sync_ui_button', text='Sync')
        self.barcode_scanner_field = MyLineEdit(object_name='barcode_scanner_field')
        self.barcode_scanner_toggle_button = [
            MyPushButton(object_name='toggle_barcode_scanner', text='On'),
            MyPushButton(object_name='untoggle_barcode_scanner', text='Off')
        ]
        self.barcode_scanner_box = MyGroupBox(object_name='barcode_scanner_box')
        self.barcode_scanner_layout = MyHBoxLayout(object_name='barcode_scanner_layout')
        self.barcode_scanner_layout.addWidget(self.sync_ui_button)
        self.barcode_scanner_layout.addWidget(self.barcode_scanner_field)
        self.barcode_scanner_layout.addWidget(self.barcode_scanner_toggle_button[0])
        self.barcode_scanner_layout.addWidget(self.barcode_scanner_toggle_button[1])
        self.barcode_scanner_box.setLayout(self.barcode_scanner_layout)

        self.pos_act_box = MyGroupBox(object_name='pos_act_box')
        self.pos_act_layout = MyHBoxLayout(object_name='pos_act_layout')
        self.pos_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.pos_act_layout.addWidget(self.barcode_scanner_box,1,Qt.AlignmentFlag.AlignRight)
        self.pos_act_box.setLayout(self.pos_act_layout)

        self.product_overview_table = MyTableWidget(object_name='pos_overview_table')
        self.product_overview_prev_button = MyPushButton(object_name='overview_prev_button', text='Prev')
        self.product_overview_page_label = MyLabel(object_name='overview_page_label', text=f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.product_overview_next_button = MyPushButton(object_name='overview_next_button', text='Next')
        self.product_display_box = MyGroupBox(object_name='overview_act_box')
        self.product_display_layout = MyHBoxLayout(object_name='overview_act_layout')
        self.product_display_layout.addWidget(self.product_overview_prev_button)
        self.product_display_layout.addWidget(self.product_overview_page_label)
        self.product_display_layout.addWidget(self.product_overview_next_button)
        self.product_display_box.setLayout(self.product_display_layout)
        self.product_overview_box = MyGroupBox()
        self.product_overview_layout = MyVBoxLayout()
        self.product_overview_layout.addWidget(self.product_overview_table)
        self.product_overview_layout.addWidget(self.product_display_box,0,Qt.AlignmentFlag.AlignCenter)
        self.product_overview_box.setLayout(self.product_overview_layout)
        
        self.pos_sort_tab = MyTabWidget()
        self.pos_sort_tab.addTab(self.product_overview_box, 'Overview')

        self.order_index_label = MyLabel(object_name='order_index_label', text='No order')
        self.order_type_field = MyComboBox(object_name='order_type_field')
        self.add_order_button = MyPushButton(object_name='add_order_button', text='Add order')
        self.manage_order_act_box = MyGroupBox(object_name='manage_order_act_box')
        self.manage_order_act_layout = MyHBoxLayout(object_name='manage_order_act_layout')
        self.manage_order_act_layout.addWidget(self.order_index_label,0,Qt.AlignmentFlag.AlignLeft)
        self.manage_order_act_layout.addWidget(self.order_type_field,1,Qt.AlignmentFlag.AlignRight)
        self.manage_order_act_layout.addWidget(self.add_order_button,0,Qt.AlignmentFlag.AlignRight)
        self.manage_order_act_box.setLayout(self.manage_order_act_layout)

        self.order_empty_tab_box = MyGroupBox(object_name='order_empty_tab_box')
        self.order_empty_tab_layout = MyVBoxLayout(object_name='order_empty_tab_layout')
        self.order_empty_add_order_button = MyPushButton(object_name='order_empty_add_order_button', text='Add order')
        self.order_empty_tab_layout.addWidget(self.order_empty_add_order_button)
        self.order_empty_tab_box.setLayout(self.order_empty_tab_layout)

        self.manage_order_tab = MyTabWidget(object_name='manage_order_tab')

        self.manage_order_box = MyGroupBox(object_name='manage_order_box')
        self.manage_order_layout = MyVBoxLayout(object_name='manage_order_layout')
        self.manage_order_layout.addWidget(self.manage_order_act_box)
        self.manage_order_layout.addWidget(self.manage_order_tab)
        self.manage_order_layout.addWidget(self.order_empty_tab_box)
        self.manage_order_box.setLayout(self.manage_order_layout)

        self.main_layout = MyGridLayout(object_name='main_layout')
        self.main_layout.addWidget(self.pos_act_box,0,0)
        self.main_layout.addWidget(self.pos_sort_tab,1,0)
        self.main_layout.addWidget(self.manage_order_box,0,1,2,1)
        self.setLayout(self.main_layout)

    def set_progress_dialog(self, action=''):
        if action == 'print_receipt':
            # self.progress_bar = MyProgressBar()
            self.progress_label = MyLabel(text='Please wait...')
            self.progress_dialog = MyDialog(object_name='progress_dialog', window_title='Step 0 out of ?')
            self.progress_layout = MyVBoxLayout(object_name='progress_layout')
            # self.progress_layout.addWidget(self.progress_bar)
            self.progress_layout.addWidget(self.progress_label)
            self.progress_dialog.setLayout(self.progress_layout)
            pass
        elif action == 'save_receipt':
            # self.progress_bar = MyProgressBar()
            self.progress_label = MyLabel(text='Saving receipt...')
            self.progress_dialog = MyDialog(object_name='progress_dialog', window_title='Saving')
            self.progress_layout = MyVBoxLayout(object_name='progress_layout')
            # self.progress_layout.addWidget(self.progress_bar)
            self.progress_layout.addWidget(self.progress_label)
            self.progress_dialog.setLayout(self.progress_layout)
        pass

    def set_overview_table_product_display_box(self, data):
        # self.product_display_label = MyLabel()
        # self.product_display_image = QPixmap(qss.product_icon)
        # self.product_display_image = self.product_display_image.scaled(30,30,Qt.AspectRatioMode.KeepAspectRatio)

        self.product_name_label = MyLabel(object_name='product_name_label', text=f"{data[0]}")
        self.product_promo_indicator = MyPushButton(object_name='product_promo_indicator')
        self.out_of_stock_indicator = MyPushButton(object_name='out_of_stock_indicator')
        self.product_name_layout = MyHBoxLayout(object_name='product_name_layout')
        self.product_name_layout.addWidget(self.product_name_label,0,Qt.AlignmentFlag.AlignLeft)
        self.product_name_layout.addWidget(self.product_promo_indicator,1,Qt.AlignmentFlag.AlignLeft)
        # self.product_name_layout.addWidget(self.out_of_stock_indicator,2,Qt.AlignmentFlag.AlignLeft)

        self.product_brand_label = MyLabel(object_name='product_brand_label', text=f"{data[1]}")
        self.product_barcode_label = MyLabel(object_name='product_barcode_label', text=f"{data[2]}")

        self.product_price_label = MyLabel(object_name='product_price_label', text=f"{data[3]}")
        self.product_disc_value_label = MyLabel(object_name='product_disc_value_label', text=f"{data[4]}")
        # self.product_onhand_label = MyLabel(object_name='product_onhand_label', text=f"Stock: {data[6]}")
        self.product_pricing_layout = MyVBoxLayout(object_name='product_pricing_layout')
        self.product_pricing_layout.addWidget(self.product_price_label)
        self.product_pricing_layout.addWidget(self.product_disc_value_label)
        # self.product_pricing_layout.addWidget(self.product_onhand_label)

        self.product_info_box = MyGroupBox(object_name='product_info_box')
        self.product_info_layout = MyVBoxLayout(object_name='product_info_layout')
        self.product_info_layout.addWidget(self.product_barcode_label)
        self.product_info_layout.addLayout(self.product_name_layout)
        self.product_info_layout.addWidget(self.product_brand_label)
        self.product_info_layout.addLayout(self.product_pricing_layout)
        self.product_info_box.setLayout(self.product_info_layout)

        self.add_products_button = MyPushButton(object_name='add_products_button', text='Add')
        self.view_data_button = MyPushButton(object_name='view_data_button', text='View')
        self.product_cell_display_act_box = MyGroupBox(object_name='product_cell_display_act_box')
        self.product_cell_display_act_layout = MyHBoxLayout(object_name='product_cell_display_act_layout')
        self.product_cell_display_act_layout.addWidget(self.add_products_button,1,Qt.AlignmentFlag.AlignRight)
        self.product_cell_display_act_layout.addWidget(self.view_data_button)
        self.product_cell_display_act_box.setLayout(self.product_cell_display_act_layout)

        self.product_cell_display_box = MyGroupBox(object_name='product_cell_display_box')
        self.product_cell_display_layout = MyVBoxLayout(object_name='pos_overview_act_layout')
        self.product_cell_display_layout.addWidget(self.product_info_box)
        self.product_cell_display_layout.addWidget(self.product_cell_display_act_box)
        self.product_cell_display_box.setLayout(self.product_cell_display_layout)

    def set_view_dialog(self, data):
        self.product_barcode_info = MyLabel(text=f"{data[0]}")
        self.product_name_info = MyLabel(text=f"{data[1]}")
        self.product_expire_dt_info = MyLabel(text=f"{data[2]}")

        self.product_type_info = MyLabel(text=f"{data[3]}")
        self.product_brand_info = MyLabel(text=f"{data[4]}")
        self.product_sales_group_info = MyLabel(text=f"{data[5]}")
        self.product_supplier_info = MyLabel(text=f"{data[6]}")

        self.product_cost_info = MyLabel(text=f"{data[7]}")
        self.product_price_info = MyLabel(text=f"{data[8]}")
        self.product_effective_dt_info = MyLabel(text=f"{data[9]}")
        self.product_promo_name_info = MyLabel(text=f"{data[10]}")
        self.product_disc_value_info = MyLabel(text=f"{data[11]}")

        self.product_stock_tracking_info = MyLabel(text=f"{data[12]}")
        self.product_stock_on_hand_info = MyLabel(text=f"{data[13]}")

        self.product_datetime_created_info = MyLabel(text=f"{data[14]}")

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
        # self.info_layout.addRow(MyLabel(text='<hr>'))
        # self.info_layout.addRow('Inventory tracking:', self.product_stock_tracking_info)
        # self.info_layout.addRow('On hand:', self.product_stock_on_hand_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Date/Time created:', self.product_datetime_created_info)

        self.info_box.setLayout(self.info_layout)
        self.view_data_scra = MyScrollArea(object_name='view_data_scra')
        self.view_data_scra.setWidget(self.info_box)

        self.view_data_act_close_button = MyPushButton(object_name='close_button', text='Close')
        self.view_data_act_box = MyGroupBox(object_name='view_data_act_box')
        self.view_data_act_layout = MyHBoxLayout(object_name='view_data_act_layout')
        self.view_data_act_layout.addWidget(self.view_data_act_close_button,0,Qt.AlignmentFlag.AlignRight)
        self.view_data_act_box.setLayout(self.view_data_act_layout)

        self.view_data_dialog = MyDialog(object_name='view_data_dialog')
        self.view_data_layout = MyVBoxLayout(object_name='view_data_layout')
        self.view_data_layout.addWidget(self.view_data_scra)
        self.view_data_layout.addWidget(self.view_data_act_box)
        self.view_data_dialog.setLayout(self.view_data_layout)
        pass
    
    def set_order_box(self):
        self.customer_name_label = MyLabel(object_name='customer_name_label', text='Customer:')
        self.customer_name_field = MyComboBox(object_name='customer_name_field')
        self.customer_data_sub_layout = MyHBoxLayout(object_name='customer_data_sub_layout')
        self.customer_data_sub_layout.addWidget(self.customer_name_label)
        self.customer_data_sub_layout.addWidget(self.customer_name_field)
        self.customer_points_display = MyLabel(object_name='customer_points_display', text='Points: <b>N/A</b>')
        self.customer_data_box = MyGroupBox()
        self.customer_data_layout = MyVBoxLayout(object_name='customer_data_layout')
        self.customer_data_layout.addLayout(self.customer_data_sub_layout)
        self.customer_data_layout.addWidget(self.customer_points_display)
        self.customer_data_box.setLayout(self.customer_data_layout)
        self.order_type_display = MyLabel(object_name='order_type_display', text='N/A')
        self.clear_order_table_button = MyPushButton(object_name='clear_order_table_button', text='Clear')
        self.order_act_a_box = MyGroupBox(object_name='order_act_a_box')
        self.order_act_a_layout = MyHBoxLayout(object_name='order_act_a_layout')
        self.order_act_a_layout.addWidget(self.customer_data_box,0,Qt.AlignmentFlag.AlignLeft)
        self.order_act_a_layout.addWidget(self.order_type_display,1,Qt.AlignmentFlag.AlignRight)
        self.order_act_a_layout.addWidget(self.clear_order_table_button,0,Qt.AlignmentFlag.AlignRight)
        self.order_act_a_box.setLayout(self.order_act_a_layout)

        self.order_table = MyTableWidget(object_name='order_table')

        self.order_subtotal_display = MyLabel(object_name='order_subtotal_display', text=f"0.00")
        self.order_discount_display = MyLabel(object_name='order_discount_display', text=f"0.00")
        self.order_tax_display = MyLabel(object_name='order_tax_display', text=f"0.00")
        self.order_total_display = MyLabel(object_name='order_total_display', text=f"0.00")
        self.order_summary_box = MyGroupBox(object_name='order_summary_box')
        self.order_summary_layout = MyFormLayout(object_name='order_summary_layout')
        self.order_summary_layout.addRow(MyLabel(object_name='order_subtotal_display', text='Subtotal'), self.order_subtotal_display)
        self.order_summary_layout.addRow(MyLabel(object_name='order_discount_display', text='Discount'), self.order_discount_display)
        self.order_summary_layout.addRow(MyLabel(object_name='order_tax_display', text='Tax'), self.order_tax_display)
        self.order_summary_layout.addRow(MyLabel(object_name='order_total_display', text='Total'), self.order_total_display)
        self.order_summary_box.setLayout(self.order_summary_layout)

        self.discard_order_button = MyPushButton(object_name='discard_order_button', text='Discard')
        self.lock_order_toggle_button = [
            MyPushButton(object_name='toggle_lock_order', text='Unlocked'),
            MyPushButton(object_name='untoggle_lock_order', text='Locked')
        ]   
        self.extra_order_act_b_layout = MyHBoxLayout(object_name='extra_order_act_b_layout')
        self.extra_order_act_b_layout.addWidget(self.discard_order_button)
        self.extra_order_act_b_layout.addWidget(self.lock_order_toggle_button[0],1,Qt.AlignmentFlag.AlignLeft)
        self.extra_order_act_b_layout.addWidget(self.lock_order_toggle_button[1],1,Qt.AlignmentFlag.AlignLeft)

        self.complete_order_button = MyPushButton(object_name='complete_order_button', text=f"COMPLETE ORDER")
        self.order_act_b_box = MyGroupBox(object_name='order_act_b_box')
        self.order_act_b_layout = MyVBoxLayout(object_name='order_act_b_layout')
        self.order_act_b_layout.addLayout(self.extra_order_act_b_layout)
        self.order_act_b_layout.addWidget(self.complete_order_button)
        self.order_act_b_box.setLayout(self.order_act_b_layout)

        self.order_box = MyGroupBox(object_name='order_box')
        self.order_layout = MyVBoxLayout(object_name='order_layout')
        self.order_layout.addWidget(self.order_act_a_box)
        self.order_layout.addWidget(self.order_table)
        self.order_layout.addWidget(self.order_summary_box)
        self.order_layout.addWidget(self.order_act_b_box)
        self.order_box.setLayout(self.order_layout)

    def set_order_table_act_box(self):
        self.drop_all_qty_button = MyPushButton(object_name='drop_all_qty_button', text='Drop all')
        self.drop_qty_button = MyPushButton(object_name='drop_qty_button', text='Drop')
        self.add_qty_button = MyPushButton(object_name='add_qty_button', text='Add')
        self.edit_qty_button = MyPushButton(object_name='edit_qty_button', text='Edit')
        self.order_table_act_box = MyGroupBox(object_name='order_table_act_box')
        self.order_table_act_layout = MyGridLayout(object_name='order_table_act_layout')
        self.order_table_act_layout.addWidget(self.drop_all_qty_button,0,0)
        self.order_table_act_layout.addWidget(self.drop_qty_button,0,1)
        self.order_table_act_layout.addWidget(self.add_qty_button,1,1)
        self.order_table_act_layout.addWidget(self.edit_qty_button,1,0)
        self.order_table_act_box.setLayout(self.order_table_act_layout)

    def set_pay_order_dialog(self):
        self.final_order_table = MyTableWidget(object_name='final_order_table')

        self.final_order_subtotal_display = MyLabel(object_name='final_order_subtotal_display', text=f"{'test'}")
        self.final_order_discount_display = MyLabel(object_name='final_order_discount_display', text=f"{'test'}")
        self.final_order_tax_display = MyLabel(object_name='final_order_tax_display', text=f"{'test'}")
        self.final_order_total_display = MyLabel(object_name='final_order_total_display', text=f"{'test'}")
        self.final_order_summary_box = MyGroupBox(object_name='final_order_summary_box')
        self.final_order_summary_layout = MyFormLayout(object_name='final_order_summary_layout')
        self.final_order_summary_layout.addRow(MyLabel(object_name='final_order_subtotal_display', text='Subtotal'), self.final_order_subtotal_display)
        self.final_order_summary_layout.addRow(MyLabel(object_name='final_order_discount_display', text='Discount'), self.final_order_discount_display)
        self.final_order_summary_layout.addRow(MyLabel(object_name='final_order_tax_display', text='Tax'), self.final_order_tax_display)
        self.final_order_summary_layout.addRow(MyLabel(object_name='final_order_total_display', text='Total'), self.final_order_total_display)
        self.final_order_summary_box.setLayout(self.final_order_summary_layout)
        self.pay_order_a_box = MyGroupBox(object_name='pay_order_a_box')
        self.payment_a_layout = MyVBoxLayout(object_name='payment_a_layout')
        self.payment_a_layout.addWidget(self.final_order_table)
        self.payment_a_layout.addWidget(self.final_order_summary_box)
        self.pay_order_a_box.setLayout(self.payment_a_layout)

        self.tender_amount_label = MyLabel(object_name='tender_amount_label', text='Amount tendered')
        self.tender_amount_field = MyLineEdit(object_name='tender_amount_field')
        self.numpad_key_toggle_button = [
            MyPushButton(object_name='toggle_numpad_key'),
            MyPushButton(object_name='untoggle_numpad_key'),
        ]
        self.numpad_key_button = [
            MyPushButton(object_name='numpad_key_button', text='1'),
            MyPushButton(object_name='numpad_key_button', text='2'),
            MyPushButton(object_name='numpad_key_button', text='3'),
            MyPushButton(object_name='numpad_key_button', text='4'),
            MyPushButton(object_name='numpad_key_button', text='5'),
            MyPushButton(object_name='numpad_key_button', text='6'),
            MyPushButton(object_name='numpad_key_button', text='7'),
            MyPushButton(object_name='numpad_key_button', text='8'),
            MyPushButton(object_name='numpad_key_button', text='9'),
            MyPushButton(object_name='numpad_key_button', text='Del'),
            MyPushButton(object_name='numpad_key_button', text='0'),
            MyPushButton(object_name='numpad_key_button', text='.'),
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

        self.cash_payment_compute_label = MyLabel(object_name='cash_payment_compute_label', text='Cash payment')
        self.points_payment_compute_label = MyLabel(object_name='points_payment_compute_label', text='Points payment')
        self.cash_points_payment_compute_label = MyLabel(object_name='cash_points_payment_compute_label', text='Cash + Points payment')
        self.cash_payment_compute_display = MyLabel(object_name='cash_payment_compute_label', text='0.00')
        self.points_payment_compute_display = MyLabel(object_name='points_payment_compute_label', text='0.00')
        self.cash_points_payment_compute_display = MyLabel(object_name='cash_points_payment_compute_label', text='0.00')
        self.payment_amount_compute_box = MyGroupBox(object_name='payment_amount_compute_box')
        self.payment_amount_compute_layout = MyFormLayout(object_name='payment_amount_compute_layout')
        # self.payment_amount_compute_layout.addRow(MyLabel(object_name='required_amount_label', text='<b>Required amount</b>'))
        self.payment_amount_compute_layout.addRow(self.cash_payment_compute_label, self.cash_payment_compute_display)
        self.payment_amount_compute_layout.addRow(self.points_payment_compute_label, self.points_payment_compute_display)
        self.payment_amount_compute_layout.addRow(self.cash_points_payment_compute_label, self.cash_points_payment_compute_display)
        self.payment_amount_compute_box.setLayout(self.payment_amount_compute_layout)

        self.pay_order_b_box = MyGroupBox(object_name='pay_order_b_box')
        self.payment_b_layout = MyGridLayout(object_name='payment_b_layout')
        self.payment_b_layout.addWidget(self.tender_amount_label,0,0,Qt.AlignmentFlag.AlignCenter)
        self.payment_b_layout.addWidget(self.tender_amount_field,1,0)
        # self.payment_b_layout.addWidget(self.numpad_key_toggle_button[0],1,1)
        # self.payment_b_layout.addWidget(self.numpad_key_toggle_button[1],1,1)
        self.payment_b_layout.addWidget(self.numpad_key_box,2,0,1,2)
        self.payment_b_layout.addWidget(self.payment_amount_compute_box,3,0,1,2)
        self.pay_order_b_box.setLayout(self.payment_b_layout)
        
    
        self.final_customer_name_display = MyLabel(text=f"Customer: {'test'}")
        self.final_customer_phone_display = MyLabel(text=f"Phone: {'test'}")
        self.final_customer_points_display = MyLabel(text=f"Points: {'0'}")
        self.final_customer_info_box = MyGroupBox(object_name='final_customer_info_box')
        self.final_customer_info_layout = MyHBoxLayout(object_name='final_customer_info_layout')
        self.final_customer_info_layout.addWidget(self.final_customer_name_display)
        self.final_customer_info_layout.addWidget(self.final_customer_phone_display)
        self.final_customer_info_layout.addWidget(self.final_customer_points_display)
        self.final_customer_info_box.setLayout(self.final_customer_info_layout)
        self.pay_cash_button = MyPushButton(object_name='pay_cash_button', text=f"Cash")
        self.pay_points_button = MyPushButton(object_name='pay_points_button', text=f"Points")
        self.pay_cash_points_button = MyPushButton(object_name='pay_cash_points_button', text=f"Cash + Points")
        self.payment_c_box = MyGroupBox(object_name='payment_c_box') 
        self.payment_act_layout = MyHBoxLayout(object_name='payment_act_layout')
        self.payment_act_layout.addWidget(self.final_customer_info_box,0,Qt.AlignmentFlag.AlignLeft)
        self.payment_act_layout.addWidget(self.pay_cash_points_button,2,Qt.AlignmentFlag.AlignRight)
        self.payment_act_layout.addWidget(self.pay_points_button,0,Qt.AlignmentFlag.AlignRight)
        self.payment_act_layout.addWidget(self.pay_cash_button,0,Qt.AlignmentFlag.AlignRight)
        self.payment_c_box.setLayout(self.payment_act_layout)

        self.pay_order_dialog = MyDialog(object_name='pay_order_dialog', window_title='Payment')
        self.pay_order_layout = MyGridLayout(object_name='pay_order_layout')
        self.pay_order_layout.addWidget(self.pay_order_a_box,0,0)
        self.pay_order_layout.addWidget(self.pay_order_b_box,0,1,Qt.AlignmentFlag.AlignTop)
        self.pay_order_layout.addWidget(self.payment_c_box,1,0,1,2,Qt.AlignmentFlag.AlignBottom)
        self.pay_order_dialog.setLayout(self.pay_order_layout)

    def setup_transaction_complete_dialog(self):
        self.transaction_order_total_amount_label = MyLabel(object_name='transaction_order_total_amount_label', text='Total amount')
        self.transaction_order_total_amount_display = MyLabel(object_name='transaction_order_total_amount_display', text=f"{'100.00'}")
        self.transaction_payment_amount_label = MyLabel(object_name='transaction_payment_amount_label', text='Paid amount')
        self.transaction_payment_amount_display = MyLabel(object_name='transaction_payment_amount_display', text=f"{'100.00'}")
        self.transaction_order_change_label = MyLabel(object_name='transaction_order_change_label', text='Change')
        self.transaction_order_change_display = MyLabel(object_name='transaction_order_change_display', text=f"{'100.00'}")
        self.transaction_info_box = MyGroupBox(object_name='transaction_info_box')
        self.transaction_info_layout = MyVBoxLayout(object_name='transaction_info_layout')
        self.transaction_info_layout.addWidget(self.transaction_order_total_amount_label,0,Qt.AlignmentFlag.AlignCenter)
        self.transaction_info_layout.addWidget(self.transaction_order_total_amount_display,0,Qt.AlignmentFlag.AlignCenter)
        self.transaction_info_layout.addWidget(self.transaction_payment_amount_label,0,Qt.AlignmentFlag.AlignCenter)
        self.transaction_info_layout.addWidget(self.transaction_payment_amount_display,0,Qt.AlignmentFlag.AlignCenter)
        self.transaction_info_layout.addWidget(self.transaction_order_change_label,0,Qt.AlignmentFlag.AlignCenter)
        self.transaction_info_layout.addWidget(self.transaction_order_change_display,0,Qt.AlignmentFlag.AlignCenter)
        self.transaction_info_box.setLayout(self.transaction_info_layout)

        self.print_receipt_button = MyPushButton(object_name='print_receipt_button', text='Print receipt')
        self.save_receipt_button = MyPushButton(object_name='save_receipt_button', text='Save')
        self.manage_receipt_layout = MyHBoxLayout(object_name='manage_receipt_layout')
        self.manage_receipt_layout.addWidget(self.print_receipt_button)
        self.manage_receipt_layout.addWidget(self.save_receipt_button)
        self.add_new_order_button = MyPushButton(object_name='add_new_order_button', text='Add new order')

        self.transaction_complete_act_a_box = MyGroupBox(object_name='transaction_complete_act_a_box')
        self.transaction_complete_act_a_layout = MyVBoxLayout(object_name='transaction_complete_act_a_layout')
        self.transaction_complete_act_a_layout.addWidget(self.print_receipt_button)
        self.transaction_complete_act_a_layout.addWidget(self.add_new_order_button)
        self.transaction_complete_act_a_box.setLayout(self.transaction_complete_act_a_layout)

        self.transaction_complete_summary_box = MyGroupBox(object_name='txn_complete_summary_box')
        self.transaction_complete_summary_layout = MyVBoxLayout(object_name='txn_complete_summary_layout')
        self.transaction_complete_summary_layout.addWidget(self.transaction_info_box,1,Qt.AlignmentFlag.AlignCenter)
        self.transaction_complete_summary_layout.addWidget(self.transaction_complete_act_a_box,1,Qt.AlignmentFlag.AlignCenter)
        self.transaction_complete_summary_box.setLayout(self.transaction_complete_summary_layout)

        self.transaction_complete_close_button = MyPushButton(object_name='close_button', text='Close')
        self.transaction_complete_act_b_box = MyGroupBox('transaction_complete_act_b_box')
        self.transaction_complete_act_b_layout = MyHBoxLayout('transaction_complete_act_b_layout')
        self.transaction_complete_act_b_layout.addWidget(self.transaction_complete_close_button,0,Qt.AlignmentFlag.AlignRight)
        self.transaction_complete_act_b_box.setLayout(self.transaction_complete_act_b_layout)
        
        self.transaction_complete_dialog = MyDialog(object_name='transaction_complete_dialog', window_title='Transaction summary')
        self.transaction_complete_layout = MyVBoxLayout(object_name='transaction_complete_layout')
        self.transaction_complete_layout.addWidget(self.transaction_complete_summary_box,0,Qt.AlignmentFlag.AlignTop)
        self.transaction_complete_layout.addWidget(self.transaction_complete_act_b_box,0,Qt.AlignmentFlag.AlignBottom)
        self.transaction_complete_dialog.setLayout(self.transaction_complete_layout)
    pass
class MyPOSController:
    def __init__(self, model: MyPOSModel, view: MyPOSView):
        self.v = view
        self.m = model

        self.set_pos_box_conn()
        self.set_order_box_conn()
        self.load_combo_box_data_handler(load='global')
        self.sync_ui_handler()
        self.panel_add_order_handler()

        # if self.v.manage_order_tab.count() <= 0:
    
    def set_pos_box_conn(self):
        self.v.order_empty_add_order_button.clicked.connect(self.on_add_order_button_clicked)

        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)

        self.v.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.v.barcode_scanner_field.returnPressed.connect(self.on_barcode_scanner_field_return_pressed)
        self.v.barcode_scanner_toggle_button[0].clicked.connect(lambda: self.on_barcode_scanner_toggle_button_clicked(flag=True))
        self.v.barcode_scanner_toggle_button[1].clicked.connect(lambda: self.on_barcode_scanner_toggle_button_clicked(flag=False))

        self.v.product_overview_prev_button.clicked.connect(self.on_overview_prev_button_clicked)
        self.v.product_overview_next_button.clicked.connect(self.on_overview_next_button_clicked)
        pass
    def on_filter_button_clicked(self): # IDEA: src
        try:
            i = self.v.manage_order_tab.currentIndex()

            text_filter = self.v.filter_field.text()
            order_type = self.m.order_type_displays[i].text()
            
            self.m.total_page_number = pos_schema.select_product_data_total_page_count(text=text_filter, order_type=order_type)
            self.m.page_number = 1 if self.m.total_page_number > 0 else 0

            self.v.product_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
            
            self.populate_overview_table(text=text_filter, order_type=order_type, page_number=self.m.page_number)
        except Exception as e:
            # self.populate_overview_table(page_number=self.m.page_number)
            pass
        pass
    def on_sync_ui_button_clicked(self):
        self.load_combo_box_data_handler(load='order_box')
        self.sync_ui_handler()
        pass
    def on_barcode_scanner_toggle_button_clicked(self, flag):
        if flag is True:
            self.v.barcode_scanner_toggle_button[0].hide()
            self.v.barcode_scanner_toggle_button[1].show()
            pass
        elif flag is False:
            self.v.barcode_scanner_toggle_button[0].show()
            self.v.barcode_scanner_toggle_button[1].hide()
            self.v.barcode_scanner_field.setFocus()
            pass

        self.v.barcode_scanner_field.setHidden(flag)
        pass
    def on_barcode_scanner_field_return_pressed(self):
        # 4800015401007
        try:
            i = self.v.manage_order_tab.currentIndex()

            product_barcode = str(self.v.barcode_scanner_field.text())
            
            if self.m.lock_order_toggle_buttons[i][0].isHidden() == False:

                if self.v.barcode_scanner_field.text() != '':
                    product_data = pos_schema.select_product_data_with_barcode(barcode=product_barcode, order_type=self.m.order_type_displays[i].text())
                    
                    # 8850006344200 test barcode
            
                    if product_data[1] != 0 and product_data[2] != 0:
                        self.set_initial_add_product_entry(product_name=product_data[0], product_price_id=product_data[1], product_id=product_data[2])
                    else:
                        QMessageBox.critical(self.v, 'Error', 'Item unavailable .')
                else:
                    QMessageBox.critical(self.v, 'Error', 'Invalid barcode.')
            else:
                QMessageBox.critical(self.v, 'Error', 'Please unlock the table first.')
                
        except Exception as e:
            QMessageBox.critical(self.v, 'Error', f'Please add a table first.')
            pass
        self.v.barcode_scanner_field.clear()
        product_barcode = ''
        product_data = []

    # FIXME NEEDS TO GETS FIXED
    def populate_overview_table(self, text='', order_type='', page_number=1): # IDEA: src
        self.v.product_overview_prev_button.setEnabled(page_number > 1)
        self.v.product_overview_next_button.setEnabled(page_number < self.m.total_page_number)
        self.v.product_overview_page_label.setText(f"Page {page_number}/{self.m.total_page_number}")

        product_data = pos_schema.select_product_data_as_display(text=text, order_type=order_type, page_number=page_number)
        
        if len(product_data) > 0:
            num_columns = min(3, len(product_data))  # Set num_columns to 3 or less if there are fewer items in product_data
            num_rows = -(-len(product_data) // num_columns)  # Equivalent to math.ceil(len(product_data) / num_columns)
        else:
            num_columns = 0
            num_rows = 0

        self.v.product_overview_table.clear()
        self.v.product_overview_table.setColumnCount(num_columns)
        self.v.product_overview_table.setRowCount(num_rows)


        for i, data in enumerate(product_data):
            self.v.set_overview_table_product_display_box(data)

            if data[11]: self.v.product_promo_indicator.show()
            if data[6] is not None and data[6] <= 0:
                # self.v.out_of_stock_indicator.show()
                pass
                
            column = i % num_columns  # Determine the column based on the index
            row = i // num_columns  # Determine the row based on the index

            self.v.product_overview_table.setCellWidget(row, column, self.v.product_cell_display_box)
            self.v.product_overview_table.setItem(row, column, MyTableWidgetItem(text='')) # NOTE: this is a temporary fix. might find other solution to fix product_overview_table display bug

            self.v.add_products_button.clicked.connect(lambda _, data=data: self.on_add_products_button_clicked(data))
            self.v.view_data_button.clicked.connect(lambda _, data=data: self.on_view_data_button_clicked(data))
        pass
    def on_add_products_button_clicked(self, data):
        i = self.v.manage_order_tab.currentIndex()

        if self.m.lock_order_toggle_buttons[i][0].isHidden() is False:
            proposed_qty, confirm = QInputDialog.getInt(self.v, f"{data[0]}", 'Set quantity:', 1, 1, 9999)

            if confirm is True:
                self.set_initial_add_product_entry(product_qty=proposed_qty, product_name=data[0], product_price_id=data[9], product_id=data[10])
        
        else:
            QMessageBox.critical(self.v, 'Error', 'Please unlock the table first.')
        self.v.barcode_scanner_field.setFocus()
        pass
    def on_view_data_button_clicked(self, data):
        product_name = str(data[0])
        product_barcode = str(data[2])

        product_data = pos_schema.select_product_data_for_view_dialog(product_name, product_barcode)


        self.v.set_view_dialog(product_data)
        self.v.view_data_dialog.setWindowTitle(f"{product_name}")

        self.set_view_data_box_conn()
        self.v.view_data_dialog.exec()
        self.v.barcode_scanner_field.setFocus()

        pass
    def set_view_data_box_conn(self):
        self.v.view_data_act_close_button.clicked.connect(lambda: self.close_dialog_handler(self.v.view_data_dialog))

    def on_overview_prev_button_clicked(self):
        i = self.v.manage_order_tab.currentIndex()

        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.product_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        
        self.populate_overview_table(text=self.v.filter_field.text(), order_type=self.m.order_type_displays[i].text(), page_number=self.m.page_number)
        pass
    def on_overview_next_button_clicked(self):
        i = self.v.manage_order_tab.currentIndex()

        if self.m.page_number < self.m.total_page_number:
            self.m.page_number += 1

            self.v.product_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        
        self.populate_overview_table(text=self.v.filter_field.text(), order_type=self.m.order_type_displays[i].text(), page_number=self.m.page_number)
        pass

    def set_order_box_conn(self): #IDEA: src
        self.v.add_order_button.clicked.connect(self.on_add_order_button_clicked)
        self.v.manage_order_tab.currentChanged.connect(self.on_manage_order_tab_current_changed)
        pass
    def on_manage_order_tab_current_changed(self):
        try:
            i = self.v.manage_order_tab.currentIndex()

            order_tab_name = self.v.manage_order_tab.tabText(i)

            for tab_i in range(self.v.manage_order_tab.count()):
                if self.v.manage_order_tab.tabText(tab_i) == order_tab_name:
                    self.m.customer_name_fields[i].setCurrentText(self.m.customer_name_fields[tab_i].currentText())
        except Exception as e:
            pass
                
        self.sync_ui_handler()
        self.v.barcode_scanner_field.setFocus()
        pass
    def on_add_order_button_clicked(self):
        if self.v.order_type_field.currentText() in ['Retail','Wholesale']:
            self.m.order_number += 1
            self.add_order_handler()
        elif self.v.order_type_field.currentText() == 'Dual':
            self.m.order_number += 1
            self.add_order_handler(order_type_display='Retail')
            self.add_order_handler(order_type_display='Wholesale')

        self.v.order_type_field.setCurrentIndex(0)
        self.panel_add_order_handler()
        self.sync_ui_handler()
        self.v.barcode_scanner_field.setFocus()
        # self.test_prints()
        pass

    def set_order_tab_content_conn(self):
        self.v.customer_name_field.currentTextChanged.connect(self.on_customer_name_field_current_text_changed)
        self.v.clear_order_table_button.clicked.connect(self.on_clear_order_table_button_clicked)
        self.v.discard_order_button.clicked.connect(self.on_discard_order_button_clicked)
        self.v.lock_order_toggle_button[0].clicked.connect(lambda: self.on_lock_order_toggle_button_clicked(lock=True))
        self.v.lock_order_toggle_button[1].clicked.connect(lambda: self.on_lock_order_toggle_button_clicked(lock=False))
        self.v.complete_order_button.clicked.connect(self.on_complete_order_button_clicked)
        pass
    def on_customer_name_field_current_text_changed(self):
        i = self.v.manage_order_tab.currentIndex()

        customer_name = self.m.customer_name_fields[i].currentText()
        customer_data = pos_schema.select_customer_data_with_customer_reward_data(customer_name=customer_name)
        customer_points = str(customer_data[2])
        
        if customer_data[0] != 'N/A' and customer_data[1] != 'N/A':
            self.m.customer_points_displays[i].setText(f'Points: <b>{customer_points}</b>')
        else:
            self.m.customer_points_displays[i].setText(f'Points: <b>N/A</b>')
        pass
    def on_clear_order_table_button_clicked(self):
        i = self.v.manage_order_tab.currentIndex()

        if self.m.order_tables[i].rowCount() > 0:
            confirm = QMessageBox.question(self.v, 'Confirm', 'Clear this order table?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if confirm is QMessageBox.StandardButton.Yes:
                self.set_clear_order_table_entry()

        else:
            QMessageBox.critical(self.v, 'Error', 'Order table doesnt contain items.')

        pass

    def set_order_table_act_box_conn(self, data): # IDEA: src
        self.v.drop_all_qty_button.clicked.connect(lambda: self.on_drop_all_qty_button_clicked(data))
        self.v.drop_qty_button.clicked.connect(lambda: self.on_drop_qty_button_clicked(data))
        self.v.add_qty_button.clicked.connect(lambda: self.on_add_qty_button_clicked(data))
        self.v.edit_qty_button.clicked.connect(lambda: self.on_edit_qty_button_clicked(data))
        pass
    def on_drop_all_qty_button_clicked(self, data):
        confirm = QMessageBox.question(self.v, 'Confirm', 'Drop all quantity?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            self.set_drop_all_product_qty_entry(product_name=data[0])

        self.v.barcode_scanner_field.setFocus()
        pass
    def on_drop_qty_button_clicked(self, data):
        self.set_drop_product_qty_entry(product_name=data[0], product_price_id=data[3], product_id=data[4])
        self.v.barcode_scanner_field.setFocus()
        pass
    def on_add_qty_button_clicked(self, data):
        self.set_add_product_qty_entry(product_name=data[0], product_price_id=data[3], product_id=data[4])
        self.v.barcode_scanner_field.setFocus()
        pass
    def on_edit_qty_button_clicked(self, data):
        proposed_qty, confirm = QInputDialog.getInt(self.v, f"{data[0]}", 'Set quantity:', 1, 1, 9999999)

        if confirm is True:
            self.set_edit_product_qty_entry(product_qty=proposed_qty, product_name=data[0], product_price_id=data[3], product_id=data[4])
        
        self.v.barcode_scanner_field.setFocus()
        pass
    
    def on_discard_order_button_clicked(self):
        i = self.v.manage_order_tab.currentIndex()
        order_tab_name = self.v.manage_order_tab.tabText(i)
        
        confirm = QMessageBox.warning(self.v, 'Confirm', "Discard this order?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm is QMessageBox.StandardButton.Yes:
            self.discard_order_handler(order_tab_name=order_tab_name)

        self.v.barcode_scanner_field.setFocus()
        # self.test_prints()
        
        pass
    def on_lock_order_toggle_button_clicked(self, lock):
        i = self.v.manage_order_tab.currentIndex()

        if lock is True:
            self.m.lock_order_toggle_buttons[i][0].hide()
            self.m.lock_order_toggle_buttons[i][1].show()
            pass
        elif lock is False:
            self.m.lock_order_toggle_buttons[i][0].show()
            self.m.lock_order_toggle_buttons[i][1].hide()
            pass

        self.m.order_type_displays[i].setDisabled(lock)
        self.m.customer_name_fields[i].setDisabled(lock)
        self.m.clear_order_table_buttons[i].setDisabled(lock)
        self.m.order_tables[i].setDisabled(lock)
        self.m.order_subtotal_displays[i].setDisabled(lock)
        self.m.order_discount_displays[i].setDisabled(lock)
        self.m.order_tax_displays[i].setDisabled(lock)
        self.m.order_total_displays[i].setDisabled(lock)
        self.m.discard_order_buttons[i].setDisabled(lock)
        self.m.complete_order_buttons[i].setDisabled(lock)

        self.v.barcode_scanner_field.setFocus()
        pass
    
    def on_complete_order_button_clicked(self): # IDEA: src
        i = self.v.manage_order_tab.currentIndex()
        
        if self.m.order_tables[i].rowCount() > 0:
            self.v.set_pay_order_dialog()
            self.v.tender_amount_field.setFocus()

            order_tab_name = self.v.manage_order_tab.tabText(i)

            final_order_subtotal_value = 0
            final_order_discount_value = 0
            final_order_tax_value = 0
            final_order_total_value = 0

            for tab_i in range(self.v.manage_order_tab.count()):
                if self.v.manage_order_tab.tabText(tab_i) == order_tab_name:

                    print('self.v.manage_order_tab.count():', self.v.manage_order_tab.count())
                    print('tab_i:', tab_i)
                    print('order_tab_name:', order_tab_name)

                    self.v.final_order_type_display = self.m.order_type_displays[tab_i].text()
                    self.v.final_customer_name_field = self.m.customer_name_fields[tab_i].currentText()

                    for row_v in range(self.m.order_tables[tab_i].rowCount()):
                        row_i = self.v.final_order_table.rowCount()
                        self.v.final_order_table.insertRow(row_i)

                        product_qty = self.m.order_tables[tab_i].item(row_v, 1).text()
                        product_name = self.m.order_tables[tab_i].item(row_v, 2).text()
                        product_amount = self.m.order_tables[tab_i].item(row_v, 3).text()
                        product_disc_value = self.m.order_tables[tab_i].item(row_v, 4).text()
                        
                        final_product_qty = MyTableWidgetItem(text=f"{product_qty}")
                        final_product_name = MyTableWidgetItem(text=f"{product_name}")
                        final_product_amount = MyTableWidgetItem(text=f"{float(product_amount):.2f}", format='bill')
                        final_product_disc_value = MyTableWidgetItem(text=f"{float(product_disc_value):.2f}", format='bill')

                        self.v.final_order_table.setItem(row_i, 0, final_product_qty)
                        self.v.final_order_table.setItem(row_i, 1, final_product_name)
                        self.v.final_order_table.setItem(row_i, 2, final_product_amount)
                        self.v.final_order_table.setItem(row_i, 3, final_product_disc_value)

                    final_order_subtotal_value += float(self.m.order_subtotal_displays[tab_i].text())
                    final_order_discount_value += float(self.m.order_discount_displays[tab_i].text())
                    final_order_tax_value += float(self.m.order_tax_displays[tab_i].text())
                    final_order_total_value += float(self.m.order_total_displays[tab_i].text())

            self.v.final_order_subtotal_display.setText(f"{final_order_subtotal_value:.2f}")
            self.v.final_order_discount_display.setText(f"{final_order_discount_value:.2f}")
            self.v.final_order_tax_display.setText(f"{final_order_tax_value:.2f}")
            self.v.final_order_total_display.setText(f"{final_order_total_value:.2f}")


            customer_data = pos_schema.select_customer_data_with_customer_reward_data(customer_name=self.m.customer_name_fields[i].currentText())

            if str(customer_data[0]) != 'N/A':
                self.v.final_customer_info_box.show()
                self.v.pay_points_button.show()

                self.m.final_customer_name = str(customer_data[0])
                self.v.final_customer_name_display.setText(f"Customer: <b>{customer_data[0]}</b>")
                self.v.final_customer_phone_display.setText(f"Phone: <b>{customer_data[1]}</b>")
                self.v.final_customer_points_display.setText(f"Points: <b>{customer_data[2]:.2f}</b>") 

                self.v.pay_points_button.setDisabled(False) if float(customer_data[2]) >= float(self.v.final_order_total_display.text()) else self.v.pay_points_button.setDisabled(True)

                self.compute_change_by_payment_amount_type_handler(customer_data, signal='on_complete_order_button_clicked')
                self.compute_change_by_payment_amount_type_handler(customer_data, signal='on_tender_amount_field_text_changed')

            else:
                if str(customer_data[0]) == "N/A": self.m.final_customer_name = "Guest" 
                self.v.points_payment_compute_label.hide()
                self.v.cash_points_payment_compute_label.hide()
                self.v.points_payment_compute_display.hide()
                self.v.cash_points_payment_compute_display.hide()

                self.v.final_customer_info_box.hide()
                self.v.pay_points_button.hide()
                self.v.pay_cash_points_button.hide()


                self.compute_change_by_payment_amount_type_handler(signal='on_tender_amount_field_text_changed')

            print('self.m.final_customer_name:', self.m.final_customer_name)

            self.set_pay_order_dialog_conn()

            self.v.pay_order_dialog.exec()
            pass
        else:
            QMessageBox.critical(self.v, 'Error', 'Please add an item first.')
        self.v.barcode_scanner_field.setFocus()

    # region > manage order table ---------------------------------------------------------------------------------------
    def set_clear_order_table_entry(self):
        i = self.v.manage_order_tab.currentIndex()

        self.m.order_tables[i].setRowCount(0)

        new_subtotal = 0
        new_discount = 0
        # new_tax = 0
        new_total = 0

        self.m.order_subtotal_displays[i].setText(f"{new_subtotal:.2f}")
        self.m.order_discount_displays[i].setText(f"{new_discount:.2f}")
        # self.m.order_tax_displays[i].setText(f"{new_tax:.2f}") # REVIEW: for next update
        self.m.order_total_displays[i].setText(f"{new_total:.2f}")

        self.v.barcode_scanner_field.setFocus()
        pass
    def set_initial_add_product_entry(self, product_qty=1, product_name='', product_price_id=0, product_id=0):
        i = self.v.manage_order_tab.currentIndex()
        
        sel_data = pos_schema.select_product_data_for_order_table(product_price_id, product_id)
        sel_product_name = str(sel_data[0])
        sel_product_price = float(sel_data[1])
        sel_product_disc_value = float(sel_data[2])

        self.product_data = [sel_product_name, sel_product_price, sel_product_disc_value, product_price_id, product_id]

        matched_product = self.m.order_tables[i].findItems(product_name, Qt.MatchFlag.MatchExactly) # becomes list

        if matched_product: # if product name matched
            # update
            for _ in matched_product:
                row_i = _.row()

                current_product_qty = int(self.m.order_tables[i].item(row_i, 1).text()) + product_qty
                current_product_amount = float(self.m.order_tables[i].item(row_i, 3).text()) + ((sel_product_price + sel_product_disc_value) * product_qty)
                current_product_disc_value = float(self.m.order_tables[i].item(row_i, 4).text()) + (sel_product_disc_value * product_qty)

                self.m.order_tables[i].item(row_i, 1).setText(f"{current_product_qty}")
                self.m.order_tables[i].item(row_i, 3).setText(f"{current_product_amount:.2f}")
                self.m.order_tables[i].item(row_i, 4).setText(f"{current_product_disc_value:.2f}")

        else: # if product name dont matched
            # populate
            row_i = self.m.order_tables[i].rowCount() 
            self.m.order_tables[i].insertRow(row_i)

            current_product_amount = (sel_product_price + sel_product_disc_value) * product_qty
            current_product_disc_value = sel_product_disc_value * product_qty

            self.v.set_order_table_act_box()
            new_product_qty = MyTableWidgetItem(text=f"{product_qty}")
            new_product_name = MyTableWidgetItem(text=f"{sel_product_name}")
            new_product_amount = MyTableWidgetItem(text=f"{current_product_amount:.2f}", format='bill')
            new_product_disc_value = MyTableWidgetItem(text=f"{current_product_disc_value:.2f}", format='bill')

            self.m.order_tables[i].setCellWidget(row_i, 0, self.v.order_table_act_box)
            self.m.order_tables[i].setItem(row_i, 1, new_product_qty)
            self.m.order_tables[i].setItem(row_i, 2, new_product_name)
            self.m.order_tables[i].setItem(row_i, 3, new_product_amount)
            self.m.order_tables[i].setItem(row_i, 4, new_product_disc_value)
            
            self.set_order_table_act_box_conn(self.product_data)

        new_subtotal = float(self.m.order_subtotal_displays[i].text()) + ((sel_product_price + sel_product_disc_value) * product_qty)
        new_discount = float(self.m.order_discount_displays[i].text()) + (sel_product_disc_value * product_qty)
        # new_tax = float(self.m.order_tax_displays[i].text()) + (0) # REVIEW: for next update
        new_total = new_subtotal - new_discount # - new_tax

        self.m.order_subtotal_displays[i].setText(f"{new_subtotal:.2f}")
        self.m.order_discount_displays[i].setText(f"{new_discount:.2f}")
        # self.m.order_tax_displays[i].setText(f"{new_tax:.2f}") # REVIEW: for next update
        self.m.order_total_displays[i].setText(f"{new_total:.2f}")

        self.product_data = []

        pass
    def set_add_product_qty_entry(self, product_qty=1, product_name='', product_price_id=0, product_id=0):
        i = self.v.manage_order_tab.currentIndex()

        sel_data = pos_schema.select_product_data_for_order_table(product_price_id, product_id)
        sel_product_price = float(sel_data[1])
        sel_product_disc_value = float(sel_data[2])

        matched_product = self.m.order_tables[i].findItems(product_name, Qt.MatchFlag.MatchExactly) # becomes list

        if matched_product: # if product name matched
            # update
            for _ in matched_product:
                row_i = _.row()

                current_product_qty = int(self.m.order_tables[i].item(row_i, 1).text()) + product_qty
                current_product_amount = float(self.m.order_tables[i].item(row_i, 3).text()) + ((sel_product_price + sel_product_disc_value) * product_qty)
                current_product_disc_value = float(self.m.order_tables[i].item(row_i, 4).text()) + (sel_product_disc_value * product_qty)

                self.m.order_tables[i].item(row_i, 1).setText(f"{current_product_qty}")
                self.m.order_tables[i].item(row_i, 3).setText(f"{current_product_amount:.2f}")
                self.m.order_tables[i].item(row_i, 4).setText(f"{current_product_disc_value:.2f}")

        new_subtotal = float(self.m.order_subtotal_displays[i].text()) + ((sel_product_price + sel_product_disc_value) * product_qty)
        new_discount = float(self.m.order_discount_displays[i].text()) + (sel_product_disc_value * product_qty)
        # new_tax = float(self.m.order_tax_displays[i].text()) + (0) # REVIEW: for next update
        new_total = new_subtotal - new_discount # - new_tax

        self.m.order_subtotal_displays[i].setText(f"{new_subtotal:.2f}")
        self.m.order_discount_displays[i].setText(f"{new_discount:.2f}")
        # self.m.order_tax_displays[i].setText(f"{new_tax:.2f}") # REVIEW: for next update
        self.m.order_total_displays[i].setText(f"{new_total:.2f}")


        pass
    def set_drop_all_product_qty_entry(self, product_name=''):
        i = self.v.manage_order_tab.currentIndex()

        matched_product = self.m.order_tables[i].findItems(product_name, Qt.MatchFlag.MatchExactly) # becomes list

        if matched_product: # if product name matched
            # update
            for _ in matched_product:
                row_i = _.row()

                current_product_qty = int(self.m.order_tables[i].item(row_i, 1).text())
                current_product_amount = float(self.m.order_tables[i].item(row_i, 3).text())
                current_product_disc_value = float(self.m.order_tables[i].item(row_i, 4).text())


                self.m.order_tables[i].removeRow(row_i)
                    

        new_subtotal = max(0, float(self.m.order_subtotal_displays[i].text()) - current_product_amount)
        new_discount = max(0, float(self.m.order_discount_displays[i].text()) - current_product_disc_value)
        # new_tax = max(0, float(self.m.order_tax_displays[i].text()) - (0)) # REVIEW: for next update
        new_total = max(0, new_subtotal + new_discount) # - new_tax

        self.m.order_subtotal_displays[i].setText(f"{new_subtotal:.2f}")
        self.m.order_discount_displays[i].setText(f"{new_discount:.2f}")
        # self.m.order_tax_displays[i].setText(f"{new_tax:.2f}") # REVIEW: for next update
        self.m.order_total_displays[i].setText(f"{new_total:.2f}")



        pass
    def set_drop_product_qty_entry(self, product_qty=1, product_name='', product_price_id=0, product_id=0):
        i = self.v.manage_order_tab.currentIndex()

        sel_data = pos_schema.select_product_data_for_order_table(product_price_id, product_id)
        sel_product_price = float(sel_data[1])
        sel_product_disc_value = float(sel_data[2])

        matched_product = self.m.order_tables[i].findItems(product_name, Qt.MatchFlag.MatchExactly) # becomes list

        if matched_product: # if product name matched
            # update
            for _ in matched_product:
                row_i = _.row()

                current_product_qty = int(self.m.order_tables[i].item(row_i, 1).text()) - product_qty
                current_product_amount = float(self.m.order_tables[i].item(row_i, 3).text()) - ((sel_product_price + sel_product_disc_value) * product_qty)
                current_product_disc_value = float(self.m.order_tables[i].item(row_i, 4).text()) - (sel_product_disc_value * product_qty)

                self.m.order_tables[i].item(row_i, 1).setText(f"{current_product_qty}")
                self.m.order_tables[i].item(row_i, 3).setText(f"{current_product_amount:.2f}")
                self.m.order_tables[i].item(row_i, 4).setText(f"{current_product_disc_value:.2f}")

                self.m.order_tables[i].removeRow(row_i) if current_product_qty <= 0 else None
                    

        new_subtotal = max(0, float(self.m.order_subtotal_displays[i].text()) - ((sel_product_price + sel_product_disc_value) * product_qty))
        new_discount = max(0, float(self.m.order_discount_displays[i].text()) - (sel_product_disc_value * product_qty))
        # new_tax = max(0, float(self.m.order_tax_displays[i].text()) - (0)) # REVIEW: for next update
        new_total = max(0, new_subtotal - new_discount) # - new_tax

        self.m.order_subtotal_displays[i].setText(f"{new_subtotal:.2f}")
        self.m.order_discount_displays[i].setText(f"{new_discount:.2f}")
        # self.m.order_tax_displays[i].setText(f"{new_tax:.2f}") # REVIEW: for next update
        self.m.order_total_displays[i].setText(f"{new_total:.2f}")
        pass
    def set_edit_product_qty_entry(self, product_qty=1, product_name='', product_price_id=0, product_id=0):
        i = self.v.manage_order_tab.currentIndex()

        sel_data = pos_schema.select_product_data_for_order_table(product_price_id, product_id)
        sel_product_price = float(sel_data[1])
        sel_product_disc_value = float(sel_data[2])

        sel_subtotal = float(self.m.order_subtotal_displays[i].text())
        sel_discount = float(self.m.order_discount_displays[i].text())
        sel_tax = float(self.m.order_tax_displays[i].text())
        sel_total = float(self.m.order_total_displays[i].text())

        matched_product = self.m.order_tables[i].findItems(product_name, Qt.MatchFlag.MatchExactly) # becomes list

        if matched_product: # if product name matched
            # update
            for _ in matched_product:
                row_i = _.row()

                current_product_qty = product_qty
                current_product_amount = (sel_product_price + sel_product_disc_value) * product_qty
                current_product_disc_value = sel_product_disc_value * product_qty

                sel_subtotal -= float(self.m.order_tables[i].item(row_i, 3).text())
                sel_discount -= float(self.m.order_tables[i].item(row_i, 4).text())
                sel_tax = 0
                sel_total = sel_subtotal - sel_discount

                self.m.order_tables[i].item(row_i, 1).setText(f"{current_product_qty}")
                self.m.order_tables[i].item(row_i, 3).setText(f"{current_product_amount:.2f}")
                self.m.order_tables[i].item(row_i, 4).setText(f"{current_product_disc_value:.2f}")

        new_subtotal = sel_subtotal + ((sel_product_price + sel_product_disc_value) * product_qty)
        new_discount = sel_discount + (sel_product_disc_value * product_qty)
        # new_tax = sel_tax + float(self.m.order_tax_displays[i].text()) + (0) # REVIEW: for next update
        new_total = new_subtotal - new_discount # - new_tax

        self.m.order_subtotal_displays[i].setText(f"{new_subtotal:.2f}")
        self.m.order_discount_displays[i].setText(f"{new_discount:.2f}")
        # self.m.order_tax_displays[i].setText(f"{new_tax:.2f}") # REVIEW: for next update
        self.m.order_total_displays[i].setText(f"{new_total:.2f}")

        pass
    # endregion ---------------------------------------------------------------------------------------------------------

    # region > pay order dialog -----------------------------------------------------------------------------------------
    def set_pay_order_dialog_conn(self):
        self.v.tender_amount_field.textChanged.connect(self.on_tender_amount_field_text_changed)
        self.v.tender_amount_field.returnPressed.connect(lambda: self.on_pay_button_clicked(payment_type='pay_cash'))
        self.v.numpad_key_toggle_button[0].clicked.connect(lambda: self.on_numpad_key_toggle_button_clicked(hide=True))
        self.v.numpad_key_toggle_button[1].clicked.connect(lambda: self.on_numpad_key_toggle_button_clicked(hide=False))
        self.v.numpad_key_button[0].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='1'))
        self.v.numpad_key_button[1].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='2'))
        self.v.numpad_key_button[2].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='3'))
        self.v.numpad_key_button[3].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='4'))
        self.v.numpad_key_button[4].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='5'))
        self.v.numpad_key_button[5].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='6'))
        self.v.numpad_key_button[6].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='7'))
        self.v.numpad_key_button[7].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='8'))
        self.v.numpad_key_button[8].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='9'))
        self.v.numpad_key_button[9].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='delete'))
        self.v.numpad_key_button[10].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='0'))
        self.v.numpad_key_button[11].clicked.connect(lambda: self.on_numpad_key_button_clicked(key_value='.'))

        self.v.pay_cash_button.clicked.connect(lambda: self.on_pay_button_clicked(payment_type='pay_cash'))
        self.v.pay_points_button.clicked.connect(lambda: self.on_pay_button_clicked(payment_type='pay_points'))
        self.v.pay_cash_points_button.clicked.connect(lambda: self.on_pay_button_clicked(payment_type='pay_cash_points'))
        pass
    def on_tender_amount_field_text_changed(self):
        try:
            i = self.v.manage_order_tab.currentIndex()
            customer_data = pos_schema.select_customer_data_with_customer_reward_data(customer_name=self.m.customer_name_fields[i].currentText())

            self.compute_change_by_payment_amount_type_handler(customer_data, signal='on_tender_amount_field_text_changed')
            pass
        except Exception as e:
            self.compute_change_by_payment_amount_type_handler(signal='on_tender_amount_field_text_changed')
            pass
        pass

    def on_numpad_key_toggle_button_clicked(self, hide):
        if hide is True:
            self.v.numpad_key_toggle_button[0].hide()
            self.v.numpad_key_toggle_button[1].show()
        else:
            self.v.numpad_key_toggle_button[0].show()
            self.v.numpad_key_toggle_button[1].hide()

        self.v.numpad_key_box.setHidden(hide)
        pass
    def on_numpad_key_button_clicked(self, key_value):
        reward_data = pos_schema.select_reward_for_reward_selection()
        print('reward_data:', reward_data)

        current_amount_tendered = self.v.tender_amount_field.text()

        if key_value == '.' and '.' in current_amount_tendered:
            return  # Do nothing if there's already a decimal point

        if key_value not in ['delete']:
            if (len(current_amount_tendered) <= 1 and current_amount_tendered == '0') or self.v.tender_amount_field.selectedText(): 
                temp_amount = key_value
                # self.v.tender_amount_field.setText(current_amount_tendered)
            else:
                temp_amount = current_amount_tendered + key_value
            parts = temp_amount.split('.')
            if len(parts[0]) > 10:  # More than 10 digits before decimal point
                return
            if len(parts) > 1 and len(parts[1]) > 2:  # More than 2 digits after decimal point
                return
            current_amount_tendered = temp_amount

        if key_value == 'delete':
            current_amount_tendered = current_amount_tendered[:-1]
            pass
        self.v.tender_amount_field.setText(current_amount_tendered)

    def on_pay_button_clicked(self, payment_type):
        try:
            i = self.v.manage_order_tab.currentIndex()

            cash_payment_amount = 0
            points_payment_amount = 0
            cash_points_payment_amount = [0,0]


            if (payment_type == 'pay_cash' and float(self.v.tender_amount_field.text()) >= float(self.m.order_total_displays[i].text())) or payment_type == 'pay_points' or payment_type == 'pay_cash_points':
                order_tab_name = self.v.manage_order_tab.tabText(i)
                sales_group_id = 0
                payment_amount = 0

                for tab_i in range(self.v.manage_order_tab.count()):
                    if self.v.manage_order_tab.tabText(tab_i) == order_tab_name:
                        sales_group_id += pos_schema.select_sales_group_id_by_name(sales_group_name=self.m.order_type_displays[tab_i].text())
                        
                customer_id = pos_schema.select_customer_id_by_name(customer_name=self.m.customer_name_fields[i].currentText())
                
                order_subtotal = float(self.v.final_order_subtotal_display.text())
                order_discount = float(self.v.final_order_discount_display.text())
                order_tax = float(self.v.final_order_tax_display.text())
                order_total = float(self.v.final_order_total_display.text())

                confirm = QMessageBox.warning(self.v.pay_order_dialog, 'Confirm', 'Proceed payment?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if confirm is QMessageBox.StandardButton.Yes:
                    if payment_type == 'pay_cash':
                        payment_amount = float(self.v.tender_amount_field.text())
                        order_change = payment_amount - order_total
                        cash_payment_amount = payment_amount
                        pass
                    elif payment_type == 'pay_points':
                        payment_amount = float(self.m.final_customer_points_value)
                        order_change = payment_amount - order_total
                        points_payment_amount = order_total
                        pos_schema.update_customer_reward_points_by_decrement(customer_id, order_total)
                        pass
                    elif payment_type == 'pay_cash_points':
                        final_customer_points = float(self.m.final_customer_points_value)

                        cash_amount = float(self.v.tender_amount_field.text())
                        points_amount = order_total - cash_amount

                        payment_amount = float(self.v.tender_amount_field.text()) + final_customer_points
                        order_change = payment_amount - order_total
                        cash_points_payment_amount = [cash_amount, points_amount]
                        pos_schema.update_customer_reward_points_by_decrement(customer_id, points_amount)


                    final_order_table = self.v.final_order_table
                    # TODO: APPEND FOR RECEIPT

                    self.m.append_final_order_info_for_receipt(
                        sales_group_id=sales_group_id, 
                        customer_id=customer_id, 

                        order_subtotal=order_subtotal, 
                        order_discount=order_discount, 
                        order_tax=order_tax, 
                        order_total=order_total, 
                        payment_amount=payment_amount, 
                        order_change=order_change, 
                        final_order_table=final_order_table,

                        payment_type=payment_type,
                        cash_payment_amount=cash_payment_amount,
                        points_payment_amount=points_payment_amount,
                        cash_points_payment_amount=cash_points_payment_amount,
                    )
                    # TODO: PERFORM TRANSACTION INSERTION


                    self.v.pay_order_dialog.close()

                    self.v.setup_transaction_complete_dialog()


                    if payment_type == 'pay_cash':
                        self.v.transaction_order_change_display.show()
                        self.v.transaction_order_change_label.show()
                        self.v.transaction_payment_amount_display.setText(f"{self.m.cash_payment_amount:.2f}")
                    elif payment_type == 'pay_points':
                        self.v.transaction_order_change_display.hide()
                        self.v.transaction_order_change_label.hide()
                        self.v.transaction_payment_amount_display.setText(f"{self.m.points_payment_amount:.2f}")
                    elif payment_type == 'pay_cash_points':
                        self.v.transaction_order_change_display.hide()
                        self.v.transaction_order_change_label.hide()
                        self.v.transaction_payment_amount_display.setText(f"{self.m.cash_points_payment_amount[0]:.2f} (Cash) + {self.m.cash_points_payment_amount[1]:.2f} (Points)")
                    
                    self.v.transaction_order_total_amount_display.setText(f"{order_total:.2f}")
                    self.v.transaction_order_change_display.setText(f"{order_change:.2f}")

                    self.set_transaction_complete_dialog_conn(sales_group_id=sales_group_id, order_tab_name=order_tab_name)


                    # # save receipt # FIXME
                    # self.v.set_progress_dialog(action='save_receipt')

                    # self.receipt_printer = ReceiptGenerator(
                    #     self.v.transaction_complete_dialog,
                    #     sales_group_id,
                    #     self.m.transaction_info,
                    #     self.m.final_order_table,
                    #     self.m.final_order_summary,
                    #     self.m.cashier_info,

                    #     self.m.payment_type,
                    #     self.m.cash_payment_amount,
                    #     self.m.points_payment_amount,
                    #     self.m.cash_points_payment_amount,

                    #     'save_receipt',
                    # )
                    # self.receipt_printer.start()
                    # self.receipt_printer.update.connect(lambda step, action='save_receipt': self.on_receipt_generator_update(step, action))
                    # self.receipt_printer.finished.connect(lambda action='save_receipt': self.on_receipt_generator_finished(action))

                    # self.v.progress_dialog.exec()
                    # # save receipt

                    self.v.transaction_complete_dialog.exec()

                    self.discard_order_handler(order_tab_name=order_tab_name)

                    self.m.final_customer_points_value = 0

                else:
                    pass
            else:
                QMessageBox.critical(self.v.pay_order_dialog, 'Error', 'Insufficient fund.')
            
        except ValueError as e:
            QMessageBox.critical(self.v.pay_order_dialog, 'Error', f"Invalid input. {e}")

        # pass
    # endregion

    def set_transaction_complete_dialog_conn(self, sales_group_id=0, order_tab_name=''): # IDEA: src
        self.v.print_receipt_button.clicked.connect(lambda: self.on_receipt_button_clicked(action='print_receipt', sales_group_id=sales_group_id))
        self.v.save_receipt_button.clicked.connect(lambda: self.on_receipt_button_clicked(action='save_receipt', sales_group_id=sales_group_id))
        self.v.add_new_order_button.clicked.connect(lambda: self.on_add_new_order_button_clicked(order_tab_name=order_tab_name))
        self.v.transaction_complete_close_button.clicked.connect(lambda: self.close_dialog_handler(self.v.transaction_complete_dialog))
        pass
    def on_add_new_order_button_clicked(self, order_tab_name):
        self.v.transaction_complete_dialog.close()
        self.discard_order_handler(order_tab_name=order_tab_name)
        self.on_add_order_button_clicked()
        pass

    def on_receipt_button_clicked(self, action, sales_group_id): # IDEA: src
        if action == 'print_receipt':
            self.v.print_receipt_button.setDisabled(True)
            
            self.v.set_progress_dialog(action='print_receipt')

            print('self.m.final_customer_name:', self.m.final_customer_name)

            self.receipt_printer = ReceiptGenerator(
                self.v.transaction_complete_dialog,
                sales_group_id,
                self.m.final_customer_name,
                self.m.transaction_info,
                self.m.final_order_table,
                self.m.final_order_summary,
                self.m.cashier_info,

                self.m.payment_type,
                self.m.cash_payment_amount,
                self.m.points_payment_amount,
                self.m.cash_points_payment_amount,

                action,
            )
            self.receipt_printer.start()
            self.receipt_printer.update.connect(lambda step, action=action: self.on_receipt_generator_update(step, action))
            self.receipt_printer.finished.connect(lambda action=action: self.on_receipt_generator_finished(action))

            self.v.progress_dialog.exec()

            pass

        # elif action == 'save':
        #     self.v.save_receipt_button.setDisabled(True)

        #     self.v.set_progress_dialog()

        #     self.receipt_printer = ReceiptGenerator(
        #         self.v.transaction_complete_dialog,
        #         sales_group_id,
        #         self.m.transaction_info,
        #         self.m.final_order_table,
        #         self.m.final_wholesale_order_table,
        #         self.m.final_order_summary,
        #         self.m.cashier_info,
        #         action,
        #     )
        #     self.receipt_printer.start()
        #     self.receipt_printer.update.connect(lambda step, action=action: self.on_receipt_generator_update(step, action))
        #     self.receipt_printer.finished.connect(lambda action=action: self.on_receipt_generator_finished(action))

        #     self.v.progress_dialog.exec()

        #     pass
    def on_receipt_generator_update(self, step, action):
        if action == 'print_receipt':
            self.v.progress_label.setText(f"Please wait...")
            self.v.progress_dialog.setWindowTitle(f"Step {step} out of 6")
        if action == 'save_receipt':
            self.v.progress_dialog.setWindowTitle(f"Saving")
    def on_receipt_generator_finished(self, action):
        self.v.print_receipt_button.setEnabled(True) if self.v.print_receipt_button.isEnabled() is not True else None
        self.v.save_receipt_button.setEnabled(True) if self.v.save_receipt_button.isEnabled() is not True else None

        self.v.progress_dialog.close_signal.emit('finished')
        self.v.progress_dialog.close()

        if action == 'print_receipt':
            QMessageBox.information(self.v.transaction_complete_dialog, 'Success', 'Receipt printed.')


    # IDEA: if the widget uses the same connection
    def load_combo_box_data_handler(self, load=''):
        self.v.set_order_box()

        if load == 'global':
            self.v.order_type_field.addItem('Retail')
            self.v.order_type_field.addItem('Wholesale')
            self.v.order_type_field.addItem('Dual')
        
        if load == 'order_box':
            self.v.customer_name_field.clear()

            customer_name_data = pos_schema.select_customer_name_for_combo_box()
            self.v.customer_name_field.addItem('')
            for customer_name in customer_name_data: self.v.customer_name_field.addItems(customer_name)
            self.v.customer_name_field.clearEditText()

            try:
                i = self.v.manage_order_tab.currentIndex()

                self.m.customer_name_fields[i].clear()

                customer_name_data = pos_schema.select_customer_name_for_combo_box()
                self.m.customer_name_fields[i].addItem('')
                for customer_name in customer_name_data: self.m.customer_name_fields[i].addItems(customer_name)
                self.m.customer_name_fields[i].clearEditText()
            except:
                pass

        pass
    def sync_ui_handler(self):
        text_filter = self.v.filter_field.text()
        try:
            i = self.v.manage_order_tab.currentIndex()

            order_type = self.m.order_type_displays[i].text()

            self.m.total_page_number = pos_schema.select_product_data_total_page_count(text=text_filter, order_type=order_type)
            self.m.page_number = 1 if self.m.total_page_number > 0 else 0

            self.v.order_index_label.setText(f"{self.v.manage_order_tab.tabText(i)}")

            self.populate_overview_table(text=text_filter, order_type=order_type, page_number=self.m.page_number)
            self.load_combo_box_data_handler(load='order_box')
        except Exception as e:
            self.m.total_page_number = pos_schema.select_product_data_total_page_count()
            self.m.page_number = 1 if self.m.total_page_number > 0 else 0

            self.populate_overview_table(page_number=self.m.page_number)
            pass
        self.v.product_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.v.barcode_scanner_field.setFocus()
        self.v.filter_field.setEnabled(self.v.manage_order_tab.count() > 0)
        self.v.filter_field.clear()
        self.v.barcode_scanner_field.setEnabled(self.v.manage_order_tab.count() > 0)
        pass
    def panel_add_order_handler(self):
        self.v.manage_order_tab.setHidden(self.v.manage_order_tab.count() <= 0)
        self.v.order_empty_tab_box.setHidden(self.v.manage_order_tab.count() > 0)
        print('count::', self.v.manage_order_tab.count())
        pass
    def discard_order_handler(self, order_tab_name=''):
        for _ in range(self.v.manage_order_tab.count()):
            i = self.v.manage_order_tab.currentIndex()

            if self.v.manage_order_tab.tabText(i) == order_tab_name:
                self.v.manage_order_tab.removeTab(i)
                self.m.remove_order_tab_content_from_container(i)

            self.v.order_index_label.setText(f"{self.v.manage_order_tab.tabText(i)}") if self.v.manage_order_tab.count() > 0 else self.v.order_index_label.setText(f"No order")
        self.v.add_order_button.setEnabled(self.v.manage_order_tab.count() < 10)
        self.sync_ui_handler()
        self.panel_add_order_handler()
        pass
    def compute_change_by_payment_amount_type_handler(self, customer_data=['','',-1], signal=''):
        cash_payment_change = 0
        cash_points_payment_change = 0
        current_amount_tendered = 0
        current_amount_tendered_with_points = 0
    
        if signal == 'on_tender_amount_field_text_changed':
            try:
                final_order_total = float(self.v.final_order_total_display.text())
                final_customer_points_value = float(customer_data[2]) # customer points stored in a new variable since final customer points display contains other strings or characters which complicates passing values
                current_amount_tendered = float(self.v.tender_amount_field.text())
                current_amount_tendered_with_points = current_amount_tendered + final_customer_points_value

                cash_payment_change = current_amount_tendered - final_order_total
                cash_points_payment_change = current_amount_tendered_with_points - final_order_total

                self.v.cash_payment_compute_display.setText(f"<b><font color='red'>{cash_payment_change:.2f}</font></b>") if cash_payment_change < 0 else self.v.cash_payment_compute_display.setText(f"<b><font color='green'>{cash_payment_change:.2f}</font></b>")
                self.v.cash_points_payment_compute_display.setText(f"<b><font color='red'>{cash_points_payment_change:.2f}</font></b>") if cash_points_payment_change < 0 else self.v.cash_points_payment_compute_display.setText(f"<b><font color='green'>{cash_points_payment_change:.2f}</font></b>")
                
                self.v.pay_cash_button.setDisabled(True) if cash_payment_change < 0 else self.v.pay_cash_button.setDisabled(False) 
                self.v.pay_cash_points_button.setDisabled(True) if cash_points_payment_change < 0 else self.v.pay_cash_points_button.setDisabled(False) 

                self.v.pay_cash_points_button.setDisabled(True) if current_amount_tendered >= final_order_total or current_amount_tendered_with_points < final_order_total else self.v.pay_cash_points_button.setDisabled(False) 
                self.v.pay_points_button.setDisabled(True) if current_amount_tendered >= final_order_total or final_customer_points_value < final_order_total else self.v.pay_points_button.setDisabled(False) 


            except ValueError as ve:
                self.v.pay_cash_button.setDisabled(False) if current_amount_tendered >= final_order_total else self.v.pay_cash_button.setDisabled(True)
                self.v.pay_cash_points_button.setDisabled(False) if current_amount_tendered_with_points >= final_order_total else self.v.pay_cash_points_button.setDisabled(True)

                self.v.cash_payment_compute_display.setText(f"<b><font color='red'>Error</font></b>")
                self.v.cash_points_payment_compute_display.setText(f"<b><font color='red'>Error</font></b>")
                pass
        elif signal == 'on_complete_order_button_clicked':
            final_order_total = float(self.v.final_order_total_display.text())
            final_customer_points_value = float(customer_data[2]) # customer points stored in a new variable since final customer points display contains other strings or characters which complicates passing values
            self.points_payment_change = final_customer_points_value - final_order_total
            self.v.points_payment_compute_display.setText(f"<b><font color='red'>{self.points_payment_change:.2f}</font></b>") if self.points_payment_change < 0 else self.v.points_payment_compute_display.setText(f"<b><font color='green'>{self.points_payment_change:.2f}</font></b>")
            
    def add_order_handler(self, order_type_display=''):
        self.v.set_order_box()
        self.load_combo_box_data_handler(load='order_box')
        self.set_order_tab_content_conn()

        current_i = 0        

        if self.v.order_type_field.currentText() == 'Retail':
            self.v.order_type_display.setText('Retail')
            current_i = self.v.manage_order_tab.addTab(self.v.order_box, QIcon(qss.retail_icon), f"Order {self.m.order_number}") 
        elif self.v.order_type_field.currentText() == 'Wholesale':
            self.v.order_type_display.setText('Wholesale')
            current_i = self.v.manage_order_tab.addTab(self.v.order_box, QIcon(qss.wholesale_icon), f"Order {self.m.order_number}")
        elif self.v.order_type_field.currentText() == 'Dual':
            self.v.order_type_display.setText(order_type_display)
            current_i = self.v.manage_order_tab.addTab(self.v.order_box, QIcon(qss.dual_icon), f"Order {self.m.order_number}")

        self.m.append_order_tab_content_to_container(
            self.v.order_type_display,
            self.v.customer_points_display,
            self.v.customer_name_field,
            self.v.clear_order_table_button,
            self.v.order_table,
            self.v.order_subtotal_display,
            self.v.order_discount_display,
            self.v.order_tax_display,
            self.v.order_total_display,
            self.v.discard_order_button,
            self.v.lock_order_toggle_button,
            self.v.complete_order_button,
        )
        
        self.v.manage_order_tab.setCurrentIndex(current_i)

        self.v.add_order_button.setDisabled(self.v.manage_order_tab.count() >= 10)
        self.v.order_index_label.setText(f"{self.v.manage_order_tab.tabText(current_i)}")
    def close_dialog_handler(self, dialog: QDialog):
        dialog.close()

    def test_prints(self):
        try: 
            i = self.v.manage_order_tab.currentIndex()




        except Exception as e:
            pass

class MyPOSWindow(MyGroupBox):
    def __init__(self, name='test', password='test', phone='test'):

        self.model = MyPOSModel(name, password, phone)
        self.view = MyPOSView(self.model)
        self.controller = MyPOSController(self.model, self.view)

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
    pos_window = MyPOSWindow()

    pos_window.run()

    app.exec()