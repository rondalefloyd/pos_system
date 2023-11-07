
import sys, os
import pythoncom
import win32com.client
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from src.gui.widget.my_widget import *
from src.core.csv_to_db_importer import MyDataImportThread
from src.core.sql.cashier.transaction import MyTXNSchema
from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()
schema = MyTXNSchema()

class MyTransactionModel:
    def __init__(self, name, password, phone):
        self.user_name = name
        self.password = password
        self.user_phone = phone

        self.total_page_number = schema.select_item_sold_data_total_page_count()
        self.page_number = 1 if self.total_page_number > 0 else 0

        self.sel_item_sold_id = 0
        self.sel_product_price_id = 0
        self.sel_customer_id = 0
        self.sel_user_id = 0
        self.sel_stock_id = 0

        self.sel_product_qty = 0
class MyTransactionView(MyWidget):
    def __init__(self, model: MyTransactionModel):
        super().__init__()

        self.m = model

        self.set_item_sold_box()

    def set_item_sold_box(self):
        self.filter_field = MyLineEdit(object_name='filter_field')
        self.filter_button = MyPushButton(object_name='filter_button', text='Filter')
        self.filter_box = MyGroupBox(object_name='filter_box')
        self.filter_layout = MyHBoxLayout(object_name='filter_layout')
        self.filter_layout.addWidget(self.filter_field)
        self.filter_layout.addWidget(self.filter_button)
        self.filter_box.setLayout(self.filter_layout)

        self.reprint_button = MyPushButton(object_name='reprint_button', text='Reprint')

        self.item_sold_act_box = MyGroupBox(object_name='item_sold_act_box')
        self.item_sold_act_layout = MyHBoxLayout(object_name='item_sold_act_layout')
        self.item_sold_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.item_sold_act_layout.addWidget(self.reprint_button,0,Qt.AlignmentFlag.AlignRight)
        self.item_sold_act_box.setLayout(self.item_sold_act_layout)

        self.item_sold_overview_table = MyTableWidget(object_name='item_sold_overview_table')
        self.item_sold_overview_prev_button = MyPushButton(object_name='overview_prev_button', text='Prev')
        self.item_sold_overview_page_label = MyLabel(object_name='overview_page_label', text=f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.item_sold_overview_next_button = MyPushButton(object_name='overview_next_button', text='Next')
        self.item_sold_overview_act_box = MyGroupBox(object_name='overview_act_box')
        self.item_sold_overview_act_layout = MyHBoxLayout(object_name='overview_act_layout')
        self.item_sold_overview_act_layout.addWidget(self.item_sold_overview_prev_button)
        self.item_sold_overview_act_layout.addWidget(self.item_sold_overview_page_label)
        self.item_sold_overview_act_layout.addWidget(self.item_sold_overview_next_button)
        self.item_sold_overview_act_box.setLayout(self.item_sold_overview_act_layout)
        self.item_sold_overview_box = MyGroupBox(object_name='item_sold_overview_box')
        self.item_sold_overview_layout = MyVBoxLayout(object_name='item_sold_overview_layout')
        self.item_sold_overview_layout.addWidget(self.item_sold_overview_table)
        self.item_sold_overview_layout.addWidget(self.item_sold_overview_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.item_sold_overview_box.setLayout(self.item_sold_overview_layout)
        
        self.item_sold_sort_tab = MyTabWidget()
        self.item_sold_sort_tab.addTab(self.item_sold_overview_box, 'Overview')

        self.main_layout = MyVBoxLayout()
        self.main_layout.addWidget(self.item_sold_act_box)
        self.main_layout.addWidget(self.item_sold_sort_tab)
        self.setLayout(self.main_layout)

    def set_manage_data_box(self):
        self.reason_label = MyLabel(text='Reason')
        self.reason_field = MyComboBox(object_name='reason_field')
        self.other_reason_field = MyPlainTextEdit(object_name='other_reason_field')
        self.field_box = MyGroupBox(object_name='field_box')
        self.field_layout = MyFormLayout(object_name='field_layout')
        self.field_layout.addRow(self.reason_label)
        self.field_layout.addRow(self.reason_field)
        self.field_layout.addRow(self.other_reason_field)
        self.field_box.setLayout(self.field_layout)

        self.save_data_button = MyPushButton(object_name='save_button', text='Save')
        self.manage_data_act_close_button = MyPushButton(object_name='close_button', text='Close')
        self.manage_data_act_box = MyGroupBox(object_name='manage_data_act_box')
        self.manage_data_act_layout = MyHBoxLayout(object_name='manage_data_act_layout')
        self.manage_data_act_layout.addWidget(self.save_data_button,1,Qt.AlignmentFlag.AlignRight)
        self.manage_data_act_layout.addWidget(self.manage_data_act_close_button)
        self.manage_data_act_box.setLayout(self.manage_data_act_layout)
        
        self.manage_data_dialog = MyDialog(object_name='manage_data_dialog')
        self.manage_data_layout = MyVBoxLayout(object_name='manage_data_layout')
        self.manage_data_layout.addWidget(self.field_box,0,Qt.AlignmentFlag.AlignTop)
        self.manage_data_layout.addWidget(self.manage_data_act_box)
        self.manage_data_dialog.setLayout(self.manage_data_layout)

    def set_overview_table_act_box(self):
        self.void_data_button = MyPushButton(object_name='void_data_button', text='Void')
        self.item_sold_overview_data_act_box = MyGroupBox(object_name='item_sold_overview_data_act_box')
        self.item_sold_overview_data_act_layout = MyHBoxLayout(object_name='item_sold_overview_data_act_layout')
        self.item_sold_overview_data_act_layout.addWidget(self.void_data_button)
        self.item_sold_overview_data_act_box.setLayout(self.item_sold_overview_data_act_layout)
class MyTransactionController:
    def __init__(self, model: MyTransactionModel, view: MyTransactionView):
        self.v = view
        self.m = model

        self.set_item_sold_box_conn()
        self.sync_ui()

    def set_item_sold_box_conn(self):
        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)
        self.v.reprint_button.clicked.connect(self.on_reprint_button_clicked)
        self.v.item_sold_overview_prev_button.clicked.connect(self.on_overview_prev_button_clicked)
        self.v.item_sold_overview_next_button.clicked.connect(self.on_overview_next_button_clicked)
        pass
    def on_filter_button_clicked(self): # IDEA: src
        text_filter = self.v.filter_field.text()
        
        self.m.total_page_number = schema.select_item_sold_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0

        print(self.m.total_page_number, self.m.page_number)

        self.v.item_sold_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")

        self.populate_overview_table(text=text_filter, page_number=1)
        pass
    
    def on_reprint_button_clicked(self):
        pythoncom.CoInitialize()
        receipt_file, _ = QFileDialog.getOpenFileName(self.v, 'Open receipt', r'G:/My Drive/receipt/saved', 'DOCX File (*docx)') #FIXME
        filename = os.path.basename(receipt_file)
        print('filename:', filename)
        docx_file = os.path.abspath(f"G:/My Drive/receipt/saved/{filename}")
        print('2filename:', docx_file)

        print(receipt_file)
        if receipt_file:
            word = win32com.client.Dispatch('Word.Application')
            self.doc = word.Documents.Open(docx_file)
            self.doc.PrintOut()
            word.Quit()

            QMessageBox.information(self.v, 'Success', 'Receipt printed.')
        else:
            pass
        pythoncom.CoInitialize()

    def populate_overview_table(self, text='', page_number=1): # IDEA: src
        self.v.item_sold_overview_prev_button.setEnabled(page_number > 1)
        self.v.item_sold_overview_next_button.setEnabled(page_number < self.m.total_page_number)
        self.v.item_sold_overview_page_label.setText(f"Page {page_number}/{self.m.total_page_number}")

        item_sold_data = schema.select_item_sold_data_as_display(text=text, page_number=page_number)

        self.v.item_sold_overview_table.setRowCount(len(item_sold_data))

        for i, data in enumerate(item_sold_data):
            self.v.set_overview_table_act_box()
            user_name = MyTableWidgetItem(text=f"{data[0]}")
            customer_name = MyTableWidgetItem(text=f"{data[1]}")
            item_name = MyTableWidgetItem(text=f"{data[2]}")
            quantity = MyTableWidgetItem(text=f"{data[3]}")
            total_amount = MyTableWidgetItem(text=f"{data[4]}", format='bill')
            void = MyTableWidgetItem(text=f"{data[5]}")
            reason = MyTableWidgetItem(text=f"{data[6]}")
            reference_number = MyTableWidgetItem(text=f"{data[7]}")
            datetime_created = MyTableWidgetItem(text=f"{data[8]}")

            # self.v.void_data_button.hide() if data[5] > 0 else None

            self.v.item_sold_overview_table.setCellWidget(i, 0, self.v.item_sold_overview_data_act_box)
            self.v.item_sold_overview_table.setItem(i, 1, user_name)
            self.v.item_sold_overview_table.setItem(i, 2, customer_name)
            self.v.item_sold_overview_table.setItem(i, 3, item_name)
            self.v.item_sold_overview_table.setItem(i, 4, quantity)
            self.v.item_sold_overview_table.setItem(i, 5, total_amount)
            self.v.item_sold_overview_table.setItem(i, 6, void)
            self.v.item_sold_overview_table.setItem(i, 7, reason)
            self.v.item_sold_overview_table.setItem(i, 8, reference_number)
            self.v.item_sold_overview_table.setItem(i, 9, datetime_created)

            self.v.void_data_button.clicked.connect(lambda _, data=data: self.on_void_data_button_clicked(data))
        pass

    def on_overview_prev_button_clicked(self):
        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.item_sold_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(page_number=self.m.page_number)
        pass
    def on_overview_next_button_clicked(self):
        if self.m.page_number < self.m.total_page_number:
            self.m.page_number += 1

            self.v.item_sold_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(page_number=self.m.page_number)
        pass

    # IDEA: if the widget uses the same connection
    def on_void_data_button_clicked(self, data):
        self.v.set_manage_data_box()
        self.load_combo_box_data()

        self.v.manage_data_dialog.setWindowTitle(f"{data[2]}")

        print('b4 data[13]:', data[13])

        self.m.sel_item_sold_id = data[9]
        self.m.sel_product_price_id = data[10]
        self.m.sel_customer_id = data[11]
        self.m.sel_user_id = data[12]
        self.m.sel_stock_id = 0 if data[13] is None else data[13]
        self.m.sel_product_qty = data[3]

        self.set_manage_data_box_conn()

        self.v.manage_data_dialog.exec()
        pass

    def set_manage_data_box_conn(self):
        self.v.reason_field.currentTextChanged.connect(self.on_reason_field_current_text_changed)
        self.v.save_data_button.clicked.connect(self.on_save_data_button_clicked)
        self.v.manage_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.manage_data_dialog))
        pass
    def on_reason_field_current_text_changed(self):
        print('changed')
        if self.v.reason_field.currentText() == 'Other (specify the reason)':
            self.v.other_reason_field.show() 
        else: 
            self.v.other_reason_field.hide()

    def load_combo_box_data(self):
        self.v.set_manage_data_box()

        self.v.reason_field.addItem('Customer Return') # -- this options updates the stock
        self.v.reason_field.addItem('Damaged Item')
        self.v.reason_field.addItem('Wrong Item')
        self.v.reason_field.addItem('Price Discrepancy')
        self.v.reason_field.addItem('Overcharge')
        self.v.reason_field.addItem('Cancelled Order')
        self.v.reason_field.addItem('Double Charged')
        self.v.reason_field.addItem('Payment Issue')
        self.v.reason_field.addItem('No Receipt')
        self.v.reason_field.addItem('Store Policy')
        self.v.reason_field.addItem('Expired Product')
        self.v.reason_field.addItem('Tested transaction')
        self.v.reason_field.addItem('Other (specify the reason)')
 
    def on_save_data_button_clicked(self):
        confirm = QMessageBox.warning(self.v.manage_data_dialog, 'Confirm', 'Are you sure you want to void this transaction?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            if self.v.reason_field.currentText() != 'Other (specify the reason)':
                reason = self.v.reason_field.currentText()
            else:
                reason = self.v.other_reason_field.toPlainText()

            schema.update_selected_item_sold_void(
                item_sold_id=self.m.sel_item_sold_id,
                product_price_id=self.m.sel_product_price_id,
                customer_id=self.m.sel_customer_id,
                user_id=self.m.sel_user_id,
                stock_id=self.m.sel_stock_id, 
                reason=reason,
                product_qty=self.m.sel_product_qty
            )

            self.sync_ui()
            self.v.manage_data_dialog.close()
            QMessageBox.information(self.v, 'Success', 'Transaction voided.')
            pass
        else:
            pass

    def sync_ui(self):
        text_filter = self.v.filter_field.text()
        self.m.total_page_number = schema.select_item_sold_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0
        self.populate_overview_table(text=text_filter, page_number=self.m.page_number)
        pass
    def close_dialog(self, dialog: QDialog):
        dialog.close()

class MyTXNWindow(MyGroupBox):
    def __init__(self, name='test', password='test', phone='test'):

        self.model = MyTransactionModel(name, password, phone)
        self.view = MyTransactionView(self.model)
        self.controller = MyTransactionController(self.model, self.view)

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
    item_sold_window = MyTXNWindow()

    item_sold_window.run()

    app.exec()