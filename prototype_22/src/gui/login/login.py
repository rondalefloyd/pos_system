
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.gui.widget.my_widget import *

class MyLoginModel:
    def __init__(self):
        pass

    def get_login_field(
        self, 
        user_name_field: QComboBox, 
        user_password_field: QLineEdit
    ):
        user_name_val = user_name_field.currentText()
        user_password_val = user_password_field.text()

        return user_name_val, user_password_val
        pass
class MyLoginView(MyDialog):
    def __init__(self, model: MyLoginModel):
        super().__init__(window_title='Login')

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
        self.reg_user_name_field = MyComboBox()
        self.reg_user_password_label = MyLabel(text='Password')
        self.reg_user_password_field = MyLineEdit()
        self.reg_user_access_level_label = MyLabel(text='Access level')
        self.reg_user_access_level_field = MyComboBox()
        self.reg_user_button = MyPushButton(text='Register')
        self.reg_user_table = MyTableWidget()

        self.dev_dialog = MyDialog()
        self.dev_layout = MyGridLayout()
        self.dev_layout.addWidget(self.reg_user_name_label,0,0)
        self.dev_layout.addWidget(self.reg_user_name_field,1,0)
        self.dev_layout.addWidget(self.reg_user_password_label,2,0)
        self.dev_layout.addWidget(self.reg_user_password_field,3,0)
        self.dev_layout.addWidget(self.reg_user_access_level_label,4,0)
        self.dev_layout.addWidget(self.reg_user_access_level_field,5,0)
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
        user_name_val, user_password_val = self.model.get_login_field(self.view.user_name_field, self.view.user_password_field)

        if user_name_val == 'dev' and user_password_val == 'dev@2023':
            self.clear_login_field()

            self.view.set_dev_dialog()
            self.view.dev_dialog.exec()
        else:
            QMessageBox.critical(self.view, 'Error', 'User not found.')
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
        self.view.exec()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    login_window = MyLoginWindow()

    login_window.run()

    app.exec()