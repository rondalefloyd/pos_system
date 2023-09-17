import sqlite3
import sys, os
import pandas as pd
import threading
from datetime import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema.product_management_schema import *

class CustomProgressDialog(QProgressDialog):
    def __init__(self, ref='', parent=None, min=0, max=0):
        super().__init__()

        if ref == 'import_progress_dialog':
            self.progress_bar = CustomProgressBar()
            self.progress_text = CustomLabel(text='test')

            self.setParent(parent)
            self.setMinimum(min)
            self.setMaximum(max)
            self.setFixedSize(400, 60)
            self.setCancelButton(None)
            self.setBar(self.progress_bar)
            self.setWindowFlag(Qt.WindowType.Dialog)
            self.setWindowModality(Qt.WindowModality.ApplicationModal)

            self.dialog_layout = CustomGridLayout()
            self.dialog_layout.addWidget(self.progress_bar)
            self.dialog_layout.addWidget(self.progress_text)

            self.setLayout(self.dialog_layout)
        pass

class CustomProgressBar(QProgressBar):
    def __init__(self, ref=''):
        super().__init__()

        self.setFixedHeight(15)
        self.setTextVisible(False)

# under construction ...
class CustomThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file, progress_dialog, import_button):
        super().__init__()
        self.csv_file = csv_file
        self.progress_dialog = progress_dialog
        self.import_button = import_button

        self.csv_file_name = os.path.basename(self.csv_file)

    def run(self):
        try:
            self.product_management_schema = ProductManagementSchema()
            # Load the CSV file into a Pandas DataFrame
            data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

            self.total_rows = len(data_frame)
            progress_min_range = 1

            for row in data_frame.itertuples(index=False):
                barcode, self.item_name, expire_dt, item_type, brand, sales_group, supplier, cost, sell_price, available_stock = row[:10]
                effective_dt = date.today()
                inventory_tracking = 'Disabled'

                # set default value if empty string
                barcode = '<unknown>' if barcode == '' else barcode
                expire_dt = '9999-12-31' if expire_dt == '' else expire_dt
                item_type = '<unknown>' if item_type == '' else item_type

                if available_stock == '0' or available_stock == '' or available_stock == None:
                    inventory_tracking = 'Disabled'
                else: 
                    inventory_tracking = 'Enabled' 

                if '' in (self.item_name, brand, sales_group, supplier, cost, sell_price):
                    QMessageBox.critical(self, 'Error', f'Unable to import due to missing values.')
                    return

                else:
                    # print('Inventory tracking: ', inventory_tracking)
                    self.product_management_schema.add_new_product(
                        barcode=barcode,
                        item_name=self.item_name,
                        expire_dt=expire_dt,
                        item_type=item_type,
                        brand=brand,
                        sales_group=sales_group,
                        supplier=supplier,
                        cost=cost,
                        sell_price=sell_price,
                        effective_dt=effective_dt,
                        inventory_tracking=inventory_tracking,
                        available_stock=available_stock
                    )

                progress_min_range += 1
                self.progress_signal.emit(progress_min_range)

                if self.progress_dialog.wasCanceled():
                    return

            self.finished_signal.emit(f"All data from '{self.csv_file}' has been imported.")

        except Exception as error_message:
            self.error_signal.emit(f'Error importing data from {self.csv_file}: {str(error_message)}')
            print(error_message)

    def update_progress(self, progress):
        current_row = progress - 1
        percentage = int((current_row / self.total_rows) * 100) 

        self.progress_dialog.setWindowTitle(f"{percentage}% complete")
        self.progress_dialog.progress_bar.setValue(percentage)
        self.progress_dialog.progress_text.setText(f"<td><font size='2'>{self.item_name}</font></td>")

        # Check if the cancel button was pressed

    def import_finished(self):
        QMessageBox.information(None, 'Success', f'All product has been imported.')
        self.import_button.setDisabled(False)
        self.progress_dialog.close()

    def import_error(self):
        QMessageBox.critical(None, 'Error', 'An error has occurred during the process.')
        self.import_button.setDisabled(False)
        self.progress_dialog.close()

# under construction ...

class CustomGridLayout(QGridLayout):
    def __init__(self, ref=''):
        super().__init__()
        if ref in ['manage_data_layout','action_layout']:
            self.setSpacing(0)
            self.setContentsMargins(0,0,0,0)
        pass

class CustomFormLayout(QFormLayout):
    def __init__(self, ref=''):
        super().__init__()

