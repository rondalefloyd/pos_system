import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyProdSchema():
    def __init__(self):
        super().__init__()

        self.setup_sales_conn()

        self.create_prod_table()

    def setup_sales_conn(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.sales_file)
        self.cursor = self.conn.cursor()

    def create_prod_table(self):
        # item type
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS ItemType (
            ItemTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        """)
        self.conn.commit()

        # brand
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Brand (
            BrandId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        """)
        self.conn.commit()

        # sales group
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS SalesGroup (
            SalesGroupId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

        # supplier
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

        # item
        self.cursor.execute(f"""
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
        self.conn.commit()

        # item price
        self.cursor.execute(f"""
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
        self.conn.commit()

        # stock
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Stock (
            StockId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemId INTEGER DEFAULT 0,
            OnHand INTEGER,
            Available INTEGER,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ItemId) REFERENCES Item(ItemId)
        );
        """)

    def insert_new_prod_data(
        self,
        prod_barcode='No barcode',
        prod_name='No name',
        prod_exp_dt='9999-99-99',
        prod_type='No type',
        prod_brand='No brand',
        prod_sales_group='No sales group',
        prod_supplier='No supplier',
        prod_cost=0,
        prod_sell_price=0,
        prod_effective_dt=str(date.today()),
        prod_promo_name='No promo',
        prod_promo_type='',
        prod_promo_percent=0,
        prod_promo_value=0,
        prod_promo_sell_price=0,
        prod_promo_start_dt=str(date.today()),
        prod_promo_end_dt=str(date.today()),
        prod_tracking=False,
        stock_available=0,
        stock_on_hand=0
    ):
        self.insert_new_item_type_data(prod_type)
        self.insert_new_brand_data(prod_brand)
        self.insert_new_sales_group_data(prod_sales_group)
        self.insert_new_supplier_data(prod_supplier)
        
        item_type_id = self.select_item_type_id(prod_type)
        brand_id = self.select_brand_id(prod_brand)
        sales_group_id = self.select_sales_group_id(prod_sales_group)
        supplier_id = self.select_supplier_id(prod_supplier)
        
        self.insert_new_item_data(
            prod_barcode, 
            prod_name, 
            prod_exp_dt, 
            item_type_id, 
            brand_id, 
            sales_group_id, 
            supplier_id
        )
        
        prod_item_id = self.select_item_id(
            prod_barcode, 
            prod_name, 
            prod_exp_dt, 
            item_type_id, 
            brand_id, 
            sales_group_id, 
            supplier_id
        )

        if prod_promo_name == 'No promo':
            self.insert_new_item_price_data_without_promo(
                prod_cost,
                prod_sell_price,
                prod_effective_dt,
                prod_item_id
            )

        else:
            self.insert_new_item_price_data_with_promo(
                prod_cost,
                prod_sell_price,
                prod_promo_name,
                prod_promo_type,
                prod_promo_percent,
                prod_promo_value,
                prod_promo_sell_price,
                prod_promo_start_dt,
                prod_promo_end_dt,
                prod_item_id
            )

        prod_stock_id = self.cursor.execute(f"""
            SELECT StockId FROM Stock
            WHERE ItemId = {prod_item_id}
        """)
        self.conn.commit()

        if prod_stock_id == None and prod_tracking == True:
            self.insert_new_stock_data(prod_item_id, stock_available, stock_on_hand)
        
        self.conn.commit()
        pass
    
    def insert_new_item_data(self, prod_barcode='', prod_name='', prod_exp_dt=str(date.today()), item_type_id=0, brand_id=0, sales_group_id=0, supplier_id=0):
        self.cursor.execute(f"""
        INSERT INTO Item (Barcode, Name, ExpireDt, ItemTypeId, BrandId, SalesGroupId, SupplierId)
        SELECT 
            "{prod_barcode}", 
            "{prod_name}", 
            "{prod_exp_dt}", 
            {item_type_id}, 
            {brand_id}, 
            {sales_group_id}, 
            {supplier_id}
        WHERE NOT EXISTS(
            SELECT 1 FROM Item
                INNER JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                INNER JOIN Brand ON Item.BrandId = Brand.BrandId
                INNER JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                INNER JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
            WHERE
                Item.Barcode = "{prod_barcode}" AND
                Item.Name = "{prod_name}" AND
                Item.ExpireDt = "{prod_exp_dt}" AND
                Item.ItemTypeId = {item_type_id} AND
                Item.BrandId = {brand_id} AND
                Item.SupplierId = {sales_group_id} AND
                Item.SalesGroupId = {supplier_id}
            )
        """)
    
    def insert_new_item_price_data_with_promo(
        self, 
        prod_cost=0, 
        prod_sell_price=0, 
        prod_promo_name='', 
        prod_promo_type='', 
        prod_promo_percent='', 
        prod_promo_value='', 
        prod_promo_sell_price='', 
        prod_promo_start_dt=str(date.today()), 
        prod_promo_end_dt=str(date.today()), 
        prod_item_id=0
    ):
        try:
            prod_promo_id = self.select_promo_id(prod_promo_name, prod_promo_type, prod_promo_percent)

            self.cursor.execute(f"""
                INSERT INTO ItemPrice (ItemId, Cost, SellPrice, PromoId, DiscountValue, EffectiveDt)
                SELECT 
                    {prod_item_id}, 
                    {prod_cost}, 
                    {prod_sell_price}, 
                    0, 
                    0, 
                    DATE("{prod_promo_end_dt}", '+1 day')
                WHERE NOT EXISTS (
                    SELECT 1 FROM ItemPrice
                    WHERE 
                        ItemId = {prod_item_id} AND
                        Cost = {prod_cost} AND
                        SellPrice = {prod_sell_price} AND
                        PromoId = 0 AND
                        DiscountValue = 0 AND
                        EffectiveDt = DATE("{prod_promo_end_dt}", '+1 day')
                    )
                """)

            self.cursor.execute(f"""
                INSERT INTO ItemPrice (ItemId, Cost, SellPrice, PromoId, DiscountValue, EffectiveDt)
                SELECT 
                    {prod_item_id}, 
                    {prod_cost}, 
                    {prod_promo_sell_price}, 
                    {prod_promo_id}, 
                    {prod_promo_value}, 
                    "{prod_promo_start_dt}"
                WHERE NOT EXISTS (
                    SELECT 1 FROM ItemPrice
                    WHERE 
                        ItemId = {prod_item_id} AND
                        Cost = {prod_cost} AND
                        SellPrice = {prod_promo_sell_price} AND
                        PromoId = {prod_promo_id} AND
                        DiscountValue = {prod_promo_value} AND
                        EffectiveDt = "{prod_promo_start_dt}"
                    )
                """)
        except Exception as e:
            print(e)
            pass
    def insert_new_item_price_data_without_promo(self, prod_cost, prod_sell_price, prod_effective_dt, prod_item_id):
        self.cursor.execute(f"""
            INSERT INTO ItemPrice (ItemId, Cost, SellPrice, DiscountValue, EffectiveDt)
            SELECT 
                {prod_item_id}, 
                {prod_cost}, 
                {prod_sell_price}, 
                0, 
                "{prod_effective_dt}"
            WHERE NOT EXISTS (
                SELECT 1 FROM ItemPrice
                WHERE 
                    ItemId = {prod_item_id} AND
                    Cost = {prod_cost} AND
                    SellPrice = {prod_sell_price} AND
                    DiscountValue = 0 AND -- discount value is set to 0 if prod_promo_name is 'No promo'
                    EffectiveDt = "{prod_effective_dt}"
                )
            """)
    def insert_new_item_type_data(self, prod_type):
        self.cursor.execute(f"""
        INSERT INTO ItemType (Name)
        SELECT "{prod_type}" WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = "{prod_type}")
        """)
    def insert_new_brand_data(self, prod_brand):
        self.cursor.execute(f"""
        INSERT INTO Brand (Name)
        SELECT "{prod_brand}" WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = "{prod_brand}")
        """)
    def insert_new_sales_group_data(self, prod_sales_group):
        self.cursor.execute(f"""
        INSERT INTO SalesGroup (Name)
        SELECT "{prod_sales_group}" WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = "{prod_sales_group}")
        """)
    def insert_new_supplier_data(self, prod_supplier):
        self.cursor.execute(f"""
        INSERT INTO Supplier (Name)
        SELECT "{prod_supplier}" WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = "{prod_supplier}")
        """)
    def insert_new_stock_data(self, prod_item_id, stock_available=0, stock_on_hand=0):
        print(prod_item_id)
        print(type(prod_item_id))
        self.cursor.execute(f"""
            INSERT INTO Stock (ItemId, Available, OnHand)
            SELECT 
                {prod_item_id}, 
                {stock_available}, 
                {stock_on_hand}
            WHERE NOT EXISTS(
                SELECT 1 FROM Stock
                WHERE
                    ItemId = {prod_item_id} AND
                    Available = {stock_available} AND
                    OnHand = {stock_on_hand}
                )
            """)
        
        self.conn.commit()
      
    def update_selected_prod_data(
        self,
        prod_barcode='',
        prod_name='',
        prod_exp_dt='',
        prod_type='',
        prod_brand='',
        prod_sales_group='',
        prod_supplier='',
        prod_cost=0,
        prod_sell_price=0,
        prod_effective_dt=str(date.today()),
        prod_promo_name='',
        prod_promo_type='',
        prod_promo_percent=0,
        prod_promo_value=0,
        prod_promo_sell_price=0,
        prod_promo_start_dt=str(date.today()),
        prod_promo_end_dt=str(date.today()),
        prod_tracking=False,

        prod_item_id = 0,
        prod_price_id = 0,
        prod_promo_id = 0,
        prod_stock_id = 0
    ):
        print(end='')
        if prod_promo_id == 0 and prod_promo_name == 'No promo':
            print('INSERT A')
            self.update_selected_item_data(prod_barcode, prod_name, prod_exp_dt, prod_item_id)
            self.update_selected_item_price_data(prod_cost, prod_sell_price, prod_effective_dt, prod_price_id)
        elif prod_promo_id == 0 and prod_promo_name != 'No promo':
            print('INSERT B')
            self.insert_new_prod_data(
                prod_barcode,
                prod_name,
                prod_exp_dt,
                prod_type,
                prod_brand,
                prod_sales_group,
                prod_supplier,
                prod_cost,
                prod_sell_price,
                prod_effective_dt,
                prod_promo_name,
                prod_promo_type,
                prod_promo_percent,
                prod_promo_value,
                prod_promo_sell_price,
                prod_promo_start_dt,
                prod_promo_end_dt,
                prod_tracking=prod_tracking
            )
        elif prod_promo_id != 0 and prod_promo_name != 'No promo':
            print('INSERT C')
            self.update_selected_item_data(prod_barcode, prod_name, prod_exp_dt, prod_item_id)

        if prod_stock_id == None and prod_tracking == True:
            print('a here!!!')
            self.insert_new_stock_data(prod_item_id)
            pass
        elif prod_stock_id != None and prod_tracking == False:
            print('b here!!!')
            self.delete_selected_stock_data(prod_item_id, prod_stock_id)
            pass
        elif prod_stock_id != None and prod_tracking == True:
            print('c here!!!')
            self.update_selected_stock_data(prod_item_id)
            pass

        pass
    def update_selected_item_data(self, prod_barcode, prod_name, prod_exp_dt, prod_item_id):
        self.cursor.execute(f"""
            UPDATE Item
            SET Barcode = "{prod_barcode}",
                Name = "{prod_name}",
                ExpireDt = "{prod_exp_dt}"
            WHERE ItemId = "{prod_item_id}"
            """)
        self.conn.commit()
    def update_selected_item_price_data(self, prod_cost, prod_sell_price, prod_effective_dt, prod_price_id):
        self.cursor.execute(f"""
            UPDATE ItemPrice
            SET 
                Cost = {prod_cost}, 
                SellPrice = {prod_sell_price}, 
                EffectiveDt = "{prod_effective_dt}"
            WHERE ItemPriceId = {prod_price_id}
            """)
        self.conn.commit()
    
    def update_selected_stock_data(self, stock_available=0, stock_on_hand=0, stock_id=0):
        self.cursor.execute(f"""
        UPDATE Stock
        SET Available = {stock_available}, OnHand = {stock_on_hand}
        WHERE StockId = {stock_id}
        """)
        self.conn.commit()
        pass
    
    def delete_selected_item_price_data(self, prod_price_id):
        self.cursor.execute(f"""
            DELETE FROM ItemPrice
            WHERE ItemPriceId = {prod_price_id} AND EffectiveDt > CURRENT_DATE
            """)
        
        self.conn.commit()
        pass
    def delete_selected_inventory(self, prod_stock_id):
        self.cursor.execute(f"""
        DELETE FROM Stock
        WHERE StockId = {prod_stock_id}
        """)
        self.conn.commit()
    def delete_selected_stock_data(self, prod_item_id, stock_id):
        print('HEEEEEEEREEE!!!!!')
        print(prod_item_id)
        print(stock_id)
        self.cursor.execute(f"""
        DELETE FROM Stock
        WHERE 
            ItemId = {prod_item_id} AND 
            StockId = {stock_id}
        """)
        self.conn.commit()

    def select_prod_data(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.cursor.execute(f"""
            SELECT
                Item.Barcode AS Barcode,
                Item.Name AS Item,
                Item.ExpireDt AS ExpireDt,
                            
                ItemType.Name AS ItemType, 
                Brand.Name AS Brand, 
                SalesGroup.Name AS SalesGroup, 
                Supplier.Name AS Supplier,
                            
                COALESCE(NULLIF(ItemPrice.Cost, ''), 0) AS Cost,
                COALESCE(NULLIF(ItemPrice.SellPrice, ''), 0) AS SellPrice,
                COALESCE(NULLIF(ItemPrice.EffectiveDt, ''), '[no data]') AS EffectiveDt,
                CASE WHEN Promo.Name IS NOT NULL THEN Promo.Name ELSE 'No promo' END AS Promo,
                COALESCE(NULLIF(ItemPrice.DiscountValue, ''), 0) AS DiscountValue,

                CASE WHEN Stock.StockId <> 0 THEN 'Enabled' ELSE 'Disabled' END AS InventoryTracking,
                            
                ItemPrice.UpdateTs, -- 13                       
                ItemPrice.ItemId, -- 14
                ItemPrice.ItemPriceId, -- 15
                ItemPrice.PromoId, -- 16
                Stock.StockId -- 17
                            
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
                Item.Barcode LIKE '%{text_filter}%' OR
                Item.Name LIKE '%{text_filter}%' OR
                ItemType.Name LIKE '%{text_filter}%' OR 
                Brand.Name LIKE '%{text_filter}%' OR 
                SalesGroup.Name LIKE '%{text_filter}%' OR 
                Supplier.Name LIKE '%{text_filter}%' OR
                InventoryTracking LIKE '%{text_filter}%'
            ORDER BY Item.ItemId DESC, ItemPrice.EffectiveDt DESC, Item.UpdateTs DESC
            LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
            """)

        product = self.cursor.fetchall()

        return product
        pass
    def select_stock_data(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.cursor.execute(f"""
            SELECT
                COALESCE(NULLIF(Item.Name, ''), '[no data]') AS Item,
                COALESCE(NULLIF(Stock.Available, ''), 0) AS Available,
                COALESCE(NULLIF(Stock.OnHand, ''), 0) AS OnHand,
                Stock.UpdateTs,
                Stock.ItemId, -- 4
                Stock.StockId -- 5
            FROM Stock
                LEFT JOIN Item ON Stock.ItemId = Item.ItemId
            WHERE
                Item LIKE '%{text_filter}%' OR
                Available LIKE '%{text_filter}%' OR
                OnHand LIKE '%{text_filter}%'
            ORDER BY Item, Stock.UpdateTs DESC
            LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
            """)
        
        stock = self.cursor.fetchall()
        
        return stock
        pass
    def select_item_type_name(self):
        self.cursor.execute(f"""
        SELECT DISTINCT Name FROM ItemType
        ORDER BY UpdateTs DESC
        """)
            
        item_type = self.cursor.fetchall()

        return item_type
        pass
    def select_brand_name(self):
        self.cursor.execute(f"""
        SELECT DISTINCT Name FROM Brand
        ORDER BY UpdateTs DESC
        """)
            
        brand = self.cursor.fetchall()

        return brand 
        pass
    def select_supplier_name(self):
        self.cursor.execute(f"""
        SELECT DISTINCT Name FROM Supplier
        ORDER BY UpdateTs DESC
        """)
            
        supplier = self.cursor.fetchall()

        return supplier 
        pass
    def select_promo_name(self):
        self.cursor.execute(f"""
        SELECT DISTINCT Name FROM Promo
        ORDER BY UpdateTs DESC
        """)
            
        promo = self.cursor.fetchall()

        return promo 
        pass
    def select_promo_type(self, prod_promo_name):
        self.cursor.execute(f"""
        SELECT DISTINCT PromoType FROM Promo
        WHERE Name = ?
        ORDER BY PromoId DESC, UpdateTs DESC                
        """, (prod_promo_name,))
        
        promo_type = self.cursor.fetchone()[0]
        
        return promo_type
        pass
    def select_promo_percent(self, prod_promo_name):
        self.cursor.execute(f"""
        SELECT DISTINCT DiscountPercent FROM Promo
        WHERE Name = ?
        ORDER BY PromoId DESC, UpdateTs DESC                
        """, (prod_promo_name,))
        
        promo_percent = self.cursor.fetchone()[0]
        
        return promo_percent

    def select_item_id(self, prod_barcode, prod_name, prod_exp_dt, item_type_id, brand_id, sales_group_id, supplier_id):
        prod_item_id = self.cursor.execute(f"""
        SELECT ItemId FROM Item
        WHERE 
            Barcode = "{prod_barcode}" AND 
            Name = "{prod_name}" AND 
            ExpireDt = "{prod_exp_dt}" AND 
            ItemTypeId = {item_type_id} AND 
            BrandId = {brand_id} AND 
            SalesGroupId = {sales_group_id} AND 
            SupplierId = {supplier_id}
        """)

        prod_item_id = self.cursor.fetchone()[0]

        return prod_item_id
    def select_item_type_id(self, prod_type):
        item_type_id = self.cursor.execute(f"""
        SELECT ItemTypeId FROM ItemType
        WHERE Name = "{prod_type}"
        """)

        item_type_id = self.cursor.fetchone()[0]

        return item_type_id
    def select_brand_id(self, prod_brand):
        brand_id = self.cursor.execute(f"""
        SELECT BrandId FROM Brand
        WHERE Name = "{prod_brand}"
        """)

        brand_id = self.cursor.fetchone()[0]

        return brand_id
    def select_sales_group_id(self, prod_sales_group):
        sales_group_id = self.cursor.execute(f"""
        SELECT SalesGroupId FROM SalesGroup
        WHERE Name = "{prod_sales_group}"
        """)
        
        sales_group_id = self.cursor.fetchone()[0]

        return sales_group_id
    def select_supplier_id(self, prod_supplier):
        supplier_id = self.cursor.execute(f"""
        SELECT SupplierId FROM Supplier
        WHERE Name = "{prod_supplier}"
        """)

        supplier_id = self.cursor.fetchone()[0]

        return supplier_id
    def select_promo_id(self, prod_promo_name, prod_promo_type, prod_promo_percent):
        try:
            prod_promo_id = self.cursor.execute(f"""
                SELECT PromoId FROM Promo
                WHERE
                    Name = "{prod_promo_name}" AND 
                    PromoType = "{prod_promo_type}" AND 
                    DiscountPercent = {prod_promo_percent}
                """)
            prod_promo_id = self.cursor.fetchone()[0]
        except Exception as e:
            prod_promo_id = 0
            
        return prod_promo_id

    def select_item_price_count_data(self):
        self.cursor.execute(f"""
        SELECT COUNT(*) FROM ItemPrice
        """)
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def select_item_price_count_total_pages(self, page_size=30):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM Item
            """)

        total_prod = self.cursor.fetchone()[0]
        total_pages = (total_prod - 1) // page_size + 1

        return total_pages
        pass
    def select_stock_count_total_pages(self, page_size=30):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM Stock
            """)

        total_prod = self.cursor.fetchone()[0]
        total_pages = (total_prod - 1) // page_size + 1

        return total_pages
    