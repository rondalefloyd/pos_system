import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

# -- changeable
from utils.schemas.sales_table_schema import *
from utils.schemas.reward_management_schema import *
from utils.widgets.reward_management_widget import *
# ----

class RewardManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.sales_table_schema = SalesTableSchema()

        # -- changeable
        self.reward_management_schema = RewardManagementSchema()
        # ----

        self.sales_table_schema.createSalesTable()

        self.main_layout = QGridLayout()

        self.panel_a_widget = self.showPanelA()
        self.panel_b_widget = self.showPanelB()

        self.main_layout.addWidget(self.panel_a_widget,0,0)
        self.main_layout.addWidget(self.panel_b_widget,0,1)

        self.setLayout(self.main_layout)

    def showPanelA(self):
        self.panel_a = CustomGroupBox(reference='panel_a')
        self.panel_a_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.filter_bar.textChanged.connect(lambda text: self.populateTable(filter_text=text))
        self.add_button = CustomPushButton(text='ADD')
        self.add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='add_button'))
        self.list_table = CustomTableWidget(reference='list_table')

        self.data_saved.connect(self.populateTable)

        self.populateTable()

        self.panel_a_layout.addWidget(self.filter_bar,0,0)
        self.panel_a_layout.addWidget(self.add_button,0,1)
        self.panel_a_layout.addWidget(self.list_table,1,0,1,2)

        self.panel_a.setLayout(self.panel_a_layout)

        return self.panel_a

    def showPanelB(self):
        self.panel_b = CustomGroupBox(reference='panel_b')
        self.panel_b_layout = QFormLayout()

        self.close_button = CustomPushButton(text='CLOSE')
        self.close_button.clicked.connect(lambda: self.onPushButtonClicked(reference='close_button'))

        # -- changeable
        self.reward_name = CustomComboBox(reference='reward_name')
        self.description = CustomTextEdit(reference='description')
        self.points_rate = CustomLineEdit(reference='points_rate')
        # ----
        self.data_saved.connect(self.updateComboBox)

        self.save_add_button = CustomPushButton(text='SAVE NEW')
        self.save_add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_add_button'))
        self.save_edit_button = CustomPushButton(text='SAVE CHANGE')
        self.save_edit_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_edit_button'))

        self.panel_b_layout.addRow(self.close_button)

        # -- changeable
        self.panel_b_layout.addRow('reward_name', self.reward_name)
        self.panel_b_layout.addRow('description', self.description)
        self.panel_b_layout.addRow('points_rate', self.points_rate)
        # ----

        self.panel_b_layout.addRow(self.save_add_button)
        self.panel_b_layout.addRow(self.save_edit_button)

        self.panel_b.setLayout(self.panel_b_layout)

        return self.panel_b


    def populateTable(self, filter_text=''):
        self.list_table.clearContents()

        # -- changeable
        if filter_text == '':
            all_data = self.reward_management_schema.listReward(filter_text)
        else:
            all_data = self.reward_management_schema.listReward(filter_text)
        # ----

        for row_index, row_value in enumerate(all_data):
            total_cell = row_value[:3]
            
            for col_index, col_value in enumerate(total_cell):
                edit_button = CustomPushButton(text='EDIT')
                edit_button.clicked.connect(lambda index=row_index, data=row_value: self.onPushButtonClicked(reference='edit_button', data=data))
                remove_button = CustomPushButton(text='REMOVE')
                remove_button.clicked.connect(lambda index=row_index, data=row_value: self.onPushButtonClicked(reference='remove_button', data=data))
                cell_value = QTableWidgetItem(str(col_value))

                self.list_table.setItem(row_index, col_index + 2, cell_value)

                
                self.list_table.setCellWidget(row_index, 0, edit_button)
                self.list_table.setCellWidget(row_index, 1, remove_button)

    def onPushButtonClicked(self, reference, data=''):
        if reference == 'close_button':
            self.panel_b.hide()

        elif reference == 'add_button':
            self.updatePanelB(reference)
        elif reference == 'edit_button':
            self.updatePanelB(reference, data)
        elif reference == 'remove_button':
            self.confirmAction(reference, data)
            
        elif reference == 'save_add_button':
            self.saveData(reference)
        elif reference == 'save_edit_button':
            self.saveData(reference)

    def updatePanelB(self, reference, data=''):
        print('data: ', data)
        if reference == 'add_button':
            self.panel_b.show()
            self.save_add_button.show()
            self.save_edit_button.hide()
            
            # -- changeable
            self.reward_name.setCurrentText(data)
            self.description.setPlainText(data)
            self.points_rate.setText(data)
            # ----
            
        elif reference == 'edit_button':
            self.panel_b.show()
            self.save_add_button.hide()
            self.save_edit_button.show()

            # -- changeable
            self.reward_name.setCurrentText(str(data[0]))
            self.description.setPlainText(str(data[1]))
            self.points_rate.setText(str(data[2]))
            self.reward_id = str(data[3])
            # ----

    def confirmAction(self, reference, data=''):
        if reference == 'remove_button':
            reward_name = str(data[0])
            reward_id = str(data[3])

            dialog = QMessageBox.warning(self, 'Remove', f"Are you sure you want to remove '{reward_name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if dialog == QMessageBox.StandardButton.Yes:
                self.reward_management_schema.removeSelectedReward(reward_id)
                self.data_saved.emit()
                
            else:
                pass

    def saveData(self, reference):
        # -- changeable
        reward_name = str(self.reward_name.currentText())
        description = str(self.description.toPlainText())
        points_rate = str(self.points_rate.text())
        # ----

        if reference == 'save_add_button':
            # -- changeable
            self.reward_management_schema.addNewReward(
                reward_name,
                description,
                points_rate
            )
            # ----
            self.data_saved.emit()

        elif reference == 'save_edit_button':
            # -- changeable
            self.reward_management_schema.editSelectedReward(
                reward_name,
                description,
                points_rate,
                self.reward_id
            )
            # ----
            self.data_saved.emit()

    def updateComboBox(self):
        self.reward_name.fillComboBox()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = RewardManagementWindow()
    window.show()
    sys.exit(pos_app.exec())

