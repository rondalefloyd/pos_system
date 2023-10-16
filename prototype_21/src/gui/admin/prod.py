
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
from src.sql.admin.prod import *
from src.widget.admin.admin import *
from templates.qss.qss_config import QSSConfig

schema = MyProdSchema()
qss = QSSConfig()

class MyProdModel: # NOTE: entries
    def __init__(self, name):
        # NOTE: global variables
        self.gdrive_path = 'G:' + f"/My Drive/"
        self.user_name = name

        self.init_selected_prod_data_entry()
        self.init_progress_data_entry()
        self.init_prod_list_page_entry()

    def init_prod_list_page_entry(self):
        self.page_number = 1
        self.total_page_number = schema.count_prod_list_total_pages()

    def init_selected_prod_data_entry(self):
        self.sel_prod_name_value = None
        self.sel_prod_address_value = None
        self.sel_prod_barrio_value = None
        self.sel_prod_town_value = None
        self.sel_prod_phone_value = None
        self.sel_prod_age_value = None
        self.sel_prod_gender_value = None
        self.sel_prod_marital_status_value = None
        self.sel_prod_points_value = None

        self.sel_datetime_created_value = None
        self.sel_prod_id_value = None
        self.sel_reward_id_value = None
        pass
    def assign_selected_prod_data_entry(self, value):
        self.sel_prod_name_value = str(value[0])
        self.sel_prod_address_value = str(value[1])
        self.sel_prod_barrio_value = str(value[2])
        self.sel_prod_town_value = str(value[3])
        self.sel_prod_phone_value = str(value[4])
        self.sel_prod_age_value = str(value[5])
        self.sel_prod_gender_value = str(value[6])
        self.sel_prod_marital_status_value = str(value[7])
        self.sel_prod_points_value = str(value[8])

        self.sel_datetime_created_value = str(value[9])
        self.sel_prod_id_value = value[10]
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

    def import_prod_entry(self, data_frame):
        self.prod_import_thread = MyDataImportThread(data_name='prod', data_frame=data_frame) # NOTE: ths is QThread for data import
        self.prod_import_thread.start()

    def setup_manage_prod_panel(self, window_title):
        self.manage_prod_dialog = MyDialog(window_title=window_title)
        self.manage_prod_layout = MyGridLayout()

        self.prod_name_label = MyLabel(text='Name')
        self.prod_address_label = MyLabel(text='Address')
        self.prod_barrio_label = MyLabel(text='Barrio')
        self.prod_town_label = MyLabel(text='Town')
        self.prod_phone_label = MyLabel(text='Phone')
        self.prod_age_label = MyLabel(text='Age')
        self.prod_gender_label = MyLabel(text='Gender')
        self.prod_marital_status_label = MyLabel(text='Marital status')
        self.prod_points_label = MyLabel(text='Points')
        
        self.prod_name_field = MyLineEdit(object_name='prod_name_field')
        self.prod_address_field = MyLineEdit(object_name='prod_address_field')
        self.prod_barrio_field = MyComboBox(object_name='prod_barrio_field')
        self.prod_town_field = MyComboBox(object_name='prod_town_field')
        self.prod_phone_field = MyLineEdit(object_name='prod_phone_field')
        self.prod_age_field = MyLineEdit(object_name='prod_age_field')
        self.prod_gender_field = MyComboBox(object_name='prod_gender_field')
        self.prod_marital_status_field = MyComboBox(object_name='prod_marital_status_field')
        self.prod_points_field = MyLineEdit(object_name='prod_points_field')

        self.prod_form_box = MyGroupBox()
        self.prod_form_layout = MyFormLayout()
        self.prod_form_layout.insertRow(0,self.prod_name_label)
        self.prod_form_layout.insertRow(2,self.prod_address_label)
        self.prod_form_layout.insertRow(4,self.prod_barrio_label)
        self.prod_form_layout.insertRow(6,self.prod_town_label)
        self.prod_form_layout.insertRow(8,self.prod_phone_label)
        self.prod_form_layout.insertRow(10,self.prod_age_label)
        self.prod_form_layout.insertRow(12,self.prod_gender_label)
        self.prod_form_layout.insertRow(14,self.prod_marital_status_label)
        self.prod_form_layout.insertRow(16,self.prod_points_label)

        self.prod_form_layout.insertRow(1,self.prod_name_field)
        self.prod_form_layout.insertRow(3,self.prod_address_field)
        self.prod_form_layout.insertRow(5,self.prod_barrio_field)
        self.prod_form_layout.insertRow(7,self.prod_town_field)
        self.prod_form_layout.insertRow(9,self.prod_phone_field)
        self.prod_form_layout.insertRow(11,self.prod_age_field)
        self.prod_form_layout.insertRow(13,self.prod_gender_field)
        self.prod_form_layout.insertRow(15,self.prod_marital_status_field)
        self.prod_form_layout.insertRow(17,self.prod_points_field)
        self.prod_form_box.setLayout(self.prod_form_layout)
        self.prod_form_scra = MyScrollArea()
        self.prod_form_scra.setWidget(self.prod_form_box)

        self.manage_prod_save_button = MyPushButton(text='Save')
        self.manage_prod_close_button = MyPushButton(text='Close')
        self.manage_prod_act_box = MyGroupBox()
        self.manage_prod_act_layout = MyHBoxLayout(object_name='prod_act_layout')
        self.manage_prod_act_layout.addWidget(self.manage_prod_save_button)
        self.manage_prod_act_layout.addWidget(self.manage_prod_close_button)
        self.manage_prod_act_box.setLayout(self.manage_prod_act_layout)

        self.manage_prod_layout.addWidget(self.prod_form_scra,0,0)
        self.manage_prod_layout.addWidget(self.manage_prod_act_box,1,0,Qt.AlignmentFlag.AlignRight)
        self.manage_prod_dialog.setLayout(self.manage_prod_layout)
        pass
    def save_new_prod_entry(self):
        prod_name = self.prod_name_field.text()
        prod_address = self.prod_address_field.text()
        prod_barrio = self.prod_barrio_field.currentText()
        prod_town = self.prod_town_field.currentText()
        prod_phone = self.prod_phone_field.text()
        prod_age = self.prod_age_field.text()
        prod_gender = self.prod_gender_field.currentText()
        prod_marital_status = self.prod_marital_status_field.currentText()
        prod_points = self.prod_points_field.text()

        schema.add_new_prod(
                prod_name=prod_name,
                prod_address=prod_address,
                prod_barrio=prod_barrio,
                prod_town=prod_town,
                prod_phone=prod_phone,
                prod_age=prod_age,
                prod_gender=prod_gender,
                prod_marital_status=prod_marital_status,
                prod_points=prod_points,
            )

        self.manage_prod_dialog.close()
        pass
    def save_edit_prod_entry(self):
        prod_name = self.prod_name_field.text()
        prod_address = self.prod_address_field.text()
        prod_barrio = self.prod_barrio_field.currentText()
        prod_town = self.prod_town_field.currentText()
        prod_phone = self.prod_phone_field.text()
        prod_age = self.prod_age_field.text()
        prod_gender = self.prod_gender_field.currentText()
        prod_marital_status = self.prod_marital_status_field.currentText()
        prod_points = self.prod_points_field.text()
        prod_id = self.sel_prod_id_value
        reward_id = self.sel_reward_id_value

        schema.edit_selected_prod(
                prod_name=prod_name,
                prod_address=prod_address,
                prod_barrio=prod_barrio,
                prod_town=prod_town,
                prod_phone=prod_phone,
                prod_age=prod_age,
                prod_gender=prod_gender,
                prod_marital_status=prod_marital_status,
                prod_points=prod_points,
                prod_id=prod_id,
                reward_id=reward_id,
            )

        self.sel_prod_id_value = 0
        self.manage_prod_dialog.close()
        pass
    
    def setup_view_prod_panel(self):
        self.view_dialog = MyDialog(window_title=f"{self.sel_prod_name_value}")
        self.view_layout = MyGridLayout()

        self.prod_name_info_label = MyLabel(text=f"{self.sel_prod_name_value}")
        self.prod_address_info_label = MyLabel(text=f"{self.sel_prod_address_value}")
        self.prod_barrio_info_label = MyLabel(text=f"{self.sel_prod_barrio_value}")
        self.prod_town_info_label = MyLabel(text=f"{self.sel_prod_town_value}")
        self.prod_phone_info_label = MyLabel(text=f"{self.sel_prod_phone_value}")
        self.prod_age_info_label = MyLabel(text=f"{self.sel_prod_age_value}")
        self.prod_gender_info_label = MyLabel(text=f"{self.sel_prod_gender_value}")
        self.prod_marital_status_info_label = MyLabel(text=f"{self.sel_prod_marital_status_value}")
        self.prod_points_info_label = MyLabel(text=f"{self.sel_prod_points_value}")
        self.datetime_created_info_label = MyLabel(text=f"{self.sel_datetime_created_value}")
        self.view_form_box = MyGroupBox()
        self.view_form_layout = MyFormLayout()
        self.view_form_layout.addRow('Name', self.prod_name_info_label)
        self.view_form_layout.addRow('Address', self.prod_address_info_label)
        self.view_form_layout.addRow('Barrio', self.prod_barrio_info_label)
        self.view_form_layout.addRow('Town', self.prod_town_info_label)
        self.view_form_layout.addRow('Phone', self.prod_phone_info_label)
        self.view_form_layout.addRow('Age', self.prod_age_info_label)
        self.view_form_layout.addRow('Gender', self.prod_gender_info_label)
        self.view_form_layout.addRow('Marital status', self.prod_marital_status_info_label)
        self.view_form_layout.addRow('Points', self.prod_points_info_label)
        self.view_form_layout.addRow('Date/Time created', self.datetime_created_info_label)
        self.view_form_box.setLayout(self.view_form_layout)
        self.view_form_scra = MyScrollArea()
        self.view_form_scra.setWidget(self.view_form_box)

        self.view_form_close_button = MyPushButton(text='Close')

        self.view_layout.addWidget(self.view_form_scra,0,0)
        self.view_layout.addWidget(self.view_form_close_button,1,0,Qt.AlignmentFlag.AlignRight)
        self.view_dialog.setLayout(self.view_layout)
    
    pass
