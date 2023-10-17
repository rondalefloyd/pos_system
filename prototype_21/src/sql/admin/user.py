import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyUserSchema():
    def __init__(self):
        super().__init__()

        self.accounts_file = os.path.abspath(qss.db_file_path + qss.accounts_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

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
    
    def add_new_user(self, user_name, user_password, user_phone):
        user_name = '[no data]' if user_name == '' else user_name
        user_password = '[no data]' if user_password == '' else user_password
        user_phone = '[no data]' if user_phone == '' else user_phone

        self.cursor.execute('''
        INSERT INTO User (Name, Password, AccessLevel, Phone)
        SELECT ?, ?, 1, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM User
        WHERE
            Name = ? AND
            Password = ? AND
            AccessLevel = 1 AND -- Cashier level
            Phone = ?
        )''', (user_name, user_password, user_phone,
              user_name, user_password, user_phone))
        self.conn.commit()
        pass
    def edit_selected_user(self, user_name, user_password, user_phone, user_id):
        user_name = '[no data]' if user_name == '' else user_name
        user_password = '[no data]' if user_password == '' else user_password
        user_phone = '[no data]' if user_phone == '' else user_phone
            
        self.cursor.execute('''
        UPDATE User
        SET Name = ?, Password = ?, Phone = ?
        WHERE UserId = ?
        ''', (user_name, user_password, user_phone, user_id))
        self.conn.commit()
    def delete_selected_user(self, user_id):
        self.cursor.execute('''
        DELETE FROM User
        WHERE UserId = ?
        ''', (user_id,))
        self.conn.commit()

    def list_all_user_col(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_user_table()


        self.cursor.execute('''
        SELECT 
            COALESCE(NULLIF(Name, ''), '[no data]') AS Name,
            COALESCE(NULLIF(Password, ''), '[no data]') AS Password,
            COALESCE(NULLIF(Phone, ''), '[no data]') AS Phone,
            UpdateTs,
            UserId,
            AccessLevel FROM User
        WHERE
            (Name LIKE ? OR
            Password LIKE ? OR
            Phone LIKE ? OR
            UpdateTs LIKE ?) AND
            AccessLevel BETWEEN 1 AND 2
        ORDER BY 
            CASE WHEN AccessLevel = 2 THEN 1 ELSE 2 END,
            UserId DESC, 
            UpdateTs DESC
        LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
        ''', (
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            page_size,  # Limit
            offset,
        ))
        
        user = self.cursor.fetchall()
        
        return user

    def count_all_user(self):
        self.create_user_table()

        self.cursor.execute('''
        SELECT COUNT(*) FROM User
        ''')
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def count_user_list_total_pages(self, page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM User
            ''')

        total_user = self.cursor.fetchone()[0]
        total_pages = (total_user - 1) // page_size + 1

        return total_pages
    