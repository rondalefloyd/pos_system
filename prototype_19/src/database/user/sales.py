import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SalesSchema():
    def __init__(self):
        super().__init__()
        # Creates folder for the db file
        self.db_file_path = os.path.abspath('data/sales.db')
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/')), exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

        self.create_product_table()

    def create_product_table(self):
        # item type
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ItemType (
            ItemTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        ''')
        self.conn.commit()

        # brand
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Brand (
            BrandId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        ''')
        self.conn.commit()

        # sales group
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS SalesGroup (
            SalesGroupId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        # supplier
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        # item
        self.cursor.execute('''
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
        ''')
        self.conn.commit()

        # item price
        self.cursor.execute('''
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
        ''')
        self.conn.commit()

        # stock
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            StockId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemId INTEGER DEFAULT 0,
            OnHand INTEGER,
            Available INTEGER,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ItemId) REFERENCES Item(ItemId)
        );
        ''')

        # customer
        self.cursor.execute('''
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
        ''')
        self.conn.commit()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS CustomerReward (
            CustomerId INTEGER,
            RewardId INTEGER,
            Points INTEGER,  
            CurrencyAmount FLOAT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        # item sold
        self.cursor.execute('''
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
        ''')
        self.conn.commit()
        
    def list_product(self, text_filter='', order_type='Retail', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_product_table()

        self.cursor.execute('''
            SELECT
                COALESCE(NULLIF(Item.Barcode, ''), '[no data]') AS Barcode,
                COALESCE(NULLIF(Item.Name, ''), '[no data]') AS Item, -- 1
                COALESCE(NULLIF(Item.ExpireDt, ''), '[no data]') AS ExpireDt,
                            
                COALESCE(NULLIF(ItemType.Name, ''), '[no data]') AS ItemType, 
                COALESCE(NULLIF(Brand.Name, ''), '[no data]') AS Brand, -- 4 
                COALESCE(NULLIF(SalesGroup.Name, ''), '[no data]') AS SalesGroup, -- 5
                COALESCE(NULLIF(Supplier.Name, ''), '[no data]') AS Supplier,
                            
                COALESCE(NULLIF(ItemPrice.Cost, ''), '[no data]') AS Cost,
                COALESCE(NULLIF(ItemPrice.SellPrice, ''), '[no data]') AS SellPrice, -- 8
                COALESCE(NULLIF(ItemPrice.EffectiveDt, ''), '[no data]') AS EffectiveDt,
                CASE WHEN Promo.Name IS NOT NULL THEN Promo.Name ELSE 'No promo' END AS Promo,
                COALESCE(NULLIF(ItemPrice.DiscountValue, ''), '[no data]') AS DiscountValue, -- 11

                CASE WHEN Stock.StockId <> 0 THEN 'Enabled' ELSE 'Disabled' END AS InventoryTracking,
                COALESCE(NULLIF(Stock.Available, ''), '[no data]') AS Available,
                COALESCE(NULLIF(Stock.OnHand, ''), '[no data]') AS OnHand,
                            
                ItemPrice.UpdateTs, -- 15
                                
                ItemPrice.ItemId,
                ItemPrice.ItemPriceId,
                ItemPrice.PromoId,
                Stock.StockId
                            
            FROM ItemPrice
                LEFT JOIN Item
                    ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType
                    ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand
                    ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier
                    ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup
                    ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo
                    ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock
                    ON Item.ItemId = Stock.ItemId
            WHERE 
                (Item.Barcode LIKE ? OR
                Item.Name LIKE ? OR
                ItemType.Name LIKE ? OR 
                Brand.Name LIKE ? OR 
                Supplier.Name LIKE ? OR
                InventoryTracking LIKE ?) AND
                SalesGroup.Name = ? AND
                ItemPrice.EffectiveDt <= CURRENT_DATE
            ORDER BY Item.ItemId DESC, ItemPrice.EffectiveDt DESC, ItemPrice.UpdateTs DESC
            LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
            ''', (
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                order_type,
                page_size,  # Limit
                offset     # Offset
            ))

        product = self.cursor.fetchall()

        return product

    def list_product_via_promo(self, text_filter='', order_type='Retail', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size
        
        self.create_product_table()

        self.cursor.execute('''
            SELECT
                COALESCE(NULLIF(Item.Barcode, ''), '[no data]') AS Barcode,
                COALESCE(NULLIF(Item.Name, ''), '[no data]') AS Item,
                COALESCE(NULLIF(Item.ExpireDt, ''), '[no data]') AS ExpireDt,
                            
                COALESCE(NULLIF(ItemType.Name, ''), '[no data]') AS ItemType, 
                COALESCE(NULLIF(Brand.Name, ''), '[no data]') AS Brand, 
                COALESCE(NULLIF(SalesGroup.Name, ''), '[no data]') AS SalesGroup, 
                COALESCE(NULLIF(Supplier.Name, ''), '[no data]') AS Supplier,
                            
                COALESCE(NULLIF(ItemPrice.Cost, ''), '[no data]') AS Cost,
                COALESCE(NULLIF(ItemPrice.SellPrice, ''), '[no data]') AS SellPrice,
                COALESCE(NULLIF(ItemPrice.EffectiveDt, ''), '[no data]') AS EffectiveDt,
                CASE WHEN Promo.Name IS NOT NULL THEN Promo.Name ELSE 'No promo' END AS Promo,
                COALESCE(NULLIF(ItemPrice.DiscountValue, ''), '[no data]') AS DiscountValue,

                CASE WHEN Stock.StockId <> 0 THEN 'Enabled' ELSE 'Disabled' END AS InventoryTracking,
                COALESCE(NULLIF(Stock.Available, ''), '[no data]') AS Available,
                COALESCE(NULLIF(Stock.OnHand, ''), '[no data]') AS OnHand,
                            
                ItemPrice.UpdateTs, -- 15
                                
                ItemPrice.ItemId,
                ItemPrice.ItemPriceId,
                ItemPrice.PromoId,
                Stock.StockId
                            
            FROM ItemPrice
                LEFT JOIN Item
                    ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType
                    ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand
                    ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier
                    ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup
                    ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo
                    ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock
                    ON Item.ItemId = Stock.ItemId     
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
            ''', (
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                order_type,
                page_size,  # Limit
                offset     # Offset
            ))

        prod_with_promo = self.cursor.fetchall()

        return prod_with_promo
    
    def list_customer(self, customer=''):
        self.cursor.execute('''
        SELECT 
            Customer.Name, Customer.Phone, CustomerReward.Points
        FROM Customer
            LEFT JOIN CustomerReward
                ON Customer.CustomerId = CustomerReward.CustomerId
        WHERE Customer.Name LIKE ?
        ORDER BY Customer.UpdateTs DESC
            
        ''', ('%' + str(customer) + '%',))
        
        customer = self.cursor.fetchall()
        
        return customer

    def list_product_via_barcode(self, barcode='', order_type='Retail'):
        self.create_product_table()

        self.cursor.execute('''
            SELECT
                COALESCE(NULLIF(Item.Barcode, ''), '[no data]') AS Barcode,
                COALESCE(NULLIF(Item.Name, ''), '[no data]') AS Item,
                COALESCE(NULLIF(Item.ExpireDt, ''), '[no data]') AS ExpireDt,
                            
                COALESCE(NULLIF(ItemType.Name, ''), '[no data]') AS ItemType, 
                COALESCE(NULLIF(Brand.Name, ''), '[no data]') AS Brand, 
                COALESCE(NULLIF(SalesGroup.Name, ''), '[no data]') AS SalesGroup, 
                COALESCE(NULLIF(Supplier.Name, ''), '[no data]') AS Supplier,
                            
                COALESCE(NULLIF(ItemPrice.Cost, ''), '[no data]') AS Cost,
                COALESCE(NULLIF(ItemPrice.SellPrice, ''), '[no data]') AS SellPrice,
                COALESCE(NULLIF(ItemPrice.EffectiveDt, ''), '[no data]') AS EffectiveDt,
                CASE WHEN Promo.Name IS NOT NULL THEN Promo.Name ELSE 'No promo' END AS Promo,
                COALESCE(NULLIF(ItemPrice.DiscountValue, ''), '[no data]') AS DiscountValue,

                CASE WHEN Stock.StockId <> 0 THEN 'Enabled' ELSE 'Disabled' END AS InventoryTracking,
                COALESCE(NULLIF(Stock.Available, ''), '[no data]') AS Available,
                COALESCE(NULLIF(Stock.OnHand, ''), '[no data]') AS OnHand,
                            
                ItemPrice.UpdateTs, -- 15
                                
                ItemPrice.ItemId,
                ItemPrice.ItemPriceId,
                ItemPrice.PromoId,
                Stock.StockId
                            
            FROM ItemPrice
                LEFT JOIN Item
                    ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType
                    ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand
                    ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier
                    ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup
                    ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo
                    ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock
                    ON Item.ItemId = Stock.ItemId
            WHERE
                Item.Barcode LIKE ? AND ItemPrice.EffectiveDt <= CURRENT_DATE
            ORDER BY 
                Item.ItemId DESC, ItemPrice.EffectiveDt DESC, ItemPrice.UpdateTs DESC LIMIT 1
            ''', (barcode,))

        product = self.cursor.fetchall()

        return product
    
    def get_customer_id(self, customer):
        self.cursor.execute('''
        SELECT CustomerId FROM Customer
        WHERE Name = ?
        ORDER BY Customer.UpdateTs DESC
        ''', (customer,))
        
        customer_id = self.cursor.fetchone()[0]

        return customer_id
    
    def register_transaction(
        self,
        item_id='',
        customer='',
        user='',

        date_id='',
        item_price_id='',
        customer_id='',
        stock_id='',
        user_id='',
        quantity='',
        reason_id='',
        total_amount='',
        void='',
        reference_id=''
    ):
        item_price_id = self.cursor.execute('''
        SELECT ItemPriceId FROM ItemPrice
        WHERE ItemId = ?
        ''', (item_id,))
        item_price_id = self.cursor.fetchone()[0]

        customer_id = self.cursor.execute('''
        SELECT CustomerId FROM Customer
        WHERE Name = ?
        ''', (customer,))
        customer_id = self.cursor.fetchone()[0]

        stock_id = self.cursor.execute('''
        SELECT StockId FROM Stock
        WHERE Name = ?
        ''', (item_id,))
        stock_id = self.cursor.fetchone()[0]

        user_id = self.cursor.execute('''
        SELECT UserId FROM User
        WHERE Name = ?
        ''', (user,))
        user_id = self.cursor.fetchone()[0]

        print('item_price_id:', item_price_id)
        print('customer_id:', customer_id)
        print('stock_id:', stock_id)
        print('user_id:', user_id)

        # self.cursor.execute('''
        # INSERT INTO ItemSold (
        #     DateId,
        #     ItemPriceId,
        #     CustomerId,
        #     StockId,
        #     UserId,
        #     Quantity,
        #     ReasonId,
        #     TotalAmount,
        #     Void,
        #     ReferenceId
        # )
        # SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        # WHERE NOT EXISTS(
        # SELECT 1 FROM ItemSold
        # WHERE
        #     DateId = ? AND
        #     ItemPriceId = ? AND
        #     CustomerId = ? AND
        #     StockId = ? AND
        #     UserId = ? AND
        #     Quantity = ? AND
        #     ReasonId = ? AND
        #     TotalAmount = ? AND
        #     Void = ? AND
        #     ReferenceId = ?
                            
        # )''', (date_id, item_price_id, customer_id, stock_id, user_id, quantity, reason_id, total_amount, void, reference_id,
        #     date_id, item_price_id, customer_id, stock_id, user_id, quantity, reason_id, total_amount, void, reference_id))
        # self.conn.commit()
        # pass
    
    def count_product(self):
        self.create_product_table()

        self.cursor.execute('''
        SELECT COUNT(*) FROM ItemPrice
        ''')
        count = self.cursor.fetchone()[0]
        
        return count

    def count_product_list_total_pages(self, order_type='Retail', page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM ItemPrice
                LEFT JOIN Item
                    ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType
                    ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand
                    ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier
                    ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup
                    ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo
                    ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock
                    ON Item.ItemId = Stock.ItemId
            WHERE 
                SalesGroup.Name = ? AND
                ItemPrice.EffectiveDt <= CURRENT_DATE
            ''', (order_type,))

        total_product = self.cursor.fetchone()[0]
        total_pages = (total_product - 1) // page_size + 1

        return total_pages

    def count_product_list_via_promo_total_pages(self, order_type='Retail', page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM ItemPrice
                LEFT JOIN Item
                    ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType
                    ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand
                    ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier
                    ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup
                    ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo
                    ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock
                    ON Item.ItemId = Stock.ItemId
            WHERE 
                SalesGroup.Name = ? AND
                Promo.Name != 'No promo' AND
                ItemPrice.EffectiveDt <= CURRENT_DATE
            ''', (order_type,))

        total_product = self.cursor.fetchone()[0]
        total_pages = (total_product - 1) // page_size + 1

        return total_pages
