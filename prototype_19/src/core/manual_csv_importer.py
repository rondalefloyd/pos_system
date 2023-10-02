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
from database.admin.reward import *
from database.admin.customer import *
from database.admin.user import *

class ImportProgressDialog(QProgressDialog):
    def __init__(self, object_name='', parent=None):
        super().__init__()
        self.import_progress_bar = QProgressBar()
        self.import_progress_bar.setFixedHeight(20)
        self.import_progress_bar.setTextVisible(False)
        self.import_progress_bar.hide()
        
        self.import_progress_label = QLabel()

        self.setObjectName(object_name)
        self.setParent(parent)
        self.setFixedSize(250, 80)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setCancelButton(None)
        self.setLabelText(self.import_progress_label.text())
        self.setBar(self.import_progress_bar)
        self.setStyleSheet("""
            QProgressDialog { border: 1px solid #bbb;  } 
            QLabel { font-size: 10px; }
        """)
        pass

class ManualProductImport(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file=None):
        super().__init__()
        self.manual_import_progress_dialog = ImportProgressDialog()

        self.csv_file = csv_file
        
    def run(self):
        self.csv_file_name = os.path.basename(self.csv_file)

        if self.csv_file:
            data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)


            self.product_schema = ProductSchema()

            self.total_rows = len(data_frame) 

            progress_min_range = 1

            count_row_data = 0

            for row in data_frame.itertuples(index=False):
                (
                    self.barcode,
                    self.item_name,
                    self.expire_dt,
                    self.item_type,
                    self.brand,
                    self.sales_group,
                    self.supplier,
                    self.cost,
                    self.sell_price,
                    # self.effective_dt,
                    # self.promo_name,
                    # self.promo_type,
                    # self.discount_percent,
                    # self.discount_value,
                    # self.new_sell_price,
                    # self.start_dt,
                    # self.end_dt,
                    # self.inventory_tracking,
                    self.available_stock
                    # self.on_hand_stock
                ) = row[:10]

                barcode = str(self.barcode)
                item_name = str(self.item_name)
                expire_dt = str(self.expire_dt)
                item_type = str(self.item_type)
                brand = str(self.brand)
                sales_group = str(self.sales_group)
                supplier = str(self.supplier)
                cost = str(self.cost)
                sell_price = str(self.sell_price)
                # effective_dt = str(self.effective_dt)
                # promo_name = str(self.promo_name)
                # promo_type = str(self.promo_type)
                # discount_percent = str(self.discount_percent)
                # discount_value = str(self.discount_value)
                # new_sell_price = str(self.new_sell_price)
                # start_dt = str(self.start_dt)
                # end_dt = str(self.end_dt)
                # inventory_tracking = str(self.inventory_tracking)
                available_stock = str(self.available_stock)
                # on_hand_stock = str(self.on_hand_stock)

                self.product_schema.add_new_product(
                    barcode=barcode,
                    item_name=item_name,
                    expire_dt=expire_dt,
                    item_type=item_type,
                    brand=brand,
                    sales_group=sales_group,
                    supplier=supplier,
                    cost=cost,
                    sell_price=sell_price,
                    # effective_dt=effective_dt,
                    # promo_name=promo_name,
                    # promo_type=promo_type,
                    # discount_percent=discount_percent,
                    # discount_value=discount_value,
                    # new_sell_price=new_sell_price,
                    # start_dt=start_dt,
                    # end_dt=end_dt,
                    # inventory_tracking=inventory_tracking,
                    available_stock=available_stock
                    # on_hand_stock=on_hand_stock
                )

                progress_min_range += 1
                self.progress_signal.emit(progress_min_range)

                count_row_data += 1
                print(count_row_data)

            self.finished_signal.emit(f"All data from '{self.csv_file}' has been imported.")

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
    pass
