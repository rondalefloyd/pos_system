import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyLoginSchema:
    def __init__(self):
        self.accounts_file = os.path.abspath(qss.db_file_path + qss.accounts_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.accounts_conn = sqlite3.connect(database=self.accounts_file)
        self.accounts_cursor = self.accounts_conn.cursor()

        print('path:', qss.db_file_path + qss.sales_file_name)

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
        print('user_name:', user_name)
        print('user_password:', user_password)

        try:
            self.accounts_cursor.execute(f"""
                SELECT UserId FROM User
                WHERE Name = "{user_name}" AND Password = "{user_password}"
            """)

            user_id = self.accounts_cursor.fetchone()[0]
            pass
        except Exception as e:
            user_id = 0

        return user_id
