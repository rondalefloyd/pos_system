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
from src.database.admin.promo import *
from src.widget.admin.promo import *

color_scheme = ColorScheme()

class PromoWindow(MyWidget):
    def __init__(self):
        super().__init__()

        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):
        self.promo_schema = PromoSchema()
        self.my_push_button = MyPushButton()

        self.data_list_curr_page = 1
        self.clicked_data_list_edit_button = None
        self.clicked_data_list_view_button = None
        self.clicked_data_list_delete_button = None
        self.selected_promo_id = None

        self.required_field_indicator = "<font color='red'>-- required</font>"

        self.total_row_count = self.promo_schema.count_promo()
        pass
    def sync_ui(self):
        self.populate_combo_box()
        self.populate_table()

        self.total_data.setText(f'Total promo: {self.promo_schema.count_promo()}')

        self.data_mgt_add_button.setDisabled(False)
        self.form_panel.hide()
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
        
        self.promo_name_field.setText(str(row_value[0]))
        self.promo_type_field.setCurrentText(str(row_value[1]))
        self.discount_percent_field.setText(str(row_value[2]))
        self.description_field.setText(str(row_value[3]))

        self.selected_promo_id = str(row_value[5])
        self.clicked_data_list_edit_button = edit_button

        pass
    def on_data_list_view_button_clicked(self, row_value, view_button):
        self.data_list_view_dialog = MyDialog(object_name='data_list_view_dialog', parent=self)
        self.data_list_view_dialog_layout = MyFormLayout()

        promo_name_info = MyLabel(text=str(row_value[0]))
        promo_type_info = MyLabel(text=str(row_value[1]))
        discount_percent_info = MyLabel(text=str(row_value[2]))
        description_info = MyLabel(text=str(row_value[3]))
        date_created_info = MyLabel(text=str(row_value[4]))

        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Promo name:'), promo_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Promo type:'), promo_type_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Discount percent:'), discount_percent_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Description:'), description_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Date and time created:'), date_created_info)
        self.data_list_view_dialog.setLayout(self.data_list_view_dialog_layout)

        self.data_list_view_dialog.exec()
        pass
    def on_data_list_delete_button_clicked(self, row_value, delete_button):
        confirmation_a = QMessageBox.warning(self, 'Confirm', f'Are you sure you want to delete {row_value[0]}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation_a == QMessageBox.StandardButton.Yes:
            self.selected_promo_id = str(row_value[5])
            self.promo_schema.delete_selected_promo(self.selected_promo_id)

            self.populate_table()
            self.populate_combo_box()
            self.total_data.setText(f'Total promo: {self.promo_schema.count_promo()}')

            QMessageBox.information(self, 'Success', 'Promo has been deleted!')
        pass

    def on_form_close_button_clicked(self):
        self.form_panel.hide()
        self.data_mgt_add_button.setDisabled(False)
        pass
    def on_form_save_new_button_clicked(self):
        # region > convert field input into str
        promo_name = str(self.promo_name_field.text())
        promo_type = str(self.promo_type_field.currentText())
        discount_percent = str(self.discount_percent_field.text())
        description = str(self.description_field.text())
        # endregion

        # region > input_restrictions
        if not discount_percent.replace('.', '', 1).isdigit():
            QMessageBox.critical(self, 'Error', 'Incorrect numerical input.')
            return
        if '' in [
            promo_name,
            promo_type,
            discount_percent
        ]:
            QMessageBox.critical(self, 'Error', 'Must fill required field.')
            return
        # endregion
        
        self.promo_schema.add_new_promo(
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            description=description
        )
        
        self.total_row_count = self.promo_schema.count_promo()
        self.populate_table()
        self.populate_combo_box()
        self.total_data.setText(f'Total promo: {self.promo_schema.count_promo()}')

        QMessageBox.information(self, 'Success', 'New promo has been added!')
        pass
    def on_form_save_edit_button_clicked(self):
        promo_name = str(self.promo_name_field.text())
        promo_type = str(self.promo_type_field.currentText())
        discount_percent = str(self.discount_percent_field.text())
        description = str(self.description_field.text())
        promo_id = str(self.selected_promo_id)

        if not discount_percent.replace('.', '', 1).isdigit():
            QMessageBox.critical(self, 'Error', 'Incorrect numerical input.')
            return
        if '' in [
            promo_name,
            promo_type,
            discount_percent
        ]:
            QMessageBox.critical(self, 'Error', 'Must fill required field.')
            return

        self.promo_schema.edit_selected_promo(
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            description=description,
            promo_id=promo_id
        )

        self.total_row_count = self.promo_schema.count_promo()
        self.populate_table()
        self.populate_combo_box()
        self.on_data_mgt_add_button_clicked()
        self.total_data.setText(f'Total promo: {self.promo_schema.count_promo()}')

        QMessageBox.information(self, 'Success', 'Promo has been edited!')
        pass
    
    def on_data_mgt_sync_button_clicked(self):
        self.sync_ui()

        pass
    def on_data_mgt_import_button_clicked(self):
        csv_file, _ = QFileDialog.getOpenFileName(None, 'Open CSV', '', 'CSV Files (*.csv)')
        
        if csv_file:
            self.manual_import = ManualPromoImport(csv_file=csv_file)
            
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

    def on_promo_name_field_text_changed(self):
        self.promo_name_label.setText(f'Promo name {self.required_field_indicator}') if self.promo_name_field.text() == '' else  self.promo_name_label.setText(f'Promo name')
        pass
    def on_promo_type_field_current_text_changed(self):
        self.promo_type_label.setText(f'Promo type {self.required_field_indicator}') if self.promo_type_field.currentText() == '' else self.promo_type_label.setText(f'Promo type') 
        pass
    def on_discount_percent_field_text_changed(self):
        self.discount_percent_label.setText(f'Discount percent {self.required_field_indicator}') if self.discount_percent_field.text() == '' else self.discount_percent_label.setText(f'Discount percent') 
        pass

    def populate_combo_box(self):
        self.promo_type_field.clear()
        # region > data_list
        promo_type_data = self.promo_schema.list_promo_type()
        # endregion

        # region > field_add_item
        for promo_type in promo_type_data: self.promo_type_field.addItem(promo_type[0])
        # endregion

        pass
    def populate_table(self, text_filter='', current_page=1):
        # region > data_list_clear_contents
        self.data_list_table.clearContents()
        # endregion

        # region > data_list
        promo_data = self.promo_schema.list_promo(text_filter=text_filter, page_number=current_page)
        # endregion

        # region > data_list_pgn_button_set_enabled
        self.data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)
        self.data_list_pgn_next_button.setEnabled(len(promo_data) == 30)
        # endregion

        # region > clicked_data_list_set_disabled
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        self.clicked_data_list_edit_button = None
        # endregion
        
        # region > data_list_table_set_row_count
        self.data_list_table.setRowCount(len(promo_data))
        # endregion

        for row_index, row_value in enumerate(promo_data):
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
            promo_name = QTableWidgetItem(str(row_value[0]))
            promo_type = QTableWidgetItem(str(row_value[1]))
            discount_percent = QTableWidgetItem(str(f'{row_value[2]}%'))
            description = QTableWidgetItem(str(row_value[3]))
            update_ts = QTableWidgetItem(str(row_value[4]))
            # endregion

            # region > set_table_item_alignment
            discount_percent.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            update_ts.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # endregion
        
            # region > set_data_list_table_cells
            self.data_list_table.setCellWidget(row_index, 0, self.data_list_action_panel)
            self.data_list_table.setItem(row_index, 1, promo_name)
            self.data_list_table.setItem(row_index, 2, promo_type)
            self.data_list_table.setItem(row_index, 3, discount_percent)
            self.data_list_table.setItem(row_index, 4, description)
            self.data_list_table.setItem(row_index, 5, update_ts)
            # endregion

        pass

    def show_extra_info_panel(self):
        self.extra_info_panel = MyGroupBox(object_name='extra_info_panel') # head.d
        self.extra_info_panel_layout = MyHBoxLayout(object_name='extra_info_panel_layout')

        # region > extra_info_labels
        self.total_data = MyLabel(object_name='total_data', text=f'Total promo: {self.total_row_count}')
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
        self.primary_info_page = MyGroupBox(object_name='primary_info_page') # head.a.a
        self.primary_info_page_layout = MyFormLayout(object_name='primary_info_page_layout')
        self.promo_name_label = MyLabel(object_name='promo_name_label', text=f'Promo name {self.required_field_indicator}')
        self.promo_type_label = MyLabel(object_name='promo_type_label', text=f'Promo type {self.required_field_indicator}')
        self.discount_percent_label = MyLabel(object_name='discount_percent_label', text=f'Discount percent {self.required_field_indicator}')
        self.description_label = MyLabel(object_name='description_label', text='Description')
        self.promo_name_field = MyLineEdit(object_name='promo_name_field')
        self.promo_type_field = MyComboBox(object_name='promo_type_field')
        self.discount_percent_field = MyLineEdit(object_name='discount_percent_field')
        self.description_field = MyLineEdit(object_name='description_field')
        self.promo_name_field.textChanged.connect(self.on_promo_name_field_text_changed)
        self.promo_type_field.currentTextChanged.connect(self.on_promo_type_field_current_text_changed)
        self.discount_percent_field.textChanged.connect(self.on_discount_percent_field_text_changed)
        self.primary_info_page_layout.insertRow(0, QLabel(f"<font color='{color_scheme.hex_main}'><b>Primary Information</b></font>"))
        self.primary_info_page_layout.insertRow(1, QLabel('<hr>'))
        self.primary_info_page_layout.insertRow(2, self.promo_name_label)
        self.primary_info_page_layout.insertRow(4, self.promo_type_label)
        self.primary_info_page_layout.insertRow(6, self.discount_percent_label)
        self.primary_info_page_layout.insertRow(8, self.description_label)
        self.primary_info_page_layout.insertRow(3, self.promo_name_field)
        self.primary_info_page_layout.insertRow(5, self.promo_type_field)
        self.primary_info_page_layout.insertRow(7, self.discount_percent_field)
        self.primary_info_page_layout.insertRow(9, self.description_field)
        self.primary_info_page.setLayout(self.primary_info_page_layout)
        self.form_page_layout.addRow(self.primary_info_page)
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
        self.data_mgt_add_button = MyPushButton(object_name='data_mgt_add_button', text=' Add Promo')
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
    window = PromoWindow()
    window.show()
    sys.exit(pos_app.exec())
