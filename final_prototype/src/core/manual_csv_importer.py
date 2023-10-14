import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
import schedule as sc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.sql.admin.promo import *


class ManualPromoImport(QThread):
    progress_signal = pyqtSignal()
    finished_signal = pyqtSignal()


    def __init__(self, promo_data_frame=''):
        super().__init__()

        self.promo_data_frame = promo_data_frame
        
    def run(self):
        self.promo_schema = MyPromoSchema() # IDEA: SQLite objects created in a thread can only be used in that same thread.

        for row in self.promo_data_frame.itertuples(index=False):
            promo_name, promo_type, discount_percent, description = row[:4]

            self.promo_schema.add_new_promo(
                promo_name=promo_name,
                promo_type=promo_type,
                discount_percent=discount_percent,
                description=description
            )

            self.progress_signal.emit()

        self.finished_signal.emit()
