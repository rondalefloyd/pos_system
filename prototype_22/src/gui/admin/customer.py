
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.gui.widget.my_widget import *
from src.core.csv_to_db_importer import MyDataImportThread
from src.core.sql.admin.customer import MyCustomerSchema
from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()
schema = MyCustomerSchema()

class MyCustomerModel:
    def __init__(self, name, phone):
        self.user_name = name
        self.user_phone = phone

        self.total_page_number = schema.select_customer_data_total_page_count()
        self.page_number = 1 if self.total_page_number > 0 else 0

        self.sel_customer_id = 0

    def set_import_data_entry(self, csv_file_path):
        self.progress_count = 0
        self.progress_percent = 100

        self.data_import_thread = MyDataImportThread(data_name='customer', csv_file_path=csv_file_path)

        self.data_import_thread.start()
    
    def init_manage_data_entry(
            self, 
            dialog, 
            task, 
            customer_name_label, 
            customer_barrio_label, 
            customer_town_label, 
            customer_phone_label, 
            customer_age_label, 
            customer_points_label, 
            customer_name, 
            customer_address, 
            customer_barrio, 
            customer_town, 
            customer_phone, 
            customer_age, 
            customer_gender, 
            customer_marstat,
            customer_points
    ):
        print('customer_points:', customer_points)
        if '' not in [customer_name, customer_barrio, customer_town, customer_phone, customer_age, customer_gender, customer_points]:
            if (customer_phone.isdigit() and customer_age.isdigit() and customer_points.replace('.', '', 1).isdigit()):
                if len(customer_phone) == 11:
                    customer_name_label.setText(f"Name")
                    customer_barrio_label.setText(f"Barrio")
                    customer_town_label.setText(f"Town")
                    customer_phone_label.setText(f"Phone")
                    customer_age_label.setText(f"Age")
                    customer_points_label.setText(f"Points")

                    if task == 'add_data':
                        schema.insert_customer_data(
                            customer_name,
                            customer_address,
                            customer_barrio,
                            customer_town,
                            customer_phone,
                            customer_age,
                            customer_gender,
                            customer_marstat,
                        )
                        QMessageBox.information(dialog, 'Success', 'Customer added.')
                        dialog.close()
                        pass
                    elif task == 'edit_data':
                        schema.update_customer_data(
                            customer_name,
                            customer_address,
                            customer_barrio,
                            customer_town,
                            customer_phone,
                            customer_age,
                            customer_gender,
                            customer_marstat,
                            customer_points,
                            self.sel_customer_id
                        )
                        QMessageBox.information(dialog, 'Success', 'Customer edited.')
                        dialog.close()
                        self.sel_customer_id = 0
                        pass
                else:
                    QMessageBox.critical(dialog, 'Error', 'Invalid phone number.')
            else:
                customer_name_label.setText(f"Name")
                customer_barrio_label.setText(f"Barrio")
                customer_town_label.setText(f"Town")
                customer_phone_label.setText(f"Phone {qss.inv_field_indicator}") if customer_phone.isdigit() is False else customer_phone_label.setText(f"Phone")
                customer_age_label.setText(f"Age {qss.inv_field_indicator}") if customer_age.isdigit() is False else customer_age_label.setText(f"Age")
                customer_points_label.setText(f"Points {qss.inv_field_indicator}") if customer_points == '' else customer_points_label.setText(f"Points")

                QMessageBox.critical(dialog, 'Error', 'Invalid numeric value.')
        else:
            customer_name_label.setText(f"Name {qss.req_field_indicator}") if customer_name == '' else customer_name_label.setText(f"Name")
            customer_barrio_label.setText(f"Barrio {qss.req_field_indicator}") if customer_barrio == '' else customer_barrio_label.setText(f"Barrio")
            customer_town_label.setText(f"Town {qss.req_field_indicator}") if customer_town == '' else customer_town_label.setText(f"Town")
            customer_phone_label.setText(f"Phone {qss.inv_field_indicator}") if customer_phone.isdigit() is False else customer_phone_label.setText(f"Phone")
            customer_age_label.setText(f"Age {qss.inv_field_indicator}") if customer_age.isdigit() is False else customer_age_label.setText(f"Age")
            customer_points_label.setText(f"Points {qss.inv_field_indicator}") if customer_points == '' else customer_points_label.setText(f"Points")

            QMessageBox.critical(dialog, 'Error', 'Please fill out all required fields.')
    pass
