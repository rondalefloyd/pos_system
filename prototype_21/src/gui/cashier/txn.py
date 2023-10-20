
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
from src.sql.cashier.txn import *
from src.widget.admin.admin import *
from templates.qss.qss_config import QSSConfig

schema = MyTXNSchema()
qss = QSSConfig()

class MyTXNModel: # NOTE: entries
    def __init__(self, name, phone):
        # NOTE: global variables
        self.gdrive_path = 'G:' + f"/My Drive/"
        self.user_name = name
        self.user_phone = phone

        self.init_selected_txn_data_entry()
        self.init_progress_data_entry()
        self.init_txn_list_page_entry()

    def init_txn_list_page_entry(self):
        self.page_number = 1
        self.total_page_number = schema.select_item_sold_total_pages_count()

    def init_selected_txn_data_entry(self):
        self.sel_txn_name_value = None
        self.sel_txn_type_value = None
        self.sel_txn_percent_value = None
        self.sel_txn_description_value = None
        self.sel_datetime_created_value = None
        self.sel_txn_id_value = None
        pass
    def assign_selected_txn_data_entry(self, value):
        self.sel_txn_id_value = value[9]

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

    def import_txn_entry(self, data_frame):
        self.txn_import_thread = MyDataImportThread(data_name='txn', data_frame=data_frame) # NOTE: ths is QThread for data import
        self.txn_import_thread.start()

    def setup_manage_txn_panel(self, window_title):
        self.manage_txn_dialog = MyDialog(window_title=window_title)
        self.manage_txn_layout = MyGridLayout()

        self.txn_void_reason_label = MyLabel(text='Reason')
        self.txn_void_reason_field = MyComboBox(object_name='txn_name_field')
        self.txn_form_box = MyGroupBox()
        self.txn_form_layout = MyFormLayout()
        self.txn_form_layout.addRow(self.txn_void_reason_label)
        self.txn_form_layout.addRow(self.txn_void_reason_field)
        self.txn_form_box.setLayout(self.txn_form_layout)
        self.txn_form_scra = MyScrollArea()
        self.txn_form_scra.setWidget(self.txn_form_box)

        self.manage_txn_save_button = MyPushButton(text='Save')
        self.manage_txn_close_button = MyPushButton(text='Close')
        self.manage_txn_act_box = MyGroupBox()
        self.manage_txn_act_layout = MyHBoxLayout(object_name='txn_act_layout')
        self.manage_txn_act_layout.addWidget(self.manage_txn_save_button)
        self.manage_txn_act_layout.addWidget(self.manage_txn_close_button)
        self.manage_txn_act_box.setLayout(self.manage_txn_act_layout)

        self.manage_txn_layout.addWidget(self.txn_form_scra,0,0)
        self.manage_txn_layout.addWidget(self.manage_txn_act_box,1,0,Qt.AlignmentFlag.AlignRight)
        self.manage_txn_dialog.setLayout(self.manage_txn_layout)
        pass
    def save_edit_txn_entry(self):
        void_reason = self.txn_void_reason_field.currentText()
        schema.update_selected_item_sold_void(item_sold_id=self.sel_txn_id_value, reason_id=void_reason)

        self.sel_txn_id_value = 0
        self.manage_txn_dialog.close()
        pass
    
    def setup_view_txn_panel(self):
        self.view_dialog = MyDialog(window_title=f"{self.sel_txn_name_value}")
        self.view_layout = MyGridLayout()

        self.txn_name_info_label = MyLabel(text=f"{self.sel_txn_name_value}")
        self.txn_type_info_label = MyLabel(text=f"{self.sel_txn_type_value}")
        self.txn_percent_info_label = MyLabel(text=f"{self.sel_txn_percent_value}")
        self.txn_description_info_label = MyLabel(text=f"{self.sel_txn_description_value}")
        self.datetime_created_info_label = MyLabel(text=f"{self.sel_datetime_created_value}")
        self.view_form_box = MyGroupBox()
        self.view_form_layout = MyFormLayout()
        self.view_form_layout.addRow('Name', self.txn_name_info_label)
        self.view_form_layout.addRow('Type', self.txn_type_info_label)
        self.view_form_layout.addRow('Percent', self.txn_percent_info_label)
        self.view_form_layout.addRow('Description', self.txn_description_info_label)
        self.view_form_layout.addRow('Date/Time created', self.datetime_created_info_label)
        self.view_form_box.setLayout(self.view_form_layout)
        self.view_form_scra = MyScrollArea()
        self.view_form_scra.setWidget(self.view_form_box)

        self.view_form_close_button = MyPushButton(text='Close')

        self.view_layout.addWidget(self.view_form_scra,0,0)
        self.view_layout.addWidget(self.view_form_close_button,1,0,Qt.AlignmentFlag.AlignRight)
        self.view_dialog.setLayout(self.view_layout)
    
    pass
