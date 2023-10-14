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
from src.core.receipt_printer import *

from database.user.txn import *
from widget.user.txn import *

class MyTXNModel: # IDEA: can't use 'MySalesView' and 'MySalesController' attributes
    def __init__(self, schema: POSSchema):
        self.schema = schema

        self.page_number = 1
        self.total_page = [
            schema.count_product_list_total_pages(),
            schema.count_product_list_via_promo_total_pages(),
        ]

class MyTXNView(MyWidget): # IDEA: can only use 'MySalesModel' attributes
    def __init__(self, model: MyTXNModel):
        super().__init__(object_name='my_sales_view')

        self.model = model
        
        self.show_main_panel()

    def show_main_panel(self):
        self.show_panel_box_a()
        self.show_panel_box_b()
        self.show_panel_box_c()

        main_panel_layout = MyGridLayout()

        main_panel_layout.addWidget(self.panel_a_box,0,0)
        main_panel_layout.addWidget(self.panel_b_box,0,1,2,1)
        main_panel_layout.addWidget(self.panel_c_box,1,0)
        self.setLayout(main_panel_layout)
        pass

    def show_panel_box_a(self):
        self.panel_a_box = MyGroupBox()
        self.panel_a_layout = MyGridLayout()

        self.text_filter_field = MyLineEdit()
        self.text_filter_button = MyPushButton(text='Filter')
        self.text_filter_box = MyGroupBox()
        self.text_filter_layout = MyHBoxLayout()
        self.text_filter_layout.addWidget(self.text_filter_field)
        self.text_filter_layout.addWidget(self.text_filter_button)
        self.text_filter_box.setLayout(self.text_filter_layout)

        self.prod_list_tab = MyTabWidget()
        self.prod_list_table = [
            MyTableWidget(object_name='prod_list_table_a'),
            MyTableWidget(object_name='prod_list_table_b'),
        ]
        self.prod_list_pag_prev_button = [
            MyPushButton(text='Prev'),
            MyPushButton(text='Prev'),
        ]
        self.prod_list_pag_page_label = [
            MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page[0]}"),
            MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page[1]}"),
        ]
        self.prod_list_pag_next_button = [
            MyPushButton(text='Next'),
            MyPushButton(text='Next'),
        ]

        self.prod_list_pag_box = [
            MyGroupBox(),
            MyGroupBox(),
        ]
        self.prod_list_pag_layout = [
            MyHBoxLayout(),
            MyHBoxLayout(),
        ]
        self.prod_list_box = [
            MyGroupBox(),
            MyGroupBox(),
        ]
        self.prod_list_layout = [
            MyVBoxLayout(),
            MyVBoxLayout(),
        ]

        self.prod_list_pag_layout[0].addWidget(self.prod_list_pag_prev_button[0])
        self.prod_list_pag_layout[0].addWidget(self.prod_list_pag_page_label[0])
        self.prod_list_pag_layout[0].addWidget(self.prod_list_pag_next_button[0])
        self.prod_list_pag_box[0].setLayout(self.prod_list_pag_layout[0])

        self.prod_list_layout[0].addWidget(self.prod_list_table[0])
        self.prod_list_layout[0].addWidget(self.prod_list_pag_box[0])
        self.prod_list_box[0].setLayout(self.prod_list_layout[0])
        
        self.prod_list_pag_layout[1].addWidget(self.prod_list_pag_prev_button[1])
        self.prod_list_pag_layout[1].addWidget(self.prod_list_pag_page_label[1])
        self.prod_list_pag_layout[1].addWidget(self.prod_list_pag_next_button[1])
        self.prod_list_pag_box[1].setLayout(self.prod_list_pag_layout[1])

        self.prod_list_layout[1].addWidget(self.prod_list_table[1])
        self.prod_list_layout[1].addWidget(self.prod_list_pag_box[1])
        self.prod_list_box[1].setLayout(self.prod_list_layout[1])

        self.prod_list_tab.addTab(self.prod_list_box[0], 'Overview')
        self.prod_list_tab.addTab(self.prod_list_box[1], 'Voided')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.prod_list_tab,1,0)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def show_panel_box_b(self):
        self.panel_b_box = MyGroupBox(object_name='panel_b_box')
        self.panel_b_layout = MyVBoxLayout()

        self.add_cust_name_sel_field = MyComboBox()
        self.add_cust_order_type_field = MyComboBox()
        self.add_cust_new_tab_button = MyPushButton(text='Add')
        self.add_cust_load_button = MyPushButton(object_name='add_cust_load_button', text='Load')
        self.add_cust_box = MyGroupBox()
        self.add_cust_layout = MyHBoxLayout()
        self.add_cust_layout.addWidget(self.add_cust_name_sel_field)
        self.add_cust_layout.addWidget(self.add_cust_order_type_field)
        self.add_cust_layout.addWidget(self.add_cust_new_tab_button)
        self.add_cust_layout.addWidget(self.add_cust_load_button)
        self.add_cust_box.setLayout(self.add_cust_layout)

        self.cust_order_tab = MyTabWidget()

        # IDEA

        self.panel_b_layout.addWidget(self.add_cust_box)
        self.panel_b_layout.addWidget(self.cust_order_tab)
        self.panel_b_box.setLayout(self.panel_b_layout)
        pass
    def show_panel_box_c(self):
        self.panel_c_box = MyGroupBox()
        self.panel_c_layout = MyHBoxLayout()

        self.current_user_label = MyLabel(text=f"Current user: ?")
        self.available_prod_label = MyLabel(text=f"Product sold today: {schema.count_product()}")
        self.panel_c_layout.addWidget(self.current_user_label)
        self.panel_c_layout.addWidget(self.available_prod_label)
        self.panel_c_box.setLayout(self.panel_c_layout)
        pass

