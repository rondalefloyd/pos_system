import sqlite3
import sys, os
import pandas as pd
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from other.csv_importer import *    
from schema.sales_table_schema import *
from schema.promo_management_schema import *
from widget.promo_management_widget import *

class ProductManagementLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.promo_management_schema = PromoManagementSchema()
        self.sales_table_schema = SalesTableSchema()
        self.sales_table_schema.setup_sales_table()

        self.default_values()
        self.show_main_panel()
        self.refresh_data()

    def default_values(self):
        self.current_page = 1
        self.tab_table_page = 1
        self.required_marker = "<font color='red'><b>!</font>"
        self.selected_promo_name = '[no promo selected]'
          
    def edit_data(self, row_value):
        self.promo_name_field.setText(str(row_value[0]))
        self.promo_type_field.setCurrentText(str(row_value[1]))
        self.discount_percent_field.setText(str(row_value[2]))
        self.description_field.setPlainText(str(row_value[3]))

        self.selected_promo_id = row_value[5]

        pass
    def view_data(self, row_value):
        self.view_data_dialog = CustomDialog(ref='view_data_dialog', parent=self, row_value=row_value)

        pass
    def delete_data(self, row_value):
        promo_id = row_value[5]

        confirmation = QMessageBox.warning(self, 'Confirm', 'Are you sure you want to delete this product?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirmation == QMessageBox.StandardButton.Yes:
            self.promo_management_schema.delete_selected_promo(promo_id)
        pass

    def refresh_data(self):
        self.populate_combo_box()
        self.populate_table()
        print('refreshed!')
        pass
    def delete_all_data(self):
        confirmation_a = QMessageBox.warning(self, 'Confirm', 'Are you sure you want to delete all product?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation_a == QMessageBox.StandardButton.Yes:
            confirmation_b = QMessageBox.warning(self, 'Confirm', 'This will delete all product in the database. Proceed?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation_b == QMessageBox.StandardButton.Yes:
                while True:
                    confirmation_c, yes = QInputDialog.getText(self, 'Confirm', "Type <b>'delete all'</b> to confirm")

                    if yes:
                        if confirmation_c == 'delete all':
                            self.promo_management_schema.delete_all_promo()
                            break
                        else:
                            QMessageBox.critical(self, 'Error', 'Invalid input. Please try again.')
                    
                    else:
                        break

        self.delete_all_button.setDisabled(False)
        pass
    def import_data(self):
        self.import_button.setDisabled(True)

        csv_file, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')

        if csv_file:
            data_frame = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)
            
            self.import_thread = CustomThread(csv_file, import_button=self.import_button)
            self.import_thread.progress_signal.connect(self.import_thread.update_progress)
            self.import_thread.finished_signal.connect(self.import_thread.import_finished)
            self.import_thread.error_signal.connect(self.import_thread.import_error)
            self.import_thread.start()
            print(data_frame)
            pass
        else:
            self.import_button.setDisabled(False)
        pass
    def add_data(self):
        # region: set default input on form fields (for adding)
        self.promo_name_field.setText('')
        self.promo_type_field.setCurrentText('')
        self.discount_percent_field.setText('')
        self.description_field.setPlainText('')
        # endregion: set default input on form fields (for adding)
        pass

    def save_new_data(self):
        # region: get fields' input
        promo_name = self.promo_name_field.text()
        promo_type = self.promo_type_field.currentText()
        discount_percent = self.discount_percent_field.text()
        description = self.description_field.toPlainText()
        # endregion: get fields' input

        # region: assign values if data is an empty string
        description = '[no data]' if description == '' else description
        # endregion: assign values if data is an empty string

        self.promo_management_schema.add_new_promo(
                # region: params
                promo_name=promo_name,
                promo_type=promo_type,
                discount_percent=discount_percent,
                description=description
                # endregion: params
        )
        pass
    def save_edit_data(self):
        # region: assign input values to variables
        promo_name = self.promo_name_field.text()
        promo_type = self.promo_type_field.currentText()
        discount_percent = self.discount_percent_field.text()
        description = self.description_field.toPlainText()

        # selected data identifier
        promo_id = self.selected_promo_id
        # endregion: assign input values to variables

        self.promo_management_schema.edit_selected_promo(
            promo_name=promo_name,
            promo_type=promo_type,
            discount_percent=discount_percent,
            description=description,

            promo_id=promo_id
        )

        self.selected_promo.setText(f'Selected promo: {promo_name}')

        QMessageBox.information(self, 'Success', 'Product has been edited!')
        pass

    def on_push_button_clicked(self, row_value='', clicked_ref=''):
        if clicked_ref == 'edit_button':
            self.panel_b_box.show()
            self.add_button.setDisabled(False)
            self.selected_data_box.show()
            self.save_new_button.hide()
            self.save_edit_button.show()

            self.selected_promo_name = f'{row_value[0]}'
            self.selected_promo.setText(f'Selected promo: {self.selected_promo_name}')

            self.edit_data(row_value)
            pass
        if clicked_ref == 'view_button':
            self.view_data(row_value)
            pass
        if clicked_ref == 'delete_button':
            self.delete_data(row_value)
            pass

        if clicked_ref == 'previous_button':
            if self.current_page > 1:
                self.current_page -= 1

                # region: pagination page label
                self.overview_pagination_page_label.setText(f'Page {self.current_page}')
                # endregion: pagination page label

            self.populate_table(current_page=self.current_page)
            pass
        if clicked_ref == 'next_button':
            self.current_page += 1

            # region: pagination page label
            self.overview_pagination_page_label.setText(f'Page {self.current_page}')
            # endregion: pagination page label
            
            self.populate_table(current_page=self.current_page)

        if clicked_ref == 'refresh_button':
            self.refresh_data()
            pass
        if clicked_ref == 'delete_all_button':
            self.delete_all_button.setDisabled(True)
            self.delete_all_data()
            pass
        if clicked_ref == 'import_button':
            self.import_data()
            pass
        if clicked_ref == 'add_button':
            self.panel_b_box.show()
            self.add_button.setDisabled(True)
            self.selected_data_box.hide()
            self.save_new_button.show()
            self.save_edit_button.hide()

            self.selected_promo_name = '[no promo selected]'
            self.selected_promo.setText(f'Selected promo: {self.selected_promo_name}')
            
            self.add_data()

        if clicked_ref == 'back_button':
            self.panel_b_box.hide()
            self.add_button.setDisabled(False)       
        if clicked_ref == 'save_new_button':
            self.save_new_data()
            pass
        if clicked_ref == 'save_edit_button':
            self.save_edit_data()
            pass
        pass
    def on_line_edit_text_changed(self, text_changed_ref):
        if text_changed_ref == 'filter_field':
            self.current_page = 1

            # region: pagination page label
            self.overview_pagination_page_label.setText(f'Page {self.current_page}')
            # endregion: pagination page label

            self.populate_table(current_page=self.current_page)
        pass

    def call_signal(
            # region: params
            self,
            edit_button=None,
            view_button=None,
            delete_button=None,
            row_value='',
            signal_ref=''
            # endregion: params
    ):
        if signal_ref == 'panel_a_signal':
            self.filter_field.textChanged.connect(lambda: self.on_line_edit_text_changed(text_changed_ref='filter_field'))

            # region: pagination
            self.overview_pagination_previous_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='previous_button'))
            self.overview_pagination_next_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='next_button'))
            # endregion: pagination
            # region: manage data buttons
            self.refresh_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='refresh_button'))
            self.delete_all_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='delete_all_button'))
            self.add_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='add_button'))
            self.import_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='import_button'))
            # endregion: manage data buttons
            pass
        if signal_ref == 'populate_table_signal':
            edit_button.clicked.connect(lambda: self.on_push_button_clicked(row_value=row_value, clicked_ref='edit_button'))
            view_button.clicked.connect(lambda: self.on_push_button_clicked(row_value=row_value, clicked_ref='view_button'))
            delete_button.clicked.connect(lambda: self.on_push_button_clicked(row_value=row_value, clicked_ref='delete_button'))
            pass

        if signal_ref == 'panel_b_signal':
            self.back_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='back_button'))
            self.save_new_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='save_new_button'))
            self.save_edit_button.clicked.connect(lambda: self.on_push_button_clicked(clicked_ref='save_edit_button'))
            pass

    def populate_combo_box(self):
        promo_type = self.promo_management_schema.list_promo_type()

        self.promo_type_field.addItems(data[0] for data in promo_type)
        pass
    def populate_table(self, current_page=1):
        promo_data = self.promo_management_schema.list_promo(text_filter=self.filter_field.text(), page_number=current_page)

        # region: table pagination button
        self.overview_pagination_previous_button.setEnabled(self.current_page > 1)
        self.overview_pagination_next_button.setEnabled(len(promo_data) == 30)
        # endregion: pagination button
        
        self.overview_table.setRowCount(len(promo_data))

        for row_index, row_value in enumerate(promo_data):
            # region: action button
            table_action_menu = CustomWidget(ref='table_action_menu')
            table_action_menu_layout = CustomHBoxLayout(ref='table_action_menu_layout')
            self.edit_button = CustomPushButton(ref='edit_button')
            self.view_button = CustomPushButton(ref='view_button')
            self.delete_button = CustomPushButton(ref='delete_button')
            table_action_menu_layout.addWidget(self.edit_button)
            table_action_menu_layout.addWidget(self.view_button)
            table_action_menu_layout.addWidget(self.delete_button)
            table_action_menu.setLayout(table_action_menu_layout)

            self.call_signal(
                edit_button=self.edit_button,
                view_button=self.view_button,
                delete_button=self.delete_button,
                row_value=row_value, 
                signal_ref='populate_table_signal'
            )
            pass
            # endregion: action button
        
            promo_name = CustomTableWidgetItem(ref='promo_name', text=f'{row_value[0]}')
            promo_type = CustomTableWidgetItem(ref='promo_type', text=f'{row_value[1]}')
            discount_percent = CustomTableWidgetItem(ref='discount_percent', text=f'₱{row_value[2]}')
            description = CustomTableWidgetItem(ref='description', text=f'{row_value[3]}')
            update_ts = CustomTableWidgetItem(ref='update_ts', text=f'{row_value[4]}')


            # region: overview list
            self.overview_table.setCellWidget(row_index, 0, table_action_menu)
            self.overview_table.setItem(row_index, 1, promo_name)
            self.overview_table.setItem(row_index, 2, promo_type)
            self.overview_table.setItem(row_index, 3, discount_percent)
            self.overview_table.setItem(row_index, 4, description)
            self.overview_table.setItem(row_index, 5, update_ts)
            # endregion: overview list


    def show_panel_b(self):
        self.panel_b_box = CustomGroupBox(ref='panel_b_box')
        self.panel_b_box_layout = CustomFormLayout()
        
        # region: overview fields
        self.overview_box = CustomGroupBox(ref='overview_box')
        self.overview_box_layout = CustomFormLayout()

        self.promo_name_field = CustomLineEdit(ref='promo_name_field')
        self.promo_type_field = CustomComboBox(ref='promo_type_field')
        self.discount_percent_field = CustomLineEdit(ref='discount_percent_field')
        self.description_field = CustomTextEdit(ref='description_field')
        
        self.overview_box_layout.insertRow(0, 'Promo name', self.promo_name_field)
        self.overview_box_layout.insertRow(1, 'Promo type', self.promo_type_field)
        self.overview_box_layout.insertRow(2, 'Discount value', self.discount_percent_field)
        self.overview_box_layout.insertRow(3, 'Description', self.description_field)
        self.overview_box.setLayout(self.overview_box_layout)
        # endregion: overview fields
        # region: form buttons
        self.selected_data_box = CustomGroupBox()
        self.selected_data_layout = CustomFormLayout()
        self.selected_promo = CustomLabel(text=f'Selected promo: {self.selected_promo_name}')
        self.selected_data_layout.addRow(self.selected_promo)
        self.selected_data_box.setLayout(self.selected_data_layout)

        self.panel_b_action_menu = CustomGroupBox()
        self.panel_b_action_menu_layout = CustomGridLayout()
        self.back_button = CustomPushButton(text='Back')
        self.save_new_button = CustomPushButton(text='Save Add')
        self.save_edit_button = CustomPushButton(text='Save Edit')
        self.panel_b_action_menu_layout.addWidget(self.back_button,0,0)
        self.panel_b_action_menu_layout.addWidget(self.save_new_button,0,1)
        self.panel_b_action_menu_layout.addWidget(self.save_edit_button,0,1)
        self.panel_b_action_menu.setLayout(self.panel_b_action_menu_layout)
        # endregion: form buttons

        self.panel_b_box_layout.insertRow(0, self.selected_data_box)
        self.panel_b_box_layout.insertRow(1, self.overview_box)
        self.panel_b_box_layout.insertRow(2, self.panel_b_action_menu)

        self.panel_b_box.setLayout(self.panel_b_box_layout)

        self.call_signal(signal_ref='panel_b_signal')
        pass
    def show_panel_a(self):
        self.panel_a_box = CustomGroupBox()
        self.panel_a_box_layout = CustomGridLayout()

        self.filter_field = CustomLineEdit(ref='filter_field')
        # region: overview pagination table
        self.overview_table = CustomTableWidget(ref='overview_table')
        self.overview_pagination = CustomWidget(ref='overview_pagination')
        self.overview_pagination_layout = CustomGridLayout(ref='overview_pagination_layout')
        self.overview_pagination_previous_button = CustomPushButton(ref='previous_button')
        self.overview_pagination_page_label = CustomLabel(text=f'Page {self.tab_table_page}')
        self.overview_pagination_next_button = CustomPushButton(ref='next_button')
        self.overview_pagination_layout.addWidget(self.overview_pagination_previous_button,0,0,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_layout.addWidget(self.overview_pagination_page_label,0,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination_layout.addWidget(self.overview_pagination_next_button,0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.overview_pagination.setLayout(self.overview_pagination_layout)
        self.overview_tab_layout = CustomGridLayout() 
        self.overview_tab_layout.addWidget(self.overview_table,0,0)
        self.overview_tab_layout.addWidget(self.overview_pagination,1,0,Qt.AlignmentFlag.AlignCenter)
        self.overview_tab = CustomWidget() 
        self.overview_tab.setLayout(self.overview_tab_layout) 
        # endregion: overview pagination table
        # region: manage data buttons
        self.tab_sort_action_menu = CustomWidget(ref='tab_sort_action_menu')
        self.tab_sort_action_menu_layout = CustomHBoxLayout()
        self.refresh_button = CustomPushButton(ref='refresh_button')
        self.delete_all_button = CustomPushButton(ref='delete_all_button')
        self.import_button = CustomPushButton(ref='import_button')
        self.add_button = CustomPushButton(ref='add_button')
        self.tab_sort_action_menu_layout.addWidget(self.refresh_button)
        self.tab_sort_action_menu_layout.addWidget(self.delete_all_button)
        self.tab_sort_action_menu_layout.addWidget(self.import_button)
        self.tab_sort_action_menu_layout.addWidget(self.add_button)
        self.tab_sort_action_menu.setLayout(self.tab_sort_action_menu_layout)
        # endregion: manage data buttons
        # region: tab layout setup
        self.tab_sort = CustomTabWidget(ref='tab_sort')
        self.tab_sort.addTab(self.overview_tab, 'Overview')
        self.tab_sort.setCornerWidget(self.tab_sort_action_menu, Qt.Corner.BottomRightCorner)
        # endregion: tab layout setup

        self.panel_a_box_layout.addWidget(self.filter_field,0,0)
        self.panel_a_box_layout.addWidget(self.tab_sort,1,0)

        self.panel_a_box.setLayout(self.panel_a_box_layout)
        pass
        
        self.call_signal(signal_ref='panel_a_signal')

    def show_main_panel(self):
        self.show_panel_a()
        self.show_panel_b()

        grid_layout = CustomGridLayout()
        grid_layout.addWidget(self.panel_a_box,0,0)
        grid_layout.addWidget(self.panel_b_box,0,1)

        self.setLayout(grid_layout)
        pass

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagementLayout()
    window.show()
    sys.exit(pos_app.exec())
