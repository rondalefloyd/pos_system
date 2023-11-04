
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from src.gui.admin.product import MyProductWindow
from src.gui.admin.promo import MyPromoWindow
from src.gui.admin.reward import MyRewardWindow
from src.gui.admin.customer import MyCustomerWindow
from src.gui.admin.user import MyUserWindow
from src.gui.widget.my_widget import *

class MyAdminModel:
    def __init__(self, user, phone):
        self.user = user
        pass
class MyAdminView(MyWidget):
    def __init__(self, model: MyAdminModel):
        super().__init__(object_name='MyAdminView', window_title='Admin')
        self.setWindowState(Qt.WindowState.WindowMaximized)

        self.m = model

        self.set_main_window()

    def set_main_window(self):
        self.set_navbar_box()
        self.set_page_stcw()
        self.set_extra_info_box()
        
        self.main_layout = MyGridLayout()
        self.main_layout.addWidget(self.navbar_scra,0,0)
        self.main_layout.addWidget(self.page_stcw,0,1)
        self.main_layout.addWidget(self.extra_info_box,1,0,1,2)
        self.setLayout(self.main_layout)

    def set_navbar_box(self):
        self.product_page_button = MyPushButton(object_name='product_page_button', text='  Product', disabled=True)
        self.promo_page_button = MyPushButton(object_name='promo_page_button', text='  Promo')
        self.reward_page_button = MyPushButton(object_name='reward_page_button', text='  Reward')
        self.customer_page_button = MyPushButton(object_name='customer_page_button', text='  Customer')
        self.user_page_button = MyPushButton(object_name='user_page_button', text='  User')
        self.logout_button = MyPushButton(object_name='logout_button', text='  Logout')
        self.navbar_box = MyGroupBox(object_name='navbar_box')
        self.navbar_layout = MyFormLayout(object_name='navbar_layout')
        self.navbar_layout.addRow(self.product_page_button)
        self.navbar_layout.addRow(self.promo_page_button)
        self.navbar_layout.addRow(self.reward_page_button)
        self.navbar_layout.addRow(self.customer_page_button)
        self.navbar_layout.addRow(self.user_page_button)
        self.navbar_layout.addRow(self.logout_button)
        self.navbar_box.setLayout(self.navbar_layout)
        self.navbar_scra = MyScrollArea(object_name='navbar_scra')
        self.navbar_scra.setWidget(self.navbar_box)
        pass
    
    def set_page_stcw(self):
        self.product_page_window = MyProductWindow(self.m.user)
        self.promo_page_window = MyPromoWindow(self.m.user)
        self.reward_page_window = MyRewardWindow(self.m.user)
        self.customer_page_window = MyCustomerWindow(self.m.user)
        self.user_page_window = MyUserWindow(self.m.user)
        self.settings_page_window = MyGroupBox()
        self.page_stcw = MyStackedWidget()
        self.page_stcw.addWidget(self.product_page_window)
        self.page_stcw.addWidget(self.promo_page_window)
        self.page_stcw.addWidget(self.reward_page_window)
        self.page_stcw.addWidget(self.customer_page_window)
        self.page_stcw.addWidget(self.user_page_window)
        self.page_stcw.addWidget(self.settings_page_window)

    def set_extra_info_box(self):
        self.current_user_label = MyLabel(object_name='current_user_label', text=f"Current user: {self.m.user}")
        self.extra_info_box = MyGroupBox(object_name='extra_info_box')
        self.extra_info_layout = MyHBoxLayout(object_name='extra_info_layout')
        self.extra_info_layout.addWidget(self.current_user_label)
        self.extra_info_box.setLayout(self.extra_info_layout)
        pass
class MyAdminController:
    def __init__(self, model: MyAdminModel, view: MyAdminView):
        self.v = view
        self.m = model

        self.set_navbar_box_conn()

    def set_navbar_box_conn(self):
        self.v.product_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=0))
        self.v.promo_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=1))
        self.v.reward_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=2))
        self.v.customer_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=3))
        self.v.user_page_button.clicked.connect(lambda: self.on_page_button_clicked(index=4))
        self.v.logout_button.clicked.connect(self.on_logout_button_clicked)

    def on_page_button_clicked(self, index):
        self.v.page_stcw.setCurrentIndex(index)

        self.v.product_page_window.controller.sync_ui() if index == 0 else None
        self.v.promo_page_window.controller.sync_ui() if index == 1 else None
        self.v.reward_page_window.controller.sync_ui() if index == 2 else None
        self.v.customer_page_window.controller.sync_ui() if index == 3 else None
        self.v.user_page_window.controller.sync_ui() if index == 4 else None

        self.v.product_page_button.setDisabled(index == 0)
        self.v.promo_page_button.setDisabled(index == 1)
        self.v.reward_page_button.setDisabled(index == 2)
        self.v.customer_page_button.setDisabled(index == 3)
        self.v.user_page_button.setDisabled(index == 4)
 
    def on_logout_button_clicked(self):
        confirm = QMessageBox.question(self.v, 'Confirm', 'Are you sure you want to logout?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm is QMessageBox.StandardButton.Yes:
            self.v.close_signal.emit('logout')
            self.v.close()

class MyAdminWindow:
    def __init__(self, user='test', phone='test'):
        self.model = MyAdminModel(user, phone)
        self.view = MyAdminView(self.model)
        self.controller = MyAdminController(self.model, self.view)

    def run(self):
        open('app_running.flag', 'w').close()
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    cashier_window = MyAdminWindow(user=sys.argv[1], phone=sys.argv[2])
    # cashier_window = MyAdminWindow(user='test', phone='test') # for testing only

    cashier_window.run()

    sys.exit(app.exec())