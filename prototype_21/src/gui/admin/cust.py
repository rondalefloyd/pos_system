
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
from src.sql.admin.cust import *
from src.widget.admin.admin import *
from templates.qss.qss_config import QSSConfig

schema = MyCustSchema()
qss = QSSConfig()

class MyCustModel: # NOTE: entries
    def __init__(self, name):
        # NOTE: global variables
        self.gdrive_path = 'G:' + f"/My Drive/"
        self.user_name = name

        self.init_selected_cust_data_entry()
        self.init_progress_data_entry()
        self.init_cust_list_page_entry()

    def init_cust_list_page_entry(self):
        self.page_number = 1
        self.total_page_number = schema.select_cust_count_total_pages()

    def init_selected_cust_data_entry(self):
        self.sel_cust_name_value = None
        self.sel_cust_address_value = None
        self.sel_cust_barrio_value = None
        self.sel_cust_town_value = None
        self.sel_cust_phone_value = None
        self.sel_cust_age_value = None
        self.sel_cust_gender_value = None
        self.sel_cust_marital_status_value = None
        self.sel_cust_points_value = None

        self.sel_datetime_created_value = None
        self.sel_cust_id_value = None
        self.sel_reward_id_value = None
        pass
    def assign_selected_cust_data_entry(self, value):
        self.sel_cust_name_value = str(value[0])
        self.sel_cust_address_value = str(value[1])
        self.sel_cust_barrio_value = str(value[2])
        self.sel_cust_town_value = str(value[3])
        self.sel_cust_phone_value = str(value[4])
        self.sel_cust_age_value = str(value[5])
        self.sel_cust_gender_value = str(value[6])
        self.sel_cust_marital_status_value = str(value[7])
        self.sel_cust_points_value = str(value[8])

        self.sel_datetime_created_value = str(value[9])
        self.sel_cust_id_value = value[10]
        self.sel_reward_id_value = value[11]

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

    def import_cust_entry(self, data_frame):
        self.cust_import_thread = MyDataImportThread(data_name='cust', data_frame=data_frame) # NOTE: ths is QThread for data import
        self.cust_import_thread.start()

    def setup_manage_cust_panel(self, window_title):
        self.manage_cust_dialog = MyDialog(window_title=window_title)
        self.manage_cust_layout = MyGridLayout()

        self.cust_name_label = MyLabel(text='Name')
        self.cust_address_label = MyLabel(text='Address')
        self.cust_barrio_label = MyLabel(text='Barrio')
        self.cust_town_label = MyLabel(text='Town')
        self.cust_phone_label = MyLabel(text='Phone')
        self.cust_age_label = MyLabel(text='Age')
        self.cust_gender_label = MyLabel(text='Gender')
        self.cust_marital_status_label = MyLabel(text='Marital status')
        self.cust_points_label = MyLabel(text='Points')
        
        self.cust_name_field = MyLineEdit(object_name='cust_name_field')
        self.cust_address_field = MyLineEdit(object_name='cust_address_field')
        self.cust_barrio_field = MyComboBox(object_name='cust_barrio_field')
        self.cust_town_field = MyComboBox(object_name='cust_town_field')
        self.cust_phone_field = MyLineEdit(object_name='cust_phone_field')
        self.cust_age_field = MyLineEdit(object_name='cust_age_field')
        self.cust_gender_field = MyComboBox(object_name='cust_gender_field')
        self.cust_marital_status_field = MyComboBox(object_name='cust_marital_status_field')
        self.cust_points_field = MyLineEdit(object_name='cust_points_field')

        self.cust_form_box = MyGroupBox()
        self.cust_form_layout = MyFormLayout()
        self.cust_form_layout.insertRow(0,self.cust_name_label)
        self.cust_form_layout.insertRow(2,self.cust_address_label)
        self.cust_form_layout.insertRow(4,self.cust_barrio_label)
        self.cust_form_layout.insertRow(6,self.cust_town_label)
        self.cust_form_layout.insertRow(8,self.cust_phone_label)
        self.cust_form_layout.insertRow(10,self.cust_age_label)
        self.cust_form_layout.insertRow(12,self.cust_gender_label)
        self.cust_form_layout.insertRow(14,self.cust_marital_status_label)
        self.cust_form_layout.insertRow(16,self.cust_points_label)

        self.cust_form_layout.insertRow(1,self.cust_name_field)
        self.cust_form_layout.insertRow(3,self.cust_address_field)
        self.cust_form_layout.insertRow(5,self.cust_barrio_field)
        self.cust_form_layout.insertRow(7,self.cust_town_field)
        self.cust_form_layout.insertRow(9,self.cust_phone_field)
        self.cust_form_layout.insertRow(11,self.cust_age_field)
        self.cust_form_layout.insertRow(13,self.cust_gender_field)
        self.cust_form_layout.insertRow(15,self.cust_marital_status_field)
        self.cust_form_layout.insertRow(17,self.cust_points_field)
        self.cust_form_box.setLayout(self.cust_form_layout)
        self.cust_form_scra = MyScrollArea()
        self.cust_form_scra.setWidget(self.cust_form_box)

        self.manage_cust_save_button = MyPushButton(text='Save')
        self.manage_cust_close_button = MyPushButton(text='Close')
        self.manage_cust_act_box = MyGroupBox()
        self.manage_cust_act_layout = MyHBoxLayout(object_name='cust_act_layout')
        self.manage_cust_act_layout.addWidget(self.manage_cust_save_button)
        self.manage_cust_act_layout.addWidget(self.manage_cust_close_button)
        self.manage_cust_act_box.setLayout(self.manage_cust_act_layout)

        self.manage_cust_layout.addWidget(self.cust_form_scra,0,0)
        self.manage_cust_layout.addWidget(self.manage_cust_act_box,1,0,Qt.AlignmentFlag.AlignRight)
        self.manage_cust_dialog.setLayout(self.manage_cust_layout)
        pass
    def save_new_cust_entry(self):
        cust_name = self.cust_name_field.text()
        cust_address = self.cust_address_field.text()
        cust_barrio = self.cust_barrio_field.currentText()
        cust_town = self.cust_town_field.currentText()
        cust_phone = self.cust_phone_field.text()
        cust_age = self.cust_age_field.text()
        cust_gender = self.cust_gender_field.currentText()
        cust_marital_status = self.cust_marital_status_field.currentText()
        cust_points = self.cust_points_field.text()

        schema.insert_new_cust_data(
                cust_name=cust_name,
                cust_address=cust_address,
                cust_barrio=cust_barrio,
                cust_town=cust_town,
                cust_phone=cust_phone,
                cust_age=cust_age,
                cust_gender=cust_gender,
                cust_marital_status=cust_marital_status,
                cust_points=cust_points,
            )

        self.manage_cust_dialog.close()
        pass
    def save_edit_cust_entry(self):
        cust_name = self.cust_name_field.text()
        cust_address = self.cust_address_field.text()
        cust_barrio = self.cust_barrio_field.currentText()
        cust_town = self.cust_town_field.currentText()
        cust_phone = self.cust_phone_field.text()
        cust_age = self.cust_age_field.text()
        cust_gender = self.cust_gender_field.currentText()
        cust_marital_status = self.cust_marital_status_field.currentText()
        cust_points = self.cust_points_field.text()
        cust_id = self.sel_cust_id_value
        reward_id = self.sel_reward_id_value

        schema.update_selected_cust_data(
                cust_name=cust_name,
                cust_address=cust_address,
                cust_barrio=cust_barrio,
                cust_town=cust_town,
                cust_phone=cust_phone,
                cust_age=cust_age,
                cust_gender=cust_gender,
                cust_marital_status=cust_marital_status,
                cust_points=cust_points,
                cust_id=cust_id,
                reward_id=reward_id,
            )

        self.sel_cust_id_value = 0
        self.manage_cust_dialog.close()
        pass
    
    def setup_view_cust_panel(self):
        self.view_dialog = MyDialog(window_title=f"{self.sel_cust_name_value}")
        self.view_layout = MyGridLayout()

        self.cust_name_info_label = MyLabel(text=f"{self.sel_cust_name_value}")
        self.cust_address_info_label = MyLabel(text=f"{self.sel_cust_address_value}")
        self.cust_barrio_info_label = MyLabel(text=f"{self.sel_cust_barrio_value}")
        self.cust_town_info_label = MyLabel(text=f"{self.sel_cust_town_value}")
        self.cust_phone_info_label = MyLabel(text=f"{self.sel_cust_phone_value}")
        self.cust_age_info_label = MyLabel(text=f"{self.sel_cust_age_value}")
        self.cust_gender_info_label = MyLabel(text=f"{self.sel_cust_gender_value}")
        self.cust_marital_status_info_label = MyLabel(text=f"{self.sel_cust_marital_status_value}")
        self.cust_points_info_label = MyLabel(text=f"{self.sel_cust_points_value}")
        self.datetime_created_info_label = MyLabel(text=f"{self.sel_datetime_created_value}")
        self.view_form_box = MyGroupBox()
        self.view_form_layout = MyFormLayout()
        self.view_form_layout.addRow('Name', self.cust_name_info_label)
        self.view_form_layout.addRow('Address', self.cust_address_info_label)
        self.view_form_layout.addRow('Barrio', self.cust_barrio_info_label)
        self.view_form_layout.addRow('Town', self.cust_town_info_label)
        self.view_form_layout.addRow('Phone', self.cust_phone_info_label)
        self.view_form_layout.addRow('Age', self.cust_age_info_label)
        self.view_form_layout.addRow('Gender', self.cust_gender_info_label)
        self.view_form_layout.addRow('Marital status', self.cust_marital_status_info_label)
        self.view_form_layout.addRow('Points', self.cust_points_info_label)
        self.view_form_layout.addRow('Date/Time created', self.datetime_created_info_label)
        self.view_form_box.setLayout(self.view_form_layout)
        self.view_form_scra = MyScrollArea()
        self.view_form_scra.setWidget(self.view_form_box)

        self.view_form_close_button = MyPushButton(text='Close')

        self.view_layout.addWidget(self.view_form_scra,0,0)
        self.view_layout.addWidget(self.view_form_close_button,1,0,Qt.AlignmentFlag.AlignRight)
        self.view_dialog.setLayout(self.view_layout)
    
    pass
