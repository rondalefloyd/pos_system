import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_manager import *

class CustomLineEdit(QLineEdit):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref == 'discount_percent':
            self.setText('0')
            self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        if self.ref == 'discount_percent':
            if event.text().isdigit() or event.key() == 16777219:  # Digit or Backspace key
                if self.text() == '0' and event.key() == 16777219:  # Backspace key
                    return
                if self.text() == '0' and event.text().isdigit():
                    self.setText(event.text())
                else:
                    super().keyPressEvent(event)

        # does nothing
        else:
            super().keyPressEvent(event)
        pass

class CustomComboBox(QComboBox):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref in ['promo_name', 'promo_type']:
            self.setEditable(True)

        pass

class CustomTextEdit(QTextEdit):
    def __init__(self, ref=None):
        super().__init__()

        pass

class CustomPushButton(QPushButton):
    def __init__(self, text=None):
        super().__init__()
        
        self.setText(text)

        pass

class CustomTableWidget(QTableWidget):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref == 'list_table':
            self.setRowCount(50)
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['','promo_name','promo_type','discount_percent','description'])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

        if self.ref == 'panel_b':
            self.setFixedWidth(300)
        pass

# ------------------------------------------------------------------------------- #

class InventoryManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.prepareDataManagement()
        self.setMainLayout()

    # -------------------------------------------------------- #

    def onClickedSaveButton(self):
        converted_promo_name = str(self.promo_name.currentText())
        converted_promo_type = str(self.promo_type.currentText())
        converted_discount_percent = str('{:.2f}'.format(float(self.discount_percent.text())))
        converted_desciption = str(self.desciption.toPlainText())

        print('converted_promo_name: ', converted_promo_name)
        print('converted_promo_type: ', converted_promo_type)
        print('converted_discount_percent: ', converted_discount_percent)
        print('converted_desciption: ', converted_desciption)

        self.sales_data_manager.addNewPromo(converted_promo_name, converted_promo_type, converted_discount_percent, converted_desciption)

        self.data_saved.emit()

    def onClickedCloseButton(self):
        self.panel_b.hide()
        self.add_button.setDisabled(False)

    def showPanelB(self): # -- PANEL B
        panel = CustomGroupBox(reference='panel_b')
        panel_layout = QFormLayout()

        self.close_button = CustomPushButton(text='BACK')
        self.close_button.setFixedWidth(50)
        self.close_button.clicked.connect(self.onClickedCloseButton)

        self.promo_name = CustomComboBox(reference='promo_name')
        self.promo_type = CustomComboBox(reference='promo_type')
        self.discount_percent = CustomLineEdit(reference='discount_percent')
        self.desciption = CustomTextEdit()


        self.save_button = CustomPushButton(text='SAVE')
        self.save_button.clicked.connect(self.onClickedSaveButton)
        
        panel_layout.addRow(self.close_button)

        panel_layout.addRow('promo_name: ', self.promo_name)
        panel_layout.addRow('promo_type: ', self.promo_type)
        panel_layout.addRow('discount_percent: ', self.discount_percent)
        panel_layout.addRow('desciption: ', self.desciption)



        panel_layout.addRow(self.save_button)

        panel.setLayout(panel_layout)

        return panel

    # -------------------------------------------------------- #

    def populateTable(self):
        data = self.sales_data_manager.listPromo()

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                cell = QTableWidgetItem(str(col_data))

                self.list_table.setItem(row_index, col_index + 1, cell)

            self.edit_button = CustomPushButton(text='EDIT')
            self.list_table.setCellWidget(row_index, 0, self.edit_button)

    def showPanelA(self): # -- PANEL A
        panel = CustomGroupBox()
        panel_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.list_table = CustomTableWidget(reference='list_table')
        self.populateTable()
        self.data_saved.connect(self.populateTable)

        panel_layout.addWidget(self.filter_bar,0,0)
        panel_layout.addWidget(self.add_button,0,1)
        panel_layout.addWidget(self.list_table,1,0,1,2)

        panel.setLayout(panel_layout)

        return panel
    
    # -------------------------------------------------------- #

    def setMainLayout(self):
        self.main_layout = QGridLayout()

        self.panel_a = self.showPanelA()
        self.panel_b = self.showPanelB()

        self.main_layout.addWidget(self.panel_a,0,0)
        self.main_layout.addWidget(self.panel_b,0,1)

        self.setLayout(self.main_layout)

    def prepareDataManagement(self):
        self.sales_data_manager = SalesDataManager()
        self.sales_data_manager.createSalesTable() # -- for temporary used while main_admin_window is not yet existing

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = InventoryManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
