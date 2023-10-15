import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.core.qss_config import *
from src.core.manual_csv_importer import *
from src.sql.admin.user import *
from src.widget.admin.user import *

class MyUserModel: # IDEA: global variables
    def __init__(self):
        self.csv_path = 'G:' + f"/My Drive/csv/"

        self.user_list_page_number = 1
        self.user_list_total_page_number = schema.count_user_list_total_pages()
        
        self.total_user = schema.count_user()

        self.user_data_count_value = 0
        self.user_data_total_value = 0
        self.user_data_remaining_value = 0

    def set_user_form_box(self):
        self.user_name_label = MyLabel(text=f"Name")
        self.user_password_label = MyLabel(text=f"Password")
        self.user_access_level_label = MyLabel(text=f"Access level")
        self.user_phone_label = MyLabel(text=f"Phone")

        self.user_name_field = MyLineEdit(object_name='user_name_field')
        self.user_password_field = MyLineEdit(object_name='user_password_field')
        self.user_access_level_field = MyComboBox(object_name='user_access_level_field')
        self.user_phone_field = MyPlainTextEdit(object_name='user_phone_field')

        self.populate_user_form_combo_box()

        self.user_form_box = MyGroupBox()
        self.user_form_layout = MyFormLayout()
        self.user_form_layout.insertRow(0, self.user_name_label)
        self.user_form_layout.insertRow(2, self.user_password_label)
        self.user_form_layout.insertRow(4, self.user_access_level_label)
        self.user_form_layout.insertRow(6, self.user_phone_label)

        self.user_form_layout.insertRow(1, self.user_name_field)
        self.user_form_layout.insertRow(3, self.user_password_field)
        self.user_form_layout.insertRow(5, self.user_access_level_field)
        self.user_form_layout.insertRow(7, self.user_phone_field)
        self.user_form_box.setLayout(self.user_form_layout)
        self.user_form_scra = MyScrollArea(object_name='user_form_scra')
        self.user_form_scra.setWidget(self.user_form_box)
        pass

    def populate_user_form_combo_box(self):
        self.user_access_level_field.addItem('1')
        self.user_access_level_field.addItem('2')
        self.user_access_level_field.addItem('3')

