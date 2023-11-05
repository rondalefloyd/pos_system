
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from src.gui.widget.my_widget import *
from src.core.csv_to_db_importer import MyDataImportThread
from src.core.sql.admin.reward import MyRewardSchema
from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()
schema = MyRewardSchema()

class MyRewardModel:
    def __init__(self, name, phone):
        self.user_name = name
        self.user_phone = phone

        self.total_page_number = schema.select_reward_data_total_page_count()
        self.page_number = 1 if self.total_page_number > 0 else 0

        self.sel_reward_id = 0

    def set_import_data_entry(self, csv_file_path):
        self.progress_count = 0
        self.progress_percent = 100

        self.data_import_thread = MyDataImportThread(data_name='reward', csv_file_path=csv_file_path)

        self.data_import_thread.start()
    
    def init_manage_data_entry(
            self, 
            dialog, 
            task, 
            reward_name_label, 
            reward_unit_label, 
            reward_points_label, 
            reward_name, 
            reward_unit, 
            reward_points, 
            reward_desc
    ):
        if '' not in [reward_name, reward_unit, reward_points]:
            if (reward_unit.replace('.', '', 1).isdigit() and reward_points.replace('.', '', 1).isdigit()):
                reward_name_label.setText(f"Name")
                reward_unit_label.setText(f"Unit")
                reward_points_label.setText(f"Points")
                                            
                if task == 'add_data':
                    schema.insert_reward_data(
                        reward_name,
                        reward_unit,
                        reward_points,
                        reward_desc,
                    )
                    QMessageBox.information(dialog, 'Success', 'Reward added.')
                    dialog.close()
                    pass
                elif task == 'edit_data':
                    schema.update_reward_data(
                        reward_name,
                        reward_unit,
                        reward_points,
                        reward_desc,
                        self.sel_reward_id
                    )
                    QMessageBox.information(dialog, 'Success', 'Reward edited.')
                    dialog.close()
                    self.sel_reward_id = 0
                    pass
            else:
                reward_name_label.setText(f"Name")
                reward_unit_label.setText(f"Unit {qss.inv_field_indicator}") if reward_unit.replace('.', '', 1).isdigit() is False else reward_unit_label.setText(f"Unit")
                reward_points_label.setText(f"Points {qss.inv_field_indicator}") if reward_points.replace('.', '', 1).isdigit() is False else reward_points_label.setText(f"Points")
                
                QMessageBox.critical(dialog, 'Error', 'Invalid numeric value.')
        else:
            reward_name_label.setText(f"Name {qss.req_field_indicator}") if reward_name == '' else reward_name_label.setText(f"Name")
            reward_unit_label.setText(f"Unit {qss.inv_field_indicator}") if reward_unit.replace('.', '', 1).isdigit() is False else reward_unit_label.setText(f"Unit")
            reward_points_label.setText(f"Points {qss.inv_field_indicator}") if reward_points.replace('.', '', 1).isdigit() is False else reward_points_label.setText(f"Points")

            QMessageBox.critical(dialog, 'Error', 'Please fill out all required fields.')
    pass
