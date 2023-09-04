import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

# -- changeable
from utils.schemas.sales_table_schema import *
from utils.schemas.item_management_schema import *
from utils.widgets.item_management_widget import *
# ----

class ItemManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.sales_table_schema = SalesTableSchema()

        # -- changeable
        self.item_management_schema = ItemManagementSchema()
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
        self.barcode = CustomLineEdit(reference='barcode')
        self.item_name = CustomComboBox(reference='item_name')
        self.expire_dt = CustomDateEdit(reference='expire_dt')

        self.item_type = CustomComboBox(reference='item_type')
        self.brand = CustomComboBox(reference='brand')
        self.sales_group = CustomComboBox(reference='sales_group')
        self.supplier = CustomComboBox(reference='supplier')

        self.cost = CustomLineEdit(reference='cost')
        self.sell_price = CustomLineEdit(reference='sell_price')
        self.sell_price.textChanged.connect(lambda: self.onLineEditTextChanged(reference='sell_price'))
        self.promo_name = CustomComboBox(reference='promo_name')
        self.promo_name.currentTextChanged.connect(lambda: self.onComboBoxCurrentTextChanged(reference='promo_name'))

        self.promo_type = CustomLineEdit(reference='promo_type')
        self.discount_percent = CustomLineEdit(reference='discount_percent')
        self.discount_value = CustomLineEdit(reference='discount_value')
        self.new_sell_price = CustomLineEdit(reference='new_sell_price')
        self.start_dt = CustomDateEdit(reference='start_dt')
        self.end_dt = CustomDateEdit(reference='end_dt')

        self.effective_dt = CustomDateEdit(reference='effective_dt')

        self.inventory_status = CustomComboBox(reference='inventory_status')
        self.inventory_status.currentTextChanged.connect(lambda: self.onComboBoxCurrentTextChanged(reference='inventory_status'))
        self.available_stock = CustomLineEdit(reference='available_stock')
        self.on_hand_stock = CustomLineEdit(reference='on_hand_stock')

        # label widgets:
        self.label_barcode = CustomLabel(text='barcode')
        self.label_item_name = CustomLabel(text='item_name')
        self.label_expire_dt = CustomLabel(text='expire_dt')
        self.label_item_type = CustomLabel(text='item_type')
        self.label_brand = CustomLabel(text='brand')
        self.label_sales_group = CustomLabel(text='sales_group')
        self.label_supplier = CustomLabel(text='supplier')
        self.label_cost = CustomLabel(text='cost')
        self.label_sell_price = CustomLabel(text='sell_price')
        self.label_promo_name = CustomLabel(text='promo_name')
        self.label_promo_type = CustomLabel(text='promo_type')
        self.label_discount_percent = CustomLabel(text='discount_percent')
        self.label_discount_value = CustomLabel(text='discount_value')
        self.label_new_sell_price = CustomLabel(text='new_sell_price')
        self.label_start_dt = CustomLabel(text='start_dt')
        self.label_end_dt = CustomLabel(text='end_dt')
        self.label_effective_dt = CustomLabel(text='effective_dt')
        self.label_inventory_status = CustomLabel(text='inventory_status')
        self.label_available_stock = CustomLabel(text='available_stock')
        self.label_on_hand_stock = CustomLabel(text='on_hand_stock')

        self.label_current_barcode = CustomLabel(text='current_barcode', reference='current_barcode')
        self.label_current_item_name = CustomLabel(text='current_item_name', reference='current_item_name')
        self.label_current_expire_dt = CustomLabel(text='current_expire_dt', reference='current_expire_dt')
        self.label_current_item_type = CustomLabel(text='current_item_type', reference='current_item_type')
        self.label_current_brand = CustomLabel(text='current_brand', reference='current_brand')
        self.label_current_sales_group = CustomLabel(text='current_sales_group', reference='current_sales_group')
        self.label_current_supplier = CustomLabel(text='current_supplier', reference='current_supplier')
        self.label_current_cost = CustomLabel(text='current_cost', reference='current_cost')
        self.label_current_sell_price = CustomLabel(text='current_sell_price', reference='current_sell_price')
        self.label_current_promo_name = CustomLabel(text='current_promo_name', reference='current_promo_name')
        self.label_current_promo_type = CustomLabel(text='current_promo_type', reference='current_promo_type')
        self.label_current_discount_percent = CustomLabel(text='current_discount_percent', reference='current_discount_percent')
        self.label_current_discount_value = CustomLabel(text='current_discount_value', reference='current_discount_value')
        self.label_current_new_sell_price = CustomLabel(text='current_new_sell_price', reference='current_new_sell_price')
        self.label_current_start_dt = CustomLabel(text='current_start_dt', reference='current_start_dt')
        self.label_current_end_dt = CustomLabel(text='current_end_dt', reference='current_end_dt')
        self.label_current_effective_dt = CustomLabel(text='current_effective_dt', reference='current_effective_dt')
        self.label_current_inventory_status = CustomLabel(text='current_inventory_status', reference='current_inventory_status')
        self.label_current_available_stock = CustomLabel(text='current_available_stock', reference='current_available_stock')
        self.label_current_on_hand_stock = CustomLabel(text='current_on_hand_stock', reference='current_on_hand_stock')

        # current data storage:
        self.current_barcode = CustomLineEdit(reference='current_barcode')
        self.current_item_name = CustomLineEdit(reference='current_item_name')
        self.current_expire_dt = CustomLineEdit(reference='current_expire_dt')
        self.current_item_type = CustomLineEdit(reference='current_item_type')
        self.current_brand = CustomLineEdit(reference='current_brand')
        self.current_sales_group = CustomLineEdit(reference='current_sales_group')
        self.current_supplier = CustomLineEdit(reference='current_supplier')
        self.current_cost = CustomLineEdit(reference='current_cost')
        self.current_sell_price = CustomLineEdit(reference='current_sell_price')
        self.current_promo_name = CustomLineEdit(reference='current_promo_name')
        self.current_promo_type = CustomLineEdit(reference='current_promo_type')
        self.current_discount_percent = CustomLineEdit(reference='current_discount_percent')
        self.current_discount_value = CustomLineEdit(reference='current_discount_value')
        self.current_new_sell_price = CustomLineEdit(reference='current_new_sell_price')
        self.current_start_dt = CustomLineEdit(reference='current_start_dt')
        self.current_end_dt = CustomLineEdit(reference='current_end_dt')
        self.current_effective_dt = CustomLineEdit(reference='current_effective_dt')
        self.current_inventory_status = CustomLineEdit(reference='current_inventory_status')
        self.current_available_stock = CustomLineEdit(reference='current_available_stock')
        self.current_on_hand_stock = CustomLineEdit(reference='current_on_hand_stock')

        # ----
        self.data_saved.connect(self.updateComboBox)

        self.save_add_button = CustomPushButton(text='SAVE NEW')
        self.save_add_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_add_button'))
        self.save_edit_button = CustomPushButton(text='SAVE CHANGE')
        self.save_edit_button.clicked.connect(lambda: self.onPushButtonClicked(reference='save_edit_button'))

        self.panel_b_layout.addRow(self.close_button)

        # -- changeable
        self.panel_b_layout.addRow(self.label_barcode, self.barcode)
        self.panel_b_layout.addRow(self.label_current_barcode, self.current_barcode)
        self.panel_b_layout.addRow(self.label_item_name, self.item_name)
        self.panel_b_layout.addRow(self.label_current_item_name, self.current_item_name)
        self.panel_b_layout.addRow(self.label_expire_dt, self.expire_dt)
        self.panel_b_layout.addRow(self.label_current_expire_dt, self.current_expire_dt)
        self.panel_b_layout.addRow(self.label_item_type, self.item_type)
        self.panel_b_layout.addRow(self.label_current_item_type, self.current_item_type)
        self.panel_b_layout.addRow(self.label_brand, self.brand)
        self.panel_b_layout.addRow(self.label_current_brand, self.current_brand)
        self.panel_b_layout.addRow(self.label_sales_group, self.sales_group)
        self.panel_b_layout.addRow(self.label_current_sales_group, self.current_sales_group)
        self.panel_b_layout.addRow(self.label_supplier, self.supplier)
        self.panel_b_layout.addRow(self.label_current_supplier, self.current_supplier)
        self.panel_b_layout.addRow(self.label_cost, self.cost)
        self.panel_b_layout.addRow(self.label_current_cost, self.current_cost)
        self.panel_b_layout.addRow(self.label_sell_price, self.sell_price)
        self.panel_b_layout.addRow(self.label_current_sell_price, self.current_sell_price)
        self.panel_b_layout.addRow(self.label_promo_name, self.promo_name)
        self.panel_b_layout.addRow(self.label_current_promo_name, self.current_promo_name)
        self.panel_b_layout.addRow(self.label_promo_type, self.promo_type)
        self.panel_b_layout.addRow(self.label_current_promo_type, self.current_promo_type)
        self.panel_b_layout.addRow(self.label_discount_percent, self.discount_percent)
        self.panel_b_layout.addRow(self.label_current_discount_percent, self.current_discount_percent)
        self.panel_b_layout.addRow(self.label_discount_value, self.discount_value)
        self.panel_b_layout.addRow(self.label_current_discount_value, self.current_discount_value)
        self.panel_b_layout.addRow(self.label_new_sell_price, self.new_sell_price)
        self.panel_b_layout.addRow(self.label_current_new_sell_price, self.current_new_sell_price)
        self.panel_b_layout.addRow(self.label_start_dt, self.start_dt)
        self.panel_b_layout.addRow(self.label_current_start_dt, self.current_start_dt)
        self.panel_b_layout.addRow(self.label_end_dt, self.end_dt)
        self.panel_b_layout.addRow(self.label_current_end_dt, self.current_end_dt)
        self.panel_b_layout.addRow(self.label_effective_dt, self.effective_dt)
        self.panel_b_layout.addRow(self.label_current_effective_dt, self.current_effective_dt)
        self.panel_b_layout.addRow(self.label_inventory_status, self.inventory_status)
        self.panel_b_layout.addRow(self.label_current_inventory_status, self.current_inventory_status)
        self.panel_b_layout.addRow(self.label_available_stock, self.available_stock)
        self.panel_b_layout.addRow(self.label_current_available_stock, self.current_available_stock)
        self.panel_b_layout.addRow(self.label_on_hand_stock, self.on_hand_stock)
        self.panel_b_layout.addRow(self.label_current_on_hand_stock, self.current_on_hand_stock)
        # ----

        self.panel_b_layout.addRow(self.save_add_button)
        self.panel_b_layout.addRow(self.save_edit_button)

        self.panel_b.setLayout(self.panel_b_layout)

        return self.panel_b


    def populateTable(self, filter_text=''):
        self.list_table.clearContents()

        # -- changeable
        if filter_text == '':
            all_data = self.item_management_schema.listItem(filter_text)
        else:
            all_data = self.item_management_schema.listItem(filter_text)
        # ----

        for row_index, row_value in enumerate(all_data):
            total_col = row_value[:13]
            for col_index, col_value in enumerate(total_col):
                edit_button = CustomPushButton(text='EDIT')
                edit_button.clicked.connect(lambda index=row_index, data=row_value: self.onPushButtonClicked(reference='edit_button', data=data))
                remove_button = CustomPushButton(text='REMOVE')
                remove_button.clicked.connect(lambda index=row_index, data=row_value: self.onPushButtonClicked(reference='remove_button', data=data))
                cell_value = QTableWidgetItem(str(col_value))

                self.list_table.setItem(row_index, col_index + 2, cell_value)

                self.list_table.setCellWidget(row_index, 0, edit_button)
                self.list_table.setCellWidget(row_index, 1, remove_button)

                promo_name = row_value[11]
                print(promo_name)
                if promo_name != 'N/A':
                    cell_value.setForeground(QColor(255, 0, 255))
                    edit_button.setText('VIEW')

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

    def onLineEditTextChanged(self, reference=''):
        if reference == 'sell_price':
            if self.sell_price.text() in ['0','']:
                self.promo_name.setDisabled(True)

            else:
                self.promo_name.setDisabled(False)

                try:
                    sell_price = float(self.sell_price.text())
                    discount_percent = float(self.discount_percent.text())

                    old_sell_price = sell_price
                    discount_amount = old_sell_price * (discount_percent / 100)
                    
                    new_sell_price = sell_price - discount_amount

                    self.discount_value.setText(f'{discount_amount:.2f}')
                    self.new_sell_price.setText(f'{new_sell_price:.2f}')
                    pass

                except ValueError:
                    pass

    def onComboBoxCurrentTextChanged(self, reference=''):
        # promo
        if reference == 'promo_name':
            if self.promo_name.currentText() == 'No promo':
                self.label_promo_type.hide()
                self.promo_type.hide()
                self.label_discount_percent.hide()
                self.discount_percent.hide()
                self.label_discount_value.hide()
                self.discount_value.hide()
                self.label_new_sell_price.hide()
                self.new_sell_price.hide()
                self.label_start_dt.hide()
                self.start_dt.hide()
                self.label_end_dt.hide()
                self.end_dt.hide()
                self.label_effective_dt.show()
                self.effective_dt.show()
                
            else:
                self.label_promo_type.show()
                self.promo_type.show()
                self.label_discount_percent.show()
                self.discount_percent.show()
                self.label_discount_value.show()
                self.discount_value.show()
                self.label_new_sell_price.show()
                self.new_sell_price.show()
                self.label_start_dt.show()
                self.start_dt.show()
                self.label_end_dt.show()
                self.end_dt.show()
                self.label_effective_dt.hide()
                self.effective_dt.hide()

                promo_name = str(self.promo_name.currentText())

                data = self.item_management_schema.getPromoTypeAndDiscountPercent(promo_name)
                for row in data:
                    self.promo_type.setText(str(row[0]))
                    self.discount_percent.setText(str(row[1]))

                try:
                    sell_price = float(self.sell_price.text())
                    discount_percent = float(self.discount_percent.text())

                    old_sell_price = sell_price
                    discount_amount = old_sell_price * (discount_percent / 100)
                    
                    new_sell_price = sell_price - discount_amount

                    self.discount_value.setText(f'{discount_amount:.2f}')
                    self.new_sell_price.setText(f'{new_sell_price:.2f}')
                    pass
                except ValueError:
                    pass

        # inventory
        if reference == 'inventory_status':
            if self.inventory_status.currentText() == 'Not tracked':
                self.label_available_stock.hide()
                self.available_stock.hide()
                self.label_on_hand_stock.hide()
                self.on_hand_stock.hide()

            else:
                self.label_available_stock.show()
                self.available_stock.show()
                self.label_on_hand_stock.show()
                self.on_hand_stock.show()


    def updatePanelB(self, reference, data=''):
        print('data: ', data)
        if reference == 'add_button':
            self.panel_b.show()
            self.save_add_button.show()
            self.save_edit_button.hide()
            
            # -- changeable
            self.label_barcode.show()
            self.label_item_name.show()
            self.label_expire_dt.show()
            self.label_item_type.show()
            self.label_brand.show()
            self.label_sales_group.show()
            self.label_supplier.show()
            self.label_cost.show()
            self.label_sell_price.show()
            self.label_promo_name.show()
            self.label_promo_type.hide()
            self.label_discount_percent.hide()
            self.label_discount_value.hide()
            self.label_new_sell_price.hide()
            self.label_start_dt.hide()
            self.label_end_dt.hide()
            self.label_effective_dt.show()
            self.label_inventory_status.show()
            self.label_available_stock.hide()
            self.label_on_hand_stock.hide()

            self.barcode.show()
            self.item_name.show()
            self.expire_dt.show()
            self.item_type.show()
            self.brand.show()
            self.sales_group.show()
            self.supplier.show()
            self.cost.show()
            self.sell_price.show()
            self.promo_name.show()
            self.promo_type.hide()
            self.discount_percent.hide()
            self.discount_value.hide()
            self.new_sell_price.hide()
            self.start_dt.hide()
            self.end_dt.hide()
            self.effective_dt.show()
            self.inventory_status.show()
            self.available_stock.hide()
            self.on_hand_stock.hide()

            # show current widgets
            self.label_current_barcode.hide()
            self.label_current_item_name.hide()
            self.label_current_expire_dt.hide()
            self.label_current_item_type.hide()
            self.label_current_brand.hide()
            self.label_current_sales_group.hide()
            self.label_current_supplier.hide()
            self.label_current_cost.hide()
            self.label_current_sell_price.hide()
            self.label_current_promo_name.hide()
            self.label_current_discount_value.hide()
            self.label_current_effective_dt.hide()
            self.label_current_inventory_status.hide()

            self.current_barcode.hide()
            self.current_item_name.hide()
            self.current_expire_dt.hide()
            self.current_item_type.hide()
            self.current_brand.hide()
            self.current_sales_group.hide()
            self.current_supplier.hide()
            self.current_cost.hide()
            self.current_sell_price.hide()
            self.current_promo_name.hide()
            self.current_discount_value.hide()
            self.current_effective_dt.hide()
            self.current_inventory_status.hide()

            self.barcode.setText(data)
            self.item_name.setCurrentText(data)
            self.item_type.setCurrentText(data)
            self.brand.setCurrentText(data)
            self.supplier.setCurrentText(data)
            self.cost.setText(data)
            self.sell_price.setText(data)
            self.promo_type.setText(data)
            self.discount_percent.setText(data)
            self.discount_value.setText(data)
            self.new_sell_price.setText(data)
            self.available_stock.setText(data)
            self.on_hand_stock.setText(data)
            # ----
            
        elif reference == 'edit_button':
            self.panel_b.show()
            self.save_add_button.hide()
            self.save_edit_button.show()

            # -- changeable
            self.label_barcode.hide()
            self.label_item_name.hide()
            self.label_expire_dt.hide()
            self.label_item_type.hide()
            self.label_brand.hide()
            self.label_sales_group.hide()
            self.label_supplier.hide()
            self.label_cost.hide()
            self.label_sell_price.hide()
            self.label_promo_name.hide()
            self.label_promo_type.hide()
            self.label_discount_percent.hide()
            self.label_discount_value.hide()
            self.label_new_sell_price.hide()
            self.label_start_dt.hide()
            self.label_end_dt.hide()
            self.label_effective_dt.hide()
            self.label_inventory_status.hide()
            self.label_available_stock.hide()
            self.label_on_hand_stock.hide()

            self.barcode.hide()
            self.item_name.hide()
            self.expire_dt.hide()
            self.item_type.hide()
            self.brand.hide()
            self.sales_group.hide()
            self.supplier.hide()
            self.cost.hide()
            self.sell_price.hide()
            self.promo_name.hide()
            self.promo_type.hide()
            self.discount_percent.hide()
            self.discount_value.hide()
            self.new_sell_price.hide()
            self.start_dt.hide()
            self.end_dt.hide()
            self.effective_dt.hide()
            self.inventory_status.hide()
            self.available_stock.hide()
            self.on_hand_stock.hide()

            # show current widgets
            self.label_current_barcode.show()
            self.label_current_item_name.show()
            self.label_current_expire_dt.show()
            self.label_current_item_type.show()
            self.label_current_brand.show()
            self.label_current_sales_group.show()
            self.label_current_supplier.show()
            self.label_current_cost.show()
            self.label_current_sell_price.show()
            self.label_current_promo_name.show()
            self.label_current_discount_value.show()
            self.label_current_effective_dt.show()
            self.label_current_inventory_status.show()

            self.current_barcode.show()
            self.current_item_name.show()
            self.current_expire_dt.show()
            self.current_item_type.show()
            self.current_brand.show()
            self.current_sales_group.show()
            self.current_supplier.show()
            self.current_cost.show()
            self.current_sell_price.show()
            self.current_promo_name.show()
            self.current_discount_value.show()
            self.current_effective_dt.show()
            self.current_inventory_status.show()

            # store data
            self.current_barcode.setText(str(data[0]))
            self.current_item_name.setText(str(data[1]))
            self.current_expire_dt.setText(str(data[2]))
            self.current_item_type.setText(str(data[3]))
            self.current_brand.setText(str(data[4]))
            self.current_sales_group.setText(str(data[5]))
            self.current_supplier.setText(str(data[6]))
            self.current_cost.setText(str(data[7]))
            self.current_sell_price.setText(str(data[8]))
            self.current_promo_name.setText(str(data[11]))
            self.current_promo_type.setText(str(data[13]))
            self.current_discount_percent.setText(str(data[14]))
            self.current_discount_value.setText(str(data[9]))
            self.current_effective_dt.setText(str(data[10]))
            self.current_inventory_status.setText(str(data[12]))
            self.item_id = str(data[15])
            self.item_price_id = str(data[16])
            self.promo_id = str(data[17])

            if self.promo_id == '0':
                self.label_barcode.show()
                self.barcode.show()
                self.label_item_name.show()
                self.item_name.show()
                self.label_expire_dt.show()
                self.expire_dt.show()
                self.label_cost.show()
                self.cost.show()
                self.label_sell_price.show()
                self.sell_price.show()
                self.label_promo_name.show()
                self.promo_name.show()
                self.label_effective_dt.show()
                self.effective_dt.show()

                self.save_edit_button.show()


                self.label_current_barcode.hide()
                self.label_current_item_name.hide()
                self.label_current_expire_dt.hide()
                self.label_current_cost.hide()
                self.label_current_sell_price.hide()
                self.label_current_promo_name.hide()
                self.label_current_discount_value.hide()
                self.label_current_effective_dt.hide()

                self.current_barcode.hide()
                self.current_item_name.hide()
                self.current_expire_dt.hide()
                self.current_cost.hide()
                self.current_sell_price.hide()
                self.current_promo_name.hide()
                self.current_discount_value.hide()
                self.current_effective_dt.hide()

                self.barcode.setText(str(data[0]))
                self.item_name.setCurrentText(str(data[1]))
                self.expire_dt.setDate(QDate.fromString(data[2], Qt.DateFormat.ISODate))
                self.cost.setText(str(data[7]))
                self.sell_price.setText(str(data[8]))
                self.promo_name.setCurrentText('No promo')
                self.effective_dt.setDate(QDate.fromString(data[10], Qt.DateFormat.ISODate))

            else:
                self.save_edit_button.hide()
            # ----

    def confirmAction(self, reference, data=''):
        if reference == 'remove_button':
            item_name = str(data[1])
            item_price = str(data[16])

            dialog = QMessageBox.warning(self, 'Remove', f"Are you sure you want to remove '{item_name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if dialog == QMessageBox.StandardButton.Yes:
                self.item_management_schema.removeSelectedItem(item_price)
                self.data_saved.emit()
                
            else:
                pass

    def saveData(self, reference):
        # -- changeable
        if reference == 'save_add_button':
            barcode = str(self.barcode.text())
            item_name = str(self.item_name.currentText())
            expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)
            item_type = str(self.item_type.currentText())
            brand = str(self.brand.currentText())
            sales_group = str(self.sales_group.currentText())
            supplier = str(self.supplier.currentText())
            cost = str(self.cost.text())
            sell_price = str(self.sell_price.text())
            promo_name = str(self.promo_name.currentText())
            promo_type = str(self.promo_type.text())
            discount_percent = str(self.discount_percent.text())
            discount_value = str(self.discount_value.text())
            new_sell_price = str(self.new_sell_price.text())
            start_dt = self.start_dt.date().toString(Qt.DateFormat.ISODate)
            end_dt = self.end_dt.date().toString(Qt.DateFormat.ISODate)
            effective_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate)
            inventory_status = str(self.inventory_status.currentText())
            available_stock = str(self.available_stock.text())
            on_hand_stock = str(self.on_hand_stock.text())

        elif reference == 'save_edit_button':
            barcode = str(self.barcode.text())
            item_name = str(self.item_name.currentText())
            expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)

            item_type = str(self.current_item_type.text())
            brand = str(self.current_brand.text())
            sales_group = str(self.current_sales_group.text())
            supplier = str(self.current_supplier.text())

            cost = str(self.cost.text())
            sell_price = str(self.sell_price.text())
            promo_name = str(self.promo_name.currentText())
            promo_type = str(self.promo_type.text())
            discount_percent = str(self.discount_percent.text())
            discount_value = str(self.discount_value.text())
            new_sell_price = str(self.new_sell_price.text())
            start_dt = self.start_dt.date().toString(Qt.DateFormat.ISODate)
            end_dt = self.end_dt.date().toString(Qt.DateFormat.ISODate)
            effective_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate)
        # ----

        if reference == 'save_add_button':
            # -- changeable
            self.item_management_schema.addNewItem(
                barcode,
                item_name,
                expire_dt,
                item_type,
                brand,
                sales_group,
                supplier,
                cost,
                sell_price,
                new_sell_price,
                effective_dt,
                promo_name,
                promo_type,
                discount_percent,
                discount_value,
                start_dt,
                end_dt,
                inventory_status,
                available_stock,
                on_hand_stock
            )
            # ----
            self.data_saved.emit()

        elif reference == 'save_edit_button':
            # -- changeable
            self.item_management_schema.editSelectedItem(
                barcode,
                item_name,
                expire_dt,
                item_type,
                brand,
                sales_group,
                supplier,
                cost,
                sell_price,
                new_sell_price,
                promo_name,
                promo_type,
                discount_percent,
                discount_value,
                start_dt,
                end_dt,
                effective_dt,
                self.item_id,
                self.item_price_id,
                self.promo_id
            )
            # ----
            self.data_saved.emit()

    def updateComboBox(self):
        self.item_name.fillComboBox()
        self.item_type.fillComboBox()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())

