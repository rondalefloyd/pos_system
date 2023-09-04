import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

# -- changeable
from utils.schemas.sales_table_schema import *
from utils.schemas.promo_management_schema import *
from utils.widgets.promo_management_widget import *
# ----

class PromoManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.sales_table_schema = SalesTableSchema()

        # -- changeable
        self.promo_management_schema = PromoManagementSchema()
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
        self.promo_name = CustomComboBox(reference='promo_name')
        self.promo_type = CustomComboBox(reference='promo_type')
        self.discount_percent = CustomLineEdit(reference='discount_percent')
        self.description = CustomTextEdit(reference='description')
        # ----
        self.data_saved.connect(self.updateComboBox)

        self.save_add_button = CustomPushButton(text='SAVE NEW')
        self.save_add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_add_button'))
        self.save_edit_button = CustomPushButton(text='SAVE CHANGE')
        self.save_edit_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_edit_button'))

        self.panel_b_layout.addRow(self.close_button)

        # -- changeable
        self.panel_b_layout.addRow('promo_name', self.promo_name)
        self.panel_b_layout.addRow('promo_type', self.promo_type)
        self.panel_b_layout.addRow('discount_percent', self.discount_percent)
        self.panel_b_layout.addRow('description', self.description)
        # ----

        self.panel_b_layout.addRow(self.save_add_button)
        self.panel_b_layout.addRow(self.save_edit_button)

        self.panel_b.setLayout(self.panel_b_layout)

        return self.panel_b


    def populateTable(self, filter_text=''):
        self.list_table.clearContents()

        # -- changeable
        if filter_text == '':
            all_data = self.promo_management_schema.listPromo(filter_text)
        else:
            all_data = self.promo_management_schema.listPromo(filter_text)
        # ----

        for row_index, row_value in enumerate(all_data):
            total_cell = row_value[:4]

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
            self.promo_name.setCurrentText(data)
            self.promo_type.setCurrentText(data)
            self.discount_percent.setText(data)
            self.description.setPlainText(data)
            # ----
            
        elif reference == 'edit_button':
            self.panel_b.show()
            self.save_add_button.hide()
            self.save_edit_button.show()

            # -- changeable
            self.promo_name.setCurrentText(str(data[0]))
            self.promo_type.setCurrentText(str(data[1]))
            self.discount_percent.setText(str(data[2]))
            self.description.setPlainText(str(data[3]))
            self.promo_id = str(data[4])
            # ----

    def confirmAction(self, reference, data=''):
        if reference == 'remove_button':
            promo_name = str(data[0])
            promo_id = str(data[4])

            dialog = QMessageBox.warning(self, 'Remove', f"Are you sure you want to remove '{promo_name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if dialog == QMessageBox.StandardButton.Yes:
                self.promo_management_schema.removeSelectedPromo(promo_id)
                self.data_saved.emit()
                
            else:
                pass

    def saveData(self, reference):
        # -- changeable
        promo_name = str(self.promo_name.currentText())
        promo_type = str(self.promo_type.currentText())
        discount_percent = str(self.discount_percent.text())
        description = str(self.description.toPlainText())
        # ----

        if reference == 'save_add_button':
            # -- changeable
            self.promo_management_schema.addNewPromo(
                promo_name,
                promo_type,
                discount_percent,
                description
            )
            # ----
            self.data_saved.emit()

        elif reference == 'save_edit_button':
            # -- changeable
            

            self.promo_management_schema.editSelectedPromo(
                promo_name,
                promo_type,
                discount_percent,
                description,
                self.promo_id
            )
            # ----
            self.data_saved.emit()

    def updateComboBox(self):
        self.promo_name.fillComboBox()
        self.promo_type.fillComboBox()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoManagementWindow()
    window.show()
    sys.exit(pos_app.exec())

