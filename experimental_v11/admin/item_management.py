import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.databse_manager import *

class CustomLabel(QLabel):
    def __init__(self, text, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref in [
            'promo_type',
            'discount_percent',
            'discount_value',
            'new_sell_price',
            'start_dt',
            'end_dt'
        ]:
            self.hide()

        self.setText(text)

class CustomLineEdit(QLineEdit):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref in ['cost', 'sell_price', 'discount_percent', 'discount_value', 'new_sell_price', 'on_hand_stock', 'available_stock']:
            self.setText('0')
            self.textChanged.connect(self.handleTextChanged)

        if self.ref in ['promo_type', 'discount_percent', 'discount_value', 'new_sell_price']:
            self.setDisabled(True)
            self.hide()

    def handleTextChanged(self, text):
        if text == '':  
            self.setText('0')

    def keyPressEvent(self, event):
        if self.ref in ['cost', 'sell_price', 'new_sell_price', 'discount_percent', 'discount_value', 'on_hand_stock', 'available_stock']:
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

        self.prepareDataManagement()

        self.ref = reference

        if self.ref in ['item_name', 'item_type', 'brand', 'supplier']:
            self.setEditable(True)

        if self.ref == 'sales_group':
            self.addItem('Retail')
            self.addItem('Wholesale')

        if self.ref == 'promo_name':
            self.setDisabled(True)
            self.addItem('No promo')
            data = self.sales_data_manager.listPromo()
            for row in data:
                self.addItem(row[0])

        if self.ref == 'inventory_status':
            self.addItem('Track inventory')
            self.addItem("Don't track inventory")

    def prepareDataManagement(self):
        self.sales_data_manager = SalesDataManager()
    

class CustomDateEdit(QDateEdit):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

        if self.ref in ['start_dt', 'end_dt']:
            self.hide()

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
            self.setColumnCount(12)
            self.setHorizontalHeaderLabels(['',
                'barcode',
                'item_name',
                'expire_dt',
                'item_type',
                'brand',
                'sales_group',
                'supplier',
                'cost',
                'sell_price',
                'discount_value',
                'effective_dt'
            ])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

        if self.ref == 'panel_b':
            self.setFixedWidth(300)
        pass

# ------------------------------------------------------------------------------- #

class ItemManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.prepareDataManagement()
        self.setMainLayout()

    # -------------------------------------------------------- #

    def onClickedSaveButton(self):
        converted_barcode = str(self.barcode.text())
        converted_item_name = str(self.item_name.currentText())
        converted_expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)

        converted_item_type = str(self.item_type.currentText())
        converted_brand = str(self.brand.currentText())
        converted_sales_group = str(self.sales_group.currentText())
        converted_supplier = str(self.supplier.currentText())

        converted_cost = str('{:.2f}'.format(float(self.cost.text())))
        converted_sell_price = str('{:.2f}'.format(float(self.sell_price.text())))
        converted_new_sell_price = str('{:.2f}'.format(float(self.new_sell_price.text())))
        converted_promo_name = str(self.promo_name.currentText())
        converted_promo_type = str(self.promo_type.text())
        converted_discount_percent = str('{:.2f}'.format(float(self.discount_percent.text())))
        converted_discount_value = str('{:.2f}'.format(float(self.discount_value.text())))
        converted_start_dt = self.start_dt.date().toString(Qt.DateFormat.ISODate)
        converted_end_dt = self.end_dt.date().toString(Qt.DateFormat.ISODate)
        converted_effective_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate)

        converted_inventory_status = str(self.inventory_status.currentText())
        converted_on_hand_stock = str(int(self.on_hand_stock.text()))
        converted_available_stock = str(int(self.available_stock.text()))

        print('converted_barcode: ', converted_barcode)
        print('converted_item_name: ', converted_item_name)
        print('converted_expire_dt: ', converted_expire_dt)
        print('converted_item_type: ', converted_item_type)
        print('converted_brand: ', converted_brand)
        print('converted_sales_group: ', converted_sales_group)
        print('converted_supplier: ', converted_supplier)
        print('converted_cost: ', converted_cost)
        print('converted_sell_price: ', converted_sell_price)
        print('converted_promo_name: ', converted_promo_name)
        print('converted_promo_type: ', converted_promo_type)
        print('converted_discount_percent: ', converted_discount_percent)
        print('converted_discount_value: ', converted_discount_value)
        print('converted_new_sell_price: ', converted_new_sell_price)
        print('converted_start_dt: ', converted_start_dt)
        print('converted_end_dt: ', converted_end_dt)
        print('converted_effective_dt: ', converted_effective_dt)
        print('converted_inventory_status: ', converted_inventory_status)
        print('converted_on_hand_stock: ', converted_on_hand_stock)
        print('converted_available_stock: ', converted_available_stock)

        self.sales_data_manager.addNewItem(
            converted_barcode,
            converted_item_name,
            converted_expire_dt,
            converted_item_type,
            converted_brand,
            converted_sales_group,
            converted_supplier,
            converted_cost,
            converted_sell_price,
            converted_new_sell_price,
            converted_effective_dt,
            converted_promo_name,
            converted_inventory_status,
            converted_promo_type,
            converted_discount_percent,
            converted_discount_value,
            converted_start_dt,
            converted_end_dt,
            converted_on_hand_stock,
            converted_available_stock
        )

        self.data_saved.emit()

    def handleTextChanged(self, text, reference=None):
        if reference == 'sell_price':
            if text == '0' or text == '':
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

    def handleCurrentTextChanged(self, currentText, reference=None):
        if reference == 'promo_name':
            if currentText == 'No promo':
                self.label_new_sell_price.hide()
                self.new_sell_price.hide()
                self.label_promo_type.hide()
                self.promo_type.hide()
                self.label_discount_percent.hide()
                self.discount_percent.hide()
                self.label_discount_value.hide()
                self.discount_value.hide()
                self.label_start_dt.hide()
                self.start_dt.hide()
                self.label_end_dt.hide()
                self.end_dt.hide()
                self.label_effective_dt.show()
                self.effective_dt.show()
            else:
                self.label_new_sell_price.show()
                self.new_sell_price.show()
                self.label_promo_type.show()
                self.promo_type.show()
                self.label_discount_percent.show()
                self.discount_percent.show()
                self.label_discount_value.show()
                self.discount_value.show()
                self.label_start_dt.show()
                self.start_dt.show()
                self.label_end_dt.show()
                self.end_dt.show()
                self.label_effective_dt.hide()
                self.effective_dt.hide()

                # -- setup the connection of promo_name to promo_type, discount_percent
                data = self.sales_data_manager.getPromoTypeAndDiscountPercent(currentText)
                for row in data:
                    self.promo_type.setText(row[0])
                    self.discount_percent.setText(str(row[1]))

                # -- setup the calculation of discount_value
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
            
        if reference == 'inventory_status':
            if currentText == 'Track inventory':
                self.label_on_hand_stock.show()
                self.on_hand_stock.show()
                self.label_available_stock.show()
                self.available_stock.show()
            
            elif currentText == "Don't track inventory":
                self.label_on_hand_stock.hide()
                self.on_hand_stock.hide()
                self.label_available_stock.hide()
                self.available_stock.hide()   

    def onClickedCloseButton(self):
        self.panel_b.hide()
        self.add_button.setDisabled(False)

    def showPanelB(self): # -- PANEL B
        panel = CustomGroupBox(reference='panel_b')
        panel_layout = QFormLayout()

        self.close_button = CustomPushButton(text='BACK')
        self.close_button.setFixedWidth(50)
        self.close_button.clicked.connect(self.onClickedCloseButton)

        self.barcode = CustomLineEdit(reference='barcode')
        self.item_name = CustomComboBox(reference='item_name')
        self.expire_dt = CustomDateEdit()

        self.item_type = CustomComboBox(reference='item_type')
        self.brand = CustomComboBox(reference='brand')
        self.sales_group = CustomComboBox(reference='sales_group')
        self.supplier = CustomComboBox(reference='supplier')

        self.cost = CustomLineEdit(reference='cost')
        self.sell_price = CustomLineEdit(reference='sell_price')
        self.sell_price.textChanged.connect(lambda text: self.handleTextChanged(text, reference='sell_price'))
        self.promo_name = CustomComboBox(reference='promo_name')
        self.promo_name.currentTextChanged.connect(lambda currentText: self.handleCurrentTextChanged(currentText, reference='promo_name'))
        self.label_promo_type = CustomLabel(text='promo_type', reference='promo_type')
        self.promo_type = CustomLineEdit(reference='promo_type')
        self.label_discount_percent = CustomLabel(text='discount_percent', reference='discount_percent')
        self.discount_percent = CustomLineEdit(reference='discount_percent')
        self.label_discount_value = CustomLabel(text='discount_value', reference='discount_value')
        self.discount_value = CustomLineEdit(reference='discount_value')
        self.label_new_sell_price = CustomLabel(text='new_sell_price', reference='new_sell_price')
        self.new_sell_price = CustomLineEdit(reference='new_sell_price')
        self.label_start_dt = CustomLabel(text='start_dt', reference='start_dt')
        self.start_dt = CustomDateEdit(reference='start_dt')
        self.label_end_dt = CustomLabel(text='end_dt', reference='end_dt')
        self.end_dt = CustomDateEdit(reference='end_dt')
        self.label_effective_dt = CustomLabel(text='effective_dt', reference='effective_dt')
        self.effective_dt = CustomDateEdit()

        self.inventory_status = CustomComboBox(reference='inventory_status')
        self.inventory_status.currentTextChanged.connect(lambda currentText: self.handleCurrentTextChanged(currentText, reference='inventory_status'))
        self.label_on_hand_stock = CustomLabel(text='on_hand_stock', reference='on_hand_stock')
        self.on_hand_stock = CustomLineEdit(reference='on_hand_stock')
        self.label_available_stock = CustomLabel(text='available_stock', reference='available_stock')
        self.available_stock = CustomLineEdit(reference='available_stock')

        self.save_button = CustomPushButton(text='SAVE')
        self.save_button.clicked.connect(self.onClickedSaveButton)
        
        panel_layout.addRow(self.close_button)

        panel_layout.addRow('barcode: ', self.barcode)
        panel_layout.addRow('item_name: ', self.item_name)
        panel_layout.addRow('expire_dt: ', self.expire_dt)

        panel_layout.addRow('item_type: ', self.item_type)
        panel_layout.addRow('brand: ', self.brand)
        panel_layout.addRow('sales_group: ', self.sales_group)
        panel_layout.addRow('supplier: ', self.supplier)

        panel_layout.addRow('cost: ', self.cost)
        panel_layout.addRow('sell_price', self.sell_price)
        panel_layout.addRow('promo_name: ', self.promo_name)
        panel_layout.addRow(self.label_promo_type, self.promo_type)
        panel_layout.addRow(self.label_discount_percent, self.discount_percent)
        panel_layout.addRow(self.label_discount_value, self.discount_value)
        panel_layout.addRow(self.label_new_sell_price, self.new_sell_price)
        panel_layout.addRow(self.label_start_dt, self.start_dt)
        panel_layout.addRow(self.label_end_dt, self.end_dt)
        panel_layout.addRow(self.label_effective_dt, self.effective_dt)

        panel_layout.addRow('inventory_status: ', self.inventory_status)
        panel_layout.addRow(self.label_on_hand_stock, self.on_hand_stock)
        panel_layout.addRow(self.label_available_stock, self.available_stock)

        panel_layout.addRow(self.save_button)

        panel.setLayout(panel_layout)

        return panel

    # -------------------------------------------------------- #
    
    def populateTable(self):
        data = self.sales_data_manager.listItem('')

        for row_index, row_data in enumerate(data):
            total_cell = row_data[:11]
            for col_index, col_data in enumerate(total_cell):
                cell = QTableWidgetItem(str(col_data))

                self.list_table.setItem(row_index, col_index + 1, cell)

            self.edit_button = CustomPushButton(text='EDIT')
            self.list_table.setCellWidget(row_index, 0, self.edit_button)

    def onClickedAddButton(self):
        self.panel_b.show()
        self.add_button.setDisabled(True)

    def showPanelA(self): # -- PANEL A
        panel = CustomGroupBox()
        panel_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.add_button = CustomPushButton(text='ADD')
        self.add_button.clicked.connect(self.onClickedAddButton)
        self.list_table = CustomTableWidget(reference='list_table')
        self.populateTable()
        self.data_saved.connect(self.populateTable)

        panel_layout.addWidget(self.filter_bar,0,0)
        panel_layout.addWidget(self.add_button,0,1)
        panel_layout.addWidget(self.list_table,2,0,1,2)

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
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
