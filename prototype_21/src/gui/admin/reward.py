
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
from src.sql.admin.reward import *
from src.widget.admin.admin import *
from templates.qss.qss_config import QSSConfig

schema = MyRewardSchema()
qss = QSSConfig()

class MyRewardModel: # NOTE: entries
    def __init__(self, name):
        # NOTE: global variables
        self.gdrive_path = 'G:' + f"/My Drive/"
        self.user_name = name

        self.init_selected_reward_data_entry()
        self.init_progress_data_entry()
        self.init_reward_list_page_entry()

    def init_reward_list_page_entry(self):
        self.page_number = 1
        self.total_page_number = schema.select_reward_total_pages_count()

    def init_selected_reward_data_entry(self):
        self.sel_reward_name_value = None
        self.sel_reward_description_value = None
        self.sel_reward_unit_value = None
        self.sel_reward_points_value = None
        self.sel_datetime_created_value = None
        self.sel_reward_id_value = None
        pass
    def assign_selected_reward_data_entry(self, value):
        self.sel_reward_name_value = str(value[0])
        self.sel_reward_description_value = str(value[1])
        self.sel_reward_unit_value = str(value[2])
        self.sel_reward_points_value = str(value[3])
        self.sel_datetime_created_value = str(value[4])
        self.sel_reward_id_value = value[5]

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

    def import_reward_entry(self, data_frame):
        self.reward_import_thread = MyDataImportThread(data_name='reward', data_frame=data_frame) # NOTE: ths is QThread for data import
        self.reward_import_thread.start()

    def setup_manage_reward_panel(self, window_title):
        self.manage_reward_dialog = MyDialog(window_title=window_title)
        self.manage_reward_layout = MyGridLayout()

        self.reward_name_label = MyLabel(text='Name')
        self.reward_description_label = MyLabel(text='Description')
        self.reward_unit_label = MyLabel(text='Unit')
        self.reward_points_label = MyLabel(text='Points')
        
        self.reward_name_field = MyLineEdit(object_name='reward_name_field')
        self.reward_description_field = MyPlainTextEdit(object_name='reward_description_field')
        self.reward_unit_field = MyLineEdit(object_name='reward_unit_field')
        self.reward_points_field = MyLineEdit(object_name='reward_points_field')

        self.reward_form_box = MyGroupBox()
        self.reward_form_layout = MyFormLayout()
        self.reward_form_layout.insertRow(0,self.reward_name_label)
        self.reward_form_layout.insertRow(2,self.reward_description_label)
        self.reward_form_layout.insertRow(4,self.reward_unit_label)
        self.reward_form_layout.insertRow(6,self.reward_points_label)
        self.reward_form_layout.insertRow(1,self.reward_name_field)
        self.reward_form_layout.insertRow(3,self.reward_description_field)
        self.reward_form_layout.insertRow(5,self.reward_unit_field)
        self.reward_form_layout.insertRow(7,self.reward_points_field)
        self.reward_form_box.setLayout(self.reward_form_layout)
        self.reward_form_scra = MyScrollArea()
        self.reward_form_scra.setWidget(self.reward_form_box)

        self.manage_reward_save_button = MyPushButton(text='Save')
        self.manage_reward_close_button = MyPushButton(text='Close')
        self.manage_reward_act_box = MyGroupBox()
        self.manage_reward_act_layout = MyHBoxLayout(object_name='reward_act_layout')
        self.manage_reward_act_layout.addWidget(self.manage_reward_save_button)
        self.manage_reward_act_layout.addWidget(self.manage_reward_close_button)
        self.manage_reward_act_box.setLayout(self.manage_reward_act_layout)

        self.manage_reward_layout.addWidget(self.reward_form_scra,0,0)
        self.manage_reward_layout.addWidget(self.manage_reward_act_box,1,0,Qt.AlignmentFlag.AlignRight)
        self.manage_reward_dialog.setLayout(self.manage_reward_layout)
        pass
    def save_new_reward_entry(self):
        reward_name = self.reward_name_field.text()
        reward_description = self.reward_description_field.toPlainText()
        reward_unit = self.reward_unit_field.text()
        reward_points = self.reward_points_field.text()

        schema.insert_new_reward_data(
                reward_name=reward_name,
                reward_description=reward_description,
                reward_unit=reward_unit,
                reward_points=reward_points
            )

        self.manage_reward_dialog.close()
        pass
    def save_edit_reward_entry(self):
        reward_name = self.reward_name_field.text()
        reward_description = self.reward_description_field.toPlainText()
        reward_unit = self.reward_unit_field.text()
        reward_points = self.reward_points_field.text()
        reward_id = self.sel_reward_id_value

        schema.update_selected_reward_data(
                reward_name=reward_name,
                reward_description=reward_description,
                reward_unit=reward_unit,
                reward_points=reward_points,
                reward_id=reward_id
            )

        self.sel_reward_id_value = 0
        self.manage_reward_dialog.close()
        pass
    
    def setup_view_reward_panel(self):
        self.view_dialog = MyDialog(window_title=f"{self.sel_reward_name_value}")
        self.view_layout = MyGridLayout()

        self.reward_name_info_label = MyLabel(text=f"{self.sel_reward_name_value}")
        self.reward_description_info_label = MyLabel(text=f"{self.sel_reward_description_value}")
        self.reward_unit_info_label = MyLabel(text=f"{self.sel_reward_unit_value}")
        self.reward_points_info_label = MyLabel(text=f"{self.sel_reward_points_value}")
        self.datetime_created_info_label = MyLabel(text=f"{self.sel_datetime_created_value}")
        self.view_form_box = MyGroupBox()
        self.view_form_layout = MyFormLayout()
        self.view_form_layout.addRow('Name', self.reward_name_info_label)
        self.view_form_layout.addRow('Description', self.reward_description_info_label)
        self.view_form_layout.addRow('Unit', self.reward_unit_info_label)
        self.view_form_layout.addRow('Points', self.reward_points_info_label)
        self.view_form_layout.addRow('Date/Time created', self.datetime_created_info_label)
        self.view_form_box.setLayout(self.view_form_layout)
        self.view_form_scra = MyScrollArea()
        self.view_form_scra.setWidget(self.view_form_box)

        self.view_form_close_button = MyPushButton(text='Close')

        self.view_layout.addWidget(self.view_form_scra,0,0)
        self.view_layout.addWidget(self.view_form_close_button,1,0,Qt.AlignmentFlag.AlignRight)
        self.view_dialog.setLayout(self.view_layout)
    
    pass