class MyCustomerView(MyWidget):
    def __init__(self, model: MyCustomerModel):
        super().__init__()

        self.m = model

        self.set_customer_box()

    def set_customer_box(self):
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

        self.customer_act_box = MyGroupBox()
        self.customer_act_layout = MyHBoxLayout()
        self.customer_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.customer_act_layout.addWidget(self.manage_data_box,1,Qt.AlignmentFlag.AlignRight)
        self.customer_act_box.setLayout(self.customer_act_layout)

        self.customer_overview_table = MyTableWidget(object_name='customer_overview_table')
        self.customer_overview_prev_button = MyPushButton(text='Prev')
        self.customer_overview_page_label = MyLabel(text=f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.customer_overview_next_button = MyPushButton(text='Next')
        self.customer_overview_act_box = MyGroupBox()
        self.customer_overview_act_layout = MyHBoxLayout()
        self.customer_overview_act_layout.addWidget(self.customer_overview_prev_button)
        self.customer_overview_act_layout.addWidget(self.customer_overview_page_label)
        self.customer_overview_act_layout.addWidget(self.customer_overview_next_button)
        self.customer_overview_act_box.setLayout(self.customer_overview_act_layout)
        self.customer_overview_box = MyGroupBox()
        self.customer_overview_layout = MyVBoxLayout()
        self.customer_overview_layout.addWidget(self.customer_overview_table)
        self.customer_overview_layout.addWidget(self.customer_overview_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.customer_overview_box.setLayout(self.customer_overview_layout)
        
        self.customer_sort_tab = MyTabWidget()
        self.customer_sort_tab.addTab(self.customer_overview_box, 'Overview')

        self.main_layout = MyVBoxLayout()
        self.main_layout.addWidget(self.customer_act_box)
        self.main_layout.addWidget(self.customer_sort_tab)
        self.setLayout(self.main_layout)

    def set_manage_data_box(self):
        self.customer_name_label = MyLabel(text='Name')
        self.customer_name_field = MyLineEdit(object_name='customer_name_field')
        self.customer_address_label = MyLabel(text='Address')
        self.customer_address_field = MyPlainTextEdit(object_name='customer_address_field')
        self.customer_barrio_label = MyLabel(text='Barrio')
        self.customer_barrio_field = MyComboBox(object_name='customer_barrio_field')
        self.customer_town_label = MyLabel(text='Town')
        self.customer_town_field = MyComboBox(object_name='customer_town_field')
        self.customer_phone_label = MyLabel(text='Phone')
        self.customer_phone_field = MyLineEdit(object_name='customer_phone_field')
        self.customer_age_label = MyLabel(text='Age')
        self.customer_age_field = MyLineEdit(object_name='customer_age_field')
        self.customer_gender_label = MyLabel(text='Town')
        self.customer_gender_field = MyComboBox(object_name='customer_gender_field')
        self.customer_marstat_label = MyLabel(text='Town')
        self.customer_marstat_field = MyComboBox(object_name='customer_marstat_field')
        self.customer_points_label = MyLabel(object_name='customer_points_label', text='Points')
        self.customer_points_field = MyLineEdit(object_name='customer_points_field')
        self.field_box = MyGroupBox()
        self.field_layout = MyFormLayout()
        self.field_layout.addRow(self.customer_name_label)
        self.field_layout.addRow(self.customer_name_field)
        self.field_layout.addRow(self.customer_address_label)
        self.field_layout.addRow(self.customer_address_field)
        self.field_layout.addRow(self.customer_barrio_label)
        self.field_layout.addRow(self.customer_barrio_field)
        self.field_layout.addRow(self.customer_town_label)
        self.field_layout.addRow(self.customer_town_field)
        self.field_layout.addRow(self.customer_phone_label)
        self.field_layout.addRow(self.customer_phone_field)
        self.field_layout.addRow(self.customer_age_label)
        self.field_layout.addRow(self.customer_age_field)
        self.field_layout.addRow(self.customer_gender_label)
        self.field_layout.addRow(self.customer_gender_field)
        self.field_layout.addRow(self.customer_marstat_label)
        self.field_layout.addRow(self.customer_marstat_field)
        self.field_layout.addRow(self.customer_points_label)
        self.field_layout.addRow(self.customer_points_field)
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

    def set_overview_table_act_box(self):
        self.edit_data_button = MyPushButton(text='Edit')
        self.view_data_button = MyPushButton(text='View')
        self.delete_data_button = MyPushButton(text='Delete')
        self.customer_overview_act_box = MyGroupBox(object_name='customer_overview_act_box')
        self.customer_overview_act_layout = MyHBoxLayout(object_name='customer_overview_act_layout')
        self.customer_overview_act_layout.addWidget(self.edit_data_button)
        self.customer_overview_act_layout.addWidget(self.view_data_button)
        self.customer_overview_act_layout.addWidget(self.delete_data_button)
        self.customer_overview_act_box.setLayout(self.customer_overview_act_layout)

    def set_view_dialog(self):
        self.customer_name_info = MyLabel(text=f"customer_name")
        self.customer_address_info = MyLabel(text=f"customer_address")
        self.customer_barrio_info = MyLabel(text=f"customer_barrio")
        self.customer_town_info = MyLabel(text=f"customer_town")
        self.customer_phone_info = MyLabel(text=f"customer_phone")
        self.customer_age_info = MyLabel(text=f"customer_age")
        self.customer_gender_info = MyLabel(text=f"customer_gender")
        self.customer_marstat_info = MyLabel(text=f"customer_marstat")
        self.datetime_created_info = MyLabel(text=f"datetime_created")
        self.info_box = MyGroupBox()
        self.info_layout = MyFormLayout()
        self.info_layout.addRow('Name:', self.customer_name_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Address:', self.customer_address_info)
        self.info_layout.addRow('Barrio:', self.customer_barrio_info)
        self.info_layout.addRow('Town:', self.customer_town_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Phone:', self.customer_phone_info)
        self.info_layout.addRow('Age:', self.customer_age_info)
        self.info_layout.addRow('Gender:', self.customer_gender_info)
        self.info_layout.addRow('Marital status:', self.customer_marstat_info)
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
class MyCustomerController:
    def __init__(self, model: MyCustomerModel, view: MyCustomerView):
        self.v = view
        self.m = model

        self.set_customer_box_conn()
        self.sync_ui()

    def set_customer_box_conn(self):
        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)
        self.v.import_data_button.clicked.connect(self.on_import_data_button_clicked)
        self.v.add_data_button.clicked.connect(self.on_add_data_button_clicked)
        self.v.customer_overview_prev_button.clicked.connect(self.on_overview_prev_button_clicked)
        self.v.customer_overview_next_button.clicked.connect(self.on_overview_next_button_clicked)
        pass
    def on_filter_button_clicked(self): # IDEA: src
        text_filter = self.v.filter_field.text()
        
        self.m.total_page_number = schema.select_customer_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0

        print(self.m.total_page_number, self.m.page_number)

        self.v.customer_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        
        self.populate_overview_table(text=text_filter, page_number=self.m.page_number)
        pass
    
    def on_import_data_button_clicked(self): # IDEA: src
        csv_file_path, _ = QFileDialog.getOpenFileName(self.v, 'Open CSV', qss.csv_folder_path, 'CSV File (*csv)')

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
        QMessageBox.information(self.v, 'Cancelled', 'Import cancelled.')
        pass
    def on_data_import_thread_finished(self):
        QMessageBox.information(self.v, 'Success', 'Import complete.')
        self.v.progress_dialog.close()
        pass
    def on_data_import_thread_invalid(self):
        QMessageBox.critical(self.v, 'Error', 'An error occurred during import.')
        self.v.progress_dialog.close()
        pass

    def on_add_data_button_clicked(self): # IDEA: src
        self.v.set_manage_data_box()
        self.load_combo_box_data()
        self.v.manage_data_dialog.setWindowTitle('Add customer')

        self.v.customer_points_label.hide()
        self.v.customer_points_field.hide()
    
        self.set_manage_data_box_conn(task='add_data')
        self.v.manage_data_dialog.exec()
        pass

    def populate_overview_table(self, text='', page_number=1): # IDEA: src
        self.v.customer_overview_prev_button.setEnabled(page_number > 1)
        self.v.customer_overview_next_button.setEnabled(page_number < self.m.total_page_number)
        self.v.customer_overview_page_label.setText(f"Page {page_number}/{self.m.total_page_number}")

        customer_data = schema.select_data_as_display(text=text, page_number=page_number)

        self.v.customer_overview_table.setRowCount(len(customer_data))

        for i, data in enumerate(customer_data):
            self.v.set_overview_table_act_box()
            customer_name = QTableWidgetItem(f"{data[0]}")
            customer_address = QTableWidgetItem(f"{data[1]}")
            customer_barrio = QTableWidgetItem(f"{data[2]}")
            customer_town = QTableWidgetItem(f"{data[3]}")
            customer_phone = QTableWidgetItem(f"{data[4]}")
            customer_age = QTableWidgetItem(f"{data[5]}")
            customer_gender = QTableWidgetItem(f"{data[6]}")
            customer_marstat = QTableWidgetItem(f"{data[7]}")
            customer_points = QTableWidgetItem(f"{data[8]}")
            datetime_created = QTableWidgetItem(f"{data[9]}")

            self.v.customer_overview_table.setCellWidget(i, 0, self.v.customer_overview_act_box)
            self.v.customer_overview_table.setItem(i, 1, customer_name)
            self.v.customer_overview_table.setItem(i, 2, customer_address)
            self.v.customer_overview_table.setItem(i, 3, customer_barrio)
            self.v.customer_overview_table.setItem(i, 4, customer_town)
            self.v.customer_overview_table.setItem(i, 5, customer_phone)
            self.v.customer_overview_table.setItem(i, 6, customer_age)
            self.v.customer_overview_table.setItem(i, 7, customer_gender)
            self.v.customer_overview_table.setItem(i, 8, customer_marstat)
            self.v.customer_overview_table.setItem(i, 9, customer_points)
            self.v.customer_overview_table.setItem(i, 10, datetime_created)

            self.v.edit_data_button.clicked.connect(lambda _, data=data: self.on_edit_data_button_clicked(data))
            self.v.view_data_button.clicked.connect(lambda _, data=data: self.on_view_data_button_clicked(data))
            self.v.delete_data_button.clicked.connect(lambda _, data=data: self.on_delete_data_button_clicked(data))
        pass
    def on_edit_data_button_clicked(self, data):
        self.v.set_manage_data_box()
        self.load_combo_box_data()
        self.v.manage_data_dialog.setWindowTitle(f"{data[0]}")

        self.v.customer_points_label.show()
        self.v.customer_points_field.show()

        sel_customer_data = schema.select_customer_data(data[0], data[3], data[4], data[5])

        for i, sel_data in enumerate(sel_customer_data):
            self.v.customer_name_field.setText(str(sel_data[0]))
            self.v.customer_address_field.setPlainText(str(sel_data[1]))
            self.v.customer_barrio_field.setCurrentText(str(sel_data[2]))
            self.v.customer_town_field.setCurrentText(str(sel_data[3]))
            self.v.customer_phone_field.setText(str(sel_data[4]))
            self.v.customer_age_field.setText(str(sel_data[5]))
            self.v.customer_gender_field.setCurrentText(str(sel_data[6]))
            self.v.customer_marstat_field.setCurrentText(str(sel_data[7]))
            self.m.sel_customer_id = sel_data[9]
            pass
        
        self.set_manage_data_box_conn(task='edit_data')
        self.v.manage_data_dialog.exec()
        pass
    def on_view_data_button_clicked(self, data):
        self.v.set_view_dialog()
        self.v.view_data_dialog.setWindowTitle(f"{data[0]}")

        self.v.customer_name_info.setText(str(data[0]))
        self.v.customer_address_info.setText(str(data[1]))
        self.v.customer_barrio_info.setText(str(data[2]))
        self.v.customer_town_info.setText(str(data[3]))
        self.v.customer_phone_info.setText(str(data[4]))
        self.v.customer_age_info.setText(str(data[5]))
        self.v.customer_gender_info.setText(str(data[6]))
        self.v.customer_marstat_info.setText(str(data[7]))
        self.v.datetime_created_info.setText(str(data[9]))

        self.set_view_data_box_conn()
        self.v.view_data_dialog.exec()
        pass
    def set_view_data_box_conn(self):
        self.v.view_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.view_data_dialog))
    def on_delete_data_button_clicked(self, data):
        sel_customer_data = schema.select_customer_data(data[0], data[3], data[4], data[5])

        for i, sel_data in enumerate(sel_customer_data):
            customer_name = sel_data[0]
            customer_id = sel_data[9]

        confirm = QMessageBox.warning(self.v, 'Confirm', f"Delete {customer_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_customer_data(customer_id)

            QMessageBox.information(self.v, 'Success', f"{customer_name} has been deleted.")

        self.sync_ui()
        pass

    def on_overview_prev_button_clicked(self):
        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.customer_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass
    def on_overview_next_button_clicked(self):
        if self.m.page_number < self.m.total_page_number:
            self.m.page_number += 1

            self.v.customer_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass

    # IDEA: if the widget uses the same connection
    def set_manage_data_box_conn(self, task):
        self.v.save_data_button.clicked.connect(lambda: self.on_save_data_button_clicked(task))
        self.v.manage_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.manage_data_dialog))
        pass
    def load_combo_box_data(self):
        self.v.set_manage_data_box()
        customer_barrio_data = schema.select_customer_barrio_for_combo_box()
        customer_town_data = schema.select_customer_town_for_combo_box()

        for customer_barrio in customer_barrio_data: self.v.customer_barrio_field.addItems(customer_barrio)
        for customer_town in customer_town_data: self.v.customer_town_field.addItems(customer_town)

        self.v.customer_gender_field.addItem('Male')
        self.v.customer_gender_field.addItem('Female')

        self.v.customer_marstat_field.addItem('Single')
        self.v.customer_marstat_field.addItem('Married')
        self.v.customer_marstat_field.addItem('Separated')
        self.v.customer_marstat_field.addItem('Widowed')
        pass
    def on_save_data_button_clicked(self, task):
        customer_name = self.v.customer_name_field.text()
        customer_address = self.v.customer_address_field.toPlainText()
        customer_barrio = self.v.customer_barrio_field.currentText()
        customer_town = self.v.customer_town_field.currentText()
        customer_phone = self.v.customer_phone_field.text()
        customer_age = self.v.customer_age_field.text()
        customer_gender = self.v.customer_town_field.currentText()
        customer_marstat =  self.v.customer_town_field.currentText()
        customer_points = self.v.customer_points_field.text() if task == 'edit_data' else '0'

        self.m.init_manage_data_entry(
            self.v.manage_data_dialog,
            task, 
            self.v.customer_name_label,
            self.v.customer_barrio_label,
            self.v.customer_town_label,
            self.v.customer_phone_label,
            self.v.customer_age_label,
            self.v.customer_points_label,
            customer_name, 
            customer_address, 
            customer_barrio, 
            customer_town,
            customer_phone,
            customer_age,
            customer_gender,
            customer_marstat,
            customer_points,
        )
            

        self.sync_ui()

    def sync_ui(self):
        text_filter = self.v.filter_field.text()
        self.m.total_page_number = schema.select_customer_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0
        self.populate_overview_table(page_number=self.m.page_number)
        pass
    def close_dialog(self, dialog: QDialog):
        dialog.close()

class MyCustomerWindow(MyGroupBox):
    def __init__(self, name='test', phone='test'):
        super().__init__()

        self.model = MyCustomerModel(name, phone)
        self.view = MyCustomerView(self.model)
        self.controller = MyCustomerController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    customer_window = MyCustomerWindow()

    customer_window.run()

    app.exec()