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
        if ref == 'cost' or ref == 'sell_price' or ref == 'new_sell_price' or ref == 'discount_percent' or ref == 'on_hand_stock' or ref == 'available_stock':
            self.setText('0')
        if ref == 'new_sell_price' or ref == 'promo_type' or ref == 'discount_percent':
            self.setDisabled(True)

class CustomComboBox(QComboBox):
    def __init__(self, ref=None):
        super().__init__()

        self.callUtils()
        self.setDefaultAttribute(ref)

    def setDefaultAttribute(self, ref):
        if ref == 'item_name' or ref == 'item_type' or ref == 'brand' or ref == 'supplier':
            self.setEditable(True)

        if ref == 'sales_group':
            self.addItem('Retail')
            self.addItem('Wholesale')

        if ref == 'promo_name':
            self.addItem('No promo')
            data = self.database_manager.listPromo()
            for row in data:
                self.addItem(row[0])

        if ref == 'inventory_status':
            self.addItem('Track inventory')
            self.addItem("Don't track inventory")

    def callUtils(self):
        self.database_manager = SalesDatabaseSetup()

class CustomDateEdit(QDateEdit):
    def __init__(self):
        super().__init__()
    
        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

class CustomPushButton(QPushButton):
    def __init__(self, setText=None):
        super().__init__()

        self.setText(setText)
        
class CustomTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setDefaultAttribute()

    def setDefaultAttribute(self):
        self.setColumnCount(12)
        self.setRowCount(50)

        self.setHorizontalHeaderLabels(['','barcode','item_name','expire_dt','item_type','brand','sales_group','supplier','cost','sell_price','discount_value','effective_dt'])


