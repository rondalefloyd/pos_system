import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyPromoSchema():
    def __init__(self):
        super().__init__()

        self.setup_sales_conn()

        self.create_promo_table()

    def setup_sales_conn(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.sales_file)
        self.cursor = self.conn.cursor()

    def create_promo_table(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Promo (
            PromoId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoType TEXT,
            DiscountPercent DECIMAL,
            Description TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    def insert_new_promo_data(self, promo_name='', promo_type='', promo_percent=0, promo_description=''):
        self.cursor.execute(f"""
        INSERT INTO Promo (Name, PromoType, DiscountPercent, Description)
        SELECT '{promo_name}', '{promo_type}', {promo_percent}, '{promo_description}'
        WHERE NOT EXISTS(
            SELECT 1 FROM Promo
            WHERE
                Name = '{promo_name}' AND
                PromoType = '{promo_type}' AND
                DiscountPercent = {promo_percent} AND
                Description = '{promo_description}'
            )
        """)
        self.conn.commit()
        pass
    def update_selected_promo_data(self, promo_name='', promo_type='', promo_percent=0, promo_description='', promo_id=0):
        self.cursor.execute(f"""
        UPDATE Promo
        SET Name = '{promo_name}', PromoType = '{promo_type}', DiscountPercent = {promo_percent}, Description = '{promo_description}'
        WHERE PromoId = {promo_id}
        """)
        self.conn.commit()
        pass
    def delete_selected_promo_data(self, promo_id=0):
        self.cursor.execute(f"""
        DELETE FROM Promo
        WHERE PromoId = {promo_id}
        """)
        self.conn.commit()

    def select_promo_data(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.cursor.execute(f"""
        SELECT 
            COALESCE(NULLIF(Name, ''), '[no data]') AS Name,
            COALESCE(NULLIF(PromoType, ''), '[no data]') AS PromoType,
            COALESCE(NULLIF(DiscountPercent, ''), 0) AS DiscountPercent,
            COALESCE(NULLIF(Description, ''), '[no data]') AS Description,
            UpdateTs,
            PromoId 
        FROM Promo
        WHERE
            Name LIKE '%{text_filter}%' OR
            PromoType LIKE '%{text_filter}%' OR
            DiscountPercent LIKE '%{text_filter}%' OR
            Description LIKE '%{text_filter}%' OR
            UpdateTs LIKE '%{text_filter}%'
        ORDER BY PromoId DESC, UpdateTs DESC
        LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
        """)
        
        promo = self.cursor.fetchall()
        
        return promo
    def select_promo_type(self):
        self.cursor.execute(f"""
        SELECT DISTINCT PromoType FROM Promo
        ORDER BY PromoId DESC, UpdateTs DESC                
        """)
        
        promo = self.cursor.fetchall()
        
        return promo

    def select_promo_count(self):
        self.cursor.execute(f"""
        SELECT COUNT(*) FROM Promo
        """)
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def select_promo_total_pages_count(self, page_size=30):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM Promo
            """)

        total_promo = self.cursor.fetchone()[0]
        total_pages = (total_promo - 1) // page_size + 1

        return total_pages
     