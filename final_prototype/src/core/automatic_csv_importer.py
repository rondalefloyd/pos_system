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

from database.admin.product import *
from database.admin.promo import *
from widget.admin.admin import*

class AutomaticPromoImport(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file=None):
        super().__init__()
        self.automatic_import_progress_dialog = MyProgressDialog()

        self.csv_file = os.path.abspath('G:' + '\My Drive\data\promo.csv')
        
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

                self.finished_signal.emit('Done')

                pass

            except Exception as error_message:
                pass

    def update_progress(self, progress):
        self.current_row = progress - 1
        percentage = int((self.current_row / self.total_rows) * 100)

        self.automatic_import_progress_dialog.setLabelText(f"{percentage}% complete ({self.current_row} out of {self.total_rows})")
        self.automatic_import_progress_dialog.setValue(percentage)

        pass
    def import_finished(self, message):
        print(message)
        QApplication.quit()
        pass
    def import_error(self):
        pass

if __name__ == '__main__':
    starter = QApplication(sys.argv)
    
    automatic_import = AutomaticPromoImport()

    automatic_import.progress_signal.connect(automatic_import.update_progress)
    automatic_import.finished_signal.connect(automatic_import.import_finished)
    automatic_import.error_signal.connect(automatic_import.import_error)
    automatic_import.start()

    sys.exit(starter.exec())
