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
        self.setup_accounts_db_conn()

        self.create_sales_table()

        self.setup_repeating_queries()
 
    def setup_repeating_queries(self):
        self.select_prod_column_query = """
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
        self.join_prod_table_query = """
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
        pass
    def setup_accounts_db_conn(self):
        self.accounts_file = os.path.abspath(qss.db_file_path + qss.accounts_file_name)
        self.accounts_conn = sqlite3.connect(database=self.accounts_file)
        self.accounts_cursor = self.accounts_conn.cursor()
        pass
    
    def create_sales_table(self):
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

        # item sold
        self.txn_cursor.execute(f"""
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
        self.txn_conn.commit()

    def select_prod_data(self, text_filter='', prod_type='Retail', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
            SELECT * FROM (
                SELECT
                    {self.select_prod_column_query},
                    RANK () OVER ( 
                        PARTITION BY ItemPrice.ItemId
                        ORDER BY ItemPrice.UpdateTs DESC
                    ) ValRank
                FROM ItemPrice
                    {self.join_prod_table_query}
                WHERE 
                    (Item.Barcode LIKE '%{text_filter}%' OR
                    Item.Name LIKE '%{text_filter}%' OR
                    ItemType.Name LIKE '%{text_filter}%' OR 
                    Brand.Name LIKE '%{text_filter}%' OR 
                    Supplier.Name LIKE '%{text_filter}%' OR
                    Stock.OnHand LIKE '%{text_filter}%') AND
                    SalesGroup.Name = "{prod_type}" AND
                    ItemPrice.EffectiveDt <= CURRENT_DATE
                    
                ORDER BY 
                    Item.ItemId DESC, 
                    ItemPrice.EffectiveDt DESC, 
                    ItemPrice.UpdateTs DESC          
            )
            WHERE ValRank = 1
            LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
            """)

        product = self.sales_cursor.fetchall()

        return product
        pass
    def select_prod_data_via_barcode(self, barcode='', prod_type='Retail'):
        self.create_sales_table()

        self.sales_cursor.execute(f"""
            SELECT
                {self.select_prod_column_query}         
            FROM ItemPrice
                {self.join_prod_table_query}
            WHERE
                Item.Barcode LIKE "{barcode}" AND SalesGroup.Name LIKE "{prod_type}" AND ItemPrice.EffectiveDt <= CURRENT_DATE
            ORDER BY 
                Item.ItemId DESC, 
                EffectiveDt DESC, 
                DateTimeCreated DESC 
            LIMIT 1
            """)

        product = self.sales_cursor.fetchall()

        return product
    def select_all_cust_name(self):
        cust_name = self.sales_cursor.execute(f"""
        SELECT DISTINCT Name FROM Customer
        ORDER BY UpdateTs DESC 
        """)
        cust_name = self.sales_cursor.fetchall()

        return cust_name
        
        pass
    def select_cust_data_via_cust_id(self, cust_id=''):
        try:
            self.sales_cursor.execute(f"""
            SELECT 
                Customer.Name AS Name,
                Customer.Phone AS Phone,
                CustomerReward.Points AS Points
            FROM Customer
                LEFT JOIN CustomerReward
                    ON Customer.CustomerId = CustomerReward.CustomerId
            WHERE Customer.CustomerId LIKE '%{cust_id}%'
            ORDER BY Customer.UpdateTs DESC
                
            """)
            
            customer = self.sales_cursor.fetchall()
            pass
        except Exception as e:
            customer = ''

        return customer

    def select_prod_count(self):
        self.create_sales_table()

        self.sales_cursor.execute(f"""
        SELECT COUNT(*) FROM ItemPrice
        """)
        count = self.sales_cursor.fetchone()[0]
        
        return count
    def select_prod_total_pages_count(self, text_filter='', prod_type='Retail', page_size=30):
        self.sales_cursor.execute(f"""
            SELECT COUNT(*)
            FROM ItemPrice
                {self.join_prod_table_query}
            WHERE 
                (Item.Barcode LIKE '%{text_filter}%' OR
                Item.Name LIKE '%{text_filter}%' OR
                ItemType.Name LIKE '%{text_filter}%' OR 
                Brand.Name LIKE '%{text_filter}%' OR 
                Supplier.Name LIKE '%{text_filter}%' OR
                Stock.OnHand LIKE '%{text_filter}%') AND
                SalesGroup.Name = "{prod_type}" AND
                ItemPrice.EffectiveDt <= CURRENT_DATE
            """)

        total_product = self.sales_cursor.fetchone()[0]
        total_pages = (total_product - 1) // page_size + 1

        return total_pages

    def insert_new_item_sold_data(
        self,
        item_price_id=0,
        cust_id=0,
        stock_id=0,
        user_id=0,
        prod_qty=0,
        prod_price=0,
        ref_id=''
    ):

        self.txn_cursor.execute(f"""
		INSERT INTO ItemSold (
            DateId # TODO:              
            ItemPriceId,
            CustomerId,
            StockId,
            UserId,
            Quantity,
            TotalAmount,
            ReferenceId
        )
		SELECT 
            {item_price_id},
            {cust_id},  
            {stock_id},
            {user_id},
            {prod_qty},
            {prod_price},
            "{ref_id}"
		""")

        self.txn_conn.commit()
        pass
    
    def update_cust_reward_points(self, cust_id, prod_price):
        try:
            reward_points = self.sales_cursor.execute(f"""
            SELECT Points FROM Reward
            WHERE {prod_price} >= Unit 
            ORDER BY Unit DESC
            LIMIT 1
            """)

            reward_points = self.sales_cursor.fetchone()[0]

            self.sales_cursor.execute(f"""
            UPDATE CustomerReward
            SET 
                Points = Points + {reward_points},
                UpdateTs = CURRENT_TIMESTAMP		
            WHERE CustomerId = {cust_id}
            """)

            self.sales_conn.commit()
        except Exception as e:
            print(e)
            pass
        pass
    def update_stock_on_hand(self, item_id, stock_id, prod_qty):
        try:
            print('item_id:', item_id)
            print('stock_id:', stock_id)
            print('prod_qty:', prod_qty)
            self.sales_cursor.execute(f"""
            UPDATE Stock
            SET 
                OnHand = CASE 
                    WHEN (OnHand - {prod_qty}) < 0 THEN 0 
                    ELSE (OnHand - {prod_qty}) 
                END
            WHERE 
                ItemId = {item_id} AND 
                StockId = {stock_id}
            """)
            
            self.sales_conn.commit()
        except Exception as e:
            print(e)
            pass

    def select_item_id(self, prod_name):
        item_id = self.sales_cursor.execute(f"""
            SELECT ItemId FROM Item
            WHERE Name = "{prod_name}"
        """)
        item_id = self.sales_cursor.fetchone()[0]

        return item_id
    def select_item_price_id(self, item_id):
        item_price_id = self.sales_cursor.execute(f"""
            SELECT ItemPriceId FROM ItemPrice
            WHERE ItemId = {item_id}
        """)
        item_price_id = self.sales_cursor.fetchone()[0]

        return item_price_id
    def select_sales_group_id(self, sales_group):
        sales_group_id = self.sales_cursor.execute(f"""
            SELECT SalesGroupId FROM SalesGroup
            WHERE Name = "{sales_group}"
        """)
        sales_group_id = self.sales_cursor.fetchone()[0]

        return sales_group_id
    def select_cust_id(self, cust_name):
        try:
            cust_id = self.sales_cursor.execute(f"""
                SELECT CustomerId FROM Customer
                WHERE Name = "{cust_name}"
            """)
            cust_id = self.sales_cursor.fetchone()[0]
        except Exception as e:
            cust_id = 0

        return cust_id
    def select_stock_id(self, item_id):
        try:
            stock_id = self.sales_cursor.execute(f"""
                SELECT StockId FROM Stock
                WHERE ItemId = {item_id}
            """)
            stock_id = self.sales_cursor.fetchone()[0]
            pass
        except Exception as e:
            stock_id = 0
        
        return stock_id
    def select_user_id(self, user_name):
        try:
            user_id = self.accounts_cursor.execute(f"""
                SELECT UserId FROM User
                WHERE Name = "{user_name}"
            """)
            user_id = self.accounts_cursor.fetchone()[0]
            pass
        except Exception as e:
            user_id = 0

            
        return user_id
