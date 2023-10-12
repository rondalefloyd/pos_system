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
        
        if object_name == 'prod_list_table_a':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['Action','Product','Brand','Sales group','Price','Promo','Discount'])
            pass
        if object_name == 'prod_list_table_b':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['Action','Product','Brand','Sales group','Price','Promo','Discount'])
            pass

        if object_name == 'cust_order_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Quantity','Product','Price','Discount'])

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

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
    
        self.setObjectName(object_name)

        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
    
        self.setObjectName(object_name)

        if object_name == 'prod_list_a_act_layout':
            self.setContentsMargins(0,0,0,0)
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

        if object_name in [
            'barcode_scan_button_untoggle',
            'cust_order_restrict_button_untoggle',
        ]:
            self.hide()
        pass
class MyCheckBox(QCheckBox):
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

        if object_name == 'barcode_scan_field':
            self.hide()
        pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name=''):
        super().__init__()
    
        self.setObjectName(object_name)

        pass
class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)
        self.setText(text)

        pass

class MyIcon(QIcon):
    pass