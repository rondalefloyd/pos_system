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
            PromoTypeValue TEXT,
            Description TEXT,
            DaysToExp INTEGER,
            LessPerc INTEGER,
            StartDt DATETIME,
            EndDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

    def insertPromoData(self, name, promo_type, promo_type_value, description):
        self.cursor.execute('''
        INSERT INTO Promo (Name, PromoType, PromoTypeValue, Description)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Promo
        WHERE
            Name = ? AND
            PromoType = ? AND
            PromoTypeValue = ? AND
            Description = ?
        )''', (name, promo_type, promo_type_value, description,
              name, promo_type, promo_type_value, description))
        self.conn.commit()

    def updatePromoData(self, name, promo_type, promo_type_value, description, old_name):
        self.cursor.execute('''
        UPDATE Promo
        SET Name = ?, PromoType = ?, PromoTypeValue = ?, Description = ?
        WHERE Name = ? 
        ''', (name, promo_type, promo_type_value, description, old_name))
        self.conn.commit()

    def selectPromoId(self, name, promo_type):
        self.cursor.execute('''
        SELECT PromoId FROM Promo
        WHERE Name = ? AND PromoType = ?
        ''', (name, promo_type))

        promo_id = self.cursor.fetchone()

        return promo_id[0]
    
    def selectAllPromoData(self, text):
        self.cursor.execute('''
        SELECT
            Name,
            PromoType,
            PromoTypeValue,
            Description
        FROM Promo
        WHERE
            Name LIKE ? OR PromoType LIKE ? OR PromoTypeValue LIKE ? OR Description LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        all_data = self.cursor.fetchall()
        
        return all_data
    
    def selectPromoData(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Promo
        ORDER BY PromoId DESC
        ''')
        
        promos = [row[0] for row in self.cursor.fetchall()]
        
        return promos
    
    def selectPromoTypeData(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Promo
        ORDER BY PromoId DESC
        ''')
        
        promo_types = self.cursor.fetchall()
        
        return promo_types[0]