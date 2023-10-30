import os, sys
import subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(r'C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22')

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

        self.on_glboal_scra()

    def on_glboal_scra(self):
        if self.object_name == 'navbar_scra':
            self.setFixedWidth(150)
            
        if self.object_name == 'manage_data_scra':
            self.setMinimumWidth(300)
    
    pass
class MyTabWidget(QTabWidget):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name
        pass
class MyWidget(QWidget):
    close_signal = pyqtSignal(str)
    def __init__(self, object_name='', parent=None, window_title=''):
        super().__init__()

        self.object_name = object_name
        self.close_signal_value = ''

        self.setObjectName(object_name)
        self.setWindowTitle(window_title)

        self.close_signal.connect(self.on_close_signal)


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

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.on_pos_group_box()

    def on_cashier_group_box(self):
        pass

    def on_pos_group_box(self):
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

        self.on_login_table()

        self.on_promo_table()
        self.on_user_table()
        self.on_reward_table()
        self.on_customer_table()
        self.on_product_table()

        self.on_pos_table()
        self.on_transaction_table()
        pass

    def on_login_table(self):
        if self.object_name == 'reg_user_table':
            self.setColumnCount(4)
            self.setHorizontalHeaderLabels(['Name','Password','Level','Phone'])

    def on_promo_table(self):
        if self.object_name == 'promo_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Type','Percent','Description','Date/Time created'])
            pass
    def on_user_table(self):
        if self.object_name == 'user_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Password','Access level','Phone','Date/Time created'])
            pass
    def on_reward_table(self):
        if self.object_name == 'reward_overview_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Name','Unit','Points','Description','Date/Time created'])
            pass 
    def on_customer_table(self):
        if self.object_name == 'customer_overview_table':
            self.setColumnCount(11)
            self.setHorizontalHeaderLabels(['Action','Name','Address','Barrio','Town','Phone','Age','Gender','Marital status','Points','Date/Time created'])
    def on_product_table(self):
        if self.object_name == 'product_overview_table':
            self.setColumnCount(15)
            self.setHorizontalHeaderLabels(['Action','Barcode','Product','Expire date','Type','Brand','Sales group','Supplier','Cost','Price','Effective date','Promo','Discount value','Inventory tracking','Date/Time created'])
            pass
        if self.object_name == 'product_stock_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Action','Barcode','Product','Available','On hand','Date/Time created'])

    def on_pos_table(self):
        if self.object_name == 'pos_overview_table':
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            # self.horizontalHeader().setHidden(True)
            # self.verticalHeader().setHidden(True)
            pass
        if self.object_name == 'order_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Qty','Product','Amount','Discount'])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            pass
        if self.object_name == 'final_order_table':
            self.setColumnCount(4)
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

class MyVBoxLayout(QVBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_global_vbox_layout()

    def on_global_vbox_layout(self):
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        pass
class MyHBoxLayout(QHBoxLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_global_hbox_layout()
        

    def on_global_hbox_layout(self):
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

        if self.object_name in [
            'promo_overview_act_layout',
            'user_overview_act_layout',
            'reward_overview_act_layout',
            'customer_overview_act_layout',
            'product_overview_act_layout',
            'product_stock_act_layout',

            'order_table_act_layout',
            'item_sold_overview_act_layout',
        ]:
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pass
class MyGridLayout(QGridLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_global_hbox_layout()
        

    def on_global_hbox_layout(self):
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        pass
class MyFormLayout(QFormLayout):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_global_hbox_layout()
        

    def on_global_hbox_layout(self):
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        pass

class MyLabel(QLabel):
    def __init__(self, object_name='', text=''):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)

        self.on_global_label()

        self.on_customer_label()
        
        self.on_pos_label()

    def on_global_label(self):
        if self.object_name in [
            'progress_label', 
            'other_label_a'
        ]:
            self.setStyleSheet(f"""
                QLabel#progress_label,
                QLabel#other_label_a {{ font-size: 10px; }}
            """)

    def on_customer_label(self):
        if self.object_name == 'customer_points_label':
            self.hide()
        pass

    def on_pos_label(self):
        if self.object_name == 'product_name_label':
            self.setStyleSheet(f"QLabel#{self.object_name} {{ font-size: 15px; font-weight: bold; }}")
            pass
        if self.object_name == 'product_barcode_label':
            pass
        if self.object_name == 'product_brand_label':
            self.setStyleSheet(f"QLabel#{self.object_name} {{ font-size: 13px; font-weight: bold; }}")
            pass
        if self.object_name == 'product_price_label':
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
        if self.object_name in [
            'reg_user_name_field', # for login

            'user_name_field', 
            'promo_type_field',
            'customer_barrio_field',
            'customer_town_field',
            'product_type_field',
            'product_brand_field',
            'product_supplier_field',
            
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

    pass
class MyPlainTextEdit(QPlainTextEdit):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.on_transaction_plain_text_edit()

    def on_transaction_plain_text_edit(self):
        if self.object_name == 'other_reason_field':
            self.hide()
        pass
class MyDateEdit(QDateEdit):
    def __init__(self, object_name=''):
        super().__init__()

        self.object_name = object_name

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate().currentDate())
        pass
class MyPushButton(QPushButton):
    def __init__(self, object_name='', text='', disabled=False):
        super().__init__()

        self.object_name = object_name

        self.setObjectName(object_name)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setDisabled(disabled)

        self.on_global_push_button()

        self.on_pos_push_button()

    def on_global_push_button(self):
        if self.object_name in ['untoggle','product_promo_indicator','out_of_stock_indicator']:
            self.hide()
        pass
    
    def on_pos_push_button(self):
        if self.object_name in [
            "drop_all_qty_button",
            "drop_qty_button",
            "add_qty_button",
            "edit_qty_button",
        ]:
            self.setText(None)
            self.setIconSize(QSize(13,13))
            self.setFixedSize(QSize(25,25))
            self.setStyleSheet(f"""
                QPushButton#drop_all_qty_button {{ border: none; background-color: #cc2929; border-radius: 3px; }}
                QPushButton#drop_qty_button,
                QPushButton#add_qty_button,
                QPushButton#edit_qty_button {{ border: none; background-color: #dddddd; border-radius: 3px; }}
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

