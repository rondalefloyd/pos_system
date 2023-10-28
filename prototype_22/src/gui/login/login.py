
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.gui.admin.admin import MyAdminWindow, MyAdminView
from src.gui.cashier.cashier import MyCashierWindow, MyCashierView
from src.gui.widget.my_widget import *
from src.core.sql.login import *


login_schema = MyLoginSchema()

class MyLoginModel:
    def __init__(self):
        pass

class MyLoginView(MyDialog):
    def __init__(self, model: MyLoginModel):
        super().__init__(object_name='MyLoginView', window_title='Login')

        self.model = model

        self.set_main_dialog()

    def set_main_dialog(self):
        self.main_layout = MyVBoxLayout()
        
        self.set_login_box()

        self.main_layout.addWidget(self.login_box)
        self.setLayout(self.main_layout)

    def set_login_box(self):
        self.login_box = MyGroupBox()
        self.login_layout = MyVBoxLayout()
        self.user_name_label = MyLabel(text='Username')
        self.user_name_field = MyComboBox(object_name='user_name_field')
        self.user_password_label = MyLabel(text='Password')
        self.user_password_field = MyLineEdit(object_name='user_password_field')
        self.login_button = MyPushButton(text='Login')
        self.login_layout.addWidget(self.user_name_label)
        self.login_layout.addWidget(self.user_name_field)
        self.login_layout.addWidget(self.user_password_label)
        self.login_layout.addWidget(self.user_password_field,4,Qt.AlignmentFlag.AlignTop)
        self.login_layout.addWidget(self.login_button,0,Qt.AlignmentFlag.AlignBottom)
        self.login_box.setLayout(self.login_layout)

    def set_dev_dialog(self):
        self.reg_user_name_label = MyLabel(text='Name')
        self.reg_user_name_field = MyComboBox(object_name='reg_user_name_field')
        self.reg_user_password_label = MyLabel(text='Password')
        self.reg_user_password_field = MyLineEdit(object_name='reg_user_password_field')
        self.reg_user_access_level_label = MyLabel(text='Access level')
        self.reg_user_access_level_field = MyComboBox(object_name='reg_user_access_level_field')
        self.reg_user_phone_label = MyLabel(text='Phone')
        self.reg_user_phone_field = MyLineEdit(object_name='reg_user_phone_field')
        self.reg_user_button = MyPushButton(text='Register')
        self.reg_user_table = MyTableWidget(object_name='reg_user_table')

        self.dev_dialog = MyDialog()
        self.dev_layout = MyGridLayout()
        self.dev_layout.addWidget(self.reg_user_name_label,0,0)
        self.dev_layout.addWidget(self.reg_user_name_field,1,0)
        self.dev_layout.addWidget(self.reg_user_password_label,2,0)
        self.dev_layout.addWidget(self.reg_user_password_field,3,0)
        self.dev_layout.addWidget(self.reg_user_access_level_label,4,0)
        self.dev_layout.addWidget(self.reg_user_access_level_field,5,0)
        self.dev_layout.addWidget(self.reg_user_phone_label,6,0)
        self.dev_layout.addWidget(self.reg_user_phone_field,7,0)
        self.dev_layout.addWidget(self.reg_user_button,6,0,Qt.AlignmentFlag.AlignRight)
        self.dev_layout.addWidget(self.reg_user_table,7,0)
        self.dev_dialog.setLayout(self.dev_layout)
        pass
class MyLoginController:
    def __init__(self, model: MyLoginModel, view: MyLoginView):
        self.view = view
        self.model = model

        self.init_main_dialog_conn()

    def init_main_dialog_conn(self):
        self.view.login_button.clicked.connect(self.on_login_button_clicked)
        pass
    def on_login_button_clicked(self):
        user_name = self.view.user_name_field.currentText()
        user_password = self.view.user_password_field.text()

        print('user_name:', user_name) # REVIEW!!!!
        print('user_password:', user_password) # REVIEW!!!!

        self.clear_login_field()
        
        if user_name == 'dev' and user_password == 'dev@2023':

            self.view.set_dev_dialog()

            self.load_combo_box_data()
            self.populate_reg_user_table()
            self.view.reg_user_button.clicked.connect(self.on_reg_user_button_clicked)

            self.view.dev_dialog.exec()

        else:
            user_data = login_schema.verify_user(
                user_name=user_name, 
                user_password=user_password
            )

            user_id = user_data[0]
            user_level = user_data[1]
            user_phone = user_data[2]


            if user_id > 0 and user_level == 1:
                self.view.close()
                subprocess.run(['python', '-Xfrozen_modules=off', 'src/gui/cashier/cashier.py', str(user_name), str(user_phone)])
                pass
            elif user_id > 0 and user_level == 2:
                self.view.close()
                subprocess.run(['python', '-Xfrozen_modules=off', 'src/gui/admin/admin.py', str(user_name), str(user_phone)])
                pass
            else:
                QMessageBox.critical(self.view, 'Error', 'User not found.')
            pass
    def on_reg_user_button_clicked(self):
        user_name = self.view.reg_user_name_field.currentText()
        user_password = self.view.reg_user_password_field.text()
        user_level = self.view.reg_user_access_level_field.currentText()
        user_phone = self.view.reg_user_phone_field.text()

        login_schema.insert_user_data(
            user_name=user_name,
            user_password=user_password,
            user_level=user_level,
            user_phone=user_phone
        )

        self.populate_reg_user_table()
        QMessageBox.information(self.view.dev_dialog, 'Success', 'User added.')
        pass
    def populate_reg_user_table(self):
        user_data = login_schema.select_user_data_as_display()

        self.view.reg_user_table.setRowCount(len(user_data))

        for i, data in enumerate(user_data):
            user_name = QTableWidgetItem(f"{data[0]}")
            user_password = QTableWidgetItem(f"{data[1]}")
            user_level = QTableWidgetItem(f"{data[2]}")
            user_phone = QTableWidgetItem(f"{data[3]}")

            self.view.reg_user_table.setItem(i, 0, user_name)
            self.view.reg_user_table.setItem(i, 1, user_password)
            self.view.reg_user_table.setItem(i, 2, user_level)
            self.view.reg_user_table.setItem(i, 3, user_phone)

    def load_combo_box_data(self):
        self.view.reg_user_name_field.clear()
        self.view.reg_user_access_level_field.clear()

        user_name_data = login_schema.select_user_name_for_combo_box()

        self.view.reg_user_access_level_field.addItem('1')
        self.view.reg_user_access_level_field.addItem('2')

        for user_name in user_name_data: self.view.reg_user_name_field.addItems(user_name)
        pass

    def clear_login_field(self):
        self.view.user_name_field.clearEditText()
        self.view.user_password_field.clear()

class MyLoginWindow:
    def __init__(self):
        self.model = MyLoginModel()
        self.view = MyLoginView(self.model)
        self.controller = MyLoginController(self.model, self.view)

    def run(self):
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    login_window = MyLoginWindow()

    login_window.run()

    sys.exit(app.exec())