class MyCustView(MyGroupBox): # NOTE: layout
    def __init__(self, model: MyCustModel):
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
        self.import_cust_button = MyPushButton(text='Import')
        self.add_cust_button = MyPushButton(text='Add')
        self.interactive_act_box = MyGroupBox()
        self.interactive_act_layout = MyHBoxLayout()
        self.interactive_act_layout.addWidget(self.sync_ui_button)
        self.interactive_act_layout.addWidget(self.import_cust_button)
        self.interactive_act_layout.addWidget(self.add_cust_button)
        self.interactive_act_box.setLayout(self.interactive_act_layout)

        self.cust_list_table = MyTableWidget(object_name='cust_list_table')
        self.cust_list_prev_button = MyPushButton(text='Prev')
        self.cust_list_page_label = MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.cust_list_next_button = MyPushButton(text='Next')
        self.cust_list_pag_box = MyGroupBox()
        self.cust_list_pag_layout = MyHBoxLayout(object_name='cust_list_pag_layout')
        self.cust_list_pag_layout.addWidget(self.cust_list_prev_button)
        self.cust_list_pag_layout.addWidget(self.cust_list_page_label)
        self.cust_list_pag_layout.addWidget(self.cust_list_next_button)
        self.cust_list_pag_box.setLayout(self.cust_list_pag_layout)
        self.cust_list_box = MyGroupBox()
        self.cust_list_layout = MyGridLayout()
        self.cust_list_layout.addWidget(self.cust_list_table,0,0)
        self.cust_list_layout.addWidget(self.cust_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.cust_list_box.setLayout(self.cust_list_layout)
        self.cust_list_tab = MyTabWidget()
        self.cust_list_tab.addTab(self.cust_list_box, 'Overview')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.interactive_act_box,0,1)
        self.panel_a_layout.addWidget(self.cust_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    pass 
class MyCustController: # NOTE: connections, setting attributes
    def __init__(self, model: MyCustModel, view: MyCustView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_cust_list_table()

    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.view.import_cust_button.clicked.connect(self.on_import_cust_button_clicked)
        self.view.add_cust_button.clicked.connect(self.on_add_cust_button_clicked)
        self.view.cust_list_prev_button.clicked.connect(lambda: self.on_cust_list_pag_button_clicked(action='go_prev'))
        self.view.cust_list_next_button.clicked.connect(lambda: self.on_cust_list_pag_button_clicked(action='go_next'))
        pass

    def populate_cust_list_table(self, text_filter='', page_number=1):
        cust_list = schema.select_cust_data(text_filter=text_filter, page_number=page_number)

        self.view.cust_list_page_label.setText(f"Page {page_number}/{self.model.total_page_number}")

        self.view.cust_list_prev_button.setEnabled(page_number > 1)
        self.view.cust_list_next_button.setEnabled(len(cust_list) == 30)

        self.view.cust_list_table.setRowCount(len(cust_list))

        for cust_list_i, cust_list_v in enumerate(cust_list):
            self.edit_cust_button = MyPushButton(text='Edit')
            self.view_cust_button = MyPushButton(text='View')
            self.delete_cust_button = MyPushButton(text='Delete')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.edit_cust_button)
            table_act_laoyut.addWidget(self.view_cust_button)
            table_act_laoyut.addWidget(self.delete_cust_button)
            table_act_panel.setLayout(table_act_laoyut)
            cust_name = QTableWidgetItem(f"{cust_list_v[0]}")
            cust_address = QTableWidgetItem(f"{cust_list_v[1]}")
            cust_barrio = QTableWidgetItem(f"{cust_list_v[2]}")
            cust_town = QTableWidgetItem(f"{cust_list_v[3]}")
            cust_phone = QTableWidgetItem(f"{cust_list_v[4]}")
            cust_age = QTableWidgetItem(f"{cust_list_v[5]}")
            cust_gender = QTableWidgetItem(f"{cust_list_v[6]}")
            cust_marital_status = QTableWidgetItem(f"{cust_list_v[7]}")
            cust_points = QTableWidgetItem(f"{cust_list_v[8]}")
            datetime_created = QTableWidgetItem(f"{cust_list_v[9]}")

            self.view.cust_list_table.setCellWidget(cust_list_i, 0, table_act_panel)
            self.view.cust_list_table.setItem(cust_list_i, 1, cust_name)
            self.view.cust_list_table.setItem(cust_list_i, 2, cust_address)
            self.view.cust_list_table.setItem(cust_list_i, 3, cust_barrio)
            self.view.cust_list_table.setItem(cust_list_i, 4, cust_town)
            self.view.cust_list_table.setItem(cust_list_i, 5, cust_phone)
            self.view.cust_list_table.setItem(cust_list_i, 6, cust_age)
            self.view.cust_list_table.setItem(cust_list_i, 7, cust_gender)
            self.view.cust_list_table.setItem(cust_list_i, 8, cust_marital_status)
            self.view.cust_list_table.setItem(cust_list_i, 9, cust_points)
            self.view.cust_list_table.setItem(cust_list_i, 10, datetime_created)

            self.setup_cust_list_table_act_panel_conn(value=cust_list_v)
            pass
        pass
    def setup_cust_list_table_act_panel_conn(self, value):
        self.edit_cust_button.clicked.connect(lambda _, value=value: self.on_edit_cust_button_clicked(value))
        self.view_cust_button.clicked.connect(lambda _, value=value: self.on_view_cust_button_clicked(value))
        self.delete_cust_button.clicked.connect(lambda _, value=value: self.on_delete_cust_button_clicked(value))

    def on_text_filter_button_clicked(self):
        self.model.page_number = 1
        self.view.cust_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

        self.populate_cust_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number) 
        pass
    def on_sync_ui_button_clicked(self):
        self.start_sync_ui()

        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass

    def start_sync_ui(self):
        self.model.init_cust_list_page_entry()
        self.view.cust_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.populate_cust_list_table()
    
    def on_import_cust_button_clicked(self):
        try:
            self.cust_csv_file, _ = QFileDialog.getOpenFileName(self.view, 'Open CSV', qss.csv_file_path, 'CSV File (*.csv)')
            self.cust_csv_df = pd.read_csv(self.cust_csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

            if self.cust_csv_file:
                self.model.prog_total_data_value = len(self.cust_csv_df)
                self.model.prog_remaining_data_value = len(self.cust_csv_df)

                self.model.setup_progress_panel(window_title=f"{'percentage'}", progress_type='cust_import')
                self.model.import_cust_entry(data_frame=self.cust_csv_df)
                self.setup_cust_import_thread_conn()
                self.model.progress_dialog.exec()

                if self.model.prog_remaining_data_value > 0 and self.model.progress_dialog.close():
                    self.model.cust_import_thread.stop()

                    self.model.init_progress_data_entry()

                    QMessageBox.critical(self.view, 'Cancelled', 'Import has been cancelled')
                    self.on_sync_ui_button_clicked()

            pass
        except Exception as e:
            self.cust_csv_file = ''
        pass
    def setup_cust_import_thread_conn(self):
        self.model.cust_import_thread.update_signal.connect(self.on_cust_import_thread_update_signal)
        self.model.cust_import_thread.finished_signal.connect(self.on_cust_import_thread_finished_signal)
        self.model.cust_import_thread.invalid_signal.connect(self.on_cust_import_thread_invalid_signal)
        pass
    def on_cust_import_thread_update_signal(self):
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
    def on_cust_import_thread_finished_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.information(self.view, 'Success', 'All cust has been imported')
        self.on_sync_ui_button_clicked()
        pass
    def on_cust_import_thread_invalid_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.critical(self.view, 'Error', 'Invalid CSV file.')
        self.on_sync_ui_button_clicked()
        pass

    def on_add_cust_button_clicked(self):
        self.model.setup_manage_cust_panel(window_title='Add cust')
        self.populate_manage_cust_combo_box_field()
        self.setup_manage_cust_panel_conn(conn_type='add_cust')

        self.model.manage_cust_dialog.exec()
        pass
    def on_edit_cust_button_clicked(self, value):
        self.model.assign_selected_cust_data_entry(value)
        self.model.setup_manage_cust_panel(window_title=f"Edit {self.model.sel_cust_name_value}")
        self.populate_manage_cust_combo_box_field()

        self.model.cust_name_field.setText(self.model.sel_cust_name_value)
        self.model.cust_address_field.setText(self.model.sel_cust_address_value)
        self.model.cust_barrio_field.setCurrentText(self.model.sel_cust_barrio_value)
        self.model.cust_town_field.setCurrentText(self.model.sel_cust_town_value)
        self.model.cust_phone_field.setText(self.model.sel_cust_phone_value)
        self.model.cust_age_field.setText(self.model.sel_cust_age_value)
        self.model.cust_gender_field.setCurrentText(self.model.sel_cust_gender_value)
        self.model.cust_marital_status_field.setCurrentText(self.model.sel_cust_marital_status_value)
        self.model.cust_points_field.setText(self.model.sel_cust_points_value)

        self.setup_manage_cust_panel_conn(conn_type='edit_cust')

        self.model.manage_cust_dialog.exec()
        pass
    def populate_manage_cust_combo_box_field(self):
        cust_barrio_data = schema.select_barrio()
        cust_town_data = schema.select_town()

        self.model.cust_barrio_field.clear()
        self.model.cust_town_field.clear()

        for cust_barrio in cust_barrio_data: self.model.cust_barrio_field.addItems(cust_barrio)
        for cust_town in cust_town_data: self.model.cust_town_field.addItems(cust_town)

        self.model.cust_gender_field.addItem('Male')
        self.model.cust_gender_field.addItem('Female')
        self.model.cust_marital_status_field.addItem('Single')
        self.model.cust_marital_status_field.addItem('Married')
        self.model.cust_marital_status_field.addItem('Separated')
        self.model.cust_marital_status_field.addItem('Widowed')

        pass
    def setup_manage_cust_panel_conn(self, conn_type):
        self.model.manage_cust_save_button.clicked.connect(lambda: self.on_manage_cust_save_button_clicked(action=conn_type))
        self.model.manage_cust_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.manage_cust_dialog))
        pass
    def on_manage_cust_save_button_clicked(self, action):
        cust_name = self.model.cust_name_field.text()
        cust_address = self.model.cust_address_field.text()
        cust_barrio = self.model.cust_barrio_field.currentText()
        cust_town = self.model.cust_town_field.currentText()
        cust_phone = self.model.cust_phone_field.text()
        cust_age = self.model.cust_age_field.text()
        cust_gender = self.model.cust_gender_field.currentText()
        cust_marital_status = self.model.cust_marital_status_field.currentText()
        cust_points = self.model.cust_points_field.text()


        if '' not in [cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status, cust_points]:
            if (cust_phone.isdigit() and cust_age.isdigit() and cust_points.replace('.', '', 1).isdigit()):
                
                if action == 'add_cust':
                    self.model.save_new_cust_entry()
                    self.model.init_selected_cust_data_entry()

                    QMessageBox.information(self.view, 'Success', 'New cust has been added.')
                    pass
                elif action == 'edit_cust':
                    self.model.save_edit_cust_entry()
                    self.model.init_selected_cust_data_entry()

                    QMessageBox.information(self.view, 'Success', 'Customer has been edited.')
                    pass
                self.on_sync_ui_button_clicked()
                pass
            else:
                QMessageBox.critical(self.model.manage_cust_dialog, 'Error', 'Invalid numerical input.')
                pass
        else:
            self.set_label_required_field_indicator(cust_name, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status, cust_points)

            QMessageBox.critical(self.model.manage_cust_dialog, 'Error', 'Please fill out the required field.')
            pass
        pass
    def set_label_required_field_indicator(self, cust_name, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status, cust_points):
        self.model.cust_name_label.setText(f"Name {qss.required_label}") if cust_name == '' else self.model.cust_name_label.setText(f"Name")
        self.model.cust_barrio_label.setText(f"Barrio {qss.required_label}") if cust_barrio == '' else self.model.cust_barrio_label.setText(f"Barrio")
        self.model.cust_town_label.setText(f"Town {qss.required_label}") if cust_town == '' else self.model.cust_town_label.setText(f"Town")
        self.model.cust_phone_label.setText(f"Phone {qss.required_label}") if cust_phone == '' else self.model.cust_phone_label.setText(f"Phone")
        self.model.cust_age_label.setText(f"Age {qss.required_label}") if cust_age == '' else self.model.cust_age_label.setText(f"Age")
        self.model.cust_gender_label.setText(f"Gender {qss.required_label}") if cust_gender == '' else self.model.cust_gender_label.setText(f"Gender")
        self.model.cust_marital_status_label.setText(f"Marital status {qss.required_label}") if cust_marital_status == '' else self.model.cust_marital_status_label.setText(f"Marital status")
        self.model.cust_points_label.setText(f"Points {qss.required_label}") if cust_points == '' else self.model.cust_points_label.setText(f"Points")
    
    def on_view_cust_button_clicked(self, value):
        self.model.assign_selected_cust_data_entry(value)

        self.model.setup_view_cust_panel()

        self.setup_view_cust_conn()

        self.model.view_dialog.exec()
        pass
    def setup_view_cust_conn(self):
        self.model.view_form_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.view_dialog))

    def on_delete_cust_button_clicked(self, value):
        self.model.assign_selected_cust_data_entry(value)

        confirm = QMessageBox.warning(self.view, 'Confirm', f"Delete {self.model.sel_cust_name_value}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_cust_data(cust_id=self.model.sel_cust_id_value, reward_id=self.model.sel_reward_id_value)

            self.model.init_selected_cust_data_entry()

            QMessageBox.information(self.view, 'Success', 'Customer has been deleted.')

            self.on_sync_ui_button_clicked()
            pass
        else:
            self.model.init_selected_cust_data_entry()
            return
        pass
    
    def on_close_button_clicked(self, widget: QWidget):
        widget.close()

        self.model.init_selected_cust_data_entry()
        pass

    def on_cust_list_pag_button_clicked(self, action):
        print('cust_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.page_number > 1:
                self.model.page_number -= 1
                self.view.cust_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_cust_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        elif action == 'go_next':
            self.model.page_number += 1
            self.view.cust_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_cust_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        pass

    pass

class MyCustWindow(MyGroupBox):
    def __init__(self, name): # NOTE: 'name' param is for the current user (cashier, admin, dev) name
        super().__init__(object_name='MyCustWindow')

        self.model = MyCustModel(name=name)
        self.view = MyCustView(self.model)
        self.controller = MyCustController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.show()


# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    cust_window = MyCustWindow(name='test-name')

    cust_window.run()
    app.exec()