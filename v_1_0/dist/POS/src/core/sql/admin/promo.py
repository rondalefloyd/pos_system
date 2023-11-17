import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

cwd = os.getcwd() # get current working dir
sys.path.append(os.path.join(cwd))

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyPromoSchema:
    def __init__(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.sales_conn = sqlite3.connect(database=self.sales_file)
        self.sales_cursor = self.sales_conn.cursor()

        self.create_promo_table()

    def create_promo_table(self):
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Promo (
                PromoId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                PromoType TEXT,
                DiscountPercent DECIMAL,
                Description TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.sales_conn.commit()

    def insert_promo_data(self, promo_name='', promo_type='', promo_percent=0, promo_desc=''):
        self.sales_cursor.execute(f"""
            INSERT INTO Promo (Name, PromoType, DiscountPercent, Description)
            SELECT 
                "{promo_name}", 
                "{promo_type}", 
                {promo_percent}, 
                "{promo_desc}"
            WHERE NOT EXISTS (
                SELECT 1 FROM Promo
                WHERE
                    Name = "{promo_name}" AND
                    PromoType = "{promo_type}" AND
                    DiscountPercent = {promo_percent} AND
                    Description = "{promo_desc}"
            )
        """)

        self.sales_conn.commit()

    def select_data_as_display(self, text='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
            SELECT 
                Name, 
                PromoType, 
                DiscountPercent, 
                Description,
                UpdateTs
            FROM Promo
            WHERE
                Name LIKE '%{text}%' OR
                PromoType LIKE '%{text}%' OR
                DiscountPercent LIKE '%{text}%' OR
                Description LIKE '%{text}%'
            ORDER BY PromoId DESC, UpdateTs DESC
            LIMIT {page_size}
            OFFSET {offset}
        """)

        promo_data = self.sales_cursor.fetchall()

        return promo_data
        pass
    def select_promo_data(self, promo_name='', promo_type=''):
        self.sales_cursor.execute(f"""
            SELECT
                Name, 
                PromoType, 
                DiscountPercent, 
                Description,
                PromoId
            FROM Promo
            WHERE
                Name = "{promo_name}" AND
                PromoType = "{promo_type}"
            ORDER BY PromoId DESC, UpdateTs DESC
        """)

        promo_data = self.sales_cursor.fetchall()

        return promo_data
    def select_promo_data_total_page_count(self, text='', page_size=30):
        self.sales_cursor.execute(f"""
            SELECT COUNT(*) FROM Promo
            WHERE
                Name LIKE '%{text}%' OR
                PromoType LIKE '%{text}%' OR
                DiscountPercent LIKE '%{text}%' OR
                Description LIKE '%{text}%'
        """)

        total_promo_data_count = self.sales_cursor.fetchone()[0]
        total_page_count = (total_promo_data_count - 1) // page_size + 1

        return total_page_count
    def select_promo_type_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT PromoType FROM Promo
            ORDER BY PromoId DESC, UpdateTs DESC
        """)

        promo_type = self.sales_cursor.fetchall()

        return promo_type

    def update_promo_data(self, promo_name='', promo_type='', promo_percent=0, promo_desc='', promo_id=0):
        self.sales_cursor.execute(f"""
            UPDATE Promo
            SET
                Name = "{promo_name}",
                PromoType = "{promo_type}",
                DiscountPercent = {promo_percent},
                Description = "{promo_desc}"
            WHERE PromoId = {promo_id}
        """)

        self.sales_conn.commit()

    def delete_promo_data(self, promo_id=0):
        self.sales_cursor.execute(f"""
            DELETE FROM Promo
            WHERE PromoId = {promo_id}
        """)

        self.sales_conn.commit()