class ManualPromoImport(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file=None):
        super().__init__()
        self.manual_import_progress_dialog = ImportProgressDialog()

        self.csv_file = csv_file
        
    def run(self):
        self.csv_file_name = os.path.basename(self.csv_file)

        if self.csv_file:
            data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)

            self.promo_schema = PromoSchema()

            self.total_rows = len(data_frame) 

            progress_min_range = 1

            count_row_data = 0

            for row in data_frame.itertuples(index=False):
                (self.promo_name,
                self.promo_type,
                self.discount_percent,
                self.description) = row[:4]

                promo_name = str(self.promo_name)
                promo_type = str(self.promo_type)
                discount_percent = str(self.discount_percent)
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
class ManualRewardImport(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file=None):
        super().__init__()
        self.manual_import_progress_dialog = ImportProgressDialog()

        self.csv_file = csv_file
        
    def run(self):
        self.csv_file_name = os.path.basename(self.csv_file)

        if self.csv_file:
            data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)

            self.reward_schema = RewardSchema()

            self.total_rows = len(data_frame) 

            progress_min_range = 1

            count_row_data = 0

            for row in data_frame.itertuples(index=False):
                (self.reward_name,
                self.description,
                self.points_rate) = row[:3]

                reward_name = str(self.reward_name)
                description = str(self.description)
                points_rate = str(self.points_rate)


                self.reward_schema.add_new_reward(
                    reward_name=reward_name,
                    description=description,
                    points_rate=points_rate
                )

                progress_min_range += 1
                self.progress_signal.emit(progress_min_range)

                
                count_row_data += 1
                print(count_row_data)

            self.finished_signal.emit(f"All data from '{self.csv_file}' has been imported.")

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
class ManualCustomerImport(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file=None):
        super().__init__()
        self.manual_import_progress_dialog = ImportProgressDialog()

        self.csv_file = csv_file
        
    def run(self):
        self.csv_file_name = os.path.basename(self.csv_file)

        if self.csv_file:
            data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)

            self.customer_schema = CustomerSchema()

            self.total_rows = len(data_frame) 

            progress_min_range = 1

            count_row_data = 0

            for row in data_frame.itertuples(index=False):
                (
                    self.customer_name,
                    self.address,
                    self.barrio,
                    self.town,
                    self.phone,
                    self.age,
                    self.gender,
                    self.marital_status
                ) = row[:8]

                customer_name = str(self.customer_name)
                address = str(self.address)
                barrio = str(self.barrio)
                town = str(self.town)
                phone = str(self.phone)
                age = str(self.age)
                gender = str(self.gender)
                marital_status = str(self.marital_status)


                self.customer_schema.add_new_customer(
                    customer_name=customer_name,
                    address=address,
                    barrio=barrio,
                    town=town,
                    phone=phone,
                    age=age,
                    gender=gender,
                    marital_status=marital_status
                )

                progress_min_range += 1
                self.progress_signal.emit(progress_min_range)

                
                count_row_data += 1
                print(count_row_data)

            self.finished_signal.emit(f"All data from '{self.csv_file}' has been imported.")


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
class ManualUserImport(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, csv_file=None):
        super().__init__()
        self.manual_import_progress_dialog = ImportProgressDialog()

        self.csv_file = csv_file
        
    def run(self):
        self.csv_file_name = os.path.basename(self.csv_file)

        if self.csv_file:
            data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)

            self.user_schema = UserSchema()

            self.total_rows = len(data_frame) 

            progress_min_range = 1

            count_row_data = 0

            for row in data_frame.itertuples(index=False):
                (
                    self.user_name,
                    self.password,
                    self.access_level,
                    self.phone
                ) = row[:8]

                user_name = str(self.user_name)
                password = str(self.password)
                access_level = str(self.access_level)
                phone = str(self.phone)

                self.user_schema.add_new_user(
                    user_name=user_name,
                    password=password,
                    access_level=access_level,
                    phone=phone
                )

                progress_min_range += 1
                self.progress_signal.emit(progress_min_range)
                
                count_row_data += 1
                print(count_row_data)

            self.finished_signal.emit(f"All data from '{self.csv_file}' has been imported.")


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
