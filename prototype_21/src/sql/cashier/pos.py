import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyPOSSchema():
    def __init__(self):
        super().__init__()

        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)
        
        self.setup_sales_db_conn()
        self.setup_txn_db_conn()

        self.create_all_sales_table()

        self.init_list_all_prod_query_entry()

    def init_list_all_prod_query_entry(self):
        self.select_prod_col = """
            COALESCE(NULLIF(Item.Barcode, ''), '[no data]') AS Barcode,
            COALESCE(NULLIF(Item.Name, ''), '[no data]') AS Product,
            COALESCE(NULLIF(Brand.Name, ''), '[no data]') AS Brand, 
            COALESCE(NULLIF(ItemPrice.SellPrice, ''), '[no data]') AS SellPrice,
            COALESCE(NULLIF(ItemPrice.EffectiveDt, ''), '[no data]') AS EffectiveDt,
            CASE WHEN Promo.Name IS NOT NULL THEN Promo.Name ELSE 'No promo' END AS Promo,
            ItemPrice.DiscountValue AS Discount,
            CASE
                WHEN Stock.OnHand IS NULL THEN 'N/A'
                WHEN Stock.OnHand = 0 THEN 'Out of stock'
                ELSE CAST(Stock.OnHand AS TEXT) -- Or use the appropriate data type conversion
            END AS OnHand,
            ItemPrice.UpdateTs AS DateTimeCreated, -- 8
            ItemPrice.ItemId, -- 9
            ItemPrice.ItemPriceId, -- 10
            ItemPrice.PromoId, -- 11
            Stock.StockId, -- 12
            SalesGroup.Name -- 13
        """
        self.join_prod_table = """
            LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
            LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
            LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
            LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
            LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
            LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
            LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
        """

    def setup_sales_db_conn(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        self.sales_conn = sqlite3.connect(database=self.sales_file)
        self.sales_cursor = self.sales_conn.cursor()
        pass
    def setup_txn_db_conn(self):
        self.txn_file = os.path.abspath(qss.db_file_path + qss.txn_file_name)
        self.txn_conn = sqlite3.connect(database=self.txn_file)
        self.txn_cursor = self.txn_conn.cursor()

    def create_all_sales_table(self):
        # item type
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS ItemType (
            ItemTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        """)
        self.sales_conn.commit()

        # brand
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Brand (
            BrandId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        """)
        self.sales_conn.commit()

        # sales group
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS SalesGroup (
            SalesGroupId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.sales_conn.commit()

        # supplier
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.sales_conn.commit()

        # item
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Item (
            ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            Barcode TEXT,
            Name TEXT,
            ItemTypeId INTEGER DEFAULT 0,
            BrandId INTEGER DEFAULT 0,
            SalesGroupId INTEGER DEFAULT 0,
            SupplierId INTEGER DEFAULT 0,
            ExpireDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (ItemTypeId) REFERENCES ItemType(ItemTypeId),
            FOREIGN KEY (BrandId) REFERENCES Brand(BrandId),
            FOREIGN KEY (SalesGroupId) REFERENCES SalesGroup(SalesGroupId),
            FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId)
        );
        """)
        self.sales_conn.commit()

        # item price
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS ItemPrice (
            ItemPriceId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemId INTEGER DEFAULT 0,
            EffectiveDt DATETIME,
            PromoId INTEGER DEFAULT 0,
            Cost DECIMAL(15, 2),
            SellPrice DECIMAL(15, 2),
            DiscountValue DECIMAL(15, 2),
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (ItemId) REFERENCES Item(ItemId),
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)
        );
        """)
        self.sales_conn.commit()

        # stock
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Stock (
            StockId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemId INTEGER DEFAULT 0,
            OnHand INTEGER,
            Available INTEGER,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ItemId) REFERENCES Item(ItemId)
        );
        """)

        # customer
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Address TEXT,
            Barrio TEXT,
            Town TEXT,
            Phone TEXT,
            Age INTEGER,
            Gender TEXT,
            MaritalStatus TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.sales_conn.commit()

        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS CustomerReward (
            CustomerId INTEGER,
            RewardId INTEGER,
            Points INTEGER,  
            CurrencyAmount FLOAT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.sales_conn.commit()

        # saved order
        self.sales_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS SavedOrder (
            SavedOrderId INTEGER PRIMARY KEY AUTOINCREMENT,
            SalesGroupId INTEGER DEFAULT 0,
            CustomerId INTEGER DEFAULT 0,
            StockId INTEGER DEFAULT 0,
            UserId INTEGER DEFAULT 0,
            Quantity INTEGER,
            Name TEXT,
            TotalAmount DECIMAL(15,2),
            DiscountValue DECIMAL (15,2),
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (SalesGroupId) REFERENCES SalesGroup(SalesGroupId),
            FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
        );
        """)
        self.sales_conn.commit()

        # item sold
        self.sales_cursor.execute(f"""
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
        self.sales_conn.commit()

    def add_new_txn(self, item_name, customer, quantity, total_amount,):
        # REVIEW: needs to be reviewed
        item_id = self.txn_cursor.execute(f"""
            SELECT ItemId FROM Item
            WHERE Name = ?
        """, (item_name,))
        item_id = self.txn_cursor.fetchone()[0]

        item_price_id = self.txn_cursor.execute(f"""
            SELECT ItemPriceId FROM ItemPrice
            WHERE ItemId = ?
        """, (item_id,))
        item_price_id = self.txn_cursor.fetchone()[0]
        
        if customer == 'Order':
            customer_id = 0
            pass
        else:
            customer_id = self.txn_cursor.execute(f"""
                SELECT CustomerId FROM Customer
                WHERE Name = ?
            """, (customer,))
            customer_id = self.txn_cursor.fetchone()[0]
            

        self.txn_cursor.execute(f"""
            INSERT INTO ItemSold (ItemPriceId, CustomerId, Quantity, TotalAmount)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS(
                SELECT 1 FROM ItemSold
                WHERE 
                    ItemPriceId = ? AND 
                    CustomerId = ? AND
                    Quantity = ? AND 
                    TotalAmount = ?
            )""", (item_price_id, customer_id, quantity, total_amount,
                   item_price_id, customer_id, quantity, total_amount))
        
        self.txn_conn.commit()

    def list_all_prod_col(self, text_filter='', prod_type='Retail', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_all_sales_table()

        self.sales_cursor.execute(f"""
            SELECT
                {self.select_prod_col}
            FROM ItemPrice
                {self.join_prod_table}
            WHERE 
                (Item.Barcode LIKE ? OR
                Item.Name LIKE ? OR
                ItemType.Name LIKE ? OR 
                Brand.Name LIKE ? OR 
                Supplier.Name LIKE ? OR
                Stock.OnHand LIKE ?) AND
                SalesGroup.Name = ?
                -- ItemPrice.EffectiveDt <= CURRENT_DATE -- NEEDS TO BE CHECKED
            ORDER BY Item.ItemId DESC, ItemPrice.EffectiveDt DESC, ItemPrice.UpdateTs DESC
            LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
            """, (
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                prod_type,
                page_size,  # Limit
                offset     # Offset
            ))

        product = self.sales_cursor.fetchall()

        return product
    pass
    def list_all_prod_col_via_promo(self, text_filter='', prod_type='Retail', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size
        
        self.create_all_sales_table()

        self.sales_cursor.execute(f"""
            SELECT
                {self.select_prod_col}  
            FROM ItemPrice
                {self.join_prod_table}
            WHERE 
                (Item.Barcode LIKE ? OR
                Item.Name LIKE ? OR
                ItemType.Name LIKE ? OR 
                Brand.Name LIKE ? OR 
                Supplier.Name LIKE ? OR
                InventoryTracking LIKE ?) AND
                SalesGroup.Name = ? AND
                Promo.Name != 'No promo' AND
                ItemPrice.EffectiveDt <= CURRENT_DATE
            ORDER BY Item.ItemId DESC, ItemPrice.EffectiveDt DESC, ItemPrice.UpdateTs DESC
            LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
            """, (
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                prod_type,
                page_size,  # Limit
                offset     # Offset
            ))

        prod_with_promo = self.sales_cursor.fetchall()

        return prod_with_promo
    def list_all_prod_col_via_barcode(self, barcode='', prod_type='Retail'):
        self.create_all_sales_table()

        self.sales_cursor.execute(f"""
            SELECT
                {self.select_prod_col}         
            FROM ItemPrice
                {self.join_prod_table}
            WHERE
                Item.Barcode LIKE ? AND SalesGroup.Name LIKE ? AND ItemPrice.EffectiveDt <= CURRENT_DATE
            ORDER BY 
                Item.ItemId DESC, EffectiveDt DESC, DateTimeCreated DESC LIMIT 1
            """, (barcode, prod_type))

        product = self.sales_cursor.fetchall()

        return product
   
    def list_cust_name_col(self):
        cust_name = self.sales_cursor.execute(f"""
        SELECT DISTINCT Name FROM Customer
        ORDER BY UpdateTs DESC 
        """)
        cust_name = self.sales_cursor.fetchall()

        return cust_name
        
        pass
    def list_all_cust_col_via_cust_id(self, cust_id=''):
        self.sales_cursor.execute(f"""
        SELECT 
            Customer.Name AS Name,
            Customer.Phone AS Phone,
            CustomerReward.Points AS Points
        FROM Customer
            LEFT JOIN CustomerReward
                ON Customer.CustomerId = CustomerReward.CustomerId
        WHERE Customer.CustomerId LIKE ?
        ORDER BY Customer.UpdateTs DESC
            
        """, ('%' + str(cust_id) + '%',))
        
        customer = self.sales_cursor.fetchall()
        
        return customer
    
    def list_cust_id(self, cust):
        self.sales_cursor.execute(f"""
        SELECT CustomerId FROM Customer
        WHERE Name = ?
        ORDER BY Customer.UpdateTs DESC
        """, (cust,))
        
        customer_id = self.sales_cursor.fetchone()[0]

        return customer_id
    
    def count_all_prod(self):
        self.create_all_sales_table()

        self.sales_cursor.execute(f"""
        SELECT COUNT(*) FROM ItemPrice
        """)
        count = self.sales_cursor.fetchone()[0]
        
        return count
    def count_prod_list_total_pages(self, text_filter='', prod_type='Retail', page_size=30):
        self.sales_cursor.execute(f"""
            SELECT COUNT(*)
            FROM ItemPrice
                {self.join_prod_table}
            WHERE 
                (Item.Barcode LIKE ? OR
                Item.Name LIKE ? OR
                ItemType.Name LIKE ? OR 
                Brand.Name LIKE ? OR 
                Supplier.Name LIKE ? OR
                Stock.OnHand LIKE ?) AND
                SalesGroup.Name = ? AND
                ItemPrice.EffectiveDt <= CURRENT_DATE
            """, (
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                prod_type,
            ))

        total_product = self.sales_cursor.fetchone()[0]
        total_pages = (total_product - 1) // page_size + 1

        return total_pages
    
    def count_prod_list_via_promo_total_pages(self, prod_type='Retail', page_size=30):
        self.sales_cursor.execute(f"""
            SELECT COUNT(*)
            FROM ItemPrice
                {self.join_prod_table}
            WHERE 
                SalesGroup.Name = ? AND
                Promo.Name != 'No promo' AND
                ItemPrice.EffectiveDt <= CURRENT_DATE
            """, (prod_type,))

        total_product = self.sales_cursor.fetchone()[0]
        total_pages = (total_product - 1) // page_size + 1

        return total_pages
