import sys, os
import pandas as pd
import time as tm
import schedule as sc
import traceback
from typing import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(r'C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22')
 
from src.core.sql.admin.promo import *
from src.core.sql.admin.user import *
from src.core.sql.admin.reward import *
from src.core.sql.admin.customer import *
from src.core.sql.admin.product import *

current_date = str(date.today())

class MyDataImportThread(QThread):
    update = pyqtSignal(int,str)
    cancelled = pyqtSignal()
    finished = pyqtSignal()
    invalid = pyqtSignal()


    def __init__(self, data_name='', csv_file_path=''):
        super().__init__()

        self.thread_running = True
        
        self.data_name = data_name
        self.csv_file_path = csv_file_path
        self.data_frame = pd.read_csv(self.csv_file_path, encoding='utf-8-sig', keep_default_na=False, header=None, skiprows=1)
        self.data_row = 1

    def run(self):
        try:
            if self.data_name == 'promo':
                self.promo_schema = MyPromoSchema()
            elif self.data_name == 'user':
                self.user_schema = MyUserSchema()
            elif self.data_name == 'reward':
                self.reward_schema = MyRewardSchema()
            elif self.data_name == 'customer':
                self.customer_schema = MyCustomerSchema()
            elif self.data_name == 'product':
                self.product_schema = MyProductSchema()

            for row_v in self.data_frame.itertuples(index=False):
                try:
                    if self.thread_running:
                        total_data_count = len(self.data_frame)
                        current_data = row_v[0]

                        if self.data_name == 'promo':
                            self.import_promo(row_v) 
                        elif self.data_name == 'user':
                            self.import_user(row_v) 
                        elif self.data_name == 'reward':
                            self.import_reward(row_v) 
                        elif self.data_name == 'customer':
                            self.import_customer(row_v) 
                        elif self.data_name == 'product':
                            self.import_product(row_v) 
                            current_data = row_v[1]

                        self.data_row += 1

                        self.update.emit(total_data_count, current_data)
                        pass
                    else:
                        self.cancelled.emit()
                        return
                except Exception as e: 
                    specific_error = f"{self.csv_file_path} contains missing values in row {self.data_row}"
                    with open(f"{current_date}_log.txt", 'a') as file: file.write(f"[{str(datetime.today())}] [{e}] [{specific_error}]\n")
                
            self.finished.emit()

        except Exception as e:
            with open(f"{current_date}_log.txt", 'a') as file: file.write(f"[{str(datetime.today())}] [{e}]\n")
            self.invalid.emit()
        pass

    def stop(self):
        self.thread_running = False

    def import_promo(self, row_v):
        promo_name, promo_type, promo_percent, promo_desc = row_v[:4]

        self.promo_schema.insert_promo_data(
            promo_name, 
            promo_type, 
            promo_percent, 
            promo_desc
        )
    def import_user(self, row_v):
        user_name, user_password, user_level, user_phone = row_v[:4]

        self.user_schema.insert_user_data(
            user_name, 
            user_password, 
            user_level, 
            user_phone
        )
    def import_reward(self, row_v):
        reward_name, reward_unit, reward_points, reward_desc = row_v[:4]

        self.reward_schema.insert_reward_data(
            reward_name, 
            reward_unit, 
            reward_points, 
            reward_desc
        )
    def import_customer(self, row_v):
        customer_name, customer_address, customer_barrio, customer_town, customer_phone, customer_age, customer_gender, customer_marstat, = row_v[:8]

        self.customer_schema.insert_customer_data(
            customer_name,
            customer_address,
            customer_barrio,
            customer_town,
            customer_phone,
            customer_age,
            customer_gender,
            customer_marstat,
        )
    def import_product(self, row_v):
        (product_barcode,
        product_name,
        product_expire_dt,
        product_type,
        product_brand,
        product_sales_group,
        product_supplier,
        product_cost,
        product_price,
        product_effective_dt,
        product_stock_available,
        product_stock_onhand) = row_v[:12]

        product_expire_dt = product_expire_dt or '9999-99-99'

        if product_sales_group not in ['Retail', 'Wholesale']:
            return # which means considered as error

        if product_stock_available > 0 or product_stock_onhand >0:
            product_stock_tracking = True
        else:
            product_stock_tracking = False

        self.product_schema.insert_product_data(
            product_barcode=product_barcode,
            product_name=product_name,
            product_expire_dt=product_expire_dt,

            product_type=product_type,
            product_brand=product_brand,
            product_sales_group=product_sales_group,
            product_supplier=product_supplier,

            product_cost=product_cost,
            product_price=product_price,
            product_effective_dt=product_effective_dt,

            product_stock_tracking=product_stock_tracking,
            product_stock_available=product_stock_available,
            product_stock_onhand=product_stock_onhand,
        )