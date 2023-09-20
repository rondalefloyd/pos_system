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

class CustomDialog(QDialog):
    def __init__(self, ref='', parent=None, row_value=''):
        super().__init__()

        self.setFixedWidth(400)
        self.setStyleSheet("QDialog { background-color: #fff; } ")
        self.setParent(parent)
        self.setWindowFlag(Qt.WindowType.Dialog)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        if ref == 'view_data_dialog':
            self.setWindowTitle(row_value[1])

            self.dialog_layout = CustomFormLayout()
            self.dialog_layout.setContentsMargins(20,20,20,20)

            print('sample: ', row_value[0])
            # region: display data
            self.barcode_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[0]}</font>")
            self.item_name_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[1]}</font>")
            self.expire_dt_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[2]}</font>")

            self.item_type_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[3]}</font>")
            self.brand_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[4]}</font>")
            self.sales_group_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[5]}</font>")
            self.supplier_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[6]}</font>")

            self.cost_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[7]}</font>")
            self.sell_price_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[8]}</font>")
            self.effective_dt_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[9]}</font>")
            self.promo_name_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[10]}</font>")
            self.discount_value_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[11]}</font>")

            self.inventory_tracking_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[12]}</font>")
            self.available_stock_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[13]}</font>")
            self.on_hand_stock_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[14]}</font>")
            self.date_added_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[15]}</font>")
            # endregion: display data
            # region: add display data as rows
            self.dialog_layout.addRow("<font size='2'>Barcode: </font>", self.barcode_data)
            self.dialog_layout.addRow("<font size='2'>Item name: </font>", self.item_name_data)
            self.dialog_layout.addRow("<font size='2'>Expire date: </font>", self.expire_dt_data)
            self.dialog_layout.addRow(CustomLabel(text='<hr>'))
            self.dialog_layout.addRow("<font size='2'>Item type: </font>", self.item_type_data)
            self.dialog_layout.addRow("<font size='2'>Brand: </font>", self.brand_data)
            self.dialog_layout.addRow("<font size='2'>Sales group: </font>", self.sales_group_data)
            self.dialog_layout.addRow("<font size='2'>Supplier: </font>", self.supplier_data)
            self.dialog_layout.addRow(CustomLabel(text='<hr>'))
            self.dialog_layout.addRow("<font size='2'>Cost: </font>", self.cost_data)
            self.dialog_layout.addRow("<font size='2'>Sell price: </font>", self.sell_price_data)
            self.dialog_layout.addRow("<font size='2'>Effective date: </font>", self.effective_dt_data)
            self.dialog_layout.addRow("<font size='2'>Promo name: </font>", self.promo_name_data)
            self.dialog_layout.addRow("<font size='2'>Discount value: </font>", self.discount_value_data)
            self.dialog_layout.addRow(CustomLabel(text='<hr>'))
            self.dialog_layout.addRow("<font size='2'>Inventory tracking: </font>", self.inventory_tracking_data)
            self.dialog_layout.addRow("<font size='2'>Available stock: </font>", self.available_stock_data)
            self.dialog_layout.addRow("<font size='2'>On hand stock: </font>", self.on_hand_stock_data)
            self.dialog_layout.addRow(CustomLabel(text='<hr>'))
            self.dialog_layout.addRow("<font size='2'>Date added: </font>", self.date_added_data)
            # endregion: add display data as rows

            self.setLayout(self.dialog_layout)

        self.exec()

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
            self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

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

class CustomThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file, import_button):
        super().__init__()
        self.csv_file = csv_file
        self.progress_dialog = CustomProgressDialog(ref='import_progress_dialog')
        self.import_button = import_button

        self.csv_file_name = os.path.basename(self.csv_file)

    def confirm(self):
        confirm = QMessageBox.warning(None, 'Confirm', 'Are you sure you want to cancel importing?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        pass

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
                barcode = '[no data]' if barcode == '' else barcode
                expire_dt = '9999-12-31' if expire_dt == '' else expire_dt
                item_type = '[no data]' if item_type == '' else item_type

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

                if self.progress_dialog.wasCanceled():
                    self.import_button.setDisabled(False)
                    return
                else:
                    pass

                progress_min_range += 1
                self.progress_signal.emit(progress_min_range)

            self.finished_signal.emit(f"All data from '{self.csv_file}' has been imported.")

        except Exception as error_message:
            self.error_signal.emit(f'Error importing data from {self.csv_file}: {str(error_message)}')
            print(error_message)

    def update_progress(self, progress):
        self.current_row = progress - 1
        percentage = int((self.current_row / self.total_rows) * 100) 

        print(self.current_row)


        self.progress_dialog.setWindowTitle(f"{percentage}% complete ({self.current_row} out of {self.total_rows})")
        self.progress_dialog.progress_bar.setValue(percentage)
        self.progress_dialog.progress_text.setText(f"<td><font size='2'>{self.item_name}</font></td>")

    def import_finished(self):
        QMessageBox.information(None, 'Success', f'All product has been imported.')
        self.import_button.setDisabled(False)
        self.progress_dialog.close()

    def import_error(self):
        QMessageBox.critical(None, 'Error', 'An error has occurred during the process.')
        self.import_button.setDisabled(False)
        self.progress_dialog.close()

class CustomHBoxLayout(QHBoxLayout):
    def __init__(self, ref=''):
        super().__init__()

        self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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

        if ref in [
            'overview_pagination',
            'primary_pagination',
            'category_pagination',
            'price_pagination',
            'inventory_pagination'
        ]:
            self.setFixedWidth(300)
            
        if ref == 'action_box':
            # self.setFixedWidth(150) # checkpoint
            pass

class CustomGroupBox(QGroupBox):
    def __init__(self, ref=''):
        super().__init__()

        if ref == 'panel_b_box':
            self.hide()
            self.setFixedWidth(400)
        pass

class CustomTabWidget(QTabWidget):
    def __init__(self, ref=''):
        super().__init__()

        if ref == 'tab_sort':
            self.setStyleSheet("""
                QTabBar::tab { height: 30px; width: 100px; }
            """)
        
        pass

class CustomLabel(QLabel):
    def __init__(self, ref='', text=''):
        super().__init__()

        if ref in [
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
            'on_hand_stock_label',
            'inactive_label'
        ]:
            self.setFixedWidth(150)

        if ref == 'inactive_label':
            self.hide()

        if ref in [
            'promo_type_label',
            'discount_percent_label',
            'discount_value_label',
            'new_sell_price_label',
            'start_dt_label',
            'end_dt_label',
            'available_stock_label',
            'on_hand_stock_label'
        ]:
            self.hide()

        self.setText(text)
        pass

class CustomTableWidget(QTableWidget):
    def __init__(self, ref=''):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setDefaultSectionSize(50)
        self.setStyleSheet('''
            QTableWidget { border: 0px; font-size: 10px; }
            QHeaderView::section { border: 0px; }
            QTableWidget::item { border: 0px; border-bottom: 1px solid #ccc; padding: 0px 10px; }
        ''')
        
        if ref == 'overview_table':
            self.setColumnCount(8)
            # checkpoint
            self.setHorizontalHeaderLabels(['Action','Item name','Brand','Sales group','Sell price','Promo','Inventory tracking','Date created'])
        elif ref == 'primary_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Bardcode','Item name','Expire date','Promo','Date created'])
        elif ref == 'category_table':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['Item name','Item type','Brand','Sales group','Supplier','Promo','Date created'])
        elif ref == 'price_table':
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['Item name','Cost','Sell price','Discount value','Effective date','Promo','Date created'])
        elif ref == 'inventory_table':
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Action','Item name','Available stock','On hand stock','Date created'])

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
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if ref in ['previous_button', 'next_button']:
            self.setFixedSize(30,30)

        if ref in ['edit_button', 'view_button', 'delete_button']:
            pass

        if ref == 'previous_button':
            self.setIcon(CustomIcon(ref='previous_icon'))
        if ref == 'next_button':
            self.setIcon(CustomIcon(ref='next_icon'))

        if ref == 'edit_button':
            self.setFixedSize(30,30)
            self.setIcon(CustomIcon(ref='edit_icon'))
            pass
        if ref == 'view_button':
            self.setFixedSize(30,30)
            self.setIcon(CustomIcon(ref='view_icon'))
            pass
        if ref == 'delete_button':
            self.setFixedSize(30,30)
            self.setIcon(CustomIcon(ref='delete_icon'))
            pass

        if ref == 'refresh_button':
            self.setFixedSize(30,30)
            self.setIcon(CustomIcon(ref='refresh_icon'))
            pass
        if ref == 'mass_delete_button':
            self.setFixedSize(30,30)
            self.setIcon(CustomIcon(ref='delete_all_icon'))
            pass
        if ref == 'import_button':
            self.setFixedSize(30,30)
            self.setIcon(CustomIcon(ref='import_icon'))
            pass
        if ref == 'add_button':
            self.setFixedSize(30,30)
            self.setIcon(CustomIcon(ref='add_icon'))
            pass
        pass

class CustomLineEdit(QLineEdit):
    def __init__(self, ref='', placeholderText=''):
        super().__init__()


        if ref == 'filter_field':
            self.setPlaceholderText('Search product (i.e. by barcode, item name, item type, brand, sales group, supplier, or inventory tracking)')
            self.setStyleSheet('QLineEdit { padding: 5px 5px }')

        if ref == 'inactive_field':
            self.setDisabled(True)
            self.hide()
        
        if ref in [
            'promo_type_field',
            'discount_percent_field',
            'discount_value_field',
            'new_sell_price_field',
            'available_stock_field',
            'on_hand_stock_field'
        ]:
            self.hide()
        pass

class CustomComboBox(QComboBox):
    def __init__(self, ref='', editable=False, disabled=False):
        super().__init__()

        if ref in ['item_type_field', 'brand_field', 'supplier_field']:
            self.setEditable(True)

        elif ref == 'sales_group_field':
            self.addItem('Retail')
            self.addItem('Wholesale')
            pass
        elif ref == 'promo_name_field':
            self.addItem('No promo')
            pass
        elif ref == 'inventory_tracking_field':
            self.addItem('Disabled')
            self.addItem('Enabled')
            pass

        pass

class CustomDateEdit(QDateEdit):
    def __init__(self, ref=''):
        super().__init__()

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

        if ref in ['start_dt_field', 'end_dt_field']:
            self.hide()
        pass

class CustomIcon(QIcon):
    def __init__(self, ref=''):
        super().__init__()
        pass

        if ref == 'previous_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/previous.png')))
        if ref == 'next_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/next.png')))
            

        if ref == 'edit_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/edit.png')))
        if ref == 'view_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/view.png')))
        if ref == 'delete_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/delete.png')))


        if ref == 'refresh_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/refresh.png')))
        if ref == 'delete_all_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/delete_all.png')))
        if ref == 'import_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/import.png')))
        if ref == 'add_icon':
            self.addFile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../icons/add.png')))