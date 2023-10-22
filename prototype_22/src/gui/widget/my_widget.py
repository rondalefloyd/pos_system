import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))


class MyStackedWidget(QStackedWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass
class MyScrollArea(QScrollArea):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.setWidgetResizable(True)

        self.on_admin_window()

    def on_admin_window(self):
        if self.object_name == 'navbar_scra':
            self.setFixedWidth(150)
        pass
class MyTabWidget(QTabWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass
class MyWidget(QWidget):
    def __init__(self, object_name='', parent=None, window_title=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setWindowTitle(window_title)
        pass
class MyGroupBox(QGroupBox):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass

class MyDialog(QDialog):
    def __init__(self, object_name='', parent=None, window_title=''):
        super().__init__()

        self.object_name = object_name
        
        self.setObjectName(object_name)
        self.setWindowTitle(window_title)

        self.on_login_dialog()

    def on_login_dialog(self):
        pass

class MyTableWidget(QTableWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_promo_table()
        self.on_user_table()
        self.on_reward_table()
        self.on_customer_table()
        pass

    def on_promo_table(self):
        if self.object_name == 'promo_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Type','Percent','Description','Date/Time created'])
            pass

    def on_user_table(self):
        if self.object_name == 'user_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Password','Access level','Phone','Date/Time created'])
            pass

    def on_reward_table(self):
        if self.object_name == 'reward_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Unit','Points','Description','Date/Time created'])
            pass
        
    def on_customer_table(self):
        if self.object_name == 'customer_overview_table':
            self.setColumnCount(10)
            self.setHorizontalHeaderLabels(['Action','Name','Address','Barrio','Town','Phone','Age','Gender','Marital status','Date/Time created'])

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass
class MyGridLayout(QGridLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass
class MyFormLayout(QFormLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass

class MyLabel(QLabel):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)
        pass

class MyComboBox(QComboBox):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_global_combo_box()

    def on_global_combo_box(self):
        if self.object_name in [
            'user_name_field', 
            'promo_type_field',
            'customer_barrio_field',
            'customer_town_field',
        ]:
            self.setEditable(True)
        pass
class MyLineEdit(QLineEdit):
    def __init__(self, object_name='', push_button = None):
        super().__init__()

        self.object_name = object_name

        self.on_global_line_edit()

        self.on_promo_line_edit()

    def on_global_line_edit(self):
        if self.object_name == 'barcode_scan_field':
            self.hide()

    def on_promo_line_edit(self):
        if self.object_name == 'filter_field':
            self.setMinimumWidth(500)
            pass
        if self.object_name == 'barcode_scan_field':
            self.setMinimumWidth(200)
        pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass
class MyDateEdit(QDateEdit):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)

        self.on_global_push_button()

    def on_global_push_button(self):
        if self.object_name == 'untoggle':
            self.hide()
        pass
class MyCheckBox(QCheckBox):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)
        pass

class MyProgressBar(QProgressBar):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setTextVisible(False)
        self.setFixedHeight(20)