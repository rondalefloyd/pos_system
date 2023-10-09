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

        self.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)

        if object_name == 'prod_list_tab':
            self.setStyleSheet(f"""
                QTabWidget#{object_name}::pane {{ background-color: #fff; border: 0px }}
                QTabBar::tab {{ border: 0px; padding: 10px 5px; min-width: 90px }}
                QTabBar::tab:selected {{ border-bottom: 2px solid {qss_config.default_color_g}; }}
                QTabBar::tab:!selected {{ border-bottom: 2px solid transparent; }}
            """)
    
        if object_name == 'cust_order_tab':
            self.setStyleSheet(f"""
                QTabWidget#{object_name}::pane {{ background-color: #fff; border: 0px }}
                QTabBar::tab {{ background-color: #fff; border: 0px; border-right: 1 solid {qss_config.default_color_e}; padding: 5px; min-width: 90px }}
                QTabBar::tab:!selected {{ background-color: {qss_config.default_color_c}; border-right: 1px solid {qss_config.default_color_e}; }}
            """)
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
        
        if object_name == 'my_sales_view':
            self.setStyleSheet(f"""
                QWidget {{ font: 12px 'Arial' }}
            """)
        pass
class MyGroupBox(QGroupBox):
    def __init__(self, object_name=''):
        super().__init__()

        self.setObjectName(object_name)

        self.setStyleSheet(f"""
            QGroupBox#{object_name} {{ border:0px }}
        """)

        if object_name == 'b_panel':
            self.setFixedWidth(400)
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{ border: 0px; border-left: 1px solid {qss_config.default_color_d} }}
            """)
        pass

        if object_name == 'numpad_panel':
            self.hide()

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
            

        if object_name == 'table_act_panel_layout':
            self.setContentsMargins(0,0,0,0)
            pass

        if object_name in [
            'order_ba_sub_act_panel_layout',
            'order_bb_sub_act_panel_layout'
        ]:
            self.setContentsMargins(10,0,10,10)
            self.setSpacing(3)

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
            'order_total',

            'fin_subtotal_label',
            'fin_discount_label',
            'cust_loy_discount_label',
            'fin_tax_label',
            'fin_total_label'
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

class MyIcon(QIcon):
    def __init__(self, icon_name=''):
        super().__init__()
        
        if icon_name == 'verified_cust_icon':
            self.addFile(os.path.abspath('src/icons/content_panel/verified_cust_icon.png'))

