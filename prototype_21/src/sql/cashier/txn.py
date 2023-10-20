import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyTXNSchema():
    def __init__(self):
        super().__init__()

        self.setup_file_path()
        
        self.setup_db_conn()

        self.create_item_sold_table()

    def setup_db_conn(self):
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.txn_file)
        self.cursor = self.conn.cursor()

        self.cursor.execute(f"ATTACH DATABASE '{self.sales_file}' AS sales")
        self.cursor.execute(f"ATTACH DATABASE '{self.accounts_file}' AS accounts")

    def setup_file_path(self):
        self.txn_file = os.path.abspath(qss.db_file_path + qss.txn_file_name)
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        self.accounts_file = os.path.abspath(qss.db_file_path + qss.accounts_file_name)

    def create_item_sold_table(self):
        # item sold
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS ItemSold (
            ItemSoldId INTEGER PRIMARY KEY AUTOINCREMENT,
            DateId INTEGER DEFAULT 0,
            ItemPriceId INTEGER DEFAULT 0,
            CustomerId INTEGER DEFAULT 0,
            StockId INTEGER DEFAULT 0,
            UserId INTEGER DEFAULT 0,
            ReasonId INTEGER DEFAULT 0,
            Quantity INTEGER,
            TotalAmount DECIMAL(15, 2),
            Void BIT DEFAULT 0,
            ReferenceId TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ItemPriceId) REFERENCES ItemPrice(ItemPriceId),
            FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId),
            FOREIGN KEY (StockId) REFERENCES Stocks(StockId)
        );
        """)
        self.conn.commit()

    def update_selected_item_sold_void(self, item_sold_id, reason_id):
        self.cursor.execute(f"""
        UPDATE ItemSold
        SET ReasonId = "{reason_id}", Void = 1
        WHERE ItemSoldId = {item_sold_id}
        """)
        self.conn.commit()
        pass
    def select_item_sold_data(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        # Now execute the SELECT statement
        self.cursor.execute(f"""
        SELECT 
            User.Name,
            COALESCE(NULLIF(Customer.Name, ''), 'Guest order') AS CustomerName,
            Item.Name,
            Quantity,
            TotalAmount,
            Void,
            ReasonId,
            ReferenceId,
            ItemSold.UpdateTs,
                                 
            ItemSold.ItemSoldId,
            ItemSold.ItemPriceId,
            ItemSold.CustomerId,
            ItemSold.UserId,
            StockId
        FROM ItemSold
            LEFT JOIN sales.ItemPrice ON ItemSold.ItemPriceId = ItemPrice.ItemPriceId
            LEFT JOIN sales.Customer ON ItemSold.CustomerId = Customer.CustomerId
            LEFT JOIN accounts.User ON ItemSold.UserId = User.UserId
            LEFT JOIN sales.Item ON ItemPrice.ItemId = Item.ItemId
        WHERE Item.Name LIKE '%{text_filter}%'
        ORDER BY 
            ItemSold.ItemSoldId DESC,
            ItemSold.UpdateTs DESC
        LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
        """)

        txn = self.cursor.fetchall()

        return txn

    def select_item_sold_count(self):
        self.cursor.execute(f"""
        SELECT COUNT(*) FROM ItemSold
        """)
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def select_item_sold_total_pages_count(self, page_size=30):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM ItemSold
            """)

        total_txn = self.cursor.fetchone()[0]
        total_pages = (total_txn - 1) // page_size + 1

        return total_pages
    