import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(''))
print('sys path: ', os.path.abspath(''))

from src.core.color_scheme import *
from src.core.manual_csv_importer import *
from src.database.admin.product import *
from src.widget.admin.product import *

color_scheme = ColorScheme()

class ProductWindow(MyWidget):
    def __init__(self):
        super().__init__()

        self.default_init()
        self.show_main_panel()
        self.sync_ui()

    def default_init(self):
        self.product_schema = ProductSchema()
        self.my_push_button = MyPushButton()

        self.data_list_curr_page = 1
        self.clicked_data_list_edit_button = None
        self.clicked_data_list_view_button = None
        self.clicked_data_list_delete_button = None
        self.selected_product_id = None

        self.required_field_indicator = "<font color='red'>-- required</font>"

        self.total_row_count = self.product_schema.count_product()
        pass
    def sync_ui(self):
        self.populate_combo_box()
        self.populate_table()

        self.total_data.setText(f'Total product: {self.product_schema.count_product()}')

        self.primary_info_page.show()
        self.category_info_page.show()
        self.price_info_page.show()
        self.inventory_info_page.show()

        self.data_mgt_add_button.setDisabled(False)
        self.form_panel.hide()

        self.promo_type_label.hide()
        self.discount_percent_label.hide()
        self.discount_value_label.hide()
        self.new_sell_price_label.hide()
        self.start_dt_label.hide()
        self.end_dt_label.hide()
        self.inventory_item_name_label.hide()
        self.available_stock_label.hide()
        self.on_hand_stock_label.hide()

        self.promo_type_field.hide()
        self.discount_percent_field.hide()
        self.discount_value_field.hide()
        self.new_sell_price_field.hide()
        self.start_dt_field.hide()
        self.end_dt_field.hide()
        self.inventory_item_name_field.hide()
        self.available_stock_field.hide()
        self.on_hand_stock_field.hide()

        self.promo_type_field.setDisabled(True)
        self.discount_percent_field.setDisabled(True)
        self.discount_value_field.setDisabled(True)
        self.new_sell_price_field.setDisabled(True)
        self.inventory_item_name_field.setDisabled(True)

        pass

    def style_data_list_action_button(self):
        self.data_list_edit_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.primary_data_list_edit_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.category_data_list_edit_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.price_data_list_edit_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)

        self.data_list_view_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.primary_data_list_view_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.category_data_list_view_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.price_data_list_view_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)

        self.data_list_delete_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.primary_data_list_delete_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.category_data_list_delete_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.price_data_list_delete_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
    def style_inventory_data_list_action_button(self):
        self.inventory_data_list_edit_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.inventory_data_list_view_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)
        self.inventory_data_list_delete_button.setStyleSheet(self.my_push_button.data_list_action_button_ss)

        pass
    
    def style_data_list_pgn_action_button(self):
        self.data_list_pgn_prev_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.primary_data_list_pgn_prev_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.category_data_list_pgn_prev_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.price_data_list_pgn_prev_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.inventory_data_list_pgn_prev_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        
        self.data_list_pgn_next_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.primary_data_list_pgn_next_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.category_data_list_pgn_next_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.price_data_list_pgn_next_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        self.inventory_data_list_pgn_next_button.setStyleSheet(self.my_push_button.data_list_pgn_button_ss)
        pass
    def style_form_action_button(self):
        self.form_close_button.setStyleSheet(self.my_push_button.form_close_button_ss)
        self.form_save_new_button.setStyleSheet(self.my_push_button.form_save_new_button_ss)
        self.form_save_edit_button.setStyleSheet(self.my_push_button.form_save_edit_button_ss)
    def style_data_mgt_action_button(self):
        self.data_mgt_sync_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        self.data_mgt_import_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        self.data_mgt_add_button.setStyleSheet(self.my_push_button.data_mgt_button_ss)
        pass

    def on_data_list_edit_button_clicked(self, row_value, edit_button):
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        edit_button.setDisabled(True)
        self.data_mgt_add_button.setDisabled(False)

        self.primary_info_page.show()
        self.category_info_page.hide()
        self.price_info_page.show()
        if row_value[12] == 'Enabled': self.inventory_info_page.hide() 
        else: self.inventory_info_page.show()

        self.inventory_tracking_label.show()
        self.inventory_tracking_field.show()

        self.inventory_item_name_label.hide()
        self.inventory_item_name_field.hide()

        self.available_stock_label.hide()
        self.on_hand_stock_label.hide()

        self.available_stock_field.hide()
        self.on_hand_stock_field.hide()

        self.form_save_new_button.hide()
        self.form_save_edit_button.show()
        self.form_panel.show()
        
        # region > set_form_field_input
        self.barcode_field.setText(str(row_value[0]))
        self.item_name_field.setText(str(row_value[1]))
        self.expire_dt_field.setDate(QDate.fromString(row_value[2], Qt.DateFormat.ISODate))
        self.item_type_field.setCurrentText(str(row_value[3]))

        self.brand_field.setCurrentText(str(row_value[4]))
        self.sales_group_field.setCurrentText(str(row_value[5]))
        self.supplier_field.setCurrentText(str(row_value[6]))

        self.cost_field.setText(str(row_value[7]))
        self.sell_price_field.setText(str(row_value[8]))
        self.effective_dt_field.setDate(QDate.fromString(row_value[9], Qt.DateFormat.ISODate))
        self.promo_name_field.setCurrentText(str(row_value[10]))

        self.inventory_tracking_field.setCurrentText(str(row_value[12]))
        self.available_stock_field.setText(str(row_value[13]))
        self.on_hand_stock_field.setText(str(row_value[14]))
        # endregion
        # region > get_selected_ids
        self.selected_item_id = str(row_value[16])
        self.selected_item_price_id = str(row_value[17])
        self.selected_promo_id = str(row_value[18])
        self.selected_stock_id = str(row_value[19])
        # endregion

        self.clicked_data_list_edit_button = edit_button
        pass
    def on_data_list_view_button_clicked(self, row_value, view_button):
        self.data_list_view_dialog = MyDialog(object_name='data_list_view_dialog', parent=self)
        self.data_list_view_dialog_layout = MyFormLayout()

        barcode_info = MyLabel(object_name='barcode_info', text=str(row_value[0]))
        item_name_info = MyLabel(object_name='item_name_info', text=str(row_value[1]))
        expire_dt_info = MyLabel(object_name='expire_dt_info', text=str(row_value[2]))

        item_type_info = MyLabel(object_name='item_type_info', text=str(row_value[3]))
        brand_info = MyLabel(object_name='brand_info', text=str(row_value[4]))
        sales_group_info = MyLabel(object_name='sales_group_info', text=str(row_value[5]))
        supplier_info = MyLabel(object_name='supplier_info', text=str(row_value[6]))

        cost_info = MyLabel(object_name='cost_info', text=f'₱{row_value[7]}')
        sell_price_info = MyLabel(object_name='sell_price_info', text=f'₱{row_value[8]}')
        effective_dt_info = MyLabel(object_name='effective_dt_info', text=str(row_value[9]))
        promo_name_info = MyLabel(object_name='promo_name_info', text=str(row_value[10]))
        discount_value_info = MyLabel(object_name='discount_value_info', text=f'₱{row_value[11]}')

        inventory_tracking_info = MyLabel(object_name='inventory_tracking_info', text=str(row_value[12]))

        date_created_info = MyLabel(object_name='date_created_info', text=str(row_value[15]))

        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Barcode:'), barcode_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Item name:'), item_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Expire date:'), expire_dt_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Item type:'), item_type_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Brand:'), brand_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Sales group:'), sales_group_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Supplier:'), supplier_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Cost:'), cost_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Sell price:'), sell_price_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Effective date:'), effective_dt_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Promo name:'), promo_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Discount value:'), discount_value_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Inventory tracking:'), inventory_tracking_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Date and time created:'), date_created_info)
        self.data_list_view_dialog.setLayout(self.data_list_view_dialog_layout)

        self.data_list_view_dialog.exec()
        pass
    def on_data_list_delete_button_clicked(self, row_value, delete_button):
        confirmation_a = QMessageBox.warning(self, 'Confirm', f'Are you sure you want to delete {row_value[1]}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation_a == QMessageBox.StandardButton.Yes:
            self.selected_item_price_id = str(row_value[17])
            self.selected_stock_id = str(row_value[19])

            self.product_schema.delete_selected_product(self.selected_item_price_id, self.selected_stock_id)
            # self.product_schema.delete_selected_inventory(self.selected_stock_id)

            self.populate_table()
            self.populate_combo_box()
            self.total_data.setText(f'Total product: {self.product_schema.count_product()}')

            QMessageBox.information(self, 'Success', 'Promo has been deleted!')
            print('item price id', row_value[17])
            print('item price id', self.selected_item_price_id)

        pass

    def on_inventory_data_list_edit_button_clicked(self, row_value, edit_button):
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        edit_button.setDisabled(True)
        self.data_mgt_add_button.setDisabled(False)

        self.primary_info_page.hide()
        self.category_info_page.hide()
        self.price_info_page.hide()
        self.inventory_info_page.show()

        self.inventory_tracking_label.hide()
        self.inventory_item_name_label.show()
        self.available_stock_label.show()
        self.on_hand_stock_label.show()

        self.inventory_tracking_field.hide()
        self.inventory_item_name_field.show()
        self.available_stock_field.show()
        self.on_hand_stock_field.show()

        self.form_save_new_button.hide()
        self.form_save_edit_button.show()
        self.form_panel.show()
        
        # region > set_form_field_input
        self.inventory_item_name_field.setText(str(row_value[0]))
        self.available_stock_field.setText(str(row_value[1]))
        self.on_hand_stock_field.setText(str(row_value[2]))
        # endregion
        # region > get_selected_ids
        self.selected_stock_id = str(row_value[5])
        # endregion

        self.clicked_data_list_edit_button = edit_button
        pass
    def on_inventory_data_list_view_button_clicked(self, row_value, view_button):
        self.data_list_view_dialog = MyDialog(object_name='data_list_view_dialog', parent=self)
        self.data_list_view_dialog_layout = MyFormLayout()

        item_name_info = MyLabel(object_name='item_name_info', text=str(row_value[0]))
        available_stock_info = MyLabel(object_name='available_stock_info', text=str(row_value[1]))
        on_hand_stock_info = MyLabel(object_name='on_hand_stock_info', text=str(row_value[2]))
        date_created_info = MyLabel(object_name='date_created_info', text=str(row_value[3]))

        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Item_name:'), item_name_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Available stock:'), available_stock_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='On hand stock:'), on_hand_stock_info)
        self.data_list_view_dialog_layout.addRow(MyLabel(text='<hr>'))
        self.data_list_view_dialog_layout.addRow(MyLabel(object_name='view_dialog_labels', text='Date and time created:'), date_created_info)
        self.data_list_view_dialog.setLayout(self.data_list_view_dialog_layout)

        self.data_list_view_dialog.exec()
        pass
    def on_inventory_data_list_delete_button_clicked(self, row_value, delete_button):
        confirmation_a = QMessageBox.warning(self, 'Confirm', f"Are you sure you want to delete {row_value[0]}'s inventory?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation_a == QMessageBox.StandardButton.Yes:
            self.selected_stock_id = str(row_value[5])

            self.product_schema.delete_selected_inventory(self.selected_stock_id)

            self.populate_table()
            self.populate_combo_box()

            QMessageBox.information(self, 'Success', 'Inventory has been deleted!')
        pass

    def on_form_close_button_clicked(self):
        self.form_panel.hide()
        self.data_mgt_add_button.setDisabled(False)
        pass
    def on_form_save_new_button_clicked(self):
        # region > convert field input into str
        barcode = str(self.barcode_field.text())
        item_name = str(self.item_name_field.text())
        expire_dt = self.expire_dt_field.date().toString(Qt.DateFormat.ISODate)

        item_type = str(self.item_type_field.currentText())
        brand = str(self.brand_field.currentText())
        sales_group = str(self.sales_group_field.currentText())
        supplier = str(self.supplier_field.currentText())

        cost = str(self.cost_field.text())
        sell_price = str(self.sell_price_field.text())
        effective_dt = self.effective_dt_field.date().toString(Qt.DateFormat.ISODate)
        promo_name = str(self.promo_name_field.currentText())
        promo_type = str(self.promo_type_field.text())
        discount_percent = str(self.discount_percent_field.text())
        discount_value = str(self.discount_value_field.text())
        new_sell_price = str(self.new_sell_price_field.text())
        start_dt = self.start_dt_field.date().toString(Qt.DateFormat.ISODate)
        end_dt = self.end_dt_field.date().toString(Qt.DateFormat.ISODate)

        inventory_tracking = str(self.inventory_tracking_field.currentText())
        available_stock = str(self.available_stock_field.text())
        on_hand_stock = str(self.on_hand_stock_field.text())
        # endregion

        # region > input_restrictions
        if not (cost.replace('.', '', 1).isdigit() and sell_price.replace('.', '', 1).isdigit()):
            QMessageBox.critical(self, 'Error', 'Incorrect numerical input.')
            return
        
        if '' in [
            item_name,
            brand,
            supplier,
            cost,
            sell_price
            # !!! CHECKPOINT !!!
        ]:
            QMessageBox.critical(self, 'Error', 'Must fill required field.')
            return

        if inventory_tracking == 'Enabled' and False in [available_stock.isdigit(), on_hand_stock.isdigit()]:
            QMessageBox.critical(self, 'Error', 'Incorrect numerical input.')
            return
        # endregion
        
        self.product_schema.add_new_product(
            barcode=barcode,
            item_name=item_name,
            expire_dt=expire_dt,

            item_type=item_type,
            brand=brand,
            sales_group=sales_group,
            supplier=supplier,

            cost=cost,
            sell_price=sell_price,
            effective_dt=effective_dt,
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            discount_value=discount_value,
            new_sell_price=new_sell_price,
            start_dt=start_dt,
            end_dt=end_dt,
            
            inventory_tracking=inventory_tracking,
            available_stock=available_stock,
            on_hand_stock=on_hand_stock
        )
        
        self.total_row_count = self.product_schema.count_product()
        self.populate_table()
        self.populate_combo_box()
        self.total_data.setText(f'Total product: {self.product_schema.count_product()}')

        QMessageBox.information(self, 'Success', 'New product has been added!')
        pass
    def on_form_save_edit_button_clicked(self):
        # region > convert field input into str
        barcode = str(self.barcode_field.text())
        item_name = str(self.item_name_field.text())
        expire_dt = str(self.expire_dt_field.date().toString(Qt.DateFormat.ISODate))

        item_type = str(self.item_type_field.currentText())
        brand = str(self.brand_field.currentText())
        sales_group = str(self.sales_group_field.currentText())
        supplier = str(self.supplier_field.currentText())

        cost = str(self.cost_field.text())
        sell_price = str(self.sell_price_field.text())
        effective_dt = str(self.effective_dt_field.date().toString(Qt.DateFormat.ISODate))
        promo_name = str(self.promo_name_field.currentText())
        promo_type = str(self.promo_type_field.text())
        discount_percent = str(self.discount_percent_field.text())
        discount_value = str(self.discount_value_field.text())
        new_sell_price = str(self.new_sell_price_field.text())
        start_dt = str(self.start_dt_field.date().toString(Qt.DateFormat.ISODate))
        end_dt = str(self.end_dt_field.date().toString(Qt.DateFormat.ISODate))

        inventory_tracking = str(self.inventory_tracking_field.currentText())
        available_stock = str(self.available_stock_field.text())
        on_hand_stock = str(self.on_hand_stock_field.text())

        item_id = self.selected_item_id
        item_price_id = self.selected_item_price_id
        promo_id = self.selected_promo_id
        stock_id = self.selected_stock_id
        # endregion

        # region > input_restrictions
        if not (cost.replace('.', '', 1).isdigit() and sell_price.replace('.', '', 1).isdigit()):
            QMessageBox.critical(self, 'Error', 'Incorrect numerical input.')
            return
        
        if '' in [
            item_name,
            cost,
            sell_price
            # !!! CHECKPOINT !!!
        ]:
            QMessageBox.critical(self, 'Error', 'Must fill required field.')
            return

        if inventory_tracking == 'Enabled' and False in [available_stock.isdigit(), on_hand_stock.isdigit()]:
            QMessageBox.critical(self, 'Error', 'Incorrect numerical input.')
            return
        # endregion

        self.product_schema.edit_selected_product(
            barcode=barcode,
            item_name=item_name,
            expire_dt=expire_dt,

            item_type=item_type,
            brand=brand,
            sales_group=sales_group,
            supplier=supplier,

            cost=cost,
            sell_price=sell_price,
            effective_dt=effective_dt,
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            discount_value=discount_value,
            new_sell_price=new_sell_price,
            start_dt=start_dt,
            end_dt=end_dt,

            inventory_tracking=inventory_tracking,
            available_stock=available_stock,
            on_hand_stock=on_hand_stock,

            item_id=item_id,
            item_price_id=item_price_id,
            promo_id=promo_id,
            stock_id=stock_id
        )
        
        self.total_row_count = self.product_schema.count_product()
        self.populate_table()
        self.populate_combo_box()
        self.on_data_mgt_add_button_clicked()
        
        self.total_data.setText(f'Total product: {self.product_schema.count_product()}')

        QMessageBox.information(self, 'Success', 'Product has been edited!')
        pass
    
    def on_data_mgt_sync_button_clicked(self):
        self.sync_ui()
        pass
    def on_data_mgt_import_button_clicked(self):
        csv_file, _ = QFileDialog.getOpenFileName(None, 'Open CSV', '', 'CSV Files (*.csv)')
        
        if csv_file:
            self.manual_import = ManualProductImport(csv_file=csv_file)
            
            self.manual_import.progress_signal.connect(self.manual_import.update_progress)
            self.manual_import.finished_signal.connect(self.manual_import.import_finished)
            self.manual_import.finished_signal.connect(self.sync_ui)
            self.manual_import.error_signal.connect(self.manual_import.import_error)
            self.manual_import.start()
        else:
            pass
        pass
    def on_data_mgt_add_button_clicked(self):
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        self.data_mgt_add_button.setDisabled(True)

        self.primary_info_page.show()
        self.category_info_page.show()
        self.price_info_page.show()
        self.inventory_info_page.show()

        self.inventory_item_name_label.hide()
        self.inventory_item_name_field.hide()

        self.form_save_new_button.show()
        self.form_save_edit_button.hide()
        self.form_panel.show()
            
        self.clicked_data_list_edit_button = None
        pass
    
    def on_data_list_pgn_prev_button_clicked(self):
        self.on_data_mgt_add_button_clicked() if self.form_panel.isVisible() == True else None
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        
        if self.data_list_curr_page > 1:
            self.data_list_curr_page -= 1
            self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')

        self.populate_table(text_filter=self.text_filter_field.text(), current_page=self.data_list_curr_page)

        self.clicked_data_list_edit_button = None
        pass
    def on_data_list_pgn_next_button_clicked(self):
        self.on_data_mgt_add_button_clicked() if self.form_panel.isVisible() == True else None
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        
        self.data_list_curr_page += 1
        self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')
        
        self.populate_table(text_filter=self.text_filter_field.text(), current_page=self.data_list_curr_page)
        
        self.clicked_data_list_edit_button = None
        pass
        pass

    def on_text_filter_field_text_changed(self):
        self.data_list_curr_page = 1
        self.data_list_pgn_page.setText(f'Page {self.data_list_curr_page}')
        self.populate_table(text_filter=str(self.text_filter_field.text()), current_page=self.data_list_curr_page)
        pass

    def on_item_name_field_text_changed(self):
        self.item_name_label.setText(f'Item name {self.required_field_indicator}') if self.item_name_field.text() == '' else  self.item_name_label.setText(f'Item name')
        pass
    def on_item_type_field_current_text_changed(self):
        self.item_type_label.setText(f'Item type {self.required_field_indicator}') if self.item_type_field.currentText() == '' else  self.item_type_label.setText(f'Item type')
        pass
    def on_brand_field_current_text_changed(self):
        self.brand_label.setText(f'Brand {self.required_field_indicator}') if self.brand_field.currentText() == '' else  self.brand_label.setText(f'Brand')
        pass
    def on_supplier_field_current_text_changed(self):
        self.supplier_label.setText(f'Supplier {self.required_field_indicator}') if self.supplier_field.currentText() == '' else  self.supplier_label.setText(f'Supplier')
        pass
    def on_cost_field_text_changed(self):
        self.cost_label.setText(f'Cost {self.required_field_indicator}') if self.cost_field.text() == '' else  self.cost_label.setText(f'Cost')
        pass
    def on_sell_price_field_text_changed(self):
        self.sell_price_label.setText(f'Sell price {self.required_field_indicator}') if self.sell_price_field.text() == '' else  self.sell_price_label.setText(f'Sell price')
        
        try:
            sell_price = float(self.sell_price_field.text())
            discount_percent = float(self.discount_percent_field.text())

            old_sell_price = sell_price
            discount_value = old_sell_price * (discount_percent / 100)
            new_sell_price = sell_price - discount_value

            self.discount_value_field.setText(f'{discount_value:.2f}')
            self.new_sell_price_field.setText(f'{new_sell_price:.2f}')
            pass
        except ValueError:
            self.discount_value_field.setText('Error')
            self.new_sell_price_field.setText('Error')
        pass
    def on_promo_name_field_current_text_changed(self):
        if self.promo_name_field.currentText() == 'No promo':
            self.effective_dt_label.show()
            self.promo_type_label.hide()
            self.discount_percent_label.hide()
            self.discount_value_label.hide()
            self.new_sell_price_label.hide()
            self.start_dt_label.hide()
            self.end_dt_label.hide()

            self.effective_dt_field.show()
            self.promo_type_field.hide()
            self.discount_percent_field.hide()
            self.discount_value_field.hide()
            self.new_sell_price_field.hide()
            self.start_dt_field.hide()
            self.end_dt_field.hide()
        else:
            self.effective_dt_label.hide()
            self.promo_type_label.show()
            self.discount_percent_label.show()
            self.discount_value_label.show()
            self.new_sell_price_label.show()
            self.start_dt_label.show()
            self.end_dt_label.show()

            self.effective_dt_field.hide()
            self.promo_type_field.show()
            self.discount_percent_field.show()
            self.discount_value_field.show()
            self.new_sell_price_field.show()
            self.start_dt_field.show()
            self.end_dt_field.show()
        
            pt_and_dp_data = self.product_schema.list_promo_type_and_discount_percent(self.promo_name_field.currentText())

            for row in pt_and_dp_data:
                self.promo_type_field.setText(str(row[0]))
                self.discount_percent_field.setText(str(row[1]))

            try:
                sell_price = float(self.sell_price_field.text())
                discount_percent = float(self.discount_percent_field.text())

                old_sell_price = sell_price
                discount_value = old_sell_price * (discount_percent / 100)
                new_sell_price = sell_price - discount_value

                self.discount_value_field.setText(f'{discount_value:.2f}')
                self.new_sell_price_field.setText(f'{new_sell_price:.2f}')
                pass
            except ValueError:
                self.discount_value_field.setText('Error')
                self.new_sell_price_field.setText('Error')
        pass
    def on_inventory_tracking_field_current_text_changed(self):
        if self.inventory_tracking_field.currentText() == 'Disabled':
            self.available_stock_label.hide()
            self.on_hand_stock_label.hide()

            self.available_stock_field.hide()
            self.on_hand_stock_field.hide()
            pass
        elif self.inventory_tracking_field.currentText() == 'Enabled':
            self.available_stock_label.show()
            self.on_hand_stock_label.show()

            self.available_stock_field.show()
            self.on_hand_stock_field.show()
        pass
    def on_available_stock_field_text_changed(self):
        self.available_stock_label.setText(f'Available stock {self.required_field_indicator}') if self.available_stock_field.text() == '' else  self.available_stock_label.setText(f'Available stock')
        pass
    def on_on_hand_stock_field_text_changed(self):
        self.on_hand_stock_label.setText(f'On hand stock {self.required_field_indicator}') if self.on_hand_stock_field.text() == '' else  self.on_hand_stock_label.setText(f'On hand stock')
        pass

    def populate_combo_box(self):
        self.item_type_field.clear()
        self.brand_field.clear()
        self.sales_group_field.clear()
        self.supplier_field.clear()
        self.promo_name_field.clear()
        self.inventory_tracking_field.clear()

        # region > data_list
        item_type_data = self.product_schema.list_item_type()
        brand_data = self.product_schema.list_brand()
        supplier_data = self.product_schema.list_supplier()
        promo_name_data = self.product_schema.list_promo()
        # endregion

        # region > field_add_item
        for item_type in item_type_data: 
            self.item_type_field.addItem('No type')
            self.item_type_field.addItem(item_type[0])
        for brand in brand_data: 
            self.brand_field.addItem('No brand')
            self.brand_field.addItem(brand[0])

        self.sales_group_field.addItem('Retail')
        self.sales_group_field.addItem('Wholesale')

        for supplier in supplier_data: 
            self.supplier_field.addItem('No supplier')
            self.supplier_field.addItem(supplier[0])

        self.promo_name_field.addItem('No promo')
        for promo_name in promo_name_data: self.promo_name_field.addItem(promo_name[0])

        self.inventory_tracking_field.addItem('Disabled')
        self.inventory_tracking_field.addItem('Enabled')
        # endregion

        pass
    def populate_table(self, text_filter='', current_page=1):
        # region > data_list_clear_contents
        self.data_list_table.clearContents()
        self.primary_data_list_table.clearContents()
        self.category_data_list_table.clearContents()
        self.price_data_list_table.clearContents()
        self.inventory_data_list_table.clearContents()
        # endregion

        # region > data_list
        product_data = self.product_schema.list_product(text_filter=text_filter, page_number=current_page)
        inventory_data = self.product_schema.list_inventory(text_filter=text_filter, page_number=current_page)
        # endregion

        # region > data_list_pgn_button_set_enabled
        self.data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)
        self.primary_data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)
        self.category_data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)
        self.price_data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)
        self.inventory_data_list_pgn_prev_button.setEnabled(self.data_list_curr_page > 1)

        self.data_list_pgn_next_button.setEnabled(len(product_data) == 30)
        self.primary_data_list_pgn_next_button.setEnabled(len(product_data) == 30)
        self.category_data_list_pgn_next_button.setEnabled(len(product_data) == 30)
        self.price_data_list_pgn_next_button.setEnabled(len(product_data) == 30)
        self.inventory_data_list_pgn_next_button.setEnabled(len(product_data) == 30)
        # endregion

        # region > clicked_data_list_set_disabled
        self.clicked_data_list_edit_button.setDisabled(False) if self.clicked_data_list_edit_button else None
        self.clicked_data_list_edit_button = None
        # endregion
        
        # region > data_list_table_set_row_count
        self.data_list_table.setRowCount(len(product_data))
        self.primary_data_list_table.setRowCount(len(product_data))
        self.category_data_list_table.setRowCount(len(product_data))
        self.price_data_list_table.setRowCount(len(product_data))
        self.inventory_data_list_table.setRowCount(len(inventory_data))
        # endregion

        for row_index, row_value in enumerate(product_data):
            # region > data_list_action
            self.data_list_action_panel = MyGroupBox(object_name='data_list_action_panel') # head.a
            self.data_list_action_panel_layout = MyHBoxLayout(object_name='data_list_action_panel_layout')
            
            # region > set_data_list_action_buttons
            self.data_list_edit_button = MyPushButton(object_name='data_list_edit_button', text='Edit')
            self.data_list_view_button = MyPushButton(object_name='data_list_view_button', text='View')
            self.data_list_delete_button = MyPushButton(object_name='data_list_delete_button')
            # endregion

            # region > data_list_action_button_connections
            self.data_list_edit_button.clicked.connect(lambda _, row_value=row_value, edit_button=self.data_list_edit_button: self.on_data_list_edit_button_clicked(row_value, edit_button))
            self.data_list_view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.data_list_view_button: self.on_data_list_view_button_clicked(row_value, view_button))
            self.data_list_delete_button.clicked.connect(lambda _, row_value=row_value, delete_button=self.data_list_delete_button: self.on_data_list_delete_button_clicked(row_value, delete_button))
            # endregion

            self.data_list_action_panel_layout.addWidget(self.data_list_edit_button)
            self.data_list_action_panel_layout.addWidget(self.data_list_view_button)
            self.data_list_action_panel_layout.addWidget(self.data_list_delete_button)
            self.data_list_action_panel.setLayout(self.data_list_action_panel_layout)
            # endregion
            # region > primary_data_list_action
            self.primary_data_list_action_panel = MyGroupBox(object_name='data_list_action_panel') # head.a
            self.primary_data_list_action_panel_layout = MyHBoxLayout(object_name='data_list_action_panel_layout')
            
            # region > set_primary_data_list_action_buttons
            self.primary_data_list_edit_button = MyPushButton(object_name='data_list_edit_button', text='Edit')
            self.primary_data_list_view_button = MyPushButton(object_name='data_list_view_button', text='View')
            self.primary_data_list_delete_button = MyPushButton(object_name='data_list_delete_button')
            # endregion

            # region > primary_data_list_action_button_connections
            self.primary_data_list_edit_button.clicked.connect(lambda _, row_value=row_value, edit_button=self.primary_data_list_edit_button: self.on_data_list_edit_button_clicked(row_value, edit_button))
            self.primary_data_list_view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.primary_data_list_view_button: self.on_data_list_view_button_clicked(row_value, view_button))
            self.primary_data_list_delete_button.clicked.connect(lambda _, row_value=row_value, delete_button=self.primary_data_list_delete_button: self.on_data_list_delete_button_clicked(row_value, delete_button))
            # endregion

            self.primary_data_list_action_panel_layout.addWidget(self.primary_data_list_edit_button)
            self.primary_data_list_action_panel_layout.addWidget(self.primary_data_list_view_button)
            self.primary_data_list_action_panel_layout.addWidget(self.primary_data_list_delete_button)
            self.primary_data_list_action_panel.setLayout(self.primary_data_list_action_panel_layout)
            # endregion
            # region > category_data_list_action
            self.category_data_list_action_panel = MyGroupBox(object_name='data_list_action_panel') # head.a
            self.category_data_list_action_panel_layout = MyHBoxLayout(object_name='data_list_action_panel_layout')
            
            # region > set_category_data_list_action_buttons
            self.category_data_list_edit_button = MyPushButton(object_name='data_list_edit_button', text='Edit')
            self.category_data_list_view_button = MyPushButton(object_name='data_list_view_button', text='View')
            self.category_data_list_delete_button = MyPushButton(object_name='data_list_delete_button')
            # endregion

            # region > category_data_list_action_button_connections
            self.category_data_list_edit_button.clicked.connect(lambda _, row_value=row_value, edit_button=self.category_data_list_edit_button: self.on_data_list_edit_button_clicked(row_value, edit_button))
            self.category_data_list_view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.category_data_list_view_button: self.on_data_list_view_button_clicked(row_value, view_button))
            self.category_data_list_delete_button.clicked.connect(lambda _, row_value=row_value, delete_button=self.category_data_list_delete_button: self.on_data_list_delete_button_clicked(row_value, delete_button))
            # endregion

            self.category_data_list_action_panel_layout.addWidget(self.category_data_list_edit_button)
            self.category_data_list_action_panel_layout.addWidget(self.category_data_list_view_button)
            self.category_data_list_action_panel_layout.addWidget(self.category_data_list_delete_button)
            self.category_data_list_action_panel.setLayout(self.category_data_list_action_panel_layout)
            # endregion
            # region > price_data_list_action
            self.price_data_list_action_panel = MyGroupBox(object_name='data_list_action_panel') # head.a
            self.price_data_list_action_panel_layout = MyHBoxLayout(object_name='data_list_action_panel_layout')
            
            # region > set_price_data_list_action_buttons
            self.price_data_list_edit_button = MyPushButton(object_name='data_list_edit_button', text='Edit')
            self.price_data_list_view_button = MyPushButton(object_name='data_list_view_button', text='View')
            self.price_data_list_delete_button = MyPushButton(object_name='data_list_delete_button')
            # endregion

            # region > price_data_list_action_button_connections
            self.price_data_list_edit_button.clicked.connect(lambda _, row_value=row_value, edit_button=self.price_data_list_edit_button: self.on_data_list_edit_button_clicked(row_value, edit_button))
            self.price_data_list_view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.price_data_list_view_button: self.on_data_list_view_button_clicked(row_value, view_button))
            self.price_data_list_delete_button.clicked.connect(lambda _, row_value=row_value, delete_button=self.price_data_list_delete_button: self.on_data_list_delete_button_clicked(row_value, delete_button))
            # endregion

            self.price_data_list_action_panel_layout.addWidget(self.price_data_list_edit_button)
            self.price_data_list_action_panel_layout.addWidget(self.price_data_list_view_button)
            self.price_data_list_action_panel_layout.addWidget(self.price_data_list_delete_button)
            self.price_data_list_action_panel.setLayout(self.price_data_list_action_panel_layout)
            # endregion

            # region > style_data_list_action_buttons
            self.style_data_list_action_button()
            # endregion

            # region > set_table_item_values
            barcode = QTableWidgetItem(str(row_value[0]))
            item_name = [
                QTableWidgetItem(str(row_value[1])),
                QTableWidgetItem(str(row_value[1])),
                QTableWidgetItem(str(row_value[1])),
                QTableWidgetItem(str(row_value[1]))
            ]
            expire_dt = QTableWidgetItem(str(row_value[2]))

            item_type = QTableWidgetItem(str(row_value[3]))
            brand = [
                QTableWidgetItem(str(row_value[4])),
                QTableWidgetItem(str(row_value[4]))
            ]
            sales_group = [
                QTableWidgetItem(str(row_value[5])),
                QTableWidgetItem(str(row_value[5]))
            ]
            supplier = QTableWidgetItem(str(row_value[6]))

            cost = QTableWidgetItem(f'₱{row_value[7]:.2f}')
            sell_price = [
                QTableWidgetItem(f'₱{row_value[8]:.2f}'),
                QTableWidgetItem(f'₱{row_value[8]:.2f}')
            ]
            effective_dt = [
                QTableWidgetItem(str(row_value[9])),
                QTableWidgetItem(str(row_value[9]))
            ]
            promo_name = [
                QTableWidgetItem(str(row_value[10])),
                QTableWidgetItem(str(row_value[10]))
            ]
            discount_value = [
                QTableWidgetItem(f'₱{row_value[11]:.2f}'),
                QTableWidgetItem(f'₱{row_value[11]:.2f}')
            ]

            inventory_tracking = [
                QTableWidgetItem(str(row_value[12])),
                QTableWidgetItem(str(row_value[12])),
                QTableWidgetItem(str(row_value[12])),
                QTableWidgetItem(str(row_value[12])),
                QTableWidgetItem(str(row_value[12]))
            ]

            update_ts = [
                QTableWidgetItem(str(row_value[15])),
                QTableWidgetItem(str(row_value[15])),
                QTableWidgetItem(str(row_value[15])),
                QTableWidgetItem(str(row_value[15])),
                QTableWidgetItem(str(row_value[15]))
            ]
            # endregion
            # region > set_table_item_alignment
            expire_dt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            for sg in sales_group: sg.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            supplier.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            cost.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            for sp in sell_price: sp.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            for ed in effective_dt: ed.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            for dv in discount_value: dv.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            
            for it in inventory_tracking: it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            for ut in update_ts: ut.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # endregion
        
            # region > set_data_list_table_cells
            # region > overview
            self.data_list_table.setCellWidget(row_index, 0, self.data_list_action_panel)
            self.data_list_table.setItem(row_index, 1, item_name[0])
            self.data_list_table.setItem(row_index, 2, brand[0])
            self.data_list_table.setItem(row_index, 3, sales_group[0])
            self.data_list_table.setItem(row_index, 4, sell_price[0])
            self.data_list_table.setItem(row_index, 5, discount_value[0])
            self.data_list_table.setItem(row_index, 6, effective_dt[0])
            self.data_list_table.setItem(row_index, 7, promo_name[0])
            self.data_list_table.setItem(row_index, 8, inventory_tracking[0])
            self.data_list_table.setItem(row_index, 9, update_ts[0])
            # endregion
            # region > primary
            self.primary_data_list_table.setCellWidget(row_index, 0, self.primary_data_list_action_panel)
            self.primary_data_list_table.setItem(row_index, 1, barcode)
            self.primary_data_list_table.setItem(row_index, 2, item_name[1])
            self.primary_data_list_table.setItem(row_index, 3, expire_dt)
            self.primary_data_list_table.setItem(row_index, 4, update_ts[1])
            # endregion
            # region > category
            self.category_data_list_table.setCellWidget(row_index, 0, self.category_data_list_action_panel)
            self.category_data_list_table.setItem(row_index, 1, item_name[2])
            self.category_data_list_table.setItem(row_index, 2, item_type)
            self.category_data_list_table.setItem(row_index, 3, brand[1])
            self.category_data_list_table.setItem(row_index, 4, sales_group[1])
            self.category_data_list_table.setItem(row_index, 5, supplier)
            self.category_data_list_table.setItem(row_index, 6, update_ts[2])
            # endregion
            # region > price
            self.price_data_list_table.setCellWidget(row_index, 0, self.price_data_list_action_panel)
            self.price_data_list_table.setItem(row_index, 1, item_name[3])
            self.price_data_list_table.setItem(row_index, 2, cost)
            self.price_data_list_table.setItem(row_index, 3, sell_price[1])
            self.price_data_list_table.setItem(row_index, 4, discount_value[1])
            self.price_data_list_table.setItem(row_index, 5, effective_dt[1])
            self.price_data_list_table.setItem(row_index, 6, promo_name[1])
            self.price_data_list_table.setItem(row_index, 7, update_ts[3])
            # endregion
            # endregion

            # region > colored_rows_if_has_promo
            if row_value[18] != 0:
                barcode.setForeground(QColor(204,49,61))
                expire_dt.setForeground(QColor(204,49,61))
                item_type.setForeground(QColor(204,49,61))
                supplier.setForeground(QColor(204,49,61))
                cost.setForeground(QColor(204,49,61))

                for itn in item_name: itn.setForeground(QColor(204,49,61))
                for br in brand: br.setForeground(QColor(204,49,61))
                for sg in sales_group: sg.setForeground(QColor(204,49,61))
                for sp in sell_price: sp.setForeground(QColor(204,49,61))
                for ed in effective_dt: ed.setForeground(QColor(204,49,61))
                for pn in promo_name: pn.setForeground(QColor(204,49,61))
                for dv in discount_value: dv.setForeground(QColor(204,49,61))
                for it in inventory_tracking: it.setForeground(QColor(204,49,61))
                for ut in update_ts: ut.setForeground(QColor(204,49,61))

                self.data_list_edit_button.hide()
            # endregion

        for row_index, row_value in enumerate(inventory_data):
            # region > inventory_data_list_action
            self.inventory_data_list_action_panel = MyGroupBox(object_name='data_list_action_panel') # head.a
            self.inventory_data_list_action_panel_layout = MyHBoxLayout(object_name='data_list_action_panel_layout')
            
            # region > set_inventory_data_list_action_buttons
            self.inventory_data_list_edit_button = MyPushButton(object_name='data_list_edit_button', text='Edit')
            self.inventory_data_list_view_button = MyPushButton(object_name='data_list_view_button', text='View')
            self.inventory_data_list_delete_button = MyPushButton(object_name='data_list_delete_button')
            # endregion

            # region > inventory_data_list_action_button_connections
            self.inventory_data_list_edit_button.clicked.connect(lambda _, row_value=row_value, edit_button=self.inventory_data_list_edit_button: self.on_inventory_data_list_edit_button_clicked(row_value, edit_button))
            self.inventory_data_list_view_button.clicked.connect(lambda _, row_value=row_value, view_button=self.inventory_data_list_view_button: self.on_inventory_data_list_view_button_clicked(row_value, view_button))
            self.inventory_data_list_delete_button.clicked.connect(lambda _, row_value=row_value, delete_button=self.inventory_data_list_delete_button: self.on_inventory_data_list_delete_button_clicked(row_value, delete_button))
            # endregion

            self.inventory_data_list_action_panel_layout.addWidget(self.inventory_data_list_edit_button)
            self.inventory_data_list_action_panel_layout.addWidget(self.inventory_data_list_view_button)
            self.inventory_data_list_action_panel_layout.addWidget(self.inventory_data_list_delete_button)
            self.inventory_data_list_action_panel.setLayout(self.inventory_data_list_action_panel_layout)
            # endregion

            # region > style_data_list_action_buttons
            self.style_inventory_data_list_action_button()
            # endregion

            # region > set_table_item_values
            item_name = QTableWidgetItem(str(row_value[0]))
            available_stock = QTableWidgetItem(str(row_value[1]))
            on_hand_stock = QTableWidgetItem(str(row_value[2]))
            update_ts = QTableWidgetItem(str(row_value[3]))
            # endregion

            # region > set_table_item_alignment
            available_stock.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            on_hand_stock.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            update_ts.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # endregion
        

            self.inventory_data_list_table.setCellWidget(row_index, 0, self.inventory_data_list_action_panel)
            self.inventory_data_list_table.setItem(row_index, 1, item_name)
            self.inventory_data_list_table.setItem(row_index, 2, available_stock)
            self.inventory_data_list_table.setItem(row_index, 3, on_hand_stock)
            self.inventory_data_list_table.setItem(row_index, 4, update_ts)
            # !!! CHECKPOINT !!!
        pass

    def show_extra_info_panel(self):
        self.extra_info_panel = MyGroupBox(object_name='extra_info_panel') # head.d
        self.extra_info_panel_layout = MyHBoxLayout(object_name='extra_info_panel_layout')

        # region > extra_info_labels
        self.total_data = MyLabel(object_name='total_data', text=f'Total product: {self.total_row_count}')
        # endregion

        self.extra_info_panel_layout.addWidget(self.total_data,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.extra_info_panel.setLayout(self.extra_info_panel_layout)
        pass
    def show_form_panel(self):
        self.form_panel = MyGroupBox(object_name='form_panel')
        self.form_panel_layout = MyVBoxLayout(object_name='form_panel_layout')

        # region > form_scroll_area
        self.form_scroll_area = MyScrollArea(object_name='form_scroll_area') # head.a
        self.form_page = MyGroupBox(object_name='form_page')
        self.form_page_layout = MyFormLayout(object_name='form_page_layout')

        # region > primary_info_page
        self.primary_info_page = MyGroupBox(object_name='primary_info_page') # head.a.a
        self.primary_info_page_layout = MyFormLayout(object_name='primary_info_page_layout')

        self.barcode_label = MyLabel(object_name='barcode_label', text=f'Barcode')
        self.item_name_label = MyLabel(object_name='item_name_label', text=f'Item name {self.required_field_indicator}')
        self.expire_dt_label = MyLabel(object_name='expire_dt_label', text=f'Expire date')

        self.barcode_field = MyLineEdit(object_name='barcode_field')
        self.item_name_field = MyLineEdit(object_name='item_name_field')
        self.expire_dt_field = MyDateEdit(object_name='expire_dt_field')

        self.item_name_field.textChanged.connect(self.on_item_name_field_text_changed)

        self.primary_info_page_layout.insertRow(0, QLabel(f"<font color='{color_scheme.hex_main}'><b>Primary Information</b></font>"))
        self.primary_info_page_layout.insertRow(1, QLabel('<hr>'))

        self.primary_info_page_layout.insertRow(2, self.barcode_label)
        self.primary_info_page_layout.insertRow(4, self.item_name_label)
        self.primary_info_page_layout.insertRow(6, self.expire_dt_label)

        self.primary_info_page_layout.insertRow(3, self.barcode_field)
        self.primary_info_page_layout.insertRow(5, self.item_name_field)
        self.primary_info_page_layout.insertRow(7, self.expire_dt_field)

        self.primary_info_page.setLayout(self.primary_info_page_layout)
        # endregion
        # region > category_info_page
        self.category_info_page = MyGroupBox(object_name='category_info_page') # head.a.a
        self.category_info_page_layout = MyFormLayout(object_name='category_info_page_layout')

        self.item_type_label = MyLabel(object_name='item_type_label', text=f'Item type {self.required_field_indicator}')
        self.brand_label = MyLabel(object_name='brand_label', text=f'Brand {self.required_field_indicator}')
        self.sales_group_label = MyLabel(object_name='sales_group_label', text=f'Sales group')
        self.supplier_label = MyLabel(object_name='supplier_label', text=f'Supplier {self.required_field_indicator}')

        self.item_type_field = MyComboBox(object_name='item_type_field')
        self.brand_field = MyComboBox(object_name='brand_field')
        self.sales_group_field = MyComboBox(object_name='sales_group_field')
        self.supplier_field = MyComboBox(object_name='supplier_field')

        self.item_type_field.currentTextChanged.connect(self.on_item_type_field_current_text_changed)
        self.brand_field.currentTextChanged.connect(self.on_brand_field_current_text_changed)
        self.supplier_field.currentTextChanged.connect(self.on_supplier_field_current_text_changed)

        self.category_info_page_layout.insertRow(0, QLabel(f"<font color='{color_scheme.hex_main}'><b>Category</b></font>"))
        self.category_info_page_layout.insertRow(1, QLabel('<hr>'))

        self.category_info_page_layout.insertRow(2, self.item_type_label)
        self.category_info_page_layout.insertRow(4, self.brand_label)
        self.category_info_page_layout.insertRow(6, self.sales_group_label)
        self.category_info_page_layout.insertRow(8, self.supplier_label)

        self.category_info_page_layout.insertRow(3, self.item_type_field)
        self.category_info_page_layout.insertRow(5, self.brand_field)
        self.category_info_page_layout.insertRow(7, self.sales_group_field)
        self.category_info_page_layout.insertRow(9, self.supplier_field)

        self.category_info_page.setLayout(self.category_info_page_layout)
        # endregion
        # region > price_info_page
        self.price_info_page = MyGroupBox(object_name='price_info_page') # head.a.a
        self.price_info_page_layout = MyFormLayout(object_name='price_info_page_layout')

        self.cost_label = MyLabel(object_name='cost_label', text=f'Cost {self.required_field_indicator}')
        self.sell_price_label = MyLabel(object_name='sell_price_label', text=f'Sell price {self.required_field_indicator}')
        self.effective_dt_label = MyLabel(object_name='effective_dt_label', text=f'Effective date')
        self.promo_name_label = MyLabel(object_name='promo_name_label', text=f'Promo name')
        self.promo_type_label = MyLabel(object_name='promo_type_label', text=f'Promo type')
        self.discount_percent_label = MyLabel(object_name='discount_percent_label', text=f'Discount percent')
        self.discount_value_label = MyLabel(object_name='discount_value_label', text=f'Discount value')
        self.new_sell_price_label = MyLabel(object_name='new_sell_price_label', text=f'New sell price')
        self.start_dt_label = MyLabel(object_name='start_dt_label', text=f'Start date')
        self.end_dt_label = MyLabel(object_name='end_dt_label', text=f'End date')

        self.cost_field = MyLineEdit(object_name='cost_field')
        self.sell_price_field = MyLineEdit(object_name='sell_price_field')
        self.effective_dt_field = MyDateEdit(object_name='effective_dt_field')
        self.promo_name_field = MyComboBox(object_name='promo_name_field')
        self.promo_type_field = MyLineEdit(object_name='promo_type_field')
        self.discount_percent_field = MyLineEdit(object_name='discount_percent_field')
        self.discount_value_field = MyLineEdit(object_name='discount_value_field')
        self.new_sell_price_field = MyLineEdit(object_name='new_sell_price_field')
        self.start_dt_field = MyDateEdit(object_name='start_dt_field')
        self.end_dt_field = MyDateEdit(object_name='end_dt_field')

        self.cost_field.textChanged.connect(self.on_cost_field_text_changed)
        self.sell_price_field.textChanged.connect(self.on_sell_price_field_text_changed)
        self.promo_name_field.currentTextChanged.connect(self.on_promo_name_field_current_text_changed)

        self.price_info_page_layout.insertRow(0, QLabel(f"<font color='{color_scheme.hex_main}'><b>Price</b></font>"))
        self.price_info_page_layout.insertRow(1, QLabel('<hr>'))

        self.price_info_page_layout.insertRow(2, self.cost_label)
        self.price_info_page_layout.insertRow(4, self.sell_price_label)
        self.price_info_page_layout.insertRow(6, self.effective_dt_label)
        self.price_info_page_layout.insertRow(8, self.promo_name_label)
        self.price_info_page_layout.insertRow(10, self.promo_type_label)
        self.price_info_page_layout.insertRow(12, self.discount_percent_label)
        self.price_info_page_layout.insertRow(14, self.discount_value_label)
        self.price_info_page_layout.insertRow(16, self.new_sell_price_label)
        self.price_info_page_layout.insertRow(18, self.start_dt_label)
        self.price_info_page_layout.insertRow(20, self.end_dt_label)

        self.price_info_page_layout.insertRow(3, self.cost_field)
        self.price_info_page_layout.insertRow(5, self.sell_price_field)
        self.price_info_page_layout.insertRow(7, self.effective_dt_field)
        self.price_info_page_layout.insertRow(9, self.promo_name_field)
        self.price_info_page_layout.insertRow(11, self.promo_type_field)
        self.price_info_page_layout.insertRow(13, self.discount_percent_field)
        self.price_info_page_layout.insertRow(15, self.discount_value_field)
        self.price_info_page_layout.insertRow(17, self.new_sell_price_field)
        self.price_info_page_layout.insertRow(19, self.start_dt_field)
        self.price_info_page_layout.insertRow(21, self.end_dt_field)

        self.price_info_page.setLayout(self.price_info_page_layout)
        # endregion
        # region > inventory_info_page
        self.inventory_info_page = MyGroupBox(object_name='inventory_info_page') # head.a.a
        self.inventory_info_page_layout = MyFormLayout(object_name='inventory_info_page_layout')

        self.inventory_tracking_label = MyLabel(object_name='inventory_tracking_label', text=f'Inventory tracking')
        self.inventory_item_name_label = MyLabel(object_name='item_name_label', text=f'Item name')
        self.available_stock_label = MyLabel(object_name='available_stock_label', text=f'Available stock {self.required_field_indicator}')
        self.on_hand_stock_label = MyLabel(object_name='on_hand_stock_label', text=f'On hand stock {self.required_field_indicator}')

        self.inventory_tracking_field = MyComboBox(object_name='inventory_tracking_field')
        self.inventory_item_name_field = MyLineEdit(object_name='item_name_field')
        self.available_stock_field = MyLineEdit(object_name='available_stock_field')
        self.on_hand_stock_field = MyLineEdit(object_name='on_hand_stock_field')

        self.inventory_tracking_field.currentTextChanged.connect(self.on_inventory_tracking_field_current_text_changed)
        self.available_stock_field.textChanged.connect(self.on_available_stock_field_text_changed)
        self.on_hand_stock_field.textChanged.connect(self.on_on_hand_stock_field_text_changed)

        self.inventory_info_page_layout.insertRow(0, QLabel(f"<font color='{color_scheme.hex_main}'><b>Inventory</b></font>"))
        self.inventory_info_page_layout.insertRow(1, QLabel('<hr>'))

        self.inventory_info_page_layout.insertRow(2, self.inventory_tracking_label)
        self.inventory_info_page_layout.insertRow(4, self.inventory_item_name_label)
        self.inventory_info_page_layout.insertRow(6, self.available_stock_label)
        self.inventory_info_page_layout.insertRow(8, self.on_hand_stock_label)

        self.inventory_info_page_layout.insertRow(3, self.inventory_tracking_field)
        self.inventory_info_page_layout.insertRow(5, self.inventory_item_name_field)
        self.inventory_info_page_layout.insertRow(7, self.available_stock_field)
        self.inventory_info_page_layout.insertRow(9, self.on_hand_stock_field)



        self.inventory_info_page.setLayout(self.inventory_info_page_layout)
        # endregion

        self.form_page_layout.addRow(self.primary_info_page)
        self.form_page_layout.addRow(self.category_info_page)
        self.form_page_layout.addRow(self.price_info_page)
        self.form_page_layout.addRow(self.inventory_info_page)
        self.form_page.setLayout(self.form_page_layout)
        self.form_scroll_area.setWidget(self.form_page)
        # endregion
        # region > form_action
        self.form_action_panel = MyGroupBox(object_name='form_action_panel') # head.b
        self.form_action_panel_layout = MyHBoxLayout(object_name='form_action_panel_layout')
        self.form_close_button = MyPushButton(object_name='form_close_button', text='Close')
        self.form_save_new_button = MyPushButton(object_name='form_save_new_button', text='SAVE NEW')
        self.form_save_edit_button = MyPushButton(object_name='form_save_edit_button', text='SAVE EDIT')
        self.form_action_panel_layout.addWidget(self.form_close_button)
        self.form_action_panel_layout.addWidget(self.form_save_new_button)
        self.form_action_panel_layout.addWidget(self.form_save_edit_button)
        self.form_action_panel.setLayout(self.form_action_panel_layout)
        # endregion

        # region > form_button_connections
        self.form_close_button.clicked.connect(self.on_form_close_button_clicked)
        self.form_save_new_button.clicked.connect(self.on_form_save_new_button_clicked)
        self.form_save_edit_button.clicked.connect(self.on_form_save_edit_button_clicked)
        # endregion
        
        # region > style_form_buttons
        self.style_form_action_button()
        # endregion

        self.form_panel_layout.addWidget(self.form_scroll_area)
        self.form_panel_layout.addWidget(self.form_action_panel)
        self.form_panel.setLayout(self.form_panel_layout)
        pass
    def show_content_panel(self):
        self.content_panel = MyGroupBox(object_name='content_panel')
        self.content_panel_layout = MyGridLayout(object_name='content_panel_layout')

        # region > text_filter
        self.text_filter_field = MyLineEdit(object_name='text_filter_field') # head.a
        # endregion
        # region > data_mgt_action
        self.data_mgt_action_panel = MyGroupBox(object_name='data_mgt_action_panel') # head.b
        self.data_mgt_action_panel_layout = MyHBoxLayout(object_name='data_mgt_action_panel_layout')
        self.data_mgt_sync_button = MyPushButton(object_name='data_mgt_sync_button')
        self.data_mgt_import_button = MyPushButton(object_name='data_mgt_import_button')
        self.data_mgt_add_button = MyPushButton(object_name='data_mgt_add_button', text=' Add Product')
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_sync_button)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_import_button)
        self.data_mgt_action_panel_layout.addWidget(self.data_mgt_add_button)
        self.data_mgt_action_panel.setLayout(self.data_mgt_action_panel_layout)
        # endregion
        # region > data_list_sorter
        self.data_list_sorter_tab = MyTabWidget(object_name='data_list_sorter_tab') # head.c

        # region > data_list_pgn_panel
        self.data_list_pgn_panel = MyGroupBox(object_name='data_list_pgn_panel') # head.c.a
        self.data_list_pgn_panel_layout = MyVBoxLayout(object_name='data_list_pgn_panel_layout')
        self.data_list_table = MyTableWidget(object_name='data_list_table')
        self.data_list_pgn_action_panel = MyGroupBox(object_name='data_list_pgn_action_panel')
        self.data_list_pgn_action_panel_layout = MyGridLayout(object_name='data_list_pgn_action_panel_layout')
        self.data_list_pgn_prev_button = MyPushButton(object_name='data_list_pgn_prev_button')
        self.data_list_pgn_page = MyLabel(object_name='data_list_pgn_page', text='Page 1')
        self.data_list_pgn_next_button = MyPushButton(object_name='data_list_pgn_next_button')
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_prev_button,0,0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_page,0,1, Qt.AlignmentFlag.AlignCenter)
        self.data_list_pgn_action_panel_layout.addWidget(self.data_list_pgn_next_button,0,2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.data_list_pgn_action_panel.setLayout(self.data_list_pgn_action_panel_layout)
        self.data_list_pgn_panel_layout.addWidget(self.data_list_table)
        self.data_list_pgn_panel_layout.addWidget(self.data_list_pgn_action_panel)
        self.data_list_pgn_panel.setLayout(self.data_list_pgn_panel_layout)
        # endregion
        # region > primary_data_list_pgn_panel
        self.primary_data_list_pgn_panel = MyGroupBox(object_name='primary_data_list_pgn_panel') # head.c.a
        self.primary_data_list_pgn_panel_layout = MyVBoxLayout(object_name='primary_data_list_pgn_panel_layout')
        self.primary_data_list_table = MyTableWidget(object_name='primary_data_list_table')
        self.primary_data_list_pgn_action_panel = MyGroupBox(object_name='data_list_pgn_action_panel')
        self.primary_data_list_pgn_action_panel_layout = MyGridLayout(object_name='data_list_pgn_action_panel_layout')
        self.primary_data_list_pgn_prev_button = MyPushButton(object_name='data_list_pgn_prev_button')
        self.primary_data_list_pgn_page = MyLabel(object_name='data_list_pgn_page', text='Page 1')
        self.primary_data_list_pgn_next_button = MyPushButton(object_name='data_list_pgn_next_button')
        self.primary_data_list_pgn_action_panel_layout.addWidget(self.primary_data_list_pgn_prev_button,0,0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.primary_data_list_pgn_action_panel_layout.addWidget(self.primary_data_list_pgn_page,0,1, Qt.AlignmentFlag.AlignCenter)
        self.primary_data_list_pgn_action_panel_layout.addWidget(self.primary_data_list_pgn_next_button,0,2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.primary_data_list_pgn_action_panel.setLayout(self.primary_data_list_pgn_action_panel_layout)
        self.primary_data_list_pgn_panel_layout.addWidget(self.primary_data_list_table)
        self.primary_data_list_pgn_panel_layout.addWidget(self.primary_data_list_pgn_action_panel)
        self.primary_data_list_pgn_panel.setLayout(self.primary_data_list_pgn_panel_layout)
        # endregion
        # region > category_data_list_pgn_panel
        self.category_data_list_pgn_panel = MyGroupBox(object_name='category_data_list_pgn_panel') # head.c.a
        self.category_data_list_pgn_panel_layout = MyVBoxLayout(object_name='category_data_list_pgn_panel_layout')
        self.category_data_list_table = MyTableWidget(object_name='category_data_list_table')
        self.category_data_list_pgn_action_panel = MyGroupBox(object_name='data_list_pgn_action_panel')
        self.category_data_list_pgn_action_panel_layout = MyGridLayout(object_name='data_list_pgn_action_panel_layout')
        self.category_data_list_pgn_prev_button = MyPushButton(object_name='data_list_pgn_prev_button')
        self.category_data_list_pgn_page = MyLabel(object_name='data_list_pgn_page', text='Page 1')
        self.category_data_list_pgn_next_button = MyPushButton(object_name='data_list_pgn_next_button')
        self.category_data_list_pgn_action_panel_layout.addWidget(self.category_data_list_pgn_prev_button,0,0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.category_data_list_pgn_action_panel_layout.addWidget(self.category_data_list_pgn_page,0,1, Qt.AlignmentFlag.AlignCenter)
        self.category_data_list_pgn_action_panel_layout.addWidget(self.category_data_list_pgn_next_button,0,2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.category_data_list_pgn_action_panel.setLayout(self.category_data_list_pgn_action_panel_layout)
        self.category_data_list_pgn_panel_layout.addWidget(self.category_data_list_table)
        self.category_data_list_pgn_panel_layout.addWidget(self.category_data_list_pgn_action_panel)
        self.category_data_list_pgn_panel.setLayout(self.category_data_list_pgn_panel_layout)
        # endregion
        # region > price_data_list_pgn_panel
        self.price_data_list_pgn_panel = MyGroupBox(object_name='price_data_list_pgn_panel') # head.c.a
        self.price_data_list_pgn_panel_layout = MyVBoxLayout(object_name='price_data_list_pgn_panel_layout')
        self.price_data_list_table = MyTableWidget(object_name='price_data_list_table')
        self.price_data_list_pgn_action_panel = MyGroupBox(object_name='data_list_pgn_action_panel')
        self.price_data_list_pgn_action_panel_layout = MyGridLayout(object_name='data_list_pgn_action_panel_layout')
        self.price_data_list_pgn_prev_button = MyPushButton(object_name='data_list_pgn_prev_button')
        self.price_data_list_pgn_page = MyLabel(object_name='data_list_pgn_page', text='Page 1')
        self.price_data_list_pgn_next_button = MyPushButton(object_name='data_list_pgn_next_button')
        self.price_data_list_pgn_action_panel_layout.addWidget(self.price_data_list_pgn_prev_button,0,0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.price_data_list_pgn_action_panel_layout.addWidget(self.price_data_list_pgn_page,0,1, Qt.AlignmentFlag.AlignCenter)
        self.price_data_list_pgn_action_panel_layout.addWidget(self.price_data_list_pgn_next_button,0,2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.price_data_list_pgn_action_panel.setLayout(self.price_data_list_pgn_action_panel_layout)
        self.price_data_list_pgn_panel_layout.addWidget(self.price_data_list_table)
        self.price_data_list_pgn_panel_layout.addWidget(self.price_data_list_pgn_action_panel)
        self.price_data_list_pgn_panel.setLayout(self.price_data_list_pgn_panel_layout)
        # endregion
        # region > inventory_data_list_pgn_panel
        self.inventory_data_list_pgn_panel = MyGroupBox(object_name='inventory_data_list_pgn_panel') # head.c.a
        self.inventory_data_list_pgn_panel_layout = MyVBoxLayout(object_name='inventory_data_list_pgn_panel_layout')
        self.inventory_data_list_table = MyTableWidget(object_name='inventory_data_list_table')
        self.inventory_data_list_pgn_action_panel = MyGroupBox(object_name='data_list_pgn_action_panel')
        self.inventory_data_list_pgn_action_panel_layout = MyGridLayout(object_name='data_list_pgn_action_panel_layout')
        self.inventory_data_list_pgn_prev_button = MyPushButton(object_name='data_list_pgn_prev_button')
        self.inventory_data_list_pgn_page = MyLabel(object_name='data_list_pgn_page', text='Page 1')
        self.inventory_data_list_pgn_next_button = MyPushButton(object_name='data_list_pgn_next_button')
        self.inventory_data_list_pgn_action_panel_layout.addWidget(self.inventory_data_list_pgn_prev_button,0,0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_data_list_pgn_action_panel_layout.addWidget(self.inventory_data_list_pgn_page,0,1, Qt.AlignmentFlag.AlignCenter)
        self.inventory_data_list_pgn_action_panel_layout.addWidget(self.inventory_data_list_pgn_next_button,0,2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.inventory_data_list_pgn_action_panel.setLayout(self.inventory_data_list_pgn_action_panel_layout)
        self.inventory_data_list_pgn_panel_layout.addWidget(self.inventory_data_list_table)
        self.inventory_data_list_pgn_panel_layout.addWidget(self.inventory_data_list_pgn_action_panel)
        self.inventory_data_list_pgn_panel.setLayout(self.inventory_data_list_pgn_panel_layout)
        # endregion

        self.data_list_sorter_tab.addTab(self.data_list_pgn_panel, 'Overview')
        self.data_list_sorter_tab.addTab(self.primary_data_list_pgn_panel, 'Primary')
        self.data_list_sorter_tab.addTab(self.category_data_list_pgn_panel, 'Category')
        self.data_list_sorter_tab.addTab(self.price_data_list_pgn_panel, 'Price')
        self.data_list_sorter_tab.addTab(self.inventory_data_list_pgn_panel, 'Inventory')
        # endregion

        # region > content_button_connections
        self.data_mgt_sync_button.clicked.connect(self.on_data_mgt_sync_button_clicked)
        self.data_mgt_import_button.clicked.connect(self.on_data_mgt_import_button_clicked)
        self.data_mgt_add_button.clicked.connect(self.on_data_mgt_add_button_clicked)

        # region > data_list_pgn_button
        self.data_list_pgn_prev_button.clicked.connect(self.on_data_list_pgn_prev_button_clicked)
        self.primary_data_list_pgn_prev_button.clicked.connect(self.on_data_list_pgn_prev_button_clicked)
        self.category_data_list_pgn_prev_button.clicked.connect(self.on_data_list_pgn_prev_button_clicked)
        self.price_data_list_pgn_prev_button.clicked.connect(self.on_data_list_pgn_prev_button_clicked)
        self.inventory_data_list_pgn_prev_button.clicked.connect(self.on_data_list_pgn_prev_button_clicked)

        self.data_list_pgn_next_button.clicked.connect(self.on_data_list_pgn_next_button_clicked)
        self.primary_data_list_pgn_next_button.clicked.connect(self.on_data_list_pgn_next_button_clicked)
        self.category_data_list_pgn_next_button.clicked.connect(self.on_data_list_pgn_next_button_clicked)
        self.price_data_list_pgn_next_button.clicked.connect(self.on_data_list_pgn_next_button_clicked)
        self.inventory_data_list_pgn_next_button.clicked.connect(self.on_data_list_pgn_next_button_clicked)
        # endregion
        # endregion
        # region > content_text_filter_connection
        self.text_filter_field.textChanged.connect(self.on_text_filter_field_text_changed)
        # endregion
        # region > style_content_buttons
        self.style_data_mgt_action_button()
        self.style_data_list_pgn_action_button()
        # endregion

        self.content_panel_layout.addWidget(self.text_filter_field,0,0,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.content_panel_layout.addWidget(self.data_mgt_action_panel,0,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.content_panel_layout.addWidget(self.data_list_sorter_tab,1,0,1,2)
        self.content_panel.setLayout(self.content_panel_layout)
        pass
    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(object_name='main_panel_layout')

        self.show_content_panel()
        self.show_form_panel()
        self.show_extra_info_panel()

        self.main_panel_layout.addWidget(self.content_panel,0,0)
        self.main_panel_layout.addWidget(self.form_panel,0,1,2,1)
        self.main_panel_layout.addWidget(self.extra_info_panel,1,0)
        self.setLayout(self.main_panel_layout)
    
if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(pos_app.exec())
