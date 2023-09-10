import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class PromoManagementSchema():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    # PROMO MANAGEMENT
    # -- for adding
    def addNewPromo(self, promo_name, promo_type, discount_percent, description):
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

    # -- for editing
    def editSelectedPromo(self, promo_name, promo_type, discount_percent, description, promo_id):
        self.cursor.execute('''
        UPDATE Promo
        SET Name = ?, PromoType = ?, DiscountPercent = ?, Description = ?
        WHERE PromoId = ?
        ''', (promo_name, promo_type, discount_percent, description, promo_id))
        self.conn.commit()

    # -- for removing
    def deleteSelectedPromo(self, promo_id):
        self.cursor.execute('''
        DELETE FROM Promo
        WHERE PromoId = ?
        ''', (promo_id,))
        self.conn.commit()

    # -- for populating
    def listPromoA(self, text=''):
        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, PromoId FROM Promo
        WHERE
            (Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ?) AND
            UpdateTs >= CURRENT_DATE
        ORDER BY PromoId DESC, UpdateTs DESC
                            
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        promo = self.cursor.fetchall()
        
        return promo
    
    def listPromoB(self, text=''):
        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, PromoId FROM Promo
        WHERE
            (Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ?) AND
            UpdateTs BETWEEN DATE(CURRENT_DATE, '-1 day') AND CURRENT_DATE
        ORDER BY PromoId DESC, UpdateTs DESC
                            
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        promo = self.cursor.fetchall()
        
        return promo
    
    def listPromoC(self, text=''):
        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, PromoId FROM Promo
        WHERE
            (Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ?) AND
            UpdateTs >= DATE(CURRENT_DATE, '-7 day')
        ORDER BY PromoId DESC, UpdateTs DESC
                            
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        promo = self.cursor.fetchall()
        
        return promo

    def listPromoD(self, text=''):
        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, PromoId FROM Promo
        WHERE
            (Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ?) AND
            UpdateTs >= DATE(CURRENT_DATE, '-30 day')
        ORDER BY PromoId DESC, UpdateTs DESC
                            
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        promo = self.cursor.fetchall()
        
        return promo
    
    def listPromoE(self, text=''):
        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, PromoId FROM Promo
        WHERE
            (Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ?) AND
            (UpdateTs BETWEEN DATE(CURRENT_DATE, 'start of month') AND DATE(CURRENT_DATE, 'start of month', '+1 month', '-1 day'))
        ORDER BY PromoId DESC, UpdateTs DESC
                            
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        promo = self.cursor.fetchall()
        
        return promo

    def listPromoF(self, text=''):
        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, PromoId FROM Promo
        WHERE
            (Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ?) AND
            (UpdateTs BETWEEN DATE(CURRENT_DATE, 'start of month', '-1 month') AND DATE(CURRENT_DATE, 'start of month', '-1 day'))
        ORDER BY PromoId DESC, UpdateTs DESC
                            
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        promo = self.cursor.fetchall()
        
        return promo
    
    def listPromoG(self, text=''):
        self.cursor.execute('''
        SELECT Name, PromoType, DiscountPercent, Description, PromoId FROM Promo
        WHERE
            Name LIKE ? OR
            PromoType LIKE ? OR
            DiscountPercent LIKE ? OR
            Description LIKE ?
        ORDER BY PromoId DESC, UpdateTs DESC
                            
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        promo = self.cursor.fetchall()
        
        return promo

    # -- for filling combo box
    def fillPromoComboBox(self):
        self.cursor.execute('''
        SELECT DISTINCT Name, PromoType FROM Promo
        ORDER BY PromoId DESC, UpdateTs DESC                
        ''')
        
        promo = self.cursor.fetchall()
        
        return promo

    def countTotalPromo(self):
        self.cursor.execute('''
        SELECT COUNT(*) FROM Promo           
        ''')
        
        total = self.cursor.fetchone()[0]
        
        return total