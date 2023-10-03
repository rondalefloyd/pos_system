import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))
print('sys path: ', os.path.abspath(''))

from src.core.color_scheme import *
from src.core.manual_csv_importer import *

from src.database.admin.product import *
from src.database.admin.promo import *
from src.database.admin.reward import *
from src.database.admin.customer import *
from src.database.admin.user import *

from src.widget.user.sales import *

color_scheme = ColorScheme()

class SalesWindow(MyWidget):
    def __init__(self):
        super().__init__()

        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):
        self.product_schema = ProductSchema()
        self.promo_schema = PromoSchema()
        self.reward_schema = RewardSchema()
        self.customer_schema = CustomerSchema()
        self.user_schema = UserSchema()

        self.my_push_button = MyPushButton()

        self.cart_list = []
        self.bill_value = [] 
        self.bill_label = []
        self.pay_button = []

        self.cart_tab_curr_index = 0
        self.data_list_curr_page = 1
        self.selected_promo_id = None

        self.required_field_indicator = "<font color='red'>-- required</font>"

        self.total_product_count = self.product_schema.count_product()
        pass
    def sync_ui(self):
        self.populate_all_combo_box()
        self.populate_data_list_table()

        self.data_mgt_untoggle_aatc_button.hide()

        self.customer_name_field.setCurrentText('')

        self.total_data.setText(f'Total promo: {self.promo_schema.count_promo()}')
        pass

    def style_data_list_action_button(self):
        self.data_list_atc_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.data_list_view_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        pass
    def style_data_list_pgn_action_button(self):
        self.data_list_pgn_prev_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.data_list_pgn_next_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        pass
    def style_sales_mgt_action_button(self):
        self.add_cart_tab_button.setStyleSheet(self.my_push_button.add_cart_tab_button_ss)
        pass
    def style_data_mgt_action_button(self):
        self.data_mgt_sync_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        self.data_mgt_toggle_aatc_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        self.data_mgt_untoggle_aatc_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        pass

    def on_data_list_atc_button_clicked(self, row_value, atc_button):
        
        current_index = self.cart_tab.currentIndex()

        try:
            self.bill_value[current_index][0] += row_value[8]
            self.bill_value[current_index][1] += row_value[11]
            self.bill_value[current_index][2] = 0
            self.bill_value[current_index][3] = (self.bill_value[current_index][0] - self.bill_value[current_index][1]) + self.bill_value[current_index][2]

            self.bill_label[current_index][0].setText(f'₱{self.bill_value[current_index][0]:.2f}') # sub_total_label
            self.bill_label[current_index][1].setText(f'₱{self.bill_value[current_index][1]:.2f}') # discount_label
            self.bill_label[current_index][2].setText(f'₱{self.bill_value[current_index][2]:.2f}') # tax_label
            self.bill_label[current_index][3].setText(f'₱{self.bill_value[current_index][3]:.2f}') # total_label
            self.pay_button[current_index].setText(f'PAY ₱{self.bill_value[current_index][3]:.2f}')

            # !!! CHECKPOINT !!!
            pass
        except Exception as e:
            print(e)

        print(self.bill_value[current_index][0], end=', ')
        print(self.bill_value[current_index][1], end=', ')
        print(self.bill_value[current_index][2], end=', ')
        print(self.bill_value[current_index][3], end=', ')

        pass
    def on_data_list_view_button_clicked(self, row_value, view_button):
        self.data_list_view_dialog = MyDialog(object_name='data_list_view_dialog', parent=self)
        self.data_list_view_dialog_layout = MyFormLayout()

        barcode_info = MyLabel(object_name='barcode_info', text=str(row_value[0]))
        item_name_info = MyLabel(object_name='item_name_info', text=str(row_value[1]))
        expire_dt_info = MyLabel(object_name='expire_dt_info', text=str(row_value[2]))

        item_type_info = MyLabel(object_name='item_type_info', text=str(row_value[3]))
        brand_info = MyLabel(object_name='brand_info', text=str(row_value[4]))
        sales_group_info = MyLabel(object_name='sales_group_info', text=str(row_value[5]))
        supplier_info = MyLabel(object_name='supplier_info', text=str(row_value[6]))

        cost_info = MyLabel(object_name='cost_info', text=f'₱{row_value[7]}')
        sell_price_info = MyLabel(object_name='sell_price_info', text=f'₱{row_value[8]}')
        effective_dt_info = MyLabel(object_name='effective_dt_info', text=str(row_value[9]))
        promo_name_info = MyLabel(object_name='promo_name_info', text=str(row_value[10]))
        discount_value_info = MyLabel(object_name='discount_value_info', text=f'₱{row_value[11]}')

        inventory_tracking_info = MyLabel(object_name='inventory_tracking_info', text=str(row_value[12]))

        date_created_info = MyLabel(object_name='date_created_info', text=str(row_value[15]))

        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Barcode:'), barcode_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Item name:'), item_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Expire date:'), expire_dt_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Item type:'), item_type_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Brand:'), brand_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Sales group:'), sales_group_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Supplier:'), supplier_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Cost:'), cost_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Sell price:'), sell_price_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Effective date:'), effective_dt_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Promo name:'), promo_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Discount value:'), discount_value_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Inventory tracking:'), inventory_tracking_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Date and time created:'), date_created_info)
        self.data_list_view_dialog.setLayout(self.data_list_view_dialog_layout)

        self.data_list_view_dialog.exec()
        pass

    def on_add_cart_tab_button_clicked(self):
        self.populate_cart_tab(cart_tab_name=self.customer_name_field.currentText())

        pass
    def on_cart_tab_current_changed(self):
        current_index = self.cart_tab.currentIndex()
        
        try:
            print(self.bill_value[current_index][0], end=', ')
            print(self.bill_value[current_index][1], end=', ')
            print(self.bill_value[current_index][2], end=', ')
            print(self.bill_value[current_index][3])
        except Exception as e:
            print(e)

    
    def on_sales_mgt_discard_button_clicked(self):
        # Close the tab at the current index
        if self.cart_tab.currentIndex() >= 0:
            self.cart_tab.removeTab(self.cart_tab.currentIndex())

        pass
    def on_sales_mgt_pay_button_clicked(self):
        # region > convert field input into str
        print('sub_total:', self.sub_total_value)
        print('discount:', self.discount_value)
        print('tax:', self.tax_value)
        print('total:', self.total_value)
        # endregion
        pass
    
    # region > data_mgt_button
    def on_data_mgt_sync_button_clicked(self):
        self.sync_ui()

        pass
    def on_data_mgt_toggle_aatc_button_clicked(self):
        self.data_mgt_toggle_aatc_button.hide()
        self.data_mgt_untoggle_aatc_button.show()
        pass
    def on_data_mgt_untoggle_aatc_button_clicked(self):
        self.data_mgt_toggle_aatc_button.show()
        self.data_mgt_untoggle_aatc_button.hide()
        pass
    # endregion
    
    def on_data_list_pgn_prev_button_clicked(self):
        
        if self.data_list_curr_page > 1:
            self.data_list_curr_page -= 1
            self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')

        self.populate_data_list_table(current_page=self.data_list_curr_page)

        pass
    def on_data_list_pgn_next_button_clicked(self):
        
        self.data_list_curr_page += 1
        self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')
        
        self.populate_data_list_table(current_page=self.data_list_curr_page)
        
        pass
        pass

    def on_text_filter_field_text_changed(self):
        self.data_list_curr_page = 1
        self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')
        self.populate_data_list_table(text_filter=str(self.text_filter_field.text()), current_page=self.data_list_curr_page)
        pass
    
    def populate_cart_list_table(self, cart_list):
        current_index = self.cart_tab.currentIndex()
        # AGENDA: data list for cart or appended items (i.e. item name, qty, price)
        # !!! CHECKPOINT !!!
        pass
    def populate_cart_tab(self, cart_tab_name=''):
        cart_tab_name = f'New customer' if self.cart_tab.count() == 0 else cart_tab_name
        cart_tab_name = f'New customer ({self.cart_tab.count()+1})' if cart_tab_name == '' else cart_tab_name
        # region > bill_value
        sub_total_value = 0
        discount_value = 0
        tax_value = 0
        total_value = 0
        # endregion

        cart_panel = MyGroupBox(object_name='cart_panel')
        cart_panel_layout = MyGridLayout(object_name='cart_panel_layout')

        # region > cart_list_table
        cart_list_table = MyTableWidget(object_name='cart_list_table')
        # endregion
        # region > cart_list_bill
        cart_list_bill = MyGroupBox(object_name='cart_list_bill')
        cart_list_bill_layout = MyFormLayout(object_name='cart_list_bill_layout')
        sub_total_value_label = MyLabel(object_name='bill_value_label', text=f'₱{sub_total_value:.2f}')
        discount_value_label = MyLabel(object_name='bill_value_label', text=f'₱{discount_value:.2f}')
        tax_value_label = MyLabel(object_name='bill_value_label', text=f'₱{tax_value:.2f}')
        total_value_label = MyLabel(object_name='bill_value_label', text=f'₱{total_value:.2f}')
        cart_list_bill_layout.addRow('Sub total', sub_total_value_label)
        cart_list_bill_layout.addRow('Discount', discount_value_label)
        cart_list_bill_layout.addRow('Tax', tax_value_label)
        cart_list_bill_layout.addRow('Total', total_value_label)
        cart_list_bill.setLayout(cart_list_bill_layout)
        # endregion
        # region > sales_mgt_action
        sales_mgt_action_panel = MyGroupBox(object_name='sales_mgt_action_panel') # head.b
        sales_mgt_action_panel_layout = MyHBoxLayout(object_name='sales_mgt_action_panel_layout')
        sales_mgt_discard_button = MyPushButton(object_name='sales_mgt_discard_button', text='Discard')
        sales_mgt_pay_button = MyPushButton(object_name='sales_mgt_pay_button', text=f'PAY ₱{total_value}')
        sales_mgt_action_panel_layout.addWidget(sales_mgt_discard_button)
        sales_mgt_action_panel_layout.addWidget(sales_mgt_pay_button)
        sales_mgt_action_panel.setLayout(sales_mgt_action_panel_layout)
        # endregion

        cart_panel_layout.addWidget(cart_list_table)
        cart_panel_layout.addWidget(cart_list_bill)
        cart_panel_layout.addWidget(sales_mgt_action_panel)
        cart_panel.setLayout(cart_panel_layout)
        
        # region > button_connections
        sales_mgt_discard_button.clicked.connect(self.on_sales_mgt_discard_button_clicked)
        sales_mgt_pay_button.clicked.connect(self.on_sales_mgt_pay_button_clicked)
        # endregion

        # region > style_buttons
        sales_mgt_discard_button.setStyleSheet(self.my_push_button.sales_mgt_discard_button_ss)
        sales_mgt_pay_button.setStyleSheet(self.my_push_button.sales_mgt_pay_button_ss)

        cart_tab_index = self.cart_tab.addTab(cart_panel, f'{cart_tab_name}')
        self.cart_list.append((cart_list_table))
        self.bill_value.append([sub_total_value, discount_value, tax_value, total_value])
        self.bill_label.append((sub_total_value_label, discount_value_label, tax_value_label, total_value_label))
        self.pay_button.append((sales_mgt_pay_button))

        self.cart_tab.setCurrentIndex(cart_tab_index)
        # endregion
        pass
    def populate_all_combo_box(self):
        customer_name_list = self.customer_schema.list_customer()

        self.customer_name_field.addItem('Customer')
        for customer_name in customer_name_list:
            self.customer_name_field.addItem(customer_name[0])
        pass
    def populate_data_list_table(self, text_filter='', current_page=1):
        # region > data_list_clear_contents
        self.data_list_table.clearContents()
        # endregion

        # region > data_list
        product_data = self.product_schema.list_product(text_filter=text_filter, page_number=current_page)
        # endregion

        # region > data_list_pgn_button_set_enabled
        self.data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)
        self.data_list_pgn_next_button.setEnabled(len(product_data) == 30)
        # endregion

        # region > clicked_data_list_set_disabled
        # endregion
        
        # region > data_list_table_set_row_count
        self.data_list_table.setRowCount(len(product_data))
        # endregion

        for row_index, row_value in enumerate(product_data):
            # region > data_list_action
            self.data_list_action_panel = MyGroupBox(object_name='data_list_action_panel') # head.a
            self.data_list_action_panel_layout = MyHBoxLayout(object_name='data_list_action_panel_layout')
            
            # region > set_data_list_action_buttons
            self.data_list_atc_button = MyPushButton(object_name='data_list_atc_button', text='Add')
            self.data_list_view_button = MyPushButton(object_name='data_list_view_button', text='View')
            # endregion

            # region > data_list_action_button_connections
            self.data_list_atc_button.clicked.connect(lambda _, row_value=row_value, atc_button=self.data_list_atc_button: self.on_data_list_atc_button_clicked(row_value, atc_button))
            self.data_list_view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.data_list_view_button: self.on_data_list_view_button_clicked(row_value, view_button))
            # endregion

            # region > style_data_list_action_buttons
            self.style_data_list_action_button()
            # endregion

            self.data_list_action_panel_layout.addWidget(self.data_list_atc_button)
            self.data_list_action_panel_layout.addWidget(self.data_list_view_button)
            self.data_list_action_panel.setLayout(self.data_list_action_panel_layout)
            # endregion

            # region > set_table_item_values
            barcode = QTableWidgetItem(str(row_value[0]))
            item_name = QTableWidgetItem(str(row_value[1]))
            brand = QTableWidgetItem(str(row_value[4]))
            sell_price = QTableWidgetItem(f'₱{row_value[8]:.2f}')
            # endregion

            # region > set_table_item_alignment
            barcode.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            sell_price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            # endregion
        
            # region > set_data_list_table_cells
            self.data_list_table.setCellWidget(row_index, 0, self.data_list_action_panel)
            self.data_list_table.setItem(row_index, 1, barcode)
            self.data_list_table.setItem(row_index, 2, item_name)
            self.data_list_table.setItem(row_index, 3, brand)
            self.data_list_table.setItem(row_index, 4, sell_price)
            # endregion

        pass

    def show_extra_info_panel(self):
        self.extra_info_panel = MyGroupBox(object_name='extra_info_panel') # head.d
        self.extra_info_panel_layout = MyHBoxLayout(object_name='extra_info_panel_layout')

        # region > extra_info_labels
        self.total_data = MyLabel(object_name='total_data', text=f'Total promo: {self.total_product_count}')
        # endregion

        self.extra_info_panel_layout.addWidget(self.total_data,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.extra_info_panel.setLayout(self.extra_info_panel_layout)
        pass
    def show_sales_mgt_panel(self):
        self.sales_mgt_panel = MyGroupBox(object_name='sales_mgt_panel')
        self.sales_mgt_panel_layout = MyVBoxLayout(object_name='sales_mgt_panel_layout')

        # region > add_cart_tab
        self.add_cart_tab_panel = MyGroupBox(object_name='add_cart_tab_panel')
        self.add_cart_tab_panel_layout = MyHBoxLayout(object_name='add_cart_tab_panel_layout')
        self.customer_name_field = MyComboBox(object_name='customer_name_field')
        self.add_cart_tab_button = MyPushButton(object_name='add_cart_tab_button')
        self.add_cart_tab_panel_layout.addWidget(self.customer_name_field,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignHCenter)
        self.add_cart_tab_panel_layout.addWidget(self.add_cart_tab_button)
        self.add_cart_tab_panel.setLayout(self.add_cart_tab_panel_layout)
        # endregion
        # region > cart_tab
        self.cart_tab = MyTabWidget(object_name='cart_tab')
        # endregion

        # region > sales_mgt_connections
        self.add_cart_tab_button.clicked.connect(self.on_add_cart_tab_button_clicked)
        self.cart_tab.currentChanged.connect(self.on_cart_tab_current_changed)
        # endregion
        
        # region > style_sales_mgt_buttons
        self.style_sales_mgt_action_button()
        # endregion

        self.sales_mgt_panel_layout.addWidget(self.add_cart_tab_panel)
        self.sales_mgt_panel_layout.addWidget(self.cart_tab)
        self.sales_mgt_panel.setLayout(self.sales_mgt_panel_layout)
        pass
    def show_content_panel(self):
        self.content_panel = MyGroupBox(object_name='content_panel')
        self.content_panel_layout = MyGridLayout(object_name='content_panel_layout')

        # region > text_filter
        self.text_filter_field = MyLineEdit(object_name='text_filter_field') # head.a
        # endregion
        # region > data_mgt_action
        self.data_mgt_action_panel = MyGroupBox(object_name='data_mgt_action_panel') # head.b
        self.data_mgt_action_panel_layout = MyHBoxLayout(object_name='data_mgt_action_panel_layout')
        self.data_mgt_sync_button = MyPushButton(object_name='data_mgt_sync_button')
        self.data_mgt_toggle_aatc_button = MyPushButton(object_name='data_mgt_toggle_aatc_button')
        self.data_mgt_untoggle_aatc_button = MyPushButton(object_name='data_mgt_untoggle_aatc_button')
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_sync_button)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_toggle_aatc_button)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_untoggle_aatc_button)
        self.data_mgt_action_panel.setLayout(self.data_mgt_action_panel_layout)
        # endregion
        # region > data_list_sorter
        self.data_list_sorter_tab = MyTabWidget(object_name='data_list_sorter_tab') # head.c
        self.data_list_pgn_panel = MyGroupBox(object_name='data_list_pgn_panel') # head.c.a
        self.data_list_pgn_panel_layout = MyVBoxLayout(object_name='data_list_pgn_panel_layout')
        self.data_list_table = MyTableWidget(object_name='data_list_table')
        self.data_list_pgn_action_panel = MyGroupBox(object_name='data_list_pgn_action_panel')
        self.data_list_pgn_action_panel_layout = MyGridLayout(object_name='data_list_pgn_action_panel_layout')
        self.data_list_pgn_prev_button = MyPushButton(object_name='data_list_pgn_prev_button')
        self.data_list_pgn_page = MyLabel(object_name='data_list_pgn_page', text='Page 1')
        self.data_list_pgn_next_button = MyPushButton(object_name='data_list_pgn_next_button')
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_prev_button,0,0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_page,0,1, Qt.AlignmentFlag.AlignCenter)
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_next_button,0,2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.data_list_pgn_action_panel.setLayout(self.data_list_pgn_action_panel_layout)
        self.data_list_pgn_panel_layout.addWidget(self.data_list_table)
        self.data_list_pgn_panel_layout.addWidget(self.data_list_pgn_action_panel)
        self.data_list_pgn_panel.setLayout(self.data_list_pgn_panel_layout)
        self.data_list_sorter_tab.addTab(self.data_list_pgn_panel, 'Overview')
        # endregion

        # region > content_button_connections
        self.data_mgt_sync_button.clicked.connect(self.on_data_mgt_sync_button_clicked)
        self.data_mgt_toggle_aatc_button.clicked.connect(self.on_data_mgt_toggle_aatc_button_clicked)
        self.data_mgt_untoggle_aatc_button.clicked.connect(self.on_data_mgt_untoggle_aatc_button_clicked)

        self.data_list_pgn_prev_button.clicked.connect(self.on_data_list_pgn_prev_button_clicked)
        self.data_list_pgn_next_button.clicked.connect(self.on_data_list_pgn_next_button_clicked)
        # endregion

        # region > content_text_filter_connection
        self.text_filter_field.textChanged.connect(self.on_text_filter_field_text_changed)
        # endregion

        # region > style_content_buttons
        self.style_data_mgt_action_button()
        self.style_data_list_pgn_action_button()
        # endregion

        self.content_panel_layout.addWidget(self.text_filter_field,0,0)
        self.content_panel_layout.addWidget(self.data_mgt_action_panel,0,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.content_panel_layout.addWidget(self.data_list_sorter_tab,1,0,1,2)
        self.content_panel.setLayout(self.content_panel_layout)
        pass
    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(object_name='main_panel_layout')

        self.show_content_panel()
        self.show_sales_mgt_panel()
        self.show_extra_info_panel()

        self.main_panel_layout.addWidget(self.content_panel,0,0)
        self.main_panel_layout.addWidget(self.sales_mgt_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.extra_info_panel,1,0)
        self.setLayout(self.main_panel_layout)
    
if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = SalesWindow()
    window.show()
    sys.exit(pos_app.exec())
