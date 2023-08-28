import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.promo_management_sql import *

class CustomLineEdit(QLineEdit):
    def __init__(self, ref=None):
        super().__init__()
        
class CustomComboBox(QComboBox):
    def __init__(self, ref=None):
        super().__init__()

        self.setCurrentAttribute(ref)

    def setCurrentAttribute(self, ref=None):
        if ref == 'promo' or ref == 'promo_type':
            self.setEditable(True)

class CustomTextEdit(QTextEdit):
    def __init__(self, ref=None):
        super().__init__()

class CustomPushButton(QPushButton):
    def __init__(self, ref=None, text=None):
        super().__init__()

        self.setDefaultAttribute(text)

    def setDefaultAttribute(self, text=None):
        self.setText(text)
        
class CustomTableWidget(QTableWidget):
    def __init__(self, ref=None):
        super().__init__()

        self.callUtils()
        self.setDefaultAttribute()

    def callUtils(self):
        self.promo_management_sql = PromoManagementSQL()    
    
    def fillTable(self):
        promo = self.promo_management_sql.listPromo()

        self.setRowCount(50)

        for row_index, row_value in enumerate(promo):
            for col_index, col_value in enumerate(row_value):
                cell_data = QTableWidgetItem(str(col_value))
                self.setItem(row_index, col_index + 1, cell_data)

    def setDefaultAttribute(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['','promo_name','promo_type','discount_value','description'])

class CustomGroupBox(QGroupBox):
    data_saved = pyqtSignal()
    def __init__(self, ref=None):
        super().__init__()

        self.setMainLayout()
        self.callUtils()
        self.setWidgetSignal()
        self.setDefaultAttribute()

    def callUtils(self):
        self.promo_management_sql = PromoManagementSQL()

    def onSaveButton(self):
        # STEP A -- convert input
        converted_promo = str(self.promo.currentText())
        converted_promo_type = str(self.promo_type.currentText())
        converted_discount_value = str('{:.2f}'.format(float(self.discount_value.text())))
        converted_description = str(self.description.toPlainText())

        # STEP B
        self.promo_management_sql.addPromo(converted_promo, converted_promo_type, converted_discount_value, converted_description)

        self.data_saved.emit()
        QMessageBox.information(self, "Success", "New promo has been added!")
        # STEP C
        # STEP D -- OPTIONAL

    def setDefaultAttribute(self):
        self.setFixedWidth(400)

    def setWidgetSignal(self):
        self.save_button.clicked.connect(self.onSaveButton)

    def setMainLayout(self):
        self.main_layout = QFormLayout()
    
        self.promo = CustomComboBox('promo')
        self.promo_type = CustomComboBox('promo_type')
        self.discount_value = CustomLineEdit()
        self.description = CustomTextEdit()

        self.save_button = CustomPushButton(text='SAVE')

        self.setWidgetSignal()
        
        self.main_layout.addRow('promo_name: ', self.promo)
        self.main_layout.addRow('promo_type: ', self.promo_type)
        self.main_layout.addRow('discount_value: ', self.discount_value)
        self.main_layout.addRow('description: ', self.description)

        self.main_layout.addRow(self.save_button)

        self.setLayout(self.main_layout)

class PromoManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.callUtils()
        self.setMainLayout()
        self.setDefaultAttribute()

    def callUtils(self):
        self.promo_management_sql = PromoManagementSQL()

    def onClickedAddButton(self):
        self.manage_item_form.show()
        self.add_button.hide()
        self.close_button.show()
        self.manage_item_form.data_saved.connect(self.list_item_table.fillTable)
    
    def onClickedCloseButton(self):
        self.manage_item_form.hide()
        self.add_button.show()
        self.close_button.hide()

    def setWidgetSignal(self):
        self.add_button.clicked.connect(self.onClickedAddButton)
        self.close_button.clicked.connect(self.onClickedCloseButton)

    def setDefaultAttribute(self):
        self.manage_item_form.hide()
        self.close_button.hide()
        self.list_item_table.fillTable()

    def setMainLayout(self):
        self.promo_management_sql.createPromoTable()

        self.main_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.add_button = CustomPushButton(text='ADD')
        self.close_button = CustomPushButton(text='CLOSE')
        self.list_item_table = CustomTableWidget()
        self.manage_item_form = CustomGroupBox()

        self.setWidgetSignal() # -- SIGNALS FOR WIDGET

        self.main_layout.addWidget(self.filter_bar,0,0)
        self.main_layout.addWidget(self.add_button,0,1)
        self.main_layout.addWidget(self.close_button,0,1)
        self.main_layout.addWidget(self.list_item_table,2,0,1,2)
        self.main_layout.addWidget(self.manage_item_form,0,3,3,1)

        self.setLayout(self.main_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
