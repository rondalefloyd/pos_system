import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class PromoManagementSQL():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

# create promo table
    def createPromoTable(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Promo (
            PromoId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoType TEXT,
            DiscountValue DECIMAL,
            Description TEXT,
            StartDt DATETIME,
            EndDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

    def addPromo(self, promo_name, promo_type, discount_value, description):
        self.cursor.execute('''
        INSERT INTO Promo (Name, PromoType, DiscountValue, Description)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Promo
        WHERE
            Name = ? AND
            PromoType = ? AND
            DiscountValue = ? AND
            Description = ?
        )''', (promo_name, promo_type, discount_value, description,
              promo_name, promo_type, discount_value, description))
        self.conn.commit()


    def listPromo(self):
        self.cursor.execute('''
        SELECT DISTINCT Name, PromoType, DiscountValue, Description FROM Promo
        ''')
        promo = self.cursor.fetchall()
        
        return promo
    
    def getPromoId(self, promo_name, promo_type, discount_value):
        self.cursor.execute('''
        SELECT DISTINCT PromoId FROM Promo
        WHERE Name = ? AND PromoType = ? AND DiscountValue = ?
        ''', (promo_name, promo_type, discount_value))
        promo_id = self.cursor.fetchall()
        
        return promo_id

    def getPromoTypeAndDiscountValue(self, promo_name):
        self.cursor.execute('''
        SELECT DISTINCT PromoType, DiscountValue FROM Promo
        WHERE Name = ?
        ''', (promo_name,))
        data = self.cursor.fetchall()
        
        return data
    
    
