import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyDevSchema():
    def __init__(self):
        super().__init__()

        self.accounts_file = os.path.abspath(qss.database_file_path + qss.accounts_file_name)
        
        os.makedirs(os.path.abspath(qss.database_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.accounts_file)
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
        user_name = '[no data]' if user_name == '' else user_name
        password = '[no data]' if password == '' else password
        access_level = '[no data]' if access_level == '' else access_level
        phone = '[no data]' if phone == '' else phone

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
        pass
    def edit_selected_user(self, user_name, password, access_level, phone, user_id):
        user_name = '[no data]' if user_name == '' else user_name
        password = '[no data]' if password == '' else password
        access_level = '[no data]' if access_level == '' else access_level
        phone = '[no data]' if phone == '' else phone
            
        self.cursor.execute('''
        UPDATE User
        SET Name = ?, Password = ?, AccessLevel = ?, Phone = ?
        WHERE UserId = ?
        ''', (user_name, password, access_level, phone, user_id))
        self.conn.commit()
        pass
    def delete_selected_user(self, user_id):
        self.cursor.execute('''
        DELETE FROM User
        WHERE UserId = ?
        ''', (user_id,))
        self.conn.commit()

    def list_user_data(self):
        self.create_user_table()

        self.cursor.execute('''
        SELECT Name, Password, AccessLevel, Phone, UpdateTs, UserId FROM User
        ORDER BY UserId DESC, UpdateTs DESC
        ''')
        
        user_list_data = self.cursor.fetchall()
        
        return user_list_data
