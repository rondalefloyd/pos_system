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

        self.on_admin_widgets()

    def on_admin_widgets(self):
        if self.object_name == 'panel_a_box':
            self.setFixedWidth(250)
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

    def on_global_widgets(self):
        self.setWordWrap(False)
        self.setShowGrid(False)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
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
            'product_list_pag_layout',
            'promo_list_pag_layout',
            'reward_list_pag_layout',
            'cust_list_pag_layout',
            'user_list_pag_layout',
        ]:
            self.setContentsMargins(0,0,0,0)


    def on_promo_widgets(self):
        if self.object_name == 'promo_act_layout':
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
        self.object_name = object_name
        
        self.setObjectName(object_name)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    pass
class MyComboBox(QComboBox):
    def __init__(self, object_name=''):
        super().__init__()
        self.object_name = object_name

        self.setObjectName(object_name)

        self.on_promo_widgets()
        self.on_cust_widgets()

    def on_promo_widgets(self):
        if self.object_name == 'promo_type_field':
            self.setEditable(True)
        pass
    def on_cust_widgets(self):
        if self.object_name in ['cust_barrio_field', 'cust_town_field']:
            self.setEditable(True)
    pass
class MyLineEdit(QLineEdit):
    def __init__(self, object_name='', push_button = None):
        super().__init__()
        
        self.object_name = object_name
        self.push_button: QPushButton = push_button

        self.setObjectName(object_name)

        self.on_promo_widgets()

    def on_promo_widgets(self):
        if self.object_name == 'text_filter_field':
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.setContentsMargins(0,0,0,0)
            layout.addWidget(self.push_button)
            self.setLayout(layout)

        pass

    pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)