class MyRewardView(MyGroupBox): # NOTE: layout
    def __init__(self, model: MyRewardModel):
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
        self.import_reward_button = MyPushButton(text='Import')
        self.add_reward_button = MyPushButton(text='Add')
        self.interactive_act_box = MyGroupBox()
        self.interactive_act_layout = MyHBoxLayout()
        self.interactive_act_layout.addWidget(self.sync_ui_button)
        self.interactive_act_layout.addWidget(self.import_reward_button)
        self.interactive_act_layout.addWidget(self.add_reward_button)
        self.interactive_act_box.setLayout(self.interactive_act_layout)

        self.reward_list_table = MyTableWidget(object_name='reward_list_table')
        self.reward_list_prev_button = MyPushButton(text='Prev')
        self.reward_list_page_label = MyLabel(text=f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.reward_list_next_button = MyPushButton(text='Next')
        self.reward_list_pag_box = MyGroupBox()
        self.reward_list_pag_layout = MyHBoxLayout(object_name='reward_list_pag_layout')
        self.reward_list_pag_layout.addWidget(self.reward_list_prev_button)
        self.reward_list_pag_layout.addWidget(self.reward_list_page_label)
        self.reward_list_pag_layout.addWidget(self.reward_list_next_button)
        self.reward_list_pag_box.setLayout(self.reward_list_pag_layout)
        self.reward_list_box = MyGroupBox()
        self.reward_list_layout = MyGridLayout()
        self.reward_list_layout.addWidget(self.reward_list_table,0,0)
        self.reward_list_layout.addWidget(self.reward_list_pag_box,1,0,Qt.AlignmentFlag.AlignCenter)
        self.reward_list_box.setLayout(self.reward_list_layout)
        self.reward_list_tab = MyTabWidget()
        self.reward_list_tab.addTab(self.reward_list_box, 'Overview')

        self.panel_a_layout.addWidget(self.text_filter_box,0,0)
        self.panel_a_layout.addWidget(self.interactive_act_box,0,1)
        self.panel_a_layout.addWidget(self.reward_list_tab,1,0,1,2)
        self.panel_a_box.setLayout(self.panel_a_layout)
        pass
    pass 
class MyRewardController: # NOTE: connections, setting attributes
    def __init__(self, model: MyRewardModel, view: MyRewardView):
        self.view = view
        self.model = model

        self.setup_panel_a_conn()
        self.populate_reward_list_table()

    def setup_panel_a_conn(self):
        self.view.text_filter_field.returnPressed.connect(self.on_text_filter_button_clicked)
        self.view.text_filter_button.clicked.connect(self.on_text_filter_button_clicked)
        self.view.sync_ui_button.clicked.connect(self.on_sync_ui_button_clicked)
        self.view.import_reward_button.clicked.connect(self.on_import_reward_button_clicked)
        self.view.add_reward_button.clicked.connect(self.on_add_reward_button_clicked)
        self.view.reward_list_prev_button.clicked.connect(lambda: self.on_reward_list_pag_button_clicked(action='go_prev'))
        self.view.reward_list_next_button.clicked.connect(lambda: self.on_reward_list_pag_button_clicked(action='go_next'))
        pass

    def populate_reward_list_table(self, text_filter='', page_number=1):
        reward_list = schema.select_reward_data(text_filter=text_filter, page_number=page_number)

        self.view.reward_list_page_label.setText(f"Page {page_number}/{self.model.total_page_number}")

        self.view.reward_list_prev_button.setEnabled(page_number > 1)
        self.view.reward_list_next_button.setEnabled(len(reward_list) == 30)

        self.view.reward_list_table.setRowCount(len(reward_list))

        for reward_list_i, reward_list_v in enumerate(reward_list):
            self.edit_reward_button = MyPushButton(text='Edit')
            self.view_reward_button = MyPushButton(text='View')
            self.delete_reward_button = MyPushButton(text='Delete')
            table_act_panel = MyGroupBox(object_name='table_act_panel')
            table_act_laoyut = MyHBoxLayout(object_name='table_act_laoyut')
            table_act_laoyut.addWidget(self.edit_reward_button)
            table_act_laoyut.addWidget(self.view_reward_button)
            table_act_laoyut.addWidget(self.delete_reward_button)
            table_act_panel.setLayout(table_act_laoyut)
            reward_name = QTableWidgetItem(f"{reward_list_v[0]}")
            reward_description = QTableWidgetItem(f"{reward_list_v[1]}")
            reward_unit = QTableWidgetItem(f"{reward_list_v[2]}")
            reward_points = QTableWidgetItem(f"{reward_list_v[3]}")
            datetime_created = QTableWidgetItem(f"{reward_list_v[4]}")

            self.view.reward_list_table.setCellWidget(reward_list_i, 0, table_act_panel)
            self.view.reward_list_table.setItem(reward_list_i, 1, reward_name)
            self.view.reward_list_table.setItem(reward_list_i, 2, reward_description)
            self.view.reward_list_table.setItem(reward_list_i, 3, reward_unit)
            self.view.reward_list_table.setItem(reward_list_i, 4, reward_points)
            self.view.reward_list_table.setItem(reward_list_i, 5, datetime_created)


            self.setup_reward_list_table_act_panel_conn(value=reward_list_v)
            pass
        pass
    def setup_reward_list_table_act_panel_conn(self, value):
        self.edit_reward_button.clicked.connect(lambda _, value=value: self.on_edit_reward_button_clicked(value))
        self.view_reward_button.clicked.connect(lambda _, value=value: self.on_view_reward_button_clicked(value))
        self.delete_reward_button.clicked.connect(lambda _, value=value: self.on_delete_reward_button_clicked(value))

    def on_text_filter_button_clicked(self):
        self.model.page_number = 1
        self.view.reward_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

        self.populate_reward_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number) 
        pass
    def on_sync_ui_button_clicked(self):
        self.start_sync_ui()

        QMessageBox.information(self.view, 'Success', 'Synced.')
        pass

    def start_sync_ui(self):
        self.model.init_reward_list_page_entry()
        self.view.reward_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")
        self.populate_reward_list_table()
    
    def on_import_reward_button_clicked(self):
        try:
            self.reward_csv_file, _ = QFileDialog.getOpenFileName(self.view, 'Open CSV', qss.csv_file_path, 'CSV File (*.csv)')
            self.reward_csv_df = pd.read_csv(self.reward_csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

            if self.reward_csv_file:
                self.model.prog_total_data_value = len(self.reward_csv_df)
                self.model.prog_remaining_data_value = len(self.reward_csv_df)

                self.model.setup_progress_panel(window_title=f"{'percentage'}", progress_type='reward_import')
                self.model.import_reward_entry(data_frame=self.reward_csv_df)
                self.setup_reward_import_thread_conn()
                self.model.progress_dialog.exec()

                if self.model.prog_remaining_data_value > 0 and self.model.progress_dialog.close():
                    self.model.reward_import_thread.stop()

                    self.model.init_progress_data_entry()

                    QMessageBox.critical(self.view, 'Cancelled', 'Import has been cancelled')
                    self.on_sync_ui_button_clicked()

            pass
        except Exception as e:
            self.reward_csv_file = ''
        pass
    def setup_reward_import_thread_conn(self):
        self.model.reward_import_thread.update_signal.connect(self.on_reward_import_thread_update_signal)
        self.model.reward_import_thread.finished_signal.connect(self.on_reward_import_thread_finished_signal)
        self.model.reward_import_thread.invalid_signal.connect(self.on_reward_import_thread_invalid_signal)
        pass
    def on_reward_import_thread_update_signal(self):
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
    def on_reward_import_thread_finished_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.information(self.view, 'Success', 'All reward has been imported')
        self.on_sync_ui_button_clicked()
        pass
    def on_reward_import_thread_invalid_signal(self):
        self.model.progress_dialog.close()
        self.model.init_progress_data_entry()
        
        QMessageBox.critical(self.view, 'Error', 'Invalid CSV file.')
        self.on_sync_ui_button_clicked()
        pass

    def on_add_reward_button_clicked(self):  
        self.model.setup_manage_reward_panel(window_title='Add reward')
        self.setup_manage_reward_panel_conn(conn_type='add_reward')

        self.model.manage_reward_dialog.exec()
        pass
    def on_edit_reward_button_clicked(self, value):
        self.model.assign_selected_reward_data_entry(value)
        self.model.setup_manage_reward_panel(window_title=f"Edit {self.model.sel_reward_name_value}")

        self.model.reward_name_field.setText(self.model.sel_reward_name_value)
        self.model.reward_description_field.setPlainText(self.model.sel_reward_description_value)
        self.model.reward_unit_field.setText(self.model.sel_reward_unit_value)
        self.model.reward_points_field.setText(self.model.sel_reward_points_value)

        self.setup_manage_reward_panel_conn(conn_type='edit_reward')

        self.model.manage_reward_dialog.exec()
        pass

    def setup_manage_reward_panel_conn(self, conn_type):
        self.model.manage_reward_save_button.clicked.connect(lambda: self.on_manage_reward_save_button_clicked(action=conn_type))
        self.model.manage_reward_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.manage_reward_dialog))
        pass
    def on_manage_reward_save_button_clicked(self, action):
        reward_name = self.model.reward_name_field.text()
        reward_unit = self.model.reward_unit_field.text()
        reward_points = self.model.reward_points_field.text()


        if '' not in [reward_name, reward_unit, reward_points]:
            if (reward_unit.replace('.', '', 1).isdigit() and reward_points.replace('.', '', 1).isdigit()):
                if action == 'add_reward':
                    self.model.save_new_reward_entry()
                    self.model.init_selected_reward_data_entry()

                    QMessageBox.information(self.view, 'Success', 'New reward has been added.')
                    pass
                elif action == 'edit_reward':
                    self.model.save_edit_reward_entry()
                    self.model.init_selected_reward_data_entry()

                    QMessageBox.information(self.view, 'Success', 'Reward has been edited.')
                    pass
                self.on_sync_ui_button_clicked()
                pass
            else:
                QMessageBox.critical(self.model.manage_reward_dialog, 'Error', 'Invalid numerical input.')
                pass
        else:
            self.set_label_required_field_indicator(reward_name, reward_unit, reward_points)

            QMessageBox.critical(self.model.manage_reward_dialog, 'Error', 'Please fill out the required field.')
            pass
        pass
    def set_label_required_field_indicator(self, reward_name, reward_unit, reward_points):
        self.model.reward_name_label.setText(f"Name {qss.required_label}") if reward_name == '' else self.model.reward_name_label.setText(f"Name")
        self.model.reward_unit_label.setText(f"Unit {qss.required_label}") if reward_unit == '' else self.model.reward_unit_label.setText(f"Unit")
        self.model.reward_points_label.setText(f"Points {qss.required_label}") if reward_points == '' else self.model.reward_points_label.setText(f"Points")
    
    def on_view_reward_button_clicked(self, value):
        self.model.assign_selected_reward_data_entry(value)

        self.model.setup_view_reward_panel()

        self.setup_view_reward_conn()

        self.model.view_dialog.exec()
        pass
    def setup_view_reward_conn(self):
        self.model.view_form_close_button.clicked.connect(lambda: self.on_close_button_clicked(widget=self.model.view_dialog))

    def on_delete_reward_button_clicked(self, value):
        self.model.assign_selected_reward_data_entry(value)

        confirm = QMessageBox.warning(self.view, 'Confirm', f"Delete {self.model.sel_reward_name_value}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_selected_reward_data(reward_id=self.model.sel_reward_id_value)

            self.model.init_selected_reward_data_entry()

            QMessageBox.information(self.view, 'Success', 'Reward has been deleted.')

            self.on_sync_ui_button_clicked()
            pass
        else:
            self.model.init_selected_reward_data_entry()
            return
        pass
    
    def on_close_button_clicked(self, widget: QWidget):
        widget.close()

        self.model.init_selected_reward_data_entry()
        pass

    def on_reward_list_pag_button_clicked(self, action):
        print('reward_list_prev_button_clicked')
        if action == 'go_prev':
            if self.model.page_number > 1:
                self.model.page_number -= 1
                self.view.reward_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_reward_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        elif action == 'go_next':
            self.model.page_number += 1
            self.view.reward_list_page_label.setText(f"Page {self.model.page_number}/{self.model.total_page_number}")

            self.populate_reward_list_table(text_filter=self.view.text_filter_field.text(), page_number=self.model.page_number)
            pass
        pass

    pass

class MyRewardWindow(MyGroupBox):
    def __init__(self, name): # NOTE: 'name' param is for the current user (cashier, admin, dev) name
        super().__init__(object_name='MyRewardWindow')

        self.model = MyRewardModel(name=name)
        self.view = MyRewardView(self.model)
        self.controller = MyRewardController(self.model, self.view)

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.show()


# NOTE: For testing purpsoes only.
if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    reward_window = MyRewardWindow(name='test-name')

    reward_window.run()
    app.exec()