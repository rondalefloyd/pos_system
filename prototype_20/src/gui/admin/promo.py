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


from src.core.qss_config import *
from src.core.manual_csv_importer import *
from src.sql.admin.promo import *
from src.widget.admin.promo import *

class MyPromoModel: # IDEA: global variables
    def __init__(self):
        self.csv_path = 'G:' + f"/My Drive/csv/"

        self.promo_list_page_number = 1
        self.promo_list_total_page_number = schema.count_promo_list_total_pages()
        
        self.total_promo = schema.count_promo()

        self.promo_data_count_value = 0
        self.promo_data_total_value = 0
        self.promo_data_remaining_value = 0

    def set_promo_form_box(self):
        self.promo_name_label = MyLabel(text=f"Promo name")
        self.promo_type_label = MyLabel(text=f"Promo type")
        self.promo_discount_percent_label = MyLabel(text=f"Discount percent")
        self.promo_description_label = MyLabel(text=f"Description {qss.optional_label}")

        self.promo_name_field = MyLineEdit(object_name='promo_name_field')
        self.promo_type_field = MyComboBox(object_name='promo_type_field')
        self.promo_discount_percent_field = MyLineEdit(object_name='promo_discount_percent_field')
        self.promo_description_field = MyPlainTextEdit(object_name='promo_description_field')

        self.populate_promo_form_combo_box()

        self.promo_form_box = MyGroupBox()
        self.promo_form_layout = MyFormLayout()

        self.promo_form_layout.insertRow(0, self.promo_name_label)
        self.promo_form_layout.insertRow(2, self.promo_type_label)
        self.promo_form_layout.insertRow(4, self.promo_discount_percent_label)
        self.promo_form_layout.insertRow(6, self.promo_description_label)

        self.promo_form_layout.insertRow(1, self.promo_name_field)
        self.promo_form_layout.insertRow(3, self.promo_type_field)
        self.promo_form_layout.insertRow(5, self.promo_discount_percent_field)
        self.promo_form_layout.insertRow(7, self.promo_description_field)
        
        self.promo_form_box.setLayout(self.promo_form_layout)
        self.promo_form_scra = MyScrollArea(object_name='promo_form_scra')
        self.promo_form_scra.setWidget(self.promo_form_box)
        pass

    def populate_promo_form_combo_box(self):
        self.promo_type_field.clear()

        self.promo_type_data = schema.list_promo_type()
        
        for promo_type in self.promo_type_data:
            self.promo_type_field.addItems(promo_type)

