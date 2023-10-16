
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
from src.sql.admin.promo import *
from src.widget.admin.admin import *
from templates.qss.qss_config import QSSConfig

schema = MyPromoSchema()
qss = QSSConfig()

class MyPromoModel: # NOTE: entries
    def __init__(self, name):
        # NOTE: global variables
        self.gdrive_path = 'G:' + f"/My Drive/"
        self.user_name = name

        self.init_selected_promo_data_entry()
        self.init_progress_data_entry()
        self.init_promo_list_page_entry()

    def init_promo_list_page_entry(self):
        self.page_number = 1
        self.total_page_number = schema.count_promo_list_total_pages()

    def init_selected_promo_data_entry(self):
        self.sel_promo_name_value = None
        self.sel_promo_type_value = None
        self.sel_promo_percent_value = None
        self.sel_promo_description_value = None
        self.sel_datetime_created_value = None
        self.sel_promo_id_value = None
        pass
    def assign_selected_promo_data_entry(self, value):
        self.sel_promo_name_value = str(value[0])
        self.sel_promo_type_value = str(value[1])
        self.sel_promo_percent_value = str(value[2])
        self.sel_promo_description_value = str(value[3])
        self.sel_datetime_created_value = str(value[4])
        self.sel_promo_id_value = value[5]

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

    def import_promo_entry(self, data_frame):
        self.promo_import_thread = MyDataImportThread(data_name='promo', data_frame=data_frame) # NOTE: ths is QThread for data import
        self.promo_import_thread.start()

    def setup_manage_promo_panel(self, window_title):
        self.manage_promo_dialog = MyDialog(window_title=window_title)
        self.manage_promo_layout = MyGridLayout()

        self.promo_name_label = MyLabel(text='Name')
        self.promo_type_label = MyLabel(text='Type')
        self.promo_percent_label = MyLabel(text='Percent')
        self.promo_description_label = MyLabel(text='Description')
        
        self.promo_name_field = MyLineEdit(object_name='promo_name_field')
        self.promo_type_field = MyComboBox(object_name='promo_type_field')
        self.promo_percent_field = MyLineEdit(object_name='promo_percent_field')
        self.promo_description_field = MyPlainTextEdit(object_name='promo_description_field')

        self.promo_form_box = MyGroupBox()
        self.promo_form_layout = MyFormLayout()
        self.promo_form_layout.insertRow(0,self.promo_name_label)
        self.promo_form_layout.insertRow(2,self.promo_type_label)
        self.promo_form_layout.insertRow(4,self.promo_percent_label)
        self.promo_form_layout.insertRow(6,self.promo_description_label)
        self.promo_form_layout.insertRow(1,self.promo_name_field)
        self.promo_form_layout.insertRow(3,self.promo_type_field)
        self.promo_form_layout.insertRow(5,self.promo_percent_field)
        self.promo_form_layout.insertRow(7,self.promo_description_field)
        self.promo_form_box.setLayout(self.promo_form_layout)
        self.promo_form_scra = MyScrollArea()
        self.promo_form_scra.setWidget(self.promo_form_box)

        self.manage_promo_save_button = MyPushButton(text='Save')
        self.manage_promo_close_button = MyPushButton(text='Close')
        self.manage_promo_act_box = MyGroupBox()
        self.manage_promo_act_layout = MyHBoxLayout(object_name='promo_act_layout')
        self.manage_promo_act_layout.addWidget(self.manage_promo_save_button)
        self.manage_promo_act_layout.addWidget(self.manage_promo_close_button)
        self.manage_promo_act_box.setLayout(self.manage_promo_act_layout)

        self.manage_promo_layout.addWidget(self.promo_form_scra,0,0)
        self.manage_promo_layout.addWidget(self.manage_promo_act_box,1,0,Qt.AlignmentFlag.AlignRight)
        self.manage_promo_dialog.setLayout(self.manage_promo_layout)
        pass
    def save_new_promo_entry(self):
        promo_name = self.promo_name_field.text()
        promo_type = self.promo_type_field.currentText()
        promo_percent = self.promo_percent_field.text()
        promo_description = self.promo_description_field.toPlainText()

        schema.add_new_promo(
                promo_name=promo_name,
                promo_type=promo_type,
                promo_percent=promo_percent,
                promo_description=promo_description
            )

        self.manage_promo_dialog.close()
        pass
    def save_edit_promo_entry(self):
        promo_name = self.promo_name_field.text()
        promo_type = self.promo_type_field.currentText()
        promo_percent = self.promo_percent_field.text()
        promo_description = self.promo_description_field.toPlainText()
        promo_id = self.sel_promo_id_value

        schema.edit_selected_promo(
                promo_name=promo_name,
                promo_type=promo_type,
                promo_percent=promo_percent,
                promo_description=promo_description,
                promo_id=promo_id
            )

        self.sel_promo_id_value = 0
        self.manage_promo_dialog.close()
        pass
    
    def setup_view_promo_panel(self):
        self.view_dialog = MyDialog(window_title=f"{self.sel_promo_name_value}")
        self.view_layout = MyGridLayout()

        self.promo_name_info_label = MyLabel(text=f"{self.sel_promo_name_value}")
        self.promo_type_info_label = MyLabel(text=f"{self.sel_promo_type_value}")
        self.promo_percent_info_label = MyLabel(text=f"{self.sel_promo_percent_value}")
        self.promo_description_info_label = MyLabel(text=f"{self.sel_promo_description_value}")
        self.datetime_created_info_label = MyLabel(text=f"{self.sel_datetime_created_value}")
        self.view_form_box = MyGroupBox()
        self.view_form_layout = MyFormLayout()
        self.view_form_layout.addRow('Name', self.promo_name_info_label)
        self.view_form_layout.addRow('Type', self.promo_type_info_label)
        self.view_form_layout.addRow('Percent', self.promo_percent_info_label)
        self.view_form_layout.addRow('Description', self.promo_description_info_label)
        self.view_form_layout.addRow('Date/Time created', self.datetime_created_info_label)
        self.view_form_box.setLayout(self.view_form_layout)
        self.view_form_scra = MyScrollArea()
        self.view_form_scra.setWidget(self.view_form_box)

        self.view_form_close_button = MyPushButton(text='Close')

        self.view_layout.addWidget(self.view_form_scra,0,0)
        self.view_layout.addWidget(self.view_form_close_button,1,0,Qt.AlignmentFlag.AlignRight)
        self.view_dialog.setLayout(self.view_layout)
    
    pass
