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

from schema.promo_management_schema import *

class CustomDialog(QDialog):
    def __init__(self, ref='', parent=None, row_value=''):
        super().__init__()

        self.setFixedWidth(400)
        self.setStyleSheet("QDialog { background-color: #fff; } ")
        self.setParent(parent)
        self.setWindowFlag(Qt.WindowType.Dialog)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        if ref == 'view_data_dialog':
            self.setWindowTitle(row_value[0])

            self.dialog_layout = CustomFormLayout()
            self.dialog_layout.setContentsMargins(20,20,20,20)

            print('sample: ', row_value[0])
            # region: display data
            self.promo_name_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[0]}</font>")
            self.promo_type_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[1]}</font>")
            self.discount_percent_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[2]}</font>")
            self.description_data = CustomLabel(ref='', text=f"<font size='2'>{row_value[3]}</font>")
            # endregion: display data
            # region: add display data as rows
            self.dialog_layout.addRow("<font size='2'>Promo name: </font>", self.promo_name_data)
            self.dialog_layout.addRow("<font size='2'>Promo type: </font>", self.promo_type_data)
            self.dialog_layout.addRow("<font size='2'>Discount percent: </font>", self.discount_percent_data)
            self.dialog_layout.addRow("<font size='2'>Description: </font>", self.description_data)
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
            self.promo_management_schema = PromoManagementSchema()
            # Load the CSV file into a Pandas DataFrame
            data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

            self.total_rows = len(data_frame) 
            progress_min_range = 1

            for row in data_frame.itertuples(index=False):
                self.promo_name, promo_type, discount_percent, description = row[:4]

                description = '[no data]' if description == '' else description

                if '' in (self.promo_name, promo_type, discount_percent):
                    QMessageBox.critical(self, 'Error', f'Unable to import due to missing values.')
                    return

                else:
                    # print('Inventory tracking: ', inventory_tracking)
                    self.promo_management_schema.add_new_promo(
                        promo_name=self.promo_name,
                        promo_type=promo_type,
                        discount_percent=discount_percent,
                        description=description
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
        self.progress_dialog.progress_text.setText(f"<td><font size='2'>{self.promo_name}</font></td>")

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
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
            # self.setFixedWidth(100) # checkpoint
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
            QTableWidget::item { border: 0px; border-bottom: 1px solid #ccc; padding: 0px 30px; }
        ''')
        
        if ref == 'overview_table':
            self.setColumnCount(6)
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.horizontalHeader().resizeSection(0, 150)
            self.setHorizontalHeaderLabels(['Action','Promo name','Promo type','Discount value','Description','Date created'])

class CustomTableWidgetItem(QTableWidgetItem):
    def __init__(self, ref='', text=''):
        super().__init__()

        self.setText(text)
        if ref == 'discount_value':
            self.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        if ref == 'update_ts':
            self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
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
        if ref == 'delete_all_button':
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
            self.setPlaceholderText('Search promo (i.e. by promo name, promo type, discount percent, or description)')
            self.setStyleSheet('QLineEdit { padding: 5px 5px }')

        pass

class CustomTextEdit(QTextEdit):
    def __init__(self, ref='', placeholderText=''):
        super().__init__()

class CustomComboBox(QComboBox):
    def __init__(self, ref='', editable=False, disabled=False):
        super().__init__()

        if ref == 'promo_type_field':
            self.setEditable(True)
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