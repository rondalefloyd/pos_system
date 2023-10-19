
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
from src.sql.admin.user import *
from src.widget.admin.admin import *
from templates.qss.qss_config import QSSConfig

schema = MyUserSchema()
qss = QSSConfig()

class MyUserModel: # NOTE: entries
    def __init__(self, name):
        # NOTE: global variables
        self.gdrive_path = 'G:' + f"/My Drive/"
        self.user_name = name

        self.init_selected_user_data_entry()
        self.init_progress_data_entry()
        self.init_user_list_page_entry()

    def init_user_list_page_entry(self):
        self.page_number = 1
        self.total_page_number = schema.count_user_list_total_pages()

    def init_selected_user_data_entry(self):
        self.sel_user_name_value = None
        self.sel_user_password_value = None
        self.sel_user_phone_value = None
        self.sel_datetime_created_value = None
        self.sel_user_id_value = None
        pass
    def assign_selected_user_data_entry(self, value):
        self.sel_user_name_value = str(value[0])
        self.sel_user_password_value = str(value[1])
        self.sel_user_phone_value = str(value[2])
        self.sel_datetime_created_value = str(value[3])
        self.sel_user_id_value = value[4]

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

    def import_user_entry(self, data_frame):
        self.user_import_thread = MyDataImportThread(data_name='user', data_frame=data_frame) # NOTE: ths is QThread for data import
        self.user_import_thread.start()

    def setup_manage_user_panel(self, window_title):
        self.manage_user_dialog = MyDialog(window_title=window_title)
        self.manage_user_layout = MyGridLayout()

        self.user_name_label = MyLabel(text='Name')
        self.user_password_label = MyLabel(text='Password')
        self.user_phone_label = MyLabel(text='Phone')
        
        self.user_name_field = MyLineEdit(object_name='user_name_field')
        self.user_password_field = MyLineEdit(object_name='user_password_field')
        self.user_phone_field = MyLineEdit(object_name='user_phone_field')

        self.user_form_box = MyGroupBox()
        self.user_form_layout = MyFormLayout()
        self.user_form_layout.insertRow(0,self.user_name_label)
        self.user_form_layout.insertRow(2,self.user_password_label)
        self.user_form_layout.insertRow(4,self.user_phone_label)
        self.user_form_layout.insertRow(1,self.user_name_field)
        self.user_form_layout.insertRow(3,self.user_password_field)
        self.user_form_layout.insertRow(5,self.user_phone_field)
        self.user_form_box.setLayout(self.user_form_layout)
        self.user_form_scra = MyScrollArea()
        self.user_form_scra.setWidget(self.user_form_box)

        self.manage_user_save_button = MyPushButton(text='Save')
        self.manage_user_close_button = MyPushButton(text='Close')
        self.manage_user_act_box = MyGroupBox()
        self.manage_user_act_layout = MyHBoxLayout(object_name='user_act_layout')
        self.manage_user_act_layout.addWidget(self.manage_user_save_button)
        self.manage_user_act_layout.addWidget(self.manage_user_close_button)
        self.manage_user_act_box.setLayout(self.manage_user_act_layout)

        self.manage_user_layout.addWidget(self.user_form_scra,0,0)
        self.manage_user_layout.addWidget(self.manage_user_act_box,1,0,Qt.AlignmentFlag.AlignRight)
        self.manage_user_dialog.setLayout(self.manage_user_layout)
        pass
    def save_new_user_entry(self):
        user_name = self.user_name_field.text()
        user_password = self.user_password_field.text()
        user_phone = self.user_phone_field.text()

        schema.add_new_user(
                user_name=user_name,
                user_password=user_password,
                user_phone=user_phone
            )

        self.manage_user_dialog.close()
        pass
    def save_edit_user_entry(self):
        user_name = self.user_name_field.text()
        user_password = self.user_password_field.text()
        user_phone = self.user_phone_field.text()
        user_id = self.sel_user_id_value

        schema.edit_selected_user(
                user_name=user_name,
                user_password=user_password,
                user_phone=user_phone,
                user_id=user_id
            )

        self.sel_user_id_value = 0
        self.manage_user_dialog.close()
        pass
    
    def setup_view_user_panel(self):
        self.view_dialog = MyDialog(window_title=f"{self.sel_user_name_value}")
        self.view_layout = MyGridLayout()

        self.user_name_info_label = MyLabel(text=f"{self.sel_user_name_value}")
        self.user_password_info_label = MyLabel(text=f"{self.sel_user_password_value}")
        self.user_phone_info_label = MyLabel(text=f"{self.sel_user_phone_value}")
        self.datetime_created_info_label = MyLabel(text=f"{self.sel_datetime_created_value}")
        self.view_form_box = MyGroupBox()
        self.view_form_layout = MyFormLayout()
        self.view_form_layout.addRow('Name', self.user_name_info_label)
        self.view_form_layout.addRow('Password', self.user_password_info_label)
        self.view_form_layout.addRow('Phone', self.user_phone_info_label)
        self.view_form_layout.addRow('Date/Time created', self.datetime_created_info_label)
        self.view_form_box.setLayout(self.view_form_layout)
        self.view_form_scra = MyScrollArea()
        self.view_form_scra.setWidget(self.view_form_box)

        self.view_form_close_button = MyPushButton(text='Close')

        self.view_layout.addWidget(self.view_form_scra,0,0)
        self.view_layout.addWidget(self.view_form_close_button,1,0,Qt.AlignmentFlag.AlignRight)
        self.view_dialog.setLayout(self.view_layout)
    
    pass
