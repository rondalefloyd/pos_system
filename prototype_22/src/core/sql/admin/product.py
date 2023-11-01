import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(r'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22')

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyProductSchema:
    def __init__(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.sales_conn = sqlite3.connect(database=self.sales_file)
        self.sales_cursor = self.sales_conn.cursor()

        self.create_product_table()

    def create_product_table(self):
        # item type
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ItemType (
                ItemTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                PromoId INTEGER DEFAULT 0,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)
            )
        """)
        self.sales_conn.commit()

        # brand
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Brand (
                BrandId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                PromoId INTEGER DEFAULT 0,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)
            );
            """)
        self.sales_conn.commit()

        # sales group
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS SalesGroup (
                SalesGroupId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.sales_conn.commit()

        # supplier
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Supplier (
                SupplierId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.sales_conn.commit()

        # item
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Item (
                ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
                Barcode TEXT,
                Name TEXT,
                ExpireDt DATETIME,
                ItemTypeId INTEGER DEFAULT 0,
                BrandId INTEGER DEFAULT 0,
                SalesGroupId INTEGER DEFAULT 0,
                SupplierId INTEGER DEFAULT 0,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (ItemTypeId) REFERENCES ItemType(ItemTypeId),
                FOREIGN KEY (BrandId) REFERENCES Brand(BrandId),
                FOREIGN KEY (SalesGroupId) REFERENCES SalesGroup(SalesGroupId),
                FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId)
            )
        """)
        self.sales_conn.commit()

        # item price
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ItemPrice (
                ItemPriceId INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemId INTEGER DEFAULT 0,
                EffectiveDt DATETIME,
                Cost DECIMAL(15, 2),
                SellPrice DECIMAL(15, 2),
                PromoId INTEGER DEFAULT 0,
                DiscountValue DECIMAL(15, 2),
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (ItemId) REFERENCES Item(ItemId),
                FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)
            )
        """)
        self.sales_conn.commit()

        # promo
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Promo (
                PromoId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                PromoType TEXT,
                DiscountPercent DECIMAL,
                Description TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # stock
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Stock (
                StockId INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemId INTEGER DEFAULT 0,
                OnHand INTEGER,
                Available INTEGER,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ItemId) REFERENCES Item(ItemId)
            )
        """)


        self.sales_conn.commit()

    def insert_product_data(
            self,
            product_barcode='',
            product_name='',
            product_expire_dt='9999-99-99',

            product_type='',
            product_brand='',
            product_sales_group='Retail',
            product_supplier='',

            product_cost='',
            product_price='',
            product_effective_dt=date.today(),
            product_promo_name='No promo',
            product_promo_type='',
            product_disc_value=0,
            product_promo_percent=0,
            product_new_price=0,
            product_start_dt=date.today(),
            product_end_dt=date.today(),

            product_stock_tracking=False,

            product_stock_available=0,    
            product_stock_onhand=0,
    ):
        self.sales_cursor.execute(f"""
            INSERT INTO ItemType (Name)
            SELECT "{product_type}" WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = "{product_type}")
        """)
        self.sales_cursor.execute(f"""
            INSERT INTO Brand (Name)
            SELECT "{product_brand}" WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = "{product_brand}")
        """)
        self.sales_cursor.execute(f"""
            INSERT INTO SalesGroup (Name)
            SELECT "{product_sales_group}" WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = "{product_sales_group}")
        """)
        self.sales_cursor.execute(f"""
            INSERT INTO Supplier (Name)
            SELECT "{product_supplier}" WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = "{product_supplier}")
        """)


        product_type_id = self.sales_cursor.execute(f"""
            SELECT ItemTypeId FROM ItemType
            WHERE Name = "{product_type}"
        """)
        product_type_id = self.sales_cursor.fetchone()[0]
        
        product_brand_id = self.sales_cursor.execute(f"""
            SELECT BrandId FROM Brand
            WHERE Name = "{product_brand}"
        """)
        product_brand_id = self.sales_cursor.fetchone()[0]
        
        product_sales_group_id = self.sales_cursor.execute(f"""
            SELECT SalesGroupId FROM SalesGroup
            WHERE Name = "{product_sales_group}"
        """)
        product_sales_group_id = self.sales_cursor.fetchone()[0]
        
        product_supplier_id = self.sales_cursor.execute(f"""
            SELECT SupplierId FROM Supplier
            WHERE Name = "{product_supplier}"
        """)
        product_supplier_id = self.sales_cursor.fetchone()[0]

        self.sales_cursor.execute(f"""
            INSERT INTO Item (Barcode, Name, ExpireDt, ItemTypeId, BrandId, SalesGroupId, SupplierId)
            SELECT 
                "{product_barcode}", 
                "{product_name}", 
                "{product_expire_dt}", 
                "{product_type_id}", 
                "{product_brand_id}", 
                "{product_sales_group_id}", 
                "{product_supplier_id}"
            WHERE NOT EXISTS (
                SELECT 1 FROM Item 
                WHERE 
                    Barcode = "{product_barcode}" AND
                    Name = "{product_name}" AND
                    ExpireDt = "{product_expire_dt}" AND
                    ItemTypeId = "{product_type_id}" AND
                    BrandId = "{product_brand_id}" AND
                    SalesGroupId = "{product_sales_group_id}" AND
                    SupplierId = "{product_supplier_id}"
            )
        """)

        product_id = self.sales_cursor.execute(f"""
            SELECT ItemId FROM Item
            WHERE Name = "{product_name}"
        """)
        product_id = self.sales_cursor.fetchone()[0]

        if product_promo_name == 'No promo':
            self.sales_cursor.execute(f"""
                INSERT INTO ItemPrice (ItemId, EffectiveDt, Cost, SellPrice, PromoId, DiscountValue)
                SELECT
                    {product_id},
                    "{product_effective_dt}",
                    {product_cost},
                    {product_price},    
                    0,
                    0
                WHERE NOT EXISTS (
                    SELECT 1 FROM ItemPrice
                    WHERE
                        ItemId = {product_id} AND 
                        EffectiveDt = "{product_effective_dt}" AND 
                        Cost = {product_cost} AND 
                        SellPrice = {product_price} AND 
                        PromoId = 0 AND
                        DiscountValue = 0
                )
            """)
        if product_promo_name != 'No promo':
            product_promo_id = self.sales_cursor.execute(f"""
                SELECT PromoId FROM Promo
                WHERE Name = "{product_promo_name}"
            """)
            product_promo_id = self.sales_cursor.fetchone()[0]

            # NOTE: inserts the item with start_dt
            self.sales_cursor.execute(f"""
                INSERT INTO ItemPrice (ItemId, EffectiveDt, Cost, SellPrice, PromoId, DiscountValue)
                SELECT
                    {product_id},
                    "{product_start_dt}",
                    {product_cost},
                    {product_new_price},    
                    {product_promo_id},
                    {product_disc_value}
                WHERE NOT EXISTS (
                    SELECT 1 FROM ItemPrice
                    WHERE
                        ItemId = {product_id} AND 
                        EffectiveDt = "{product_start_dt}" AND 
                        Cost = {product_cost} AND 
                        SellPrice = {product_new_price} AND 
                        PromoId = {product_promo_id} AND
                        DiscountValue = {product_disc_value}
                )
            """)

            # NOTE: inserts the item with end_dt
            self.sales_cursor.execute(f"""
                INSERT INTO ItemPrice (ItemId, EffectiveDt, Cost, SellPrice, PromoId, DiscountValue)
                SELECT
                    {product_id},
                    DATE("{product_end_dt}", '+1 day'),
                    {product_cost},
                    {product_price},    
                    0,
                    0
                WHERE NOT EXISTS (
                    SELECT 1 FROM ItemPrice
                    WHERE
                        ItemId = {product_id} AND 
                        EffectiveDt = DATE("{product_end_dt}", '+1 day') AND 
                        Cost = {product_cost} AND 
                        SellPrice = {product_price} AND 
                        PromoId = 0 AND
                        DiscountValue = 0
                )
            """)
            pass
        
        if product_stock_tracking is True:
            self.sales_cursor.execute(f"""
                INSERT INTO Stock (ItemId, OnHand, Available)
                SELECT {product_id}, {product_stock_available}, {product_stock_onhand}
                WHERE NOT EXISTS (
                    SELECT 1 FROM Stock
                    WHERE ItemId = {product_id} AND OnHand = {product_stock_available} AND Available = {product_stock_onhand}
                )
            """)

        self.sales_conn.commit()

    def select_product_data_as_display(self, text='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
            WITH RankedProduct AS (
                SELECT DISTINCT
                    Item.Barcode, 
                    Item.Name, 
                    Item.ExpireDt, 
                                            
                    ItemType.Name AS ItemTypeName, 
                    Brand.Name AS BrandName, 
                    SalesGroup.Name AS SalesGroupName, 
                    Supplier.Name AS SupplierName, 
                                            
                    ItemPrice.Cost, 
                    ItemPrice.SellPrice, 
                    ItemPrice.EffectiveDt, 
                    Promo.Name AS PromoName, 
                    ItemPrice.DiscountValue, 
                                    
                    CASE WHEN Stock.StockId > 0 THEN 'Enabled' ELSE 'Disabled' END AS StockStatus,
                            
                    ItemPrice.UpdateTs,
                    
                    ROW_NUMBER() OVER (PARTITION BY Item.Name ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC) AS RowNumber
                FROM ItemPrice
                LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
                WHERE
                    Item.Barcode LIKE "%{text}%" OR
                    Item.Name LIKE "%{text}%" OR
                    Item.ExpireDt LIKE "%{text}%" OR
                    ItemType.Name LIKE "%{text}%" OR
                    Brand.Name LIKE "%{text}%" OR
                    SalesGroup.Name LIKE "%{text}%" OR
                    Supplier.Name LIKE "%{text}%" OR
                    ItemPrice.UpdateTs LIKE "%{text}%"
                ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC
            )
            SELECT * FROM RankedProduct 
            WHERE RowNumber <= 2 
            LIMIT {page_size} OFFSET {offset}
        """)

        product_data = self.sales_cursor.fetchall()

        return product_data
        pass
    
    def select_product_data(self, product_barcode='', product_name=''):
        self.sales_cursor.execute(f"""
            SELECT
                Item.Barcode,
                Item.Name,
                Item.ExpireDt,
                                  
                ItemType.Name,
                Brand.Name,
                SalesGroup.Name,
                Supplier.Name,
                                  
                ItemPrice.Cost,
                ItemPrice.SellPrice,
                ItemPrice.EffectiveDt,

                COALESCE(NULLIF(Item.ItemId, ''), 0),
                COALESCE(NULLIF(ItemPrice.ItemPriceId, ''), 0),
                COALESCE(NULLIF(Stock.StockId, ''), 0),
                COALESCE(NULLIF(Promo.PromoId, ''), 0)
            FROM ItemPrice
                LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
            WHERE
                Item.Barcode = "{product_barcode}" AND
                Item.Name = "{product_name}"
            ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC
            LIMIT 1
        """)

        product_data = self.sales_cursor.fetchall()

        return product_data
    def select_product_data_total_page_count(self, text='', page_size=30):
        self.sales_cursor.execute(f"""
            WITH RankedProduct AS (
                SELECT 
                    Item.Barcode, 
                    Item.Name, 
                    Item.ExpireDt, 
                                            
                    ItemType.Name AS ItemTypeName, 
                    Brand.Name AS BrandName, 
                    SalesGroup.Name AS SalesGroupName, 
                    Supplier.Name AS SupplierName, 
                                            
                    ItemPrice.Cost, 
                    ItemPrice.SellPrice, 
                    ItemPrice.EffectiveDt, 
                    Promo.Name AS PromoName, 
                    ItemPrice.DiscountValue, 
                                    
                    CASE WHEN Stock.StockId > 0 THEN 'Enabled' ELSE 'Disabled' END AS StockStatus,
                            
                    ItemPrice.UpdateTs,
                    
                    ROW_NUMBER() OVER (PARTITION BY Item.Name ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC) AS RowNumber
                FROM ItemPrice
                LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
                WHERE
                    Item.Barcode LIKE "%{text}%" OR
                    Item.Name LIKE "%{text}%" OR
                    Item.ExpireDt LIKE "%{text}%" OR
                    ItemType.Name LIKE "%{text}%" OR
                    Brand.Name LIKE "%{text}%" OR
                    SalesGroup.Name LIKE "%{text}%" OR
                    Supplier.Name LIKE "%{text}%" OR
                    ItemPrice.UpdateTs LIKE "%{text}%"
            )
            SELECT COUNT(*) FROM RankedProduct 
            WHERE RowNumber <= 2 
        """)

        total_product_data_count = self.sales_cursor.fetchone()[0]
        total_page_count = (total_product_data_count - 1) // page_size + 1

        return total_page_count
        pass
    
    def select_stock_data_as_display(self, text='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
            SELECT 
                Item.Barcode, 
                Item.Name, 
                Stock.Available,
                Stock.OnHand,
                Stock.UpdateTs,
                                  
                Stock.StockId,
                Stock.ItemId
            FROM Stock
            LEFT JOIN Item ON Stock.ItemId = Item.ItemId
            LEFT JOIN ItemPrice ON Item.ItemId = ItemPrice.ItemId
            WHERE
                Item.Barcode LIKE "%{text}%" OR
                Item.Name LIKE "%{text}%" OR
                Stock.Available LIKE "%{text}%" OR
                Stock.OnHand LIKE "%{text}%" OR
                Stock.UpdateTs LIKE "%{text}%"
            ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC
            LIMIT {page_size}
            OFFSET {offset}
        """)

        stock_data = self.sales_cursor.fetchall()

        return stock_data
        pass
    def select_stock_data(self, stock_id=0, stock_product_id=0):
        self.sales_cursor.execute(f"""
            SELECT
                Item.Barcode,
                Item.Name,
                Stock.Available,
                Stock.OnHand,
                                  
                Stock.StockId,
                Stock.ItemId
            FROM Stock
                LEFT JOIN Item ON Stock.ItemId = Item.ItemId
            WHERE Stock.StockId = {stock_id} AND Stock.ItemId = {stock_product_id}
            ORDER BY Stock.StockId DESC, Stock.UpdateTs DESC
            LIMIT 1
        """)

        stock_data = self.sales_cursor.fetchall()

        return stock_data
    def select_stock_data_total_page_count(self, text='', page_size=30):
        self.sales_cursor.execute(f"""
            SELECT COUNT(*) FROM Stock
            LEFT JOIN Item ON Stock.ItemId = Item.ItemId
            LEFT JOIN ItemPrice ON Item.ItemId = ItemPrice.ItemId
            WHERE
                Item.Barcode LIKE "%{text}%" OR
                Item.Name LIKE "%{text}%"
        """)

        total_stock_data_count = self.sales_cursor.fetchone()[0]
        total_page_count = (total_stock_data_count - 1) // page_size + 1

        return total_page_count
        pass
    
    def select_product_type_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT Name FROM ItemType
            ORDER BY ItemTypeId DESC, UpdateTs DESC
        """)

        product_type = self.sales_cursor.fetchall()

        return product_type
        pass
    def select_product_brand_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT Name FROM Brand
            ORDER BY BrandId DESC, UpdateTs DESC
        """)

        product_brand = self.sales_cursor.fetchall()

        return product_brand
        pass
    def select_product_supplier_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT Name FROM Brand
            ORDER BY BrandId DESC, UpdateTs DESC
        """)

        product_supplier = self.sales_cursor.fetchall()

        return product_supplier
        pass
    def select_product_promo_name_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT Name FROM Promo
            ORDER BY PromoId DESC, UpdateTs DESC
        """)

        product_promo_name = self.sales_cursor.fetchall()

        return product_promo_name
        pass

    def select_promo_type(self, promo_name):
        try:
            promo_type = self.sales_cursor.execute(f"""
                SELECT PromoType FROM Promo
                WHERE
                    Name = "{promo_name}"
            """)

            promo_type = self.sales_cursor.fetchone()[0]
        except Exception as e:
            promo_type = ''

        return promo_type
        pass
    def select_promo_percent(self, promo_name):
        try:
            promo_percent = self.sales_cursor.execute(f"""
                SELECT DiscountPercent FROM Promo
                WHERE
                    Name = "{promo_name}"
            """)

            promo_percent = self.sales_cursor.fetchone()[0]
        except Exception as e:
            promo_percent = 0

        return promo_percent

    def select_product_id(self, product_barcode, product_name):
        product_id = self.sales_cursor.execute(f"""
            SELECT ItemId FROM Item
            WHERE
                Barcode = "{product_barcode}" AND
                Name = "{product_name}"
        """)

        product_id = self.sales_cursor.fetchone()[0]

        return product_id

    def update_product_data(
            self, 
            product_barcode='',
            product_name='',
            product_expire_dt='9999-99-99',

            product_type='',
            product_brand='',
            product_sales_group='Retail',
            product_supplier='',

            product_cost='',
            product_price='',
            product_effective_dt=date.today(),
            product_promo_name='No promo',
            product_promo_type='',
            product_disc_value=0,
            product_promo_percent=0,
            product_new_price=0,
            product_start_dt=date.today(),
            product_end_dt=date.today(),

            product_stock_tracking=False,

            product_id=0,
            product_price_id=0,
            product_stock_id=0,
            product_promo_id=0,
    ):
        if product_promo_id <= 0 and product_promo_name == 'No promo':
            self.sales_cursor.execute(f"""
                UPDATE Item
                SET
                    Barcode = "{product_barcode}",
                    Name = "{product_name}",
                    ExpireDt = "{product_expire_dt}"
                WHERE ItemId = {product_id}
            """)

            self.sales_cursor.execute(f"""
                UPDATE ItemPrice
                SET
                    Cost = {product_cost},
                    SellPrice = {product_price},
                    EffectiveDt = "{product_effective_dt}"
                WHERE ItemPriceId = {product_price_id}
            """)
            pass  
        elif product_promo_id <= 0 and product_promo_name != 'No promo':
            self.insert_product_data(
                product_barcode,
                product_name,
                product_expire_dt,
                
                product_type,
                product_brand,
                product_sales_group,
                product_supplier,
                
                product_cost,
                product_price,
                product_effective_dt,
                product_promo_name,
                product_promo_type,
                product_disc_value,
                product_promo_percent,
                product_new_price,
                product_start_dt,
                product_end_dt,
            )
            pass
        elif product_promo_id > 0 and product_promo_name == 'No promo':
            self.sales_cursor.execute(f"""
                UPDATE Item
                SET
                    Barcode = "{product_barcode}",
                    Name = "{product_name}",
                    ExpireDt = "{product_expire_dt}"
                WHERE ItemId = {product_id}
            """)

            self.sales_cursor.execute(f"""
                UPDATE ItemPrice
                SET
                    Cost = {product_cost},
                    SellPrice = {product_price},
                    EffectiveDt = "{product_effective_dt}"
                WHERE ItemPriceId = {product_price_id}
            """)
            pass  

        if product_stock_id <= 0 and product_stock_tracking is True:
            self.sales_cursor.execute(f"""
                INSERT INTO Stock (ItemId, OnHand, Available)
                SELECT {product_id}, 0, 0
                WHERE NOT EXISTS (
                    SELECT 1 FROM Stock
                    WHERE ItemId = {product_id} AND OnHand = 0 AND Available = 0
                )
            """)
        elif product_stock_id > 0 and product_stock_tracking is False:
            self.sales_cursor.execute(f"""
                DELETE FROM Stock
                WHERE StockId = {product_stock_id}
            """)

        self.sales_conn.commit()
    def update_stock_data(self, stock_available, stock_onhand, stock_id, product_id):
        print('stock_id:', stock_id)
        print('product_id:', product_id)

        print('stock_available:', stock_available)
        print('stock_onhand:', stock_onhand)

        self.sales_cursor.execute(f"""
            UPDATE Stock
            SET
                Available = {stock_available},
                OnHand = {stock_onhand}
            WHERE StockId = {stock_id} OR ItemId = {product_id}
        """)

        self.sales_conn.commit()
        pass

    def delete_product_data(self, product_price_id=0, product_effective_dt=date.today()):
        self.sales_cursor.execute(f"""
            DELETE FROM ItemPrice
            -- WHERE ItemPriceId = {product_price_id} AND EffectiveDt > CURRENT_DATE
            WHERE ItemPriceId <= 0
        """)

        self.sales_conn.commit()
    def delete_stock_data(self, stock_id, stock_product_id):
        self.sales_cursor.execute(f"""
            DELETE FROM Stock
            WHERE StockId = {stock_id} AND ItemId = {stock_product_id}
        """)

        self.sales_conn.commit()


