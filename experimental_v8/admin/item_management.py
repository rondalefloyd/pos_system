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

class GlobalWidget():
    def customLabel(self, text):
        label = QLabel(text)
        return label
    def customLineEdit(self, manage_item_mode, ref):
        line_edit = QLineEdit()
        if ref == 'discount':
            line_edit.setDisabled(True)
        if ref == 'promo_type':
            line_edit.setDisabled(True)
        return line_edit
    def customComboBox(self, manage_item_mode, ref):
        combo_box = QComboBox()
        if ref == 'item_name' or ref == 'item_type' or ref == 'brand' or ref == 'supplier':
            combo_box.setEditable(True)
        if ref == 'sales_group':
            combo_box.addItem('Retail')
            combo_box.addItem('Wholesale')
        if ref == 'promo':
            combo_box.insertItem(0,'No promo')
            combo_box.setCurrentIndex(0)
        if ref == 'inventory_status':
            combo_box.insertItem(0,"Track inventory for this item")
            combo_box.insertItem(1,"Don't track inventory for this item")
            combo_box.setCurrentIndex(0)
        
        if manage_item_mode == 'edit_item':
            if ref == 'item_type' or ref == 'brand' or ref == 'brand' or ref == 'supplier':
                combo_box.setDisabled(True)

        return combo_box
    def customDateEdit(self, manage_item_mode, ref):
        date_edit = QDateEdit()
        date_edit.setMinimumDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        return date_edit
    def customPushButton(self, text):
        push_button = QPushButton(text)
        return push_button

