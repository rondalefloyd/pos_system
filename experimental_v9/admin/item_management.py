import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.item_management_sql import *
from utils.inventory_management_sql import *
from utils.promo_management_sql import *

class CustomLineEdit(QLineEdit):
    def __init__(self, ref=None):
        super().__init__()
        
        self.setCurrentAttribute(ref)

    def callUtils(self):
        self.manage_item_form = CustomGroupBox()

    def setCurrentAttribute(self, ref=None):
        if ref == 'promo_type': 
            self.setDisabled(True)

class CustomComboBox(QComboBox):
    def __init__(self, ref=None):
        super().__init__()

        self.callUtils()
        self.setCurrentAttribute(ref)

    def callUtils(self):
        self.promo_management_sql = PromoManagementSQL()

    def setCurrentAttribute(self, ref=None):
        if ref == 'item_name' or ref == 'item_type' or ref == 'brand' or ref == 'supplier':
            self.setEditable(True)

        if ref == 'sales_group':
            self.addItem('Retail')
            self.addItem('Wholesale')

        if ref == 'promo':
            self.addItem('No promo')
            promo = self.promo_management_sql.listPromo()
            for row in promo:
                self.addItem(row[0])

        if ref == 'inventory_status':
            self.addItem("Track inventory")
            self.addItem("Don't track inventory")
            self.setCurrentText("Don't track inventory")

class CustomDateEdit(QDateEdit):
    def __init__(self, ref=None):
        super().__init__()

        self.setDefaultAttribute()
        self.setCurrentAttribute(ref)

    def setDefaultAttribute(self):
        self.setCalendarPopup(True)

    def setCurrentAttribute(self, ref=None):
        if ref == 'expire_dt' or ref == 'start_dt' or ref == 'end_dt' or ref == 'effective_dt':
            self.setMinimumDate(QDate.currentDate())

        # if ref == 'end_dt':
        #     self.date().addDays(+1)

class CustomPushButton(QPushButton):
    def __init__(self, ref=None, text=None):
        super().__init__()

        self.setDefaultAttribute(text)

    def setDefaultAttribute(self, text=None):
        self.setText(text)
        
