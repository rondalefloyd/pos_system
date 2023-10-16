
import sqlite3
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import QSSConfig
from src.sql.dev.dev import MyDevSchema

qss = QSSConfig()
schema = MyDevSchema()

class MyDevModel:
    def __init__(self):
        self.gdrive_path = 'G:' + f"/My Drive/"

    pass
class MyDevView(QWidget):
    def __init__(self, model: MyDevModel):
        super().__init__()

        self.model = model

        self.set_main_panel()

    def set_main_panel(self):
        self.main_layout = QFormLayout()

        self.user_list_table = QTableWidget()

        self.name_field = QLineEdit()
        self.password_field = QLineEdit()
        self.access_level_field = QComboBox()
        self.phone_field = QLineEdit()
        self.save_button = QPushButton('Save')

        self.main_layout.addRow(self.user_list_table)
        self.main_layout.addRow(self.name_field)
        self.main_layout.addRow(self.password_field)
        self.main_layout.addRow(self.access_level_field)
        self.main_layout.addRow(self.phone_field)
        self.main_layout.addRow(self.save_button)
        self.setLayout(self.main_layout)
        pass
    pass

class MyDevController:
    def __init__(self, model: MyDevModel, view: MyDevView):
        self.view = view
        self.model = model

        self.set_main_panel_conn()
        self.populate_access_level_field()
        self.populate_user_list_table()
        pass
    
    def set_main_panel_conn(self):
        self.view.save_button.clicked.connect(self.on_save_button_clicked)
        pass

    def populate_user_list_table(self):
        self.user_list_data = schema.list_user_data()

        self.view.user_list_table.setColumnCount(4)
        self.view.user_list_table.setRowCount(len(self.user_list_data))

        self.view.user_list_table.setHorizontalHeaderLabels(['Nmae','Password','Access level','Phone'])

        for row_i, row_v in enumerate(self.user_list_data):
            name = QTableWidgetItem(str(row_v[0]))
            password = QTableWidgetItem(str(row_v[1]))
            access_level = QTableWidgetItem(str(row_v[2]))
            phone = QTableWidgetItem(str(row_v[3]))

            self.view.user_list_table.setItem(row_i, 0, name)
            self.view.user_list_table.setItem(row_i, 1, password)
            self.view.user_list_table.setItem(row_i, 2, access_level)
            self.view.user_list_table.setItem(row_i, 3, phone)

        pass
    def populate_access_level_field(self):
        self.view.access_level_field.addItem('1')
        self.view.access_level_field.addItem('2')
        self.view.access_level_field.addItem('3')

    def on_save_button_clicked(self):
        name = self.view.name_field.text()
        password = self.view.password_field.text()
        access_level = self.view.access_level_field.currentText()
        phone = self.view.phone_field.text()

        schema.add_new_user(user_name=name, user_password=password, user_level=access_level, user_phone=phone)

        print('SAVED!')
    pass

class MyDevWindow:
    def __init__(self):
        super().__init__()

        self.model = MyDevModel()
        self.view = MyDevView(self.model)
        self.controller = MyDevController(self.model, self.view)

    def run(self):
        self.view.show()
    pass

# # NOTE: For testing purpsoes only.
# if __name__ == ('__main__'):
#     app = QApplication(sys.argv)
#     dev_window = MyDevWindow()

#     dev_window.run()
#     app.exec()