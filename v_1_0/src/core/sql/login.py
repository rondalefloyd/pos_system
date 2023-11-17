import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

cwd = os.getcwd() # get current working dir
sys.path.append(os.path.join(cwd))

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyLoginSchema:
    def __init__(self):
        self.accounts_file = os.path.abspath(qss.db_file_path + qss.accounts_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.accounts_conn = sqlite3.connect(database=self.accounts_file)
        self.accounts_cursor = self.accounts_conn.cursor()

        self.create_transaction_table()

    def create_transaction_table(self):
        self.accounts_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ItemSold (
                ItemSoldId INTEGER PRIMARY KEY AUTOINCREMENT,
                DateId INTEGER DEFAULT 0,
                CustomerId INTEGER DEFAULT 0,
                ItemPriceId INTEGER DEFAULT 0,
                StockId INTEGER DEFAULT 0,
                UserId INTEGER DEFAULT 0,
                Reason TEXT,
                Quantity INTEGER,
                TotalAmount DECIMAL(15, 2),
                Void BIT DEFAULT 0,
                ReferenceNumber TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ItemPriceId) REFERENCES ItemPrice(ItemPriceId),
                FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId),
                FOREIGN KEY (StockId) REFERENCES Stocks(StockId)
            )
        """)

        self.accounts_conn.commit()

    def verify_user(self, user_name='', user_password=''):
        try:
            self.accounts_cursor.execute(f"""
                SELECT UserId, AccessLevel, Phone FROM User
                WHERE Name = "{user_name}" AND Password = "{user_password}"
            """)

            user_data = self.accounts_cursor.fetchall()[0]
            pass
        except Exception as e:
            user_data = [(0,0,0)][0]
        return user_data
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

    def select_user_data_as_display(self):
        self.accounts_cursor.execute(f"""
            SELECT 
                Name, 
                Password, 
                AccessLevel, 
                Phone,
                UpdateTs
            FROM User
            ORDER BY UserId DESC, UpdateTs DESC
        """)

        user_data = self.accounts_cursor.fetchall() 

        return user_data
    
    def select_user_name_for_combo_box(self):
        self.accounts_cursor.execute(f"""
            SELECT Name FROM User
            ORDER BY UserId DESC, UpdateTs DESC
        """)

        user_name = self.accounts_cursor.fetchall()

        return user_name
