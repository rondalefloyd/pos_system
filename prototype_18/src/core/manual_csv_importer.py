import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
import schedule as sc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.product import *
from database.promo import *
from widget.promo import*

class ManualPromoImport(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file=None):
        super().__init__()
        self.manual_import_progress_dialog = MyProgressDialog()

        self.csv_file = csv_file
        
    def run(self):
        self.csv_file_name = os.path.basename(self.csv_file)

        if self.csv_file:
            data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)

            try:
                self.promo_schema = PromoSchema()
                # Load the CSV file into a Pandas DataFrame
                data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

                self.total_rows = len(data_frame) 

                progress_min_range = 1

                count_row_data = 0

                for row in data_frame.itertuples(index=False):
                    (self.promo_name,
                    self.promo_type,
                    self.discount_percent,
                    self.description) = row[:4]

                    if '' in [
                        self.promo_name,
                        self.promo_type,
                        self.discount_percent
                    ]:
                        pass
                    else:
                        promo_name = str(self.promo_name)
                        promo_type = str(self.promo_type)
                        discount_percent = float(self.discount_percent)
                        description = str(self.description)

                        self.promo_schema.add_new_promo(
                            promo_name=promo_name,
                            promo_type=promo_type,
                            discount_percent=discount_percent,
                            description=description
                        )

                    progress_min_range += 1
                    self.progress_signal.emit(progress_min_range)

                    
                    count_row_data += 1
                    print(count_row_data)

                self.finished_signal.emit(f"All data from '{self.csv_file}' has been imported.")

            except Exception as error_message:
                self.error_signal.emit(f'Error importing data from {self.csv_file}: {str(error_message)}')
                print(error_message)

    def update_progress(self, progress):
        self.current_row = progress - 1
        percentage = int((self.current_row / self.total_rows) * 100)

        self.manual_import_progress_dialog.setLabelText(f"{percentage}% complete ({self.current_row} out of {self.total_rows})")
        self.manual_import_progress_dialog.setValue(percentage)

        pass
    def import_finished(self):
        pass
    def import_error(self):
        pass
