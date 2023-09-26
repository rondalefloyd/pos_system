import sqlite3
import sys, os
import pandas as pd
import threading
import configparser

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.csv_importer import *
from core.manage_settings import *
from core.scheduled_scv_importer import *
from database.promo import *
from widget.settings import *

class SettingsWindow(MyWidget):
    def __init__(self):
        super().__init__(widget_ref='promo_window')
        
        self.promo_schema = PromoSchema()

        self.show_main_panel()
        self.default_values()
        self.apply_settings()
        self.background_process()

    def default_values(self):
        self.manage_settings_core = ManageSettings()
        self.scheduled_csv_importer = None
        pass

    def background_process(self):
        # region -- auto_update_process
        if self.auto_csv_import_option.currentText() == 'Disabled':
            if self.scheduled_csv_importer and self.scheduled_csv_importer.isRunning():
                if self.scheduled_csv_importer:
                    self.scheduled_csv_importer.stop()
                    self.scheduled_csv_importer.wait()

                pass
        elif self.auto_csv_import_option.currentText() == 'Enabled':
            if self.scheduled_csv_importer is None or not self.scheduled_csv_importer.isRunning():
                self.scheduled_csv_importer = ScheduledCSVImporter(
                    product_import=self.product_import_status,
                    promo_import=self.promo_import_status,
                    customer_import=self.customer_import_status,
                    user_import=self.user_import_status
                )
                
                self.scheduled_csv_importer.import_data_signal.connect(self.scheduled_csv_importer.update_promo_import_status_label)
                self.scheduled_csv_importer.start()

                pass
        # endregion -- auto_update_process

    def on_use_default_button_clicked(self):
        
        pass
    def on_save_changes_button_clicked(self):
        self.manage_settings_core.save_settings(auto_csv_import_option=self.auto_csv_import_option)
        self.background_process()

    def apply_settings(self):
        self.manage_settings_core.load_settings(auto_csv_import_option=self.auto_csv_import_option)
        
    def show_settings_nav_panel(self):
        # region -- self.settings_nav = MyGroupBox()
        self.settings_nav = MyGroupBox()
        self.settings_nav_layout = MyHBoxLayout(hbox_layout_ref='settings_nav_layout')
        self.use_default_button = MyPushButton(push_button_ref='use_default_button', text='Use default')
        self.use_default_button.clicked.connect(self.on_use_default_button_clicked)
        self.save_changes_button = MyPushButton(push_button_ref='save_changes_button', text='Save changes')
        self.save_changes_button.clicked.connect(self.on_save_changes_button_clicked)
        self.settings_nav_layout.addWidget(self.use_default_button)
        self.settings_nav_layout.addWidget(self.save_changes_button)
        self.settings_nav.setLayout(self.settings_nav_layout)
        # endregion -- self.settings_nav = MyGroupBox()

    def show_content_panel(self):
        self.scrolling_content_panel = MyScrollArea(scroll_area_ref='scrolling_content_panel')
        self.content_panel = MyWidget(widget_ref='content_panel')
        self.content_panel_layout = MyFormLayout(form_layout_ref='content_panel_layout')

        # region -- self.settings_a = MyGroupBox()
        self.settings_a = MyGroupBox(group_box_ref='settings_a')
        self.settings_a_layout = MyFormLayout()

        self.settings_a_title = MyLabel(text='<b>Database</b>')
        self.auto_csv_import_option_label = MyLabel(text='Auto update:')

        self.product_import_status_label = MyLabel(label_ref='product_import_status_label', text='Product import status:')
        self.promo_import_status_label = MyLabel(label_ref='promo_import_status_label', text='Promo import status:')
        self.customer_import_status_label = MyLabel(label_ref='customer_import_status_label', text='Customer import status:')
        self.user_import_status_label = MyLabel(label_ref='user_import_status_label', text='User import status:')

        self.auto_csv_import_option = MyComboBox(combo_box_ref='auto_csv_import_option')
        self.product_import_status = MyLabel(text="<font color='red'>None</font>")
        self.promo_import_status = MyLabel(text="<font color='red'>None</font>")
        self.customer_import_status = MyLabel(text="<font color='red'>None</font>")
        self.user_import_status = MyLabel(text="<font color='red'>None</font>")
        
        self.settings_a_layout.addRow(self.settings_a_title)
        self.settings_a_layout.addRow(self.auto_csv_import_option_label, self.auto_csv_import_option)

        self.settings_a_layout.addRow(self.product_import_status_label, self.product_import_status)
        self.settings_a_layout.addRow(self.promo_import_status_label, self.promo_import_status)
        self.settings_a_layout.addRow(self.customer_import_status_label, self.customer_import_status)
        self.settings_a_layout.addRow(self.user_import_status_label, self.user_import_status)

        self.settings_a.setLayout(self.settings_a_layout)
        # endregion -- self.settings_a = MyGroupBox()

        self.content_panel_layout.addWidget(self.settings_a)
        self.content_panel.setLayout(self.content_panel_layout)
        self.scrolling_content_panel.setWidget(self.content_panel)

    def show_main_panel(self):
        self.main_panel_layout = MyGridLayout(grid_layout_ref='main_panel_layout')

        self.show_content_panel()
        self.show_settings_nav_panel()

        self.main_panel_layout.addWidget(self.scrolling_content_panel,0,0)
        self.main_panel_layout.addWidget(self.settings_nav,1,0)
        self.setLayout(self.main_panel_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(pos_app.exec())
