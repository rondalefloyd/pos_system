import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.databse_manager import *

# -- global widgets
class CustomLineEdit(QLineEdit):
    def __init__(self, ref=None):
        super().__init__()
    
        self.setDefaultAttribute(ref)

    def setDefaultAttribute(self, ref):
        pass

class CustomComboBox(QComboBox):
    def __init__(self, ref=None):
        super().__init__()

        self.setDefaultAttribute(ref)

    def setDefaultAttribute(self, ref):
        if ref == 'promo_name' or ref == 'promo_type':
            self.setEditable(True)
        pass

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
    
        pass

class CustomPushButton(QPushButton):
    def __init__(self, setText=None):
        super().__init__()

        self.setText(setText)
        
class CustomTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setDefaultAttribute()

    def setDefaultAttribute(self):
        self.setColumnCount(5)
        self.setRowCount(50)

        self.setHorizontalHeaderLabels(['','promo_name', 'promo_type', 'discount_percent', 'description'])


# -- for layouts
class ManagePromoForm(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.callClass()
        self.setMainLayout()
        self.setWidgetSignal()
        self.setCurrentValues()

    def onClickedSaveButton(self):
        # -- step a: set datatypes to inputs
        converted_promo_name = str(self.promo_name.currentText())
        converted_promo_type = str(self.promo_type.currentText())
        converted_discount_value = str('{:.2f}'.format(float(self.discount_percent.text())))
        converted_description = str(self.description.toPlainText())

        self.database_manager.addNewPromo(
            converted_promo_name,
            converted_promo_type,
            converted_discount_value,
            converted_description
        )

        self.data_saved.emit()

    def setWidgetSignal(self):
        self.save_button.clicked.connect(self.onClickedSaveButton)
        pass

    def setCurrentValues(self, mode=None, row_index=None, row_value=None):
        pass

    def setMainLayout(self):
        self.grid_layout = QFormLayout()

        self.promo_name = CustomComboBox(ref='promo_name')
        self.promo_type = CustomComboBox(ref='promo_type')
        self.discount_percent = QLineEdit()
        self.description = CustomTextEdit()

        self.save_button = CustomPushButton(setText='SAVE')

        self.grid_layout.addRow('promo_name: ', self.promo_name)
        self.grid_layout.addRow('promo_type: ', self.promo_type)
        self.grid_layout.addRow('discount_percent: ', self.discount_percent)
        self.grid_layout.addRow('description: ', self.description)

        self.grid_layout.addRow(self.save_button)

        self.setLayout(self.grid_layout)

    def callClass(self):
        self.database_manager = SalesDatabaseSetup()

class PromoManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.callClass()
        self.setMainLayout()
        self.setWidgetSignal()
        self.setCurrentValues()

    def onTextChangedFilterBar(self):
        pass
    
    def onClickedCloseButton(self):
        self.manage_promo_form.hide()
        self.close_button.hide()
        self.add_button.show()
        pass

    def onClickedAddButton(self, mode):
        self.manage_promo_form.setCurrentValues(mode=mode)
        self.manage_promo_form.show()
        self.close_button.show()
        self.add_button.hide()
        self.manage_promo_form.data_saved.connect(self.fillPromoListTable)
        pass

    def onClickedEditButton(self, mode, row_index, row_value):
        self.manage_promo_form.setCurrentValues(mode=mode, row_value=row_value)
        self.manage_promo_form.show()
        self.close_button.show()
        self.add_button.hide()
        self.manage_promo_form.data_saved.connect(self.fillPromoListTable)
        pass

    def fillPromoListTable(self):
        data = self.database_manager.listPromo()

        for row_index, row_value in enumerate(data):
            total_cell = row_value[:11]
            for col_index, col_value in enumerate(total_cell):
                cell = QTableWidgetItem(str(col_value))
                self.promo_list_table.setItem(row_index, col_index + 1, cell)

            self.edit_button = CustomPushButton(setText='EDIT')
            self.promo_list_table.setCellWidget(row_index, 0, self.edit_button)
            self.edit_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.onClickedEditButton('edit_mode', row_index, row_value))

    def setWidgetSignal(self):
        pass
    
    def setCurrentValues(self):
        self.manage_promo_form.hide()
        self.close_button.hide()
        self.fillPromoListTable()

    def setMainLayout(self):
        self.grid_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.add_button = CustomPushButton(setText='ADD')
        self.add_button.clicked.connect(lambda: self.onClickedAddButton('add_mode'))
        self.close_button = CustomPushButton(setText='CLOSE')
        self.close_button.clicked.connect(self.onClickedCloseButton)
        self.promo_list_table = CustomTableWidget()
        self.manage_promo_form = ManagePromoForm() # -- for adding and editing items

        self.grid_layout.addWidget(self.filter_bar,0,0)
        self.grid_layout.addWidget(self.add_button,0,1)
        self.grid_layout.addWidget(self.close_button,0,1)
        self.grid_layout.addWidget(self.promo_list_table,1,0,1,2)
        self.grid_layout.addWidget(self.manage_promo_form,0,2,2,2)


        self.setLayout(self.grid_layout)

    def callClass(self):
        self.database_manager = SalesDatabaseSetup()
        self.database_manager.createSalesTable() # -- for temporary use only     

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
