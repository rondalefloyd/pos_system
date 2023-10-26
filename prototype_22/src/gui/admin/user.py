
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.gui.widget.my_widget import *
from src.core.csv_to_db_importer import MyDataImportThread
from src.core.sql.admin.user import MyUserSchema
from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()
schema = MyUserSchema()

class MyUserModel:
    def __init__(self, name, phone):
        self.user_name = name
        self.user_phone = phone

        self.total_page_number = schema.select_user_data_total_page_count()
        self.page_number = 1 if self.total_page_number > 0 else 0

        self.sel_user_id = 0

    def set_import_data_entry(self, csv_file_path):
        self.progress_count = 0
        self.progress_percent = 100

        self.data_import_thread = MyDataImportThread(data_name='user', csv_file_path=csv_file_path)

        self.data_import_thread.start()
    
    def init_manage_data_entry(
            self, 
            dialog, 
            task, 
            user_name_label, 
            user_password_label, 
            user_level_label, 
            user_phone_label,
            user_name, 
            user_password, 
            user_level, 
            user_phone
    ):
        if '' not in [user_name, user_password, user_level, user_phone]:
            if (user_level.isdigit() and user_phone.isdigit()):
                if len(user_phone) == 11:
                    user_name_label.setText(f"Name")
                    user_password_label.setText(f"Password")
                    user_level_label.setText(f"Level")
                    user_phone_label.setText(f"Phone")

                    if task == 'add_data':
                        schema.insert_user_data(
                            user_name,
                            user_password,
                            user_level,
                            user_phone,
                        )
                        QMessageBox.information(dialog, 'Success', 'User added.')
                        dialog.close()
                        pass
                    elif task == 'edit_data':
                        schema.update_user_data(
                            user_name,
                            user_password,
                            user_level,
                            user_phone,
                            self.sel_user_id
                        )
                        QMessageBox.information(dialog, 'Success', 'User edited.')
                        dialog.close()
                        self.sel_user_id = 0
                        pass
                else:
                    QMessageBox.critical(dialog, 'Error', 'Invalid phone number.')
            else:
                user_name_label.setText(f"Name")
                user_password_label.setText(f"Password")
                user_level_label.setText(f"Level {qss.inv_field_indicator}") if user_level.isdigit() is False else user_level_label.setText(f"Level")
                user_phone_label.setText(f"Phone {qss.inv_field_indicator}") if user_phone.isdigit() is False else user_phone_label.setText(f"Phone")
  
                QMessageBox.critical(dialog, 'Error', 'Invalid numeric value.')
        else:
            user_name_label.setText(f"Name {qss.req_field_indicator}") if user_name == '' else user_name_label.setText(f"Name")
            user_password_label.setText(f"Password {qss.req_field_indicator}") if user_password == '' else user_password_label.setText(f"Password")
            user_level_label.setText(f"Level {qss.inv_field_indicator}") if user_level.isdigit() is False else user_level_label.setText(f"Level")
            user_phone_label.setText(f"Phone {qss.inv_field_indicator}") if user_phone.isdigit() is False else user_phone_label.setText(f"Phone")

            QMessageBox.critical(dialog, 'Error', 'Please fill out all required fields.')
    pass
