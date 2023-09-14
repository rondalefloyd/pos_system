import sqlite3
import sys, os
from datetime import *
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema.product_management_schema import *

class ImportThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, data_frame):
        super().__init__()
        self.data_frame = data_frame

    def run(self):
        product_management_schema = ProductManagementSchema()  # Create a new connection here

        for index, row in self.data_frame.iterrows():
            barcode, item_name, expire_dt, item_type, brand, sales_group, supplier, cost, sell_price, available_stock = row[:10]

            # set default values on optional fields
            barcode = '<unknown>' if barcode == '' else barcode
            expire_dt = '9999-12-31' if expire_dt == '' else expire_dt
            item_type = '<unknown>' if item_type == '' else item_type

            if '' in (item_name, brand, sales_group, supplier, cost, sell_price):
                print('Failed to import due to missing values for required data.')
            else:
                product_management_schema.add_new_product(barcode=barcode, item_name=item_name, expire_dt=expire_dt, item_type=item_type, brand=brand, sales_group=sales_group, supplier=supplier, cost=cost, sell_price=sell_price, available_stock=available_stock)
            
            # Emit progress signal after processing each row
            self.progress_signal.emit(index)

