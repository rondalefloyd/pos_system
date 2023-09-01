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

        if self.ref == 'access_level':
            self.setText('0')
            self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        if self.ref == 'access_level':
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
    data_saved = pyqtSignal()

    def __init__(self, reference=None):
        super().__init__()

        self.prepareDataManagement()    

        self.ref = reference

        if self.ref == 'user_name':
            self.setEditable(True)

        self.updateComboBox()
        
    def updateComboBox(self):
        data = self.accounts_data_manager.fillUserComboBox()
        
        self.clear()

        if self.ref == 'user_name': 
            for row in data:
                self.addItem(row[0])

        self.data_saved.emit()

    def prepareDataManagement(self):
        self.accounts_data_manager = AccountsDataManager()
    
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
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['','','user_name','password','access_level'])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

        if self.ref == 'panel_b':
            self.setFixedWidth(300)
            self.hide()
        pass

# ------------------------------------------------------------------------------- #

class UserManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__() 

        self.prepareDataManagement()
        self.setMainLayout()

    # PANEL B SECTION -------------------------------------------------------- #
    def refreshComboBox(self):
        self.user_name.updateComboBox()
    
    def updateEditPanelB(self, row_index, row_data):
        self.save_add_button.hide()
        self.save_edit_button.show()

        data = row_data

        self.user_name.setCurrentText(str(data[0]))
        self.password.setText(str(data[1]))
        self.access_level.setText(str(data[2]))
        self.user_id = str(data[3])

    def updateAddPanelB(self):
        self.save_add_button.show()
        self.save_edit_button.hide()

    def onSaveButtonClicked(self, reference):
        converted_user_name = str(self.user_name.currentText())
        converted_password = str(self.password.text())
        converted_access_level = int(self.access_level.text())


        if reference == 'add':
            print(reference)
            self.accounts_data_manager.addNewUser(converted_user_name, converted_password, converted_access_level)
            QMessageBox.information(self, "Success", "New user has been added!")
            

        elif reference == 'edit':
            print(reference)
            self.accounts_data_manager.editSelectedUser(converted_user_name, converted_password, converted_access_level, self.user_id)
            QMessageBox.information(self, "Success", "User has been edited!")
            

        self.data_saved.emit()
        

    def handleTextChanged(self, text, reference=None):
        if reference == 'filter_bar':
            self.populateTable(text)
            print(text)

    def onCloseButtonClicked(self):
        self.panel_b.hide()
        self.add_button.setDisabled(False)

    def showPanelB(self): # -- PANEL B
        panel = CustomGroupBox(reference='panel_b')
        panel_layout = QFormLayout()

        self.close_button = CustomPushButton(text='BACK')
        self.close_button.setFixedWidth(50)
        self.close_button.clicked.connect(self.onCloseButtonClicked)

        self.user_name = CustomComboBox(reference='user_name')
        self.password = CustomLineEdit(reference='password')
        self.access_level = CustomLineEdit(reference='access_level')

        self.save_add_button = CustomPushButton(text='SAVE ADD', reference='save_button')
        self.save_add_button.clicked.connect(lambda: self.onSaveButtonClicked('add'))

        self.save_edit_button = CustomPushButton(text='SAVE EDIT', reference='save_button')
        self.save_edit_button.clicked.connect(lambda: self.onSaveButtonClicked('edit'))
        
        panel_layout.addRow(self.close_button)

        panel_layout.addRow('user_name: ', self.user_name)
        panel_layout.addRow('password: ', self.password)
        panel_layout.addRow('access_level: ', self.access_level)


        panel_layout.addRow(self.save_add_button)
        panel_layout.addRow(self.save_edit_button)

        panel.setLayout(panel_layout)

        return panel

    # PANEL A SECTION -------------------------------------------------------- #
    def showRemoveConfirmationDialog(self, row_index, row_data):
        data = row_data
        user_name = str(data[0])
        user_id = str(data[3])

        confirmation = QMessageBox.question(self, "Remove", f"Are you sure you want to remove {user_name}", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            self.accounts_data_manager.removeSelectedUser(user_id)
            self.data_saved.emit()
        else:
            pass

    def onRemoveButtonClicked(self, row_index, row_data):
        self.showRemoveConfirmationDialog(row_index, row_data)
    
    def onEditButtonClicked(self, row_index, row_data):
        self.updateEditPanelB(row_index, row_data)
        self.panel_b.show()
        self.add_button.setDisabled(True)

    def onAddButtonClicked(self):
        self.updateAddPanelB()
        self.panel_b.show()
        self.add_button.setDisabled(True)

    def populateTable(self, text):
        self.list_table.clearContents()
        if text == '':
            data = self.accounts_data_manager.listUser('')
        else:
            data = self.accounts_data_manager.listUser(text)

    
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
        self.filter_bar.textChanged.connect(lambda text: self.handleTextChanged(text, reference='filter_bar'))
        self.add_button = CustomPushButton(text='ADD')
        self.add_button.clicked.connect(self.onAddButtonClicked)
        self.list_table = CustomTableWidget(reference='list_table')
        self.populateTable('')
        self.data_saved.connect(lambda: self.populateTable(''))
        self.data_saved.connect(self.refreshComboBox)


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
        self.accounts_data_manager = AccountsDataManager()
        self.accounts_data_manager.createAccountsTable() # -- for temporary used while main_admin_window is not yet existing

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = UserManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
