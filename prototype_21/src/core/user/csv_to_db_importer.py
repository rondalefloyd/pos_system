import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
import schedule as sc
from typing import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.sql.admin.cust import *
from src.sql.admin.prod import *
from src.sql.admin.promo import *
from src.sql.admin.reward import *
from src.sql.admin.user import *


class MyDataImportThread(QThread):
    update_signal = pyqtSignal()
    finished_signal = pyqtSignal()
    invalid_signal = pyqtSignal()


    def __init__(self, data_name='', data_frame: pd.DataFrame=''):
        super().__init__()

        self.data_name = data_name
        self.data_frame = data_frame
        self.thread_running = True
        
    def stop(self):
        self.thread_running = False

    def run(self):
        try:
            # IDEA: SQLite objects created in a thread can only be used in that same thread.
            self.promo_schema = MyPromoSchema() if self.data_name == 'promo' else None
            self.user_schema = MyUserSchema() if self.data_name == 'user' else None
            self.cust_schema = MyCustSchema() if self.data_name == 'cust' else None
            self.reward_schema = MyRewardSchema() if self.data_name == 'reward' else None
            self.prod_schema = MyProdSchema() if self.data_name == 'prod' else None

            for row_v in self.data_frame.itertuples(index=False):
                print('PASSED')
                # FIX: needs to change the condition (i.e. if the df does not contain the expected header)
                if self.thread_running:
                    self.import_promo(row_v) if self.data_name == 'promo' else None
                    self.import_user(row_v) if self.data_name == 'user' else None
                    self.import_cust(row_v) if self.data_name == 'cust' else None
                    self.import_reward(row_v) if self.data_name == 'reward' else None
                    self.import_prod(row_v) if self.data_name == 'prod' else None
                    self.update_signal.emit()
                    pass
                else:
                    print('import cancelled')
                    return
                
            self.finished_signal.emit()
            pass
        
        except Exception as e:
            print('Error:', e)


    def import_promo(self, row_v):
        promo_name, promo_type, promo_percent, promo_description = row_v[:4]

        self.promo_schema.add_new_promo(
                            promo_name=promo_name,
                            promo_type=promo_type,
                            promo_percent=promo_percent,
                            promo_description=promo_description
                        )
        pass
    def import_user(self, row_v):
        user_name, user_password, user_phone = row_v[:3]

        self.user_schema.add_new_user(
                            user_name=user_name,
                            user_password=user_password,
                            user_phone=user_phone
                        )
        pass
    def import_cust(self, row_v):
        cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status = row_v[:8]

        self.cust_schema.add_new_cust(
                            cust_name=cust_name,
                            cust_address=cust_address,
                            cust_barrio=cust_barrio,
                            cust_town=cust_town,
                            cust_phone=cust_phone,
                            cust_age=cust_age,
                            cust_gender=cust_gender,
                            cust_marital_status=cust_marital_status
                        )
        pass
    def import_reward(self, row_v):
        reward_name, reward_description, reward_unit, reward_points = row_v[:4]

        self.reward_schema.add_new_reward(
                            reward_name=reward_name,
                            reward_description=reward_description,
                            reward_unit=reward_unit,
                            reward_points=reward_points,
                        )
        pass
    def import_prod(self, row_v):
        prod_barcode, prod_name, prod_exp_dt, prod_type, prod_brand, prod_sales_group, prod_supplier, prod_cost, prod_sell_price, stock_available, stock_on_hand = row_v[:11]

        print('PASSED')
        # NOTE: for temporary use only!
        current_date = QDateEdit()
        current_date.setDate(QDate().currentDate())
        temp_effective_data = current_date.date().toString(Qt.DateFormat.ISODate)

        
        if '' not in [stock_available, stock_on_hand]:
            prod_tracking = True
        else:
            prod_tracking = False
            
        self.prod_schema.add_new_prod(
                            prod_barcode=prod_barcode,
                            prod_name=prod_name,
                            prod_exp_dt='9999-99-99',
                            prod_type=prod_type,
                            prod_brand=prod_brand,
                            prod_sales_group=prod_sales_group,
                            prod_supplier=prod_supplier,
                            prod_cost=prod_cost,
                            prod_sell_price=prod_sell_price,
                            prod_effective_dt=temp_effective_data, # REVIEW
                            prod_tracking=prod_tracking, # REVIEW
                            stock_available=stock_available, 
                            stock_on_hand=stock_on_hand
                        )
        pass

