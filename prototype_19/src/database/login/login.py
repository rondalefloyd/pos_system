import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class LoginSchema():
    def __init__(self):
        super().__init__()
        # Creates folder for the db file
        self.db_file_path = os.path.abspath('data/sales.db')
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/')), exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

        self.create_user_table()

    def create_user_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Password TEXT,
            AccessLevel INTEGER,
            Phone TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()
    
    def add_new_user(self, user_name, password, access_level, phone):
        # region -- assign values if empty string
        user_name = '[no data]' if user_name == '' else user_name
        password = '[no data]' if password == '' else password
        access_level = '[no data]' if access_level == '' else access_level
        phone = '[no data]' if phone == '' else phone
        # endregion -- assign values if empty string

        self.cursor.execute('''
        INSERT INTO User (Name, Password, AccessLevel, Phone)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM User
        WHERE
            Name = ? AND
            Password = ? AND
            AccessLevel = ? AND
            Phone = ?
        )''', (user_name, password, access_level, phone,
              user_name, password, access_level, phone))
        self.conn.commit()

    def edit_selected_user(self, user_name, password, access_level, phone, user_id):
        # region -- assign values if empty string
        user_name = '[no data]' if user_name == '' else user_name
        password = '[no data]' if password == '' else password
        access_level = '[no data]' if access_level == '' else access_level
        phone = '[no data]' if phone == '' else phone
        # endregion -- assign values if empty string
            
        self.cursor.execute('''
        UPDATE User
        SET Name = ?, Password = ?, AccessLevel = ?, Phone = ?
        WHERE UserId = ?
        ''', (user_name, password, access_level, phone, user_id))
        self.conn.commit()

    def get_user(self, text_filter=''):
        self.create_user_table()

        self.cursor.execute('''
        SELECT Name, Password, AccessLevel, Phone, UpdateTs, UserId FROM User
        WHERE
            Name LIKE ? OR
            Password LIKE ? OR
            AccessLevel LIKE ? OR
            Phone LIKE ? OR
            UpdateTs LIKE ?
        ORDER BY UserId DESC, UpdateTs DESC
        LIMIT 1
        ''', (
            '%' + str(text_filter) + '%',
        ))
        
        user = self.cursor.fetchall()
        
        return user

    def count_user(self):
        self.create_user_table()

        self.cursor.execute('''
        SELECT COUNT(*) FROM User
        ''')
        count = self.cursor.fetchone()[0]
        
        return count