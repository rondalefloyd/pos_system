import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class MyPromoSchema():
    def __init__(self):
        super().__init__()
        dir_path = 'G:' + f"/My Drive/database/"
        self.db_file_path = os.path.abspath(dir_path + '/sales.db')
        os.makedirs(os.path.abspath(dir_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.db_file_path)
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

    def add_new_promo(self, promo_name, promo_type, discount_percent, description):
        promo_name = '[no data]' if promo_name == '' else promo_name
        promo_type = '[no data]' if promo_type == '' else promo_type
        discount_percent = 0 if discount_percent == '' else discount_percent
        description = '[no data]' if description == '' else description

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
        )''', (promo_name, promo_type, discount_percent, description,
              promo_name, promo_type, discount_percent, description))
        self.conn.commit()

    def edit_selected_promo(self, promo_name, promo_type, discount_percent, description, promo_id):
        promo_name = '[no data]' if promo_name == '' else promo_name
        promo_type = '[no data]' if promo_type == '' else promo_type
        discount_percent = 0 if discount_percent == '' else discount_percent
        description = '[no data]' if description == '' else description
            
        self.cursor.execute('''
        UPDATE Promo
        SET Name = ?, PromoType = ?, DiscountPercent = ?, Description = ?
        WHERE PromoId = ?
        ''', (promo_name, promo_type, discount_percent, description, promo_id))
        self.conn.commit()
    def delete_selected_promo(self, promo_id):
        self.cursor.execute('''
        DELETE FROM Promo
        WHERE PromoId = ?
        ''', (promo_id,))
        self.conn.commit()

    def list_promo_data(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_promo_table()

        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, UpdateTs, PromoId FROM Promo
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
    def list_promo_type(self):
        self.cursor.execute('''
        SELECT DISTINCT PromoType FROM Promo
        ORDER BY PromoId DESC, UpdateTs DESC                
        ''')
        
        promo = self.cursor.fetchall()
        
        return promo

    def count_promo(self):
        self.create_promo_table()

        self.cursor.execute('''
        SELECT COUNT(*) FROM Promo
        ''')
        count = self.cursor.fetchone()[0]
        
        return count