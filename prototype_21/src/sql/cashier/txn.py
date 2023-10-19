import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyTXNSchema():
    def __init__(self):
        super().__init__()

        self.txn_file = os.path.abspath(qss.db_file_path + qss.txn_file_name)
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        self.accounts_file = os.path.abspath(qss.db_file_path + qss.accounts_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.txn_file)
        self.cursor = self.conn.cursor()

        # Attach the databases
        self.cursor.execute(f"ATTACH DATABASE '{self.sales_file}' AS sales")
        self.cursor.execute(f"ATTACH DATABASE '{self.accounts_file}' AS accounts")

        self.create_item_sold_table()

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

    def void_selected_txn(self, item_sold_id, void_reason):
        self.cursor.execute('''
        UPDATE ItemSold
        SET ReasonId = ?, Void = 1
        WHERE ItemSoldId = ?
        ''', (void_reason, item_sold_id))
        self.conn.commit()
        pass
    def list_all_txn_col(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        # Now execute the SELECT statement
        self.cursor.execute(f'''
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
            LEFT JOIN
                sales.ItemPrice ON ItemSold.ItemPriceId = ItemPrice.ItemPriceId
            LEFT JOIN
                sales.Customer ON ItemSold.CustomerId = Customer.CustomerId
            LEFT JOIN
                accounts.User ON ItemSold.UserId = User.UserId
            LEFT JOIN
                sales.Item ON ItemPrice.ItemId = Item.ItemId
        -- WHERE Item.Name LIKE ? OR
        ORDER BY ItemSold.ItemSoldId DESC, ItemSold.UpdateTs DESC
        LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
        ''', (
            # '%' + str(text_filter) + '%',
            page_size,  # Limit
            offset,
        ))

        txn = self.cursor.fetchall()

        return txn

    def count_all_txn(self):
        self.cursor.execute('''
        SELECT COUNT(*) FROM ItemSold
        ''')
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def count_txn_list_total_pages(self, page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM ItemSold
            ''')

        total_txn = self.cursor.fetchone()[0]
        total_pages = (total_txn - 1) // page_size + 1

        return total_pages
    