class MyUserView(MyGroupBox): # NOTE: layout
    def __init__(self, model: MyUserModel):
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
        self.import_user_button = MyPushButton(text='Import')
        self.add_user_button = MyPushButton(text='Add')
        self.interactive_act_box = MyGroupBox()
        self.interactive_act_layout = MyHBoxLayout()
        self.interactive_act_layout.addWidget(self.sync_ui_button)
        self.interactive_act_layout.addWidget(self.import_user_button)
        self.interactive_act_layout.addWidget(self.add_user_button)
        self.interactive_act_box.setLayout(self.interactive_act_layout)

        self.user_list_table = MyTableWidget(object_name='user_list_table')
        self.user_list_prev_button = MyPushButton(text='Prev')
        self.user_list_page_label = MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.user_list_next_button = MyPushButton(text='Next')
        self.user_list_pag_box = MyGroupBox()
        self.user_list_pag_layout = MyHBoxLayout(object_name='user_list_pag_layout')
        self.user_list_pag_layout.addWidget(self.user_list_prev_button)
        self.user_list_pag_layout.addWidget(self.user_list_page_label)
        self.user_list_pag_layout.addWidget(self.user_list_next_button)
        self.user_list_pag_box.setLayout(self.user_list_pag_layout)
        self.user_list_box = MyGroupBox()
        self.user_list_layout = MyGridLayout()
        self.user_list_layout.addWidget(self.user_list_table,0,0)
        self.user_list_layout.addWidget(self.user_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.user_list_box.setLayout(self.user_list_layout)
        self.user_list_tab = MyTabWidget()
        self.user_list_tab.addTab(self.user_list_box, 'Overview')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.interactive_act_box,0,1)
        self.panel_a_layout.addWidget(self.user_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    pass 
class MyUserController: # NOTE: connections, setting attributes
    def __init__(self, model: MyUserModel, view: MyUserView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_user_list_table()

    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.view.import_user_button.clicked.connect(self.on_import_user_button_clicked)
        self.view.add_user_button.clicked.connect(self.on_add_user_button_clicked)
        self.view.user_list_prev_button.clicked.connect(lambda: self.on_user_list_pag_button_clicked(action='go_prev'))
        self.view.user_list_next_button.clicked.connect(lambda: self.on_user_list_pag_button_clicked(action='go_next'))
        pass

    def populate_user_list_table(self, text_filter='', page_number=1):
        user_list = schema.list_all_user_col(text_filter=text_filter, page_number=page_number)

        self.view.user_list_page_label.setText(f"Page {page_number}/{self.model.total_page_number}")

        self.view.user_list_prev_button.setEnabled(page_number > 1)
        self.view.user_list_next_button.setEnabled(len(user_list) == 30)

        self.view.user_list_table.setRowCount(len(user_list))

        for user_list_i, user_list_v in enumerate(user_list):
            self.edit_user_button = MyPushButton(text='Edit')
            self.view_user_button = MyPushButton(text='View')
            self.delete_user_button = MyPushButton(text='Delete')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.edit_user_button)
            table_act_laoyut.addWidget(self.view_user_button)
            table_act_laoyut.addWidget(self.delete_user_button)
            table_act_panel.setLayout(table_act_laoyut)
            user_name = QTableWidgetItem(f"{user_list_v[0]}")
            user_password = QTableWidgetItem(f"{user_list_v[1]}")
            user_phone = QTableWidgetItem(f"{user_list_v[2]}")
            datetime_created = QTableWidgetItem(f"{user_list_v[3]}")

            self.view.user_list_table.setCellWidget(user_list_i, 0, table_act_panel)
            self.view.user_list_table.setItem(user_list_i, 1, user_name)
            self.view.user_list_table.setItem(user_list_i, 2, user_password)
            self.view.user_list_table.setItem(user_list_i, 3, user_phone)
            self.view.user_list_table.setItem(user_list_i, 4, datetime_created)

            access_level = user_list_v[5]
            if access_level >= 2:
                self.delete_user_button.hide()

            self.setup_user_list_table_act_panel_conn(value=user_list_v)
            pass
        pass
    def setup_user_list_table_act_panel_conn(self, value):
        self.edit_user_button.clicked.connect(lambda _, value=value: self.on_edit_user_button_clicked(value))
        self.view_user_button.clicked.connect(lambda _, value=value: self.on_view_user_button_clicked(value))
        self.delete_user_button.clicked.connect(lambda _, value=value: self.on_delete_user_button_clicked(value))

    def on_text_filter_button_clicked(self):
        self.model.page_number = 1
        self.view.user_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

        self.populate_user_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number) 
        pass
    def on_sync_ui_button_clicked(self):
        self.start_sync_ui()

        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass

    def start_sync_ui(self):
        self.model.init_user_list_page_entry()
        self.view.user_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.populate_user_list_table()
    
    def on_import_user_button_clicked(self):
        try:
            self.user_csv_file, _ = QFileDialog.getOpenFileName(self.view, 'Open CSV', qss.csv_file_path, 'CSV File (*.csv)')
            self.user_csv_df = pd.read_csv(self.user_csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

            if self.user_csv_file:
                self.model.prog_total_data_value = len(self.user_csv_df)
                self.model.prog_remaining_data_value = len(self.user_csv_df)

                self.model.setup_progress_panel(window_title=f"{'percentage'}", progress_type='user_import')
                self.model.import_user_entry(data_frame=self.user_csv_df)
                self.setup_user_import_thread_conn()
                self.model.progress_dialog.exec()

                if self.model.prog_remaining_data_value > 0 and self.model.progress_dialog.close():
                    self.model.user_import_thread.stop()

                    self.model.init_progress_data_entry()

                    QMessageBox.critical(self.view, 'Cancelled', 'Import has been cancelled')
                    self.on_sync_ui_button_clicked()
            pass
        except Exception as e:
            self.user_csv_file = ''
        pass
    def setup_user_import_thread_conn(self):
        self.model.user_import_thread.update_signal.connect(self.on_user_import_thread_update_signal)
        self.model.user_import_thread.finished_signal.connect(self.on_user_import_thread_finished_signal)
        self.model.user_import_thread.invalid_signal.connect(self.on_user_import_thread_invalid_signal)
        pass
    def on_user_import_thread_update_signal(self):
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
    def on_user_import_thread_finished_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.information(self.view, 'Success', 'All user has been imported')
        self.on_sync_ui_button_clicked()
        pass
    def on_user_import_thread_invalid_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.critical(self.view, 'Error', 'Invalid CSV file.')
        self.on_sync_ui_button_clicked()
        pass

    def on_add_user_button_clicked(self):
        self.model.setup_manage_user_panel(window_title='Add user')
        self.setup_manage_user_panel_conn(conn_type='add_user')

        self.model.manage_user_dialog.exec()
        pass
    def on_edit_user_button_clicked(self, value):
        self.model.assign_selected_user_data_entry(value)
        self.model.setup_manage_user_panel(window_title=f"Edit {self.model.sel_user_name_value}")

        self.model.user_name_field.setText(self.model.sel_user_name_value)
        self.model.user_password_field.setText(self.model.sel_user_password_value)
        self.model.user_phone_field.setText(self.model.sel_user_phone_value)

        self.setup_manage_user_panel_conn(conn_type='edit_user')

        self.model.manage_user_dialog.exec()
        pass

    def setup_manage_user_panel_conn(self, conn_type):
        self.model.manage_user_save_button.clicked.connect(lambda: self.on_manage_user_save_button_clicked(action=conn_type))
        self.model.manage_user_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.manage_user_dialog))
        pass
    def on_manage_user_save_button_clicked(self, action):
        user_name = self.model.user_name_field.text()
        user_password = self.model.user_password_field.text()
        user_phone = self.model.user_phone_field.text()

        if '' not in [user_name, user_password, user_phone]:
            if user_phone.isdigit() is True:
                if action == 'add_user':
                    self.model.save_new_user_entry()
                    self.model.init_selected_user_data_entry()

                    QMessageBox.information(self.view, 'Success', 'New user has been added.')
                    pass
                elif action == 'edit_user':
                    self.model.save_edit_user_entry()
                    self.model.init_selected_user_data_entry()

                    QMessageBox.information(self.view, 'Success', 'User has been edited.')
                    pass
                self.on_sync_ui_button_clicked()
                pass
            else:
                QMessageBox.critical(self.model.manage_user_dialog, 'Error', 'Invalid numerical input.')
                pass
        else:
            self.set_label_required_field_indicator(user_name,user_name, user_password, user_phone)

            QMessageBox.critical(self.model.manage_user_dialog, 'Error', 'Please fill out the required field.')
            pass
        pass
    def set_label_required_field_indicator(self, user_name, user_password, user_phone):
        self.model.user_name_label.setText(f"Name {qss.required_label}") if user_name == '' else self.model.user_name_label.setText(f"Name")
        self.model.user_password_label.setText(f"Type {qss.required_label}") if user_password == '' else self.model.user_password_label.setText(f"Password")
        self.model.user_phone_label.setText(f"Percent {qss.required_label}") if user_phone == '' else self.model.user_phone_label.setText(f"Phone")
    
    def on_view_user_button_clicked(self, value):
        self.model.assign_selected_user_data_entry(value)

        self.model.setup_view_user_panel()

        self.setup_view_user_conn()

        self.model.view_dialog.exec()
        pass
    def setup_view_user_conn(self):
        self.model.view_form_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.view_dialog))

    def on_delete_user_button_clicked(self, value):
        self.model.assign_selected_user_data_entry(value)

        confirm = QMessageBox.warning(self.view, 'Confirm', f"Delete {self.model.sel_user_name_value}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_user(user_id=self.model.sel_user_id_value)

            self.model.init_selected_user_data_entry()

            QMessageBox.information(self.view, 'Success', 'User has been deleted.')

            self.on_sync_ui_button_clicked()
            pass
        else:
            self.model.init_selected_user_data_entry()
            return
        pass
    
    def on_close_button_clicked(self, widget: QWidget):
        widget.close()

        self.model.init_selected_user_data_entry()
        pass

    def on_user_list_pag_button_clicked(self, action):
        print('user_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.page_number > 1:
                self.model.page_number -= 1
                self.view.user_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_user_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        elif action == 'go_next':
            self.model.page_number += 1
            self.view.user_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_user_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        pass

    pass

class MyUserWindow(MyGroupBox):
    def __init__(self, name): # NOTE: 'name' param is for the current user (cashier, admin, dev) name
        super().__init__(object_name='MyUserWindow')

        self.model = MyUserModel(name=name)
        self.view = MyUserView(self.model)
        self.controller = MyUserController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.show()


# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    user_window = MyUserWindow(name='test-name')

    user_window.run()
    app.exec()