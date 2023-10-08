import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))

from src.core.color_scheme import *

color_scheme = ColorScheme()

class MyScrollArea(QScrollArea):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)
        pass
class MyTabWidget(QTabWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        self.setStyleSheet(f"""
            QTabWidget#{object_name}::pane {{ background-color: #fff; border: 0px }}
            QTabBar::tab {{ border: 0px; padding: 5px; width: 100px }} # TODO
        """)

        self.tabBar().setFixedHeight(100)
        pass
class MyTableWidget(QTableWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        self.setStyleSheet(f"""
            QTableWidget#{object_name} {{ background-color: #fff; border: 0px }}
        """)

        if object_name == 'a_prod_list_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Brand','Sales group','Price','Discount'])
            pass
        if object_name == 'b_prod_list_table':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['Action','Name','Brand','Sales group','Price','Discount','Promo'])
            pass
        if object_name == 'order_list_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Qty','Name','Price','Discount'])
            pass
        pass
class MyWidget(QWidget):
    def __init__(self, object_name='', parent=None):
        super().__init__()

        self.setObjectName(object_name)
        self.setParent(parent)
        pass
class MyGroupBox(QGroupBox):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        self.setStyleSheet(f"""
            QGroupBox#{object_name} {{ border:0px }}
        """)
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

        if object_name in [
            'a_prod_list_panel_layout',
            'b_prod_list_panel_layout'
        ]:
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        if object_name == 'order_b_act_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        if object_name in [
            'text_filter_panel_layout',
            'barcode_scan_panel_layout'
        ]:
            self.setContentsMargins(0,0,0,0)
            


        pass
class MyGridLayout(QGridLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        if object_name == 'main_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        if object_name == 'b_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        if object_name == 'cust_tab_cont_panel_panel':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
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

        if object_name in [
            'order_subtotal',
            'order_discount',
            'order_tax',
            'order_total'
        ]:
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)
        self.setText(text)

        if object_name in [
            'order_locked_button',
            'order_wholesale_button',
            'barcode_scan_toggled_button'
        ]:
            self.hide()
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
