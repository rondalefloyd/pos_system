import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from other.csv_importer import *    
from schema.sales_table_schema import *
from schema.product_management_schema_test import *
from widget.product_management_widget_test import *

class ProductManagementLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.product_management_schema = ProductManagementSchema()
        # for temporary use --
        self.sales_table_schema = SalesTableSchema()

        self.sales_table_schema.setup_sales_table()
        # --
        self.createLayout()
        self.refresh_data()

    def refresh_data(self):
        print(str(self.product_management_schema.count_total_product()))
        self.current_page = 1
        self.populate_table()
        pass
    def delete_data(self):
        pass
# under construction...
    def import_data(self):
        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')
        csv_file_name = os.path.basename(csv_file)

        if csv_file:
            df = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(df)

            self.progress_dialog = QProgressDialog(f'Importing Data...', 'Cancel', 0, total_rows, self)
            self.progress_dialog.setWindowTitle('Import Progress')

            self.import_thread = CustomThread(csv_file, self.progress_dialog)
            self.import_thread.progress_signal.connect(self.import_thread.update_progress)
            self.import_thread.finished_signal.connect(self.import_thread.import_finished)
            self.import_thread.error_signal.connect(self.import_thread.import_error)
            self.import_thread.start()
# under construction...

    def add_data(self):
        pass

    def populate_table(self, current_page=1):
        data = self.product_management_schema.list_product(page_number=current_page)

        for index, p_button, page, n_button, row, col in self.tab_content_pagination_button:
            p_button.setEnabled(self.current_page > 1)
            n_button.setEnabled(len(data) == 30)
            
        for index, table, row, col in self.tab_content_table:
            table.setRowCount(len(data))

            for row_index, row_value in enumerate(data):
                action_box = CustomWidget(ref='action_box')
                action_layout = CustomGridLayout(ref='action_layout')
                self.action_button = [
                    (0, CustomPushButton(text='Edit'),0,0),
                    (1, CustomPushButton(text='View'),0,1),
                    (2, CustomPushButton(text='Delete'),0,2)
                ]
                for _, push_button, row, col in self.action_button:
                    action_layout.addWidget(push_button, row, col)
                action_box.setLayout(action_layout)
                
                item_name = [
                    (CustomTableWidgetItem(text=f'{row_value[1]}')),
                    (CustomTableWidgetItem(text=f'{row_value[1]}')),
                    (CustomTableWidgetItem(text=f'{row_value[1]}')),
                    (CustomTableWidgetItem(text=f'{row_value[1]}')),
                    (CustomTableWidgetItem(text=f'{row_value[1]}')),
                ]
                barcode = CustomTableWidgetItem(text=f'{row_value[0]}')
                expire_dt = CustomTableWidgetItem(text=f'{row_value[2]}')
                
                item_type = CustomTableWidgetItem(text=f'{row_value[3]}')
                brand = [
                    (CustomTableWidgetItem(text=f'{row_value[4]}')),
                    (CustomTableWidgetItem(text=f'{row_value[4]}')),
                    (CustomTableWidgetItem(text=f'{row_value[4]}')),
                    (CustomTableWidgetItem(text=f'{row_value[4]}')),
                    (CustomTableWidgetItem(text=f'{row_value[4]}'))
                ]
                sales_group = [
                    CustomTableWidgetItem(text=f'{row_value[5]}'),
                    CustomTableWidgetItem(text=f'{row_value[5]}'),
                    CustomTableWidgetItem(text=f'{row_value[5]}'),
                    CustomTableWidgetItem(text=f'{row_value[5]}'),
                    CustomTableWidgetItem(text=f'{row_value[5]}')
                ]
                supplier = CustomTableWidgetItem(text=f'{row_value[6]}')
                cost = CustomTableWidgetItem(text=f'₱{row_value[7]}')
                sell_price = [
                    CustomTableWidgetItem(text=f'₱{row_value[8]}'),
                    CustomTableWidgetItem(text=f'₱{row_value[8]}'),
                    CustomTableWidgetItem(text=f'₱{row_value[8]}'),
                    CustomTableWidgetItem(text=f'₱{row_value[8]}'),
                    CustomTableWidgetItem(text=f'₱{row_value[8]}')
                ]
                discount_value = CustomTableWidgetItem(text=f'₱{row_value[11]}')
                effective_dt = CustomTableWidgetItem(text=f'{row_value[9]}')
                promo_name = [
                    CustomTableWidgetItem(text=f'{row_value[10]}'),
                    CustomTableWidgetItem(text=f'{row_value[10]}'),
                    CustomTableWidgetItem(text=f'{row_value[10]}'),
                    CustomTableWidgetItem(text=f'{row_value[10]}'),
                    CustomTableWidgetItem(text=f'{row_value[10]}')
                ]

                inventory_tracking = [
                    CustomTableWidgetItem(text=f'{row_value[12]}'),
                    CustomTableWidgetItem(text=f'{row_value[12]}'),
                    CustomTableWidgetItem(text=f'{row_value[12]}'),
                    CustomTableWidgetItem(text=f'{row_value[12]}'),
                    CustomTableWidgetItem(text=f'{row_value[12]}')
                ]
                available = CustomTableWidgetItem(text=f'{row_value[13]}')
                on_hand = CustomTableWidgetItem(text=f'{row_value[14]}')
                update_ts = [
                    CustomTableWidgetItem(text=f'{row_value[15]}'),
                    CustomTableWidgetItem(text=f'{row_value[15]}'),
                    CustomTableWidgetItem(text=f'{row_value[15]}'),
                    CustomTableWidgetItem(text=f'{row_value[15]}'),
                    CustomTableWidgetItem(text=f'{row_value[15]}')
                ]
            
                if index == 0:
                    table.setCellWidget(row_index, 0, action_box)
                    table.setItem(row_index, 1, item_name[0])
                    table.setItem(row_index, 2, brand[0])
                    table.setItem(row_index, 3, sales_group[0])
                    table.setItem(row_index, 4, sell_price[0])
                    table.setItem(row_index, 5, promo_name[0])
                    table.setItem(row_index, 6, inventory_tracking[0])
                    table.setItem(row_index, 7, update_ts[0])
                        
                if index == 1:
                    table.setItem(row_index, 0, barcode)
                    table.setItem(row_index, 1, item_name[1])
                    table.setItem(row_index, 2, expire_dt)
                    table.setItem(row_index, 3, promo_name[1])
                    table.setItem(row_index, 4, update_ts[1])

                if index == 2:
                    table.setItem(row_index, 0, item_name[2])
                    table.setItem(row_index, 1, item_type)
                    table.setItem(row_index, 2, brand[2])
                    table.setItem(row_index, 3, sales_group[2])
                    table.setItem(row_index, 4, supplier)
                    table.setItem(row_index, 5, promo_name[2])
                    table.setItem(row_index, 6, update_ts[2])

                if index == 3:
                    table.setItem(row_index, 0, item_name[3])
                    table.setItem(row_index, 1, cost)
                    table.setItem(row_index, 2, sell_price[3])
                    table.setItem(row_index, 3, discount_value)
                    table.setItem(row_index, 4, effective_dt)
                    table.setItem(row_index, 5, promo_name[3])
                    table.setItem(row_index, 6, update_ts[3])
                
                if index == 4:
                    table.setItem(row_index, 0, item_name[4])
                    table.setItem(row_index, 1, inventory_tracking[4])
                    table.setItem(row_index, 2, available)
                    table.setItem(row_index, 3, on_hand)
                    table.setItem(row_index, 4, promo_name[4])
                    table.setItem(row_index, 5, update_ts[4])
        pass

    def on_push_button_clicked(self, clicked_ref):
        if clicked_ref == 'refresh_button':
            self.refresh_data()
            pass
        if clicked_ref == 'import_button':
            self.import_data()

        elif clicked_ref == 'previous_button':
            if self.current_page > 1:
                self.current_page -= 1
            for index, p_button, page, n_button, row, col in self.tab_content_pagination_button:
                page.setText(f'Page {self.current_page}')
            self.populate_table(self.current_page)

        elif clicked_ref == 'next_button':
            self.current_page += 1
            for index, p_button, page, n_button, row, col in self.tab_content_pagination_button:
                page.setText(f'Page {self.current_page}')
            self.populate_table(self.current_page)
        
        pass

    def call_signal(self, signal_ref):
        if signal_ref == 'panel_a_signal':
            self.manage_data_button[0][1].clicked.connect(lambda: self.on_push_button_clicked('refresh_button'))
            self.manage_data_button[1][1].clicked.connect(lambda: self.on_push_button_clicked('delete_all_button'))
            self.manage_data_button[2][1].clicked.connect(lambda: self.on_push_button_clicked('import_button'))
            self.manage_data_button[3][1].clicked.connect(lambda: self.on_push_button_clicked('add_button'))

            for index, p_button, page, n_button, row, col in self.tab_content_pagination_button:
                p_button.clicked.connect(lambda: self.on_push_button_clicked('previous_button'))
                n_button.clicked.connect(lambda: self.on_push_button_clicked('next_button'))
        if signal_ref == 'panel_b_signal':
            pass
        pass

    def show_panel_b(self):
        self.panel_b = CustomGroupBox(ref='panel_b_box')
        self.panel_b_layout = CustomFormLayout()
 
        self.form_field = [
            (0, CustomLabel(ref='barcode', text='barcode'), (CustomLineEdit(ref='barcode'))),
            (1, CustomLabel(ref='current_barcode', text='current_barcode'), (CustomLineEdit(ref='current_barcode'))), # inactive
            (2, CustomLabel(ref='item_name', text='item_name'), (CustomLineEdit(ref='item_name'))),
            (3, CustomLabel(ref='current_item_name', text='current_item_name'), (CustomLineEdit(ref='current_item_name'))), # inactive
            (4, CustomLabel(ref='expire_dt', text='expire_dt'), (CustomDateEdit(ref='expire_dt'))),

            (5, CustomLabel(ref='current_expire_dt', text='current_expire_dt'), (CustomLineEdit(ref='current_expire_dt'))), # inactive
            (6, CustomLabel(ref='item_type', text='item_type'), (CustomComboBox(ref='item_type'))),
            (7, CustomLabel(ref='current_item_type', text='current_item_type'), (CustomLineEdit(ref='current_item_type'))), # inactive
            (8, CustomLabel(ref='brand', text='brand'), (CustomComboBox(ref='brand'))),
            (9, CustomLabel(ref='current_brand', text='current_brand'), (CustomLineEdit(ref='current_brand'))), # inactive
            (10, CustomLabel(ref='sales_group', text='sales_group'), (CustomComboBox(ref='sales_group'))),
            (11, CustomLabel(ref='current_sales_group', text='current_sales_group'), (CustomLineEdit(ref='current_sales_group'))), # inactive
            (12, CustomLabel(ref='supplier', text='supplier'), (CustomComboBox(ref='supplier'))),
            (13, CustomLabel(ref='current_supplier', text='current_supplier'), (CustomLineEdit(ref='current_supplier'))), # inactive

            (14, CustomLabel(ref='cost', text='cost'), (CustomLineEdit(ref='cost'))),
            (15, CustomLabel(ref='current_cost', text='current_cost'), (CustomLineEdit(ref='current_cost'))), # inactive
            (16, CustomLabel(ref='sell_price', text='sell_price'), (CustomLineEdit(ref='sell_price'))),
            (17, CustomLabel(ref='current_sell_price', text='current_sell_price'), (CustomLineEdit(ref='current_sell_price'))), # inactive
            (18, CustomLabel(ref='effective_dt', text='effective_dt'), (CustomDateEdit(ref='effective_dt'))),
            (19, CustomLabel(ref='current_effective_dt', text='current_effective_dt'), (CustomLineEdit(ref='current_effective_dt'))), # inactive
            (20, CustomLabel(ref='promo_name', text='promo_name'), (CustomComboBox(ref='promo_name'))),
            (21, CustomLabel(ref='current_promo_name', text='current_promo_name'), (CustomLineEdit(ref='current_promo_name'))), # inactive
            (22, CustomLabel(ref='promo_type', text='promo_type'), (CustomLineEdit(ref='promo_type'))),
            (23, CustomLabel(ref='current_promo_type', text='current_promo_type'), (CustomLineEdit(ref='current_promo_type'))), # inactive
            (24, CustomLabel(ref='discount_percent', text='discount_percent'), (CustomLineEdit(ref='discount_percent'))),
            (25, CustomLabel(ref='current_discount_percent', text='current_discount_percent'), (CustomLineEdit(ref='current_discount_percent'))), # inactive
            (26, CustomLabel(ref='discount_value', text='discount_value'), (CustomLineEdit(ref='discount_value'))),
            (27, CustomLabel(ref='current_discount_value', text='current_discount_value'), (CustomLineEdit(ref='current_discount_value'))), # inactive
            (28, CustomLabel(ref='new_sell_price', text='new_sell_price'), (CustomLineEdit(ref='new_sell_price'))),
            (29, CustomLabel(ref='current_new_sell_price', text='current_new_sell_price'), (CustomLineEdit(ref='current_new_sell_price'))), # inactive
            (30, CustomLabel(ref='start_dt', text='start_dt'), (CustomDateEdit(ref='start_dt'))),
            (31, CustomLabel(ref='end_dt', text='end_dt'), (CustomDateEdit(ref='end_dt'))),

            (32, CustomLabel(ref='inventory_tracking', text='inventory_tracking'), (CustomComboBox(ref='inventory_tracking'))),
            (33, CustomLabel(ref='current_inventory_tracking', text='current_inventory_tracking'), (CustomLineEdit(ref='current_inventory_tracking'))), # inactive
            (34, CustomLabel(ref='available_stock', text='available_stock'), (CustomLineEdit(ref='available_stock'))),
            (35, CustomLabel(ref='on_hand_stock', text='on_hand_stock'), (CustomLineEdit(ref='on_hand_stock')))
        ]
        for _, label, field in self.form_field:
            self.panel_b_layout.addRow(label, field)

        self.form_button = [
            (0, CustomPushButton(text='Save New Data')),
            (1, CustomPushButton(text='Save Edit Data')),
            (2, CustomPushButton(text='Back')),
        ]

        for _, button in self.form_button:
            self.panel_b_layout.addRow(button)

        self.call_signal(signal_ref='panel_b_signal')

        pass
    def show_panel_a(self):
        self.panel_a = CustomGroupBox(ref='panel_a_box')
        self.panel_a_layout = CustomGridLayout()

        self.filter_field = CustomLineEdit()
        self.tab_sort = CustomTabWidget()
        # can be changed from here ...
        self.manage_data_box = CustomWidget()
        self.manage_data_box_layout = CustomGridLayout(ref='manage_data_layout')

        self.manage_data_button = [
            (0, CustomPushButton(text='Refresh'),0,0),
            (1, CustomPushButton(text='Delete All'),0,1),
            (2, CustomPushButton(text='Import'),0,2),
            (3, CustomPushButton(text='Add'),0,3)            
        ]
        for index, push_button, row, col in self.manage_data_button:
            self.manage_data_box_layout.addWidget(push_button, row, col)

        self.manage_data_box.setLayout(self.manage_data_box_layout)

        self.tab_sort.setCornerWidget(self.manage_data_box, Qt.Corner.BottomRightCorner)
        # under construction
        self.tab_content_box = [
            (0, CustomWidget(ref='overview_box'), 'Overview'),
            (1, CustomWidget(ref='primary_box'), 'Primary'),
            (2, CustomWidget(ref='category_box'), 'Category'),
            (3, CustomWidget(ref='price_box'), 'Price'),
            (4, CustomWidget(ref='inventory_box'), 'Inventory')
        ]
        
        self.tab_content_layout = [
            (0, CustomGridLayout(ref='overview_layout')),
            (1, CustomGridLayout(ref='primary_layout')),
            (2, CustomGridLayout(ref='category_layout')),
            (3, CustomGridLayout(ref='price_layout')),
            (4, CustomGridLayout(ref='inventory_layout'))
        ]
        
        self.tab_content_table = [
            (0, CustomTableWidget(ref='overview_table'), 0, 0),
            (1, CustomTableWidget(ref='primary_table'), 0, 0),
            (2, CustomTableWidget(ref='category_table'), 0, 0),
            (3, CustomTableWidget(ref='price_table'), 0, 0),
            (4, CustomTableWidget(ref='inventory_table'), 0, 0)
        ]

        self.tab_content_pagination_button = [
            (0, CustomPushButton(ref='overview_previous_button', text='Previous'), CustomLabel(text=f'Page 1'), CustomPushButton(ref='overview_next_button', text='Next'), 0, 0),
            (1, CustomPushButton(ref='primary_previous_button', text='Previous'), CustomLabel(text=f'Page 1'), CustomPushButton(ref='primary_next_button', text='Next'), 0, 0),
            (2, CustomPushButton(ref='category_previous_button', text='Previous'), CustomLabel(text=f'Page 1'), CustomPushButton(ref='category_next_button', text='Next'), 0, 0),
            (3, CustomPushButton(ref='price_previous_button', text='Previous'), CustomLabel(text=f'Page 1'), CustomPushButton(ref='price_next_button', text='Next'), 0, 0),
            (4, CustomPushButton(ref='inventory_previous_button', text='Previous'), CustomLabel(text=f'Page 1'), CustomPushButton(ref='inventory_next_button', text='Next'), 0, 0)
        ]

        for index, table, row, col in self.tab_content_table:
            self.tab_content_layout[index][1].addWidget(table, 0, 0, 1, 3)
            for index, p_button, page, n_button, row, col in self.tab_content_pagination_button:
                self.tab_content_layout[index][1].addWidget(p_button, 1, 0)
                self.tab_content_layout[index][1].addWidget(page, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.tab_content_layout[index][1].addWidget(n_button, 1, 2)
                for index, layout in self.tab_content_layout:
                    self.tab_content_box[index][1].setLayout(layout)
                    for index, box, name in self.tab_content_box:
                        self.tab_sort.addTab(box, name)

        self.call_signal(signal_ref='panel_a_signal')

            
        # until here ...
        
        self.panel_a_layout.addWidget(self.filter_field)
        self.panel_a_layout.addWidget(self.tab_sort)
        self.panel_a.setLayout(self.panel_a_layout)
        pass

    def createLayout(self):
        # ---- self.setWindowState(Qt.WindowState.WindowMaximized)

        grid_layout = CustomGridLayout()

        self.show_panel_a()
        self.show_panel_b()

        grid_layout.addWidget(self.panel_a,0,0)
        grid_layout.addWidget(self.panel_b,0,1)

        self.setLayout(grid_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagementLayout()
    window.show()
    sys.exit(pos_app.exec())
