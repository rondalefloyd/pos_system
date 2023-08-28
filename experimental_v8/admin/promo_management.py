import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.promo_management_sql import *

class GlobalWidget():
    def customLabel(self, text):
        label = QLabel(text)
        return label
    def customLineEdit(self, manage_promo_mode, ref):
        line_edit = QLineEdit()
        return line_edit
    def customTextEdit(self, manage_promo_mode, ref):
        text_edit = QTextEdit()
        return text_edit
    def customComboBox(self, manage_promo_mode, ref):
        combo_box = QComboBox()
        if ref == 'promo' or ref == 'promo_type':
            combo_box.setEditable(True)
        return combo_box
    def customDateEdit(self, manage_promo_mode, ref):
        date_edit = QDateEdit()
        date_edit.setMinimumDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        return date_edit
    def customPushButton(self, text):
        push_button = QPushButton(text)
        return push_button

class ManagePromoDialog(QDialog):
    def __init__(self, manage_promo_mode):
        super().__init__()

        self.callClass()
        self.setMainLayout(manage_promo_mode)
        self.setWidgetSignal(manage_promo_mode)
        self.setDefaultAttributes()
    
    def callClass(self):
        self.global_widget = GlobalWidget()
        self.promo_management_sql = PromoManagementSQL()

    def onSavePromoButton(self, manage_promo_mode):
        # convert input
        converted_promo = str(self.promo.currentText())
        converted_promo_type = str(self.promo_type.currentText())
        converted_promo_type_value = str(self.promo_type_value.text())
        converted_description = str(self.description.toPlainText())
        # converted_promo_start_dt = self.start_dt.date().toString(Qt.DateFormat.ISODate) # -- same with effective dt
        # converted_promo_end_dt = self.end_dt.date().toString(Qt.DateFormat.ISODate) # -- same with effective dt

        # step a
        self.promo_management_sql.insertPromoData(converted_promo, converted_promo_type, converted_promo_type_value, converted_description)
        pass

    def fillAllItemDataComboBox(self):
        promo = self.promo_management_sql.selectPromoData()
        promo_type = self.promo_management_sql.selectPromoTypeData()

        self.promo.addItems([row for row in promo])
        self.promo_type.addItems([row for row in promo_type])

    def setDefaultAttributes(self):
        self.promo_management_sql.createPromoTable()

        self.fillAllItemDataComboBox()

    def setWidgetSignal(self, manage_promo_mode):
        self.save_promo_button.clicked.connect(lambda: self.onSavePromoButton(manage_promo_mode))
    
    def setMainLayout(self, manage_promo_mode):
        self.main_layout = QFormLayout()

        self.promo = self.global_widget.customComboBox(manage_promo_mode, ref='promo')
        self.promo_type = self.global_widget.customComboBox(manage_promo_mode, ref='promo_type')
        self.promo_type_value = self.global_widget.customLineEdit(manage_promo_mode, ref='promo_type_value')
        self.description = self.global_widget.customTextEdit(manage_promo_mode, ref='description')
        # self.start_dt = self.global_widget.customDateEdit(manage_promo_mode, ref='start_dt')
        # self.end_dt = self.global_widget.customDateEdit(manage_promo_mode, ref='end_dt')

        self.save_promo_button = self.global_widget.customPushButton('SAVE')

        # add widget
        self.main_layout.addRow('promo: ', self.promo)
        self.main_layout.addRow('promo_type: ', self.promo_type)
        self.main_layout.addRow('promo_type_value (%): ', self.promo_type_value)
        self.main_layout.addRow('description: ', self.description)
        # self.main_layout.addRow('start_dt: ', self.start_dt)
        # self.main_layout.addRow('end_dt: ', self.end_dt)

        self.main_layout.addRow(self.save_promo_button)

        self.setLayout(self.main_layout)

class ListPromoTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setMainLayout()
    
    def setMainLayout(self):
        pass

class PromoManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setMainLayout()

    def onClickedAddPromoButton(self, manage_promo_mode):
        self.manage_item_dialog = ManagePromoDialog(manage_promo_mode)
        self.manage_item_dialog.exec()

    def setWidgetSignal(self):
        self.add_promo_button.clicked.connect(lambda: self.onClickedAddPromoButton('add_promo'))

    def setMainLayout(self):
        self.main_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.add_promo_button = QPushButton('ADD')
        self.list_promo_table = ListPromoTable()

        self.setWidgetSignal()

        self.main_layout.addWidget(self.filter_bar)
        self.main_layout.addWidget(self.add_promo_button)
        self.main_layout.addWidget(self.list_promo_table)

        self.setLayout(self.main_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
