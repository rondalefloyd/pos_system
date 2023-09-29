import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

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

        if object_name == 'data_list_sorter_tab':
            self.setStyleSheet(f"""
                QGroupBox#data_list_pgn_panel {{  }}
                QTabBar::tab {{ height: 30px; width: 100px; }}
            """)
        pass
class MyTableWidget(QTableWidget):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        self.setWordWrap(False)
        self.setShowGrid(False)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setStyleSheet('''
            QTableWidget#data_list_table { border: 0px; border-bottom: 1px solid #ddd }
            QHeaderView::section { background-color: rgba(255,255,255,255); border: 0px; border-bottom: 1px solid #ddd; }
            QTableWidget::item { border: 0px; border-bottom: 1px solid #ccc; font-size: 10px; padding: 0px 20px }
        ''')

        if object_name == 'data_list_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Promo name','Promo type','Discount percent','Description','Date and time created'])
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.verticalHeader().setVisible(False)
            self.verticalHeader().setDefaultSectionSize(50)
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

        if object_name == 'content_panel':
            self.setStyleSheet(f"""
            QGroupBox {{ border: 0px }}
            QGroupBox#{object_name} {{ border-top: 1px solid #ddd }}
            QLineEdit#text_filter_field {{ padding: 5px }}
            """)

        if object_name == 'form_panel':
            self.setFixedWidth(300)

            self.setStyleSheet(f"""
                QGroupBox {{ background-color: #fff; border: 0px }}
                QGroupBox#{object_name} {{ border-top: 1px solid #ddd; border-left: 1px solid #ddd }}
                QScrollArea#form_scroll_area {{ border: 0px }}

                QGroupBox#primary_info_page {{ background-color: #fff; border: 0px; border-top: 3px solid #EE4E34 }}
                QGroupBox#category_info_page {{ background-color: #fff; border: 0px; border-top: 3px solid #EE4E34 }}
                QGroupBox#price_info_page {{ background-color: #fff; border: 0px; border-top: 3px solid #EE4E34 }}
                QGroupBox#inventory_info_page {{ background-color: #fff; border: 0px; border-top: 3px solid #EE4E34 }}

                QLabel {{ color: #222 }}
                QLineEdit#barcode_field {{ padding: 5px; margin-bottom: 10px }}
                QLineEdit#item_name_field {{ padding: 5px; margin-bottom: 10px }}
                QDateEdit#expire_dt_field {{ padding: 5px; }}

                QComboBox#item_type_field {{ padding: 5px; margin-bottom: 10px }}
                QComboBox#brand_field {{ padding: 5px; margin-bottom: 10px }}
                QComboBox#sales_group_field {{ padding: 5px; margin-bottom: 10px }}
                QComboBox#supplier_field {{ padding: 5px; }}

                QLineEdit#cost_field {{ padding: 5px; margin-bottom: 10px }}
                QLineEdit#sell_price_field {{ padding: 5px; margin-bottom: 10px }}
                QDateEdit#effective_dt_field {{ padding: 5px; margin-bottom: 10px }}
                QComboBox#promo_name_field {{ padding: 5px; margin-bottom: 10px }}
                QLineEdit#promo_type_field {{ padding: 5px; margin-bottom: 10px }}
                QLineEdit#discount_percent_field {{ padding: 5px; margin-bottom: 10px }}
                QLineEdit#discount_value_field {{ padding: 5px; margin-bottom: 10px }}
                QLineEdit#new_sell_price_field {{ padding: 5px; margin-bottom: 10px }}
                QDateEdit#start_dt_field {{ padding: 5px; margin-bottom: 10px }}
                QDateEdit {{ padding: 5px; }}

                QComboBox#inventory_tracking_field {{ padding: 5px; margin-bottom: 10px }}
                QLineEdit#available_stock_field {{ padding: 5px; margin-bottom: 10px }}
                QLineEdit#on_hand_stock_field {{ padding: 5px; }}
            """)

        if object_name in [
            'primary_info_page', 
            'category_info_page',
            'price_info_page',
            'inventory_info_page'
        ]:
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{background-color: #FCEDDA}};
            """)
            pass

        if object_name == 'extra_info_panel':
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{ background-color: #EE4E34; border: 0px }}
            """)
        pass

class MyDialog(QDialog):
    def __init__(self, object_name='', parent=None):
        super().__init__()
        
        self.setObjectName(object_name)

        self.setParent(parent)
        self.setWindowFlag(Qt.WindowType.Dialog)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        if object_name == 'data_list_view_dialog':
            self.setMinimumWidth(300)
            pass
        pass
class MyProgressDialog(QProgressDialog):
    def __init__(self, object_name='', parent=None):
        super().__init__()
        
        self.setObjectName(object_name)
        pass

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'data_list_pgn_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        if object_name == 'form_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'data_list_action_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(3)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if object_name == 'extra_info_panel_layout':
            self.setContentsMargins(10,5,10,5)

        if object_name == 'data_mgt_action_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(3)
        pass
