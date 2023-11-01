import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyTXNSchema:
    def __init__(self):
        self.txn_file = os.path.abspath(qss.db_file_path + qss.txn_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.txn_conn = sqlite3.connect(database=self.txn_file)
        self.txn_cursor = self.txn_conn.cursor()

        print('path:', qss.db_file_path + qss.sales_file_name)

        self.txn_cursor.execute(f"ATTACH DATABASE '{qss.db_file_path + qss.sales_file_name}' AS sales")
        self.txn_cursor.execute(f"ATTACH DATABASE '{qss.db_file_path + qss.accounts_file_name}' AS accounts")

        self.create_transaction_table()

    def create_transaction_table(self):
        self.txn_cursor.execute(f"""
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

        self.txn_conn.commit()

    def select_item_sold_data_as_display(self, text='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        # Now execute the SELECT statement
        self.txn_cursor.execute(f"""
            SELECT 
                User.Name,
                COALESCE(NULLIF(Customer.Name, ''), 'Guest') AS CustomerName,
                Item.Name,
                ItemSold.Quantity,
                ItemSold.TotalAmount,
                ItemSold.Void,
                ItemSold.Reason,
                ItemSold.ReferenceNumber,
                ItemSold.UpdateTs,
                                    
                ItemSold.ItemSoldId,
                ItemSold.ItemPriceId,
                ItemSold.CustomerId,
                ItemSold.UserId,
                Stock.StockId
            FROM ItemSold
                LEFT JOIN sales.ItemPrice ON ItemSold.ItemPriceId = ItemPrice.ItemPriceId
                LEFT JOIN sales.Customer ON ItemSold.CustomerId = Customer.CustomerId
                LEFT JOIN accounts.User ON ItemSold.UserId = User.UserId
                LEFT JOIN sales.Item ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN sales.Stock ON Item.ItemId = Stock.ItemId
            WHERE Item.Name LIKE "%{text}%" OR ItemSold.ReferenceNumber LIKE "%{text}%"
            ORDER BY 
                ItemSold.ItemSoldId DESC,
                ItemSold.UpdateTs DESC
            LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
        """)


        txn = self.txn_cursor.fetchall()

        return txn
        pass
    

    def select_item_sold_data(self, item_sold_id=0, product_price_id=0, customer_id=0, user_id=0):
        self.txn_cursor.execute(f"""
            SELECT 
                Reason,

                ItemSoldId,
                ItemPriceId,
                CustomerId,
                UserId
            FROM Promo
            WHERE
                ItemSoldId = {item_sold_id} AND
                ItemPriceId = {product_price_id} AND
                CustomerId = {customer_id} AND
                UserId = {user_id}
            ORDER BY ItemSoldId DESC, UpdateTs DESC
        """)

        item_sold_data = self.txn_cursor.fetchall()

        return item_sold_data
    
        pass
    def select_item_sold_data_total_page_count(self, text='', page_size=30):
        self.txn_cursor.execute(f"""
            SELECT COUNT(*) FROM ItemSold
            LEFT JOIN sales.ItemPrice ON ItemSold.ItemPriceId = ItemPrice.ItemPriceId
            LEFT JOIN sales.Item ON ItemPrice.ItemId = Item.ItemId
            WHERE Item.Name LIKE "%{text}%" OR ItemSold.ReferenceNumber LIKE "%{text}%"
        """)

        total_item_sold_data_count = self.txn_cursor.fetchone()[0]
        total_page_count = (total_item_sold_data_count - 1) // page_size + 1

        return total_page_count
    
    def update_selected_item_sold_void(
            self,
            item_sold_id,
            product_price_id,
            customer_id,
            user_id,
            stock_id,
            reason,
            product_qty=0
    ):
        self.txn_cursor.execute(f"""
            UPDATE ItemSold
            SET Reason = "{reason}", Void = 1
            WHERE 
                ItemSoldId = {item_sold_id} AND
                ItemPriceId = {product_price_id} AND
                CustomerId = {customer_id} AND
                UserId = {user_id} AND
                StockId = {stock_id}
        """)
        
        if stock_id is not None or stock_id > 0:
            # REVIEW: execute depending on the specific reason?
            self.txn_cursor.execute(f"""
                UPDATE Stock
                SET OnHand = Onhand + {product_qty}
                WHERE StockId = {stock_id}
            """)

            self.txn_conn.commit()