class MyPromoView(MyGroupBox): # NOTE: layout
    def __init__(self, model: MyPromoModel):
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
        self.import_promo_button = MyPushButton(text='Import')
        self.add_promo_button = MyPushButton(text='Add')
        self.interactive_act_box = MyGroupBox()
        self.interactive_act_layout = MyHBoxLayout()
        self.interactive_act_layout.addWidget(self.sync_ui_button)
        self.interactive_act_layout.addWidget(self.import_promo_button)
        self.interactive_act_layout.addWidget(self.add_promo_button)
        self.interactive_act_box.setLayout(self.interactive_act_layout)

        self.promo_list_table = MyTableWidget(object_name='promo_list_table')
        self.promo_list_prev_button = MyPushButton(text='Prev')
        self.promo_list_page_label = MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.promo_list_next_button = MyPushButton(text='Next')
        self.promo_list_pag_box = MyGroupBox()
        self.promo_list_pag_layout = MyHBoxLayout(object_name='promo_list_pag_layout')
        self.promo_list_pag_layout.addWidget(self.promo_list_prev_button)
        self.promo_list_pag_layout.addWidget(self.promo_list_page_label)
        self.promo_list_pag_layout.addWidget(self.promo_list_next_button)
        self.promo_list_pag_box.setLayout(self.promo_list_pag_layout)
        self.promo_list_box = MyGroupBox()
        self.promo_list_layout = MyGridLayout()
        self.promo_list_layout.addWidget(self.promo_list_table,0,0)
        self.promo_list_layout.addWidget(self.promo_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.promo_list_box.setLayout(self.promo_list_layout)
        self.promo_list_tab = MyTabWidget()
        self.promo_list_tab.addTab(self.promo_list_box, 'Overview')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.interactive_act_box,0,1)
        self.panel_a_layout.addWidget(self.promo_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    pass 
class MyPromoController: # NOTE: connections, setting attributes
    def __init__(self, model: MyPromoModel, view: MyPromoView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_promo_list_table()

    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.view.import_promo_button.clicked.connect(self.on_import_promo_button_clicked)
        self.view.add_promo_button.clicked.connect(self.on_add_promo_button_clicked)
        self.view.promo_list_prev_button.clicked.connect(lambda: self.on_promo_list_pag_button_clicked(action='go_prev'))
        self.view.promo_list_next_button.clicked.connect(lambda: self.on_promo_list_pag_button_clicked(action='go_next'))
        pass

    def populate_promo_list_table(self, text_filter='', page_number=1):
        promo_list = schema.list_all_promo_col(text_filter=text_filter, page_number=page_number)

        self.view.promo_list_page_label.setText(f"Page {page_number}/{self.model.total_page_number}")

        self.view.promo_list_prev_button.setEnabled(page_number > 1)
        self.view.promo_list_next_button.setEnabled(len(promo_list) == 30)

        self.view.promo_list_table.setRowCount(len(promo_list))

        for promo_list_i, promo_list_v in enumerate(promo_list):
            self.edit_promo_button = MyPushButton(text='Edit')
            self.view_promo_button = MyPushButton(text='View')
            self.delete_promo_button = MyPushButton(text='Delete')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.edit_promo_button)
            table_act_laoyut.addWidget(self.view_promo_button)
            table_act_laoyut.addWidget(self.delete_promo_button)
            table_act_panel.setLayout(table_act_laoyut)
            promo_name = QTableWidgetItem(f"{promo_list_v[0]}")
            promo_type = QTableWidgetItem(f"{promo_list_v[1]}")
            promo_percent = QTableWidgetItem(f"{promo_list_v[2]}")
            promo_description = QTableWidgetItem(f"{promo_list_v[3]}")
            datetime_created = QTableWidgetItem(f"{promo_list_v[4]}")

            self.view.promo_list_table.setCellWidget(promo_list_i, 0, table_act_panel)
            self.view.promo_list_table.setItem(promo_list_i, 1, promo_name)
            self.view.promo_list_table.setItem(promo_list_i, 2, promo_type)
            self.view.promo_list_table.setItem(promo_list_i, 3, promo_percent)
            self.view.promo_list_table.setItem(promo_list_i, 4, promo_description)
            self.view.promo_list_table.setItem(promo_list_i, 5, datetime_created)


            self.setup_promo_list_table_act_panel_conn(value=promo_list_v)
            pass
        pass
    def setup_promo_list_table_act_panel_conn(self, value):
        self.edit_promo_button.clicked.connect(lambda _, value=value: self.on_edit_promo_button_clicked(value))
        self.view_promo_button.clicked.connect(lambda _, value=value: self.on_view_promo_button_clicked(value))
        self.delete_promo_button.clicked.connect(lambda _, value=value: self.on_delete_promo_button_clicked(value))

    def on_text_filter_button_clicked(self):
        self.model.page_number = 1
        self.view.promo_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

        self.populate_promo_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number) 
        pass
    def on_sync_ui_button_clicked(self):
        self.model.init_promo_list_page_entry()
        self.view.promo_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.populate_promo_list_table()

        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass
    
    def on_import_promo_button_clicked(self):
        try:
            self.promo_csv_file, _ = QFileDialog.getOpenFileName(self.view, 'Open CSV', qss.csv_file_path, 'CSV File (*.csv)')
            self.promo_csv_df = pd.read_csv(self.promo_csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

            if self.promo_csv_file:
                self.model.prog_total_data_value = len(self.promo_csv_df)
                self.model.prog_remaining_data_value = len(self.promo_csv_df)

                self.model.setup_progress_panel(window_title=f"{'percentage'}", progress_type='promo_import')
                self.model.import_promo_entry(data_frame=self.promo_csv_df)
                self.setup_promo_import_thread_conn()
                self.model.progress_dialog.exec()

                if self.model.prog_remaining_data_value > 0 and self.model.progress_dialog.close():
                    self.model.promo_import_thread.stop()

                    self.model.init_progress_data_entry()

                    QMessageBox.critical(self.view, 'Cancelled', 'Import has been cancelled')
                    self.on_sync_ui_button_clicked()

            pass
        except Exception as e:
            self.promo_csv_file = ''
        pass
    def setup_promo_import_thread_conn(self):
        self.model.promo_import_thread.update_signal.connect(self.on_promo_import_thread_update_signal)
        self.model.promo_import_thread.finished_signal.connect(self.on_promo_import_thread_finished_signal)
        self.model.promo_import_thread.invalid_signal.connect(self.on_promo_import_thread_invalid_signal)
        pass
    def on_promo_import_thread_update_signal(self):
        try:
            self.model.prog_data_count_value += 1
            self.model.prog_remaining_data_value -= 1
            progress_percent_value = int((self.model.prog_data_count_value / self.model.prog_total_data_value) * 100)

            self.model.progress_dialog.setWindowTitle(f"{progress_percent_value}% complete")
            self.model.progress_label.setText(f"Please wait...({self.model.prog_remaining_data_value})")
            self.model.progress_bar.setValue(progress_percent_value)

            pass
        except Exception as e:
            self.model.init_progress_data_entry()
        pass
    def on_promo_import_thread_finished_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.information(self.view, 'Success', 'All promo has been imported')
        self.on_sync_ui_button_clicked()
        pass
    def on_promo_import_thread_invalid_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.critical(self.view, 'Error', 'Invalid CSV file.')
        self.on_sync_ui_button_clicked()
        pass

    def on_add_promo_button_clicked(self):  
        self.model.setup_manage_promo_panel(window_title='Add promo')
        self.populate_manage_promo_combo_box_field()
        self.setup_manage_promo_panel_conn(conn_type='add_promo')

        self.model.manage_promo_dialog.exec()
        pass
    def on_edit_promo_button_clicked(self, value):
        self.model.assign_selected_promo_data_entry(value)
        self.model.setup_manage_promo_panel(window_title=f"Edit {self.model.sel_promo_name_value}")
        self.populate_manage_promo_combo_box_field()

        self.model.promo_name_field.setText(self.model.sel_promo_name_value)
        self.model.promo_type_field.setCurrentText(self.model.sel_promo_type_value)
        self.model.promo_percent_field.setText(self.model.sel_promo_percent_value)
        self.model.promo_description_field.setPlainText(self.model.sel_promo_description_value)

        self.setup_manage_promo_panel_conn(conn_type='edit_promo')

        self.model.manage_promo_dialog.exec()
        pass
    def populate_manage_promo_combo_box_field(self):
        promo_type_data = schema.list_promo_type_col()

        self.model.promo_type_field.clear()
        for promo_type in promo_type_data: self.model.promo_type_field.addItems(promo_type)
        pass
    def setup_manage_promo_panel_conn(self, conn_type):
        self.model.manage_promo_save_button.clicked.connect(lambda: self.on_manage_promo_save_button_clicked(action=conn_type))
        self.model.manage_promo_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.manage_promo_dialog))
        pass
    def on_manage_promo_save_button_clicked(self, action):
        promo_name = self.model.promo_name_field.text()
        promo_type = self.model.promo_type_field.currentText()
        promo_percent = self.model.promo_percent_field.text()

        if '' not in [promo_name, promo_type, promo_percent]:
            if promo_percent.replace('.', '', 1).isdigit():
                if action == 'add_promo':
                    self.model.save_new_promo_entry()
                    self.model.init_selected_promo_data_entry()

                    QMessageBox.information(self.view, 'Success', 'New promo has been added.')
                    pass
                elif action == 'edit_promo':
                    self.model.save_edit_promo_entry()
                    self.model.init_selected_promo_data_entry()

                    QMessageBox.information(self.view, 'Success', 'Promo has been edited.')
                    pass
                self.on_sync_ui_button_clicked()
                pass
            else:
                QMessageBox.critical(self.model.manage_promo_dialog, 'Error', 'Invalid numerical input.')
                pass
        else:
            self.set_label_required_field_indicator(promo_name, promo_type, promo_percent)

            QMessageBox.critical(self.model.manage_promo_dialog, 'Error', 'Please fill out the required field.')
            pass
        pass
    def set_label_required_field_indicator(self, promo_name, promo_type, promo_percent):
        self.model.promo_name_label.setText(f"Name {qss.required_label}") if promo_name == '' else self.model.promo_name_label.setText(f"Name")
        self.model.promo_type_label.setText(f"Type {qss.required_label}") if promo_type == '' else self.model.promo_type_label.setText(f"Type")
        self.model.promo_percent_label.setText(f"Percent {qss.required_label}") if promo_percent == '' else self.model.promo_percent_label.setText(f"Percent")
    
    def on_view_promo_button_clicked(self, value):
        self.model.assign_selected_promo_data_entry(value)

        self.model.setup_view_promo_panel()

        self.setup_view_promo_conn()

        self.model.view_dialog.exec()
        pass
    def setup_view_promo_conn(self):
        self.model.view_form_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.view_dialog))

    def on_delete_promo_button_clicked(self, value):
        self.model.assign_selected_promo_data_entry(value)

        confirm = QMessageBox.warning(self.view, 'Confirm', f"Delete {self.model.sel_promo_name_value}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_promo(promo_id=self.model.sel_promo_id_value)

            self.model.init_selected_promo_data_entry()

            QMessageBox.information(self.view, 'Success', 'Promo has been deleted.')

            self.on_sync_ui_button_clicked()
            pass
        else:
            self.model.init_selected_promo_data_entry()
            return
        pass
    
    def on_close_button_clicked(self, widget: QWidget):
        widget.close()

        self.model.init_selected_promo_data_entry()
        pass

    def on_promo_list_pag_button_clicked(self, action):
        print('promo_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.page_number > 1:
                self.model.page_number -= 1
                self.view.promo_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_promo_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        elif action == 'go_next':
            self.model.page_number += 1
            self.view.promo_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_promo_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        pass

    pass

class MyPromoWindow(MyGroupBox):
    def __init__(self, name): # NOTE: 'name' param is for the current user (cashier, admin, dev) name
        super().__init__(object_name='MyPromoWindow')

        self.model = MyPromoModel(name=name)
        self.view = MyPromoView(self.model)
        self.controller = MyPromoController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.show()


# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    promo_window = MyPromoWindow(name='test-name')

    promo_window.run()
    app.exec()