class MyRewardView(MyWidget):
    def __init__(self, model: MyRewardModel):
        super().__init__()

        self.m = model

        self.set_reward_box()

    def set_reward_box(self):
        self.filter_field = MyLineEdit(object_name='filter_field')
        self.filter_button = MyPushButton(object_name='filter_button', text='Filter')
        self.filter_box = MyGroupBox(object_name='filter_box')
        self.filter_layout = MyHBoxLayout(object_name='filter_layout')
        self.filter_layout.addWidget(self.filter_field)
        self.filter_layout.addWidget(self.filter_button)
        self.filter_box.setLayout(self.filter_layout)

        self.import_data_button = MyPushButton(object_name='import_data_button',text='Import')
        self.add_data_button = MyPushButton(object_name='add_data_button',text='Add')
        self.manage_data_box = MyGroupBox(object_name='manage_data_box')
        self.manage_data_layout = MyHBoxLayout(object_name='manage_data_layout')
        # self.manage_data_layout.addWidget(self.import_data_button)
        self.manage_data_layout.addWidget(self.add_data_button)
        self.manage_data_box.setLayout(self.manage_data_layout)

        self.reward_act_box = MyGroupBox(object_name='reward_act_box')
        self.reward_act_layout = MyHBoxLayout(object_name='reward_act_layout')
        self.reward_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.reward_act_layout.addWidget(self.manage_data_box,1,Qt.AlignmentFlag.AlignRight)
        self.reward_act_box.setLayout(self.reward_act_layout)

        self.reward_overview_table = MyTableWidget(object_name='reward_overview_table')
        self.reward_overview_prev_button = MyPushButton(object_name='overview_prev_button', text='Prev')
        self.reward_overview_page_label = MyLabel(object_name='overview_page_label', text=f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.reward_overview_next_button = MyPushButton(object_name='overview_next_button', text='Next')
        self.reward_overview_act_box = MyGroupBox(object_name='overview_act_box')
        self.reward_overview_act_layout = MyHBoxLayout(object_name='overview_act_layout')
        self.reward_overview_act_layout.addWidget(self.reward_overview_prev_button)
        self.reward_overview_act_layout.addWidget(self.reward_overview_page_label)
        self.reward_overview_act_layout.addWidget(self.reward_overview_next_button)
        self.reward_overview_act_box.setLayout(self.reward_overview_act_layout)
        self.reward_overview_box = MyGroupBox()
        self.reward_overview_layout = MyVBoxLayout()
        self.reward_overview_layout.addWidget(self.reward_overview_table)
        self.reward_overview_layout.addWidget(self.reward_overview_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.reward_overview_box.setLayout(self.reward_overview_layout)
        
        self.reward_sort_tab = MyTabWidget()
        self.reward_sort_tab.addTab(self.reward_overview_box, 'Overview')

        self.main_layout = MyVBoxLayout()
        self.main_layout.addWidget(self.reward_act_box)
        self.main_layout.addWidget(self.reward_sort_tab)
        self.setLayout(self.main_layout)

    def set_manage_data_box(self):
        self.reward_name_field = MyLineEdit(object_name='reward_name_field')
        self.reward_name_label = MyLabel(text='Name')
        self.reward_unit_field = MyLineEdit(object_name='reward_unit_field')
        self.reward_unit_label = MyLabel(text='Unit')
        self.reward_points_field = MyLineEdit(object_name='reward_points_field')
        self.reward_points_label = MyLabel(text='Points')
        self.reward_desc_field = MyPlainTextEdit(object_name='reward_desc_field')
        self.reward_desc_label = MyLabel(text='Description')
        self.field_box = MyGroupBox(object_name='field_box')
        self.field_layout = MyFormLayout(object_name='field_layout')
        self.field_layout.addRow(self.reward_name_label)
        self.field_layout.addRow(self.reward_name_field)
        self.field_layout.addRow(self.reward_unit_label)
        self.field_layout.addRow(self.reward_unit_field)
        self.field_layout.addRow(self.reward_points_label)
        self.field_layout.addRow(self.reward_points_field)
        self.field_layout.addRow(self.reward_desc_label)
        self.field_layout.addRow(self.reward_desc_field)
        self.field_box.setLayout(self.field_layout)
        self.manage_data_scra = MyScrollArea()
        self.manage_data_scra.setWidget(self.field_box)

        self.save_data_button = MyPushButton(object_name='save_button', text='Save')
        self.manage_data_act_close_button = MyPushButton(object_name='close_button', text='Close')
        self.manage_data_act_box = MyGroupBox(object_name='manage_data_act_box')
        self.manage_data_act_layout = MyHBoxLayout(object_name='manage_data_act_layout')
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
        self.progress_layout = MyVBoxLayout(object_name='progress_layout')
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_dialog.setLayout(self.progress_layout)
        pass

    def set_overview_table_act_box(self):
        self.edit_data_button = MyPushButton(object_name='edit_data_button', text='Edit')
        self.view_data_button = MyPushButton(object_name='view_data_button', text='View')
        self.delete_data_button = MyPushButton(object_name='delete_data_button', text='Delete')
        self.reward_overview_data_act_box = MyGroupBox(object_name='reward_overview_data_act_box')
        self.reward_overview_data_act_layout = MyHBoxLayout(object_name='reward_overview_data_act_layout')
        self.reward_overview_data_act_layout.addWidget(self.edit_data_button)
        self.reward_overview_data_act_layout.addWidget(self.view_data_button)
        self.reward_overview_data_act_layout.addWidget(self.delete_data_button)
        self.reward_overview_data_act_box.setLayout(self.reward_overview_data_act_layout)

    def set_view_dialog(self):
        self.reward_name_info = MyLabel(text=f"reward_name")
        self.reward_unit_info = MyLabel(text=f"reward_unit")
        self.reward_points_info = MyLabel(text=f"reward_points")
        self.reward_desc_info = MyLabel(text=f"reward_desc")
        self.datetime_created_info = MyLabel(text=f"datetime_created")
        self.info_box = MyGroupBox(object_name='info_box')
        self.info_layout = MyFormLayout(object_name='info_layout')
        self.info_layout.addRow('Name:', self.reward_name_info)
        self.info_layout.addRow('Type:', self.reward_unit_info)
        self.info_layout.addRow('Percent:', self.reward_points_info)
        self.info_layout.addRow('Description:', self.reward_desc_info)
        self.info_layout.addRow(MyLabel(text='<hr>'))
        self.info_layout.addRow('Date/Time created:', self.datetime_created_info)
        self.info_box.setLayout(self.info_layout)
        self.view_data_scra = MyScrollArea()
        self.view_data_scra.setWidget(self.info_box)


        self.view_data_act_close_button = MyPushButton(object_name='close_button', text='Close')
        self.view_data_act_box = MyGroupBox(object_name='view_data_act_box')
        self.view_data_act_layout = MyHBoxLayout(object_name='view_data_act_layout')
        self.view_data_act_layout.addWidget(self.view_data_act_close_button,0,Qt.AlignmentFlag.AlignRight)
        self.view_data_act_box.setLayout(self.view_data_act_layout)

        self.view_data_dialog = MyDialog()
        self.view_data_layout = MyVBoxLayout()
        self.view_data_layout.addWidget(self.view_data_scra)
        self.view_data_layout.addWidget(self.view_data_act_box)
        self.view_data_dialog.setLayout(self.view_data_layout)
class MyRewardController:
    def __init__(self, model: MyRewardModel, view: MyRewardView):
        self.v = view
        self.m = model

        self.set_reward_box_conn()
        self.sync_ui()

    def set_reward_box_conn(self):
        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)
        self.v.import_data_button.clicked.connect(self.on_import_data_button_clicked)
        self.v.add_data_button.clicked.connect(self.on_add_data_button_clicked)
        self.v.reward_overview_prev_button.clicked.connect(self.on_overview_prev_button_clicked)
        self.v.reward_overview_next_button.clicked.connect(self.on_overview_next_button_clicked)
        pass
    def on_filter_button_clicked(self): # IDEA: src
        text_filter = self.v.filter_field.text()
        
        self.m.total_page_number = schema.select_reward_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0


        self.v.reward_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        
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
        self.m.progress_percent = int((self.m.progress_count * 100) / total_data_count)
        self.v.progress_dialog.setWindowTitle(f"{self.m.progress_percent}% complete")
        self.v.progress_bar.setValue(self.m.progress_percent)
        self.v.progress_label.setText(current_data)
        pass
    def on_data_import_thread_cancelled(self):
        QMessageBox.information(None, 'Cancelled', 'Import cancelled.')
        pass
    def on_data_import_thread_finished(self):
        QMessageBox.information(None, 'Success', 'Import complete.')
        self.v.progress_dialog.close_signal.emit('finished')
        self.v.progress_dialog.close()
        pass
    def on_data_import_thread_invalid(self):
        QMessageBox.critical(None, 'Error', 'An error occurred during import.')
        self.v.progress_dialog.close()
        pass

    def on_add_data_button_clicked(self): # IDEA: src
        self.v.set_manage_data_box()
        # self.load_combo_box_data() -- just in case
        self.set_manage_data_box_conn(task='add_data')
        self.v.manage_data_dialog.exec()
        pass

    def populate_overview_table(self, text='', page_number=1): # IDEA: src
        self.v.reward_overview_prev_button.setEnabled(page_number > 1)
        self.v.reward_overview_next_button.setEnabled(page_number < self.m.total_page_number)
        self.v.reward_overview_page_label.setText(f"Page {page_number}/{self.m.total_page_number}")

        reward_data = schema.select_data_as_display(text=text, page_number=page_number)

        self.v.reward_overview_table.setRowCount(len(reward_data))

        for i, data in enumerate(reward_data):
            self.v.set_overview_table_act_box()
            reward_name = MyTableWidgetItem(text=f"{data[0]}")
            reward_unit = MyTableWidgetItem(text=f"{data[1]}", format='bill')
            reward_points = MyTableWidgetItem(text=f"{data[2]}", format='bill')
            reward_desc = MyTableWidgetItem(text=f"{data[3]}")
            datetime_created = MyTableWidgetItem(text=f"{data[4]}")

            self.v.reward_overview_table.setCellWidget(i, 0, self.v.reward_overview_data_act_box)
            self.v.reward_overview_table.setItem(i, 1, reward_name)
            self.v.reward_overview_table.setItem(i, 2, reward_unit)
            self.v.reward_overview_table.setItem(i, 3, reward_points)
            self.v.reward_overview_table.setItem(i, 4, reward_desc)
            self.v.reward_overview_table.setItem(i, 5, datetime_created)

            self.v.edit_data_button.clicked.connect(lambda _, data=data: self.on_edit_data_button_clicked(data))
            self.v.view_data_button.clicked.connect(lambda _, data=data: self.on_view_data_button_clicked(data))
            self.v.delete_data_button.clicked.connect(lambda _, data=data: self.on_delete_data_button_clicked(data))
        pass
    def on_edit_data_button_clicked(self, data):
        self.v.set_manage_data_box()
        # self.load_combo_box_data() -- just in case
        self.v.manage_data_dialog.setWindowTitle(f"{data[0]}")
        sel_reward_data = schema.select_reward_data(data[0], data[1])

        for i, sel_data in enumerate(sel_reward_data):
            self.v.reward_name_field.setText(str(sel_data[0]))
            self.v.reward_unit_field.setText(str(sel_data[1]))
            self.v.reward_points_field.setText(str(sel_data[2]))
            self.v.reward_desc_field.setPlainText(str(sel_data[3]))
            self.m.sel_reward_id = sel_data[4]
            pass
        
        self.set_manage_data_box_conn(task='edit_data')
        self.v.manage_data_dialog.exec()
        pass
    def on_view_data_button_clicked(self, data):
        self.v.set_view_dialog()
        self.v.view_data_dialog.setWindowTitle(f"{data[0]}")

        self.v.reward_name_info.setText(str(data[0]))
        self.v.reward_unit_info.setText(str(data[1]))
        self.v.reward_points_info.setText(str(data[2]))
        self.v.reward_desc_info.setText(str(data[3]))
        self.v.datetime_created_info.setText(str(data[4]))

        self.set_view_data_box_conn()
        self.v.view_data_dialog.exec()
        pass
    def set_view_data_box_conn(self):
        self.v.view_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.view_data_dialog))
    def on_delete_data_button_clicked(self, data):
        sel_reward_data = schema.select_reward_data(data[0], data[1])

        for i, sel_data in enumerate(sel_reward_data):
            reward_name = sel_data[0]
            reward_id = sel_data[4]

        confirm = QMessageBox.warning(None, 'Confirm', f"Delete {reward_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_reward_data(reward_id)

            QMessageBox.information(None, 'Success', f"{reward_name} has been deleted.")

        self.sync_ui()
        pass

    def on_overview_prev_button_clicked(self):
        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.reward_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass
    def on_overview_next_button_clicked(self):
        if self.m.page_number < self.m.total_page_number:
            self.m.page_number += 1

            self.v.reward_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass

    # IDEA: if the widget uses the same connection
    def set_manage_data_box_conn(self, task):
        self.v.save_data_button.clicked.connect(lambda: self.on_save_data_button_clicked(task))
        self.v.manage_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.manage_data_dialog))
        pass
    # def load_combo_box_data(self): -- just in case

    def on_save_data_button_clicked(self, task):
        reward_name = self.v.reward_name_field.text()
        reward_unit = self.v.reward_unit_field.text()
        reward_points = self.v.reward_points_field.text()
        reward_desc = self.v.reward_desc_field.toPlainText()

        self.m.init_manage_data_entry(
            self.v.manage_data_dialog, 
            task, 
            self.v.reward_name_label,
            self.v.reward_unit_label,
            self.v.reward_points_label,
            reward_name, 
            reward_unit, 
            reward_points, 
            reward_desc
        )

        self.sync_ui()

    def sync_ui(self):
        text_filter = self.v.filter_field.text()
        self.m.total_page_number = schema.select_reward_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0
        self.populate_overview_table(text=text_filter, page_number=self.m.page_number)
        pass
    def close_dialog(self, dialog: QDialog):
        dialog.close()

class MyRewardWindow(MyGroupBox):
    def __init__(self, name='test', phone='test'):

        self.model = MyRewardModel(name, phone)
        self.view = MyRewardView(self.model)
        self.controller = MyRewardController(self.model, self.view)

        self.set_box() # NOTE: comment this out if will be tested individually

    def set_box(self):
        super().__init__()

        layout = MyGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def run(self):
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    reward_window = MyRewardWindow()

    reward_window.run()

    app.exec()