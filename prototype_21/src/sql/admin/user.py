import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyUserSchema():
    def __init__(self):
        super().__init__()

        self.setup_sales_conn()

        self.create_user_table()

    def setup_sales_conn(self):
        self.accounts_file = os.path.abspath(qss.db_file_path + qss.accounts_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.accounts_file)
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS User (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Password TEXT,
            AccessLevel INTEGER,
            Phone TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()
    
    def insert_new_user_data(self, user_name='', user_password='', user_phone=0):
        self.cursor.execute(f"""
        INSERT INTO User (Name, Password, AccessLevel, Phone)
        SELECT {user_name}, {user_password}, 1, {user_phone}
        WHERE NOT EXISTS(
            SELECT 1 FROM User
            WHERE
                Name = {user_name} AND
                Password = {user_password} AND
                AccessLevel = 1 AND -- Cashier level
                Phone = {user_phone}
            )
        """)
        self.conn.commit()
        pass
    def update_selected_user_data(self,  user_name='', user_password='', user_phone=0, user_id=0):
        self.cursor.execute(f"""
        UPDATE User
        SET Name = {user_name}, Password = {user_password}, Phone = {user_phone}
        WHERE UserId = {user_id}
        """, (user_name, user_password, user_phone, user_id))
        self.conn.commit()
        pass
    def delete_selected_user_data(self, user_id=0):
        self.cursor.execute(f"""
        DELETE FROM User
        WHERE UserId = {user_id}
        """)
        self.conn.commit()

    def select_user_data(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_user_table()

        self.cursor.execute(f"""
        SELECT 
            COALESCE(NULLIF(Name, ''), '[no data]') AS Name,
            COALESCE(NULLIF(Password, ''), '[no data]') AS Password,
            COALESCE(NULLIF(Phone, ''), '[no data]') AS Phone,
            UpdateTs,
            UserId,
            AccessLevel FROM User
        WHERE
            (Name LIKE '%{text_filter}%' OR
            Password LIKE '%{text_filter}%' OR
            Phone LIKE '%{text_filter}%' OR
            UpdateTs LIKE '%{text_filter}%') AND
            AccessLevel BETWEEN 1 AND 2
        ORDER BY 
            CASE WHEN AccessLevel = 2 THEN 1 ELSE 2 END,
            UserId DESC, 
            UpdateTs DESC
        LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
        """)
        
        user = self.cursor.fetchall()
        
        return user

    def select_user_count(self):
        self.create_user_table()

        self.cursor.execute(f"""
        SELECT COUNT(*) FROM User
        """)
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def select_user_total_pages_count(self, page_size=30):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM User
            """)

        total_user = self.cursor.fetchone()[0]
        total_pages = (total_user - 1) // page_size + 1

        return total_pages
    