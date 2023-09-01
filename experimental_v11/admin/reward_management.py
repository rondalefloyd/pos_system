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

        if self.ref == 'points_rate':
            self.setText('0')
            self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        if self.ref == 'points_rate':
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

        self.setEditable(True)

        self.updateComboBox()
        
    def updateComboBox(self):
        data = self.sales_data_manager.fillRewardComboBox()
         
        self.clear()
        for row in data:
            self.addItem(row[0])

        self.data_saved.emit()

    def prepareDataManagement(self):
        self.sales_data_manager = SalesDataManager()
    
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
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['','','reward_name','points_rate','description'])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

        if self.ref == 'panel_b':
            self.setFixedWidth(300)
            self.hide()
        pass

# ------------------------------------------------------------------------------- #

class RewardManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__() 

        self.prepareDataManagement()
        self.setMainLayout()

    # PANEL B SECTION -------------------------------------------------------- #
    def refreshComboBox(self):
        self.reward_name.updateComboBox()
    
    def updateEditPanelB(self, row_index, row_data):
        self.save_add_button.hide()
        self.save_edit_button.show()

        data = row_data

        self.reward_name.setCurrentText(str(data[0]))
        self.points_rate.setText(str(data[1]))
        self.desciption.setPlainText(str(data[2]))
        self.reward_id = str(data[3])

    def updateAddPanelB(self):
        self.save_add_button.show()
        self.save_edit_button.hide()

    def onSaveButtonClicked(self, reference):
        converted_reward_name = str(self.reward_name.currentText())
        converted_points_rate = str('{:.2f}'.format(float(self.points_rate.text())))
        converted_description = str(self.desciption.toPlainText())

        if reference == 'add':
            print(reference)
            self.sales_data_manager.addNewReward(converted_reward_name, converted_points_rate, converted_description)
            QMessageBox.information(self, "Success", "New reward has been added!")
            

        elif reference == 'edit':
            print(reference)
            self.sales_data_manager.editSelectedReward(converted_reward_name, converted_points_rate, converted_description, self.reward_id)
            QMessageBox.information(self, "Success", "Reward has been edited!")
            

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

        self.reward_name = CustomComboBox(reference='reward_name')
        self.points_rate = CustomLineEdit(reference='points_rate')
        self.desciption = CustomTextEdit()

        self.save_add_button = CustomPushButton(text='SAVE ADD', reference='save_button')
        self.save_add_button.clicked.connect(lambda: self.onSaveButtonClicked('add'))

        self.save_edit_button = CustomPushButton(text='SAVE EDIT', reference='save_button')
        self.save_edit_button.clicked.connect(lambda: self.onSaveButtonClicked('edit'))
        
        panel_layout.addRow(self.close_button)

        panel_layout.addRow('reward_name: ', self.reward_name)
        panel_layout.addRow('points_rate: ', self.points_rate)
        panel_layout.addRow('desciption: ', self.desciption)

        panel_layout.addRow(self.save_add_button)
        panel_layout.addRow(self.save_edit_button)

        panel.setLayout(panel_layout)

        return panel

    # PANEL A SECTION -------------------------------------------------------- #
    def showRemoveConfirmationDialog(self, row_index, row_data):
        data = row_data
        reward_name = str(data[0])
        reward_id = str(data[3])

        confirmation = QMessageBox.question(self, "Remove", f"Are you sure you want to remove {reward_name}", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            self.sales_data_manager.removeSelectedReward(reward_id)
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
            data = self.sales_data_manager.listReward('')
        else:
            data = self.sales_data_manager.listReward(text)

    
        for row_index, row_data in enumerate(data):
            total_cell = row_data[:3]

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
        self.sales_data_manager = SalesDataManager()
        self.sales_data_manager.createSalesTable() # -- for temporary used while main_admin_window is not yet existing

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = RewardManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