class MyTXNController: # IDEA: can use 'MySalesModel' and 'MySalesView' attributes
    def __init__(self, model: MyTXNModel, view: MyTXNView):
        self.model = model
        self.view = view

        self.populate_prod_list_table()

        self.set_panel_box_a_conn()

    def populate_prod_list_table(self, text_filter='', order_type='Retail', page_number=1):
        if self.view.cust_order_tab.count() > 0:
            self.prod_list_data = [
                schema.list_product(text_filter, order_type, page_number),
                schema.list_product_via_promo(text_filter, order_type, page_number)
            ]

            self.view.prod_list_pag_page_label[0].setText(f"Page {self.model.page_number}/{self.model.total_page[0]}")
            self.view.prod_list_pag_page_label[1].setText(f"Page {self.model.page_number}/{self.model.total_page[1]}")

            self.view.prod_list_pag_prev_button[0].setEnabled(self.model.page_number > 1)
            self.view.prod_list_pag_next_button[0].setEnabled(len(self.prod_list_data[0]) == 30)

            self.view.prod_list_pag_prev_button[1].setEnabled(self.model.page_number > 1)
            self.view.prod_list_pag_next_button[1].setEnabled(len(self.prod_list_data[1]) == 30)

            self.view.prod_list_table[0].setRowCount(len(self.prod_list_data[0]))
            self.view.prod_list_table[1].setRowCount(len(self.prod_list_data[1]))
        
            for ai, av in enumerate(self.prod_list_data[0]):
                self.prod_list_add_button = MyPushButton(text='Add')
                self.prod_list_view_button = MyPushButton(text='View')
                prod_list_table_act_box = MyGroupBox()
                prod_list_table_act_layout = MyHBoxLayout()
                prod_list_table_act_layout.addWidget(self.prod_list_add_button)
                prod_list_table_act_layout.addWidget(self.prod_list_view_button)
                prod_list_table_act_box.setLayout(prod_list_table_act_layout)

                product = QTableWidgetItem(f"{av[1]}")
                brand = QTableWidgetItem(f"{av[4]}")
                sales_group = QTableWidgetItem(f"{av[5]}")
                price = QTableWidgetItem(f"{av[8]}")
                promo = QTableWidgetItem(f"{av[10]}")
                discount = QTableWidgetItem(f"{av[11]}")

                self.view.prod_list_table[0].setCellWidget(ai, 0, prod_list_table_act_box)
                self.view.prod_list_table[0].setItem(ai, 1, product)
                self.view.prod_list_table[0].setItem(ai, 2, brand)
                self.view.prod_list_table[0].setItem(ai, 3, sales_group)
                self.view.prod_list_table[0].setItem(ai, 4, price)
                self.view.prod_list_table[0].setItem(ai, 5, promo)
                self.view.prod_list_table[0].setItem(ai, 6, discount)

                self.prod_list_add_button.clicked.connect(lambda _, av=av: self.on_prod_list_add_button_clicked(row_v=av))
                self.prod_list_view_button.clicked.connect(lambda _, av=av: self.on_prod_list_view_button_clicked(row_v=av))
                pass
            for bi, bv in enumerate(self.prod_list_data[1]):
                
                self.prod_list_add_button = MyPushButton(text='Add')
                self.prod_list_view_button = MyPushButton(text='View')
                prod_list_table_act_box = MyGroupBox()
                prod_list_table_act_layout = MyHBoxLayout()
                prod_list_table_act_layout.addWidget(self.prod_list_add_button)
                prod_list_table_act_layout.addWidget(self.prod_list_view_button)
                prod_list_table_act_box.setLayout(prod_list_table_act_layout)

                product = QTableWidgetItem(f"{bv[1]}")
                brand = QTableWidgetItem(f"{bv[4]}")
                sales_group = QTableWidgetItem(f"{bv[5]}")
                price = QTableWidgetItem(f"{bv[8]}")
                promo = QTableWidgetItem(f"{bv[10]}")
                discount = QTableWidgetItem(f"{bv[11]}")

                self.view.prod_list_table[1].setCellWidget(bi, 0, prod_list_table_act_box)
                self.view.prod_list_table[1].setItem(bi, 1, product)
                self.view.prod_list_table[1].setItem(bi, 2, brand)
                self.view.prod_list_table[1].setItem(bi, 3, sales_group)
                self.view.prod_list_table[1].setItem(bi, 4, price)
                self.view.prod_list_table[1].setItem(bi, 5, promo)
                self.view.prod_list_table[1].setItem(bi, 6, discount)

                self.prod_list_add_button.clicked.connect(lambda _, bv=bv: self.on_prod_list_add_button_clicked(row_v=bv))
                self.prod_list_view_button.clicked.connect(lambda _, bv=bv: self.on_prod_list_view_button_clicked(row_v=bv))
                pass
        else: 
            self.view.prod_list_pag_prev_button[0].setDisabled(True)
            self.view.prod_list_pag_next_button[0].setDisabled(True)
            
            self.view.prod_list_pag_prev_button[1].setDisabled(True)
            self.view.prod_list_pag_next_button[1].setDisabled(True)

            self.view.prod_list_pag_page_label[0].setText(f"Page 0/0")
            self.view.prod_list_pag_page_label[1].setText(f"Page 0/0")

            self.view.prod_list_table[0].setRowCount(0)
            self.view.prod_list_table[1].setRowCount(0)
        pass

    def set_panel_box_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)

        self.view.prod_list_tab.currentChanged.connect(self.on_prod_list_tab_current_changed)
        self.view.prod_list_pag_prev_button[0].clicked.connect(self.on_prod_list_pag_prev_button_clicked)
        self.view.prod_list_pag_next_button[0].clicked.connect(self.on_prod_list_pag_next_button_clicked)
        self.view.prod_list_pag_prev_button[1].clicked.connect(self.on_prod_list_pag_prev_button_clicked)
        self.view.prod_list_pag_next_button[1].clicked.connect(self.on_prod_list_pag_next_button_clicked)
        pass

    def on_text_filter_button_clicked(self):
        i = self.view.cust_order_tab.currentIndex()

        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    
    def on_prod_list_tab_current_changed(self):
        if self.view.cust_order_tab.count() > 0:
            i = self.view.cust_order_tab.currentIndex()

            self.model.page_number = 1

            self.view.prod_list_pag_page_label[0].setText(f"Page {self.model.page_number}/{self.model.total_page[0]}")
            self.view.prod_list_pag_page_label[1].setText(f"Page {self.model.page_number}/{self.model.total_page[1]}")

            self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    def on_prod_list_add_button_clicked(self, row_v):
        # DONE: add_button
        i = self.view.cust_order_tab.currentIndex()

        if self.view.cust_order_tab.count() > 0:
            while True:
                prop_quantity, confirm = QInputDialog.getText(self.view, 'Add', 'Input quantity:')

                if confirm == True:
                    try: 
                        if int(prop_quantity) > 0:
                            cust_order_list = self.model.cust_order_tables[i].findItems(row_v[1], Qt.MatchFlag.MatchExactly) # finds the item in the table by matching the item name
                            
                            if cust_order_list: # if order list exist
                                for item_v in cust_order_list:
                                    item_i = item_v.row()  # get row index
                                    current_quantity = int(self.model.cust_order_tables[i].item(item_i, 1).text().replace('x', ''))  # Get the current value and convert it to an integer
                                    current_price = float(self.model.cust_order_tables[i].item(item_i, 3).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]
                                    current_discount = float(self.model.cust_order_tables[i].item(item_i, 4).text().replace('₱', ''))  # Remove '₱' and convert to an integer[]

                                    self.model.new_quantity = int(current_quantity + int(prop_quantity))
                                    self.model.new_price = current_price + (float(row_v[8]) * int(prop_quantity))
                                    self.model.new_discount = current_discount + (float(row_v[11]) * int(prop_quantity))

                                    quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                                    price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")  # Create a new 
                                    discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")  # Create a new 

                                    self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                                    self.model.cust_order_tables[i].setItem(item_i, 3, price)
                                    self.model.cust_order_tables[i].setItem(item_i, 4, discount)
                                pass
                            else:
                                item_i = self.model.cust_order_tables[i].rowCount()

                                self.model.cust_order_tables[i].insertRow(item_i)
                                
                                self.model.new_quantity = int(prop_quantity)
                                self.model.new_price = float(row_v[8]) * int(prop_quantity)
                                self.model.new_discount = float(row_v[11]) * int(prop_quantity)

                                self.drop_all_quantity_button = MyPushButton(text='Drop all')
                                self.drop_quantity_button = MyPushButton(text='Drop')
                                self.add_quantity_button = MyPushButton(text='Add')
                                self.edit_quantity_button = MyPushButton(text='Edit')
                                cust_order_table_act_box = MyGroupBox()
                                cust_order_table_act_box_layout = MyHBoxLayout()
                                cust_order_table_act_box_layout.addWidget(self.drop_all_quantity_button)
                                cust_order_table_act_box_layout.addWidget(self.drop_quantity_button)
                                cust_order_table_act_box_layout.addWidget(self.add_quantity_button)
                                cust_order_table_act_box_layout.addWidget(self.edit_quantity_button)
                                cust_order_table_act_box.setLayout(cust_order_table_act_box_layout)

                                quantity = QTableWidgetItem(f"{self.model.new_quantity}")  # Create a new 
                                item_name = QTableWidgetItem(str(row_v[1]))
                                price = QTableWidgetItem(f"₱{self.model.new_price:.2f}")
                                discount = QTableWidgetItem(f"₱{self.model.new_discount:.2f}")
                    
                                self.model.cust_order_tables[i].setCellWidget(item_i, 0, cust_order_table_act_box)
                                self.model.cust_order_tables[i].setItem(item_i, 1, quantity)
                                self.model.cust_order_tables[i].setItem(item_i, 2, item_name)
                                self.model.cust_order_tables[i].setItem(item_i, 3, price)
                                self.model.cust_order_tables[i].setItem(item_i, 4, discount)

                                self.drop_all_quantity_button.clicked.connect(lambda: self.on_drop_all_quantity_button_clicked(row_v))
                                self.drop_quantity_button.clicked.connect(lambda: self.on_drop_quantity_button_clicked(row_v))
                                self.add_quantity_button.clicked.connect(lambda: self.on_add_quantity_button_clicked(row_v))
                                self.edit_quantity_button.clicked.connect(lambda: self.on_edit_quantity_button_clicked(row_v))


                            self.model.cust_order_subtotal_values[i] += (float(row_v[8]) * int(prop_quantity))
                            self.model.cust_order_discount_values[i] += (float(row_v[11]) * int(prop_quantity))
                            self.model.cust_order_tax_values[i] += (0 * int(prop_quantity))
                            self.model.cust_order_total_values[i] = (self.model.cust_order_subtotal_values[i] - self.model.cust_order_discount_values[i]) + self.model.cust_order_tax_values[i]

                            self.model.cust_order_subtotal_labels[i].setText(f"₱{self.model.cust_order_subtotal_values[i]:.2f}")
                            self.model.cust_order_discount_labels[i].setText(f"₱{self.model.cust_order_discount_values[i]:.2f}")
                            self.model.cust_order_tax_labels[i].setText(f"₱{self.model.cust_order_tax_values[i]:.2f}")
                            self.model.cust_order_total_labels[i].setText(f"₱{self.model.cust_order_total_values[i]:.2f}")

                            self.model.cust_order_pay_buttons[i].setText(f"Pay ₱{self.model.cust_order_total_values[i]:.2f}")

                            break
                            pass
                        else:
                            QMessageBox.critical(self.view, 'Error', 'Must be greater than 0.')
                            pass
                    except ValueError as e:
                        QMessageBox.critical(self.view, 'Error', 'Invalid input.')
                else:
                    break
        else:
            QMessageBox.critical(self.view, 'Error', 'Must add order first.')

        self.new_quantity = 0
        self.new_price = 0
        pass
    def on_prod_list_view_button_clicked(self, row_v):
        self.view_dialog = MyDialog(parent=self.view)
        self.view_layout = MyFormLayout()

        item_data = [
            ['Barcode:', MyLabel(text=f"{row_v[0]}")],
            ['Item name:', MyLabel(text=f"{row_v[1]}")],
            ['Expire dt:', MyLabel(text=f"{row_v[2]}")],
            [None, MyLabel(text='<hr>')],
            ['Item type:', MyLabel(text=f"{row_v[3]}")],
            ['Brand:', MyLabel(text=f"{row_v[4]}")],
            ['Sales group:', MyLabel(text=f"{row_v[5]}")],
            ['Supplier:', MyLabel(text=f"{row_v[6]}")],
            [None, MyLabel(text='<hr>')],
            ['Cost:', MyLabel(text=f"{row_v[7]}")],
            ['Sell price:', MyLabel(text=f"{row_v[8]}")],
            ['Effective dt:', MyLabel(text=f"{row_v[9]}")],
            ['Promo name:', MyLabel(text=f"{row_v[10]}")],
            ['Discount value:', MyLabel(text=f"{row_v[11]}")],
            [None, MyLabel(text='<hr>')],
            ['Inventory tracking:', MyLabel(text=f"{row_v[12]}")],
            ['Available stock:', MyLabel(text=f"{row_v[13]}")],
            ['On hand stock:', MyLabel(text=f"{row_v[14]}")],
        ]

        for label, data in item_data:
            if label:
                self.view_layout.addRow(label, data)
            else:
                self.view_layout.addRow(data)

        self.view_dialog.setLayout(self.view_layout)

        self.view_dialog.exec()
        pass
    def on_prod_list_pag_prev_button_clicked(self):
        i = self.view.cust_order_tab.currentIndex()
        
        if self.model.page_number > 1:
            self.model.page_number -= 1
            self.view.prod_list_pag_page_label[0].setText(f"Page {self.model.page_number}/{self.model.total_page[0]}")
            self.view.prod_list_pag_page_label[1].setText(f"Page {self.model.page_number}/{self.model.total_page[1]}")

        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass
    def on_prod_list_pag_next_button_clicked(self):
        i = self.view.cust_order_tab.currentIndex()
        
        self.model.page_number += 1
        self.view.prod_list_pag_page_label[0].setText(f"Page {self.model.page_number}/{self.model.total_page[0]}")
        self.view.prod_list_pag_page_label[1].setText(f"Page {self.model.page_number}/{self.model.total_page[1]}")
        
        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), order_type=self.model.cust_order_type_values[i], page_number=self.model.page_number)
        pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)

    schema = POSSchema()

    model = MyTXNModel(schema)
    view = MyTXNView(model)
    controller = MyTXNController(model, view)

    view.show()
    sys.exit(app.exec())
