import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class UserManagementSQL():
    def __init__(self, db_file='USERS.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/users/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def createUserDatabaseTable(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name INTEGER,
            Password TEXT,
            AccessLevel INTEGER, 
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

    def selectUserData(self, access_level):
        self.cursor.execute('''
        SELECT Name , AccessLevel
        FROM User
        WHERE AccessLevel = ?
        ''', (access_level,))
        all_data = self.cursor.fetchall()        
        return all_data
        
    def selectAllFilteredUserData(self, filtered_text):
        self.cursor.execute('''
        SELECT Name, AccessLevel
        FROM User
        WHERE Name LIKE ? OR AccessLevel LIKE ?
        ''', ('%' + filtered_text + '%', '%' + filtered_text + '%'))
        all_data = self.cursor.fetchall()
        return all_data
    
    def selectAllUserData(self, text):
        self.cursor.execute('''
        SELECT Name, AccessLevel
        FROM User
        ''')
        all_data = self.cursor.fetchall()
        return all_data

    def insertUserData(self, name, password, access_level):
        self.cursor.execute('''
        INSERT INTO User (Name, Password, AccessLevel)
        SELECT ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM User
        WHERE
            Name = ?
        )''', (name, password, access_level, name))
        self.conn.commit()

    def updateUserData(self, access_level, password, name):
        self.cursor.execute('''
        UPDATE User
        SET  AccessLevel = ?,
             Password = ?,
             UpdateTs = CURRENT_TIMESTAMP
        WHERE Name = ?                                                        
        ''', (access_level, password, name))
        self.conn.commit()

    def deleteUserData(self, name):
        self.cursor.execute('''
        DELETE User
        WHERE   Name = ?                                                        
        )''', (name,))
        self.conn.commit()    