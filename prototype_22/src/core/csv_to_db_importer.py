import sys, os
import pandas as pd
import time as tm
import schedule as sc
from typing import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))
 
from src.core.sql.admin.promo import *
from src.core.sql.admin.user import *
from src.core.sql.admin.reward import *
from src.core.sql.admin.customer import *


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
        self.data_frame = pd.read_csv(self.csv_file_path, encoding='utf-8-sig', keep_default_na=False, header=None)
        
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

            for row_v in self.data_frame.itertuples(index=False):
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
                    
                    self.update.emit(total_data_count, current_data)
                    pass
                else:
                    self.cancelled.emit()
                    return
                
            self.finished.emit()
        except Exception as e:
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