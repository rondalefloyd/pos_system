
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.gui.widget.my_widget import *
from src.core.sql.cashier.pos import MyPOSSchema
from src.core.sql.admin.product import MyProductSchema
from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()
pos_schema = MyPOSSchema()
product_schema = MyProductSchema()

class MyPOSModel:
    def __init__(self, name, phone):
        self.user_name = name
        self.user_phone = phone

        self.total_page_number = pos_schema.select_product_data_total_page_count()
        self.page_number = 1 if self.total_page_number > 0 else 0

        self.set_order_tab_content_container()
        
        self.order_number = 0
        self.sel_product_id = 0

    def set_order_tab_content_container(self):
        self.order_type_displays: List[MyLabel] = []
        self.customer_name_fields: List[MyLineEdit] = []
        self.clear_order_table_buttons: List[MyPushButton] = []

        self.order_tables: List[MyTableWidget] = []

        self.order_subtotal_displays: List[MyLabel] = []
        self.order_discount_displays: List[MyLabel] = []
        self.order_tax_displays: List[MyLabel] = []
        self.order_total_displays: List[MyLabel] = []

        self.discard_order_buttons: List[MyPushButton] = []
        self.lock_order_toggle_buttons: List[MyPushButton] = []
        self.pay_order_buttons: List[MyPushButton] = []
        pass
    def append_order_tab_content_to_container(
            self,
            order_type_display,
            customer_name_field,
            clear_order_table_button,
            order_table,
            order_subtotal_display,
            order_discount_display,
            order_tax_display,
            order_total_display,
            discard_order_button,
            lock_order_toggle_button,
            pay_order_button,
    ):
        self.order_type_displays.append(order_type_display)
        self.customer_name_fields.append(customer_name_field)
        self.clear_order_table_buttons.append(clear_order_table_button)

        self.order_tables.append(order_table)

        self.order_subtotal_displays.append(order_subtotal_display)
        self.order_discount_displays.append(order_discount_display)
        self.order_tax_displays.append(order_tax_display)
        self.order_total_displays.append(order_total_display)

        self.discard_order_buttons.append(discard_order_button)
        self.lock_order_toggle_buttons.append(lock_order_toggle_button)
        self.pay_order_buttons.append(pay_order_button)
        pass
    def remove_order_tab_content_from_container(self, i:int):
        self.order_type_displays.remove(self.order_type_displays[i])
        self.customer_name_fields.remove(self.customer_name_fields[i])
        self.clear_order_table_buttons.remove(self.clear_order_table_buttons[i])

        self.order_tables.remove(self.order_tables[i])

        self.order_subtotal_displays.remove(self.order_subtotal_displays[i])
        self.order_discount_displays.remove(self.order_discount_displays[i])
        self.order_tax_displays.remove(self.order_tax_displays[i])
        self.order_total_displays.remove(self.order_total_displays[i])

        self.discard_order_buttons.remove(self.discard_order_buttons[i])
        self.lock_order_toggle_buttons.remove(self.lock_order_toggle_buttons[i])
        self.pay_order_buttons.remove(self.pay_order_buttons[i])
    pass