class CustomWidget(QWidget):
    def __init__(self, ref=''):
        super().__init__()
        
        if ref == 'action_box':
            self.setFixedWidth(100)
            pass

class CustomGroupBox(QGroupBox):
    def __init__(self, ref=''):
        super().__init__()

        if ref == 'panel_b_box':
            self.setFixedWidth(300)
        pass

class CustomTabWidget(QTabWidget):
    def __init__(self, ref=''):
        super().__init__()
        pass

class CustomLabel(QLabel):
    def __init__(self, ref='', text=''):
        super().__init__()

        if ref in [
            'current_barcode',
            'current_item_name',
            'current_expire_dt',
            'current_item_type',
            'current_brand',
            'current_sales_group',
            'current_supplier',
            'current_cost',
            'current_sell_price',
            'current_effective_dt',
            'current_promo_name',
            'current_promo_type',
            'current_discount_percent',
            'current_discount_value',
            'current_new_sell_price',
            'current_inventory_tracking'
        ]:
            self.hide()

        self.setText(text)
        pass

class CustomTableWidget(QTableWidget):
    def __init__(self, ref=''):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setDefaultSectionSize(50)
        self.setStyleSheet('''
            QTableWidget { border: 0px; font-size: 10px; }
            QHeaderView::section { border: 0px; padding: 0px 40px; }
            QTableWidget::item { border: 0px; border-bottom: 1px solid #ccc; padding: 0px 10px; }
        ''')
        
        if ref == 'overview_table':
            self.setColumnCount(8)
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            self.setHorizontalHeaderLabels(['action','item_name','brand','sales_group','sell_price','promo','inventory_tracking','time_stamp'])

        elif ref == 'primary_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['bardcode','item_name','expire_dt','promo','time_stamp'])

        elif ref == 'category_table':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['item_name','item_type','brand','sales_group','supplier','promo','time_stamp'])

        elif ref == 'price_table':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['item_name','cost','sell_price','discount_value','effective_dt','promo','time_stamp'])

        elif ref == 'inventory_table':
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['item_name','inventory_tracking','available_stock','on_hand_stock','promo','time_stamp'])

class CustomTableWidgetItem(QTableWidgetItem):
    def __init__(self, ref='', text=''):
        super().__init__()

        self.setText(text)
        if ref in ['cost','sell_price','discount_value']:
            self.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            pass

class CustomPushButton(QPushButton):
    def __init__(self, ref='', text=''):
        super().__init__()

        self.setText(text)

        if ref == 'refresh_button':
            self.setIcon(CustomIcon(ref='refresh_icon'))
            
        if ref == 'delete_all_button':
            self.setIcon(CustomIcon(ref='delete_all_icon'))

        if ref == 'import_button':
            self.setIcon(CustomIcon(ref='import_icon'))

        if ref == 'add_button':
            self.setIcon(CustomIcon(ref='add_icon'))
        pass

class CustomLineEdit(QLineEdit):
    def __init__(self, ref='', placeholderText=''):
        super().__init__()

        if ref in [
            'current_barcode',
            'current_item_name',
            'current_expire_dt',
            'current_item_type',
            'current_brand',
            'current_sales_group',
            'current_supplier',
            'current_cost',
            'current_sell_price',
            'current_effective_dt',
            'current_promo_name',
            'current_promo_type',
            'current_discount_percent',
            'current_discount_value',
            'current_new_sell_price',
            'current_inventory_tracking'
        ]:
            self.hide()

        pass

class CustomComboBox(QComboBox):
    def __init__(self, ref='', editable=False, disabled=False):
        super().__init__()

        if ref in ['item_type', 'brand', 'supplier']:
            self.setEditable(True)

        elif ref == 'sales_group':
            self.addItem('Retail')
            self.addItem('Wholesale')
            pass
        elif ref == 'promo_name':
            self.addItem('No promo')
            pass
        elif ref == 'inventory_tracking':
            self.addItem('Enabled')
            self.addItem('Disabled')
            pass

        pass

class CustomDateEdit(QDateEdit):
    def __init__(self, ref=''):
        super().__init__()
        pass

class CustomIcon(QIcon):
    def __init__(self, ref=''):
        super().__init__()
        pass

        if ref == 'refresh_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/refresh.png')))

        if ref == 'delete_all_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/delete-all.png')))

        if ref == 'import_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/import.png')))

        if ref == 'add_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/add.png')))