# -- for layouts
class ManageItemForm(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.callClass()
        self.setMainLayout()
        self.setWidgetSignal()
        self.setCurrentValues()

    def onClickedSaveButton(self):
        # -- step a: set datatypes to inputs
        converted_barcode = str(self.barcode.text())
        converted_item_name = str(self.item_name.currentText())
        converted_expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)

        converted_item_type = str(self.item_type.currentText())
        converted_brand = str(self.brand.currentText())
        converted_sales_group = str(self.sales_group.currentText())
        converted_supplier = str(self.supplier.currentText())

        converted_cost = str('{:.2f}'.format(float(self.cost.text())))
        converted_sell_price = str('{:.2f}'.format(float(self.sell_price.text())))
        converted_effective_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate)
        converted_promo_name = str(self.promo_name.currentText())
        converted_inventory_status = str(self.inventory_status.currentText())

        converted_new_sell_price = str('{:.2f}'.format(float(self.new_sell_price.text())))
        converted_promo_type = str(self.promo_type.text())
        converted_discount_percent = str('{:.2f}'.format(float(self.discount_percent.text())))
        converted_discount_value = str('{:.2f}'.format(float(self.discount_value.text())))
        converted_start_dt = self.start_dt.date().toString(Qt.DateFormat.ISODate)
        converted_end_dt = self.end_dt.date().toString(Qt.DateFormat.ISODate)

        converted_on_hand_stock = str(int(self.on_hand_stock.text()))
        converted_available_stock = str(int(self.available_stock.text()))

        self.database_manager.addNewItem(
            converted_barcode,
            converted_item_name,
            converted_expire_dt,
            converted_item_type,
            converted_brand,
            converted_sales_group,
            converted_supplier,
            converted_cost,
            converted_sell_price,
            converted_effective_dt,
            promo_name=converted_promo_name,
            inventory_status=converted_inventory_status,
            new_sell_price=converted_new_sell_price,
            promo_type=converted_promo_type,
            discount_percent=converted_discount_percent,
            discount_value=converted_discount_value,
            start_dt=converted_start_dt,
            end_dt=converted_end_dt,
            on_hand_stock=converted_on_hand_stock,
            available_stock=converted_available_stock
        )

        self.data_saved.emit()

    def onCurrentTextChangedInventoryStatus(self, text):
        if text == "Don't track inventory":
            self.label_on_hand_stock.hide()
            self.on_hand_stock.hide()
            self.label_available_stock.hide()
            self.available_stock.hide()
        elif text == "Track inventory":
            self.label_on_hand_stock.show()
            self.on_hand_stock.show()
            self.label_available_stock.show()
            self.available_stock.show()

    def onCurrentTextChangedPromoName(self, text):
        if text == 'No promo':
            self.label_sell_price.show()
            self.sell_price.show()
            self.label_new_sell_price.hide()
            self.new_sell_price.hide()
            self.label_promo_type.hide()
            self.promo_type.hide()
            self.label_discount_percent.hide()
            self.discount_percent.hide()
            self.label_start_dt.hide()
            self.start_dt.hide()
            self.label_end_dt.hide()
            self.end_dt.hide()
            self.label_effective_dt.show()
            self.effective_dt.show()

        else:
            self.label_sell_price.hide()
            self.sell_price.hide()
            self.label_new_sell_price.show()
            self.new_sell_price.show()
            self.label_promo_type.show()
            self.promo_type.show()
            self.label_discount_percent.show()
            self.discount_percent.show()
            self.label_start_dt.show()
            self.start_dt.show()
            self.label_end_dt.show()
            self.end_dt.show()
            self.label_effective_dt.hide()
            self.effective_dt.hide()
            data = self.database_manager.getPromoTypeAndDiscountValue(text)
            for row in data:
                self.promo_type.setText(row[0])
                self.discount_percent.setText(str(row[1]))

            try:
                converted_sell_price = float(self.sell_price.text())
                converted_discount_percent = float(self.discount_percent.text())

                old_sell_price = converted_sell_price
                discount_amount = old_sell_price * (converted_discount_percent / 100)

                print('(ADD ITEM) OLD SELL PRICE', old_sell_price)
                
                new_sell_price = converted_sell_price - discount_amount

                self.discount_value.setText(f'{discount_amount:.2f}')
                self.new_sell_price.setText(f'{new_sell_price:.2f}')
            except ValueError:
                pass
            
    
    def onTextChangedSellPrice(self, text):
        if text == '':
            self.promo_name.setDisabled(True)
        else:
            self.promo_name.setDisabled(False)
    
    def setWidgetSignal(self):
        self.sell_price.textChanged.connect(self.onTextChangedSellPrice)
        self.promo_name.currentTextChanged.connect(self.onCurrentTextChangedPromoName)
        self.inventory_status.currentTextChanged.connect(self.onCurrentTextChangedInventoryStatus)
        self.save_button.clicked.connect(self.onClickedSaveButton)

    def setCurrentValues(self, mode=None, row_index=None, row_value=None):
        self.promo_name.setCurrentText('No promo')
        self.inventory_status.setCurrentText("Don't track inventory")

        self.onTextChangedSellPrice('')
        self.onCurrentTextChangedPromoName('No promo')
        self.onCurrentTextChangedInventoryStatus("Don't track inventory")

        data = row_value
        print(data)
        if data is not None and mode == 'edit_mode':
            self.barcode.setText(data[0])
            self.item_name.setCurrentText(data[1])
            self.expire_dt.setDate(QDate.fromString(data[2], Qt.DateFormat.ISODate))
            self.item_type.setCurrentText(data[3])
            self.brand.setCurrentText(data[4])
            self.sales_group.setCurrentText(data[5])
            self.supplier.setCurrentText(data[6])
            self.cost.setText(str(data[7]))

            
            self.sell_price.setText(str(data[8]))
            # self.new_sell_price
            retrieved_promo_name = self.database_manager.getPromoNameById(str(data[13]))
            print('promo id: ', data[13], ' promo name: ', retrieved_promo_name)
            self.promo_name.setCurrentText(retrieved_promo_name)

            # self.promo_type
            self.discount_value.setText(str(data[9]))
            # self.start_dt
            # self.end_dt
            self.effective_dt.setDate(QDate.fromString(data[10], Qt.DateFormat.ISODate))
            # self.inventory_status
            # self.on_hand_stock
            # self.available_stock
            self.item_id = data[11]
            self.item_price_id = data[12]
            # self.promo_id = data[13]


            self.item_type.setDisabled(True)
            self.brand.setDisabled(True)
            self.sales_group.setDisabled(True)
            self.supplier.setDisabled(True)

    def setMainLayout(self):
        self.grid_layout = QFormLayout()

        self.barcode = CustomLineEdit()
        self.item_name = CustomComboBox(ref='item_name')
        self.expire_dt = CustomDateEdit()

        self.item_type = CustomComboBox(ref='item_type')
        self.brand = CustomComboBox(ref='brand')
        self.sales_group = CustomComboBox(ref='sales_group')
        self.supplier = CustomComboBox(ref='supplier')

        self.cost = CustomLineEdit(ref='cost')
        self.sell_price = CustomLineEdit(ref='sell_price')
        self.new_sell_price = CustomLineEdit(ref='new_sell_price')
        self.promo_name = CustomComboBox(ref='promo_name')
        self.promo_type = CustomLineEdit(ref='promo_type')

        self.discount_percent = CustomLineEdit(ref='discount_percent')
        self.discount_value = CustomLineEdit()
        self.start_dt = CustomDateEdit()
        self.end_dt = CustomDateEdit()
        self.effective_dt = CustomDateEdit()

        self.inventory_status = CustomComboBox(ref='inventory_status')
        self.on_hand_stock = CustomLineEdit(ref='on_hand_stock')
        self.available_stock = CustomLineEdit(ref='available_stock')

        self.save_button = CustomPushButton(setText='SAVE')


        # labels
        self.label_sell_price = QLabel('sell_price: ')
        self.label_new_sell_price = QLabel('new_sell_price: ')
        self.label_promo_type = QLabel('promo_type: ')
        self.label_discount_percent = QLabel('discount_percent: ')
        self.label_start_dt = QLabel('start_dt: ')
        self.label_end_dt = QLabel('end_dt: ')
        self.label_effective_dt = QLabel('effective_dt: ')

        self.label_on_hand_stock = QLabel('on_hand_stock: ')
        self.label_available_stock = QLabel('available_stock: ')

        self.setCurrentValues()

        self.grid_layout.addRow('barcode: ', self.barcode)
        self.grid_layout.addRow('item_name: ', self.item_name)
        self.grid_layout.addRow('expire_dt: ', self.expire_dt)

        self.grid_layout.addRow('item_type: ', self.item_type)
        self.grid_layout.addRow('brand: ', self.brand)
        self.grid_layout.addRow('sales_group: ', self.sales_group)
        self.grid_layout.addRow('supplier: ', self.supplier)

        self.grid_layout.addRow('cost: ', self.cost)
        self.grid_layout.addRow(self.label_sell_price, self.sell_price)
        self.grid_layout.addRow(self.label_new_sell_price, self.new_sell_price)
        self.grid_layout.addRow('promo_name: ', self.promo_name)
        self.grid_layout.addRow(self.label_promo_type, self.promo_type)
        self.grid_layout.addRow(self.label_discount_percent, self.discount_percent)
        self.grid_layout.addRow(self.label_start_dt, self.start_dt)
        self.grid_layout.addRow(self.label_end_dt, self.end_dt)
        self.grid_layout.addRow(self.label_effective_dt, self.effective_dt)

        self.grid_layout.addRow('inventory_status: ', self.inventory_status)
        self.grid_layout.addRow(self.label_on_hand_stock, self.on_hand_stock)
        self.grid_layout.addRow(self.label_available_stock, self.available_stock)

        self.grid_layout.addRow(self.save_button)

        self.setLayout(self.grid_layout)

    def callClass(self):
        self.database_manager = SalesDatabaseSetup()


class ItemManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.callClass()
        self.setMainLayout()
        self.setWidgetSignal()
        self.setCurrentValues()

    def onTextChangedFilterBar(self):
        pass
    
    def onClickedCloseButton(self):
        self.manage_item_form.hide()
        self.close_button.hide()
        self.add_button.show()
        pass

    def onClickedAddButton(self, mode):
        self.manage_item_form.setCurrentValues(mode=mode)
        self.manage_item_form.show()
        self.close_button.show()
        self.add_button.hide()
        self.manage_item_form.data_saved.connect(self.fillItemListTable)
        pass

    def onClickedEditButton(self, mode, row_index, row_value):
        self.manage_item_form.setCurrentValues(mode=mode, row_value=row_value)
        self.manage_item_form.show()
        self.close_button.show()
        self.add_button.hide()
        self.manage_item_form.data_saved.connect(self.fillItemListTable)
        pass

    def fillItemListTable(self):
        data = self.database_manager.listItem('')

        for row_index, row_value in enumerate(data):
            total_cell = row_value[:11]
            for col_index, col_value in enumerate(total_cell):
                cell = QTableWidgetItem(str(col_value))
                self.item_list_table.setItem(row_index, col_index + 1, cell)

                if row_value[13] != 0:
                    cell.setForeground(QColor(255, 0, 0))

            self.edit_button = CustomPushButton(setText='EDIT')
            self.item_list_table.setCellWidget(row_index, 0, self.edit_button)
            self.edit_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.onClickedEditButton('edit_mode', row_index, row_value))

    def setWidgetSignal(self):
        pass
    def setCurrentValues(self):
        self.manage_item_form.hide()
        self.close_button.hide()
        self.fillItemListTable()

    def setMainLayout(self):
        self.grid_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.add_button = CustomPushButton(setText='ADD')
        self.add_button.clicked.connect(lambda: self.onClickedAddButton('add_mode'))
        self.close_button = CustomPushButton(setText='CLOSE')
        self.close_button.clicked.connect(self.onClickedCloseButton)
        self.item_list_table = CustomTableWidget()
        self.manage_item_form = ManageItemForm() # -- for adding and editing items

        self.grid_layout.addWidget(self.filter_bar,0,0)
        self.grid_layout.addWidget(self.add_button,0,1)
        self.grid_layout.addWidget(self.close_button,0,1)
        self.grid_layout.addWidget(self.item_list_table,1,0,1,2)
        self.grid_layout.addWidget(self.manage_item_form,0,2,2,2)


        self.setLayout(self.grid_layout)

    def callClass(self):
        self.database_manager = SalesDatabaseSetup()
        self.database_manager.createSalesTable() # -- for temporary use only     

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