class MyPOSView(MyWidget):
    def __init__(self, model: MyPOSModel):
        super().__init__()

        self.m = model

        self.set_pos_box()

    def set_pos_box(self):
        self.filter_field = MyLineEdit(object_name='filter_field')
        self.filter_button = MyPushButton(text='Filter')
        self.filter_box = MyGroupBox()
        self.filter_layout = MyHBoxLayout()
        self.filter_layout.addWidget(self.filter_field)
        self.filter_layout.addWidget(self.filter_button)
        self.filter_box.setLayout(self.filter_layout)

        self.barcode_scanner_field = MyLineEdit()
        self.barcode_scanner_toggle_button = [
            MyPushButton(object_name='toggle', text='Off'),
            MyPushButton(object_name='untoggle', text='On')
        ]
        self.barcode_scanner_box = MyGroupBox()
        self.barcode_scanner_layout = MyHBoxLayout()
        self.barcode_scanner_layout.addWidget(self.barcode_scanner_field)
        self.barcode_scanner_layout.addWidget(self.barcode_scanner_toggle_button[0])
        self.barcode_scanner_layout.addWidget(self.barcode_scanner_toggle_button[1])
        self.barcode_scanner_box.setLayout(self.barcode_scanner_layout)

        self.pos_act_box = MyGroupBox()
        self.pos_act_layout = MyHBoxLayout()
        self.pos_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.pos_act_layout.addWidget(self.barcode_scanner_box,1,Qt.AlignmentFlag.AlignRight)
        self.pos_act_box.setLayout(self.pos_act_layout)

        self.product_overview_table = MyTableWidget(object_name='pos_overview_table')
        self.product_overview_prev_button = MyPushButton(text='Prev')
        self.product_overview_page_label = MyLabel(text=f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.product_overview_next_button = MyPushButton(text='Next')
        self.product_overview_act_box = MyGroupBox()
        self.product_overview_act_layout = MyHBoxLayout()
        self.product_overview_act_layout.addWidget(self.product_overview_prev_button)
        self.product_overview_act_layout.addWidget(self.product_overview_page_label)
        self.product_overview_act_layout.addWidget(self.product_overview_next_button)
        self.product_overview_act_box.setLayout(self.product_overview_act_layout)
        self.product_overview_box = MyGroupBox()
        self.product_overview_layout = MyVBoxLayout()
        self.product_overview_layout.addWidget(self.product_overview_table)
        self.product_overview_layout.addWidget(self.product_overview_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.product_overview_box.setLayout(self.product_overview_layout)
        
        self.pos_sort_tab = MyTabWidget()
        self.pos_sort_tab.addTab(self.product_overview_box, 'Overview')

        self.order_index_label = MyLabel(text='No order')
        self.order_type_field = MyComboBox()
        self.add_order_button = MyPushButton(text='Add')
        self.manage_order_act_box = MyGroupBox()
        self.manage_order_act_layout = MyHBoxLayout()
        self.manage_order_act_layout.addWidget(self.order_index_label)
        self.manage_order_act_layout.addWidget(self.order_type_field)
        self.manage_order_act_layout.addWidget(self.add_order_button)
        self.manage_order_act_box.setLayout(self.manage_order_act_layout)

        self.manage_order_tab = MyTabWidget()

        self.manage_order_box = MyGroupBox('manage_order_box')
        self.manage_order_layout = MyVBoxLayout()
        self.manage_order_layout.addWidget(self.manage_order_act_box)
        self.manage_order_layout.addWidget(self.manage_order_tab)
        self.manage_order_box.setLayout(self.manage_order_layout)

        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.pos_act_box,0,0)
        self.main_layout.addWidget(self.pos_sort_tab,1,0)
        self.main_layout.addWidget(self.manage_order_box,0,1,2,1)
        self.setLayout(self.main_layout)

    def set_progress_dialog(self):
        self.progress_bar = MyProgressBar()
        self.progress_label = MyLabel(text='Please wait...')
        self.progress_dialog = MyDialog(window_title='99% complete')
        self.progress_layout = MyVBoxLayout()
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_dialog.setLayout(self.progress_layout)
        pass

    def set_overview_table_product_display_box(self, data):
        self.product_display_label = MyLabel()
        self.product_display_image = QPixmap(os.path.abspath(f"template/icon/pos/product_box.png"))
        self.product_display_label.setPixmap(self.product_display_image)

        self.add_products_button = MyPushButton(text='Add')
        self.view_data_button = MyPushButton(text='View')
        self.product_display_act_box = MyGroupBox(object_name='product_display_act_box')
        self.product_display_act_layout = MyGridLayout(object_name='product_display_act_layout')
        self.product_display_act_layout.addWidget(self.product_display_label,0,0,1,2,Qt.AlignmentFlag.AlignCenter)
        self.product_display_act_layout.addWidget(self.add_products_button,1,0)
        self.product_display_act_layout.addWidget(self.view_data_button,1,1)
        self.product_display_act_box.setLayout(self.product_display_act_layout)

        self.product_name_label = MyLabel(object_name='product_name_label', text=f"{data[0]}")
        self.product_brand_label = MyLabel(object_name='product_brand_label', text=f"{data[1]}")
        self.product_barcode_label = MyLabel(object_name='product_barcode_label', text=f"{data[2]}")

        self.product_price_label = MyLabel(object_name='product_price_label', text=f"Price: {data[4]}")
        self.product_disc_value_label = MyLabel(object_name='product_disc_value_label', text=f"Discount: {data[4]}")
        self.product_pricing_layout = MyHBoxLayout()
        self.product_pricing_layout.addWidget(self.product_price_label)
        self.product_pricing_layout.addWidget(self.product_disc_value_label,1,Qt.AlignmentFlag.AlignLeft)

        self.product_effective_dt_label = MyLabel(object_name='product_effective_dt_label', text=f"Effective date: {data[5]}")
        self.product_onhand_label = MyLabel(object_name='product_onhand_label', text=f"Stock: {data[6]}")
        self.product_info_box = MyGroupBox()
        self.product_info_layout = MyVBoxLayout()
        self.product_info_layout.addWidget(self.product_name_label)
        self.product_info_layout.addWidget(self.product_brand_label)
        self.product_info_layout.addWidget(self.product_barcode_label)
        self.product_info_layout.addLayout(self.product_pricing_layout)
        self.product_info_layout.addWidget(self.product_effective_dt_label)
        self.product_info_layout.addWidget(self.product_onhand_label)
        self.product_info_box.setLayout(self.product_info_layout)

        self.product_overview_act_box = MyGroupBox(object_name='pos_overview_act_box')
        self.product_overview_act_layout = MyHBoxLayout(object_name='pos_overview_act_layout')
        self.product_overview_act_layout.addWidget(self.product_display_act_box,0,Qt.AlignmentFlag.AlignLeft)
        self.product_overview_act_layout.addWidget(self.product_info_box)
        self.product_overview_act_box.setLayout(self.product_overview_act_layout)

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

        self.product_datetime_created_info = MyLabel(text=f"{data[13]}")

        self.info_box = MyGroupBox()
        self.info_layout = MyFormLayout()
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

        self.view_data_act_close_button = MyPushButton(text='Close')
        self.view_data_act_box = MyGroupBox()
        self.view_data_act_layout = MyHBoxLayout()
        self.view_data_act_layout.addWidget(self.view_data_act_close_button,0,Qt.AlignmentFlag.AlignRight)
        self.view_data_act_box.setLayout(self.view_data_act_layout)

        self.view_data_dialog = MyDialog()
        self.view_data_layout = MyVBoxLayout()
        self.view_data_layout.addWidget(self.view_data_scra)
        self.view_data_layout.addWidget(self.view_data_act_box)
        self.view_data_dialog.setLayout(self.view_data_layout)
        pass
    
    def set_order_box(self):
        self.order_type_display = MyLabel(text=f"{self.order_type_field.currentText()}")
        self.customer_name_field = MyComboBox()
        self.clear_order_table_button = MyPushButton(text='Clear')
        self.order_act_a_box = MyGroupBox()
        self.order_act_a_layout = MyHBoxLayout()
        self.order_act_a_layout.addWidget(self.order_type_display)
        self.order_act_a_layout.addWidget(self.customer_name_field)
        self.order_act_a_layout.addWidget(self.clear_order_table_button)
        self.order_act_a_box.setLayout(self.order_act_a_layout)

        self.order_table = MyTableWidget(object_name='order_table')

        self.order_subtotal_display = MyLabel(object_name='order_subtotal_display', text=f"0.00")
        self.order_discount_display = MyLabel(object_name='order_discount_display', text=f"0.00")
        self.order_tax_display = MyLabel(object_name='order_tax_display', text=f"0.00")
        self.order_total_display = MyLabel(object_name='order_total_display', text=f"0.00")
        self.order_summary_box = MyGroupBox()
        self.order_summary_layout = MyFormLayout()
        self.order_summary_layout.addRow('Subtotal', self.order_subtotal_display)
        self.order_summary_layout.addRow('Discount', self.order_discount_display)
        self.order_summary_layout.addRow('Tax', self.order_tax_display)
        self.order_summary_layout.addRow('Total', self.order_total_display)
        self.order_summary_box.setLayout(self.order_summary_layout)

        self.discard_order_button = MyPushButton(text='Discard')
        self.lock_order_toggle_button = [
            MyPushButton(object_name='toggle', text='Lock'),
            MyPushButton(object_name='untoggle', text='Unlock')
        ]
        self.extra_order_act_b_layout = MyHBoxLayout()
        self.extra_order_act_b_layout.addWidget(self.discard_order_button)
        self.extra_order_act_b_layout.addWidget(self.lock_order_toggle_button[0],1,Qt.AlignmentFlag.AlignLeft)
        self.extra_order_act_b_layout.addWidget(self.lock_order_toggle_button[1],1,Qt.AlignmentFlag.AlignLeft)

        self.pay_order_button = MyPushButton(text=f"Pay {self.order_total_display.text()}")
        self.order_act_b_box = MyGroupBox()
        self.order_act_b_layout = MyVBoxLayout()
        self.order_act_b_layout.addLayout(self.extra_order_act_b_layout)
        self.order_act_b_layout.addWidget(self.pay_order_button)
        self.order_act_b_box.setLayout(self.order_act_b_layout)

        self.order_box = MyGroupBox()
        self.order_layout = MyVBoxLayout()
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
        self.order_table_act_box = MyGroupBox()
        self.order_table_act_layout = MyHBoxLayout()
        self.order_table_act_layout.addWidget(self.drop_all_qty_button)
        self.order_table_act_layout.addWidget(self.drop_qty_button)
        self.order_table_act_layout.addWidget(self.add_qty_button)
        self.order_table_act_layout.addWidget(self.edit_qty_button)
        self.order_table_act_box.setLayout(self.order_table_act_layout)

    pass
class MyPOSController:
    def __init__(self, model: MyPOSModel, view: MyPOSView):
        self.v = view
        self.m = model

        self.set_pos_box_conn()
        self.set_order_box_conn()
        self.load_combo_box_data()
        self.sync_ui()

    def set_pos_box_conn(self):
        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)

        self.v.barcode_scanner_field.returnPressed.connect(self.on_barcode_scanner_field_return_pressed)
        self.v.barcode_scanner_toggle_button[0].clicked.connect(lambda: self.on_barcode_scanner_toggle_button_clicked(flag=True))
        self.v.barcode_scanner_toggle_button[1].clicked.connect(lambda: self.on_barcode_scanner_toggle_button_clicked(flag=False))

        self.v.product_overview_prev_button.clicked.connect(self.on_overview_prev_button_clicked)
        self.v.product_overview_next_button.clicked.connect(self.on_overview_next_button_clicked)
        pass
    def on_filter_button_clicked(self): # IDEA: src
        text_filter = self.v.filter_field.text()
        
        self.populate_overview_table(text=text_filter, page_number=1)
        pass
    def on_barcode_scanner_toggle_button_clicked(self, flag):
        if flag is True:
            self.v.barcode_scanner_toggle_button[0].hide()
            self.v.barcode_scanner_toggle_button[1].show()
            pass
        elif flag is False:
            self.v.barcode_scanner_toggle_button[0].show()
            self.v.barcode_scanner_toggle_button[1].hide()
            pass

        self.v.barcode_scanner_field.setHidden(flag)
        pass
    def on_barcode_scanner_field_return_pressed(self):
        pass
    
    def populate_overview_table(self, text='', order_type='', page_number=1): # IDEA: src
        self.v.product_overview_prev_button.setEnabled(page_number > 1)
        self.v.product_overview_next_button.setEnabled(page_number < self.m.total_page_number)
        self.v.product_overview_page_label.setText(f"Page {page_number}/{self.m.total_page_number}")

        pos_data = pos_schema.select_product_data_as_display(text=text, order_type=order_type, page_number=page_number)

        self.v.product_overview_table.setColumnCount(1)
        self.v.product_overview_table.setRowCount(len(pos_data))

        for i, data in enumerate(pos_data):
            self.v.set_overview_table_product_display_box(data)

            self.v.product_overview_table.setCellWidget(i, 0, self.v.product_overview_act_box)

            self.v.add_products_button.clicked.connect(lambda _, data=data: self.on_add_products_button_clicked(data))
            self.v.view_data_button.clicked.connect(lambda _, data=data: self.on_view_data_button_clicked(data))
        pass
    def on_add_products_button_clicked(self, data):
        proposed_qty, confirm = QInputDialog.getInt(self.v, f"{data[0]}", 'Set quantity:', 1, 1, 9999999)

        if confirm is True:
            print(proposed_qty)
            self.set_add_product_with_custom_qty_entry(product_qty=proposed_qty, product_name=data[0], product_barcode=data[2])
        pass
    def on_view_data_button_clicked(self, data):
        product_name = str(data[0])
        product_barcode = str(data[2])

        product_data = pos_schema.select_product_data_for_view_dialog(product_name, product_barcode)

        print(product_data)

        self.v.set_view_dialog(product_data)
        self.v.view_data_dialog.setWindowTitle(f"{product_name}")

        self.set_view_data_box_conn()
        self.v.view_data_dialog.exec()
        pass
    def set_view_data_box_conn(self):
        self.v.view_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.view_data_dialog))

    def on_overview_prev_button_clicked(self):
        i = self.v.manage_order_tab.currentIndex()

        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.product_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        
        self.m.total_page_number = pos_schema.select_product_data_total_page_count(order_type=self.m.order_type_displays[i].text())
        self.populate_overview_table(page_number=self.m.page_number, order_type=self.m.order_type_displays[i].text())
        pass
    def on_overview_next_button_clicked(self):
        i = self.v.manage_order_tab.currentIndex()

        if self.m.page_number < self.m.total_page_number:
            self.m.page_number += 1

            self.v.product_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        
        self.m.total_page_number = pos_schema.select_product_data_total_page_count(order_type=self.m.order_type_displays[i].text())
        self.populate_overview_table(page_number=self.m.page_number, order_type=self.m.order_type_displays[i].text())
        pass

    def set_order_box_conn(self): #IDEA: src
        self.v.add_order_button.clicked.connect(self.on_add_order_button_clicked)
        self.v.manage_order_tab.currentChanged.connect(self.on_manage_order_tab_current_changed)
        pass
    def on_manage_order_tab_current_changed(self):
        try:
            i = self.v.manage_order_tab.currentIndex()

            self.v.order_index_label.setText(f"{self.v.manage_order_tab.tabText(i)}")

            self.sync_ui()
            pass
        except Exception as e:
            self.populate_overview_table(page_number=self.m.page_number, order_type=self.v.order_type_display.text())
            self.test_prints()
        pass
    def on_add_order_button_clicked(self):
        self.v.set_order_box()
        self.load_combo_box_data()
        self.set_order_tab_content_conn()
        
        self.m.order_number += 1

        current_i = self.v.manage_order_tab.addTab(self.v.order_box, f"Order {self.m.order_number}")

        self.m.append_order_tab_content_to_container(
            self.v.order_type_display,
            self.v.customer_name_field,
            self.v.clear_order_table_button,
            self.v.order_table,
            self.v.order_subtotal_display,
            self.v.order_discount_display,
            self.v.order_tax_display,
            self.v.order_total_display,
            self.v.discard_order_button,
            self.v.lock_order_toggle_button,
            self.v.pay_order_button,

        )
        
        self.v.manage_order_tab.setCurrentIndex(current_i)

        self.v.add_order_button.setDisabled(self.v.manage_order_tab.count() >= 10)
        self.v.order_index_label.setText(f"{self.v.manage_order_tab.tabText(current_i)}")

        print('page_number:', self.m.page_number)
        print('total_page_number:', self.m.total_page_number)

        self.sync_ui()
        self.test_prints()
        pass
    def set_order_tab_content_conn(self):
        self.v.clear_order_table_button.clicked.connect(self.on_clear_order_table_button_clicked)
        self.v.discard_order_button.clicked.connect(self.on_discard_order_button_clicked)
        self.v.lock_order_toggle_button[0].clicked.connect(lambda: self.on_lock_order_toggle_button_clicked(lock=True))
        self.v.lock_order_toggle_button[1].clicked.connect(lambda: self.on_lock_order_toggle_button_clicked(lock=False))
        self.v.pay_order_button.clicked.connect(self.on_pay_order_button_clicked)
    def on_clear_order_table_button_clicked(self):
        print('on_clear_order_table_button_clicked')
        pass
    def on_discard_order_button_clicked(self):
        print('on_discard_order_button_clicked')
        i = self.v.manage_order_tab.currentIndex()
        
        confirm = QMessageBox.warning(self.v, 'Confirm', "Discard this order?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm is QMessageBox.StandardButton.Yes:
            self.v.manage_order_tab.removeTab(i)

            self.m.remove_order_tab_content_from_container(i)

            self.v.add_order_button.setEnabled(self.v.manage_order_tab.count() < 10)
            
            self.v.order_index_label.setText(f"{self.v.manage_order_tab.tabText(i)}") if self.v.manage_order_tab.count() > 0 else self.v.order_index_label.setText(f"No order")

        self.test_prints()
        
        pass
    def on_lock_order_toggle_button_clicked(self, lock):
        print('on_lock_order_toggle_button_clicked')
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
        self.m.pay_order_buttons[i].setDisabled(lock)

        pass
    def on_pay_order_button_clicked(self):
        print('on_pay_order_button_clicked')
        pass

    # region > manage order table ---------------------------------------------------------------------------------------
    def set_add_product_with_barcode_scanner_entry(self):
        pass
    def set_add_product_with_custom_qty_entry(self, product_qty, product_name, product_barcode):
        i = self.v.manage_order_tab.currentIndex()

        print('product_name:', product_name)
        print('product_barcode:', product_barcode)

        matched_product = self.m.order_tables[i].findItems(product_name, Qt.MatchFlag.MatchExactly) # becomes list
        
        sel_data = pos_schema.select_product_data_for_order_table(product_name, product_barcode)
        sel_product_name = str(sel_data[0])
        sel_product_price = float(sel_data[1])
        sel_product_disc_value = float(sel_data[2])

        print('sel_product_name:', sel_product_name)
        print('sel_product_price:', sel_product_price)
        print('sel_product_disc_value:', sel_product_disc_value)

        if matched_product:
            for _ in matched_product:
                print('Found!')
                # update
                row_i = _.row()

                self.m.order_subtotal_displays[i].text()

                current_product_qty = int(self.m.order_tables[i].item(row_i, 1).text()) + product_qty
                current_product_amount = float(self.m.order_tables[i].item(row_i, 3).text()) + sel_product_price

                self.m.order_tables[i].item(row_i, 1).setText(f"{current_product_qty}")
                self.m.order_tables[i].item(row_i, 3).setText(f"{current_product_amount}")

        else:
            # populate
            print('matched_product:', matched_product)
            row_i = self.m.order_tables[i].rowCount() 
            self.m.order_tables[i].insertRow(row_i)

            self.v.set_order_table_act_box()
            new_product_qty = MyTableWidgetItem(text=f"{product_qty}")
            new_product_name = MyTableWidgetItem(text=f"{sel_product_name}")
            new_product_amount = MyTableWidgetItem(text=f"{sel_product_price}")

            self.m.order_tables[i].setCellWidget(row_i, 0, self.v.order_table_act_box)
            self.m.order_tables[i].setItem(row_i, 1, new_product_qty)
            self.m.order_tables[i].setItem(row_i, 2, new_product_name)
            self.m.order_tables[i].setItem(row_i, 3, new_product_amount)
            print('Not found!')

        # compute

        pass
    def set_add_product_qty_entry(self):
        pass

    def set_drop_all_product_qty_from_table(self):
        pass
    def set_drop_all_product_qty_entry(self):
        pass
    def set_drop_product_qty_entry(self):
        pass

    def set_edit_product_qty_entry(self):
        pass
    # endregion ---------------------------------------------------------------------------------------------------------

    # IDEA: if the widget uses the same connection
    def load_combo_box_data(self):
        self.v.set_order_box()
        
        self.v.order_type_field.clear()
        self.v.customer_name_field.clear()

        customer_name_data = pos_schema.select_customer_name_for_combo_box()

        self.v.order_type_field.addItem('Retail')
        self.v.order_type_field.addItem('Wholesale')
        
        self.v.customer_name_field.addItem('Guest')
        for customer_name in customer_name_data: 
            self.v.customer_name_field.addItems(customer_name)

        pass

    def sync_ui(self):
        try:
            i = self.v.manage_order_tab.currentIndex()

            self.m.total_page_number = pos_schema.select_product_data_total_page_count(order_type=self.m.order_type_displays[i].text())
            self.m.page_number = 1 if self.m.total_page_number > 0 else 0
            self.populate_overview_table(page_number=self.m.page_number, order_type=self.m.order_type_displays[i].text())
        except Exception as e:
            print(e)  
        pass
    
    def close_dialog(self, dialog: QDialog):
        dialog.close()


    def test_prints(self):
        try: 
            i = self.v.manage_order_tab.currentIndex()
            print(os.system('cls'))
            print(len(self.m.order_type_displays), end=',')
            print(len(self.m.customer_name_fields), end=',')
            print(len(self.m.clear_order_table_buttons), end=',')
            print(len(self.m.order_tables), end=',')
            print(len(self.m.order_subtotal_displays), end=',')
            print(len(self.m.order_discount_displays), end=',')
            print(len(self.m.order_tax_displays), end=',')
            print(len(self.m.order_total_displays), end=',')
            print(len(self.m.discard_order_buttons), end=',')
            print(len(self.m.pay_order_buttons))

            print(self.m.order_type_displays[i].text(), end=',')
            print(self.m.customer_name_fields[i].text(), end=',')
            print(self.m.clear_order_table_buttons[i].text(), end=',')
            print(self.m.order_tables[i], end=',')
            print(self.m.order_subtotal_displays[i].text(), end=',')
            print(self.m.order_discount_displays[i].text(), end=',')
            print(self.m.order_tax_displays[i].text(), end=',')
            print(self.m.order_total_displays[i].text(), end=',')
            print(self.m.discard_order_buttons[i].text(), end=',')
            print(self.m.pay_order_buttons[i].text())

            print(self.m.order_type_displays[i].text())
        except Exception as e:
            pass

class MyPOSWindow(MyGroupBox):
    def __init__(self, name='test', phone='test'):
        super().__init__()

        self.model = MyPOSModel(name, phone)
        self.view = MyPOSView(self.model)
        self.controller = MyPOSController(self.model, self.view)

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