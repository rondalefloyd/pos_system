import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyUserSchema:
    def __init__(self):
        self.accounts_file = os.path.abspath(qss.db_file_path + qss.accounts_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.accounts_conn = sqlite3.connect(database=self.accounts_file)
        self.accounts_cursor = self.accounts_conn.cursor()

        self.create_user_table()

    def create_user_table(self):
        self.accounts_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS User (
                UserId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Password TEXT,
                AccessLevel INTEGER,
                Phone TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.accounts_conn.commit()

    def insert_user_data(self, user_name='', user_password='', user_level=0, user_phone=''):
        self.accounts_cursor.execute(f"""
            INSERT INTO User (Name, Password, AccessLevel, Phone)
            SELECT 
                "{user_name}", 
                "{user_password}", 
                {user_level}, 
                "{user_phone}"
            WHERE NOT EXISTS (
                SELECT 1 FROM User
                WHERE
                    Name = "{user_name}" AND
                    Password = "{user_password}" AND
                    AccessLevel = {user_level} AND
                    Phone = "{user_phone}"
            )
        """)

        self.accounts_conn.commit()

    def select_data_as_display(self, text='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.accounts_cursor.execute(f"""
            SELECT 
                Name, 
                Password, 
                AccessLevel, 
                Phone,
                UpdateTs
            FROM User
            WHERE
                Name LIKE '%{text}%' OR
                Password LIKE '%{text}%' OR
                AccessLevel LIKE '%{text}%' OR
                Phone LIKE '%{text}%'
            ORDER BY UserId DESC, UpdateTs DESC
            LIMIT {page_size}
            OFFSET {offset}
        """)

        user_data = self.accounts_cursor.fetchall()

        return user_data
        pass
    def select_user_data(self, user_name='', user_password=''):
        self.accounts_cursor.execute(f"""
            SELECT
                Name, 
                Password, 
                AccessLevel, 
                Phone,
                UserId
            FROM User
            WHERE
                Name = "{user_name}" AND
                Password = "{user_password}"
            ORDER BY UserId DESC, UpdateTs DESC
        """)

        user_data = self.accounts_cursor.fetchall()

        return user_data
    def select_user_data_total_page_count(self, page_size=30):
        self.accounts_cursor.execute(f"SELECT COUNT(*) FROM User")

        total_user_data_count = self.accounts_cursor.fetchone()[0]
        total_page_count = (total_user_data_count - 1) // page_size + 1

        return total_page_count
    def select_user_password_for_combo_box(self):
        self.accounts_cursor.execute(f"""
            SELECT Password FROM User
            ORDER BY UserId DESC, UpdateTs DESC
        """)

        user_password = self.accounts_cursor.fetchall()

        return user_password

    def update_user_data(self, user_name='', user_password='', user_level=0, user_phone='', user_id=0):
        self.accounts_cursor.execute(f"""
            UPDATE User
            SET
                Name = "{user_name}",
                Password = "{user_password}",
                AccessLevel = {user_level},
                Phone = "{user_phone}"
            WHERE UserId = {user_id}
        """)

        self.accounts_conn.commit()

    def delete_user_data(self, user_id=0):
        self.accounts_cursor.execute(f"""
            DELETE FROM User
            WHERE UserId = {user_id}
        """)

        self.accounts_conn.commit()
