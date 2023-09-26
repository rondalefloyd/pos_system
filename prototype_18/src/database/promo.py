import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class PromoSchema():
    def __init__(self, db_file='sales.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'data/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

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
        # region -- assign values if empty string
        promo_name = '[no data]' if promo_name == '' else promo_name
        promo_type = '[no data]' if promo_type == '' else promo_type
        discount_percent = 0 if discount_percent == '' else discount_percent
        description = '[no data]' if description == '' else description
        # endregion -- assign values if empty string

        self.create_promo_table()

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
        # region -- assign values if empty string
        promo_name = '[no data]' if promo_name == '' else promo_name
        promo_type = '[no data]' if promo_type == '' else promo_type
        discount_percent = 0 if discount_percent == '' else discount_percent
        description = '[no data]' if description == '' else description
        # endregion -- assign values if empty string
            
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

    def delete_all_promo(self):
        self.cursor.execute('''
        DELETE FROM Promo
        ''')
        self.conn.commit()

    def list_promo(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_promo_table()

        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, UpdateTs, PromoId FROM Promo
        WHERE
            Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ?
        ORDER BY PromoId DESC, UpdateTs DESC
        LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
        ''', (
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            page_size,  # Limit
            offset     # Offset
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