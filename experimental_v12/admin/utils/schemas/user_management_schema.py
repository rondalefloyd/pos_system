import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class AccountsManagementSchema():
    def __init__(self, db_file='ACCOUNTS.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/accounts/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    # for creating all accounts table
    def createAccountsTable(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Password TEXT,
            AccessLevel INTEGER, 
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

    # -- for adding
    def addNewUser(self, user_name, password, access_level):
        self.cursor.execute('''
        INSERT INTO User (Name, Password, AccessLevel)
        SELECT ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM User
        WHERE
            Name = ? AND 
            Password = ? AND 
            AccessLevel = ?
        )''', (user_name, password, access_level,
              user_name, password, access_level))
        self.conn.commit()

    # -- for editing
    def editSelectedUser(self, user_name, password, access_level, user_id):
        self.cursor.execute('''
        UPDATE User
        SET Name = ?, Password = ?, AccessLevel = ?
        WHERE UserId = ?
        ''', (user_name, password, access_level, user_id))
        self.conn.commit()

    # -- for removing
    def removeSelectedUser(self, user_id):
        self.cursor.execute('''
        DELETE FROM User
        WHERE UserId = ?
        ''', (user_id,))
        self.conn.commit()

    # -- for populating
    def listUser(self, text):
        self.cursor.execute('''
        SELECT Name, Password, AccessLevel, UserId FROM User
        WHERE Name LIKE ? OR Password LIKE ? OR AccessLevel LIKE ?
        ORDER BY UpdateTs DESC
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        stock = self.cursor.fetchall()
        
        return stock
    
    # -- for filling combo box
    def fillUserComboBox(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM User
        ORDER BY UserId DESC, UpdateTs DESC                
        ''')
        
        user = self.cursor.fetchall()
        
        return user

