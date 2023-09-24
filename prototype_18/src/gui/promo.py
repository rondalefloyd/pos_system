import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.csv_importer import *
from database.promo import *
from widget.promo import *

class PromoWindow(MyWidget):
    def __init__(self):
        super().__init__(widget_ref='promo_window')

        self.show_main_panel()
        self.default_values()
        self.on_refresh_data_button_clicked()


    def default_values(self):
        self.promo_schema = PromoSchema()

        self.current_page = 1

        self.clicked_edit_button = None
        self.clicked_view_button = None
        self.clicked_delete_button = None

        # checkpoint!!!
        
        pass

    # region -- on_push_button_clicked functions
    def on_edit_button_clicked(self, row_value, edit_button):
        self.scrolling_manage_data_panel.show()
        self.add_data_button.setDisabled(False)
        self.save_edit_button.show()
        self.save_new_button.hide()

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        edit_button.setDisabled(True)

        # region -- set values
        self.promo_name_field.setText(str(row_value[0]))
        self.promo_type_field.setCurrentText(str(row_value[1]))
        self.discount_percent_field.setText(str(row_value[2]))
        self.description_field.setPlainText(str(row_value[3]))
        self.selected_promo_id = int(row_value[5])
        # endregion -- set values

        self.clicked_edit_button = edit_button
        pass
    def on_view_button_clicked(self, row_value, view_button):
        self.clicked_view_button.setDisabled(False) if self.clicked_view_button else None
        view_button.setDisabled(True)
        self.clicked_view_button = view_button

        # region -- view_panel_dialog = MyDialog()
        view_panel_dialog = MyDialog(dialog_ref='view_panel_dialog', parent=self)
        view_panel_layout = MyFormLayout()
        promo_name_value = MyLabel(text=f'{row_value[0]}')
        promo_type_value = MyLabel(text=f'{row_value[1]}')
        discount_percent_value = MyLabel(text=f'{row_value[2]}')
        description_value = MyLabel(text=f'{row_value[3]}')
        date_created_value = MyLabel(text=f'{row_value[4]}')

        view_panel_layout.addRow('Promo name: ', promo_name_value)
        view_panel_layout.addRow('Promo type: ', promo_type_value)
        view_panel_layout.addRow('Discount percent: ', discount_percent_value)
        view_panel_layout.addRow('Description: ', description_value)
        view_panel_layout.addRow(QLabel('<hr>'))
        view_panel_layout.addRow('Date created: ', date_created_value)
        view_panel_dialog.setLayout(view_panel_layout)
        view_panel_dialog.exec()
        # endregion -- view_panel_dialog = MyDialog()

        self.clicked_view_button.setDisabled(False) if view_panel_dialog.isVisible() == False else None

        pass
    def on_delete_button_clicked(self, row_value, delete_button):
        self.clicked_delete_button.setDisabled(False) if self.clicked_delete_button else None
        delete_button.setDisabled(True)
        self.clicked_delete_button = delete_button

        # region -- confirmation_a = QMessageBox.warning()
        confirmation_a = QMessageBox.warning(self, 'Confirm', f'Are you sure you want to delete {row_value[0]}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation_a == QMessageBox.StandardButton.Yes:
            selected_promo_id = str(row_value[5])
            self.promo_schema.delete_selected_promo(selected_promo_id)
        # endregion -- confirmation_a = QMessageBox.warning()

        self.clicked_delete_button.setDisabled(False) if self.clicked_delete_button else None
        self.clicked_delete_button = None

        pass

    def on_discard_button_clicked(self):
        self.add_data_button.setDisabled(False)
        self.scrolling_manage_data_panel.hide()

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None

        self.clicked_edit_button = None
        pass
    def on_save_new_button_clicked(self):
        promo_name = str(self.promo_name_field.text())
        promo_type = str(self.promo_type_field.currentText())
        discount_percent = float(self.discount_percent_field.text())
        description = str(self.description_field.toPlainText())

        self.promo_schema.add_new_promo(
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            description=description
        )

        QMessageBox.information(self, 'Success', 'New promo added.')
        pass
    def on_save_edit_button_clicked(self):
        promo_name = str(self.promo_name_field.text())
        promo_type = str(self.promo_type_field.currentText())
        discount_percent = float(self.discount_percent_field.text())
        description = str(self.description_field.toPlainText())
        promo_id = self.selected_promo_id

        self.promo_schema.edit_selected_promo(
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            description=description,
            promo_id=promo_id
        )

        QMessageBox.information(self, 'Success', 'New promo added.')
        pass

    def on_overview_pagination_prev_button_clicked(self):
        self.on_add_data_button_clicked() if self.scrolling_manage_data_panel.isVisible() == True else None
        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        
        # region -- if self.current_page > 1:
        if self.current_page > 1:
            self.current_page -= 1
            self.overview_pagination_page.setText(f'Page {self.current_page}')

        self.populate_table(current_page=self.current_page)
        # endregion -- if self.current_page > 1:

        self.clicked_edit_button = None
        pass
    def on_overview_pagination_next_button_clicked(self):
        self.on_add_data_button_clicked() if self.scrolling_manage_data_panel.isVisible() == True else None
        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        
        # region -- self.current_page += 1
        self.current_page += 1
        self.overview_pagination_page.setText(f'Page {self.current_page}')
        
        self.populate_table(current_page=self.current_page)
        # endregion -- self.current_page += 1
        
        self.clicked_edit_button = None
        pass

    def on_refresh_data_button_clicked(self):
        self.current_page = 1
        self.clicked_edit_button = None
        self.clicked_view_button = None
        self.clicked_delete_button = None

        self.populate_table()
        self.populate_combo_box()

        self.on_add_data_button_clicked() if self.scrolling_manage_data_panel.isVisible() == True else None

        self.total_promo_count.setText(f'Total promo: {self.promo_schema.count_promo()}')
        self.overview_pagination_page.setText(f'Page {self.current_page}')

            
        pass
    def on_delete_all_data_button_clicked(self):
        pass
    def on_import_data_button_clicked(self):
        self.import_data_button.setDisabled(True)

        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')

        print(csv_file)
        if csv_file:
            data_frame = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)
            
            self.import_thread = CSVImporter(
                csv_file=csv_file,
                import_data_button=self.import_data_button
            )
            self.import_thread.progress_signal.connect(self.import_thread.update_progress)
            self.import_thread.finished_signal.connect(self.import_thread.import_finished)
            self.import_thread.error_signal.connect(self.import_thread.import_error)
            self.import_thread.start()
            # print(data_frame)
            pass
        else:
            self.import_data_button.setDisabled(False)
        pass
    def on_add_data_button_clicked(self):
        self.add_data_button.setDisabled(True)
        self.scrolling_manage_data_panel.show()
        self.save_edit_button.hide()
        self.save_new_button.show()

        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None

        self.promo_name_field.setText('')
        self.promo_type_field.setCurrentText('')
        self.discount_percent_field.setText('')
        self.description_field.setPlainText('')

        self.clicked_edit_button = None
        pass
    # endregion -- on_push_button_clicked functions

    def populate_combo_box(self):
        promo_type_data = self.promo_schema.list_promo_type()
        for promo_type in promo_type_data: self.promo_type_field.addItem(promo_type[0])
        pass
    def populate_table(self, current_page=1):
        promo_data = self.promo_schema.list_promo(page_number=current_page)
        
        # region -- pagination_button.setEnabled()
        self.overview_pagination_prev_button.setEnabled(self.current_page > 1)
        self.overview_pagination_next_button.setEnabled(len(promo_data) == 30)
        # endregion -- pagination_button.setEnabled()

        # region -- self.clicked_edit_button.setDisabled()
        self.clicked_edit_button.setDisabled(False) if self.clicked_edit_button else None
        self.clicked_edit_button = None
        # endregion -- self.clicked_edit_button.setDisabled()
        
        self.overview_table.setRowCount(len(promo_data))

        for row_index, row_value in enumerate(promo_data):
            # region -- assign values
            # region -- action_nav = MyGroupBox()
            action_nav = MyWidget()
            action_nav_layout = MyHBoxLayout(hbox_layout_ref='action_nav_layout')
            self.edit_button = MyPushButton(push_button_ref='edit_button', text='Edit')
            self.edit_button.clicked.connect(lambda _, row_value=row_value, edit_button=self.edit_button: self.on_edit_button_clicked(row_value, edit_button))
            self.view_button = MyPushButton(push_button_ref='view_button', text='View')
            self.view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.view_button: self.on_view_button_clicked(row_value, view_button))
            self.delete_button = MyPushButton(push_button_ref='delete_button', text='Delete')
            self.delete_button.clicked.connect(lambda _, row_value=row_value, delete_button=self.delete_button: self.on_delete_button_clicked(row_value, delete_button))
            action_nav_layout.addWidget(self.edit_button)
            action_nav_layout.addWidget(self.view_button)
            action_nav_layout.addWidget(self.delete_button)
            action_nav.setLayout(action_nav_layout)
            # endregion -- action_nav = MyGroupBox()
            
            promo_name = MyTableWidgetItem(table_widget_item_ref='promo_name', text=str(row_value[0]))
            promo_type = MyTableWidgetItem(table_widget_item_ref='promo_type', text=str(row_value[1]))
            discount_percent = MyTableWidgetItem(table_widget_item_ref='discount_percent', text=str(f'₱{row_value[2]}'))
            description = MyTableWidgetItem(table_widget_item_ref='description', text=str(row_value[3]))
            # endregion -- assign values

            self.overview_table.setCellWidget(row_index, 0, action_nav)
            self.overview_table.setItem(row_index, 1, promo_name)
            self.overview_table.setItem(row_index, 2, promo_type)
            self.overview_table.setItem(row_index, 3, discount_percent)
            self.overview_table.setItem(row_index, 4, description)
        pass

    def show_operation_panel(self):
        self.operation_status_panel = MyGroupBox(group_box_ref='operation_status_panel')
        self.operation_status_layout = MyHBoxLayout(hbox_layout_ref='operation_status_layout')

        self.total_promo_count = MyLabel(text=f'Total promo: {self.promo_schema.count_promo()}')
        self.operation_status_layout.addWidget(self.total_promo_count)
        self.operation_status_panel.setLayout(self.operation_status_layout)
        pass
    def show_manage_data_panel(self):
        self.scrolling_manage_data_panel = MyScrollArea(scroll_area_ref='scrolling_manage_data_panel')
        self.manage_data_panel = MyWidget(widget_ref='manage_data_panel')
        self.manage_data_panel_layout = MyFormLayout()
        
        # region -- self.primary_form = MyGroupBox()
        self.primary_form = MyGroupBox()
        self.primary_form_layout = MyFormLayout()
        self.promo_name_field = MyLineEdit(line_edit_ref='promo_name_field')
        self.promo_type_field = MyComboBox(combo_box_ref='promo_type_field')
        self.discount_percent_field = MyLineEdit(line_edit_ref='discount_percent_field')
        self.description_field = MyTextEdit(textedit_ref='description_field')
        self.primary_form_layout.addRow('Promo name:', self.promo_name_field)
        self.primary_form_layout.addRow('Promo type:', self.promo_type_field)
        self.primary_form_layout.addRow('Discount percent:', self.discount_percent_field)
        self.primary_form_layout.addRow('Description:', self.description_field)
        self.primary_form.setLayout(self.primary_form_layout)
        # endregion -- self.primary_form = MyGroupBox()
        # region -- self.form_nav = MyGroupBox()
        self.form_nav = MyGroupBox()
        self.form_nav_layout = MyGridLayout()
        self.discard_button = MyPushButton(text='Discard')
        self.discard_button.clicked.connect(self.on_discard_button_clicked)
        self.save_new_button = MyPushButton(text='Save New')
        self.save_new_button.clicked.connect(self.on_save_new_button_clicked)
        self.save_edit_button = MyPushButton(text='Save Edit')
        self.save_edit_button.clicked.connect(self.on_save_edit_button_clicked)
        self.form_nav_layout.addWidget(self.discard_button,0,0)
        self.form_nav_layout.addWidget(self.save_new_button,0,1)
        self.form_nav_layout.addWidget(self.save_edit_button,0,1)
        self.form_nav.setLayout(self.form_nav_layout)
        # endregion -- self.form_nav = MyGroupBox()

        self.manage_data_panel_layout.addRow(self.primary_form)
        self.manage_data_panel_layout.addRow(self.form_nav)
        self.manage_data_panel.setLayout(self.manage_data_panel_layout)
        self.scrolling_manage_data_panel.setWidget(self.manage_data_panel)
        pass
    def show_content_panel(self):
        self.content_panel = MyWidget()
        self.content_panel_layout = MyGridLayout(grid_layout_ref='content_panel_layout')

        self.filter_field = MyLineEdit(line_edit_ref='filter_field')

        # region -- self.manage_data_nav = MyGroupBox()
        self.manage_data_nav = MyWidget(widget_ref='manage_data_nav')
        self.manage_data_layout = MyHBoxLayout(hbox_layout_ref='manage_data_layout')
        self.refresh_data_button = MyPushButton(push_button_ref='refresh_data_button', text='Refresh')
        self.refresh_data_button.clicked.connect(self.on_refresh_data_button_clicked)
        self.delete_all_data_button = MyPushButton(push_button_ref='delete_all_data_button', text='Delete All')
        self.delete_all_data_button.clicked.connect(self.on_delete_all_data_button_clicked)
        self.import_data_button = MyPushButton(push_button_ref='import_data_button', text='Import')
        self.import_data_button.clicked.connect(self.on_import_data_button_clicked)
        self.add_data_button = MyPushButton(push_button_ref='add_data_button', text='Add')
        self.add_data_button.clicked.connect(self.on_add_data_button_clicked)
        self.manage_data_layout.addWidget(self.refresh_data_button)
        self.manage_data_layout.addWidget(self.delete_all_data_button)
        self.manage_data_layout.addWidget(self.import_data_button)
        self.manage_data_layout.addWidget(self.add_data_button)
        self.manage_data_nav.setLayout(self.manage_data_layout)
        # endregion -- self.manage_data_nav = MyGroupBox()

        self.table_sorter = MyTabWidget()

        # region -- self.overview_pagination
        self.overview_pagination = MyWidget(widget_ref='overview_pagination')
        self.overview_pagination_layout = MyGridLayout(grid_layout_ref='overview_pagination_layout')
        self.overview_table = MyTableWidget(table_widget_ref='overview_table')
        self.overview_pagination_nav = MyWidget(widget_ref='overview_pagination_nav')
        self.overview_pagination_nav_layout = MyGridLayout()
        self.overview_pagination_prev_button = MyPushButton(text='Prev')
        self.overview_pagination_prev_button.clicked.connect(self.on_overview_pagination_prev_button_clicked)
        self.overview_pagination_page = MyLabel('Page 1')
        self.overview_pagination_next_button = MyPushButton(text='Next')
        self.overview_pagination_next_button.clicked.connect(self.on_overview_pagination_next_button_clicked)
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_prev_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_page,0,1,Qt.AlignmentFlag.AlignCenter)
        self.overview_pagination_nav_layout.addWidget(self.overview_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_nav.setLayout(self.overview_pagination_nav_layout)
        self.overview_pagination_layout.addWidget(self.overview_table,0,0)
        self.overview_pagination_layout.addWidget(self.overview_pagination_nav,1,0,Qt.AlignmentFlag.AlignCenter)
        self.overview_pagination.setLayout(self.overview_pagination_layout)
        # endregion -- self.overview_pagination
        
        # region -- self.table_sorter.addTab
        self.table_sorter.addTab(self.overview_pagination, 'Overview')
        # endregion -- self.table_sorter.addTab

        self.content_panel_layout.addWidget(self.filter_field,0,0)
        self.content_panel_layout.addWidget(self.manage_data_nav,0,1)
        self.content_panel_layout.addWidget(self.table_sorter,1,0,1,2)
        self.content_panel.setLayout(self.content_panel_layout)

    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(grid_layout_ref='main_panel_layout')

        self.show_content_panel()
        self.show_manage_data_panel()
        self.show_operation_panel()

        self.main_panel_layout.addWidget(self.content_panel,0,0)
        self.main_panel_layout.addWidget(self.scrolling_manage_data_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.operation_status_panel,1,0)
        self.setLayout(self.main_panel_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoWindow()
    window.show()
    sys.exit(pos_app.exec())