class MyGridLayout(QGridLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'main_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
            pass

        pass
class MyFormLayout(QFormLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'form_page_layout':
            self.setContentsMargins(10,10,10,10)
            self.setSpacing(20)
        pass

        if object_name in [
            'primary_info_page_layout',
            'category_info_page_layout',
            'price_info_page_layout',
            'inventory_info_page_layout'
        ]:
            self.setContentsMargins(20,20,20,20)

class MyLabel(QLabel):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)

        self.setText(text)

        if object_name == 'total_data':
            self.setStyleSheet(f"QLabel#{object_name} {{ color: #fff; font-size: 10px }} ")

        if object_name in [
            'barcode_label',
            'item_name_label',
            'expire_dt_label',
            'item_type_label',
            'brand_label',
            'sales_group_label',
            'supplier_label',
            'cost_label',
            'sell_price_label',
            'effective_dt_label',
            'promo_name_label',
            'promo_type_label',
            'discount_percent_label',
            'discount_value_label',
            'new_sell_price_label',
            'start_dt_label',
            'end_dt_label',
            'inventory_tracking_label',
            'available_stock_label',
            'on_hand_stock_label'
        ]:
            self.setStyleSheet(f"""
                QLabel#{object_name} {{ font-size: 10px }}
            """)
        
        if object_name == 'view_dialog_labels':
            self.setFixedWidth(125)
            

        pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)

        self.data_list_action_button_ss = f"""
            QPushButton#data_list_edit_button, 
            QPushButton#data_list_view_button {{ background-color: #ddd; border: 0px; border-radius: 3px; color: #222; font-size: 10px; padding: 3px }}
            QPushButton#data_list_delete_button {{ background-color: #DC143C; border: 0px; border-radius: 3px; color: #222; padding: 3px }}

            QPushButton#data_list_edit_button:hover, 
            QPushButton#data_list_view_button:hover {{ background-color: rgba(0,0,0,60) }}
            QPushButton#data_list_delete_button:hover {{ background-color: rgba(190,0,30,225) }}
        """

        self.form_close_button_ss = f"""
            QPushButton#form_close_button {{ background-color: #ddd; border: 0px; border-radius: 3px; color: #222; padding: 10px }}
            QPushButton#form_close_button:hover {{ background-color: rgba(0, 0, 0, 50) }}
        """
        self.form_save_new_button_ss = f"""
            QPushButton#form_save_new_button {{ background-color: #EE4E34; border: 0px; border-radius: 3px; color: #fff; padding: 10px }}
            QPushButton#form_save_new_button:hover {{ background-color: rgba(218,58,42,255) }}
        """
        self.form_save_edit_button_ss = f"""
            QPushButton#form_save_edit_button {{ background-color: #EE4E34; border: 0px; border-radius: 3px; color: #fff; padding: 10px }}
            QPushButton#form_save_edit_button:hover {{ background-color: rgba(238,78,52,200) }}
        """

        self.data_mgt_button_ss = f"""
            QPushButton#data_mgt_sync_button, 
            QPushButton#data_mgt_import_button {{ background-color: #ddd; border: 0px; border-radius: 3px; color: #222; padding: 3px }}
            QPushButton#data_mgt_add_button {{ background-color: #EE4E34; border: 0px; border-radius: 3px; color: #fff; font-size: 10px; padding: 3px }}

            QPushButton#data_mgt_sync_button:hover, 
            QPushButton#data_mgt_import_button:hover {{ background-color: rgba(0, 0, 0, 30) }}
            QPushButton#data_mgt_add_button:hover {{ background-color: rgba(208,48,22,255) }}
            QPushButton#data_mgt_add_button:focus {{ background-color: rgba(208,48,22,255) }}
        """

        self.data_list_pgn_button_ss = f"""
            QPushButton#data_list_pgn_prev_button, QPushButton#data_list_pgn_next_button {{ background-color: #ddd; border: 0px; border-radius: 3px; color: #222; padding: 3px }}
            QPushButton#data_list_pgn_prev_button:hover, QPushButton#data_list_pgn_next_button:hover {{ background-color: rgba(0, 0, 0, 50) }}
        """

        edit_icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/content_panel/edit.png'))
        view_icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/content_panel/view.png'))
        delete_icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/content_panel/delete.png'))

        sync_icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/content_panel/sync.png'))
        import_icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/content_panel/import.png'))
        add_icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/content_panel/add.png'))

        prev_icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/content_panel/prev.png'))
        next_icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../icons/content_panel/next.png'))

        if object_name == 'data_list_edit_button':
            self.setIcon(QIcon(edit_icon_path))
            self.setIconSize(QSize(15,20))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass
        if object_name == 'data_list_view_button':
            self.setIcon(QIcon(view_icon_path))
            self.setIconSize(QSize(15,20))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass
        if object_name == 'data_list_delete_button':
            self.setIcon(QIcon(delete_icon_path))
            self.setIconSize(QSize(15,20))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass

        if object_name == 'form_close_button':
            self.setFixedWidth(100)

        if object_name == 'data_mgt_sync_button':
            self.setIcon(QIcon(sync_icon_path))
            self.setIconSize(QSize(15,20))
        if object_name == 'data_mgt_import_button':
            self.setIcon(QIcon(import_icon_path))
            self.setIconSize(QSize(15,20))
        if object_name == 'data_mgt_add_button':
            self.setIcon(QIcon(add_icon_path))
            self.setIconSize(QSize(15,20))

        if object_name == 'data_list_pgn_prev_button':
            self.setIcon(QIcon(prev_icon_path))
            self.setIconSize(QSize(15,20))
        if object_name == 'data_list_pgn_next_button':
            self.setIcon(QIcon(next_icon_path))
            self.setIconSize(QSize(15,20))
        pass
class MyComboBox(QComboBox):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name in [
            'item_type_field',
            'brand_field',
            'supplier_field'
        ]:
            self.setEditable(True)

        
        pass
class MyLineEdit(QLineEdit):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'text_filter_field':
            self.setMaximumWidth(600)
            self.setPlaceholderText('Filter item by name, type, discount percent, description, and date created')

        if object_name in [
            'promo_type_field',
            'discount_percent_field',
            'discount_value_field',
            'new_sell_price_field',
            'start_dt_field',
            'end_dt_field'
        ]:
            self.setDisabled(True)
        pass
class MyTextEdit(QTextEdit):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
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
