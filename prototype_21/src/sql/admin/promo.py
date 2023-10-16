import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyPromoSchema():
    def __init__(self):
        super().__init__()

        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.sales_file)
        self.cursor = self.conn.cursor()

        self.create_promo_table()

    def create_promo_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Promo (
            PromoId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoType TEXT,
            DiscountPercent DECIMAL,
            Description TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

    def add_new_promo(self, promo_name, promo_type, promo_percent, promo_description):
        promo_name = '[no data]' if promo_name == '' else promo_name
        promo_type = '[no data]' if promo_type == '' else promo_type
        promo_percent = 0 if promo_percent == '' else promo_percent
        promo_description = '[no data]' if promo_description == '' else promo_description

        self.cursor.execute('''
        INSERT INTO Promo (Name, PromoType, DiscountPercent, Description)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Promo
        WHERE
            Name = ? AND
            PromoType = ? AND
            DiscountPercent = ? AND
            Description = ?
        )''', (promo_name, promo_type, promo_percent, promo_description,
              promo_name, promo_type, promo_percent, promo_description))
        self.conn.commit()
    def edit_selected_promo(self, promo_name, promo_type, promo_percent, promo_description, promo_id):
        promo_name = '[no data]' if promo_name == '' else promo_name
        promo_type = '[no data]' if promo_type == '' else promo_type
        promo_percent = 0 if promo_percent == '' else promo_percent
        promo_description = '[no data]' if promo_description == '' else promo_description
            
        self.cursor.execute('''
        UPDATE Promo
        SET Name = ?, PromoType = ?, DiscountPercent = ?, Description = ?
        WHERE PromoId = ?
        ''', (promo_name, promo_type, promo_percent, promo_description, promo_id))
        self.conn.commit()
        pass
    def delete_selected_promo(self, promo_id):
        self.cursor.execute('''
        DELETE FROM Promo
        WHERE PromoId = ?
        ''', (promo_id,))
        self.conn.commit()

    def list_all_promo_col(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.cursor.execute('''
        SELECT 
            COALESCE(NULLIF(Name, ''), '[no data]') AS Name,
            COALESCE(NULLIF(PromoType, ''), '[no data]') AS PromoType,
            COALESCE(NULLIF(DiscountPercent, ''), 0) AS DiscountPercent,
            COALESCE(NULLIF(Description, ''), '[no data]') AS Description,
            UpdateTs,
            PromoId 
        FROM Promo
        WHERE
            Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ? OR
            UpdateTs LIKE ?
        ORDER BY PromoId DESC, UpdateTs DESC
        LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
        ''', (
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            page_size,  # Limit
            offset,
        ))
        
        promo = self.cursor.fetchall()
        
        return promo
    def list_promo_type_col(self):
        self.cursor.execute('''
        SELECT DISTINCT PromoType FROM Promo
        ORDER BY PromoId DESC, UpdateTs DESC                
        ''')
        
        promo = self.cursor.fetchall()
        
        return promo

    def count_all_promo(self):
        self.cursor.execute('''
        SELECT COUNT(*) FROM Promo
        ''')
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def count_promo_list_total_pages(self, page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM Promo
            ''')

        total_promo = self.cursor.fetchone()[0]
        total_pages = (total_promo - 1) // page_size + 1

        return total_pages
    