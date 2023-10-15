import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import QSSConfig

qss_config = QSSConfig()

class MyStackedWidget(QStackedWidget):
    def __init__(self, object_name=''):
        super().__init__()
    
        self.setObjectName(object_name)
    
    pass
class MyScrollArea(QScrollArea):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

    pass
class MyTabWidget(QTabWidget):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

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

    pass
class MyTableWidget(QTableWidget):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

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


