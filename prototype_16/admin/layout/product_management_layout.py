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
from schema.product_management_schema import *
from widget.product_management_widget import *

class ProductManagementLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.product_management_schema = ProductManagementSchema()
        # for temporary use --
        self.sales_table_schema = SalesTableSchema()

        self.sales_table_schema.setup_sales_table()
        # --

        # default values
        self.current_page = 1

        self.createLayout()
        self.refresh_data()

    def refresh_data(self):
        self.current_page = 1
        self.populate_table()
        pass
    def delete_data(self):
        pass
# under construction...
    def import_data(self):
        self.import_button.setDisabled(True)

        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')

        if csv_file:
            data_frame = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)

            self.progress_dialog = CustomProgressDialog(ref='import_progress_dialog', parent=self, min=0, max=total_rows)

            self.import_thread = CustomThread(csv_file, self.progress_dialog, self.import_button)
            self.import_thread.progress_signal.connect(self.import_thread.update_progress)
            self.import_thread.finished_signal.connect(self.import_thread.import_finished)
            
            self.import_thread.error_signal.connect(self.import_thread.import_error)
            self.import_thread.start()
        else:
            self.import_button.setDisabled(False)

        pass
# under construction...

    def add_data(self):
        barcode = self.form_field[0][2].text()
        item_name = self.form_field[2][2].text()
        expire_dt = self.form_field[4][2].date()

        item_type = self.form_field[6][2].currentText()
        brand = self.form_field[8][2].currentText()
        sales_group = self.form_field[10][2].currentText()
        supplier = self.form_field[12][2].currentText()

        cost = self.form_field[14][2].text()
        sell_price = self.form_field[16][2].text()
        effective_dt = self.form_field[18][2].date()
        promo_name = self.form_field[20][2].currentText()
        promo_type = self.form_field[22][2].text()
        discount_percent = self.form_field[24][2].text()
        discount_value = self.form_field[26][2].text()
        new_sell_price = self.form_field[28][2].text()
        start_dt = self.form_field[30][2].date()
        end_dt = self.form_field[31][2].date()

        inventory_tracking = self.form_field[32][2].currentText()
        available_stock = self.form_field[34][2].text()
        on_hand_stock = self.form_field[35][2].text()

        
        pass

    def populate_table(self, current_page=1):
        data = self.product_management_schema.list_product(page_number=current_page)

        for _, p_button, _, n_button, _, _ in self.tab_content_pagination_button:
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
            self.current_page = 1
            for index, p_button, page, n_button, row, col in self.tab_content_pagination_button:
                page.setText(f'Page {self.current_page}')
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
            # manage_data_box buttons
            self.refresh_button = self.manage_data_button[0][1]
            self.delete_all_button = self.manage_data_button[1][1]
            self.import_button = self.manage_data_button[2][1]
            self.add_button = self.manage_data_button[3][1]

            self.refresh_button.clicked.connect(lambda: self.on_push_button_clicked('refresh_button'))
            self.delete_all_button.clicked.connect(lambda: self.on_push_button_clicked('delete_all_button'))
            self.import_button.clicked.connect(lambda: self.on_push_button_clicked('import_button'))
            self.add_button.clicked.connect(lambda: self.on_push_button_clicked('add_button'))

            # tab_content_pagination buttons
            for _, p_button, _, n_button, _, _ in self.tab_content_pagination_button:
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
            (2, CustomLabel(ref='item_name', text='item_name'), (CustomLineEdit(ref='item_name'))),
            (4, CustomLabel(ref='expire_dt', text='expire_dt'), (CustomDateEdit(ref='expire_dt'))),
            (6, CustomLabel(ref='item_type', text='item_type'), (CustomComboBox(ref='item_type'))),
            (8, CustomLabel(ref='brand', text='brand'), (CustomComboBox(ref='brand'))),
            (10, CustomLabel(ref='sales_group', text='sales_group'), (CustomComboBox(ref='sales_group'))),
            (12, CustomLabel(ref='supplier', text='supplier'), (CustomComboBox(ref='supplier'))),

            (14, CustomLabel(ref='cost', text='cost'), (CustomLineEdit(ref='cost'))),
            (16, CustomLabel(ref='sell_price', text='sell_price'), (CustomLineEdit(ref='sell_price'))),
            (18, CustomLabel(ref='effective_dt', text='effective_dt'), (CustomDateEdit(ref='effective_dt'))),
            (20, CustomLabel(ref='promo_name', text='promo_name'), (CustomComboBox(ref='promo_name'))),
            (22, CustomLabel(ref='promo_type', text='promo_type'), (CustomLineEdit(ref='promo_type'))),
            (24, CustomLabel(ref='discount_percent', text='discount_percent'), (CustomLineEdit(ref='discount_percent'))),
            (26, CustomLabel(ref='discount_value', text='discount_value'), (CustomLineEdit(ref='discount_value'))),
            (28, CustomLabel(ref='new_sell_price', text='new_sell_price'), (CustomLineEdit(ref='new_sell_price'))),
            (30, CustomLabel(ref='start_dt', text='start_dt'), (CustomDateEdit(ref='start_dt'))),
            (31, CustomLabel(ref='end_dt', text='end_dt'), (CustomDateEdit(ref='end_dt'))),

            (32, CustomLabel(ref='inventory_tracking', text='inventory_tracking'), (CustomComboBox(ref='inventory_tracking'))),
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

        self.panel_b.setLayout(self.panel_b_layout)
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
            (0, CustomPushButton(ref='refresh_button'),0,0),
            (1, CustomPushButton(ref='delete_all_button'),0,1),
            (2, CustomPushButton(ref='import_button'),0,2),
            (3, CustomPushButton(ref='add_button'),0,3)            
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
            (0, CustomPushButton(ref='overview_previous_button', text='Previous'), CustomLabel(text=f'Page {self.current_page}'), CustomPushButton(ref='overview_next_button', text='Next'), 0, 0),
            (1, CustomPushButton(ref='primary_previous_button', text='Previous'), CustomLabel(text=f'Page {self.current_page}'), CustomPushButton(ref='primary_next_button', text='Next'), 0, 0),
            (2, CustomPushButton(ref='category_previous_button', text='Previous'), CustomLabel(text=f'Page {self.current_page}'), CustomPushButton(ref='category_next_button', text='Next'), 0, 0),
            (3, CustomPushButton(ref='price_previous_button', text='Previous'), CustomLabel(text=f'Page {self.current_page}'), CustomPushButton(ref='price_next_button', text='Next'), 0, 0),
            (4, CustomPushButton(ref='inventory_previous_button', text='Previous'), CustomLabel(text=f'Page {self.current_page}'), CustomPushButton(ref='inventory_next_button', text='Next'), 0, 0)
        ]

        for index_a, table, _, _ in self.tab_content_table:
            self.tab_content_layout[index_a][1].addWidget(table, 0, 0, 1, 3)
            for index_b, p_button, page, n_button, _, _ in self.tab_content_pagination_button:
                self.tab_content_layout[index_b][1].addWidget(p_button, 1, 0)
                self.tab_content_layout[index_b][1].addWidget(page, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.tab_content_layout[index_b][1].addWidget(n_button, 1, 2)
                for index_c, layout in self.tab_content_layout:
                    self.tab_content_box[index_c][1].setLayout(layout)
                    for _, box, name in self.tab_content_box:
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
