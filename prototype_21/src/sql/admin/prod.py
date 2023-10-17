import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyProdSchema():
    def __init__(self):
        super().__init__()

        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.sales_file)
        self.cursor = self.conn.cursor()

        self.create_prod_table()

    def create_prod_table(self):
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

    def add_new_prod(
        # region -- params
        self='',
        prod_barcode='',
        prod_name='',
        prod_exp_dt='',
        prod_type='',
        prod_brand='',
        prod_sales_group='',
        prod_supplier='',
        prod_cost='',
        prod_sell_price='',
        prod_effective_dt='',
        prod_promo_name='',
        prod_promo_type='',
        prod_promo_percent='',
        prod_promo_value='',
        prod_promo_sell_price='',
        prod_promo_start_dt='',
        prod_promo_end_dt='',
        prod_tracking='',
        stock_available='',
        stock_on_hand=''
        # endregion -- params
    ):
        # region -- assign values if empty string
        prod_barcode = '[no data]' if prod_barcode == '' else prod_barcode
        prod_name = '[no data]' if prod_name == '' else prod_name
        prod_exp_dt = '9999-12-31' if prod_exp_dt == '' else prod_exp_dt

        prod_type = '[no data]' if prod_type == '' else prod_type
        prod_brand = '[no data]' if prod_brand == '' else prod_brand
        prod_sales_group = '[no data]' if prod_sales_group == '' else prod_sales_group
        prod_supplier = '[no data]' if prod_supplier == '' else prod_supplier

        prod_cost = 0 if prod_cost == '' else prod_cost
        prod_sell_price = 0 if prod_sell_price == '' else prod_sell_price
        prod_effective_dt = str(date.today()) if prod_effective_dt == '' else prod_effective_dt
        prod_promo_name = 'No promo' if prod_promo_name == '' else prod_promo_name
        prod_promo_type = '[no data]' if prod_promo_type == '' else prod_promo_type
        prod_promo_percent = 0 if prod_promo_percent == '' else prod_promo_percent
        prod_promo_value = 0 if prod_promo_value == '' else prod_promo_value
        prod_promo_sell_price = 0 if prod_promo_sell_price == '' else prod_promo_sell_price
        prod_promo_start_dt = str(date.today()) if prod_promo_start_dt == '' else prod_promo_start_dt
        prod_promo_end_dt = str(date.today()) if prod_promo_end_dt == '' else prod_promo_end_dt

        prod_tracking = False if prod_tracking == '' else prod_tracking
        stock_available = 0 if stock_available == '' else stock_available
        stock_on_hand = 0 if stock_on_hand == '' else stock_on_hand
         
        # endregion

        # region -- step a: insert item_type, brand, sales_group, and supplier into their respective tables
        self.cursor.execute('''
        INSERT INTO ItemType (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = ?)
        ''', (prod_type, prod_type))

        self.cursor.execute('''
        INSERT INTO Brand (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = ?)
        ''', (prod_brand, prod_brand))

        self.cursor.execute('''
        INSERT INTO SalesGroup (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = ?)
        ''', (prod_sales_group, prod_sales_group))

        self.cursor.execute('''
        INSERT INTO Supplier (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = ?)
        ''', (prod_supplier, prod_supplier))
        # endregion -- step a: insert item_type, brand, sales_group, and supplier into their respective tables
        # region -- step b: select item_type_id, brand_id, sales_group_id, and supplier_id to get their ids
        item_type_id = self.cursor.execute('''
        SELECT ItemTypeId FROM ItemType
        WHERE Name = ?
        ''', (prod_type,))
        item_type_id = self.cursor.fetchone()[0]

        brand_id = self.cursor.execute('''
        SELECT BrandId FROM Brand
        WHERE Name = ?
        ''', (prod_brand,))
        brand_id = self.cursor.fetchone()[0]

        sales_group_id = self.cursor.execute('''
        SELECT SalesGroupId FROM SalesGroup
        WHERE Name = ?
        ''', (prod_sales_group,))
        sales_group_id = self.cursor.fetchone()[0]

        supplier_id = self.cursor.execute('''
        SELECT SupplierId FROM Supplier
        WHERE Name = ?
        ''', (prod_supplier,))
        supplier_id = self.cursor.fetchone()[0]
        # endregion -- step b: select item_type_id, brand_id, sales_group_id, and supplier_id to get their ids
        # region -- step c: insert barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, and supplier_id into the item table
        self.cursor.execute('''
        INSERT INTO Item (Barcode, Name, ExpireDt, ItemTypeId, BrandId, SalesGroupId, SupplierId)
        SELECT ?, ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Item
            INNER JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
            INNER JOIN Brand ON Item.BrandId = Brand.BrandId
            INNER JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
            INNER JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
        WHERE
            Item.Barcode = ? AND
            Item.Name = ? AND
            Item.ExpireDt = ? AND
            Item.ItemTypeId = ? AND
            Item.BrandId = ? AND
            Item.SupplierId = ? AND
            Item.SalesGroupId = ?
        )''', (prod_barcode, prod_name, prod_exp_dt, item_type_id, brand_id, sales_group_id, supplier_id,
              prod_barcode, prod_name, prod_exp_dt, item_type_id, brand_id, sales_group_id, supplier_id))
        # endregion -- step c: insert barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, and supplier_id into the item table
        # region -- step d: select prod_item_id to get its id
        prod_item_id = self.cursor.execute('''
        SELECT ItemId FROM Item
        WHERE Barcode = ? AND Name = ? AND ExpireDt = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?
        ''', (prod_barcode, prod_name, prod_exp_dt, item_type_id, brand_id, sales_group_id, supplier_id))
        prod_item_id = self.cursor.fetchone()[0]
        # endregion -- step d: select prod_item_id to get its id
        # region -- step e: insert item_price data depending on the conditions
        # region -- condition 1
        if prod_promo_name == 'No promo':
            self.cursor.execute('''
            INSERT INTO ItemPrice (ItemId, Cost, SellPrice, DiscountValue, EffectiveDt)
            SELECT ?, ?, ?, 0, ?
            WHERE NOT EXISTS (
            SELECT 1 FROM ItemPrice
            WHERE 
                ItemId = ? AND
                Cost = ? AND
                SellPrice = ? AND
                DiscountValue = 0 AND -- discount value is set to 0 if prod_promo_name is 'No promo'
                EffectiveDt = ?
            )''', (prod_item_id, prod_cost, prod_sell_price, prod_effective_dt,
                prod_item_id, prod_cost, prod_sell_price, prod_effective_dt))
            self.conn.commit()
        # endregion -- condition 1
        # region -- condition 2
        else:
            # select prod_promo_id to get its id
            prod_promo_id = self.cursor.execute('''
            SELECT PromoId FROM Promo
            WHERE Name = ? AND PromoType = ? AND DiscountPercent = ?
            ''', (prod_promo_name, prod_promo_type, prod_promo_percent))
            prod_promo_id = self.cursor.fetchone()[0]

            # insert item_price with end_date 
            self.cursor.execute('''
            INSERT INTO ItemPrice (ItemId, Cost, SellPrice, PromoId, DiscountValue, EffectiveDt)
            SELECT ?, ?, ?, 0, 0, DATE(?, '+1 day')
            WHERE NOT EXISTS (
            SELECT 1 FROM ItemPrice
            WHERE 
                ItemId = ? AND
                Cost = ? AND
                SellPrice = ? AND
                PromoId = 0 AND
                DiscountValue = 0 AND
                EffectiveDt = DATE(?, '+1 day')
            )''', (prod_item_id, prod_cost, prod_sell_price, prod_promo_end_dt,
                prod_item_id, prod_cost, prod_sell_price, prod_promo_end_dt))

            # insert item_price with start_date
            self.cursor.execute('''
            INSERT INTO ItemPrice (ItemId, Cost, SellPrice, PromoId, DiscountValue, EffectiveDt)
            SELECT ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
            SELECT 1 FROM ItemPrice
            WHERE 
                ItemId = ? AND
                Cost = ? AND
                SellPrice = ? AND
                PromoId = ? AND
                DiscountValue = ? AND
                EffectiveDt = ?
            )''', (prod_item_id, prod_cost, prod_promo_sell_price, prod_promo_id, prod_promo_value, prod_promo_start_dt,
                prod_item_id, prod_cost, prod_promo_sell_price, prod_promo_id, prod_promo_value, prod_promo_start_dt))
            self.conn.commit()
        # endregion -- condition 2
        # endregion -- step e: insert item_price data depending on the conditions
        # region -- step f: insert stock data depending on the conditions
        if prod_tracking == True:
            self.cursor.execute('''
            INSERT INTO Stock (ItemId, Available, OnHand)
            SELECT ?, ?, ?
            WHERE NOT EXISTS(
            SELECT 1 FROM Stock
            WHERE
                ItemId = ? AND
                Available = ? AND
                OnHand = ?
            )''', (prod_item_id, stock_available, stock_on_hand,
                   prod_item_id, stock_available, stock_on_hand))
            self.conn.commit()
            pass
        # endregion -- step f: insert stock data depending on the conditions
    def edit_selected_prod(
        self,
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
        prod_tracking,

        prod_item_id,
        prod_price_id,
        prod_promo_id,
        prod_stock_id
    ):
        # region -- assign values if empty string
        prod_barcode = '[no data]' if prod_barcode == '' else prod_barcode
        prod_name = '[no data]' if prod_name == '' else prod_name
        prod_exp_dt = '9999-12-31' if prod_exp_dt == '' else prod_exp_dt

        prod_type = '[no data]' if prod_type == '' else prod_type
        prod_brand = '[no data]' if prod_brand == '' else prod_brand
        prod_sales_group = '[no data]' if prod_sales_group == '' else prod_sales_group
        prod_supplier = '[no data]' if prod_supplier == '' else prod_supplier

        prod_cost = 0 if prod_cost == '' else prod_cost
        prod_sell_price = 0 if prod_sell_price == '' else prod_sell_price
        prod_effective_dt = str(date.today()) if prod_effective_dt == '' else prod_effective_dt
        prod_promo_name = 'No promo' if prod_promo_name == '' else prod_promo_name
        prod_promo_type = '[no data]' if prod_promo_type == '' else prod_promo_type
        prod_promo_percent = 0 if prod_promo_percent == '' else prod_promo_percent
        prod_promo_value = 0 if prod_promo_value == '' else prod_promo_value
        prod_promo_sell_price = 0 if prod_promo_sell_price == '' else prod_promo_sell_price
        prod_promo_start_dt = str(date.today()) if prod_promo_start_dt == '' else prod_promo_start_dt
        prod_promo_end_dt = str(date.today()) if prod_promo_end_dt == '' else prod_promo_end_dt

        prod_tracking = False if prod_tracking == '' else prod_tracking
        # endregion
        
        if prod_promo_id == 0 and prod_promo_name == 'No promo':
            print(prod_name)
            self.cursor.execute('''
            UPDATE Item
            SET Barcode = ?,
                Name = ?,
                ExpireDt = ?
            WHERE ItemId = ? 
            ''', (prod_barcode, prod_name, prod_exp_dt, prod_item_id))
            self.conn.commit()

            self.cursor.execute('''
            UPDATE ItemPrice
            SET Cost = ?, SellPrice = ?, EffectiveDt = ?
            WHERE ItemPriceId = ?
            ''', (prod_cost, prod_sell_price, prod_effective_dt, prod_price_id))
            self.conn.commit()
        elif prod_promo_id == 0 and prod_promo_name != 'No promo':
            # step a: insert item_type, brand, sales_group, and supplier into their respective tables
            self.cursor.execute('''
            INSERT INTO ItemType (Name)
            SELECT ? WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = ?)
            ''', (prod_type, prod_type))
            self.conn.commit()

            self.cursor.execute('''
            INSERT INTO Brand (Name)
            SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = ?)
            ''', (prod_brand, prod_brand))
            self.conn.commit()

            self.cursor.execute('''
            INSERT INTO SalesGroup (Name)
            SELECT ? WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = ?)
            ''', (prod_sales_group, prod_sales_group))
            self.conn.commit()

            self.cursor.execute('''
            INSERT INTO Supplier (Name)
            SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = ?)
            ''', (prod_supplier, prod_supplier))
            self.conn.commit()

            # step b: select item_type_id, brand_id, sales_group_id, and supplier_id to get their ids
            item_type_id = self.cursor.execute('''
            SELECT ItemTypeId FROM ItemType
            WHERE Name = ?
            ''', (prod_type,))
            item_type_id = self.cursor.fetchone()[0]

            brand_id = self.cursor.execute('''
            SELECT BrandId FROM Brand
            WHERE Name = ?
            ''', (prod_brand,))
            brand_id = self.cursor.fetchone()[0]

            sales_group_id = self.cursor.execute('''
            SELECT SalesGroupId FROM SalesGroup
            WHERE Name = ?
            ''', (prod_sales_group,))
            sales_group_id = self.cursor.fetchone()[0]

            supplier_id = self.cursor.execute('''
            SELECT SupplierId FROM Supplier
            WHERE Name = ?
            ''', (prod_supplier,))
            supplier_id = self.cursor.fetchone()[0]

            # step c: insert barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, and supplier_id into the item table
            self.cursor.execute('''
            INSERT INTO Item (Barcode, Name, ExpireDt, ItemTypeId, BrandId, SalesGroupId, SupplierId)
            SELECT ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS(
            SELECT 1 FROM Item
                INNER JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                INNER JOIN Brand ON Item.BrandId = Brand.BrandId
                INNER JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                INNER JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
            WHERE
                Item.Barcode = ? AND
                Item.Name = ? AND
                Item.ExpireDt = ? AND
                Item.ItemTypeId = ? AND
                Item.BrandId = ? AND
                Item.SupplierId = ? AND
                Item.SalesGroupId = ?
            )''', (prod_barcode, prod_name, prod_exp_dt, item_type_id, brand_id, sales_group_id, supplier_id,
                prod_barcode, prod_name, prod_exp_dt, item_type_id, brand_id, sales_group_id, supplier_id))
            self.conn.commit()

            # step d:
            # select prod_item_id to get its id
            prod_item_id = self.cursor.execute('''
            SELECT ItemId FROM Item
            WHERE Barcode = ? AND Name = ? AND ExpireDt = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?
            ''', (prod_barcode, prod_name, prod_exp_dt, item_type_id, brand_id, sales_group_id, supplier_id))
            prod_item_id = self.cursor.fetchone()[0]

            # select prod_promo_id to get its id
            new_prod_promo_id = self.cursor.execute('''
            SELECT PromoId FROM Promo
            WHERE Name = ? AND PromoType = ? AND DiscountPercent = ?
            ''', (prod_promo_name, prod_promo_type, prod_promo_percent))
            new_prod_promo_id = self.cursor.fetchone()[0]

            # insert item_price with end_date 
            self.cursor.execute('''
            INSERT INTO ItemPrice (ItemId, Cost, SellPrice, PromoId, DiscountValue, EffectiveDt)
            SELECT ?, ?, ?, 0, 0, DATE(?, '+1 day')
            WHERE NOT EXISTS (
            SELECT 1 FROM ItemPrice
            WHERE 
                ItemId = ? AND
                Cost = ? AND
                SellPrice = ? AND
                PromoId = 0 AND
                DiscountValue = 0 AND
                EffectiveDt = DATE(?, '+1 day')
            )''', (prod_item_id, prod_cost, prod_sell_price, prod_promo_end_dt,
                prod_item_id, prod_cost, prod_sell_price, prod_promo_end_dt))
            self.conn.commit()

            # insert item_price with start_date
            self.cursor.execute('''
            INSERT INTO ItemPrice (ItemId, Cost, SellPrice, PromoId, DiscountValue, EffectiveDt)
            SELECT ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
            SELECT 1 FROM ItemPrice
            WHERE 
                ItemId = ? AND
                Cost = ? AND
                SellPrice = ? AND
                PromoId = ? AND
                DiscountValue = ? AND
                EffectiveDt = ?
            )''', (prod_item_id, prod_cost, prod_promo_sell_price, new_prod_promo_id, prod_promo_value, prod_promo_start_dt,
                prod_item_id, prod_cost, prod_promo_sell_price, prod_promo_id, prod_promo_value, prod_promo_start_dt))
            self.conn.commit()
        elif prod_promo_id != 0 and prod_promo_name != 'No promo':
            self.cursor.execute('''
            UPDATE Item
            SET Barcode = ?, Name = ?, ExpireDt = ?
            WHERE ItemId = ?
            ''', (prod_barcode, prod_name, prod_exp_dt, prod_item_id))
            self.conn.commit()

        if prod_stock_id == str(None) and prod_tracking == True:
            print('a here!!!')
            self.cursor.execute('''
            INSERT INTO Stock (ItemId, Available, OnHand)
            SELECT ?, 0, 0
            WHERE NOT EXISTS(
            SELECT 1 FROM Stock
            WHERE
                ItemId = ? AND
                Available = 0 AND
                OnHand = 0
            )''', (prod_item_id, prod_item_id))
            self.conn.commit()
            pass
        elif prod_stock_id != str(None) and prod_tracking == False:
            print('b here!!!')
            self.cursor.execute('''
            DELETE FROM Stock
            WHERE StockId = ? AND ItemId = ?
            ''', (prod_stock_id, prod_item_id))
            self.conn.commit()
            pass
        elif prod_stock_id != str(None) and prod_tracking == True:
            print('a here!!!')
            self.cursor.execute('''
            INSERT INTO Stock (ItemId, Available, OnHand)
            SELECT ?, 0, 0
            WHERE NOT EXISTS(
            SELECT 1 FROM Stock
            WHERE
                ItemId = ? AND
                Available = 0 AND
                OnHand = 0
            )''', (prod_item_id, prod_item_id))
            self.conn.commit()
            pass

        pass
    def delete_selected_prod(self, prod_price_id):
        self.cursor.execute('''
            DELETE FROM ItemPrice
            WHERE ItemPriceId = ? AND EffectiveDt > CURRENT_DATE
            ''', (prod_price_id,))
        
        self.conn.commit()
        pass
    def delete_selected_inventory(self, prod_stock_id):
        self.cursor.execute('''
        DELETE FROM Stock
        WHERE StockId = ?
        ''', (prod_stock_id,))
        self.conn.commit()

    def edit_selected_stock(self, stock_available, stock_on_hand, stock_id):
        stock_available = 0 if stock_available == '' else stock_available
        stock_on_hand = 0 if stock_on_hand == '' else stock_on_hand
            
        self.cursor.execute('''
        UPDATE Stock
        SET Available = ?, OnHand = ?
        WHERE StockId = ?
        ''', (stock_available, stock_on_hand, stock_id))
        self.conn.commit()
        pass
    def delete_selected_stock(self, stock_id):
        self.cursor.execute('''
        DELETE FROM Stock
        WHERE StockId = ?
        ''', (stock_id,))
        self.conn.commit()

    def list_all_prod_col(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.cursor.execute('''
            SELECT
                COALESCE(NULLIF(Item.Barcode, ''), '[no data]') AS Barcode,
                COALESCE(NULLIF(Item.Name, ''), '[no data]') AS Item,
                COALESCE(NULLIF(Item.ExpireDt, ''), '[no data]') AS ExpireDt,
                            
                COALESCE(NULLIF(ItemType.Name, ''), '[no data]') AS ItemType, 
                COALESCE(NULLIF(Brand.Name, ''), '[no data]') AS Brand, 
                COALESCE(NULLIF(SalesGroup.Name, ''), '[no data]') AS SalesGroup, 
                COALESCE(NULLIF(Supplier.Name, ''), '[no data]') AS Supplier,
                            
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
                Item.Barcode LIKE ? OR
                Item.Name LIKE ? OR
                ItemType.Name LIKE ? OR 
                Brand.Name LIKE ? OR 
                SalesGroup.Name LIKE ? OR 
                Supplier.Name LIKE ? OR
                InventoryTracking LIKE ?
            ORDER BY Item.ItemId DESC, ItemPrice.EffectiveDt DESC, Item.UpdateTs DESC
            LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
            ''', (
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                '%' + str(text_filter) + '%',
                page_size,  # Limit
                offset     # Offset
            ))

        product = self.cursor.fetchall()

        return product
        pass
    def list_all_stock_col(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.cursor.execute('''
            SELECT
                COALESCE(NULLIF(Item.Name, ''), '[no data]') AS Item,
                COALESCE(NULLIF(Stock.Available, ''), 0) AS Available,
                COALESCE(NULLIF(Stock.OnHand, ''), 0) AS OnHand,
                Stock.UpdateTs,
                Stock.ItemId, -- 4
                StockId -- 5
            FROM Stock
                LEFT JOIN Item ON Stock.ItemId = Item.ItemId
            WHERE
                Item LIKE ? OR
                Available LIKE ? OR
                OnHand LIKE ?
            ORDER BY Item, Stock.UpdateTs DESC
            LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
                                
            ''', (
                '%' + text_filter + '%', 
                '%' + text_filter + '%', 
                '%' + text_filter + '%',
                page_size,  # Limit
                offset     # Offset
            ))
        
        stock = self.cursor.fetchall()
        
        return stock
        pass
    
    def list_item_type_col(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM ItemType
        ORDER BY UpdateTs DESC
        ''')
            
        item_type = self.cursor.fetchall()

        return item_type
        pass
    def list_brand_col(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Brand
        ORDER BY UpdateTs DESC
        ''')
            
        brand = self.cursor.fetchall()

        return brand 
        pass
    def list_supplier_col(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Supplier
        ORDER BY UpdateTs DESC
        ''')
            
        supplier = self.cursor.fetchall()

        return supplier 
        pass
    def list_promo_name_col(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Promo
        ORDER BY UpdateTs DESC
        ''')
            
        promo = self.cursor.fetchall()

        return promo 
        pass
    def list_promo_type_col(self, prod_promo_name):
        self.cursor.execute('''
        SELECT DISTINCT PromoType FROM Promo
        WHERE Name = ?
        ORDER BY PromoId DESC, UpdateTs DESC                
        ''', (prod_promo_name,))
        
        promo_type = self.cursor.fetchone()[0]
        
        return promo_type
        pass
    def list_promo_percent_col(self, prod_promo_name):
        self.cursor.execute('''
        SELECT DISTINCT DiscountPercent FROM Promo
        WHERE Name = ?
        ORDER BY PromoId DESC, UpdateTs DESC                
        ''', (prod_promo_name,))
        
        promo_percent = self.cursor.fetchone()[0]
        
        return promo_percent

    def count_all_prod(self):
        self.cursor.execute('''
        SELECT COUNT(*) FROM ItemPrice
        ''')
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def count_prod_list_total_pages(self, page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM Item
            ''')

        total_prod = self.cursor.fetchone()[0]
        total_pages = (total_prod - 1) // page_size + 1

        return total_pages
        pass
    def count_stock_list_total_pages(self, page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM Stock
            ''')

        total_prod = self.cursor.fetchone()[0]
        total_pages = (total_prod - 1) // page_size + 1

        return total_pages
    