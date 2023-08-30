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
    def __init__(self, text=None, reference=None):
        super().__init__()
        
        self.setText(text)
    
class CustomTableWidget(QTableWidget):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref == 'list_table':
            self.setRowCount(50)
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['','','promo_name','promo_type','discount_percent','description'])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

        if self.ref == 'panel_b':
            self.setFixedWidth(300)
            self.hide()
        pass

# ------------------------------------------------------------------------------- #

class PromoManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__() 

        self.prepareDataManagement()
        self.setMainLayout()

    # PANEL B SECTION -------------------------------------------------------- #
    def updateEditPanelB(self, row_index, row_data):
        self.save_add_button.hide()
        self.save_edit_button.show()

        data = row_data

        self.promo_name.setCurrentText(str(data[0]))
        self.promo_type.setCurrentText(str(data[1]))
        self.discount_percent.setText(str(data[2]))
        self.desciption.setPlainText(str(data[3]))
        self.promo_id = str(data[4])

    def updateAddPanelB(self):
        self.save_add_button.show()
        self.save_edit_button.hide()

        self.promo_name.setCurrentText('')
        self.promo_type.setCurrentText('')
        self.discount_percent.setText('')
        self.desciption.setPlainText('')

    def onSaveButtonClicked(self, reference):
        converted_promo_name = str(self.promo_name.currentText())
        converted_promo_type = str(self.promo_type.currentText())
        converted_discount_percent = str('{:.2f}'.format(float(self.discount_percent.text())))
        converted_description = str(self.desciption.toPlainText())

        if reference == 'add':
            print(reference)
            self.sales_data_manager.addNewPromo(converted_promo_name, converted_promo_type, converted_discount_percent, converted_description)
            QMessageBox.information(self, "Success", "New promo has been added!")
            self.data_saved.emit()

        elif reference == 'edit':
            print(reference)
            self.sales_data_manager.editSelectedPromo(converted_promo_name, converted_promo_type, converted_discount_percent, converted_description, self.promo_id)
            QMessageBox.information(self, "Success", "Promo has been edited!")
            self.data_saved.emit()

    def onCloseButtonClicked(self):
        self.panel_b.hide()
        self.add_button.setDisabled(False)

    def showPanelB(self): # -- PANEL B
        panel = CustomGroupBox(reference='panel_b')
        panel_layout = QFormLayout()

        self.close_button = CustomPushButton(text='BACK')
        self.close_button.setFixedWidth(50)
        self.close_button.clicked.connect(self.onCloseButtonClicked)

        self.promo_name = CustomComboBox(reference='promo_name')
        self.promo_type = CustomComboBox(reference='promo_type')
        self.discount_percent = CustomLineEdit(reference='discount_percent')
        self.desciption = CustomTextEdit()

        self.save_add_button = CustomPushButton(text='SAVE ADD', reference='save_button')
        self.save_add_button.clicked.connect(lambda: self.onSaveButtonClicked('add'))

        self.save_edit_button = CustomPushButton(text='SAVE EDIT', reference='save_button')
        self.save_edit_button.clicked.connect(lambda: self.onSaveButtonClicked('edit'))
        
        panel_layout.addRow(self.close_button)

        panel_layout.addRow('promo_name: ', self.promo_name)
        panel_layout.addRow('promo_type: ', self.promo_type)
        panel_layout.addRow('discount_percent: ', self.discount_percent)
        panel_layout.addRow('desciption: ', self.desciption)

        panel_layout.addRow(self.save_add_button)
        panel_layout.addRow(self.save_edit_button)

        panel.setLayout(panel_layout)

        return panel

    # PANEL A SECTION -------------------------------------------------------- #
    def showRemoveConfirmationDialog(self, promo_id):
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to remove this promo?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            self.sales_data_manager.removeSelectedPromo(promo_id)
            self.data_saved.emit()
        else:
            pass

    def onRemoveButtonClicked(self, row_index, row_data):
        promo_id = str(row_data[4])
        self.showRemoveConfirmationDialog(promo_id)
    
    def onEditButtonClicked(self, row_index, row_data):
        self.updateEditPanelB(row_index, row_data)
        self.panel_b.show()
        self.add_button.setDisabled(True)

    def onAddButtonClicked(self):
        self.updateAddPanelB()
        self.panel_b.show()
        self.add_button.setDisabled(True)

    def populateTable(self):
        self.list_table.clearContents()
        data = self.sales_data_manager.listPromo()

        for row_index, row_data in enumerate(data):
            total_cell = row_data[:4]

            for col_index, col_data in enumerate(total_cell):
                cell = QTableWidgetItem(str(col_data))

                self.list_table.setItem(row_index, col_index + 2, cell)

            self.edit_button = CustomPushButton(text='EDIT')
            self.edit_button.clicked.connect(lambda row_index=row_index, row_data=row_data: self.onEditButtonClicked(row_index, row_data))
            self.list_table.setCellWidget(row_index, 0, self.edit_button)
            
            self.remove_button = CustomPushButton(text='REMOVE')
            self.remove_button.clicked.connect(lambda row_index=row_index, row_data=row_data: self.onRemoveButtonClicked(row_index, row_data))
            self.list_table.setCellWidget(row_index, 1, self.remove_button)


    def showPanelA(self): # -- PANEL A
        panel = CustomGroupBox()
        panel_layout = QGridLayout()

        self.filter_bar = CustomLineEdit(reference='filter_bar')
        self.add_button = CustomPushButton(text='ADD')
        self.add_button.clicked.connect(self.onAddButtonClicked)
        self.list_table = CustomTableWidget(reference='list_table')
        self.populateTable()
        self.data_saved.connect(self.populateTable)

        panel_layout.addWidget(self.filter_bar,0,0)
        panel_layout.addWidget(self.add_button,0,1)
        panel_layout.addWidget(self.list_table,1,0,1,2)

        panel.setLayout(panel_layout)

        return panel
    
    # MAIN SECTION -------------------------------------------------------- #
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
    window = PromoManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
