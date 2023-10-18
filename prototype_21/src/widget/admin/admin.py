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
        
        # NOTE: global attributes
        self.setObjectName(object_name)
        self.setWidgetResizable(True)

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
        self.object_name = object_name
        
        self.setObjectName(object_name)

        self.on_global_widgets()

        self.on_admin_widgets()
        self.on_pos_widgets()

    def on_global_widgets(self):
        if self.object_name == 'numpad_key_box':
            self.hide()

    def on_admin_widgets(self):
        if self.object_name == 'panel_a_box':
            self.setFixedWidth(250)
    
    def on_pos_widgets(self):
        if self.object_name == 'panel_b_box':
            self.setFixedWidth(450)
    pass
class MyDialog(QDialog):
    def __init__(self, object_name='', parent=None, window_title=''):
        super().__init__()
        
        self.setObjectName(object_name)
        self.setWindowTitle(window_title)

    pass
class MyTableWidget(QTableWidget):
    def __init__(self, object_name=''):
        super().__init__()
        self.object_name = object_name

        self.setObjectName(object_name)
        
        self.on_global_widgets()
        
        self.on_promo_widgets()
        self.on_user_widgets()
        self.on_cust_widgets()
        self.on_reward_widgets()
        self.on_prod_widgets()

        self.on_pos_widgets()

    def on_global_widgets(self):
        self.setWordWrap(False)
        self.setShowGrid(False)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    
    def on_promo_widgets(self):
        if self.object_name == 'promo_list_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Type','Percent','Description','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
    def on_user_widgets(self):
        if self.object_name == 'user_list_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Name','Password','Phone','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
    def on_cust_widgets(self):
        if self.object_name == 'cust_list_table':
            self.setColumnCount(11)
            self.setHorizontalHeaderLabels(['Action','Name','Address','Barrio','Town','Phone','Age','Gender','Marital_status','Points','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeMode.ResizeToContents)
    def on_reward_widgets(self):
        if self.object_name == 'reward_list_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Description','Unit','Points','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
    def on_prod_widgets(self):
        if self.object_name == 'prod_list_table':
            self.setColumnCount(15)
            self.setHorizontalHeaderLabels(['Action','Barcode','Product','Expire date','Item type','Brand','Sales group','Supplier','Cost','Price','Effective date','Promo','Discount value','Inventory tracking','Date/Time created'])

            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # 'Action',
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # 'Barcode',
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # 'Product',
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # 'Expire date',
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # 'Item type',
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # 'Brand',
            self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents) # 'Sales group',
            self.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents) # 'Supplier',
            self.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents) # 'Cost',
            self.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents) # 'Price',
            self.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeMode.ResizeToContents) # 'Effective date',
            self.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeMode.ResizeToContents) # 'Promo',
            self.horizontalHeader().setSectionResizeMode(12, QHeaderView.ResizeMode.ResizeToContents) # 'Discount value',
            self.horizontalHeader().setSectionResizeMode(13, QHeaderView.ResizeMode.ResizeToContents) # 'Inventory tracking',
            self.horizontalHeader().setSectionResizeMode(14, QHeaderView.ResizeMode.ResizeToContents) # 'Date/Time created'

        if self.object_name == 'stock_list_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Product','Available','On hand','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # 'Action',
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # 'Barcode',
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # 'Product',
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # 'Date/Time created'
    
    def on_pos_widgets(self):
        if self.object_name == 'pos_list_table':
            self.setColumnCount(9)
            self.setHorizontalHeaderLabels(['Action','Barcode','Product','Brand','Price','Effective date','Promo','Discount','On hand stock'])

            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # 'Action'
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # 'Barcode'
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # 'Product'
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # 'Brand'
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # 'Price'
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # 'Effective date'
            self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents) # 'Promo'
            self.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents) # 'Discuont'
            self.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents) # 'On hand stock'
    
        if self.object_name == 'order_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Qty','Product','Price','Discount'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch) # 'Action'
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # 'Action'
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # 'Action'
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # 'Action'
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # 'Action'

        if self.object_name == 'final_order_table':
            self.setColumnCount(3)
            self.setHorizontalHeaderLabels(['Qty','Product','Price'])  
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # 'Action'
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # 'Action'
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # 'Action'

    pass

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
        self.object_name = object_name
        
        self.setObjectName(object_name)

        self.on_admin_widgets()

    def on_admin_widgets(self):
        self.setContentsMargins(0,0,0,0)
        pass

    pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
        self.object_name = object_name

        self.setObjectName(object_name)

        self.on_global_widgets()

        self.on_promo_widgets()

    def on_global_widgets(self):
        if self.object_name == 'table_act_laoyut':
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setContentsMargins(0,0,0,0)

        if self.object_name in [
            'prod_list_pag_layout',
            'stock_list_pag_layout',
            'promo_list_pag_layout',
            'reward_list_pag_layout',
            'cust_list_pag_layout',
            'user_list_pag_layout',

            'prod_act_layout',
            'stock_act_layout',
            'promo_act_layout',
            'reward_act_layout',
            'cust_act_layout',
            'user_act_layout',

            'cust_order_act_layout',
        ]:
            self.setContentsMargins(0,0,0,0)

    def on_promo_widgets(self):
        pass
        
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
class MyComboBox(QComboBox):
    def __init__(self, object_name=''):
        super().__init__()
        self.object_name = object_name

        self.setObjectName(object_name)

        self.on_promo_widgets()
        self.on_cust_widgets()
        self.on_product_widgets()

    def on_promo_widgets(self):
        if self.object_name == 'promo_type_field':
            self.setEditable(True)
        pass
    def on_cust_widgets(self):
        if self.object_name in ['cust_barrio_field', 'cust_town_field']:
            self.setEditable(True)
    def on_product_widgets(self):
        if self.object_name in [
            'prod_type_field',
            'prod_brand_field',
            'prod_supplier_field',
        ]:
            self.setEditable(True)
    pass
class MyLineEdit(QLineEdit):
    def __init__(self, object_name='', push_button = None):
        super().__init__()
        
        self.object_name = object_name
        self.push_button: QPushButton = push_button

        self.setObjectName(object_name)

        self.on_promo_widgets()
        self.on_product_widgets()

    def on_promo_widgets(self):
        if self.object_name == 'text_filter_field':
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.setContentsMargins(0,0,0,0)
            layout.addWidget(self.push_button)
            self.setLayout(layout)

        pass
    def on_product_widgets(self):
        if self.object_name in [
            'prod_promo_type_field',
            'prod_promo_percent_field',
            'prod_promo_value_field',
            'prod_promo_sell_price_field',
        ]:
            self.setDisabled(True)
    pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
    
    pass
class MyDateEdit(QDateEdit):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate().currentDate())
    pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text=''):
        super().__init__()
        self.object_name = object_name
        
        self.setObjectName(object_name)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.on_global_widgets()

    def on_global_widgets(self):
        if self.object_name == 'numpad_key_untoggle_button':
            self.hide()
    pass
class MyCheckBox(QCheckBox):
    def __init__(self, object_name='', text=''):
        super().__init__()
        self.object_name = object_name
        
        self.setObjectName(object_name)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    pass

class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, text='', has_promo=False):
        super().__init__()

        self.has_promo = has_promo
        
        self.setText(text)

        self.on_prod_widgets()

    def on_prod_widgets(self):
        if self.has_promo is True:
            self.setForeground(QColor(255,0,0))