class MyTXNView(MyGroupBox): # NOTE: layout
    def __init__(self, model: MyTXNModel):
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
        self.interactive_act_box = MyGroupBox()
        self.interactive_act_layout = MyHBoxLayout()
        self.interactive_act_layout.addWidget(self.sync_ui_button)
        self.interactive_act_box.setLayout(self.interactive_act_layout)

        self.txn_list_table = MyTableWidget(object_name='txn_list_table')
        self.txn_list_prev_button = MyPushButton(text='Prev')
        self.txn_list_page_label = MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.txn_list_next_button = MyPushButton(text='Next')
        self.txn_list_pag_box = MyGroupBox()
        self.txn_list_pag_layout = MyHBoxLayout(object_name='txn_list_pag_layout')
        self.txn_list_pag_layout.addWidget(self.txn_list_prev_button)
        self.txn_list_pag_layout.addWidget(self.txn_list_page_label)
        self.txn_list_pag_layout.addWidget(self.txn_list_next_button)
        self.txn_list_pag_box.setLayout(self.txn_list_pag_layout)
        self.txn_list_box = MyGroupBox()
        self.txn_list_layout = MyGridLayout()
        self.txn_list_layout.addWidget(self.txn_list_table,0,0)
        self.txn_list_layout.addWidget(self.txn_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.txn_list_box.setLayout(self.txn_list_layout)
        self.txn_list_tab = MyTabWidget()
        self.txn_list_tab.addTab(self.txn_list_box, 'Overview')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.interactive_act_box,0,1)
        self.panel_a_layout.addWidget(self.txn_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    pass 
class MyTXNController: # NOTE: connections, setting attributes
    def __init__(self, model: MyTXNModel, view: MyTXNView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_txn_list_table()

    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.view.txn_list_prev_button.clicked.connect(lambda: self.on_txn_list_pag_button_clicked(action='go_prev'))
        self.view.txn_list_next_button.clicked.connect(lambda: self.on_txn_list_pag_button_clicked(action='go_next'))
        pass

    def populate_txn_list_table(self, text_filter='', page_number=1):
        txn_list = schema.select_item_sold_data(text_filter=text_filter, page_number=page_number)

        self.view.txn_list_page_label.setText(f"Page {page_number}/{self.model.total_page_number}")

        self.view.txn_list_prev_button.setEnabled(page_number > 1)
        self.view.txn_list_next_button.setEnabled(len(txn_list) == 30)

        self.view.txn_list_table.setRowCount(len(txn_list))

        for txn_list_i, txn_list_v in enumerate(txn_list):
            self.edit_txn_button = MyPushButton(text='Edit')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.edit_txn_button)
            table_act_panel.setLayout(table_act_laoyut)

            user_name = QTableWidgetItem(f"{txn_list_v[0]}")
            cust_name = QTableWidgetItem(f"{txn_list_v[1]}")
            prod_name = QTableWidgetItem(f"{txn_list_v[2]}")
            prod_qty = QTableWidgetItem(f"{txn_list_v[3]}")
            prod_price = QTableWidgetItem(f"{txn_list_v[4]}")
            txn_void = QTableWidgetItem(f"{txn_list_v[5]}")
            txn_reason = QTableWidgetItem(f"{txn_list_v[6]}")
            txn_ref_id = QTableWidgetItem(f"{txn_list_v[7]}")
            datetime_created = QTableWidgetItem(f"{txn_list_v[8]}")

            self.view.txn_list_table.setCellWidget(txn_list_i, 0, table_act_panel)
            self.view.txn_list_table.setItem(txn_list_i, 1, user_name)
            self.view.txn_list_table.setItem(txn_list_i, 2, cust_name)
            self.view.txn_list_table.setItem(txn_list_i, 3, prod_name)
            self.view.txn_list_table.setItem(txn_list_i, 4, prod_qty)
            self.view.txn_list_table.setItem(txn_list_i, 5, prod_price)
            self.view.txn_list_table.setItem(txn_list_i, 6, txn_void)
            self.view.txn_list_table.setItem(txn_list_i, 7, txn_reason)
            self.view.txn_list_table.setItem(txn_list_i, 8, txn_ref_id)
            self.view.txn_list_table.setItem(txn_list_i, 9, datetime_created)


            self.setup_txn_list_table_act_panel_conn(value=txn_list_v)
            pass
        pass
    def setup_txn_list_table_act_panel_conn(self, value):
        self.edit_txn_button.clicked.connect(lambda _, value=value: self.on_edit_txn_button_clicked(value))

    def on_text_filter_button_clicked(self):
        self.model.page_number = 1
        self.view.txn_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

        self.populate_txn_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number) 
        pass
    def on_sync_ui_button_clicked(self):
        self.start_sync_ui()

        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass

    def start_sync_ui(self):
        self.model.init_txn_list_page_entry()
        self.view.txn_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.populate_txn_list_table()
    
    def on_edit_txn_button_clicked(self, value):
        self.model.assign_selected_txn_data_entry(value)
        self.model.setup_manage_txn_panel(window_title=f"Edit {self.model.sel_txn_name_value}")
        self.populate_manage_txn_combo_box_field()

        self.setup_manage_txn_panel_conn(conn_type='edit_txn')

        self.model.manage_txn_dialog.exec()
        pass
    def populate_manage_txn_combo_box_field(self):
        self.model.txn_void_reason_field.addItem('Customer Request')
        self.model.txn_void_reason_field.addItem('Wrong Item')
        self.model.txn_void_reason_field.addItem('Pricing Error')
        self.model.txn_void_reason_field.addItem('Quantity Error')
        self.model.txn_void_reason_field.addItem('Cancelled Order')
        self.model.txn_void_reason_field.addItem('Defective Product')
        self.model.txn_void_reason_field.addItem('Transaction Error')
        self.model.txn_void_reason_field.addItem('Duplicate Transaction')
        self.model.txn_void_reason_field.addItem('Out of Stock')
        self.model.txn_void_reason_field.addItem('Other')
        pass
    def setup_manage_txn_panel_conn(self, conn_type):
        self.model.manage_txn_save_button.clicked.connect(lambda: self.on_manage_txn_save_button_clicked(action=conn_type))
        self.model.manage_txn_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.manage_txn_dialog))
        pass
    def on_manage_txn_save_button_clicked(self, action):
        try:
            void_reason = self.model.txn_void_reason_field.currentText()

            self.model.save_edit_txn_entry()
            self.model.init_selected_txn_data_entry()

            QMessageBox.information(self.view, 'Success', 'TXN has been edited.')
            pass
            self.on_sync_ui_button_clicked()
            pass
        except Exception as e:
            QMessageBox.critical(self.view, 'Error', f"{e}")
            pass
    
    def on_close_button_clicked(self, widget: QWidget):
        widget.close()

        self.model.init_selected_txn_data_entry()
        pass

    def on_txn_list_pag_button_clicked(self, action):
        print('txn_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.page_number > 1:
                self.model.page_number -= 1
                self.view.txn_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_txn_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        elif action == 'go_next':
            self.model.page_number += 1
            self.view.txn_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_txn_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        pass

    pass

class MyTXNWindow(MyGroupBox):
    def __init__(self, name, phone): # NOTE: 'name' param is for the current user (cashier, admin, dev) name
        super().__init__(object_name='MyTXNWindow')

        self.model = MyTXNModel(name=name, phone=phone)
        self.view = MyTXNView(self.model)
        self.controller = MyTXNController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.show()


# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    txn_window = MyTXNWindow(name='test-name')

    txn_window.run()
    app.exec()