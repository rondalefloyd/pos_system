
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.gui.widget.my_widget import *
from src.core.csv_to_db_importer import MyDataImportThread
from src.core.sql.admin.promo import MyPromoSchema
from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()
schema = MyPromoSchema()

class MyPromoModel:
    def __init__(self, name, phone):
        self.user_name = name
        self.user_phone = phone

        self.total_page_number = schema.select_promo_data_total_page_count()
        self.page_number = 1 if self.total_page_number > 0 else 0

        self.sel_promo_id = 0

    def set_import_data_entry(self, csv_file_path):
        self.progress_count = 0
        self.progress_percent = 100

        self.data_import_thread = MyDataImportThread(data_name='promo', csv_file_path=csv_file_path)

        self.data_import_thread.start()
    
    def init_manage_data_entry(
            self, 
            dialog, 
            task, 
            promo_name_label,
            promo_type_label,
            promo_percent_label,
            promo_name, 
            promo_type, 
            promo_percent, 
            promo_desc
    ):
        if '' not in [promo_name, promo_type, promo_percent]:
            if promo_percent.replace('.', '', 1).isdigit():
                promo_name_label.setText(f"Name")
                promo_type_label.setText(f"Type")
                promo_percent_label.setText(f"Percent")
                
                if task == 'add_data':
                    schema.insert_promo_data(
                        promo_name,
                        promo_type,
                        promo_percent,
                        promo_desc,
                    )
                    QMessageBox.information(dialog, 'Success', 'Promo added.')
                    dialog.close()
                    pass
                elif task == 'edit_data':
                    schema.update_promo_data(
                        promo_name,
                        promo_type,
                        promo_percent,
                        promo_desc,
                        self.sel_promo_id
                    )
                    QMessageBox.information(dialog, 'Success', 'Promo edited.')
                    dialog.close()
                    self.sel_promo_id = 0
                    pass
            else:
                promo_name_label.setText(f"Name")
                promo_type_label.setText(f"Type")
                promo_percent_label.setText(f"Percent {qss.inv_field_indicator}") if promo_percent.replace('.', '', 1).isdigit() is False else promo_percent_label.setText(f"Percent")

                QMessageBox.critical(dialog, 'Error', 'Invalid numeric value.')
        else:
            promo_name_label.setText(f"Name {qss.req_field_indicator}") if promo_name == '' else promo_name_label.setText(f"Name")
            promo_type_label.setText(f"Type {qss.req_field_indicator}") if promo_type == '' else promo_type_label.setText(f"Type")
            promo_percent_label.setText(f"Percent {qss.inv_field_indicator}") if promo_percent.replace('.', '', 1).isdigit() is False else promo_percent_label.setText(f"Percent")

            QMessageBox.critical(dialog, 'Error', 'Please fill out all required fields.')
    pass
