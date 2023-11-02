import os, sys
import subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyStackedWidget(QStackedWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        
        self.setCurrentIndex(0)
        pass
class MyScrollArea(QScrollArea):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.setWidgetResizable(True)
        self.setObjectName(object_name)

        self.on_glboal_scra()

    def on_glboal_scra(self):
        self.setStyleSheet(f"""
            QScrollArea {{ border: none;}}
            QScrollArea#navbar_scra {{ background-color: {qss.navbar_bg_color};}}
        """)

        if self.object_name == 'navbar_scra':
            self.setFixedWidth(150)
            
        if self.object_name == 'manage_data_scra':
            self.setMinimumWidth(300)
    
    pass
class MyTabWidget(QTabWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        self.setObjectName(object_name)
        self.setFont(QFont(qss.global_font))

    def on_global_tab_widget(self):
        self.setStyleSheet(f"""
            QTabBar::tab {{ padding: 5px }}
        """)
        pass

class MyWidget(QWidget):
    close_signal = pyqtSignal(str)
    def __init__(self, object_name='', parent=None, window_title=''):
        super().__init__()

        self.object_name = object_name
        self.close_signal_value = ''

        self.setObjectName(object_name)
        self.setWindowTitle(window_title)
        self.setWindowIcon(QIcon(qss.app_icon))
        self.setFont(QFont(qss.global_font))

        self.on_global_widget()
        
        self.close_signal.connect(self.on_close_signal)

    def on_global_widget(self):
        if self.object_name == 'MyPOSView':
            self.setStyleSheet(f"""
                QWidget#MyPOSView {{ background-color: {qss.secondary_color} }}
            """)

    def on_close_signal(self, text):
        self.close_signal_value = text
        
    def closeEvent(self, event: QKeyEvent):
        print('CLOSE SIGNAL:', self.close_signal_value)
        if self.object_name in [
            'MyCashierView',
            'MyAdminView',
        ]:
            if self.close_signal_value == 'logout':
                event.accept()
                pass
            else:
                confirm = QMessageBox.warning(self, 'Confirm', 'Are you sure you want to close this application?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if confirm == QMessageBox.StandardButton.Yes:
                    os.remove('app_running.flag')
                else:
                    event.ignore()
                    pass
            
        
        pass
class MyGroupBox(QGroupBox):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.on_global_group_box()

        self.on_pos_group_box()

    def on_global_group_box(self):
        self.setStyleSheet(f"""
            QGroupBox {{ border: none }}
            QGroupBox#navbar_box {{ background-color: {qss.navbar_bg_color};}}
            QGroupBox#extra_info_box {{ background-color: {qss.main_color}; }}
            QGroupBox#extra_info_box > QLabel {{ color: {qss.main_txt_color}; }}

            QGroupBox#MyPOSView {{ background-color: {qss.secondary_color}}}

            QGroupBox#product_cell_display_box {{ background-color: #eee; border: 1px solid #eee; border-radius: 3px; margin: 10px; padding: 5px }}

            QGroupBox#manage_order_box {{ background-color: {qss.main_color} }}

            QGroupBox#manage_data_act_box,
            QGroupBox#payment_c_box,
            QGroupBox#view_data_act_box,
            QGroupBox#transaction_complete_act_b_box {{ background-color: {qss.default_panel_color}; border-top: 1px solid {qss.default_hr_color} }}

            QGroupBox#txn_complete_summary_box {{ padding: 20px }}
        """)

        if self.object_name in [
            'product_overview_act_box',
            'product_stock_overview_act_box',
            'promo_overview_act_box',
            'reward_overview_act_box',
            'customer_overview_act_box',
            'user_overview_act_box',

            'transaction_overview_act_box',
        ]:
            self.setStyleSheet(f"""
                QGroupBox#{self.object_name} {{ border: none; }}
            """)

        if self.object_name == [
            'pay_order_b_box',
            'transaction_complete_act_b_box'
        ]:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def on_cashier_group_box(self):
        pass

    def on_pos_group_box(self):
        if self.object_name == 'MyPOSView':
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            pass
        if self.object_name == 'product_cell_display_box':
            pass

        if self.object_name == 'manage_order_box':
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.setMaximumWidth(450)
        pass
class MyDialog(QDialog):
    close_signal = pyqtSignal(str)
    def __init__(self, object_name='', parent=None, window_title=''):
        super().__init__()

        self.object_name = object_name
        self.close_signal_value = ''
        
        self.setObjectName(object_name)
        self.setWindowTitle(window_title)
        self.setWindowIcon(QIcon(qss.app_icon))
        self.setFont(QFont(qss.global_font))

        self.on_global_dialog()

        self.on_login_dialog()

        self.on_pos_dialog()
        self.on_transaction_dialog()

        self.close_signal.connect(self.on_close_signal)

    def on_login_dialog(self):
        pass

    def on_global_dialog(self):
        if self.object_name == 'updater_progress_dialog':
            self.setMinimumWidth(250)

        if self.object_name == 'progress_dialog':
            self.setMinimumWidth(200)
        pass

    def on_pos_dialog(self):
        if self.object_name == 'pay_order_dialog':
            self.setMinimumWidth(800)

        if self.object_name == 'transaction_complete_dialog':
            self.setMinimumWidth(500)

        pass
    def on_transaction_dialog(self):
        if self.object_name == 'manage_data_dialog':
            self.setMinimumWidth(300)

    def on_close_signal(self, text):
        self.close_signal_value = text

    def closeEvent(self, event: QKeyEvent):
        print('CLOSE SIGNAL:', self.close_signal_value)
        if self.object_name == 'MyLoginView':
            os.remove('login_running.flag')
            os.remove('app_running.flag')

        elif self.object_name in [
            'updater_progress_dialog',
            'progress_dialog'
        ]:
            if self.close_signal_value == 'finished':
                event.accept()
            else:
                confirm = QMessageBox.question(self, 'Confirm', 'Do you want to cancel this update and proceed?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if confirm == QMessageBox.StandardButton.Yes:
                    event.accept()
                else:
                    event.ignore()
                    pass
                
            pass

class MyTableWidget(QTableWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        self.setObjectName(object_name)
        self.setFont(QFont(qss.global_font))
        self.horizontalHeader().setFont(QFont(qss.global_font))
        self.verticalHeader().setFont(QFont(qss.global_font))

        self.on_global_table()

        self.on_login_table()

        self.on_promo_table()
        self.on_user_table()
        self.on_reward_table()
        self.on_customer_table()
        self.on_product_table()

        self.on_pos_table()
        self.on_transaction_table()
        pass
    
    def on_global_table(self):
        if self.object_name in [
            'product_overview_table',
            'product_stock_table',
            'promo_overview_table',
            'reward_overview_table',
            'customer_overview_table',
            'user_overview_table',
            
            'order_table',
            'final_order_table',

            'item_sold_overview_table',
        ]:
            self.setShowGrid(False)
            self.setWordWrap(True)
            self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.verticalHeader().setDefaultSectionSize(50)
            self.verticalHeader().setSectionsClickable(False)
            self.horizontalHeader().setSectionsClickable(False)
            self.setStyleSheet(f"""
                QTableWidget#{self.object_name} {{ border: none; border-bottom: 1px solid #ddd}}
                QTableWidget#{self.object_name}::item {{ border-bottom: 1px solid #ddd; }}
                QTableWidget#{self.object_name}::item:selected {{ background-color: #eee; }}
            """)

    def on_login_table(self):
        if self.object_name == 'reg_user_table':
            self.setColumnCount(4)
            self.setHorizontalHeaderLabels(['Name','Password','Level','Phone'])

    def on_promo_table(self):
        if self.object_name == 'promo_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Type','Percent','Description','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
            pass
    def on_user_table(self):
        if self.object_name == 'user_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Password','Access level','Phone','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
            pass
    def on_reward_table(self):
        if self.object_name == 'reward_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Unit','Points','Description','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
            pass 
    def on_customer_table(self):
        if self.object_name == 'customer_overview_table':
            self.setColumnCount(11)
            self.setHorizontalHeaderLabels(['Action','Name','Address','Barrio','Town','Phone','Age','Gender','Marital status','Points','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeMode.ResizeToContents)
    def on_product_table(self):
        if self.object_name == 'product_overview_table':
            self.setColumnCount(15)
            self.setHorizontalHeaderLabels(['Action','Barcode','Product','Expire date','Type','Brand','Sales group','Supplier','Cost','Price','Effective date','Promo','Discount value','Inventory tracking','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(12, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(13, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(14, QHeaderView.ResizeMode.ResizeToContents)
            pass
        if self.object_name == 'product_stock_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Barcode','Product','Available','On hand','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

    def on_pos_table(self):
        if self.object_name == 'pos_overview_table':
            self.setShowGrid(False)
            self.setWordWrap(False)
            self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setHidden(True)
            self.verticalHeader().setHidden(True)
            self.setStyleSheet(f"""
                QTableWidget#{self.object_name} {{ border: none; }}
            """)

            pass
        if self.object_name == 'order_table':
            self.setColumnCount(5)
            self.verticalHeader().setDefaultSectionSize(40)
            self.setHorizontalHeaderLabels(['Action','Qty','Product','Amount','Discount'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            pass
        if self.object_name == 'final_order_table':
            self.setColumnCount(4)
            self.verticalHeader().setDefaultSectionSize(40)
            self.setHorizontalHeaderLabels(['Qty','Product','Amount','Discount'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            pass
    def on_transaction_table(self):
        if self.object_name == 'item_sold_overview_table':
            self.setColumnCount(10)
            self.setHorizontalHeaderLabels(['Acion','Cashier','Customer','Product','Quantity','Total amount','Void','Reason','ReferenceNumber','Date/Time created'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        self.setObjectName(object_name)
        self.on_global_vbox_layout()

    def on_global_vbox_layout(self):
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

        if self.object_name == 'progress_layout':
            self.setContentsMargins(10,10,10,10)
            self.setSpacing(5)

        if self.object_name == 'login_layout':
            
            self.setContentsMargins(20,20,20,20)
            self.setSpacing(5)

        if self.object_name == 'product_info_layout':
            self.setContentsMargins(10,10,10,10)

        if self.object_name == 'order_act_b_layout':
            self.setSpacing(5)
            self.setContentsMargins(10,10,10,10)
        
        if self.object_name == 'transaction_complete_act_a_layout': self.setSpacing(5)

        if self.object_name == 'sub_field_layout': self.setSpacing(5)
        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        self.setObjectName(object_name)

        self.on_global_hbox_layout()
        self.on_pos_hbox_layout()
        
    def on_global_hbox_layout(self):
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

        if self.object_name in [
            'filter_layout',
            'barcode_scanner_layout',
            'manage_data_layout',
        ]:
            self.setSpacing(5)
            
        if self.object_name == 'overview_act_layout':
            self.setContentsMargins(15,15,15,15)
            self.setSpacing(20)
            
        if self.object_name in [
            'product_act_layout',
            'promo_act_layout',
            'reward_act_layout',
            'customer_act_layout',
            'user_act_layout',

            'pos_act_layout',
            'item_sold_act_layout',
            
            'manage_order_act_layout',
            'order_act_a_layout',

            'payment_act_layout',
            'transaction_complete_act_b_layout',
            'manage_data_act_layout',
            'view_data_act_layout',
        ]:
            self.setContentsMargins(10,10,10,10)
            self.setSpacing(5)

        if self.object_name in [
            'promo_overview_act_layout',
            'user_overview_act_layout',
            'reward_overview_act_layout',
            'customer_overview_act_layout',
            'product_overview_act_layout',
            'product_stock_act_layout',

            'item_sold_overview_act_layout',            
        ]:
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setContentsMargins(20,0,20,0)
            self.setSpacing(5)

        if self.object_name == 'extra_info_layout':
            self.setContentsMargins(10,0,10,0)
            self.setSpacing(20)

        if self.object_name == 'order_table_act_layout':
            self.setContentsMargins(5,0,5,0)
            self.setSpacing(5)

        if self.object_name == 'final_customer_info_layout':
            self.setSpacing(20)

        if self.object_name in [
            'manage_receipt_layout',
            'product_name_layout'
        ]:
            self.setSpacing(5)

    def on_pos_hbox_layout(self):
        if self.object_name == 'product_cell_display_act_layout':
            self.setContentsMargins(5,5,5,5)
            self.setSpacing(5)

        if self.object_name in [
            'extra_order_act_b_layout',
            'product_status_indicator_layout', 
        ]:
            self.setSpacing(5)
        pass

class MyGridLayout(QGridLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_global_hbox_layout()
        

    def on_global_hbox_layout(self):
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

        if self.object_name == 'payment_b_layout':
            self.setContentsMargins(10,10,10,10)
            self.setSpacing(5)
        if self.object_name == 'numpad_key_layout':
            self.setSpacing(3)

        if self.object_name == 'field_layout':
            self.setContentsMargins(10,10,10,10)
            self.setSpacing(10)
        if self.object_name == 'sub_field_layout':
            self.setSpacing(5)




        pass
class MyFormLayout(QFormLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        self.setObjectName(object_name)

        self.on_global_hbox_layout()
        
    def on_global_hbox_layout(self):
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

        if self.object_name in [
            'order_summary_layout',
            'final_order_summary_layout',
        ]:
            self.setContentsMargins(15,15,15,15)
            self.setSpacing(10)

        if self.object_name == 'payment_amount_compute_layout':
            self.setContentsMargins(0,15,0,0)
            self.setSpacing(10)
            
        if self.object_name in ['field_layout','info_layout']:
            self.setContentsMargins(10,10,10,10)
            self.setSpacing(5)

        pass

class MyLabel(QLabel):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)
        self.setFont(QFont(qss.global_font))

        self.on_global_label()

        self.on_customer_label()
        
        self.on_pos_label()

    def on_global_label(self):
        self.setStyleSheet(f"""
            QLabel#tender_amount_label {{ font-size: 14px }}
        """)
        pass

    def on_customer_label(self):
        if self.object_name in ['customer_points_label', 'customer_points_display']:
            self.hide()
        pass

    def on_pos_label(self):
        self.setStyleSheet(f"""
            QLabel#order_index_label {{ color: #fff; font-size: 15px; font-weight: bold; }}
        """)
        if self.object_name == 'order_type_display': 
            self.setStyleSheet(f"QLabel#{self.object_name} {{ font-size: 14px; font-weight: bold; padding: 0px 10px 0px 0px;}}")

        if self.object_name == 'product_name_label':
            self.setStyleSheet(f"QLabel#{self.object_name} {{ font-size: 15px; font-weight: bold;}}")
            self.setWordWrap(True)
            pass
        if self.object_name == 'product_barcode_label':
            pass
        if self.object_name == 'product_brand_label':
            self.setStyleSheet(f"QLabel#{self.object_name} {{ font-size: 13px; font-weight: bold; }}")
            pass
        if self.object_name == 'product_price_label':
            self.setStyleSheet(f"QLabel#{self.object_name} {{ color: {qss.main_color}; font-weight: bold; font-size: 15px; }}")
            pass
        if self.object_name == 'product_disc_value_label':
            pass
        if self.object_name == 'product_effective_dt_label':
            pass
        if self.object_name == 'product_onhand_label':
            pass

        if self.object_name in [
            'order_subtotal_display',
            'order_discount_display',
            'order_tax_display',
            'order_total_display',

            'final_order_subtotal_display',
            'final_order_discount_display',
            'final_order_tax_display',
            'final_order_total_display',

            'cash_payment_compute_label',
            'points_payment_compute_label',
            'cash_points_payment_compute_label',
        ]:
            self.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.setStyleSheet(f"""
                QLabel#{self.object_name} {{ font-size: 14px }}
            """)


            if self.object_name in [
                'order_total_display',
                'final_order_total_display',
            ]:
                self.setStyleSheet(f"""
                    QLabel#{self.object_name} {{ font-weight: bold; font-size: 18px }}
                """)

        if self.object_name in [
            'transaction_payment_amount_display',
            'transaction_order_total_amount_display',
            'transaction_order_change_display',
        ]:
            self.setStyleSheet(f"""
                QLabel#{self.object_name} {{ font-size: 25px; font-weight: bold; }}
                QLabel#transaction_order_change_display {{ font-size: 35px; color: green }}
            """)
            self.setContentsMargins(0,0,0,20)
    pass
class MyComboBox(QComboBox):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_global_combo_box()

    def on_global_combo_box(self):
        self.setStyleSheet(f"""
            QComboBox {{ padding: 5px }}
        """)
        if self.object_name in [
            'user_name_field', 
            'promo_type_field',
            'customer_barrio_field',
            'customer_town_field',
            'product_type_field',
            'product_brand_field',
            'product_supplier_field',   
            'customer_name_field',
            
        ]:
            self.setEditable(True)
        pass
class MyLineEdit(QLineEdit):
    def __init__(self, object_name='', text='', push_button = None):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)

        self.on_global_line_edit()

        self.on_promo_line_edit()

    def on_global_line_edit(self):
        self.setStyleSheet(f"""
            QLineEdit {{ padding: 5px }}
        """)
        if self.object_name == 'user_password_field':
            self.setEchoMode(QLineEdit.EchoMode.Password)
            pass
        if self.object_name == 'barcode_scan_field':
            self.hide()

        if self.object_name in [
            'product_promo_type_field',
            'product_promo_percent_field',
            'product_disc_value_field',
            'product_new_price_field',
        ]:
            self.setDisabled(True)

        if self.object_name in [
            'product_cost_field',
            'product_price_field',
            'product_disc_value_field',
            'product_new_price_field',

            'reward_unit_field',
            'reward_points_field',

            'customer_points_field',

            'tender_amount_field',
        ]:
            self.setText('0')
            self.setValidator(QRegularExpressionValidator(QRegularExpression(r'^\d{0,10}(\.\d{0,2})?$')))
            if self.object_name == 'tender_amount_field':
                self.setStyleSheet(f"""
                    QLineEdit#{self.object_name} {{ font-size: 17px; padding: 10px; }}
                """)
            
        if self.object_name == 'customer_age_field':
            self.setText('1')
            self.setMaxLength(3)

        if self.object_name == 'promo_percent_field':
            self.setText('0.0')
            self.setValidator(QRegularExpressionValidator(QRegularExpression(r'^\d{0,3}(\.\d{0,2})?$')))

        if self.object_name in [
            'customer_phone_field',
            'user_phone_field',
        ]:
            self.setText("09")
            self.setMaxLength(11) # always start with 0 not +63
            self.textChanged.connect(self.on_text_changed)

    def on_promo_line_edit(self):
        if self.object_name == 'filter_field':
            self.setMinimumWidth(200)
            pass
        if self.object_name == 'barcode_scan_field':
            self.setMinimumWidth(200)
    
    def on_customer_line_edit(self):
        if self.object_name == 'customer_points_field':
            self.hide()
    
    def on_text_changed(self):
        if self.object_name in [
            'customer_phone_field',
            'user_phone_field',
        ]:
            try:
                if len(self.text()) <= 2:
                    self.setText('09')
            except ValueError as e:
                self.setText('09')
        pass

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.object_name in [
            'product_cost_field',
            'product_price_field',
            'product_disc_value_field',
            'product_new_price_field',

            'reward_unit_field',
            'reward_points_field',

            'customer_points_field',

            'tender_amount_field',
        ]:
            self.selectAll()
    pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        self.setObjectName(object_name)
        self.on_transaction_plain_text_edit()

    def on_global_plain_text_edit(self):
        self.setStyleSheet(f"""
            QPlainTextEdit {{ padding: 5px }}
        """)

    def on_transaction_plain_text_edit(self):
        if self.object_name == 'other_reason_field':
            self.hide()
        pass
class MyDateEdit(QDateEdit):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        self.setObjectName(object_name)
        self.setCalendarPopup(True)
        self.setMinimumDate(QDate().currentDate())
        self.on_global_date_edit()

    def on_global_date_edit(self):
        self.setStyleSheet(f"""
            QDateEdit {{ padding: 5px }}
        """)
        pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text='', disabled=False):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)
        self.setFont(QFont(qss.global_font))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setDisabled(disabled)

        self.on_global_push_button()

        self.on_pos_push_button()

    def on_global_push_button(self):
        if self.object_name in [
            'untoggle_barcode_scanner',
            'untoggle_barcode_scanner',
            'untoggle_lock_order',
            'untoggle_numpad_key',
            'product_delete_data_button', # unavailable for now 
        ]:
            self.hide()

        if self.object_name in [
            'product_page_button',
            'promo_page_button',
            'reward_page_button',
            'customer_page_button',
            'user_page_button',
            'pos_page_button',
            'transaction_page_button',
            'logout_button',
        ]:
            self.setStyleSheet(f"""
                QPushButton#{self.object_name} {{ background-color: none; border: none; color: {qss.navbar_btn_txt_color}; font-size: 14px; text-align: left; padding: 10px }}
                QPushButton#{self.object_name}:hover {{ background-color: {qss.navbar_btn_bg_color_alt}; }}
                QPushButton#{self.object_name}:disabled {{ background-color: {qss.navbar_btn_bg_color_alt}; }} 
            """)
            if self.object_name == 'product_page_button': self.setIcon(QIcon(qss.nav_product_icon))
            if self.object_name == 'promo_page_button': self.setIcon(QIcon(qss.nav_promo_icon))
            if self.object_name == 'reward_page_button': self.setIcon(QIcon(qss.nav_reward_icon))
            if self.object_name == 'customer_page_button': self.setIcon(QIcon(qss.nav_customer_icon))
            if self.object_name == 'user_page_button': self.setIcon(QIcon(qss.nav_user_icon))

            if self.object_name == 'pos_page_button': self.setIcon(QIcon(qss.nav_pos_icon))
            if self.object_name == 'transaction_page_button': self.setIcon(QIcon(qss.nav_transaction_icon))

            if self.object_name == 'logout_button': self.setIcon(QIcon(qss.nav_logout_icon))
        pass

        if self.object_name in [
            'login_button',

            'filter_button',
            'add_data_button',
            'import_data_button',
            'toggle_barcode_scanner',
            'untoggle_barcode_scanner',

            'edit_data_button',     
            'view_data_button',
            'delete_data_button',
            'void_data_button',

            'overview_prev_button',
            'overview_next_button',

            'add_products_button',
            'add_order_button',

            'clear_order_table_button',

            'discard_order_button',
            'toggle_lock_order',
            'untoggle_lock_order',
            'complete_order_button',

            'toggle_numpad_key',
            'untoggle_numpad_key',

            'pay_cash_button',
            'pay_points_button',
            'pay_cash_points_button',

            'print_receipt_button',
            'save_receipt_button',

            'add_new_order_button',

            'save_button',
            'close_button'
        ]:
            self.setStyleSheet(f"""
                QPushButton#{self.object_name} {{ background-color: {qss.act_btn_bg_color}; border: none; border-radius: 3px; color: {qss.act_btn_txt_color}; text-align: center; padding: 5px }}
                QPushButton#{self.object_name}:hover {{ background-color: {qss.act_btn_bg_color_alt} }}
                QPushButton#{self.object_name}:disabled {{ background-color: {qss.disabled_bg_color}  }}

                QPushButton#login_button {{ background-color: {qss.main_color}; border: none; border-radius: 3px; color: {qss.main_txt_color}; text-align: center; padding: 10px }}
                QPushButton#login_button:hover {{ background-color: {qss.main_color_alt} }}

                QPushButton#filter_button,
                QPushButton#add_data_button,
                QPushButton#overview_prev_button,
                QPushButton#toggle_barcode_scanner,
                QPushButton#overview_next_button,
                QPushButton#toggle_numpad_key {{ background-color: {qss.main_color}; border: none; border-radius: 3px; color: {qss.main_txt_color}; text-align: center; padding: 5px }}
                
                QPushButton#filter_button:hover,
                QPushButton#add_data_button:hover,
                QPushButton#toggle_barcode_scanner:hover,
                QPushButton#overview_prev_button:hover,
                QPushButton#overview_next_button:hover,
                QPushButton#toggle_numpad_key:hover {{ background-color: {qss.main_color_alt}; }}
            

                QPushButton#overview_prev_button:disabled,
                QPushButton#overview_next_button:disabled {{ background-color: {qss.secondary_color_alt}; color: {qss.secondary_text_color} }}

                QPushButton#delete_data_button, 
                QPushButton#void_data_button,
                QPushButton#discard_order_button,
                QPushButton#clear_order_table_button {{ background-color: {qss.act_neg_bg_color}; border: none; border-radius: 3px; color: {qss.act_neg_txt_color}; text-align: center; padding: 5px }}
                QPushButton#delete_data_button:hover,
                QPushButton#void_data_button:hover,
                QPushButton#discard_order_button:hover,
                QPushButton#clear_order_table_button:hover {{ background-color: {qss.act_neg_bg_color_alt} }}

                QPushButton#add_products_button {{ background-color: {qss.act_pos_bg_color}; border: none; border-radius: 3px; color: {qss.act_pos_txt_color}; text-align: center; padding: 5px }}
                QPushButton#add_products_button:hover {{ background-color: {qss.act_pos_bg_color_alt} }}

                QPushButton#add_order_button {{ background-color: {qss.act_pas_bg_color}; border: none; border-radius: 3px; color: {qss.act_pas_txt_color}; text-align: center; padding: 5px }}
                QPushButton#add_order_button:hover {{ background-color: {qss.act_pas_bg_color_alt} }}

                QPushButton#untoggle_lock_order {{ background-color: {qss.main_color}; border: none; border-radius: 3px; color: {qss.act_pas_txt_color}; text-align: center; padding: 5px }}
                QPushButton#untoggle_lock_order:hover {{ background-color: {qss.main_color_alt} }}

                QPushButton#complete_order_button {{ background-color: {qss.act_pos_bg_color}; border: none; border-radius: 3px; color: {qss.act_pos_txt_color}; font-size: 14px; font-weight: bold; text-align: center; padding: 15px }}
                QPushButton#complete_order_button:hover {{ background-color: {qss.act_pos_bg_color_alt} }}

                QPushButton#pay_cash_button,
                QPushButton#pay_points_button,
                QPushButton#pay_cash_points_button {{ background-color: {qss.act_pos_bg_color}; border: none; border-radius: 3px; color: {qss.act_pos_txt_color}; }}
                QPushButton#pay_cash_button:hover,
                QPushButton#pay_points_button:hover,
                QPushButton#pay_cash_points_button:hover {{ background-color: {qss.act_pos_bg_color_alt};}}
                QPushButton#pay_cash_button:disabled,
                QPushButton#pay_points_button:disabled,
                QPushButton#pay_cash_points_button:disabled {{ background-color: {qss.disabled_bg_color} }}            

                QPushButton#save_receipt_button {{ background-color: {qss.act_pos_bg_color}; border: none; border-radius: 3px; color: {qss.act_pos_txt_color}; padding: 10px }}
                QPushButton#save_receipt_button:hover {{ background-color: {qss.act_pos_bg_color_alt};}}
                QPushButton#print_receipt_button {{ background-color: {qss.act_pos_bg_color}; border: none; border-radius: 3px; color: {qss.act_pos_txt_color}; padding: 10px }}
                QPushButton#print_receipt_button:hover {{ background-color: {qss.act_pos_bg_color_alt};}}

                QPushButton#add_new_order_button {{ background-color: {qss.main_color}; border: none; border-radius: 3px; color: {qss.main_txt_color}; padding: 10px }}
                QPushButton#add_new_order_button:hover {{ background-color: {qss.main_color_alt};}}

                QPushButton#save_button {{ background-color: {qss.act_pos_bg_color}; border: none; border-radius: 3px; color: {qss.act_pos_txt_color}; text-align: center; padding: 5px }}
                QPushButton#save_button:hover {{ background-color: {qss.act_pos_bg_color_alt};}}
                
            """)
            if self.object_name == 'filter_button': self.setIcon(QIcon(qss.filter_icon))
            if self.object_name == 'add_data_button': self.setIcon(QIcon(qss.add_data_icon))
            if self.object_name == 'import_data_button': self.setIcon(QIcon(qss.import_data_icon))

            if self.object_name == 'toggle_barcode_scanner': self.setIcon(QIcon(qss.untoggle_barcode_scanner_icon))
            if self.object_name == 'untoggle_barcode_scanner': self.setIcon(QIcon(qss.toggle_barcode_scanner_icon))

            if self.object_name == 'edit_data_button': self.setIcon(QIcon(qss.act_edit_icon))
            if self.object_name == 'view_data_button': self.setIcon(QIcon(qss.act_view_icon))
            if self.object_name == 'delete_data_button': self.setIcon(QIcon(qss.act_delete_icon))
            if self.object_name == 'void_data_button': self.setIcon(QIcon(qss.act_void_icon))

            if self.object_name == 'add_products_button': self.setIcon(QIcon(qss.add_products_icon))
            if self.object_name == 'add_order_button': self.setIcon(QIcon(qss.add_order_icon))

            if self.object_name == 'clear_order_table_button': self.setIcon(QIcon(qss.clear_table_icon))

            if self.object_name == 'discard_order_button': self.setIcon(QIcon(qss.act_void_icon))
            if self.object_name == 'toggle_lock_order': self.setIcon(QIcon(qss.unlocked_icon))
            if self.object_name == 'untoggle_lock_order': self.setIcon(QIcon(qss.locked_icon))
            if self.object_name == 'complete_order_button': 
                self.setIcon(QIcon(qss.pay_order_icon))
                self.setIconSize(QSize(25,25))
            
            if self.object_name == 'toggle_numpad_key': self.setIcon(QIcon(qss.toggle_numpad_icon))
            if self.object_name == 'untoggle_numpad_key': self.setIcon(QIcon(qss.untoggle_numpad_icon))

            if self.object_name == 'pay_cash_button': self.setIcon(QIcon(qss.pay_cash_icon))
            if self.object_name == 'pay_points_button': self.setIcon(QIcon(qss.pay_points_icon))

            if self.object_name == 'print_receipt_button': self.setIcon(QIcon(qss.print_receipt_icon))
            if self.object_name == 'add_new_order_button': self.setIcon(QIcon(qss.add_order_icon))

            if self.object_name in ['close_button','save_button']: self.setFixedWidth(80)

    def on_pos_push_button(self):
        if self.object_name in [
            "drop_all_qty_button",
            "drop_qty_button",
            "add_qty_button",
            "edit_qty_button",
        ]:
            self.setText(None)
            self.setFixedSize(QSize(25,25))
            self.setIconSize(QSize(15,15))
            self.setStyleSheet(f"""
                QPushButton#{self.object_name} {{ background-color: {qss.act_btn_bg_color}; border: none; border-radius: 3px; }}
                QPushButton#{self.object_name}:hover {{ background-color: {qss.act_btn_bg_color_alt};}}
                QPushButton#{self.object_name}:disabled {{ background-color: {qss.disabled_bg_color}  }}

                QPushButton#drop_all_qty_button {{ background-color: {qss.act_neg_bg_color}; border: none; border-radius: 3px; }}
                QPushButton#drop_all_qty_button:hover {{ background-color: {qss.act_neg_bg_color_alt};}}

                QPushButton#drop_qty_button {{ background-color: {qss.act_sm_neg_bg_color}; border: none; border-radius: 3px; }}
                QPushButton#drop_qty_button:hover {{ background-color: {qss.act_sm_neg_bg_color_alt};}}

                QPushButton#add_qty_button {{ background-color: {qss.act_pos_bg_color}; border: none; border-radius: 3px; }}
                QPushButton#add_qty_button:hover {{ background-color: {qss.act_pos_bg_color_alt};}}
            """)

        if self.object_name == "drop_all_qty_button":
            self.setIcon(QIcon(qss.drop_all_qty_icon))
            pass
        if self.object_name == "drop_qty_button":
            self.setIcon(QIcon(qss.drop_qty_icon))
            pass
        if self.object_name == "add_qty_button":
            self.setIcon(QIcon(qss.add_qty_icon))
            pass
        if self.object_name == "edit_qty_button":
            self.setIcon(QIcon(qss.edit_qty_icon))
            pass

        if self.object_name in [
            'pay_cash_button',
            'pay_points_button',
            'pay_cash_points_button',
        ]:
            self.setDisabled(True)
            self.setFixedWidth(100)

        if self.object_name == 'numpad_key_button':
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.setStyleSheet(f"""
                QPushButton#{self.object_name} {{ background-color: {qss.main_color}; border: none; border-radius: 3px; color: {qss.main_txt_color}; font-size: 13px; font-weight: bold; padding: 10px; }}
                QPushButton#{self.object_name}:hover {{ background-color: {qss.main_color_alt};}}
            """)

        if self.object_name in ['product_promo_indicator','out_of_stock_indicator']:
            self.hide()
            self.setStyleSheet(f"""
                QPushButton#{self.object_name} {{ background-color: none; border: none; }}
            """)
            self.setIconSize(QSize(20,20))
            self.setFixedSize(20,20)
            self.setCursor(Qt.CursorShape.ArrowCursor)
            if self.object_name == 'product_promo_indicator': self.setIcon(QIcon(qss.product_promo_indicator_icon))
            if self.object_name == 'out_of_stock_indicator': self.setIcon(QIcon(qss.out_of_stock_indicator_icon))

    pass
class MyCheckBox(QCheckBox):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)
        pass

class MyProgressBar(QProgressBar):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setTextVisible(False)
        self.setFixedHeight(20)

class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, text='', has_promo=False):
        super().__init__() 
        
        self.setText(text)
        self.has_promo = has_promo

        self.on_product_table_widget_item()

    def on_product_table_widget_item(self):
        if self.has_promo is True:
            self.setForeground(QColor(255,0,0))

