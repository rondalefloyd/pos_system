import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

# -- changeable
from utils.schemas.sales_table_schema import *
from utils.schemas.inventory_management_schema import *
from utils.widgets.inventory_management_widget import *
# ----

class InventoryManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.sales_table_schema = SalesTableSchema()

        # -- changeable
        self.inventory_management_schema = InventoryManagementSchema()
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
        self.list_table = CustomTableWidget(reference='list_table')

        self.data_saved.connect(self.populateTable)

        self.populateTable()

        self.panel_a_layout.addWidget(self.filter_bar,0,0)
        self.panel_a_layout.addWidget(self.list_table,1,0)

        self.panel_a.setLayout(self.panel_a_layout)

        return self.panel_a

    def showPanelB(self):
        self.panel_b = CustomGroupBox(reference='panel_b')
        self.panel_b_layout = QFormLayout()

        self.close_button = CustomPushButton(text='CLOSE')
        self.close_button.clicked.connect(lambda: self.onPushButtonClicked(reference='close_button'))

        # -- changeable
        self.current_item_name = CustomLineEdit(reference='current_item_name')
        self.available_stock = CustomLineEdit(reference='available_stock')
        self.on_hand_stock = CustomLineEdit(reference='on_hand_stock')
        # ----

        self.save_add_button = CustomPushButton(text='SAVE NEW')
        self.save_add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_add_button'))
        self.save_edit_button = CustomPushButton(text='SAVE CHANGE')
        self.save_edit_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_edit_button'))

        self.panel_b_layout.addRow(self.close_button)

        # -- changeable
        self.panel_b_layout.addRow('current_item_name', self.current_item_name)
        self.panel_b_layout.addRow('available_stock', self.available_stock)
        self.panel_b_layout.addRow('on_hand_stock', self.on_hand_stock)
        # ----

        self.panel_b_layout.addRow(self.save_add_button)
        self.panel_b_layout.addRow(self.save_edit_button)

        self.panel_b.setLayout(self.panel_b_layout)

        return self.panel_b


    def populateTable(self, filter_text=''):
        self.list_table.clearContents()

        # -- changeable
        if filter_text == '':
            all_data = self.inventory_management_schema.listStock(filter_text)
        else:
            all_data = self.inventory_management_schema.listStock(filter_text)
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
        if reference == 'edit_button':
            self.panel_b.show()
            self.save_add_button.hide()
            self.save_edit_button.show()

            # -- changeable
            self.current_item_name.setText(str(data[0]))
            self.available_stock.setText(str(data[1]))
            self.on_hand_stock.setText(str(data[2]))
            self.item_id = str(data[3])
            self.stock_id = str(data[4])
            # ----

    def confirmAction(self, reference, data=''):
        if reference == 'remove_button':
            current_item_name = str(data[0])
            stock_id = str(data[4])

            dialog = QMessageBox.warning(self, 'Stop tracking', f"Are you sure you want to stop tracking '{current_item_name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if dialog == QMessageBox.StandardButton.Yes:
                self.inventory_management_schema.removeSelectedStock(stock_id)
                self.data_saved.emit()
            else:
                pass

    def saveData(self, reference):
        # -- changeable
        available_stock = str(self.available_stock.text())
        on_hand_stock = str(self.on_hand_stock.text())
        # ----

        if reference == 'save_edit_button':
            # -- changeable
            self.inventory_management_schema.editSelectedStock(
                available_stock,
                on_hand_stock,
                self.item_id,
                self.stock_id
            )
            # ----
            self.data_saved.emit()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = InventoryManagementWindow()
    window.show()
    sys.exit(pos_app.exec())