class CustomTableWidget(QTableWidget):
    def __init__(self, ref=None):
        super().__init__()

        self.callUtils()
        self.setMainLayout()

    def callUtils(self):
        self.item_management_sql = ItemManagementSQL()

    def fillTable(self):
        item = self.item_management_sql.listItem('')

        self.setRowCount(50)

        for row_index, row_value in enumerate(item):
            total_cell = row_value[:11]

            for col_index, col_value in enumerate(total_cell):
                item = QTableWidgetItem(str(col_value))

                self.setItem(row_index, col_index + 1, item)

                if row_value[11] != 0:
                    item.setForeground(QColor(255, 0, 0))

            self.edit_button = CustomPushButton(text='EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)
                                        
    def setCurrentAttribute(self):
        self.setColumnCount(12)
        self.setHorizontalHeaderLabels(['','barcode','item_name','expire_dt','item_type','brand','sales_group','supplier','cost','sell_price','discount_value','effective_dt'])

    def setMainLayout(self):
        self.setCurrentAttribute()

class CustomGroupBox(QGroupBox):
    data_saved = pyqtSignal()
    def __init__(self, ref=None):
        super().__init__()

        self.callUtils()
        self.setMainLayout()
        self.setWidgetSignal()
        self.setCurrentAttribute()
        self.setDefaultAttribute()

    def callUtils(self):
        self.item_management_sql = ItemManagementSQL()
        self.promo_management_sql = PromoManagementSQL()

    def onSaveButton(self):
        # STEP A -- convert input
        converted_barcode = str(self.barcode.text())
        converted_item_name = str(self.item_name.currentText())
        converted_expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)

        converted_item_type = str(self.item_type.currentText())
        converted_brand = str(self.brand.currentText())
        converted_sales_group = str(self.sales_group.currentText())
        converted_supplier = str(self.supplier.currentText())

        converted_cost = str('{:.2f}'.format(float(self.cost.text())))
        converted_sell_price = str('{:.2f}'.format(float(self.sell_price.text())))
        converted_promo = str(self.promo.currentText())
        converted_effective_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate)

        if converted_promo != 'No promo':
            converted_new_sell_price = str('{:.2f}'.format(float(self.new_sell_price.text())))
            converted_promo_type = str(self.promo_type.text())
            converted_discount_value = str('{:.2f}'.format(float(self.discount_value.text())))
            converted_start_dt = self.start_dt.date().toString(Qt.DateFormat.ISODate)

            # adds +1 day
            end_dt = self.end_dt.date()
            new_end_dt = end_dt.addDays(1)
            converted_end_dt = new_end_dt.toString(Qt.DateFormat.ISODate)
        else:
            pass

        converted_inventory_status = str(self.inventory_status.currentText())

        if converted_inventory_status == 'Track inventory':
            converted_on_hand_stock = str(self.on_hand_stock.text())
            converted_available_stock = str(self.available_stock.text())
        else:
            pass

        # STEP B
        if converted_promo == 'No promo':
            self.item_management_sql.addItem(
                converted_item_type,
                converted_brand,
                converted_sales_group,
                converted_supplier,
                converted_barcode,
                converted_item_name,
                converted_expire_dt,
                converted_cost,
                converted_sell_price,
                converted_promo,
                converted_effective_dt
            )
        else:
            self.item_management_sql.addItem(
                converted_item_type,
                converted_brand,
                converted_sales_group,
                converted_supplier,
                converted_barcode,
                converted_item_name,
                converted_expire_dt,
                converted_cost,
                converted_sell_price,
                converted_promo,
                converted_effective_dt,
                converted_new_sell_price,
                converted_promo_type,
                converted_discount_value,
                converted_start_dt,
                converted_end_dt,
                converted_inventory_status,
                converted_on_hand_stock,
                converted_available_stock
            )
        
        self.data_saved.emit()

        QMessageBox.information(self, "Success", "New promo has been added!")
        # STEP C -- OPTIONAL

    def onTextChangedSellPrice(self, text):
        if text == '':
            self.promo.setDisabled(True)
        else:
            self.promo.setDisabled(False)

    def onCurrentTextChangedPromo(self, text):
        if text == 'No promo':
            self.label_sell_price.show()
            self.newisplay_sell_price.hide()
            self.label_promo_type.hide()
            self.label_discount_value.hide()
            self.label_start_dt.hide()
            self.label_end_dt.hide()
            self.label_effective_dt.show()
            self.sell_price.show()
            self.new_sell_price.hide()
            self.promo_type.hide()
            self.discount_value.hide()
            self.start_dt.hide()
            self.end_dt.hide()
            self.effective_dt.show()
        else:
            self.label_sell_price.hide()
            self.newisplay_sell_price.show()
            self.label_promo_type.show()
            self.label_start_dt.show()
            self.label_end_dt.show()
            self.label_effective_dt.hide()
            self.sell_price.hide()
            self.new_sell_price.show()
            self.new_sell_price.setDisabled(True)
            self.promo_type.show()
            self.discount_value.setDisabled(True)
            self.start_dt.show()
            self.end_dt.show()
            self.effective_dt.hide()

            data = self.promo_management_sql.getPromoTypeAndDiscountValue(text)
            for row in data:
                print(row[0])
                self.promo_type.setText(row[0])
                self.discount_value.setText(str(row[1]))
            try:
                converted_sell_price = float(self.sell_price.text())
                converted_discount_value = float(self.discount_value.text())
                old_sell_price = converted_sell_price
                discount_amount = old_sell_price * (converted_discount_value / 100)
                new_sell_price = converted_sell_price - discount_amount
                self.new_sell_price.setText(f'{new_sell_price:.2f}')
            except ValueError:
                pass
    
    def onCurrentTextChangedInventoryStatus(self, text):
        if text == "Track inventory":
            self.label_on_hand_stock.show()
            self.label_available_stock.show()
            self.on_hand_stock.show()
            self.available_stock.show()
        else:
            self.label_on_hand_stock.hide()
            self.label_available_stock.hide()
            self.on_hand_stock.hide()
            self.available_stock.hide()

    def setCurrentAttribute(self):
        pass

    def setDefaultAttribute(self):
        self.setFixedWidth(400)
        self.onCurrentTextChangedPromo('No promo')
        self.onTextChangedSellPrice('')
        self.onCurrentTextChangedInventoryStatus("Don't track inventory")

    def setWidgetSignal(self):
        self.sell_price.textChanged.connect(self.onTextChangedSellPrice)
        self.promo.currentTextChanged.connect(self.onCurrentTextChangedPromo)
        self.inventory_status.currentTextChanged.connect(self.onCurrentTextChangedInventoryStatus)
        self.save_button.clicked.connect(self.onSaveButton)

    def setMainLayout(self):
        self.main_layout = QFormLayout()
    
        self.barcode = CustomLineEdit()
        self.item_name = CustomComboBox(ref='item_name')
        self.expire_dt = CustomDateEdit(ref='expire_dt')

        self.item_type = CustomComboBox(ref='item_type')
        self.brand = CustomComboBox(ref='brand')
        self.sales_group = CustomComboBox(ref='sales_group')
        self.supplier = CustomComboBox(ref='supplier')

        self.cost = CustomLineEdit()
        self.sell_price = CustomLineEdit()
        self.new_sell_price = CustomLineEdit()
        self.promo = CustomComboBox(ref='promo')
        self.promo_type = CustomLineEdit(ref='promo_type')
        self.discount_value = CustomLineEdit(ref='discount_value')
        self.start_dt = CustomDateEdit(ref='start_dt')
        self.end_dt = CustomDateEdit(ref='end_dt')
        self.effective_dt = CustomDateEdit(ref='effective_dt')

        self.inventory_status = CustomComboBox(ref='inventory_status') # not included in sql
        self.on_hand_stock = CustomLineEdit()
        self.available_stock = CustomLineEdit()

        self.save_button = CustomPushButton(text='SAVE')
        
        # -- labelszxc
        self.label_sell_price = QLabel('sell_price')
        self.newisplay_sell_price = QLabel('new_sell_price')
        self.label_promo_type = QLabel('promo_type')
        self.label_discount_value = QLabel('promo_type')
        self.label_start_dt = QLabel('start_dt')
        self.label_end_dt = QLabel('end_dt')
        self.label_effective_dt = QLabel('effective_dt')
        
        self.label_on_hand_stock = QLabel('on_hand_stock')
        self.label_available_stock = QLabel('available_stock')

        self.setCurrentAttribute()
        
        self.main_layout.addRow('barcode: ', self.barcode)
        self.main_layout.addRow('item_name: ', self.item_name)
        self.main_layout.addRow('expire_dt: ', self.expire_dt)
        
        self.main_layout.addRow('item_type: ', self.item_type)
        self.main_layout.addRow('brand: ', self.brand)
        self.main_layout.addRow('sales_group: ', self.sales_group)
        self.main_layout.addRow('supplier: ', self.supplier)

        self.main_layout.addRow('cost: ', self.cost)
        self.main_layout.addRow(self.label_sell_price, self.sell_price)
        self.main_layout.addRow(self.newisplay_sell_price, self.new_sell_price)
        self.main_layout.addRow('promo: ', self.promo)
        self.main_layout.addRow(self.label_promo_type, self.promo_type)
        self.main_layout.addRow(self.label_discount_value, self.discount_value)
        self.main_layout.addRow(self.label_start_dt, self.start_dt)
        self.main_layout.addRow(self.label_end_dt, self.end_dt)
        self.main_layout.addRow(self.label_effective_dt, self.effective_dt)

        self.main_layout.addRow('inventory_status: ', self.inventory_status)
        self.main_layout.addRow(self.label_on_hand_stock, self.on_hand_stock)
        self.main_layout.addRow(self.label_available_stock, self.available_stock)

        self.main_layout.addRow(self.save_button)

        self.setLayout(self.main_layout)

class ItemManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.callUtils()
        self.setMainLayout()
        self.setDefaultAttribute()

    def callUtils(self):
        self.item_management_sql = ItemManagementSQL()

    def onClickedAddButton(self):
        self.manage_item_form.show()
        self.add_button.hide()
        self.close_button.show()
        self.manage_item_form.data_saved.connect(self.list_item_table.fillTable)
    
    def onClickedCloseButton(self):
        self.manage_item_form.hide()
        self.add_button.show()
        self.close_button.hide()

    def setWidgetSignal(self):
        self.add_button.clicked.connect(self.onClickedAddButton)
        self.close_button.clicked.connect(self.onClickedCloseButton)

    def setDefaultAttribute(self):
        self.manage_item_form.hide()
        self.close_button.hide()
        self.list_item_table.fillTable()

    def setMainLayout(self):
        self.item_management_sql.createItemManagementTable()

        self.main_layout = QGridLayout()

        self.filter_bar = CustomLineEdit()
        self.add_button = CustomPushButton(text='ADD')
        self.close_button = CustomPushButton(text='CLOSE')
        self.list_item_table = CustomTableWidget()
        self.manage_item_form = CustomGroupBox()

        self.setWidgetSignal() # -- SIGNALS FOR WIDGET

        self.main_layout.addWidget(self.filter_bar,0,0)
        self.main_layout.addWidget(self.add_button,0,1)
        self.main_layout.addWidget(self.close_button,0,1)
        self.main_layout.addWidget(self.list_item_table,2,0,1,2)
        self.main_layout.addWidget(self.manage_item_form,0,3,3,1)

        self.setLayout(self.main_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
