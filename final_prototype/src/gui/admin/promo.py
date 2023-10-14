import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
from typing import List
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))


from src.core.manual_csv_importer import *
from src.sql.admin.promo import *
from src.widget.admin.promo import *

class MyPromoModel:
    def __init__(self):
        self.csv_path = 'G:' + f"/My Drive/csv/"

        self.promo_data_count_value = 0
        self.promo_data_total_value = 0
        self.promo_data_remaining_value = 0
        pass

class MyPromoView(MyWidget):
    def __init__(self, model: MyPromoModel):
        super().__init__(object_name='my_sales_view')

        self.model = model

        self.set_main_layout()

    def set_main_layout(self):
        self.set_panel_a_box()
        self.set_panel_b_box()

        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.panel_a_box)
        self.main_layout.addWidget(self.panel_b_box)
        self.setLayout(self.main_layout)
        pass

    def set_panel_a_box(self):
        self.panel_a_box = MyGroupBox()
        self.panel_a_layout = MyGridLayout()
        
        self.text_filter_field = MyLineEdit()
        self.text_filter_button = MyPushButton(text='Filter')
        self.text_filter_box = MyGroupBox()
        self.text_filter_layout = MyHBoxLayout()
        self.text_filter_layout.addWidget(self.text_filter_field)
        self.text_filter_layout.addWidget(self.text_filter_button)
        self.text_filter_box.setLayout(self.text_filter_layout)

        self.import_promo_button = MyPushButton(text='Import')
        self.add_promo_button = MyPushButton(text='Add')
        self.add_promo_box = MyGroupBox()
        self.add_promo_layout = MyHBoxLayout()
        self.add_promo_layout.addWidget(self.import_promo_button)
        self.add_promo_layout.addWidget(self.add_promo_button)
        self.add_promo_box.setLayout(self.add_promo_layout)

        self.promo_list_table = MyTableWidget(object_name='promo_list_table')
        self.promo_list_pag_prev_button = MyPushButton(text='Prev')
        self.promo_list_pag_page_label = MyLabel(text='Page 99/99')
        self.promo_list_pag_next_button = MyPushButton(text='Next')
        self.promo_list_pag_act_box = MyGroupBox()
        self.promo_list_pag_act_layout = MyHBoxLayout(object_name='promo_list_pag_act_layout')
        self.promo_list_pag_act_layout.addWidget(self.promo_list_pag_prev_button)
        self.promo_list_pag_act_layout.addWidget(self.promo_list_pag_page_label)
        self.promo_list_pag_act_layout.addWidget(self.promo_list_pag_next_button)
        self.promo_list_pag_act_box.setLayout(self.promo_list_pag_act_layout)
        self.promo_list_box = MyGroupBox()
        self.promo_list_layout = MyVBoxLayout()
        self.promo_list_layout.addWidget(self.promo_list_table)
        self.promo_list_layout.addWidget(self.promo_list_pag_act_box)
        self.promo_list_box.setLayout(self.promo_list_layout)
        self.promo_list_tab = MyTabWidget()
        self.promo_list_tab.addTab(self.promo_list_box, 'Overview')
    
        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.add_promo_box,0,1)
        self.panel_a_layout.addWidget(self.promo_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def set_panel_b_box(self):
        self.panel_b_box = MyGroupBox()
        self.panel_b_layout = MyHBoxLayout()

        self.current_user_label = MyLabel(text=f"Current user: {'Phoebe'} (Admin)")
        self.total_promo_label = MyLabel(text=f"Total promo: {'9999'}")
        
        self.panel_b_layout.addWidget(self.current_user_label)
        self.panel_b_layout.addWidget(self.total_promo_label)
        self.panel_b_box.setLayout(self.panel_b_layout)

    def set_import_progress_dialog(self):
        self.import_progress_dialog = MyDialog()
        self.import_progress_layout = MyGridLayout()
        self.import_progress_label = MyLabel(text=f"Please wait... ({self.model.promo_data_count_value})")
        self.import_progress_bar = QProgressBar()
        self.import_progress_layout.addWidget(self.import_progress_label)
        self.import_progress_layout.addWidget(self.import_progress_bar)
        self.import_progress_dialog.setLayout(self.import_progress_layout)
        pass
    def set_add_promo_dialog(self):
        self.add_promo_dialog = MyDialog()
        self.add_promo_layout = MyVBoxLayout()

        self.add_promo_name_field = MyLineEdit(object_name='add_promo_name_field')
        self.add_promo_type_field = MyComboBox(object_name='add_promo_type_field')
        self.add_promo_discount_percent_field = MyLineEdit(object_name='add_promo_discount_percent_field')
        self.add_promo_description_field = MyPlainTextEdit(object_name='add_promo_description_field')
        self.add_promo_form_box = MyGroupBox()
        self.add_promo_form_layout = MyFormLayout()
        self.add_promo_form_layout.addRow(MyLabel(text='Promo name'))
        self.add_promo_form_layout.addRow(self.add_promo_name_field)
        self.add_promo_form_layout.addRow(MyLabel(text='Promo type'))
        self.add_promo_form_layout.addRow(self.add_promo_type_field)
        self.add_promo_form_layout.addRow(MyLabel(text='Discount percent'))
        self.add_promo_form_layout.addRow(self.add_promo_discount_percent_field)
        self.add_promo_form_layout.addRow(MyLabel(text='Description'))
        self.add_promo_form_layout.addRow(self.add_promo_description_field)
        self.add_promo_form_box.setLayout(self.add_promo_form_layout)
        self.add_promo_form_scra = MyScrollArea(object_name='add_promo_form_scra')
        self.add_promo_form_scra.setWidget(self.add_promo_form_box)

        self.add_promo_save_button = MyPushButton(object_name='add_promo_save_button', text='Save')
        self.add_promo_cancel_button = MyPushButton(object_name='add_promo_cancel_button', text='Cancel')
        self.add_promo_form_act_box = MyGroupBox()
        self.add_promo_form_act_layout = MyHBoxLayout(object_name='add_promo_form_act_layout')
        self.add_promo_form_act_layout.addWidget(self.add_promo_save_button)
        self.add_promo_form_act_layout.addWidget(self.add_promo_cancel_button)
        self.add_promo_form_act_box.setLayout(self.add_promo_form_act_layout)

        self.add_promo_layout.addWidget(self.add_promo_form_scra)
        self.add_promo_layout.addWidget(self.add_promo_form_act_box)
        self.add_promo_dialog.setLayout(self.add_promo_layout)
        pass

class MyPromoController:
    def __init__(self, model: MyPromoModel, view: MyPromoView):
        self.model = model
        self.view = view

        self.set_panel_a_box_conn()
        self.populate_promo_list_table()

    def set_panel_a_box_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)

        self.view.import_promo_button.clicked.connect(self.on_import_promo_button_clicked)
        self.view.add_promo_button.clicked.connect(self.on_add_promo_button_clicked)
        pass

    def populate_promo_list_table(self, text_filter='', page_number=1):
        self.promo_list_data = schema.list_promo_data(text_filter=text_filter, page_number=page_number)        

        self.view.promo_list_table.setRowCount(len(self.promo_list_data))

        for list_i, list_v in enumerate(self.promo_list_data):
            self.list_edit_button = MyPushButton(text='Edit')
            self.list_view_button = MyPushButton(text='View')
            self.list_delete_button = MyPushButton(text='Delete')
            list_a_act_box = MyGroupBox()
            list_a_act_layout = MyHBoxLayout()
            list_a_act_layout.addWidget(self.list_edit_button)
            list_a_act_layout.addWidget(self.list_view_button)
            list_a_act_layout.addWidget(self.list_delete_button)
            list_a_act_box.setLayout(list_a_act_layout)

            promo_name = QTableWidgetItem(f"{list_v[0]}")
            promo_type = QTableWidgetItem(f"{list_v[1]}")
            promo_discount_percent = QTableWidgetItem(f"{list_v[2]}")
            promo_description = QTableWidgetItem(f"{list_v[3]}")

            self.view.promo_list_table.setCellWidget(list_i, 0, list_a_act_box)
            self.view.promo_list_table.setItem(list_i, 1, promo_name)
            self.view.promo_list_table.setItem(list_i, 2, promo_type)
            self.view.promo_list_table.setItem(list_i, 3, promo_discount_percent)
            self.view.promo_list_table.setItem(list_i, 4, promo_description)
        
    def on_text_filter_button_clicked(self):
        text_filter_text = self.view.text_filter_field.text()

        self.populate_promo_list_table(text_filter=text_filter_text, page_number=1)

    def on_import_promo_button_clicked(self):
        # TODO: add the importer thread

        self.promo_csv_file_path, _ = QFileDialog.getOpenFileName(self.view, 'Import promo', self.model.csv_path, 'CSV Files (*.csv)')

        if self.promo_csv_file_path:
            self.promo_data_frame = pd.read_csv(self.promo_csv_file_path, encoding='utf-8-sig', keep_default_na=False, header=None)
            
            self.model.promo_data_total_value = len(self.promo_data_frame)
            self.model.promo_data_remaining_value = len(self.promo_data_frame)
            
            self.view.set_import_progress_dialog()

            self.manual_csv_importer = ManualPromoImport(promo_data_frame=self.promo_data_frame)
            self.manual_csv_importer.start()

            self.manual_csv_importer.progress_signal.connect(self.on_manual_csv_importer_progress_signal)
            self.manual_csv_importer.finished_signal.connect(self.on_manual_csv_importer_finished_signal)

            self.view.import_progress_dialog.exec()
            

        pass
    def on_manual_csv_importer_progress_signal(self):
        self.model.promo_data_count_value += 1
        self.model.promo_data_remaining_value -= 1
        progress_value = int((self.model.promo_data_count_value / self.model.promo_data_total_value) * 100)

        self.view.import_progress_label.setText(f"Please wait... ({self.model.promo_data_remaining_value})")
        self.view.import_progress_bar.setValue(progress_value)
        pass
    def on_manual_csv_importer_finished_signal(self):
        self.view.import_progress_dialog.close()
        QMessageBox.information(self.view, 'Success', 'All promo has been imported.')
        pass
    def on_add_promo_button_clicked(self):
        self.view.set_add_promo_dialog()
        
        self.view.add_promo_save_button.clicked.connect(self.on_add_promo_save_button_clicked)
        self.view.add_promo_cancel_button.clicked.connect(self.on_add_promo_cancel_button_clicked)

        self.view.add_promo_dialog.exec()
        pass
    def on_add_promo_save_button_clicked(self):
        text_filter_text = self.view.text_filter_field.text()
        
        promo_name = self.view.add_promo_name_field.text()
        promo_type = self.view.add_promo_type_field.currentText()
        discount_percent = self.view.add_promo_discount_percent_field.text()
        description = self.view.add_promo_description_field.toPlainText()

        schema.add_new_promo(
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            description=description
        )

        self.view.add_promo_dialog.close()

        QMessageBox.information(self.view, 'Success', 'Promo has been imported.')

        self.populate_promo_list_table(text_filter=text_filter_text, page_number=1)
        pass
    def on_add_promo_cancel_button_clicked(self):
        self.view.add_promo_dialog.close()
        pass

if __name__ == ('__main__'):
    promo_app = QApplication(sys.argv)
    
    schema = MyPromoSchema()

    model = MyPromoModel()
    view = MyPromoView(model)
    controller = MyPromoController(model, view)
    
    
    view.showMaximized()
    sys.exit(promo_app.exec())