class MyUserView(MyWidget):
    def __init__(self, model: MyUserModel):
        super().__init__()

        self.m = model

        self.set_user_box()

    def set_user_box(self):
        self.filter_field = MyLineEdit(object_name='filter_field')
        self.filter_button = MyPushButton(text='Filter')
        self.filter_box = MyGroupBox()
        self.filter_layout = MyHBoxLayout()
        self.filter_layout.addWidget(self.filter_field)
        self.filter_layout.addWidget(self.filter_button)
        self.filter_box.setLayout(self.filter_layout)

        self.import_data_button = MyPushButton(text='Import')
        self.add_data_button = MyPushButton(text='Add')
        self.manage_data_box = MyGroupBox()
        self.field_layout = MyHBoxLayout()
        self.field_layout.addWidget(self.import_data_button)
        self.field_layout.addWidget(self.add_data_button)
        self.manage_data_box.setLayout(self.field_layout)

        self.user_act_box = MyGroupBox()
        self.user_act_layout = MyHBoxLayout()
        self.user_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.user_act_layout.addWidget(self.manage_data_box,1,Qt.AlignmentFlag.AlignRight)
        self.user_act_box.setLayout(self.user_act_layout)

        self.user_overview_table = MyTableWidget(object_name='user_overview_table')
        self.user_overview_prev_button = MyPushButton(text='Prev')
        self.user_overview_page_label = MyLabel(text=f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.user_overview_next_button = MyPushButton(text='Next')

        self.user_overview_act_box = MyGroupBox()
        self.user_overview_act_layout = MyHBoxLayout()
        self.user_overview_act_layout.addWidget(self.user_overview_prev_button)
        self.user_overview_act_layout.addWidget(self.user_overview_page_label)
        self.user_overview_act_layout.addWidget(self.user_overview_next_button)
        self.user_overview_act_box.setLayout(self.user_overview_act_layout)
        self.user_overview_box = MyGroupBox()
        self.user_overview_layout = MyVBoxLayout()
        self.user_overview_layout.addWidget(self.user_overview_table)
        self.user_overview_layout.addWidget(self.user_overview_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.user_overview_box.setLayout(self.user_overview_layout)
        
        self.user_sort_tab = MyTabWidget()
        self.user_sort_tab.addTab(self.user_overview_box, 'Overview')

        self.main_layout = MyVBoxLayout()
        self.main_layout.addWidget(self.user_act_box)
        self.main_layout.addWidget(self.user_sort_tab)
        self.setLayout(self.main_layout)

    def set_manage_data_box(self):
        self.user_name_field = MyLineEdit(object_name='user_name_field')
        self.user_name_label = MyLabel(text='Name')
        self.user_password_field = MyLineEdit(object_name='user_password_field')
        self.user_password_label = MyLabel(text='Password')
        self.user_level_field = MyComboBox(object_name='user_level_field')
        self.user_level_label = MyLabel(text='Access level')
        self.user_phone_field = MyLineEdit(object_name='user_phone_field')
        self.user_phone_label = MyLabel(text='Phone')
        self.field_box = MyGroupBox()
        self.field_layout = MyFormLayout()
        self.field_layout.addRow(self.user_name_label)
        self.field_layout.addRow(self.user_name_field)
        self.field_layout.addRow(self.user_password_label)
        self.field_layout.addRow(self.user_password_field)
        self.field_layout.addRow(self.user_level_label)
        self.field_layout.addRow(self.user_level_field)
        self.field_layout.addRow(self.user_phone_label)
        self.field_layout.addRow(self.user_phone_field)
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
        self.progress_dialog = MyDialog(object_name='progress_dialog', window_title='99% complete')
        self.progress_layout = MyVBoxLayout()
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_dialog.setLayout(self.progress_layout)
        pass

    def set_overview_table_act_box(self):
        self.edit_data_button = MyPushButton(text='Edit')
        self.view_data_button = MyPushButton(text='View')
        self.delete_data_button = MyPushButton(text='Delete')
        self.user_overview_act_box = MyGroupBox(object_name='user_overview_act_box')
        self.user_overview_act_layout = MyHBoxLayout(object_name='user_overview_act_layout')
        self.user_overview_act_layout.addWidget(self.edit_data_button)
        self.user_overview_act_layout.addWidget(self.view_data_button)
        self.user_overview_act_layout.addWidget(self.delete_data_button)
        self.user_overview_act_box.setLayout(self.user_overview_act_layout)

    def set_view_dialog(self):
        self.user_name_info = MyLabel(text=f"user_name")
        self.user_password_info = MyLabel(text=f"user_password")
        self.user_level_info = MyLabel(text=f"user_level")
        self.user_phone_info = MyLabel(text=f"user_phone")
        self.datetime_created_info = MyLabel(text=f"datetime_created")
        self.info_box = MyGroupBox()
        self.info_layout = MyFormLayout()
        self.info_layout.addRow('Name:', self.user_name_info)
        self.info_layout.addRow('Type:', self.user_password_info)
        self.info_layout.addRow('Percent:', self.user_level_info)
        self.info_layout.addRow('Description:', self.user_phone_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Date/Time created:', self.datetime_created_info)
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
class MyUserController:
    def __init__(self, model: MyUserModel, view: MyUserView):
        self.v = view
        self.m = model

        self.set_user_box_conn()
        self.sync_ui()

    def set_user_box_conn(self):
        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)
        self.v.import_data_button.clicked.connect(self.on_import_data_button_clicked)
        self.v.add_data_button.clicked.connect(self.on_add_data_button_clicked)
        self.v.user_overview_prev_button.clicked.connect(self.on_overview_prev_button_clicked)
        self.v.user_overview_next_button.clicked.connect(self.on_overview_next_button_clicked)
        pass
    def on_filter_button_clicked(self): # IDEA: src
        text_filter = self.v.filter_field.text()
        
        self.m.total_page_number = schema.select_user_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0

        print(self.m.total_page_number, self.m.page_number)

        self.v.user_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        
        self.populate_overview_table(text=text_filter, page_number=self.m.page_number)
        pass
    
    def on_import_data_button_clicked(self): # IDEA: src
        csv_file_path, _ = QFileDialog.getOpenFileName(None, 'Open CSV', qss.csv_folder_path, 'CSV File (*csv)')

        if csv_file_path:
            self.v.set_progress_dialog()
            self.m.set_import_data_entry(csv_file_path)
            self.set_data_import_thread_conn()

            self.v.progress_dialog.exec()
            if self.v.progress_dialog.close(): self.m.data_import_thread.stop()
            
            self.sync_ui()
        pass
    def set_data_import_thread_conn(self):
        self.m.data_import_thread.update.connect(self.on_data_import_thread_update)
        self.m.data_import_thread.cancelled.connect(self.on_data_import_thread_cancelled)
        self.m.data_import_thread.finished.connect(self.on_data_import_thread_finished)
        self.m.data_import_thread.invalid.connect(self.on_data_import_thread_invalid)
        pass
    def on_data_import_thread_update(self, total_data_count, current_data):
        self.m.progress_count += 1
        print(self.m.progress_count)
        self.m.progress_percent = int((self.m.progress_count / total_data_count) * 100)
        self.v.progress_dialog.setWindowTitle(f"{self.m.progress_percent}% complete")
        self.v.progress_bar.setValue(self.m.progress_percent)
        self.v.progress_label.setText(current_data)
        pass
    def on_data_import_thread_cancelled(self):
        QMessageBox.information(None, 'Cancelled', 'Import cancelled.')
        pass
    def on_data_import_thread_finished(self):
        QMessageBox.information(None, 'Success', 'Import complete.')
        self.v.progress_dialog.close()
        pass
    def on_data_import_thread_invalid(self):
        QMessageBox.critical(None, 'Error', 'An error occurred during import.')
        self.v.progress_dialog.close()
        pass

    def on_add_data_button_clicked(self): # IDEA: src
        self.v.set_manage_data_box()
        self.load_combo_box_data()
        self.set_manage_data_box_conn(task='add_data')
        self.v.manage_data_dialog.exec()
        pass

    def populate_overview_table(self, text='', page_number=1): # IDEA: src
        self.v.user_overview_prev_button.setEnabled(page_number > 1)
        self.v.user_overview_next_button.setEnabled(page_number < self.m.total_page_number)
        self.v.user_overview_page_label.setText(f"Page {page_number}/{self.m.total_page_number}")

        user_data = schema.select_user_data_as_display(text=text, page_number=page_number)

        self.v.user_overview_table.setRowCount(len(user_data))

        for i, data in enumerate(user_data):
            self.v.set_overview_table_act_box()
            user_name = QTableWidgetItem(f"{data[0]}")
            user_password = QTableWidgetItem(f"{data[1]}")
            user_level = QTableWidgetItem(f"{data[2]}")
            user_phone = QTableWidgetItem(f"{data[3]}")
            datetime_created = QTableWidgetItem(f"{data[4]}")

            self.v.user_overview_table.setCellWidget(i, 0, self.v.user_overview_act_box)
            self.v.user_overview_table.setItem(i, 1, user_name)
            self.v.user_overview_table.setItem(i, 2, user_password)
            self.v.user_overview_table.setItem(i, 3, user_level)
            self.v.user_overview_table.setItem(i, 4, user_phone)
            self.v.user_overview_table.setItem(i, 5, datetime_created)

            self.v.edit_data_button.clicked.connect(lambda _, data=data: self.on_edit_data_button_clicked(data))
            self.v.view_data_button.clicked.connect(lambda _, data=data: self.on_view_data_button_clicked(data))
            self.v.delete_data_button.clicked.connect(lambda _, data=data: self.on_delete_data_button_clicked(data))
        pass
    def on_edit_data_button_clicked(self, data):
        self.v.set_manage_data_box()
        self.load_combo_box_data()
        self.v.manage_data_dialog.setWindowTitle(f"{data[0]}")
        sel_user_data = schema.select_user_data(data[0], data[1])

        for i, sel_data in enumerate(sel_user_data):
            self.v.user_name_field.setText(str(sel_data[0]))
            self.v.user_password_field.setText(str(sel_data[1]))
            self.v.user_level_field.setCurrentText(str(sel_data[2]))
            self.v.user_phone_field.setText(str(sel_data[3]))
            self.m.sel_user_id = sel_data[4]
            pass
        
        self.set_manage_data_box_conn(task='edit_data')
        self.v.manage_data_dialog.exec()
        pass
    def on_view_data_button_clicked(self, data):
        self.v.set_view_dialog()
        self.v.view_data_dialog.setWindowTitle(f"{data[0]}")

        self.v.user_name_info.setText(str(data[0]))
        self.v.user_password_info.setText(str(data[1]))
        self.v.user_level_info.setText(str(data[2]))
        self.v.user_phone_info.setText(str(data[3]))
        self.v.datetime_created_info.setText(str(data[4]))

        self.set_view_data_box_conn()
        self.v.view_data_dialog.exec()
        pass
    def set_view_data_box_conn(self):
        self.v.view_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.view_data_dialog))
    def on_delete_data_button_clicked(self, data):
        sel_user_data = schema.select_user_data(data[0], data[1])

        for i, sel_data in enumerate(sel_user_data):
            user_name = sel_data[0]
            user_id = sel_data[4]

        confirm = QMessageBox.warning(None, 'Confirm', f"Delete {user_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_user_data(user_id)

            QMessageBox.information(None, 'Success', f"{user_name} has been deleted.")

        self.sync_ui()
        pass

    def on_overview_prev_button_clicked(self):
        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.user_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass
    def on_overview_next_button_clicked(self):
        if self.m.page_number < self.m.total_page_number:
            self.m.page_number += 1

            self.v.user_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass

    # IDEA: if the widget uses the same connection
    def set_manage_data_box_conn(self, task):
        self.v.save_data_button.clicked.connect(lambda: self.on_save_data_button_clicked(task))
        self.v.manage_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.manage_data_dialog))
        pass
    def load_combo_box_data(self):
        self.v.set_manage_data_box()

        self.v.user_level_field.addItem('1')
        self.v.user_level_field.addItem('2')
        pass
    def on_save_data_button_clicked(self, task):
        user_name = self.v.user_name_field.text()
        user_password = self.v.user_password_field.text()
        user_level = self.v.user_level_field.currentText()
        user_phone = self.v.user_phone_field.text()

        self.m.init_manage_data_entry(
            self.v.manage_data_dialog, 
            task, 
            self.v.user_name_label, 
            self.v.user_password_label, 
            self.v.user_level_label, 
            self.v.user_phone_label,
            user_name, 
            user_password, 
            user_level, 
            user_phone
        )

        self.sync_ui()

    def sync_ui(self):
        text_filter = self.v.filter_field.text()
        self.total_page_number = schema.select_user_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0
        self.populate_overview_table(page_number=self.m.page_number)
        pass
    def close_dialog(self, dialog: QDialog):
        dialog.close()

class MyUserWindow(MyGroupBox):
    def __init__(self, name='test', phone='test'):
        super().__init__()

        self.model = MyUserModel(name, phone)
        self.view = MyUserView(self.model)
        self.controller = MyUserController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    user_window = MyUserWindow()

    user_window.run()

    app.exec()


# TODO: fix the manage_dialog (use for loop to prevent it from closing when it's currently in use and the inputs were errors)