class MyPromoView(MyWidget):  # IDEA: groupbox, layouts, dialogs
    def __init__(self, model: MyPromoModel):
        super().__init__(object_name='my_sales_view')

        self.model = model

        self.set_main_panel()

    def set_main_panel(self):
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
        self.text_filter_layout = MyHBoxLayout(object_name='text_filter_layout')
        self.text_filter_layout.addWidget(self.text_filter_field)
        self.text_filter_layout.addWidget(self.text_filter_button)
        self.text_filter_box.setLayout(self.text_filter_layout)

        self.import_promo_button = MyPushButton(text='Import')
        self.add_promo_button = MyPushButton(text='Add')
        self.add_promo_box = MyGroupBox()
        self.add_promo_layout = MyHBoxLayout(object_name='add_promo_layout')
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
        self.panel_b_layout = MyHBoxLayout(object_name='panel_b_layout')

        self.current_user_label = MyLabel(text=f"Current user: {'Phoebe'} (Admin)")
        self.total_promo_label = MyLabel(text=f"Total promo: {self.model.total_promo}")
        
        self.panel_b_layout.addWidget(self.current_user_label)
        self.panel_b_layout.addWidget(self.total_promo_label)
        self.panel_b_box.setLayout(self.panel_b_layout)

    def set_import_progress_dialog(self):
        self.import_progress_dialog = MyDialog()
        self.import_progress_layout = MyGridLayout()
        self.import_progress_label = MyLabel(text=f"Please wait...")
        self.import_progress_bar = QProgressBar()
        self.import_progress_layout.addWidget(self.import_progress_label)
        self.import_progress_layout.addWidget(self.import_progress_bar)
        self.import_progress_dialog.setLayout(self.import_progress_layout)
        pass
    def set_add_promo_dialog(self):
        self.add_promo_dialog = MyDialog()
        self.add_promo_layout = MyVBoxLayout()

        self.model.set_promo_form_box()

        self.add_promo_save_button = MyPushButton(object_name='add_promo_save_button', text='Save')
        self.add_promo_cancel_button = MyPushButton(object_name='add_promo_cancel_button', text='Cancel')
        self.add_promo_form_act_box = MyGroupBox()
        self.add_promo_form_act_layout = MyHBoxLayout(object_name='add_promo_form_act_layout')
        self.add_promo_form_act_layout.addWidget(self.add_promo_save_button)
        self.add_promo_form_act_layout.addWidget(self.add_promo_cancel_button)
        self.add_promo_form_act_box.setLayout(self.add_promo_form_act_layout)

        self.add_promo_layout.addWidget(self.model.promo_form_scra)
        self.add_promo_layout.addWidget(self.add_promo_form_act_box)
        self.add_promo_dialog.setLayout(self.add_promo_layout)
        pass
    
    def set_edit_promo_dialog(self):
        self.edit_promo_dialog = MyDialog()
        self.edit_promo_layout = MyVBoxLayout()

        self.model.set_promo_form_box()

        self.edit_promo_save_button = MyPushButton(object_name='edit_promo_save_button', text='Save')
        self.edit_promo_cancel_button = MyPushButton(object_name='edit_promo_cancel_button', text='Cancel')
        self.edit_promo_form_act_box = MyGroupBox()
        self.edit_promo_form_act_layout = MyHBoxLayout(object_name='edit_promo_form_act_layout')
        self.edit_promo_form_act_layout.addWidget(self.edit_promo_save_button)
        self.edit_promo_form_act_layout.addWidget(self.edit_promo_cancel_button)
        self.edit_promo_form_act_box.setLayout(self.edit_promo_form_act_layout)

        self.edit_promo_layout.addWidget(self.model.promo_form_scra)
        self.edit_promo_layout.addWidget(self.edit_promo_form_act_box)
        self.edit_promo_dialog.setLayout(self.edit_promo_layout)
        pass
    def set_show_promo_dialog(self):
        self.show_promo_dialog = MyDialog()
        self.show_promo_layout = MyFormLayout()
        
        self.promo_name_info_label = MyLabel()
        self.promo_type_info_label = MyLabel()
        self.promo_discount_percent_info_label = MyLabel()
        self.promo_description_info_label = MyLabel()
        self.promo_date_created_info_label = MyLabel()
        self.show_promo_form_box = MyGroupBox()
        self.show_promo_form_layout = MyFormLayout()
        self.show_promo_form_layout.addRow('Name:', self.promo_name_info_label)
        self.show_promo_form_layout.addRow('Type:', self.promo_type_info_label)
        self.show_promo_form_layout.addRow('Discount_percent:', self.promo_discount_percent_info_label)
        self.show_promo_form_layout.addRow('Description:', self.promo_description_info_label)
        self.show_promo_form_layout.addRow(MyLabel(text='<hr>'))
        self.show_promo_form_layout.addRow('Date created:', self.promo_date_created_info_label)
        self.show_promo_form_box.setLayout(self.show_promo_form_layout)
        self.show_promo_form_scra = MyScrollArea(object_name='promo_form_scra')
        self.show_promo_form_scra.setWidget(self.show_promo_form_box)

        self.show_promo_close_button = MyPushButton(text='Close')
        self.show_promo_act_box = MyGroupBox()
        self.show_promo_act_layout = MyHBoxLayout(object_name='show_promo_act_layout')
        self.show_promo_act_layout.addWidget(self.show_promo_close_button)
        self.show_promo_act_box.setLayout(self.show_promo_act_layout)

        self.show_promo_layout.addRow(self.show_promo_form_scra)
        self.show_promo_layout.addRow(self.show_promo_act_box)

        self.show_promo_dialog.setLayout(self.show_promo_layout)

