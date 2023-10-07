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

        if object_name == 'cart_tab':
            self.setStyleSheet(f"""
                QTabWidget#{object_name} {{ }}
                QTabBar::tab {{ height: 30px; }}

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
            QTableWidget#data_list_table,
            QTableWidget#cart_list_table { border: 0px; border-bottom: 1px solid #ddd; }
            QTableWidget#bill_review_cart_list { border: 0px; }
                           
            QHeaderView::section { background-color: #fff; border: 0px; border-bottom: 1px solid #ddd; }
                           
            QTableWidget#data_list_table::item { border: 0px; border-bottom: 1px solid #ccc; padding: 0px 20px }
            QTableWidget#cart_list_table::item { border: 0px; border-bottom: 1px solid #ccc; padding: 0px 5px }
            QTableWidget#bill_review_cart_list::item { border: 0px; padding: 0px 10px; }
        ''')

        if object_name == 'data_list_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels([
                'Action',
                'Barcode',
                'Item name',
                'Brand',
                'Sales group',
                'Sell price'
            ])
            self.horizontalHeader().setMinimumSectionSize(100)
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().resizeSection(0, 150)
            self.verticalHeader().setVisible(False)
            self.verticalHeader().setDefaultSectionSize(50)

        if object_name == 'cart_list_table':
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.setColumnCount(4)
            self.setHorizontalHeaderLabels(['Action','Qty','Item name','Price'])
            self.horizontalHeader().setMinimumSectionSize(50)
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().resizeSection(0, 110)
            self.verticalHeader().setVisible(False)
            self.verticalHeader().setDefaultSectionSize(50)
            pass
        if object_name == 'bill_review_cart_list':
            self.horizontalHeader().setObjectName('bill_review_cart_list')
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.setColumnCount(3)        
            self.setHorizontalHeaderLabels(['Qty','Item name','Price'])
            self.horizontalHeader().setMinimumSectionSize(60)
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            self.verticalHeader().setDefaultSectionSize(20)
            self.verticalHeader().setVisible(False)

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

        if object_name == 'text_filter_panel':
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{ border: 0px; }}
            """)

        if object_name == 'content_panel':
            self.setStyleSheet(f"""
            QGroupBox {{ border: 0px }}
            QGroupBox#{object_name} {{ border-top: 1px solid #ddd }}
            
            QLineEdit#text_filter_field,
            QLineEdit#data_mgt_scanned_barcode_field {{ padding: 3px 5px }}
            """)

        if object_name == 'data_list_action_panel':
            pass

        if object_name == 'sales_mgt_panel':
            self.setFixedWidth(400)

            self.setStyleSheet(f"""
                QGroupBox {{ background-color: #fff; border: 0px }}
                QGroupBox#{object_name} {{ border-top: 1px solid #ddd; border-left: 1px solid #ddd }}
                QScrollArea#sales_mgt_scroll_area {{ border: 0px }}
                QComboBox#customer_name_field {{ padding: 3px 5px }}
            """)

        if object_name == 'bill_review_panel':
            self.setFixedWidth(350)
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{ background-color: #fff; border: 0px; border-right: 1px solid #ddd; border-top: 1px solid #ddd }}
                QGroupBox#bill_review_summary {{  }}
            """)
        
        if object_name == 'payment_panel':
            self.setFixedWidth(300)
            self.setStyleSheet(f"""
                QGroupBox#{object_name} {{ border: 0px }}
                QGroupBox#amt_tendered_panel {{ border: 0px; border-top: 1px solid #ddd }}

                QLineEdit#amt_tendered_field {{ padding: 3px 5px }}

                QGroupBox#payment_action_button_panel {{border: 0px;  }}
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
        
        if object_name == 'payment_dialog':
            self.setFixedWidth(650)
            pass
        pass

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'data_list_pgn_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        if object_name == 'sales_mgt_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'text_filter_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(3)

        if object_name == 'data_list_action_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(3)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if object_name == 'extra_info_panel_layout':
            self.setContentsMargins(10,5,10,5)

        if object_name == 'data_mgt_action_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(3)

        if object_name == 'add_cart_tab_panel_layout':
            pass
        
        if object_name == 'cart_list_action_panel_layout':
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        if object_name == 'cart_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)
            pass

        if object_name == 'payment_dialog_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        pass
class MyFormLayout(QFormLayout):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'sales_mgt_page_layout':
            self.setContentsMargins(10,10,10,10)

        if object_name == 'cart_list_bill_layout':
            self.setContentsMargins(10,10,10,10)

        if object_name == 'payment_panel_layout':
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

        if object_name == 'bill_review_panel_layout':
            pass


class MyLabel(QLabel):
    def __init__(self, object_name='', text=''):
        super().__init__()
        
        self.setObjectName(object_name)

        self.setText(text)

        if object_name == 'total_data':
            self.setStyleSheet(f"QLabel#{object_name} {{ color: #fff; font-size: 10px }} ")

        if object_name in ['bill_value_label', 'bill_total_value_label']:
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            pass
        
        if object_name in ['bill_review_total', 'bill_total_value_label']:
            self.setStyleSheet(f"""
                QLabel#bill_review_total,
                QLabel#bill_total_value_label {{ font-weight: bold; }}
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

        self.text_filter_button_ss = f"""
            QPushButton#text_filter_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; font-size: 10px; padding: 3px }}
        """

        self.data_list_action_button_ss = f"""
            QPushButton#data_list_atc_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; font-size: 10px; padding: 3px }}
            QPushButton#data_list_view_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; font-size: 10px; padding: 3px }}

            QPushButton#data_list_atc_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
            QPushButton#data_list_view_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
        """

        self.add_cart_tab_button_ss = f"""
            QPushButton#add_cart_tab_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; font-size: 10px; padding: 3px }}
            QPushButton#add_cart_tab_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
        """

        self.cart_list_action_panel_ss = f"""
            QPushButton#cart_list_drop_all_qty_button {{ background-color: {color_scheme.hex_delete}; border: 0px; border-radius: 3px; color: #222; font-size: 10px; padding: 3px }}
            QPushButton#cart_list_drop_qty_button,
            QPushButton#cart_list_add_qty_button,
            QPushButton#cart_list_edit_qty_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; font-size: 10px; padding: 3px }}

            QPushButton#cart_list_drop_all_qty_button:hover {{ background-color: {color_scheme.hex_delete_hover} }}
            QPushButton#cart_list_drop_qty_button:hover,
            QPushButton#cart_list_add_qty_button:hover,
            QPushButton#cart_list_edit_qty_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
        """

        self.sales_mgt_discard_button_ss = f"""
            QPushButton#sales_mgt_discard_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; padding: 10px }}
            QPushButton#sales_mgt_discard_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
        """
        self.sales_mgt_pay_button_ss = f"""
            QLabel {{ color: #fff; font-weight: bold; font-size: 15px; }}
            QPushButton#sales_mgt_pay_button {{ background-color: {color_scheme.hex_main}; border: 0px; color: #fff; font-weight: bold; font-size: 25px; text-align: right; padding: 15px }}
            QPushButton#sales_mgt_pay_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
        """

        self.amt_tendered_opt_button_ss = f"""
            QPushButton#amt_tendered_opt_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; padding: 5px }}
            QPushButton#amt_tendered_opt_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
        """

        self.payment_back_button_ss = f"""
            QPushButton#payment_back_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; padding: 10px }}
            QPushButton#payment_back_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
        """
        self.process_payment_button_ss = f"""
            QPushButton#process_payment_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; padding: 10px }}
            QPushButton#process_payment_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
        """

        self.data_mgt_button_ss = f"""
            QPushButton#data_mgt_sync_button, 

            QPushButton#data_mgt_toggle_retail_txn_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; font-size: 10px; padding: 3px }}
            QPushButton#data_mgt_toggle_wholesale_txn_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; font-size: 10px; padding: 3px }}

            QPushButton#data_mgt_toggle_aatc_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; padding: 3px }}
            QPushButton#data_mgt_untoggle_aatc_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #222; padding: 3px }}

            QPushButton#data_mgt_add_button {{ background-color: {color_scheme.hex_main}; border: 0px; border-radius: 3px; color: #fff; font-size: 10px; padding: 3px }}

            
            QPushButton#data_mgt_sync_button:hover, 

            QPushButton#data_mgt_toggle_retail_txn_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
            QPushButton#data_mgt_toggle_wholesale_txn_button:hover {{ background-color: {color_scheme.hex_main_hover} }}

            QPushButton#data_mgt_toggle_aatc_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
            QPushButton#data_mgt_untoggle_aatc_button:hover {{ background-color: {color_scheme.hex_main_hover} }}

            QPushButton#data_mgt_add_button:hover {{ background-color: {color_scheme.hex_main_hover} }}
        """

        self.data_list_pgn_button_ss = f"""
            QPushButton#data_list_pgn_prev_button, QPushButton#data_list_pgn_next_button {{ background-color: {color_scheme.hex_light_button}; border: 0px; border-radius: 3px; color: #222; padding: 3px }}
            QPushButton#data_list_pgn_prev_button:hover, QPushButton#data_list_pgn_next_button:hover {{ background-color: {color_scheme.hex_light_button_hover} }}
        """

        text_filter_icon_path = os.path.abspath('src/icons/content_panel/text_filter.png')

        drop_all_qty_icon = os.path.abspath('src/icons/content_panel/drop_all_qty.png')
        drop_qty_icon = os.path.abspath('src/icons/content_panel/drop_qty.png')
        add_qty_icon = os.path.abspath('src/icons/content_panel/add_qty.png')
        edit_qty_icon = os.path.abspath('src/icons/content_panel/edit_qty.png')

        atc_icon_path = os.path.abspath('src/icons/content_panel/atc.png')
        view_icon_path = os.path.abspath('src/icons/content_panel/view.png')

        sync_icon_path = os.path.abspath('src/icons/content_panel/sync.png')
        toggle_retail_txn_icon_path = os.path.abspath('src/icons/content_panel/toggle_retail_txn.png')
        toggle_wholesale_txn_icon_path = os.path.abspath('src/icons/content_panel/toggle_wholesale_txn.png')
        toggle_aatc_icon_path = os.path.abspath('src/icons/content_panel/toggle_aatc.png')
        untoggle_aatc_icon_path = os.path.abspath('src/icons/content_panel/untoggle_aatc.png')

        prev_icon_path = os.path.abspath('src/icons/content_panel/prev.png')
        next_icon_path = os.path.abspath('src/icons/content_panel/next.png')

        add_icon_path = os.path.abspath('src/icons/content_panel/add_cart_tab.png')

        if object_name == 'text_filter_button':
            self.setIcon(QIcon(text_filter_icon_path))
            self.setIconSize(QSize(15,20))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass

        if object_name == 'cart_list_drop_all_qty_button':
            self.setIcon(QIcon(drop_all_qty_icon))
            self.setFixedSize(20,20)
            self.setIconSize(QSize(12,15))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass
        if object_name == 'cart_list_drop_qty_button':
            self.setIcon(QIcon(drop_qty_icon))
            self.setFixedSize(20,20)
            self.setIconSize(QSize(12,15))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass
        if object_name == 'cart_list_add_qty_button':
            self.setIcon(QIcon(add_qty_icon))
            self.setFixedSize(20,20)
            self.setIconSize(QSize(12,15))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass
        if object_name == 'cart_list_edit_qty_button':
            self.setIcon(QIcon(edit_qty_icon))
            self.setFixedSize(20,20)
            self.setIconSize(QSize(12,15))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass

        if object_name == 'data_list_atc_button':
            self.setIcon(QIcon(atc_icon_path))
            self.setIconSize(QSize(15,20))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass
        if object_name == 'data_list_view_button':
            self.setIcon(QIcon(view_icon_path))
            self.setIconSize(QSize(15,20))
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            pass

        if object_name == 'add_cart_tab_button':
            self.setIcon(QIcon(add_icon_path))
            self.setIconSize(QSize(15,20))
            pass
        
        if object_name == 'sales_mgt_discard_button':
            self.setFixedWidth(100)
        if object_name == 'sales_mgt_pay_button':
            layout = MyHBoxLayout()
            layout.setContentsMargins(15,15,15,15)
            pay_label = QLabel('PAY')
            pay_label.setStyleSheet('font-size: 25px')
            layout.addWidget(pay_label)
            self.setLayout(layout)
            
            
        if object_name == 'payment_back_button':
            self.setFixedWidth(100)

        if object_name == 'data_mgt_sync_button':
            self.setIcon(QIcon(sync_icon_path))
            self.setIconSize(QSize(15,20))
        if object_name == 'data_mgt_toggle_retail_txn_button':
            self.setIcon(QIcon(toggle_retail_txn_icon_path))
            self.setIconSize(QSize(15,20))
            pass
        if object_name == 'data_mgt_toggle_wholesale_txn_button':
            self.setIcon(QIcon(toggle_wholesale_txn_icon_path))
            self.setIconSize(QSize(15,20))
            pass
        if object_name == 'data_mgt_toggle_aatc_button':
            self.setIcon(QIcon(toggle_aatc_icon_path))
            self.setIconSize(QSize(15,20))
            pass
        if object_name == 'data_mgt_untoggle_aatc_button':
            self.setIcon(QIcon(untoggle_aatc_icon_path))
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

        self.setEditable(True)
        pass
class MyLineEdit(QLineEdit):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)

        if object_name == 'text_filter_field':
            self.setMinimumWidth(400)
            self.setPlaceholderText('Filter product')

        if object_name == 'data_mgt_scanned_barcode_field':
            self.setMaximumWidth(350)
            self.setPlaceholderText('Scan barcode')
        pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name=''):
        super().__init__()
        
        self.setObjectName(object_name)
        pass

class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.setText(text)
        self.setToolTip(text)