class MyPromoView(MyWidget):
    def __init__(self, model: MyPromoModel):
        super().__init__()

        self.m = model

        self.set_promo_box()

    def set_promo_box(self):
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

        self.promo_act_box = MyGroupBox()
        self.promo_act_layout = MyHBoxLayout()
        self.promo_act_layout.addWidget(self.filter_box,0,Qt.AlignmentFlag.AlignLeft)
        self.promo_act_layout.addWidget(self.manage_data_box,1,Qt.AlignmentFlag.AlignRight)
        self.promo_act_box.setLayout(self.promo_act_layout)

        self.promo_overview_table = MyTableWidget(object_name='promo_overview_table')
        self.promo_overview_prev_button = MyPushButton(text='Prev')
        self.promo_overview_page_label = MyLabel(text=f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.promo_overview_next_button = MyPushButton(text='Next')
        self.promo_overview_act_box = MyGroupBox()
        self.promo_overview_act_layout = MyHBoxLayout()
        self.promo_overview_act_layout.addWidget(self.promo_overview_prev_button)
        self.promo_overview_act_layout.addWidget(self.promo_overview_page_label)
        self.promo_overview_act_layout.addWidget(self.promo_overview_next_button)
        self.promo_overview_act_box.setLayout(self.promo_overview_act_layout)
        self.promo_overview_box = MyGroupBox()
        self.promo_overview_layout = MyVBoxLayout()
        self.promo_overview_layout.addWidget(self.promo_overview_table)
        self.promo_overview_layout.addWidget(self.promo_overview_act_box,0,Qt.AlignmentFlag.AlignCenter)
        self.promo_overview_box.setLayout(self.promo_overview_layout)
        
        self.promo_sort_tab = MyTabWidget()
        self.promo_sort_tab.addTab(self.promo_overview_box, 'Overview')

        self.main_layout = MyVBoxLayout()
        self.main_layout.addWidget(self.promo_act_box)
        self.main_layout.addWidget(self.promo_sort_tab)
        self.setLayout(self.main_layout)

    def set_manage_data_box(self):
        self.promo_name_field = MyLineEdit(object_name='promo_name_field')
        self.promo_name_label = MyLabel(text='Name')
        self.promo_type_field = MyComboBox(object_name='promo_type_field')
        self.promo_type_label = MyLabel(text='Type')
        self.promo_percent_field = MyLineEdit(object_name='promo_percent_field')
        self.promo_percent_label = MyLabel(text='Percent')
        self.promo_desc_field = MyPlainTextEdit(object_name='promo_desc_field')
        self.promo_desc_label = MyLabel(text='Description')
        self.field_box = MyGroupBox()
        self.field_layout = MyFormLayout()
        self.field_layout.addRow(self.promo_name_label)
        self.field_layout.addRow(self.promo_name_field)
        self.field_layout.addRow(self.promo_type_label)
        self.field_layout.addRow(self.promo_type_field)
        self.field_layout.addRow(self.promo_percent_label)
        self.field_layout.addRow(self.promo_percent_field)
        self.field_layout.addRow(self.promo_desc_label)
        self.field_layout.addRow(self.promo_desc_field)
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
        self.promo_overview_act_box = MyGroupBox(object_name='promo_overview_act_box')
        self.promo_overview_act_layout = MyHBoxLayout(object_name='promo_overview_act_layout')
        self.promo_overview_act_layout.addWidget(self.edit_data_button)
        self.promo_overview_act_layout.addWidget(self.view_data_button)
        self.promo_overview_act_layout.addWidget(self.delete_data_button)
        self.promo_overview_act_box.setLayout(self.promo_overview_act_layout)

    def set_view_dialog(self):
        self.promo_name_info = MyLabel(text=f"promo_name")
        self.promo_type_info = MyLabel(text=f"promo_type")
        self.promo_percent_info = MyLabel(text=f"promo_percent")
        self.promo_desc_info = MyLabel(text=f"promo_desc")
        self.datetime_created_info = MyLabel(text=f"datetime_created")
        self.info_box = MyGroupBox()
        self.info_layout = MyFormLayout()
        self.info_layout.addRow('Name:', self.promo_name_info)
        self.info_layout.addRow('Type:', self.promo_type_info)
        self.info_layout.addRow('Percent:', self.promo_percent_info)
        self.info_layout.addRow('Description:', self.promo_desc_info)
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
class MyPromoController:
    def __init__(self, model: MyPromoModel, view: MyPromoView):
        self.v = view
        self.m = model

        self.set_promo_box_conn()
        self.sync_ui()

    def set_promo_box_conn(self):
        self.v.filter_field.returnPressed.connect(self.on_filter_button_clicked)
        self.v.filter_button.clicked.connect(self.on_filter_button_clicked)
        self.v.import_data_button.clicked.connect(self.on_import_data_button_clicked)
        self.v.add_data_button.clicked.connect(self.on_add_data_button_clicked)
        self.v.promo_overview_prev_button.clicked.connect(self.on_overview_prev_button_clicked)
        self.v.promo_overview_next_button.clicked.connect(self.on_overview_next_button_clicked)
        pass
    def on_filter_button_clicked(self): # IDEA: src
        text_filter = self.v.filter_field.text()
        
        self.m.total_page_number = schema.select_promo_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0

        print(self.m.total_page_number, self.m.page_number)

        self.v.promo_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        
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
        self.m.progress_percent = int((self.m.progress_count * 100) / total_data_count)
        self.v.progress_dialog.setWindowTitle(f"{self.m.progress_percent}% complete")
        self.v.progress_bar.setValue(self.m.progress_percent)
        self.v.progress_label.setText(current_data)
        pass
    def on_data_import_thread_cancelled(self):
        QMessageBox.information(self.v, 'Cancelled', 'Import cancelled.')
        pass
    def on_data_import_thread_finished(self):
        QMessageBox.information(self.v, 'Success', 'Import complete.')
        self.v.progress_dialog.close_signal.emit('finished')
        self.v.progress_dialog.close()
        pass
    def on_data_import_thread_invalid(self):
        QMessageBox.critical(self.v, 'Error', 'An error occurred during import.')
        self.v.progress_dialog.close()
        pass

    def on_add_data_button_clicked(self): # IDEA: src
        self.v.set_manage_data_box()
        self.load_combo_box_data()
        self.set_manage_data_box_conn(task='add_data')
        self.v.manage_data_dialog.exec()
        pass

    def populate_overview_table(self, text='', page_number=1): # IDEA: src
        self.v.promo_overview_prev_button.setEnabled(page_number > 1)
        self.v.promo_overview_next_button.setEnabled(page_number < self.m.total_page_number)
        self.v.promo_overview_page_label.setText(f"Page {page_number}/{self.m.total_page_number}")

        promo_data = schema.select_data_as_display(text=text, page_number=page_number)

        self.v.promo_overview_table.setRowCount(len(promo_data))

        for i, data in enumerate(promo_data):
            self.v.set_overview_table_act_box()
            promo_name = QTableWidgetItem(f"{data[0]}")
            promo_type = QTableWidgetItem(f"{data[1]}")
            promo_percent = QTableWidgetItem(f"{data[2]}")
            promo_desc = QTableWidgetItem(f"{data[3]}")
            datetime_created = QTableWidgetItem(f"{data[4]}")

            self.v.promo_overview_table.setCellWidget(i, 0, self.v.promo_overview_act_box)
            self.v.promo_overview_table.setItem(i, 1, promo_name)
            self.v.promo_overview_table.setItem(i, 2, promo_type)
            self.v.promo_overview_table.setItem(i, 3, promo_percent)
            self.v.promo_overview_table.setItem(i, 4, promo_desc)
            self.v.promo_overview_table.setItem(i, 5, datetime_created)

            self.v.edit_data_button.clicked.connect(lambda _, data=data: self.on_edit_data_button_clicked(data))
            self.v.view_data_button.clicked.connect(lambda _, data=data: self.on_view_data_button_clicked(data))
            self.v.delete_data_button.clicked.connect(lambda _, data=data: self.on_delete_data_button_clicked(data))
        pass
    def on_edit_data_button_clicked(self, data):
        self.v.set_manage_data_box()
        self.load_combo_box_data()
        self.v.manage_data_dialog.setWindowTitle(f"{data[0]}")
        sel_promo_data = schema.select_promo_data(data[0], data[1])

        for i, sel_data in enumerate(sel_promo_data):
            self.v.promo_name_field.setText(str(sel_data[0]))
            self.v.promo_type_field.setCurrentText(str(sel_data[1]))
            self.v.promo_percent_field.setText(str(sel_data[2]))
            self.v.promo_desc_field.setPlainText(str(sel_data[3]))
            self.m.sel_promo_id = sel_data[4]
            pass
        
        self.set_manage_data_box_conn(task='edit_data')
        self.v.manage_data_dialog.exec()
        pass
    def on_view_data_button_clicked(self, data):
        self.v.set_view_dialog()
        self.v.view_data_dialog.setWindowTitle(f"{data[0]}")

        self.v.promo_name_info.setText(str(data[0]))
        self.v.promo_type_info.setText(str(data[1]))
        self.v.promo_percent_info.setText(str(data[2]))
        self.v.promo_desc_info.setText(str(data[3]))
        self.v.datetime_created_info.setText(str(data[4]))

        self.set_view_data_box_conn()
        self.v.view_data_dialog.exec()
        pass
    def set_view_data_box_conn(self):
        self.v.view_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.view_data_dialog))
    def on_delete_data_button_clicked(self, data):
        sel_promo_data = schema.select_promo_data(data[0], data[1])

        for i, sel_data in enumerate(sel_promo_data):
            promo_name = sel_data[0]
            promo_id = sel_data[4]

        confirm = QMessageBox.warning(self.v, 'Confirm', f"Delete {promo_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            schema.delete_promo_data(promo_id)

            QMessageBox.information(self.v, 'Success', f"{promo_name} has been deleted.")

        self.sync_ui()
        pass

    def on_overview_prev_button_clicked(self):
        if self.m.page_number > 1: 
            self.m.page_number -= 1

            self.v.promo_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass
    def on_overview_next_button_clicked(self):
        if self.m.page_number < self.m.total_page_number:
            self.m.page_number += 1

            self.v.promo_overview_page_label.setText(f"Page {self.m.page_number}/{self.m.total_page_number}")
        self.populate_overview_table(text=self.v.filter_field.text(), page_number=self.m.page_number)
        pass

    # IDEA: if the widget uses the same connection
    def set_manage_data_box_conn(self, task):
        self.v.save_data_button.clicked.connect(lambda: self.on_save_data_button_clicked(task))
        self.v.manage_data_act_close_button.clicked.connect(lambda: self.close_dialog(self.v.manage_data_dialog))
        pass
    def load_combo_box_data(self):
        self.v.set_manage_data_box()

        promo_type_data = schema.select_promo_type_for_combo_box()

        for promo_type in promo_type_data: self.v.promo_type_field.addItems(promo_type)
    def on_save_data_button_clicked(self, task):
        promo_name = self.v.promo_name_field.text()
        promo_type = self.v.promo_type_field.currentText()
        promo_percent = self.v.promo_percent_field.text()
        promo_desc = self.v.promo_desc_field.toPlainText()

        self.m.init_manage_data_entry(
            self.v.manage_data_dialog, 
            task, 
            self.v.promo_name_label,
            self.v.promo_type_label,
            self.v.promo_percent_label,
            promo_name, 
            promo_type, 
            promo_percent, 
            promo_desc
        )

        self.sync_ui()

    def sync_ui(self):
        text_filter = self.v.filter_field.text()

        self.m.total_page_number = schema.select_promo_data_total_page_count(text=text_filter)
        self.m.page_number = 1 if self.m.total_page_number > 0 else 0
        self.populate_overview_table(text=text_filter, page_number=self.m.page_number)
        pass
    def close_dialog(self, dialog: QDialog):
        dialog.close()

class MyPromoWindow(MyGroupBox):
    def __init__(self, name='test', phone='test'):

        self.model = MyPromoModel(name, phone)
        self.view = MyPromoView(self.model)
        self.controller = MyPromoController(self.model, self.view)

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
    promo_window = MyPromoWindow()

    promo_window.run()

    app.exec()