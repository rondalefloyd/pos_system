import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))
print('sys path: ', os.path.abspath(''))

from src.core.color_scheme import *
from src.core.manual_csv_importer import *
from src.database.admin.customer import *
from src.widget.admin.customer import *

color_scheme = ColorScheme()

class CustomerWindow(MyWidget):
    def __init__(self):
        super().__init__()

        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):
        self.customer_schema = CustomerSchema()
        self.my_push_button = MyPushButton()

        self.data_list_curr_page = 1
        self.clicked_data_list_edit_button = None
        self.clicked_data_list_view_button = None
        self.clicked_data_list_delete_button = None
        self.selected_customer_id = None

        self.required_field_indicator = "<font color='red'>-- required</font>"

        self.total_row_count = self.customer_schema.count_customer()
        pass
    def sync_ui(self):
        self.populate_combo_box()
        self.populate_table()

        self.total_data.setText(f'Total customer: {self.customer_schema.count_customer()}')

        self.data_mgt_add_button.setDisabled(False)
        self.form_panel.hide()

        self.points_label.hide()
        self.currency_amount_label.hide()
        self.points_field.hide()
        self.currency_amount_field.hide()

        self.points_field.setDisabled(True)
        self.currency_amount_field.setDisabled(True)
        pass

    def style_data_list_action_button(self):
        self.data_list_edit_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.data_list_view_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.data_list_delete_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        pass
    def style_data_list_pgn_action_button(self):
        self.data_list_pgn_prev_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.data_list_pgn_next_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        pass
    def style_form_action_button(self):
        self.form_close_button.setStyleSheet(self.my_push_button.form_close_button_ss)
        self.form_save_new_button.setStyleSheet(self.my_push_button.form_save_new_button_ss)
        self.form_save_edit_button.setStyleSheet(self.my_push_button.form_save_edit_button_ss)
    def style_data_mgt_action_button(self):
        self.data_mgt_sync_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        self.data_mgt_import_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        self.data_mgt_add_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        pass

    def on_data_list_edit_button_clicked(self, row_value, edit_button):
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        edit_button.setDisabled(True)
        self.data_mgt_add_button.setDisabled(False)

        self.form_save_new_button.hide()
        self.form_save_edit_button.show()
        self.form_panel.show()
        
        self.customer_name_field.setText(str(row_value[0]))
        self.address_field.setCurrentText(str(row_value[1]))
        self.barrio_field.setCurrentText(str(row_value[2]))
        self.town_field.setCurrentText(str(row_value[3]))
        self.phone_field.setText(str(row_value[4]))
        self.age_field.setText(str(row_value[5]))
        self.gender_field.setCurrentText(str(row_value[6]))
        self.marital_status_field.setCurrentText(str(row_value[7]))
        self.reward_name_field.setCurrentText(str(row_value[8]))

        self.selected_customer_id = str(row_value[10])
        self.clicked_data_list_edit_button = edit_button

        pass
    def on_data_list_view_button_clicked(self, row_value, view_button):
        self.data_list_view_dialog = MyDialog(object_name='data_list_view_dialog', parent=self)
        self.data_list_view_dialog_layout = MyFormLayout()

        customer_name_info = MyLabel(text=str(row_value[0]))
        address_info = MyLabel(text=str(row_value[1]))
        barrio_info = MyLabel(text=str(row_value[2]))
        town_info = MyLabel(text=str(row_value[3]))
        phone_info = MyLabel(text=str(row_value[4]))
        age_info = MyLabel(text=str(row_value[5]))
        gender_info = MyLabel(text=str(row_value[6]))
        marital_status_info = MyLabel(text=str(row_value[7]))
        reward_name_info = MyLabel(text=str(row_value[8]))

        date_created_info = MyLabel(text=str(row_value[9]))

        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Customer name:'), customer_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Address:'), address_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Barrio:'), barrio_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Town:'), town_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Phone:'), phone_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Age:'), age_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Gender:'), gender_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Marital status:'), marital_status_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Reward name:'), reward_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Date and time created:'), date_created_info)
        self.data_list_view_dialog.setLayout(self.data_list_view_dialog_layout)

        self.data_list_view_dialog.exec()
        pass
    def on_data_list_delete_button_clicked(self, row_value, delete_button):
        confirmation_a = QMessageBox.warning(self, 'Confirm', f'Are you sure you want to delete {row_value[0]}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation_a == QMessageBox.StandardButton.Yes:
            self.selected_customer_id = str(row_value[10])
            self.customer_schema.delete_selected_customer(self.selected_customer_id)

            self.populate_table()
            self.populate_combo_box()
            self.total_data.setText(f'Total customer: {self.customer_schema.count_customer()}')

            QMessageBox.information(self, 'Success', 'Customer has been deleted!')
        pass

    def on_form_close_button_clicked(self):
        self.form_panel.hide()
        self.data_mgt_add_button.setDisabled(False)
        pass
    def on_form_save_new_button_clicked(self):
        # region > convert field input into str
        customer_name = str(self.customer_name_field.text())
        address = str(self.address_field.currentText())
        barrio = str(self.barrio_field.currentText())
        town = str(self.town_field.currentText())
        phone = str(self.phone_field.text())
        age = str(self.age_field.text())
        gender = str(self.gender_field.currentText())
        marital_status = str(self.marital_status_field.currentText())
        reward_name = str(self.reward_name_field.currentText())
        # endregion

        # region > input_restrictions
        if not (age.replace('.', '', 1).isdigit() and phone.replace('.', '', 1).isdigit()):
            QMessageBox.critical(self, 'Error', 'Incorrect numerical input.')
            return
        if '' in [
            customer_name,
            barrio,
            town,
            phone,
            age,
            gender,
            marital_status,
        ]:
            QMessageBox.critical(self, 'Error', 'Must fill required field.')
            return
        # endregion
        
        self.customer_schema.add_new_customer(
            customer_name=customer_name,
            address=address,
            barrio=barrio,
            town=town,
            phone=phone,
            age=age,
            gender=gender,
            marital_status=marital_status,
            reward_name=reward_name
        )
        
        self.total_row_count = self.customer_schema.count_customer()
        self.populate_table()
        self.populate_combo_box()
        self.total_data.setText(f'Total customer: {self.customer_schema.count_customer()}')

        QMessageBox.information(self, 'Success', 'New customer has been added!')
        pass
    def on_form_save_edit_button_clicked(self):
        # region > convert field input into str
        customer_name = str(self.customer_name_field.text())
        address = str(self.address_field.currentText())
        barrio = str(self.barrio_field.currentText())
        town = str(self.town_field.currentText())
        phone = str(self.phone_field.text())
        age = str(self.age_field.text())
        gender = str(self.gender_field.currentText())
        marital_status = str(self.marital_status_field.currentText())
        reward_name = str(self.reward_name_field.currentText())

        customer_id = str(self.selected_customer_id)
        # endregion

        # region > input_restrictions
        if not (age.replace('.', '', 1).isdigit() and phone.replace('.', '', 1).isdigit()):
            QMessageBox.critical(self, 'Error', 'Incorrect numerical input.')
            return
        if '' in [
            customer_name,
            barrio,
            town,
            phone,
            age,
            gender,
            marital_status,
        ]:
            QMessageBox.critical(self, 'Error', 'Must fill required field.')
            return
        # endregion

        self.customer_schema.edit_selected_customer(
            customer_name=customer_name,
            address=address,
            barrio=barrio,
            town=town,
            phone=phone,
            age=age,
            gender=gender,
            marital_status=marital_status,
            reward_name=reward_name,
            customer_id=customer_id
        )

        self.total_row_count = self.customer_schema.count_customer()
        self.populate_table()
        self.populate_combo_box()
        self.on_data_mgt_add_button_clicked()
        self.total_data.setText(f'Total customer: {self.customer_schema.count_customer()}')

        QMessageBox.information(self, 'Success', 'Customer has been edited!')
        pass
    
    def on_data_mgt_sync_button_clicked(self):
        self.sync_ui()

        pass
    def on_data_mgt_import_button_clicked(self):
        csv_file, _ = QFileDialog.getOpenFileName(None, 'Open CSV', '', 'CSV Files (*.csv)')
        
        if csv_file:
            self.manual_import = ManualCustomerImport(csv_file=csv_file)
            
            self.manual_import.progress_signal.connect(self.manual_import.update_progress)
            self.manual_import.finished_signal.connect(self.manual_import.import_finished)
            self.manual_import.finished_signal.connect(self.sync_ui)
            self.manual_import.error_signal.connect(self.manual_import.import_error)
            self.manual_import.start()
        else:
            pass
        pass
    def on_data_mgt_add_button_clicked(self):
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        self.data_mgt_add_button.setDisabled(True)

        self.form_save_new_button.show()
        self.form_save_edit_button.hide()
        self.form_panel.show()
            
        self.clicked_data_list_edit_button = None
        pass
    
    def on_data_list_pgn_prev_button_clicked(self):
        self.on_data_mgt_add_button_clicked() if self.form_panel.isVisible() == True else None
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        
        if self.data_list_curr_page > 1:
            self.data_list_curr_page -= 1
            self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')

        self.populate_table(text_filter=self.text_filter_field.text(), current_page=self.data_list_curr_page)

        self.clicked_data_list_edit_button = None
        pass
    def on_data_list_pgn_next_button_clicked(self):
        self.on_data_mgt_add_button_clicked() if self.form_panel.isVisible() == True else None
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        
        self.data_list_curr_page += 1
        self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')
        
        self.populate_table(text_filter=self.text_filter_field.text(), current_page=self.data_list_curr_page)
        
        self.clicked_data_list_edit_button = None
        pass
        pass

    def on_text_filter_field_text_changed(self):
        self.data_list_curr_page = 1
        self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')
        self.populate_table(text_filter=str(self.text_filter_field.text()), current_page=self.data_list_curr_page)
        pass

    def on_customer_name_field_text_changed(self):
        self.customer_name_label.setText(f'Customer name {self.required_field_indicator}') if self.customer_name_field.text() == '' else  self.customer_name_label.setText(f'Customer name')
        pass
    def on_barrio_field_current_text_changed(self):
        self.barrio_label.setText(f'Barrio {self.required_field_indicator}') if self.barrio_field.currentText() == '' else  self.barrio_label.setText(f'Barrio')
        pass
    def on_town_field_current_text_changed(self):
        self.town_label.setText(f'Town {self.required_field_indicator}') if self.town_field.currentText() == '' else  self.town_label.setText(f'Town')
        pass
    def on_phone_field_text_changed(self):
        self.phone_label.setText(f'Phone {self.required_field_indicator}') if self.phone_field.text() == '' else  self.phone_label.setText(f'Phone')
        pass
    def on_age_field_text_changed(self):
        self.age_label.setText(f'Age {self.required_field_indicator}') if self.age_field.text() == '' else  self.age_label.setText(f'Age')
        pass
    def on_gender_field_current_text_changed(self):
        self.gender_label.setText(f'Gender {self.required_field_indicator}') if self.gender_field.currentText() == '' else  self.gender_label.setText(f'Gender')
        pass
    def on_marital_status_field_current_text_changed(self):
        self.marital_status_label.setText(f'Marital status {self.required_field_indicator}') if self.marital_status_field.currentText() == '' else  self.marital_status_label.setText(f'Marital status')
        pass
    def on_reward_name_field_current_text_changed(self):
        if self.reward_name_field.currentText() == 'No reward':
            self.points_label.hide()
            self.currency_amount_label.hide()
            self.points_field.hide()
            self.currency_amount_field.hide()
        else:
            self.points_label.show()
            self.currency_amount_label.show()
            self.points_field.show()
            self.currency_amount_field.show()
        pass

    def populate_combo_box(self):
        self.reward_name_field.clear()
        self.gender_field.clear()
        self.marital_status_field.clear()

        # region > data_list
        reward_name_data = self.customer_schema.list_reward()
        # endregion

        self.gender_field.addItem('Male')
        self.gender_field.addItem('Female')

        self.marital_status_field.addItem('Single')
        self.marital_status_field.addItem('Married')
        self.marital_status_field.addItem('Separated')
        self.marital_status_field.addItem('Widowed')

        # region > field_add_item
        self.reward_name_field.addItem('No reward')
        for reward_name in reward_name_data: self.reward_name_field.addItem(reward_name[0])
        # endregion

        pass
    def populate_table(self, text_filter='', current_page=1):
        # region > data_list_clear_contents
        self.data_list_table.clearContents()
        # endregion

        # region > data_list
        customer_data = self.customer_schema.list_customer(text_filter=text_filter, page_number=current_page)
        # endregion

        # region > data_list_pgn_button_set_enabled
        self.data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)
        self.data_list_pgn_next_button.setEnabled(len(customer_data) == 30)
        # endregion

        # region > clicked_data_list_set_disabled
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        self.clicked_data_list_edit_button = None
        # endregion
        
        # region > data_list_table_set_row_count
        self.data_list_table.setRowCount(len(customer_data))
        # endregion

        for row_index, row_value in enumerate(customer_data):
            # region > data_list_action
            self.data_list_action_panel = MyGroupBox(object_name='data_list_action_panel') # head.a
            self.data_list_action_panel_layout = MyHBoxLayout(object_name='data_list_action_panel_layout')
            
            # region > set_data_list_action_buttons
            self.data_list_edit_button = MyPushButton(object_name='data_list_edit_button', text='Edit')
            self.data_list_view_button = MyPushButton(object_name='data_list_view_button', text='View')
            self.data_list_delete_button = MyPushButton(object_name='data_list_delete_button')
            # endregion

            # region > data_list_action_button_connections
            self.data_list_edit_button.clicked.connect(lambda _, row_value=row_value, edit_button=self.data_list_edit_button: self.on_data_list_edit_button_clicked(row_value, edit_button))
            self.data_list_view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.data_list_view_button: self.on_data_list_view_button_clicked(row_value, view_button))
            self.data_list_delete_button.clicked.connect(lambda _, row_value=row_value, delete_button=self.data_list_delete_button: self.on_data_list_delete_button_clicked(row_value, delete_button))
            # endregion

            # region > style_data_list_action_buttons
            self.style_data_list_action_button()
            # endregion

            self.data_list_action_panel_layout.addWidget(self.data_list_edit_button)
            self.data_list_action_panel_layout.addWidget(self.data_list_view_button)
            self.data_list_action_panel_layout.addWidget(self.data_list_delete_button)
            self.data_list_action_panel.setLayout(self.data_list_action_panel_layout)
            # endregion

            # region > set_table_item_values
            customer_name = QTableWidgetItem(str(row_value[0]))
            address = QTableWidgetItem(str(row_value[1]))
            barrio = QTableWidgetItem(str(row_value[2]))
            town = QTableWidgetItem(str(row_value[3]))
            phone = QTableWidgetItem(str(row_value[4]))
            age = QTableWidgetItem(str(row_value[5]))
            gender = QTableWidgetItem(str(row_value[6]))
            marital_status = QTableWidgetItem(str(row_value[7]))
            reward_name = QTableWidgetItem(str(row_value[8]))
            update_ts = QTableWidgetItem(str(row_value[9]))
            # endregion

            # region > set_table_item_alignment
            phone.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            age.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            gender.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            marital_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            update_ts.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # endregion
        
            # region > set_data_list_table_cells
            self.data_list_table.setCellWidget(row_index, 0, self.data_list_action_panel)
            self.data_list_table.setItem(row_index, 1, customer_name)
            self.data_list_table.setItem(row_index, 2, address)
            self.data_list_table.setItem(row_index, 3, barrio)
            self.data_list_table.setItem(row_index, 4, town)
            self.data_list_table.setItem(row_index, 5, phone)
            self.data_list_table.setItem(row_index, 6, age)
            self.data_list_table.setItem(row_index, 7, gender)
            self.data_list_table.setItem(row_index, 8, marital_status)
            self.data_list_table.setItem(row_index, 9, reward_name)
            self.data_list_table.setItem(row_index, 10, update_ts)
            # endregion

        pass

    def show_extra_info_panel(self):
        self.extra_info_panel = MyGroupBox(object_name='extra_info_panel') # head.d
        self.extra_info_panel_layout = MyHBoxLayout(object_name='extra_info_panel_layout')

        # region > extra_info_labels
        self.total_data = MyLabel(object_name='total_data', text=f'Total customer: {self.total_row_count}')
        # endregion

        self.extra_info_panel_layout.addWidget(self.total_data,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.extra_info_panel.setLayout(self.extra_info_panel_layout)
        pass
    def show_form_panel(self):
        self.form_panel = MyGroupBox(object_name='form_panel')
        self.form_panel_layout = MyVBoxLayout(object_name='form_panel_layout')

        # region > form_scroll_area
        self.form_scroll_area = MyScrollArea(object_name='form_scroll_area') # head.a
        self.form_page = MyGroupBox(object_name='form_page')
        self.form_page_layout = MyFormLayout(object_name='form_page_layout')

        # region > primary_info_page
        self.primary_info_page = MyGroupBox(object_name='primary_info_page') # head.a.a
        self.primary_info_page_layout = MyFormLayout(object_name='primary_info_page_layout')

        self.customer_name_label = MyLabel(object_name='customer_name_label', text=f'Customer name {self.required_field_indicator}')
        self.address_label = MyLabel(object_name='address_label', text=f'Address')
        self.barrio_label = MyLabel(object_name='barrio_label', text=f'Barrio {self.required_field_indicator}')
        self.town_label = MyLabel(object_name='town_label', text=f'Town {self.required_field_indicator}')
        self.phone_label = MyLabel(object_name='phone_label', text=f'Phone {self.required_field_indicator}')
        self.age_label = MyLabel(object_name='age_label', text=f'Age {self.required_field_indicator}')
        self.gender_label = MyLabel(object_name='gender_label', text=f'Gender {self.required_field_indicator}')
        self.marital_status_label = MyLabel(object_name='marital_status_label', text=f'Marital status {self.required_field_indicator}')

        self.customer_name_field = MyLineEdit(object_name='customer_name_field')
        self.address_field = MyComboBox(object_name='address_field')
        self.barrio_field = MyComboBox(object_name='barrio_field')
        self.town_field = MyComboBox(object_name='town_field')
        self.phone_field = MyLineEdit(object_name='phone_field')
        self.age_field = MyLineEdit(object_name='age_field')
        self.gender_field = MyComboBox(object_name='gender_field')
        self.marital_status_field = MyComboBox(object_name='marital_status_field')

        self.customer_name_field.textChanged.connect(self.on_customer_name_field_text_changed)
        self.barrio_field.currentTextChanged.connect(self.on_barrio_field_current_text_changed)
        self.town_field.currentTextChanged.connect(self.on_town_field_current_text_changed)
        self.phone_field.textChanged.connect(self.on_phone_field_text_changed)
        self.age_field.textChanged.connect(self.on_age_field_text_changed)
        self.gender_field.currentTextChanged.connect(self.on_gender_field_current_text_changed)
        self.marital_status_field.currentTextChanged.connect(self.on_marital_status_field_current_text_changed)

        self.primary_info_page_layout.insertRow(0, QLabel(f"<font color='{color_scheme.hex_main}'><b>Primary Information</b></font>"))
        self.primary_info_page_layout.insertRow(1, QLabel('<hr>'))

        self.primary_info_page_layout.insertRow(2, self.customer_name_label)
        self.primary_info_page_layout.insertRow(4, self.address_label)
        self.primary_info_page_layout.insertRow(6, self.barrio_label)
        self.primary_info_page_layout.insertRow(8, self.town_label)
        self.primary_info_page_layout.insertRow(10, self.phone_label)
        self.primary_info_page_layout.insertRow(12, self.age_label)
        self.primary_info_page_layout.insertRow(14, self.gender_label)
        self.primary_info_page_layout.insertRow(16, self.marital_status_label)

        self.primary_info_page_layout.insertRow(3, self.customer_name_field)
        self.primary_info_page_layout.insertRow(5, self.address_field)
        self.primary_info_page_layout.insertRow(7, self.barrio_field)
        self.primary_info_page_layout.insertRow(9, self.town_field)
        self.primary_info_page_layout.insertRow(11, self.phone_field)
        self.primary_info_page_layout.insertRow(13, self.age_field)
        self.primary_info_page_layout.insertRow(15, self.gender_field)
        self.primary_info_page_layout.insertRow(17, self.marital_status_field)

        self.primary_info_page.setLayout(self.primary_info_page_layout)
        # endregion
        # region > reward_info_page
        self.reward_info_page = MyGroupBox(object_name='reward_info_page') # head.a.a
        self.reward_info_page_layout = MyFormLayout(object_name='reward_info_page_layout')

        self.reward_name_label = MyLabel(object_name='reward_name_label', text=f'Reward name')
        self.points_label = MyLabel(object_name='points_label', text=f'Points')
        self.currency_amount_label = MyLabel(object_name='currency_amount_label', text=f'Currency amount')

        self.reward_name_field = MyComboBox(object_name='reward_name_field')
        self.points_field = MyLineEdit(object_name='points_field')
        self.currency_amount_field = MyLineEdit(object_name='currency_amount_field')

        self.reward_name_field.currentTextChanged.connect(self.on_reward_name_field_current_text_changed)

        self.reward_info_page_layout.insertRow(0, QLabel(f"<font color='{color_scheme.hex_main}'><b>Reward</b></font>"))
        self.reward_info_page_layout.insertRow(1, QLabel('<hr>'))

        self.reward_info_page_layout.insertRow(2, self.reward_name_label)
        self.reward_info_page_layout.insertRow(4, self.points_label)
        self.reward_info_page_layout.insertRow(6, self.currency_amount_label)

        self.reward_info_page_layout.insertRow(3, self.reward_name_field)
        self.reward_info_page_layout.insertRow(5, self.points_field)
        self.reward_info_page_layout.insertRow(7, self.currency_amount_field)


        self.reward_info_page.setLayout(self.reward_info_page_layout)
        # endregion

        self.form_page_layout.addRow(self.primary_info_page)
        self.form_page_layout.addRow(self.reward_info_page)
        self.form_page.setLayout(self.form_page_layout)
        self.form_scroll_area.setWidget(self.form_page)
        # endregion
        # region > form_action
        self.form_action_panel = MyGroupBox(object_name='form_action_panel') # head.b
        self.form_action_panel_layout = MyHBoxLayout(object_name='form_action_panel_layout')
        self.form_close_button = MyPushButton(object_name='form_close_button', text='Close')
        self.form_save_new_button = MyPushButton(object_name='form_save_new_button', text='SAVE NEW')
        self.form_save_edit_button = MyPushButton(object_name='form_save_edit_button', text='SAVE EDIT')
        self.form_action_panel_layout.addWidget(self.form_close_button)
        self.form_action_panel_layout.addWidget(self.form_save_new_button)
        self.form_action_panel_layout.addWidget(self.form_save_edit_button)
        self.form_action_panel.setLayout(self.form_action_panel_layout)
        # endregion

        # region > form_button_connections
        self.form_close_button.clicked.connect(self.on_form_close_button_clicked)
        self.form_save_new_button.clicked.connect(self.on_form_save_new_button_clicked)
        self.form_save_edit_button.clicked.connect(self.on_form_save_edit_button_clicked)
        # endregion
        
        # region > style_form_buttons
        self.style_form_action_button()
        # endregion

        self.form_panel_layout.addWidget(self.form_scroll_area)
        self.form_panel_layout.addWidget(self.form_action_panel)
        self.form_panel.setLayout(self.form_panel_layout)
        pass
    def show_content_panel(self):
        self.content_panel = MyGroupBox(object_name='content_panel')
        self.content_panel_layout = MyGridLayout(object_name='content_panel_layout')

        # region > text_filter
        self.text_filter_field = MyLineEdit(object_name='text_filter_field') # head.a
        # endregion
        # region > data_mgt_action
        self.data_mgt_action_panel = MyGroupBox(object_name='data_mgt_action_panel') # head.b
        self.data_mgt_action_panel_layout = MyHBoxLayout(object_name='data_mgt_action_panel_layout')
        self.data_mgt_sync_button = MyPushButton(object_name='data_mgt_sync_button')
        self.data_mgt_import_button = MyPushButton(object_name='data_mgt_import_button')
        self.data_mgt_add_button = MyPushButton(object_name='data_mgt_add_button', text=' Add Customer')
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_sync_button)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_import_button)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_add_button)
        self.data_mgt_action_panel.setLayout(self.data_mgt_action_panel_layout)
        # endregion
        # region > data_list_sorter
        self.data_list_sorter_tab = MyTabWidget(object_name='data_list_sorter_tab') # head.c
        self.data_list_pgn_panel = MyGroupBox(object_name='data_list_pgn_panel') # head.c.a
        self.data_list_pgn_panel_layout = MyVBoxLayout(object_name='data_list_pgn_panel_layout')
        self.data_list_table = MyTableWidget(object_name='data_list_table')
        self.data_list_pgn_action_panel = MyGroupBox(object_name='data_list_pgn_action_panel')
        self.data_list_pgn_action_panel_layout = MyGridLayout(object_name='data_list_pgn_action_panel_layout')
        self.data_list_pgn_prev_button = MyPushButton(object_name='data_list_pgn_prev_button')
        self.data_list_pgn_page = MyLabel(object_name='data_list_pgn_page', text='Page 1')
        self.data_list_pgn_next_button = MyPushButton(object_name='data_list_pgn_next_button')
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_prev_button,0,0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_page,0,1, Qt.AlignmentFlag.AlignCenter)
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_next_button,0,2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.data_list_pgn_action_panel.setLayout(self.data_list_pgn_action_panel_layout)
        self.data_list_pgn_panel_layout.addWidget(self.data_list_table)
        self.data_list_pgn_panel_layout.addWidget(self.data_list_pgn_action_panel)
        self.data_list_pgn_panel.setLayout(self.data_list_pgn_panel_layout)
        self.data_list_sorter_tab.addTab(self.data_list_pgn_panel, 'Overview')
        # endregion

        # region > content_button_connections
        self.data_mgt_sync_button.clicked.connect(self.on_data_mgt_sync_button_clicked)
        self.data_mgt_import_button.clicked.connect(self.on_data_mgt_import_button_clicked)
        self.data_mgt_add_button.clicked.connect(self.on_data_mgt_add_button_clicked)
        self.data_list_pgn_prev_button.clicked.connect(self.on_data_list_pgn_prev_button_clicked)
        self.data_list_pgn_next_button.clicked.connect(self.on_data_list_pgn_next_button_clicked)
        # endregion

        # region > content_text_filter_connection
        self.text_filter_field.textChanged.connect(self.on_text_filter_field_text_changed)
        # endregion

        # region > style_content_buttons
        self.style_data_mgt_action_button()
        self.style_data_list_pgn_action_button()
        # endregion

        self.content_panel_layout.addWidget(self.text_filter_field,0,0)
        self.content_panel_layout.addWidget(self.data_mgt_action_panel,0,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.content_panel_layout.addWidget(self.data_list_sorter_tab,1,0,1,2)
        self.content_panel.setLayout(self.content_panel_layout)
        pass
    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(object_name='main_panel_layout')

        self.show_content_panel()
        self.show_form_panel()
        self.show_extra_info_panel()

        self.main_panel_layout.addWidget(self.content_panel,0,0)
        self.main_panel_layout.addWidget(self.form_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.extra_info_panel,1,0)
        self.setLayout(self.main_panel_layout)
    
if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = CustomerWindow()
    window.show()
    sys.exit(pos_app.exec())
