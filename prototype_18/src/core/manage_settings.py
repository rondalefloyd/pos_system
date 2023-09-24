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
from core.scheduled_scv_importer import *
from database.promo import *
from widget.settings import *

class ManageSettings():
    def __init__(self):
        super().__init__()

        self.settings_file_path = os.path.join('config/', 'settings.ini')


    def save_settings(self, auto_csv_import_option=None):
        # region -- save_settings_process
        auto_csv_import_option = auto_csv_import_option.currentText()

        # Create a configparser instance and write the settings to an .ini file
        config = configparser.ConfigParser()
        config['settings'] = {'auto_update': auto_csv_import_option}

        with open(self.settings_file_path, 'w') as configfile:
            config.write(configfile)
        # endregion -- save_settings_process

    def load_settings(self, auto_csv_import_option=None):
        # region -- load settings_process
        config = configparser.ConfigParser()

        try:
            config.read(self.settings_file_path)

            # Get the 'AutoUpdate' setting from the INI file
            auto_update_setting = config.get('settings', 'auto_update')

            # Set the combo box to the loaded value
            auto_csv_import_option.setCurrentText(auto_update_setting)

        except configparser.Error:
            # Handle errors if the file doesn't exist or has incorrect format
            pass
        # endregion -- load settings_process