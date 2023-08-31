import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_manager import *

class CustomLabel(QLabel):
    def __init__(self, text, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref in [
            'current_promo_name',
            'promo_type',
            'discount_percent',
            'discount_value',
            'new_sell_price',
            'start_dt',
            'end_dt',
            'current_effective_dt',
            'current_inventory_status',
            'on_hand_stock',
            'available_stock'
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

        if self.ref in [
            'promo_type', 
            'discount_percent', 
            'discount_value', 
            'new_sell_price',
            'current_promo_type',
            'current_discount_percent',
            'current_discount_value'
        ]:
            self.setDisabled(True)
            self.hide()

        if self.ref in ['on_hand_stock', 'available_stock']:
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
    data_saved = pyqtSignal()

    def __init__(self, reference=None):
        super().__init__()

        self.prepareDataManagement()

        self.ref = reference

        if self.ref in ['item_name', 'item_type', 'brand', 'supplier']:
            self.setEditable(True)

        if self.ref == 'sales_group':
            self.addItem('Retail')
            self.addItem('Wholesale')

        if self.ref in ['promo_name', 'current_promo_name']:
            self.setDisabled(True)
            self.addItem('No promo')
            data = self.sales_data_manager.listPromo('')
            for row in data:
                self.addItem(row[0])

        if self.ref in ['current_promo_name', 'current_inventory_status']:
            self.setDisabled(True)
            self.hide()

        if self.ref in ['inventory_status', 'current_inventory_status']:
            self.addItem('Not tracked')
            self.addItem('Tracked')

        self.updateComboBox()

    def updateComboBox(self):
        data = self.sales_data_manager.fillItemComboBox()

        if self.ref == 'item_name':
            self.clear()
            for row in data:
                self.addItem(row[0])

        if self.ref == 'item_type':
            self.clear()
            for row in data:
                self.addItem(row[1])

        if self.ref == 'brand':
            self.clear()
            for row in data:
                self.addItem(row[2])

        if self.ref == 'supplier':
            self.clear()
            for row in data:
                self.addItem(row[3])

        self.data_saved.emit()

    def prepareDataManagement(self):
        self.sales_data_manager = SalesDataManager()
    
class CustomDateEdit(QDateEdit):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference


        self.setCalendarPopup(True)
        self.setMinimumDate(QDate.currentDate())

        if self.ref in ['start_dt', 'end_dt', 'current_effective_dt']:
            self.hide()

        if self.ref == 'current_effective_dt':
            self.setDisabled(True)

class CustomPushButton(QPushButton):
    def __init__(self, text=None, reference=None):
        super().__init__()
        
        self.setText(text)

        if reference == 'save_button':
            pass

class CustomTableWidget(QTableWidget):
    def __init__(self, reference=None):
        super().__init__()

        self.ref = reference

        if self.ref == 'list_table':
            self.setRowCount(50)
            self.setColumnCount(15)
            self.setHorizontalHeaderLabels(['','',
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
                'effective_dt',
                'promo_name',
                'inventory_status'
            ])

class CustomGroupBox(QGroupBox):
    def __init__(self, reference=None):
        super().__init__()
    
        self.ref = reference

        if self.ref == 'panel_b':
            self.setFixedWidth(300)
            self.hide()
        pass

# ------------------------------------------------------------------------------- #

class ItemManagementWindow(QGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.prepareDataManagement()
        self.setMainLayout()

    # PANEL B SECTION-------------------------------------------------------- #
    def refreshComboBox(self):
        self.item_name.updateComboBox()
        self.item_type.updateComboBox()
        self.brand.updateComboBox()
        self.supplier.updateComboBox()

    def updateEditPanelB(self, row_index, row_data):
        self.label_inventory_status.hide()
        self.inventory_status.hide()
        self.label_current_inventory_status.show()
        self.current_inventory_status.show()
        self.save_add_button.hide()

        self.item_type.setDisabled(True)
        self.brand.setDisabled(True)
        self.sales_group.setDisabled(True)
        self.supplier.setDisabled(True)

        data = row_data

        self.item_id = data[14]
        self.item_price_id = data[15]
        self.promo_id = data[16]
        self.inventory_id = data[17]
        print('item_id: ', self.item_id)
        print('item_price_id: ', self.item_price_id)
        print('promo_id: ', self.promo_id)
        print('inventory_status: ', self.inventory_id)

        if self.promo_id == 0:
            print('this item has no promo')
            self.label_promo_name.show()
            self.promo_name.show()
            self.label_current_promo_name.hide()
            self.current_promo_name.hide()
            self.label_current_promo_name.hide()
            self.current_promo_name.hide()
            self.label_current_promo_type.hide()
            self.current_promo_type.hide()
            self.label_current_discount_percent.hide()
            self.current_discount_percent.hide()
            self.label_current_discount_value.hide()
            self.current_discount_value.hide()
            self.label_effective_dt.show()
            self.effective_dt.show()
            self.label_current_effective_dt.hide()
            self.current_effective_dt.hide()
            self.save_edit_button.show()


            self.barcode.setDisabled(False)
            self.item_name.setDisabled(False)
            self.expire_dt.setDisabled(False)
            self.cost.setDisabled(False)
            self.sell_price.setDisabled(False)

            self.barcode.setText(str(data[0]))
            self.item_name.setCurrentText(str(data[1]))
            self.expire_dt.setDate(QDate.fromString(data[2], Qt.DateFormat.ISODate))

            self.item_type.setCurrentText(str(data[3]))
            self.brand.setCurrentText(str(data[4]))
            self.sales_group.setCurrentText(str(data[5]))
            self.supplier.setCurrentText(str(data[6]))
            self.cost.setText(str(data[7]))
            self.sell_price.setText(str(data[8]))
            self.promo_name.setCurrentText(str('No promo'))
            self.effective_dt.setDate(QDate.fromString(data[10], Qt.DateFormat.ISODate))

            if self.inventory_id == 'Tracked':
                self.current_inventory_status.setCurrentText(str(self.inventory_id))
            else:
                self.current_inventory_status.setCurrentText(str(self.inventory_id))

        else:
            print('this item has promo')
            self.label_promo_name.hide()
            self.promo_name.hide()
            self.label_current_promo_name.show()
            self.current_promo_name.show()
            self.label_current_promo_name.show()
            self.current_promo_name.show()
            self.label_current_promo_type.show()
            self.current_promo_type.show()
            self.label_current_discount_percent.show()
            self.current_discount_percent.show()
            self.label_current_discount_value.show()
            self.current_discount_value.show()
            self.label_effective_dt.hide()
            self.effective_dt.hide()
            self.label_current_effective_dt.show()
            self.current_effective_dt.show()
            self.save_edit_button.hide()
            
            self.barcode.setDisabled(True)
            self.item_name.setDisabled(True)
            self.expire_dt.setDisabled(True)
            self.cost.setDisabled(True)
            self.sell_price.setDisabled(True)

            self.barcode.setText(str(data[0]))
            self.item_name.setCurrentText(str(data[1]))
            self.expire_dt.setDate(QDate.fromString(data[2], Qt.DateFormat.ISODate))

            self.item_type.setCurrentText(str(data[3]))
            self.brand.setCurrentText(str(data[4]))
            self.sales_group.setCurrentText(str(data[5]))
            self.supplier.setCurrentText(str(data[6]))

            self.cost.setText(str(data[7]))
            self.sell_price.setText(str(data[8]))
            self.current_promo_name.setCurrentText(str(data[11]))
            self.current_promo_type.setText(str(data[12]))
            self.current_discount_percent.setText(str(data[13]))
            self.current_discount_value.setText(str(data[9]))
            self.current_effective_dt.setDate(QDate.fromString(data[10], Qt.DateFormat.ISODate))

            if self.inventory_id == 'Tracked' or self.inventory_id == 'Not tracked':
                self.current_inventory_status.setCurrentText(str(self.inventory_id))



    def updateAddPanelB(self):
        self.label_promo_name.show()
        self.promo_name.show()
        self.label_current_promo_name.hide()
        self.current_promo_name.hide()
        self.label_current_promo_name.hide()
        self.current_promo_name.hide()
        self.label_current_promo_type.hide()
        self.current_promo_type.hide()
        self.label_current_discount_percent.hide()
        self.current_discount_percent.hide()
        self.label_current_discount_value.hide()
        self.current_discount_value.hide()
        self.label_effective_dt.show()
        self.effective_dt.show()
        self.label_current_effective_dt.hide()
        self.current_effective_dt.hide()
        self.label_inventory_status.show()
        self.inventory_status.show()
        self.label_current_inventory_status.hide()
        self.current_inventory_status.hide()
        self.save_add_button.show()
        self.save_edit_button.hide()

        self.barcode.setDisabled(False)
        self.item_name.setDisabled(False)
        self.expire_dt.setDisabled(False)
        self.item_type.setDisabled(False)
        self.brand.setDisabled(False)
        self.sales_group.setDisabled(False)
        self.supplier.setDisabled(False)
        self.cost.setDisabled(False)
        self.sell_price.setDisabled(False)

        self.expire_dt.setDate(QDate.currentDate())
        self.start_dt.setDate(QDate.currentDate())
        self.end_dt.setDate(QDate.currentDate())
        self.effective_dt.setDate(QDate.currentDate())
        self.current_effective_dt.setDate(QDate.currentDate())

    def onSaveButtonClicked(self, reference):
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

        if reference == 'add':
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
                converted_promo_type,
                converted_discount_percent,
                converted_discount_value,
                converted_start_dt,
                converted_end_dt,
                converted_inventory_status,
                converted_on_hand_stock,
                converted_available_stock
            )
            QMessageBox.information(self, "Success", "New item has been added!")
            self.data_saved.emit()

        elif reference == 'edit':
            print(reference)
            self.sales_data_manager.editSelectedItem(
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
                converted_promo_type,
                converted_discount_percent,
                converted_discount_value,
                converted_start_dt,
                converted_end_dt,
                self.item_id,
                self.item_price_id,
                self.promo_id
            )
            QMessageBox.information(self, "Success", "Item has been edited!")
            self.data_saved.emit()

    def handleTextChanged(self, text, reference=None):
        if reference == 'filter_bar':
            self.populateTable(text)
            print(text)
        
        if reference == 'sell_price':
            if text == '0' or text == '':
                self.promo_name.setCurrentText('No promo')
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
            if currentText == 'Tracked':
                self.label_on_hand_stock.show()
                self.on_hand_stock.show()
                self.label_available_stock.show()
                self.available_stock.show()
            
            else:
                self.label_on_hand_stock.hide()
                self.on_hand_stock.hide()
                self.label_available_stock.hide()
                self.available_stock.hide()   

    def onCloseButtonClicked(self):
        self.panel_b.hide()
        self.add_button.setDisabled(False)


    def showPanelB(self): # -- PANEL B
        panel = CustomGroupBox(reference='panel_b')
        panel_layout = QFormLayout()

        self.close_button = CustomPushButton(text='BACK')
        self.close_button.setFixedWidth(50)
        self.close_button.clicked.connect(self.onCloseButtonClicked)

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
        self.label_promo_name = CustomLabel(text='promo_name: ', reference='promo_name')
        self.promo_name = CustomComboBox(reference='promo_name')
        self.promo_name.currentTextChanged.connect(lambda currentText: self.handleCurrentTextChanged(currentText, reference='promo_name'))

        self.label_promo_type = CustomLabel(text='promo_type: ', reference='promo_type')
        self.promo_type = CustomLineEdit(reference='promo_type')
        self.label_discount_percent = CustomLabel(text='discount_percent: ', reference='discount_percent')
        self.discount_percent = CustomLineEdit(reference='discount_percent')
        self.label_discount_value = CustomLabel(text='discount_value: ', reference='discount_value')
        self.discount_value = CustomLineEdit(reference='discount_value')
        self.label_new_sell_price = CustomLabel(text='new_sell_price: ', reference='new_sell_price')
        self.new_sell_price = CustomLineEdit(reference='new_sell_price')
        self.label_start_dt = CustomLabel(text='start_dt: ', reference='start_dt')
        self.start_dt = CustomDateEdit(reference='start_dt')
        self.label_end_dt = CustomLabel(text='end_dt: ', reference='end_dt')
        self.end_dt = CustomDateEdit(reference='end_dt')
        self.label_effective_dt = CustomLabel(text='effective_dt: ', reference='effective_dt')
        self.effective_dt = CustomDateEdit()

        self.label_inventory_status = CustomLabel(text='inventory_status: ')
        self.inventory_status = CustomComboBox(reference='inventory_status')
        self.inventory_status.currentTextChanged.connect(lambda currentText: self.handleCurrentTextChanged(currentText, reference='inventory_status'))
        self.label_current_inventory_status = CustomLabel(text='current_inventory_status: ', reference='current_inventory_status')
        self.current_inventory_status = CustomComboBox(reference='current_inventory_status')
        self.label_on_hand_stock = CustomLabel(text='on_hand_stock: ', reference='on_hand_stock')
        self.on_hand_stock = CustomLineEdit(reference='on_hand_stock')
        self.label_available_stock = CustomLabel(text='available_stock: ', reference='available_stock')
        self.available_stock = CustomLineEdit(reference='available_stock')

        # additional widgets
        self.label_current_promo_name = CustomLabel(text='current_promo_name: ', reference='current_promo_name')
        self.current_promo_name = CustomComboBox(reference='current_promo_name')
        self.label_current_promo_type = CustomLabel(text='current_promo_type: ', reference='current_promo_type')
        self.current_promo_type = CustomLineEdit(reference='current_promo_type')
        self.label_current_discount_percent = CustomLabel(text='current_discount_percent: ', reference='current_discount_percent')
        self.current_discount_percent = CustomLineEdit(reference='current_discount_percent')
        self.label_current_discount_value = CustomLabel(text='current_discount_value: ', reference='current_discount_value')
        self.current_discount_value = CustomLineEdit(reference='current_discount_value')
        self.label_current_effective_dt = CustomLabel(text='current_effective_dt: ', reference='current_effective_dt')
        self.current_effective_dt = CustomDateEdit(reference='current_effective_dt')

        self.save_add_button = CustomPushButton(text='SAVE ADD', reference='save_button')
        self.save_add_button.clicked.connect(lambda: self.onSaveButtonClicked('add'))

        self.save_edit_button = CustomPushButton(text='SAVE EDIT', reference='save_button')
        self.save_edit_button.clicked.connect(lambda: self.onSaveButtonClicked('edit'))
        
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

        panel_layout.addRow(self.label_promo_name, self.promo_name)
        panel_layout.addRow(self.label_current_promo_name, self.current_promo_name)

        panel_layout.addRow(self.label_promo_type, self.promo_type)
        panel_layout.addRow(self.label_current_promo_type, self.current_promo_type)

        panel_layout.addRow(self.label_discount_percent, self.discount_percent)
        panel_layout.addRow(self.label_current_discount_percent, self.current_discount_percent)

        panel_layout.addRow(self.label_discount_value, self.discount_value)
        panel_layout.addRow(self.label_current_discount_value, self.current_discount_value)

        panel_layout.addRow(self.label_new_sell_price, self.new_sell_price)
        panel_layout.addRow(self.label_start_dt, self.start_dt)
        panel_layout.addRow(self.label_end_dt, self.end_dt)

        panel_layout.addRow(self.label_effective_dt, self.effective_dt)
        panel_layout.addRow(self.label_current_effective_dt, self.current_effective_dt)

        panel_layout.addRow(self.label_inventory_status, self.inventory_status)
        panel_layout.addRow(self.label_current_inventory_status, self.current_inventory_status)
        panel_layout.addRow(self.label_on_hand_stock, self.on_hand_stock)
        panel_layout.addRow(self.label_available_stock, self.available_stock)

        panel_layout.addRow(self.save_add_button)
        panel_layout.addRow(self.save_edit_button)

        panel.setLayout(panel_layout)

        return panel

    # PANEL A SECTION -------------------------------------------------------- #
    def showRemoveConfirmationDialog(self, row_index, row_data):
        data = row_data

        item_name = str(data[1])
        item_price_id = str(data[15])
        effective_dt = QDate.fromString(data[10], 'yyyy-MM-dd')
        current_dt = QDateTime.currentDateTime().date()

        # Convert current_datetime to QDate

        if effective_dt >= current_dt:
            confirmation = QMessageBox.warning(self, "Remove", f"Are you sure you want to remove <b>{item_name}</b>?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                    self.sales_data_manager.removeSelectedItem(item_price_id)
                    print(effective_dt)
                    print(item_price_id)
                    self.data_saved.emit()
            else:
                pass
        else:
            converted_effective_dt = effective_dt.toString('MM-dd-yyyy')
            converted_current_dt = current_dt.toString('MM-dd-yyyy')
            print(converted_effective_dt)
            print(converted_current_dt)
            QMessageBox.critical(self, "Invalid action", f"Item cannot be deleted.")

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
            data = self.sales_data_manager.listItem('')
        else:
            data = self.sales_data_manager.listItem(text)


        for row_index, row_data in enumerate(data):
            data = row_data
            total_cell = data[:12]

            effective_dt = QDate.fromString(data[10], 'yyyy-MM-dd')
            current_dt = QDateTime.currentDateTime().date()
            item_id = data[14]
            item_price_id = data[15]
            promo_id = data[16]
            stock_id = data[17]
            print('stock_id: ', stock_id)


            for col_index, col_data in enumerate(total_cell):
                cell = QTableWidgetItem(str(col_data))
                inventory_status = QTableWidgetItem(str(stock_id))

                self.edit_button = CustomPushButton(text='EDIT')
                self.edit_button.clicked.connect(lambda row_index=row_index, row_data=row_data: self.onEditButtonClicked(row_index, row_data))
                self.list_table.setCellWidget(row_index, 0, self.edit_button)
                
                self.remove_button = CustomPushButton(text='REMOVE')
                self.remove_button.clicked.connect(lambda row_index=row_index, row_data=row_data: self.onRemoveButtonClicked(row_index, row_data))
                self.list_table.setCellWidget(row_index, 1, self.remove_button)

                self.list_table.setItem(row_index, col_index + 2, cell)
                self.list_table.setItem(row_index, 14, inventory_status)

                if promo_id != 0:
                    cell.setForeground(QColor(255, 0, 255))
                    self.edit_button.setText('VIEW')
                
                if effective_dt < current_dt:
                    self.remove_button.setDisabled(True)


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
        panel_layout.addWidget(self.list_table,2,0,1,2)

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
    window = ItemManagementWindow()
    window.show()
    sys.exit(pos_app.exec())