class MyPromoController: # IDEA: connections, populations, on signals
    def __init__(self, model: MyPromoModel, view: MyPromoView):
        self.model = model
        self.view = view

        self.set_panel_a_box_conn()
        self.set_promo_list_table_conn()

        self.populate_promo_list_table()

    def set_panel_a_box_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)

        self.view.import_promo_button.clicked.connect(self.on_import_promo_button_clicked)
        self.view.add_promo_button.clicked.connect(self.on_add_promo_button_clicked)
        pass
    def set_promo_list_table_conn(self):
        self.view.promo_list_pag_prev_button.clicked.connect(lambda: self.on_promo_list_pag_button_clicked(action='prev'))
        self.view.promo_list_pag_next_button.clicked.connect(lambda: self.on_promo_list_pag_button_clicked(action='next'))
        pass

    def populate_form_required_label(self, promo_name, promo_type, discount_percent):
        self.model.promo_name_label.setText(f"Promo name {qss.required_label}") if promo_name == '' else self.model.promo_name_label.setText(f"Promo name")
        self.model.promo_type_label.setText(f"Promo type {qss.required_label}") if promo_type == '' else self.model.promo_type_label.setText(f"Promo type")
        self.model.promo_discount_percent_label.setText(f"Discount percent {qss.required_label}") if discount_percent == '' else self.model.promo_discount_percent_label.setText(f"Discount percent")
        pass
    def populate_promo_list_table(self):
        text_filter_value = self.view.text_filter_field.text()
        page_number = self.model.promo_list_page_number
        total_page_number = self.model.promo_list_total_page_number

        print('text_filter_value:', text_filter_value)
        print('page_number:', page_number)
        print('total_page_number:', total_page_number)

        self.promo_list_data = schema.list_promo_data(text_filter=text_filter_value, page_number=page_number)        

        self.view.promo_list_pag_page_label.setText(f"Page {page_number}/{total_page_number}")

        self.view.promo_list_pag_prev_button.setEnabled(page_number > 1)
        self.view.promo_list_pag_next_button.setEnabled(len(self.promo_list_data) == 30)

        self.view.promo_list_table.setRowCount(len(self.promo_list_data))

        for list_i, list_v in enumerate(self.promo_list_data):
            self.list_edit_button = MyPushButton(text='Edit')
            self.list_show_button = MyPushButton(text='Show')
            self.list_delete_button = MyPushButton(text='Delete')
            list_act_box = MyGroupBox()
            list_act_layout = MyHBoxLayout(object_name='list_act_layout')
            list_act_layout.addWidget(self.list_edit_button)
            list_act_layout.addWidget(self.list_show_button)
            list_act_layout.addWidget(self.list_delete_button)
            list_act_box.setLayout(list_act_layout)

            promo_name = QTableWidgetItem(f"{list_v[0]}")
            promo_type = QTableWidgetItem(f"{list_v[1]}")
            promo_discount_percent = QTableWidgetItem(f"{list_v[2]}")
            promo_description = QTableWidgetItem(f"{list_v[3]}")
            date_created = QTableWidgetItem(f"{list_v[4]}")

            self.view.promo_list_table.setCellWidget(list_i, 0, list_act_box)
            self.view.promo_list_table.setItem(list_i, 1, promo_name)
            self.view.promo_list_table.setItem(list_i, 2, promo_type)
            self.view.promo_list_table.setItem(list_i, 3, promo_discount_percent)
            self.view.promo_list_table.setItem(list_i, 4, promo_description)
            self.view.promo_list_table.setItem(list_i, 5, date_created)

            self.list_edit_button.clicked.connect(lambda _, list_v=list_v: self.on_list_edit_button_clicked(list_v))
            self.list_show_button.clicked.connect(lambda _, list_v=list_v: self.on_list_show_button_clicked(list_v))
            self.list_delete_button.clicked.connect(lambda _, list_v=list_v: self.on_list_delete_button_clicked(list_v))
        
    def on_text_filter_button_clicked(self):
        self.populate_promo_list_table()
    
    def on_import_promo_button_clicked(self):
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

        self.model.promo_list_page_number = 1
        self.populate_promo_list_table()
        pass
    
    def on_add_promo_button_clicked(self):
        self.view.set_add_promo_dialog()
        
        self.view.add_promo_save_button.clicked.connect(self.on_add_promo_save_button_clicked)
        self.view.add_promo_cancel_button.clicked.connect(self.on_add_promo_cancel_button_clicked)

        self.view.add_promo_dialog.exec()
        pass
    def on_add_promo_save_button_clicked(self):
        promo_name = self.model.promo_name_field.text()
        promo_type = self.model.promo_type_field.currentText()
        discount_percent = self.model.promo_discount_percent_field.text()
        description = self.model.promo_description_field.toPlainText()

        if '' not in [promo_name, promo_type, discount_percent]:
            if discount_percent.isdigit() is True:
                schema.add_new_promo(
                    promo_name=promo_name,
                    promo_type=promo_type,
                    discount_percent=discount_percent,
                    description=description
                )

                self.view.add_promo_dialog.close()

                QMessageBox.information(self.view, 'Success', 'Promo has been added.')

                self.model.promo_list_page_number = 1
                self.populate_promo_list_table()
                pass
            else:
                QMessageBox.critical(self.view.add_promo_dialog, 'Error', 'Invalid numerical input.')
            pass
        else:
            self.populate_form_required_label(promo_name, promo_type, discount_percent)
            
            QMessageBox.critical(self.view.add_promo_dialog, 'Error', 'Please fill out all required fields.')
            pass
        pass

    def on_add_promo_cancel_button_clicked(self):
        self.view.add_promo_dialog.close()
        pass

    def on_list_edit_button_clicked(self, list_v):
        self.view.set_edit_promo_dialog()
        
        self.model.promo_name_field.setText(f"{list_v[0]}")
        self.model.promo_type_field.setCurrentText(f"{list_v[1]}")
        self.model.promo_discount_percent_field.setText(f"{list_v[2]}")
        self.model.promo_description_field.setPlainText(f"{list_v[3]}")

        self.view.edit_promo_save_button.clicked.connect(lambda: self.on_edit_promo_save_button_clicked(promo_id=list_v[5]))
        self.view.edit_promo_cancel_button.clicked.connect(self.on_edit_promo_cancel_button_clicked)

        self.view.edit_promo_dialog.exec()
        pass 
    def on_edit_promo_save_button_clicked(self, promo_id):
        promo_name = self.model.promo_name_field.text()
        promo_type = self.model.promo_type_field.currentText()
        discount_percent = self.model.promo_discount_percent_field.text()
        description = self.model.promo_description_field.toPlainText()

        if '' not in [promo_name, promo_type, discount_percent]:
            if discount_percent.isdigit() is True:
                schema.edit_selected_promo(
                    promo_name=promo_name,
                    promo_type=promo_type,
                    discount_percent=discount_percent,
                    description=description,
                    promo_id=promo_id,
                )

                self.view.edit_promo_dialog.close()

                QMessageBox.information(self.view, 'Success', 'Promo has been added.')

                self.model.promo_list_page_number = 1
                self.populate_promo_list_table()
                pass
            else:
                QMessageBox.critical(self.view.edit_promo_dialog, 'Error', 'Invalid numerical input.')
            pass
        else:
            self.populate_form_required_label(promo_name, promo_type, discount_percent)
            
            QMessageBox.critical(self.view.edit_promo_dialog, 'Error', 'Please fill out all required fields.')
            pass
        pass
    def on_edit_promo_cancel_button_clicked(self):
        self.view.edit_promo_dialog.close()
        pass

    def on_list_show_button_clicked(self, list_v):
        self.view.set_show_promo_dialog()

        self.view.promo_name_info_label.setText(f"{list_v[0]}")
        self.view.promo_type_info_label.setText(f"{list_v[1]}")
        self.view.promo_discount_percent_info_label.setText(f"{list_v[2]}")
        self.view.promo_description_info_label.setText(f"{list_v[3]}")
        self.view.promo_date_created_info_label.setText(f"{list_v[4]}")

        self.view.show_promo_close_button.clicked.connect(self.on_show_promo_close_button_clicked)

        self.view.show_promo_dialog.exec()
        pass
    def on_show_promo_close_button_clicked(self):
        self.view.show_promo_dialog.close()

    def on_list_delete_button_clicked(self, list_v):
        # TODO: delete_button
        promo_id = list_v[5]

        confirm = QMessageBox.warning(
            self.view,
            'Delete',
            f"Are you sure you want to delete this {list_v[0]}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_promo(promo_id=promo_id)
        
            QMessageBox.information(self.view, 'Success', 'Promo has been deleted.')

            self.populate_promo_list_table()
        pass

    def on_promo_list_pag_button_clicked(self, action):
        if action == 'prev':
            if self.model.promo_list_page_number > 1:
                self.model.promo_list_page_number -= 1
                self.view.promo_list_pag_page_label.setText(f"Page {self.model.promo_list_page_number}/{self.model.promo_list_total_page_number}")

            self.populate_promo_list_table()
            pass
        elif action == 'next':
            self.model.promo_list_page_number += 1
            self.view.promo_list_pag_page_label.setText(f"Page {self.model.promo_list_page_number}/{self.model.promo_list_total_page_number}")

            self.populate_promo_list_table()
            pass

if __name__ == ('__main__'):
    promo_app = QApplication(sys.argv)
    
    schema = MyPromoSchema()
    qss = QSSConfig()

    model = MyPromoModel()
    view = MyPromoView(model)
    controller = MyPromoController(model, view)
    
    
    view.showMaximized()
    sys.exit(promo_app.exec())
