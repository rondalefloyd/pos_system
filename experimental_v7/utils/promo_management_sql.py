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
            Description TEXT,
            PromoType TEXT,
            PromoTypeValue TEXT,
            DaysToExp INTEGER,
            LessPerc INTEGER,
            StartDt DATETIME,
            EndDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

    def insertPromoData(self, name, description, promo_type, promo_type_value):
        self.cursor.execute('''
        INSERT INTO Promo (Name, Description, PromoType, PromoTypeValue)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Promo
        WHERE
            Name = ? AND
            Description = ? AND
            PromoType = ? AND
            PromoTypeValue = ?
        )''', (name, description, promo_type, promo_type_value,
              name, description, promo_type, promo_type_value))
        self.conn.commit()

    def updatePromoData(self, name, description, promo_type, promo_type_value, old_name):
        self.cursor.execute('''
        UPDATE Promo
        SET Name = ?, Description = ?, PromoType = ?, PromoTypeValue = ?
        WHERE Name = ? 
        ''', (name, description, promo_type, promo_type_value, old_name))
        self.conn.commit()

    def selectAllPromoData(self, text):
        self.cursor.execute('''
        SELECT
            Name,
            Description, 
            PromoType,
            PromoTypeValue 
        FROM Promo
        WHERE
            Name LIKE ? OR Description LIKE ? OR PromoType LIKE ? OR PromoTypeValue LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        all_data = self.cursor.fetchall()
        
        return all_data
    

# for filling combo boxes
    def selectPromoData(self, text):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Promo
        ORDER BY UpdateTs DESC
        ''')

        promo_names = [row[0] for row in self.cursor.fetchall()]

        return promo_names
    
    def selectPromoTypeData(self, text):
        self.cursor.execute('''
        SELECT DISTINCT PromoType FROM Promo
        ORDER BY UpdateTs DESC
        ''')

        promo_types = [row[0] for row in self.cursor.fetchall()]

        return promo_types
    
    def selectPromoTypeValueData(self, text):
        self.cursor.execute('''
        SELECT DISTINCT PromoTypeValue FROM Promo
        ORDER BY UpdateTs DESC
        ''')

        promo_type_values = [row[0] for row in self.cursor.fetchall()]

        return promo_type_values
