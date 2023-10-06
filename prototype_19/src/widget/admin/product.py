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
            QTableWidget#primary_data_list_table { border: 0px; border-bottom: 1px solid #ddd }
            QTableWidget#category_data_list_table { border: 0px; border-bottom: 1px solid #ddd }
            QTableWidget#price_data_list_table { border: 0px; border-bottom: 1px solid #ddd }
            QTableWidget#inventory_data_list_table { border: 0px; border-bottom: 1px solid #ddd }
                           
            QHeaderView::section { background-color: rgba(255,255,255,255); border: 0px; border-bottom: 1px solid #ddd; }
            QTableWidget::item { border: 0px; border-bottom: 1px solid #ccc; font-size: 10px; padding: 0px 20px }
        ''')

        if object_name in [
            'data_list_table',
            'primary_data_list_table',
            'category_data_list_table',
            'price_data_list_table',
            'inventory_data_list_table'
        ]:
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setMinimumSectionSize(160)
            self.verticalHeader().setVisible(False)
            self.verticalHeader().setDefaultSectionSize(50)
            pass

        if object_name == 'data_list_table':
            self.setColumnCount(10)
            self.setHorizontalHeaderLabels([
                'Action',
                'Item name',
                'Brand',
                'Sales group',
                'Sell price',
                'Discount value',
                'Effective date',
                'Promo name',
                'Inventory tracking',
                'Date and time created'
            ])
            pass
        if object_name == 'primary_data_list_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action', 'Barcode', 'Item name', 'Expire date', 'Date and time created'])
            pass
        if object_name == 'category_data_list_table':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['Action', 'Item name', 'Item type', 'Brand', 'Sales group', 'Supplier', 'Date and time created'])
            pass
        if object_name == 'price_data_list_table':
            self.setColumnCount(8)
            self.setHorizontalHeaderLabels(['Action', 'Item name', 'Cost', 'Sell price', 'Discount value', 'Effective date', 'Promo name', 'Date and time created'])
            pass
        if object_name == 'inventory_data_list_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action', 'Item name', 'Available stock', 'On hand stock', 'Date and time created'])
            pass
    
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
            QLineEdit#text_filter_field {{ padding: 3px 5px }}
            """)

        if object_name == 'data_list_action_panel':
            pass

        if object_name == 'form_panel':
            self.setFixedWidth(300)

            self.setStyleSheet(f"""
                QGroupBox {{ background-color: #fff; border: 0px }}
                QGroupBox#{object_name} {{ border-top: 1px solid #ddd; border-left: 1px solid #ddd }}
                QScrollArea#form_scroll_area {{ border: 0px }}
            """)

        if object_name in [
            'primary_info_page',
            'category_info_page',
            'price_info_page',
            'inventory_info_page'
        ]:
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{background-color: #eee; border: 0px; border-top: 3px solid {color_scheme.hex_main}}}
                QLabel {{ color: #222 }}
            """)
            pass

        if object_name == 'extra_info_panel':
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{ background-color: {color_scheme.hex_main}; border: 0px }}
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

        if object_name in [
            'data_list_pgn_panel_layout',
            'primary_data_list_pgn_panel_layout',
            'category_data_list_pgn_panel_layout',
            'price_data_list_pgn_panel_layout',
            'inventory_data_list_pgn_panel_layout'
        ]:
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
            # self.setStyleSheet(f"""
            #     QLabel#{object_name} {{ font-size: 10px }}
            # """)
            pass
        
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
            QPushButton#data_list_view_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; font-size: 10px; padding: 3px }}
            QPushButton#data_list_delete_button {{ background-color: {color_scheme.hex_delete}; border: 0px; border-radius: 3px; color: #222; padding: 3px }}

            QPushButton#data_list_edit_button:hover, 
            QPushButton#data_list_view_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
            QPushButton#data_list_delete_button:hover {{ background-color: {color_scheme.hex_delete_hover} }}
        """

        self.form_close_button_ss = f"""
            QPushButton#form_close_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; padding: 10px }}
            QPushButton#form_close_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
        """
        self.form_save_new_button_ss = f"""
            QPushButton#form_save_new_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; padding: 10px }}
            QPushButton#form_save_new_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
        """
        self.form_save_edit_button_ss = f"""
            QPushButton#form_save_edit_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; padding: 10px }}
            QPushButton#form_save_edit_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
        """

        self.data_mgt_button_ss = f"""
            QPushButton#data_mgt_sync_button, 
            QPushButton#data_mgt_import_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; padding: 3px }}
            QPushButton#data_mgt_add_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; font-size: 10px; padding: 3px }}

            QPushButton#data_mgt_sync_button:hover, 
            QPushButton#data_mgt_import_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
            QPushButton#data_mgt_add_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
        """

        self.data_list_pgn_button_ss = f"""
            QPushButton#data_list_pgn_prev_button, QPushButton#data_list_pgn_next_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; padding: 3px }}
            QPushButton#data_list_pgn_prev_button:hover, QPushButton#data_list_pgn_next_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
        """

        edit_icon_path = os.path.abspath('src/icons/content_panel/edit.png')
        view_icon_path = os.path.abspath('src/icons/content_panel/view.png')
        delete_icon_path = os.path.abspath('src/icons/content_panel/delete.png')

        sync_icon_path = os.path.abspath('src/icons/content_panel/sync.png')
        import_icon_path = os.path.abspath('src/icons/content_panel/import.png')
        add_icon_path = os.path.abspath('src/icons/content_panel/add.png')

        prev_icon_path = os.path.abspath('src/icons/content_panel/prev.png')
        next_icon_path = os.path.abspath('src/icons/content_panel/next.png')

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
            self.setMinimumWidth(400)
            self.setPlaceholderText('Filter product')
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