class ManageItemDialog(QDialog):
    def __init__(self, manage_item_mode, row_value=None):
        super().__init__()

        self.callClass()
        self.setMainLayout(manage_item_mode)
        self.setWidgetSignal(manage_item_mode)
        self.setCurrentAttributes(row_value)
        self.setDefaultAttributes()
    
    def callClass(self):
        self.global_widget = GlobalWidget()
        self.item_management_sql = ItemManagementSQL()
        self.inventory_management_sql = InventoryManagementSQL()
        self.promo_management_sql = PromoManagementSQL()

    def onSaveItemButton(self, manage_item_mode):
        # convert input
        converted_barcode = str(self.barcode.text())
        converted_item_name = str(self.item_name.currentText())
        converted_expire_dt = self.expire_dt.date().toString(Qt.DateFormat.ISODate)

        converted_item_type = str(self.item_type.currentText())
        converted_brand = str(self.brand.currentText())
        converted_sales_group = str(self.sales_group.currentText())
        converted_supplier = str(self.supplier.currentText())

        converted_cost = str('{:.2f}'.format(float(self.cost.text())))
        converted_promo = str(self.promo.currentText())
        converted_discount = str('{:.2f}'.format(float(self.discount.text())))
        converted_sell_price = str('{:.2f}'.format(float(self.sell_price.text())))
        converted_promo = str(self.promo.currentText())
        converted_promo_type = str(self.promo_type.text())
        converted_promo_start_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate) # -- same with effective dt
        converted_promo_end_dt = self.promo_end_dt.date().toString(Qt.DateFormat.ISODate)
        converted_effective_dt = self.effective_dt.date().toString(Qt.DateFormat.ISODate)

        converted_inventory_status = str(self.inventory_status.currentText())

        if manage_item_mode == 'add_item':
            # step a
            self.item_management_sql.insertItemTypeData(converted_item_type)
            self.item_management_sql.insertBrandData(converted_brand)
            self.item_management_sql.insertSalesGroupData(converted_sales_group)
            self.item_management_sql.insertSupplierData(converted_supplier)

            # step b
            retrieved_item_type_id = self.item_management_sql.selectItemTypeId(converted_item_type)
            retrieved_brand_id = self.item_management_sql.selectBrandId(converted_brand)
            retrieved_sales_group_id = self.item_management_sql.selectSalesGroupId(converted_sales_group)
            retrieved_supplier_id = self.item_management_sql.selectSupplierId(converted_supplier)

            self.item_management_sql.insertItemData(converted_barcode, converted_item_name, converted_expire_dt, retrieved_item_type_id, retrieved_brand_id, retrieved_sales_group_id, retrieved_supplier_id)

            retrieved_item_id = self.item_management_sql.selectItemId(converted_barcode, converted_item_name, converted_expire_dt, retrieved_item_type_id, retrieved_brand_id, retrieved_sales_group_id, retrieved_supplier_id)
            # step c
            if converted_promo == 'No promo':

                self.item_management_sql.insertItemPriceData(retrieved_item_id, converted_cost, converted_discount, converted_sell_price, converted_effective_dt)
            else:
                retrieved_promo_id = self.promo_management_sql.selectPromoId(converted_promo, converted_promo_type)
                print('WITH PROMO!', retrieved_promo_id)

                self.item_management_sql.insertItemPromoPriceData(retrieved_item_id, retrieved_promo_id, converted_cost, converted_discount, converted_sell_price, converted_promo_start_dt)
                pass
            
            if converted_inventory_status == "Don't track inventory for this item":
                pass
            else:
                converted_on_hand_stock = int(self.on_hand_stock.text())
                converted_available_stock = int(self.available_stock.text())
                self.inventory_management_sql.insertStockData(retrieved_supplier_id, retrieved_item_id, converted_on_hand_stock, converted_available_stock)

            QMessageBox.information(self, "Success", "New item has been added!")
              
        elif manage_item_mode == 'edit_item':
            # step a
            pass
        
    def onClickedPromo(self, index):
        if index == 0:
            self.promo_type.hide()
            self.promo_start_dt.hide()
            self.promo_end_dt.hide()
            self.effective_dt.show()
            self.label_promo_type.hide()
            self.label_promo_start_dt.hide()
            self.label_promo_end_dt.hide()
            self.label_effective_dt.show()
        else:
            self.promo_type.show()
            self.promo_start_dt.show()
            self.promo_end_dt.show()
            self.effective_dt.hide()
            self.label_promo_type.show()
            self.label_promo_start_dt.show()
            self.label_promo_end_dt.show()
            self.label_effective_dt.hide()

    def onClickedInventoryStatus(self, index):
        if index == 0:
            self.on_hand_stock.show()
            self.available_stock.show()
            self.label_on_hand_stock.show()
            self.label_available_stock.show()
        else:
            self.on_hand_stock.hide()
            self.available_stock.hide()
            self.label_on_hand_stock.hide()
            self.label_available_stock.hide()

    def onCurrentTextChangedPromoType(self, text):
        converted_promo = str(text.currentText())

        converted_promo_type = self.item_management_sql.selectPromoTypeDataByName(converted_promo)

        self.promo_type.setText(converted_promo_type)

        print(converted_promo_type)

    def fillAllItemDataComboBox(self):
        item_name = self.item_management_sql.selectItemData()
        item_type = self.item_management_sql.selectItemTypeData()
        brand = self.item_management_sql.selectBrandData()
        sales_group = self.item_management_sql.selectSalesGroupData()
        supplier = self.item_management_sql.selectSupplierData()
        promo = self.promo_management_sql.selectPromoData()

        self.item_name.addItems([row for row in item_name])
        self.item_type.addItems([row for row in item_type])
        self.brand.addItems([row for row in brand])
        self.sales_group.addItems([row for row in sales_group])
        self.supplier.addItems([row for row in supplier])
        self.promo.addItems([row for row in promo])

    def calculateDiscount(self):
        try:
            converted_cost = float(self.cost.text())
            converted_discount = float(self.discount.text())

            discount_amount = converted_cost * (converted_discount / 100)
            converted_sell_price = converted_cost - discount_amount

            self.sell_price.setText(f'{converted_sell_price:.2f}')
        except ValueError:
            self.sell_price.setText('Error')

    def setWidgetSignal(self, manage_item_mode):
        self.promo.currentIndexChanged.connect(self.onClickedPromo)

        self.cost.textChanged.connect(self.calculateDiscount)
        self.discount.textChanged.connect(self.calculateDiscount)

        self.promo.currentTextChanged.connect(lambda: self.onCurrentTextChangedPromoType(self.promo))

        self.inventory_status.currentIndexChanged.connect(self.onClickedInventoryStatus)
        self.save_item_button.clicked.connect(lambda: self.onSaveItemButton(manage_item_mode))

    def setCurrentAttributes(self, row_value):
        pass
        # self.barcode.setText(row_value[0])
        # self.item_name.setCurrentText(row_value[1])
        # self.expire_dt.setDate(row_value[2])

        # self.item_type.setCurrentText(row_value[3])
        # self.brand.setCurrentText(row_value[4])
        # self.sales_group.setCurrentText(row_value[5])
        # self.supplier.setCurrentText(row_value[6])
        
        # self.cost.setText(row_value[7])
        # self.promo_type.setText(row_value[8])
        # if self.promo_type.text() != '':
        #     pass
        #     # self.promo.setCurrentText(row_value[8])
        # self.discount.setText(row_value[9])
        # self.sell_price.setText(row_value[10])
        # self.promo_start_dt.setDate(row_value[11])
        # self.promo_end_dt.setDate(row_value[12])
        # self.effective_dt.setDate(row_value[13])

        # self.on_hand_stock.setText(row_value[14])
        # self.available_stock.setText(row_value[15])
        # # self.inventory_status.setCurrentText(row_value[15])

    def setDefaultAttributes(self):
        self.item_management_sql.createAllItemTable()
        self.inventory_management_sql.createStockTable()
        self.promo_management_sql.createPromoTable()

        self.cost.setText('0')
        self.discount.setText('0')
        self.sell_price.setText('0')
        self.on_hand_stock.setText('0')
        self.available_stock.setText('0')

        self.onClickedPromo(0)
        self.fillAllItemDataComboBox()
    
    def setMainLayout(self, manage_item_mode):
        self.main_layout = QFormLayout()

        self.barcode = self.global_widget.customLineEdit(manage_item_mode, ref='barcode')
        self.item_name = self.global_widget.customComboBox(manage_item_mode, ref='item_name')
        self.expire_dt = self.global_widget.customDateEdit(manage_item_mode, ref='expire_dt')

        self.item_type = self.global_widget.customComboBox(manage_item_mode, ref='item_type')
        self.brand = self.global_widget.customComboBox(manage_item_mode, ref='brand')
        self.sales_group = self.global_widget.customComboBox(manage_item_mode, ref='sales_group')
        self.supplier = self.global_widget.customComboBox(manage_item_mode, ref='supplier')
        
        self.cost = self.global_widget.customLineEdit(manage_item_mode, ref='cost')
        self.sell_price = self.global_widget.customLineEdit(manage_item_mode, ref='sell_price')
        self.promo = self.global_widget.customComboBox(manage_item_mode, ref='promo')
        self.promo_type = self.global_widget.customLineEdit(manage_item_mode, ref='promo_type')
        self.discount = self.global_widget.customLineEdit(manage_item_mode, ref='discount')
        self.promo_start_dt = self.global_widget.customDateEdit(manage_item_mode, ref='promo_start_dt')
        self.promo_end_dt = self.global_widget.customDateEdit(manage_item_mode, ref='promo_end_dt')
        self.effective_dt = self.global_widget.customDateEdit(manage_item_mode, ref='effective_dt')

        self.inventory_status = self.global_widget.customComboBox(manage_item_mode, ref='inventory_status')
        self.on_hand_stock = self.global_widget.customLineEdit(manage_item_mode, ref='on_hand_stock')
        self.available_stock = self.global_widget.customLineEdit(manage_item_mode, ref='available_stock')

        self.save_item_button = self.global_widget.customPushButton('SAVE')

        # labels
        self.label_promo = self.global_widget.customLabel('promo: ')
        self.label_promo_type = self.global_widget.customLabel('promo_type: ')
        self.label_promo_start_dt = self.global_widget.customLabel('promo_start_dt: ')
        self.label_promo_end_dt = self.global_widget.customLabel('promo_end_dt: ')
        self.label_effective_dt = self.global_widget.customLabel('effective_dt: ')

        self.label_on_hand_stock = self.global_widget.customLabel('on_hand_stock: ') 
        self.label_available_stock = self.global_widget.customLabel('available_stock: ') 

        # add widget
        self.main_layout.addRow('barcode: ', self.barcode)
        self.main_layout.addRow('item_name: ', self.item_name)
        self.main_layout.addRow('expire_dt: ', self.expire_dt)

        self.main_layout.addRow('item_type: ', self.item_type)
        self.main_layout.addRow('brand: ', self.brand)
        self.main_layout.addRow('sales_group: ', self.sales_group)
        self.main_layout.addRow('supplier: ', self.supplier)

        self.main_layout.addRow('cost: ', self.cost)
        self.main_layout.addRow('sell_price: ', self.sell_price)
        self.main_layout.addRow(self.label_promo, self.promo)
        self.main_layout.addRow(self.label_promo_type, self.promo_type)
        self.main_layout.addRow('discount: ', self.discount)
        self.main_layout.addRow(self.label_promo_start_dt, self.promo_start_dt)
        self.main_layout.addRow(self.label_promo_end_dt, self.promo_end_dt)
        self.main_layout.addRow(self.label_effective_dt, self.effective_dt)

        self.main_layout.addRow('inventory_status: ', self.inventory_status)
        self.main_layout.addRow(self.label_on_hand_stock, self.on_hand_stock)
        self.main_layout.addRow(self.label_available_stock, self.available_stock)

        self.main_layout.addRow(self.save_item_button)

        self.setLayout(self.main_layout)

class ListItemTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.callClass()
        self.setDefaultAttributes()
        self.setWidgetSignal()
    
    def callClass(self):
        self.global_widget = GlobalWidget()
        self.item_management_sql = ItemManagementSQL()
        self.inventory_management_sql = InventoryManagementSQL()
        self.promo_management_sql = PromoManagementSQL()
    
    def onClickedEditItemButton(self, manage_item_mode, row_value=None):
        self.manage_item_dialog = ManageItemDialog(manage_item_mode, row_value)
        self.manage_item_dialog.exec()

    def fillListItemTable(self):
        all_item_data = self.item_management_sql.selectAllItemData('')

        for row_index, row_value in enumerate(all_item_data):
            total_cell = row_value[:11]
            for col_index, col_value in enumerate(total_cell):
                data = QTableWidgetItem(str(col_value))
                self.setItem(row_index, col_index + 1, data)

                if row_value[11] != 0:
                    data.setForeground(QColor(255, 0, 0))
            
            self.edit_item_button = self.global_widget.customPushButton('EDIT')
            self.setCellWidget(row_index, 0, self.edit_item_button)
            self.setWidgetSignal(row_value)


    def setWidgetSignal(self, row_value=None):
        self.edit_item_button.clicked.connect(lambda: self.onClickedEditItemButton('edit_item', row_value))
        pass

    def setDefaultAttributes(self):
        self.setColumnCount(12)
        self.setHorizontalHeaderLabels(['', 'barcode', 'item_name', 'expire_dt', 'item_type', 'brand', 'sales_group', 'supplier', 'cost', 'discount', 'sell_price', 'effective_dt'])
        self.setRowCount(50)
        self.fillListItemTable()

class ItemManagementWindow(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setMainLayout()

    def onClickedAddItemButton(self, manage_item_mode):
        self.manage_item_dialog = ManageItemDialog(manage_item_mode)
        self.manage_item_dialog.exec()

    def setWidgetSignal(self):
        self.add_item_button.clicked.connect(lambda: self.onClickedAddItemButton('add_item'))

    def setMainLayout(self):
        self.main_layout = QGridLayout()

        self.filter_bar = QLineEdit()
        self.add_item_button = QPushButton('ADD')
        self.list_item_table = ListItemTable()

        self.setWidgetSignal()

        self.main_layout.addWidget(self.filter_bar)
        self.main_layout.addWidget(self.add_item_button)
        self.main_layout.addWidget(self.list_item_table)

        self.setLayout(self.main_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
