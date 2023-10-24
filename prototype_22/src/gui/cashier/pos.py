
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

        self.total_page_number = product_schema.select_product_data_total_page_count()
        self.page_number = 1 if self.total_page_number > 0 else 0

        self.sel_pos_id = 0

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

        self.import_data_button = MyPushButton(text='Import')
        self.add_product_button = MyPushButton(text='Add')
        self.manage_data_box = MyGroupBox()
        self.field_layout = MyHBoxLayout()
        self.field_layout.addWidget(self.import_data_button)
        self.field_layout.addWidget(self.add_product_button)
        self.manage_data_box.setLayout(self.field_layout)

        self.pos_act_box = MyGroupBox()
        self.pos_act_layout = MyHBoxLayout()
        self.pos_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.pos_act_layout.addWidget(self.manage_data_box,1,Qt.AlignmentFlag.AlignRight)
        self.pos_act_box.setLayout(self.pos_act_layout)

        self.pos_overview_table = MyTableWidget(object_name='pos_overview_table')
        self.pos_overview_prev_button = MyPushButton(text='Prev')
        self.pos_overview_page_label = MyLabel(text=f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.pos_overview_next_button = MyPushButton(text='Next')
        self.pos_overview_act_box = MyGroupBox()
        self.pos_overview_act_layout = MyHBoxLayout()
        self.pos_overview_act_layout.addWidget(self.pos_overview_prev_button)
        self.pos_overview_act_layout.addWidget(self.pos_overview_page_label)
        self.pos_overview_act_layout.addWidget(self.pos_overview_next_button)
        self.pos_overview_act_box.setLayout(self.pos_overview_act_layout)
        self.pos_overview_box = MyGroupBox()
        self.pos_overview_layout = MyVBoxLayout()
        self.pos_overview_layout.addWidget(self.pos_overview_table)
        self.pos_overview_layout.addWidget(self.pos_overview_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.pos_overview_box.setLayout(self.pos_overview_layout)
        
        self.pos_sort_tab = MyTabWidget()
        self.pos_sort_tab.addTab(self.pos_overview_box, 'Overview')

        self.main_layout = MyVBoxLayout()
        self.main_layout.addWidget(self.pos_act_box)
        self.main_layout.addWidget(self.pos_sort_tab)
        self.setLayout(self.main_layout)

    def set_manage_data_box(self):
        self.pos_name_field = MyLineEdit(object_name='pos_name_field')
        self.pos_name_label = MyLabel(text='Name')
        self.pos_type_field = MyComboBox(object_name='pos_type_field')
        self.pos_type_label = MyLabel(text='Type')
        self.pos_percent_field = MyLineEdit(object_name='pos_percent_field')
        self.pos_percent_label = MyLabel(text='Percent')
        self.pos_desc_field = MyPlainTextEdit(object_name='pos_desc_field')
        self.pos_desc_label = MyLabel(text='Description')
        self.field_box = MyGroupBox()
        self.field_layout = MyFormLayout()
        self.field_layout.addRow(self.pos_name_label)
        self.field_layout.addRow(self.pos_name_field)
        self.field_layout.addRow(self.pos_type_label)
        self.field_layout.addRow(self.pos_type_field)
        self.field_layout.addRow(self.pos_percent_label)
        self.field_layout.addRow(self.pos_percent_field)
        self.field_layout.addRow(self.pos_desc_label)
        self.field_layout.addRow(self.pos_desc_field)
        self.field_box.setLayout(self.field_layout)
        self.manage_data_scra = MyScrollArea()
        self.manage_data_scra.setWidget(self.field_box)

        self.save_data_button = MyPushButton(text='Save')
        self.manage_data_act_close_button = MyPushButton(text='Close')
        self.manage_data_act_box = MyGroupBox()
        self.manage_data_act_layout = MyHBoxLayout()
        self.manage_data_act_layout.addWidget(self.save_data_button,1,Qt.AlignmentFlag.AlignRight)
        self.manage_data_act_layout.addWidget(self.manage_data_act_close_button)
        self.manage_data_act_box.setLayout(self.manage_data_act_layout)
        
        self.manage_data_dialog = MyDialog()
        self.manage_data_layout = MyVBoxLayout()
        self.manage_data_layout.addWidget(self.manage_data_scra)
        self.manage_data_layout.addWidget(self.manage_data_act_box)
        self.manage_data_dialog.setLayout(self.manage_data_layout)

    def set_progress_dialog(self):
        self.progress_bar = MyProgressBar()
        self.progress_label = MyLabel(text='Please wait...')
        self.progress_dialog = MyDialog(window_title='99% complete')
        self.progress_layout = MyVBoxLayout()
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_dialog.setLayout(self.progress_layout)
        pass

    def set_overview_table_act_box(self, data):
        self.add_product_button = MyPushButton(text='Add')
        self.view_data_button = MyPushButton(text='View')

        # self.product_barcode_label = MyLabel(text=f"{data[0]}")
        # self.product_name_label = MyLabel(text=f"{data[1]}")
        # self.product_brand_dt_label = MyLabel(text=f"{data[2]}")
        # self.product_sales_group_dt_label = MyLabel(text=f"{data[3]}")
        # self.product_price_label = MyLabel(text=f"{data[4]}")
        # self.product_effective_dt_label = MyLabel(text=f"{data[5]}")
        # self.product_onhand_label = MyLabel(text=f"{data[6]}")
        # self.product_info_box = MyGroupBox()
        # self.product_info_layout = MyFormLayout()
        # self.product_info_layout.addRow(self.product_barcode_label)
        # self.product_info_layout.addRow(self.product_name_label)
        # self.product_info_layout.addRow(self.product_brand_dt_label)
        # self.product_info_layout.addRow(self.product_sales_group_dt_label)
        # self.product_info_layout.addRow(self.product_price_label)
        # self.product_info_layout.addRow(self.product_effective_dt_label)
        # self.product_info_layout.addRow(self.product_onhand_label)
        # self.product_info_box.setLayout(self.product_info_layout)

        self.pos_overview_act_box = MyGroupBox(object_name='pos_overview_act_box')
        self.pos_overview_act_layout = MyGridLayout(object_name='pos_overview_act_layout')
        self.pos_overview_act_layout.addWidget(self.add_product_button,0,0)
        self.pos_overview_act_layout.addWidget(self.view_data_button,1,0)
        # self.pos_overview_act_layout.addWidget(self.product_info_box,0,1,2,1)
        self.pos_overview_act_box.setLayout(self.pos_overview_act_layout)

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
    pass
class MyPOSController:
    def __init__(self, model: MyPOSModel, view: MyPOSView):
        self.v = view
        self.m = model

        self.set_pos_box_conn()
        self.sync_ui()

    def set_pos_box_conn(self):
        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)
        
        self.v.add_product_button.clicked.connect(self.on_add_product_button_clicked)
        self.v.pos_overview_prev_button.clicked.connect(self.on_overview_prev_button_clicked)
        self.v.pos_overview_next_button.clicked.connect(self.on_overview_next_button_clicked)
        pass
    def on_filter_button_clicked(self): # IDEA: src
        text_filter = self.v.filter_field.text()
        
        self.populate_overview_table(text=text_filter, page_number=1)
        pass
    
    def on_add_product_button_clicked(self): # IDEA: src
        pass

    def populate_overview_table(self, text='', page_number=1): # IDEA: src
        self.v.pos_overview_prev_button.setEnabled(page_number > 1)
        self.v.pos_overview_next_button.setEnabled(page_number < self.m.total_page_number)
        self.v.pos_overview_page_label.setText(f"Page {page_number}/{self.m.total_page_number}")

        pos_data = product_schema.select_product_data_as_display(text=text, page_number=page_number)

        self.v.pos_overview_table.setRowCount(len(pos_data))

        for i, data in enumerate(pos_data):
            self.v.set_overview_table_act_box(pos_data)

            self.v.pos_overview_table.setCellWidget(i, 0, self.v.pos_overview_act_box)

            self.v.add_product_button.clicked.connect(lambda _, data=data: self.on_edit_data_button_clicked(data))
            self.v.view_data_button.clicked.connect(lambda _, data=data: self.on_view_data_button_clicked(data))
        pass
    def on_view_data_button_clicked(self, data):
        self.v.set_view_dialog()
        self.v.view_data_dialog.setWindowTitle(f"{data[0]}")

        self.v.pos_name_info.setText(str(data[0]))
        self.v.pos_type_info.setText(str(data[1]))
        self.v.pos_percent_info.setText(str(data[2]))
        self.v.pos_desc_info.setText(str(data[3]))
        self.v.datetime_created_info.setText(str(data[4]))

        self.set_view_data_box_conn()
        self.v.view_data_dialog.exec()
        pass
    def set_view_data_box_conn(self):
        self.v.view_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.view_data_dialog))

    def on_overview_prev_button_clicked(self):
        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.pos_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(page_number=self.m.page_number)
        pass
    def on_overview_next_button_clicked(self):
        if self.m.page_number < self.m.total_page_number:
            self.m.page_number += 1

            self.v.pos_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(page_number=self.m.page_number)
        pass

    # IDEA: if the widget uses the same connection
    def load_combo_box_data(self):
        pass

    def sync_ui(self):
        self.m.total_page_number = product_schema.select_product_data_total_page_count()
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0
        self.populate_overview_table(page_number=self.m.page_number)
        pass
    
    def close_dialog(self, dialog: QDialog):
        dialog.close()

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