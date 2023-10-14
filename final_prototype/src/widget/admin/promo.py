import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))

from src.core.qss_config import *

qss_config = QSSConfig()

class MyScrollArea(QScrollArea):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)
        self.setWidgetResizable(True)
        pass
class MyTabWidget(QTabWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        pass
class MyTableWidget(QTableWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        if object_name == 'promo_list_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Promo name','Promo type','Discount percent','Description'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        pass

class MyWidget(QWidget):
    def __init__(self, object_name='', parent=None):
        super().__init__()

        self.setObjectName(object_name)

        pass
class MyGroupBox(QGroupBox):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        pass

class MyDialog(QDialog):
    def __init__(self, object_name='', parent=None):
        super().__init__()

        self.setObjectName(object_name)
        self.setParent(parent)

        pass

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        if object_name == 'add_promo_form_act_layout':
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        if object_name == 'promo_list_pag_act_layout':
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pass
class MyGridLayout(QGridLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        pass
class MyFormLayout(QFormLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        pass

class MyLabel(QLabel):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.setObjectName(object_name)
        self.setText(text)
        pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.setObjectName(object_name)
        self.setText(text)

        pass
class MyComboBox(QComboBox):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        if object_name == 'add_promo_type_field':
            self.setEditable(True)
        pass
class MyLineEdit(QLineEdit):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        pass