class MyProdView(MyGroupBox): # NOTE: layout
    def __init__(self, model: MyProdModel):
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
        self.import_prod_button = MyPushButton(text='Import')
        self.add_prod_button = MyPushButton(text='Add')
        self.interactive_act_box = MyGroupBox()
        self.interactive_act_layout = MyHBoxLayout()
        self.interactive_act_layout.addWidget(self.sync_ui_button)
        self.interactive_act_layout.addWidget(self.import_prod_button)
        self.interactive_act_layout.addWidget(self.add_prod_button)
        self.interactive_act_box.setLayout(self.interactive_act_layout)

        self.prod_list_table = MyTableWidget(object_name='prod_list_table')
        self.prod_list_prev_button = MyPushButton(text='Prev')
        self.prod_list_page_label = MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.prod_list_next_button = MyPushButton(text='Next')
        self.prod_list_pag_box = MyGroupBox()
        self.prod_list_pag_layout = MyHBoxLayout(object_name='prod_list_pag_layout')
        self.prod_list_pag_layout.addWidget(self.prod_list_prev_button)
        self.prod_list_pag_layout.addWidget(self.prod_list_page_label)
        self.prod_list_pag_layout.addWidget(self.prod_list_next_button)
        self.prod_list_pag_box.setLayout(self.prod_list_pag_layout)
        self.prod_list_box = MyGroupBox()
        self.prod_list_layout = MyGridLayout()
        self.prod_list_layout.addWidget(self.prod_list_table,0,0)
        self.prod_list_layout.addWidget(self.prod_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.prod_list_box.setLayout(self.prod_list_layout)
        self.prod_list_tab = MyTabWidget()
        self.prod_list_tab.addTab(self.prod_list_box, 'Overview')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.interactive_act_box,0,1)
        self.panel_a_layout.addWidget(self.prod_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    pass 
class MyProdController: # NOTE: connections, setting attributes
    def __init__(self, model: MyProdModel, view: MyProdView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_prod_list_table()

    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.view.import_prod_button.clicked.connect(self.on_import_prod_button_clicked)
        self.view.add_prod_button.clicked.connect(self.on_add_prod_button_clicked)
        self.view.prod_list_prev_button.clicked.connect(lambda: self.on_prod_list_pag_button_clicked(action='go_prev'))
        self.view.prod_list_next_button.clicked.connect(lambda: self.on_prod_list_pag_button_clicked(action='go_next'))
        pass

    def populate_prod_list_table(self, text_filter='', page_number=1):
        prod_list = schema.list_all_prod_col(text_filter=text_filter, page_number=page_number)

        self.view.prod_list_page_label.setText(f"Page {page_number}/{self.model.total_page_number}")

        self.view.prod_list_prev_button.setEnabled(page_number > 1)
        self.view.prod_list_next_button.setEnabled(len(prod_list) == 30)

        self.view.prod_list_table.setRowCount(len(prod_list))

        for prod_list_i, prod_list_v in enumerate(prod_list):
            self.edit_prod_button = MyPushButton(text='Edit')
            self.view_prod_button = MyPushButton(text='View')
            self.delete_prod_button = MyPushButton(text='Delete')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.edit_prod_button)
            table_act_laoyut.addWidget(self.view_prod_button)
            table_act_laoyut.addWidget(self.delete_prod_button)
            table_act_panel.setLayout(table_act_laoyut)
            prod_name = QTableWidgetItem(f"{prod_list_v[0]}")
            prod_address = QTableWidgetItem(f"{prod_list_v[1]}")
            prod_barrio = QTableWidgetItem(f"{prod_list_v[2]}")
            prod_town = QTableWidgetItem(f"{prod_list_v[3]}")
            prod_phone = QTableWidgetItem(f"{prod_list_v[4]}")
            prod_age = QTableWidgetItem(f"{prod_list_v[5]}")
            prod_gender = QTableWidgetItem(f"{prod_list_v[6]}")
            prod_marital_status = QTableWidgetItem(f"{prod_list_v[7]}")
            prod_points = QTableWidgetItem(f"{prod_list_v[8]}")
            datetime_created = QTableWidgetItem(f"{prod_list_v[9]}")

            self.view.prod_list_table.setCellWidget(prod_list_i, 0, table_act_panel)
            self.view.prod_list_table.setItem(prod_list_i, 1, prod_name)
            self.view.prod_list_table.setItem(prod_list_i, 2, prod_address)
            self.view.prod_list_table.setItem(prod_list_i, 3, prod_barrio)
            self.view.prod_list_table.setItem(prod_list_i, 4, prod_town)
            self.view.prod_list_table.setItem(prod_list_i, 5, prod_phone)
            self.view.prod_list_table.setItem(prod_list_i, 6, prod_age)
            self.view.prod_list_table.setItem(prod_list_i, 7, prod_gender)
            self.view.prod_list_table.setItem(prod_list_i, 8, prod_marital_status)
            self.view.prod_list_table.setItem(prod_list_i, 9, prod_points)
            self.view.prod_list_table.setItem(prod_list_i, 10, datetime_created)

            self.setup_prod_list_table_act_panel_conn(value=prod_list_v)
            pass
        pass
    def setup_prod_list_table_act_panel_conn(self, value):
        self.edit_prod_button.clicked.connect(lambda _, value=value: self.on_edit_prod_button_clicked(value))
        self.view_prod_button.clicked.connect(lambda _, value=value: self.on_view_prod_button_clicked(value))
        self.delete_prod_button.clicked.connect(lambda _, value=value: self.on_delete_prod_button_clicked(value))

    def on_text_filter_button_clicked(self):
        self.model.page_number = 1
        self.view.prod_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

        self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number) 
        pass
    def on_sync_ui_button_clicked(self):
        self.model.init_prod_list_page_entry()
        self.view.prod_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.populate_prod_list_table()

        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass
    
    def on_import_prod_button_clicked(self):
        try:
            self.prod_csv_file, _ = QFileDialog.getOpenFileName(self.view, 'Open CSV', qss.csv_file_path, 'CSV File (*.csv)')
            self.prod_csv_df = pd.read_csv(self.prod_csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

            if self.prod_csv_file:
                self.model.prog_total_data_value = len(self.prod_csv_df)
                self.model.prog_remaining_data_value = len(self.prod_csv_df)

                self.model.setup_progress_panel(window_title=f"{'percentage'}", progress_type='prod_import')
                self.model.import_prod_entry(data_frame=self.prod_csv_df)
                self.setup_prod_import_thread_conn()
                self.model.progress_dialog.exec()

                if self.model.prog_remaining_data_value > 0 and self.model.progress_dialog.close():
                    self.model.prod_import_thread.stop()

                    self.model.init_progress_data_entry()

                    QMessageBox.critical(self.view, 'Cancelled', 'Import has been cancelled')
                    self.on_sync_ui_button_clicked()

            pass
        except Exception as e:
            self.prod_csv_file = ''
        pass
    def setup_prod_import_thread_conn(self):
        self.model.prod_import_thread.update_signal.connect(self.on_prod_import_thread_update_signal)
        self.model.prod_import_thread.finished_signal.connect(self.on_prod_import_thread_finished_signal)
        self.model.prod_import_thread.invalid_signal.connect(self.on_prod_import_thread_invalid_signal)
        pass
    def on_prod_import_thread_update_signal(self):
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
    def on_prod_import_thread_finished_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.information(self.view, 'Success', 'All prod has been imported')
        self.on_sync_ui_button_clicked()
        pass
    def on_prod_import_thread_invalid_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.critical(self.view, 'Error', 'Invalid CSV file.')
        self.on_sync_ui_button_clicked()
        pass

    def on_add_prod_button_clicked(self):
        self.model.setup_manage_prod_panel(window_title='Add prod')
        self.populate_manage_prod_combo_box_field()
        self.setup_manage_prod_panel_conn(conn_type='add_prod')

        self.model.manage_prod_dialog.exec()
        pass
    def on_edit_prod_button_clicked(self, value):
        self.model.assign_selected_prod_data_entry(value)
        self.model.setup_manage_prod_panel(window_title=f"Edit {self.model.sel_prod_name_value}")
        self.populate_manage_prod_combo_box_field()

        self.model.prod_name_field.setText(self.model.sel_prod_name_value)
        self.model.prod_address_field.setText(self.model.sel_prod_address_value)
        self.model.prod_barrio_field.setCurrentText(self.model.sel_prod_barrio_value)
        self.model.prod_town_field.setCurrentText(self.model.sel_prod_town_value)
        self.model.prod_phone_field.setText(self.model.sel_prod_phone_value)
        self.model.prod_age_field.setText(self.model.sel_prod_age_value)
        self.model.prod_gender_field.setCurrentText(self.model.sel_prod_gender_value)
        self.model.prod_marital_status_field.setCurrentText(self.model.sel_prod_marital_status_value)
        self.model.prod_points_field.setText(self.model.sel_prod_points_value)

        self.setup_manage_prod_panel_conn(conn_type='edit_prod')

        self.model.manage_prod_dialog.exec()
        pass
    def populate_manage_prod_combo_box_field(self):
        prod_barrio_data = schema.list_barrio_col()
        prod_town_data = schema.list_town_col()

        self.model.prod_barrio_field.clear()
        self.model.prod_town_field.clear()

        for prod_barrio in prod_barrio_data: self.model.prod_barrio_field.addItems(prod_barrio)
        for prod_town in prod_town_data: self.model.prod_town_field.addItems(prod_town)

        self.model.prod_gender_field.addItem('Male')
        self.model.prod_gender_field.addItem('Female')
        self.model.prod_marital_status_field.addItem('Single')
        self.model.prod_marital_status_field.addItem('Married')
        self.model.prod_marital_status_field.addItem('Separated')
        self.model.prod_marital_status_field.addItem('Widowed')

        pass
    def setup_manage_prod_panel_conn(self, conn_type):
        self.model.manage_prod_save_button.clicked.connect(lambda: self.on_manage_prod_save_button_clicked(action=conn_type))
        self.model.manage_prod_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.manage_prod_dialog))
        pass
    def on_manage_prod_save_button_clicked(self, action):
        prod_name = self.model.prod_name_field.text()
        prod_address = self.model.prod_address_field.text()
        prod_barrio = self.model.prod_barrio_field.currentText()
        prod_town = self.model.prod_town_field.currentText()
        prod_phone = self.model.prod_phone_field.text()
        prod_age = self.model.prod_age_field.text()
        prod_gender = self.model.prod_gender_field.currentText()
        prod_marital_status = self.model.prod_marital_status_field.currentText()
        prod_points = self.model.prod_points_field.text()


        if '' not in [prod_name, prod_address, prod_barrio, prod_town, prod_phone, prod_age, prod_gender, prod_marital_status, prod_points]:
            if (prod_phone.isdigit() and prod_age.isdigit() and prod_points.replace('.', '', 1).isdigit()):
                
                if action == 'add_prod':
                    self.model.save_new_prod_entry()
                    self.model.init_selected_prod_data_entry()

                    QMessageBox.information(self.view, 'Success', 'New prod has been added.')
                    pass
                elif action == 'edit_prod':
                    self.model.save_edit_prod_entry()
                    self.model.init_selected_prod_data_entry()

                    QMessageBox.information(self.view, 'Success', 'Prodomer has been edited.')
                    pass
                self.on_sync_ui_button_clicked()
                pass
            else:
                QMessageBox.critical(self.model.manage_prod_dialog, 'Error', 'Invalid numerical input.')
                pass
        else:
            self.set_label_required_field_indicator(prod_name, prod_barrio, prod_town, prod_phone, prod_age, prod_gender, prod_marital_status, prod_points)

            QMessageBox.critical(self.model.manage_prod_dialog, 'Error', 'Please fill out the required field.')
            pass
        pass
    def set_label_required_field_indicator(self, prod_name, prod_barrio, prod_town, prod_phone, prod_age, prod_gender, prod_marital_status, prod_points):
        self.model.prod_name_label.setText(f"Name {qss.required_label}") if prod_name == '' else self.model.prod_name_label.setText(f"Name")
        self.model.prod_barrio_label.setText(f"Barrio {qss.required_label}") if prod_barrio == '' else self.model.prod_barrio_label.setText(f"Barrio")
        self.model.prod_town_label.setText(f"Town {qss.required_label}") if prod_town == '' else self.model.prod_town_label.setText(f"Town")
        self.model.prod_phone_label.setText(f"Phone {qss.required_label}") if prod_phone == '' else self.model.prod_phone_label.setText(f"Phone")
        self.model.prod_age_label.setText(f"Age {qss.required_label}") if prod_age == '' else self.model.prod_age_label.setText(f"Age")
        self.model.prod_gender_label.setText(f"Gender {qss.required_label}") if prod_gender == '' else self.model.prod_gender_label.setText(f"Gender")
        self.model.prod_marital_status_label.setText(f"Marital status {qss.required_label}") if prod_marital_status == '' else self.model.prod_marital_status_label.setText(f"Marital status")
        self.model.prod_points_label.setText(f"Points {qss.required_label}") if prod_points == '' else self.model.prod_points_label.setText(f"Points")
    
    def on_view_prod_button_clicked(self, value):
        self.model.assign_selected_prod_data_entry(value)

        self.model.setup_view_prod_panel()

        self.setup_view_prod_conn()

        self.model.view_dialog.exec()
        pass
    def setup_view_prod_conn(self):
        self.model.view_form_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.view_dialog))

    def on_delete_prod_button_clicked(self, value):
        self.model.assign_selected_prod_data_entry(value)

        confirm = QMessageBox.warning(self.view, 'Confirm', f"Delete {self.model.sel_prod_name_value}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_prod(prod_id=self.model.sel_prod_id_value, reward_id=self.model.sel_reward_id_value)

            self.model.init_selected_prod_data_entry()

            QMessageBox.information(self.view, 'Success', 'Prodomer has been deleted.')

            self.on_sync_ui_button_clicked()
            pass
        else:
            self.model.init_selected_prod_data_entry()
            return
        pass
    
    def on_close_button_clicked(self, widget: QWidget):
        widget.close()

        self.model.init_selected_prod_data_entry()
        pass

    def on_prod_list_pag_button_clicked(self, action):
        print('prod_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.page_number > 1:
                self.model.page_number -= 1
                self.view.prod_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        elif action == 'go_next':
            self.model.page_number += 1
            self.view.prod_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_prod_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        pass

    pass

class MyProdWindow(MyGroupBox):
    def __init__(self, name): # NOTE: 'name' param is for the current user (cashier, admin, dev) name
        super().__init__(object_name='MyProdWindow')

        self.model = MyProdModel(name=name)
        self.view = MyProdView(self.model)
        self.controller = MyProdController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.show()


# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    prod_window = MyProdWindow(name='test-name')

    prod_window.run()
    app.exec()