class MyUserView(MyWidget):  # IDEA: groupbox, layouts, dialogs
    def __init__(self, model: MyUserModel):
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

        self.import_user_button = MyPushButton(text='Import')
        self.add_user_button = MyPushButton(text='Add')
        self.add_user_box = MyGroupBox()
        self.add_user_layout = MyHBoxLayout(object_name='add_user_layout')
        self.add_user_layout.addWidget(self.import_user_button)
        self.add_user_layout.addWidget(self.add_user_button)
        self.add_user_box.setLayout(self.add_user_layout)

        self.user_list_table = MyTableWidget(object_name='user_list_table')
        self.user_list_pag_prev_button = MyPushButton(text='Prev')
        self.user_list_pag_page_label = MyLabel(text='Page 99/99')
        self.user_list_pag_next_button = MyPushButton(text='Next')
        self.user_list_pag_act_box = MyGroupBox()
        self.user_list_pag_act_layout = MyHBoxLayout(object_name='user_list_pag_act_layout')
        self.user_list_pag_act_layout.addWidget(self.user_list_pag_prev_button)
        self.user_list_pag_act_layout.addWidget(self.user_list_pag_page_label)
        self.user_list_pag_act_layout.addWidget(self.user_list_pag_next_button)
        self.user_list_pag_act_box.setLayout(self.user_list_pag_act_layout)
        self.user_list_box = MyGroupBox()
        self.user_list_layout = MyVBoxLayout()
        self.user_list_layout.addWidget(self.user_list_table)
        self.user_list_layout.addWidget(self.user_list_pag_act_box)
        self.user_list_box.setLayout(self.user_list_layout)
        self.user_list_tab = MyTabWidget()
        self.user_list_tab.addTab(self.user_list_box, 'Overview')
    
        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.add_user_box,0,1)
        self.panel_a_layout.addWidget(self.user_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    def set_panel_b_box(self):
        self.panel_b_box = MyGroupBox()
        self.panel_b_layout = MyHBoxLayout(object_name='panel_b_layout')

        self.current_user_label = MyLabel(text=f"Current user: {'Phoebe'} (Admin)")
        self.total_user_label = MyLabel(text=f"Total user: {self.model.total_user}")
        
        self.panel_b_layout.addWidget(self.current_user_label)
        self.panel_b_layout.addWidget(self.total_user_label)
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
    def set_add_user_dialog(self):
        self.add_user_dialog = MyDialog()
        self.add_user_layout = MyVBoxLayout()

        self.model.set_user_form_box()

        self.add_user_save_button = MyPushButton(object_name='add_user_save_button', text='Save')
        self.add_user_cancel_button = MyPushButton(object_name='add_user_cancel_button', text='Cancel')
        self.add_user_form_act_box = MyGroupBox()
        self.add_user_form_act_layout = MyHBoxLayout(object_name='add_user_form_act_layout')
        self.add_user_form_act_layout.addWidget(self.add_user_save_button)
        self.add_user_form_act_layout.addWidget(self.add_user_cancel_button)
        self.add_user_form_act_box.setLayout(self.add_user_form_act_layout)

        self.add_user_layout.addWidget(self.model.user_form_scra)
        self.add_user_layout.addWidget(self.add_user_form_act_box)
        self.add_user_dialog.setLayout(self.add_user_layout)
        pass
    
    def set_edit_user_dialog(self):
        self.edit_user_dialog = MyDialog()
        self.edit_user_layout = MyVBoxLayout()

        self.model.set_user_form_box()

        self.edit_user_save_button = MyPushButton(object_name='edit_user_save_button', text='Save')
        self.edit_user_cancel_button = MyPushButton(object_name='edit_user_cancel_button', text='Cancel')
        self.edit_user_form_act_box = MyGroupBox()
        self.edit_user_form_act_layout = MyHBoxLayout(object_name='edit_user_form_act_layout')
        self.edit_user_form_act_layout.addWidget(self.edit_user_save_button)
        self.edit_user_form_act_layout.addWidget(self.edit_user_cancel_button)
        self.edit_user_form_act_box.setLayout(self.edit_user_form_act_layout)

        self.edit_user_layout.addWidget(self.model.user_form_scra)
        self.edit_user_layout.addWidget(self.edit_user_form_act_box)
        self.edit_user_dialog.setLayout(self.edit_user_layout)
        pass
    def set_show_user_dialog(self):
        self.show_user_dialog = MyDialog()
        self.show_user_layout = MyFormLayout()
        
        self.user_name_info_label = MyLabel()
        self.user_password_info_label = MyLabel()
        self.user_access_level_info_label = MyLabel()
        self.user_phone_info_label = MyLabel()
        self.user_date_created_info_label = MyLabel()
        self.show_user_form_box = MyGroupBox()
        self.show_user_form_layout = MyFormLayout()
        self.show_user_form_layout.addRow('Name:', self.user_name_info_label)
        self.show_user_form_layout.addRow('Password:', self.user_password_info_label)
        self.show_user_form_layout.addRow('Access level:', self.user_access_level_info_label)
        self.show_user_form_layout.addRow('Phone:', self.user_phone_info_label)
        self.show_user_form_layout.addRow(MyLabel(text='<hr>'))
        self.show_user_form_layout.addRow('Date created:', self.user_date_created_info_label)
        self.show_user_form_box.setLayout(self.show_user_form_layout)
        self.show_user_form_scra = MyScrollArea(object_name='user_form_scra')
        self.show_user_form_scra.setWidget(self.show_user_form_box)

        self.show_user_close_button = MyPushButton(text='Close')
        self.show_user_act_box = MyGroupBox()
        self.show_user_act_layout = MyHBoxLayout(object_name='show_user_act_layout')
        self.show_user_act_layout.addWidget(self.show_user_close_button)
        self.show_user_act_box.setLayout(self.show_user_act_layout)

        self.show_user_layout.addRow(self.show_user_form_scra)
        self.show_user_layout.addRow(self.show_user_act_box)

        self.show_user_dialog.setLayout(self.show_user_layout)

class MyUserController: # IDEA: connections, populations, on signals
    def __init__(self, model: MyUserModel, view: MyUserView):
        self.model = model
        self.view = view

        self.set_panel_a_box_conn()
        self.set_user_list_table_conn()

        self.populate_user_list_table()

    def set_panel_a_box_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)

        self.view.import_user_button.clicked.connect(self.on_import_user_button_clicked)
        self.view.add_user_button.clicked.connect(self.on_add_user_button_clicked)
        pass
    def set_user_list_table_conn(self):
        self.view.user_list_pag_prev_button.clicked.connect(lambda: self.on_user_list_pag_button_clicked(action='prev'))
        self.view.user_list_pag_next_button.clicked.connect(lambda: self.on_user_list_pag_button_clicked(action='next'))
        pass

    def populate_form_required_label(self, user_name, password, access_level):
        self.model.user_name_label.setText(f"Name {qss.required_label}") if user_name == '' else self.model.user_name_label.setText(f"Name")
        self.model.user_password_label.setText(f"Password {qss.required_label}") if password == '' else self.model.user_password_label.setText(f"Password")
        self.model.user_access_level_label.setText(f"Access level {qss.required_label}") if access_level == '' else self.model.user_access_level_label.setText(f"Access level")
        pass
    def populate_user_list_table(self):
        text_filter_value = self.view.text_filter_field.text()
        page_number = self.model.user_list_page_number
        total_page_number = self.model.user_list_total_page_number

        print('text_filter_value:', text_filter_value)
        print('page_number:', page_number)
        print('total_page_number:', total_page_number)

        self.user_list_data = schema.list_user_data(text_filter=text_filter_value, page_number=page_number)        

        self.view.user_list_pag_page_label.setText(f"Page {page_number}/{total_page_number}")

        self.view.user_list_pag_prev_button.setEnabled(page_number > 1)
        self.view.user_list_pag_next_button.setEnabled(len(self.user_list_data) == 30)

        self.view.user_list_table.setRowCount(len(self.user_list_data))

        for list_i, list_v in enumerate(self.user_list_data):
            self.list_edit_button = MyPushButton(text='Edit')
            self.list_show_button = MyPushButton(text='Show')
            self.list_delete_button = MyPushButton(text='Delete')
            list_act_box = MyGroupBox()
            list_act_layout = MyHBoxLayout(object_name='list_act_layout')
            list_act_layout.addWidget(self.list_edit_button)
            list_act_layout.addWidget(self.list_show_button)
            list_act_layout.addWidget(self.list_delete_button)
            list_act_box.setLayout(list_act_layout)

            user_name = QTableWidgetItem(f"{list_v[0]}")
            user_password = QTableWidgetItem(f"{list_v[1]}")
            user_access_level = QTableWidgetItem(f"{list_v[2]}")
            user_phone = QTableWidgetItem(f"{list_v[3]}")
            date_created = QTableWidgetItem(f"{list_v[4]}")

            self.view.user_list_table.setCellWidget(list_i, 0, list_act_box)
            self.view.user_list_table.setItem(list_i, 1, user_name)
            self.view.user_list_table.setItem(list_i, 2, user_password)
            self.view.user_list_table.setItem(list_i, 3, user_access_level)
            self.view.user_list_table.setItem(list_i, 4, user_phone)
            self.view.user_list_table.setItem(list_i, 5, date_created)

            self.list_edit_button.clicked.connect(lambda _, list_v=list_v: self.on_list_edit_button_clicked(list_v))
            self.list_show_button.clicked.connect(lambda _, list_v=list_v: self.on_list_show_button_clicked(list_v))
            self.list_delete_button.clicked.connect(lambda _, list_v=list_v: self.on_list_delete_button_clicked(list_v))
        
        self.view.total_user_label.setText(f"Total user: {self.model.total_user}")

    def on_text_filter_button_clicked(self):
        self.populate_user_list_table()
    
    def on_import_user_button_clicked(self):
        self.user_csv_file_path, _ = QFileDialog.getOpenFileName(self.view, 'Import user', self.model.csv_path, 'CSV Files (*.csv)')

        if self.user_csv_file_path:
            self.user_data_frame = pd.read_csv(self.user_csv_file_path, encoding='utf-8-sig', keep_default_na=False, header=None)
            
            self.model.user_data_total_value = len(self.user_data_frame)
            self.model.user_data_remaining_value = len(self.user_data_frame)
            
            self.view.set_import_progress_dialog()

            self.manual_csv_importer = ManualUserImport(user_data_frame=self.user_data_frame)
            self.manual_csv_importer.start()

            self.manual_csv_importer.progress_signal.connect(self.on_manual_csv_importer_progress_signal)
            self.manual_csv_importer.finished_signal.connect(self.on_manual_csv_importer_finished_signal)

            self.view.import_progress_dialog.exec()
        pass
    def on_manual_csv_importer_progress_signal(self):
        self.model.user_data_count_value += 1
        self.model.user_data_remaining_value -= 1
        progress_value = int((self.model.user_data_count_value / self.model.user_data_total_value) * 100)

        self.view.import_progress_label.setText(f"Please wait... ({self.model.user_data_remaining_value})")
        self.view.import_progress_bar.setValue(progress_value)
        pass
    def on_manual_csv_importer_finished_signal(self):
        self.view.import_progress_dialog.close()

        QMessageBox.information(self.view, 'Success', 'All user has been imported.')

        self.model.user_list_page_number = 1
        self.populate_user_list_table()
        pass
    
    def on_add_user_button_clicked(self):
        self.view.set_add_user_dialog()
        
        self.view.add_user_save_button.clicked.connect(self.on_add_user_save_button_clicked)
        self.view.add_user_cancel_button.clicked.connect(self.on_add_user_cancel_button_clicked)

        self.view.add_user_dialog.exec()
        pass
    def on_add_user_save_button_clicked(self):
        user_name = self.model.user_name_field.text()
        password = self.model.user_password_field.text()
        access_level = self.model.access_level_field.currentText()
        phone = self.model.user_phone_field.toPlainText()

        if '' not in [user_name, access_level, password]:
            schema.add_new_user(
                user_name=user_name,
                password=password,
                access_level=access_level,
                phone=phone
            )

            self.view.add_user_dialog.close()

            QMessageBox.information(self.view, 'Success', 'User has been added.')

            self.model.user_list_page_number = 1
            self.populate_user_list_table()
            pass
        else:
            self.populate_form_required_label(user_name, password, access_level)
            
            QMessageBox.critical(self.view.add_user_dialog, 'Error', 'Please fill out all required fields.')
            pass
        pass

    def on_add_user_cancel_button_clicked(self):
        self.view.add_user_dialog.close()
        pass

    def on_list_edit_button_clicked(self, list_v):
        self.view.set_edit_user_dialog()
        
        self.model.user_name_field.setText(f"{list_v[0]}")
        self.model.user_password_field.setText(f"{list_v[1]}")
        self.model.user_access_level_field.setCurrentText(f"{list_v[2]}")
        self.model.user_phone_field.setPlainText(f"{list_v[3]}")

        self.view.edit_user_save_button.clicked.connect(lambda: self.on_edit_user_save_button_clicked(user_id=list_v[5]))
        self.view.edit_user_cancel_button.clicked.connect(self.on_edit_user_cancel_button_clicked)

        self.view.edit_user_dialog.exec()
        pass 
    def on_edit_user_save_button_clicked(self, user_id):
        user_name = self.model.user_name_field.text()
        password = self.model.user_password_field.text()
        access_level = self.model.user_access_level_field.currentText()
        phone = self.model.user_phone_field.toPlainText()

        if '' not in [user_name, access_level, password]:
            schema.edit_selected_user(
                user_name=user_name,
                access_level=access_level,
                password=password,
                phone=phone,
                user_id=user_id,
            )

            self.view.edit_user_dialog.close()

            QMessageBox.information(self.view, 'Success', 'User has been added.')

            self.model.user_list_page_number = 1
            self.populate_user_list_table()
            pass
        else:
            self.populate_form_required_label(user_name, password, access_level)
            
            QMessageBox.critical(self.view.edit_user_dialog, 'Error', 'Please fill out all required fields.')
            pass
        pass
    def on_edit_user_cancel_button_clicked(self):
        self.view.edit_user_dialog.close()
        pass

    def on_list_show_button_clicked(self, list_v):
        self.view.set_show_user_dialog()

        self.view.user_name_info_label.setText(f"{list_v[0]}")
        self.view.user_password_info_label.setText(f"{list_v[1]}")
        self.view.user_access_level_info_label.setText(f"{list_v[2]}")
        self.view.user_phone_info_label.setText(f"{list_v[3]}")
        self.view.user_date_created_info_label.setText(f"{list_v[4]}")

        self.view.show_user_close_button.clicked.connect(self.on_show_user_close_button_clicked)

        self.view.show_user_dialog.exec()
        pass
    def on_show_user_close_button_clicked(self):
        self.view.show_user_dialog.close()

    def on_list_delete_button_clicked(self, list_v):
        # TODO: delete_button
        user_id = list_v[5]

        confirm = QMessageBox.warning(
            self.view,
            'Delete',
            f"Are you sure you want to delete this {list_v[0]}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_user(user_id=user_id)
        
            QMessageBox.information(self.view, 'Success', 'User has been deleted.')

            self.populate_user_list_table()
        pass

    def on_user_list_pag_button_clicked(self, action):
        if action == 'prev':
            if self.model.user_list_page_number > 1:
                self.model.user_list_page_number -= 1
                self.view.user_list_pag_page_label.setText(f"Page {self.model.user_list_page_number}/{self.model.user_list_total_page_number}")

            self.populate_user_list_table()
            pass
        elif action == 'next':
            self.model.user_list_page_number += 1
            self.view.user_list_pag_page_label.setText(f"Page {self.model.user_list_page_number}/{self.model.user_list_total_page_number}")

            self.populate_user_list_table()
            pass

if __name__ == ('__main__'):
    user_app = QApplication(sys.argv)
    
    schema = MyUserSchema()
    qss = QSSConfig()

    model = MyUserModel()
    view = MyUserView(model)
    controller = MyUserController(model, view)
    
    
    view.showMaximized()
    sys.exit(user_app.exec())
