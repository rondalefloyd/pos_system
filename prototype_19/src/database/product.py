import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

class ProductSchema():
    def __init__(self):
        super().__init__()
        # Creates folder for the db file
        self.db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/sales.db'))
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/')), exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

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

    def add_new_product(
        # region -- params
        self='',
        barcode='',
        item_name='',
        expire_dt='',
        item_type='',
        brand='',
        sales_group='',
        supplier='',
        cost='',
        sell_price='',
        effective_dt='',
        promo_name='',
        promo_type='',
        discount_percent='',
        discount_value='',
        new_sell_price='',
        start_dt='',
        end_dt='',
        inventory_tracking='',
        available_stock='',
        on_hand_stock=''
        # endregion -- params
    ):
        # WILL BE REVIEWED !!!!
        barcode = '[no data]' if barcode == '' else barcode
        item_name = '[no data]' if item_name == '' else item_name
        expire_dt = '[no data]' if expire_dt == '' else expire_dt

        item_type = '[no data]' if item_type == '' else item_type
        brand = '[no data]' if brand == '' else brand
        sales_group = '[no data]' if sales_group == '' else sales_group
        supplier = '[no data]' if supplier == '' else supplier

        cost = 0 if cost == '' else cost
        sell_price = 0 if sell_price == '' else sell_price
        effective_dt = '[no data]' if effective_dt == '' else effective_dt
        promo_name = '[no data]' if promo_name == '' else promo_name
        promo_type = '[no data]' if promo_type == '' else promo_type
        discount_percent = 0 if discount_percent == '' else discount_percent
        discount_value = 0 if discount_value == '' else discount_value
        new_sell_price = 0 if new_sell_price == '' else new_sell_price
        start_dt = '[no data]' if start_dt == '' else start_dt
        end_dt = '[no data]' if end_dt == '' else end_dt

        inventory_tracking = '[no data]' if inventory_tracking == '' else inventory_tracking
        available_stock = 0 if available_stock == '' else available_stock
        on_hand_stock = 0 if on_hand_stock == '' else on_hand_stock

        self.create_product_table()

        # region -- step a: insert item_type, brand, sales_group, and supplier into their respective tables
        self.cursor.execute('''
        INSERT INTO ItemType (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = ?)
        ''', (item_type, item_type))

        self.cursor.execute('''
        INSERT INTO Brand (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = ?)
        ''', (brand, brand))

        self.cursor.execute('''
        INSERT INTO SalesGroup (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = ?)
        ''', (sales_group, sales_group))

        self.cursor.execute('''
        INSERT INTO Supplier (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = ?)
        ''', (supplier, supplier))
        # endregion -- step a: insert item_type, brand, sales_group, and supplier into their respective tables
        # region -- step b: select item_type_id, brand_id, sales_group_id, and supplier_id to get their ids
        item_type_id = self.cursor.execute('''
        SELECT ItemTypeId FROM ItemType
        WHERE Name = ?
        ''', (item_type,))
        item_type_id = self.cursor.fetchone()[0]

        brand_id = self.cursor.execute('''
        SELECT BrandId FROM Brand
        WHERE Name = ?
        ''', (brand,))
        brand_id = self.cursor.fetchone()[0]

        sales_group_id = self.cursor.execute('''
        SELECT SalesGroupId FROM SalesGroup
        WHERE Name = ?
        ''', (sales_group,))
        sales_group_id = self.cursor.fetchone()[0]

        supplier_id = self.cursor.execute('''
        SELECT SupplierId FROM Supplier
        WHERE Name = ?
        ''', (supplier,))
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
        )''', (barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id,
              barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))
        # endregion -- step c: insert barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, and supplier_id into the item table
        # region -- step d: select item_id to get its id
        item_id = self.cursor.execute('''
        SELECT ItemId FROM Item
        WHERE Barcode = ? AND Name = ? AND ExpireDt = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?
        ''', (barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))
        item_id = self.cursor.fetchone()[0]
        # endregion -- step d: select item_id to get its id
        # region -- step e: insert item_price data depending on the conditions
        # region -- condition 1
        if promo_name == 'No promo':
            self.cursor.execute('''
            INSERT INTO ItemPrice (ItemId, Cost, SellPrice, DiscountValue, EffectiveDt)
            SELECT ?, ?, ?, 0, ?
            WHERE NOT EXISTS (
            SELECT 1 FROM ItemPrice
            WHERE 
                ItemId = ? AND
                Cost = ? AND
                SellPrice = ? AND
                DiscountValue = 0 AND -- discount value is set to 0 if promo_name is 'No promo'
                EffectiveDt = ?
            )''', (item_id, cost, sell_price, effective_dt,
                item_id, cost, sell_price, effective_dt))
            self.conn.commit()
        # endregion -- condition 1
        # region -- condition 2
        else:
            # select promo_id to get its id
            promo_id = self.cursor.execute('''
            SELECT PromoId FROM Promo
            WHERE Name = ? AND PromoType = ? AND DiscountPercent = ?
            ''', (promo_name, promo_type, discount_percent))
            promo_id = self.cursor.fetchone()[0]

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
            )''', (item_id, cost, sell_price, end_dt,
                item_id, cost, sell_price, end_dt))

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
            )''', (item_id, cost, new_sell_price, promo_id, discount_value, start_dt,
                item_id, cost, new_sell_price, promo_id, discount_value, start_dt))
            self.conn.commit()
        # endregion -- condition 2
        # endregion -- step e: insert item_price data depending on the conditions
        # region -- step f: insert stock data depending on the conditions
        if inventory_tracking == 'Enabled':
            self.cursor.execute('''
            INSERT INTO Stock (ItemId, Available, OnHand)
            SELECT ?, ?, ?
            WHERE NOT EXISTS(
            SELECT 1 FROM Stock
            WHERE
                ItemId = ? AND
                Available = ? AND
                OnHand = ?
            )''', (item_id, available_stock, on_hand_stock,
                item_id, available_stock, on_hand_stock))
            self.conn.commit()
            pass
        else:
            pass
        # endregion -- step f: insert stock data depending on the conditions

    def edit_selected_product(
        # region -- params
        self,
        barcode,
        item_name,
        expire_dt,
        item_type,
        brand,
        sales_group,
        supplier,
        cost,
        sell_price,
        effective_dt,
        promo_name,
        promo_type,
        discount_percent,
        discount_value,
        new_sell_price,
        start_dt,
        end_dt,
        inventory_tracking,
        available_stock,
        on_hand_stock,

        item_id,
        item_price_id,
        promo_id,
        stock_id
        # endregion -- params
    ):
        if '' in [
            # region -- conditions
            barcode,
            item_name,
            expire_dt,
            item_type,
            brand,
            sales_group,
            supplier,
            cost,
            sell_price,
            effective_dt,
            promo_name,
            promo_type,
            discount_percent,
            discount_value,
            new_sell_price,
            start_dt,
            end_dt,
            inventory_tracking,
            available_stock,
            on_hand_stock
            # endregion -- conditions
        ]:
            # region -- assign default values
            barcode='[no data]'
            item_name='[no data]'
            expire_dt='9999-12-31'
            item_type='[no data]'
            brand='[no data]'
            sales_group='[no data]'
            supplier='[no data]'
            cost=0
            sell_price=0
            effective_dt=date.today()
            promo_name='No promo'
            promo_type='[no data]'
            discount_percent=0
            discount_value=0
            new_sell_price=0
            start_dt=date.today()
            end_dt=date.today()
            inventory_tracking='Disabled'
            available_stock=0
            on_hand_stock=0
            # endregion -- assign default values
            
        if promo_id == 0 and promo_name == 'No promo':
            print(item_name)
            self.cursor.execute('''
            UPDATE Item
            SET Barcode = ?,
                Name = ?,
                ExpireDt = ?
            WHERE ItemId = ? 
            AND EXISTS (
                SELECT 1
                FROM ItemPrice
                WHERE Item.ItemId = ItemPrice.ItemId
                AND ItemPrice.EffectiveDt > CURRENT_DATE
            )''', (barcode, item_name, expire_dt, item_id))
            self.conn.commit()

            self.cursor.execute('''
            UPDATE ItemPrice
            SET Cost = ?, SellPrice = ?, EffectiveDt = ?
            WHERE ItemPriceId = ? AND EffectiveDt > CURRENT_DATE
            ''', (cost, sell_price, effective_dt, item_price_id))
            self.conn.commit()
        elif promo_id == 0 and promo_name != 'No promo':
            # step a: insert item_type, brand, sales_group, and supplier into their respective tables
            self.cursor.execute('''
            INSERT INTO ItemType (Name)
            SELECT ? WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = ?)
            ''', (item_type, item_type))
            self.conn.commit()

            self.cursor.execute('''
            INSERT INTO Brand (Name)
            SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = ?)
            ''', (brand, brand))
            self.conn.commit()

            self.cursor.execute('''
            INSERT INTO SalesGroup (Name)
            SELECT ? WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = ?)
            ''', (sales_group, sales_group))
            self.conn.commit()

            self.cursor.execute('''
            INSERT INTO Supplier (Name)
            SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = ?)
            ''', (supplier, supplier))
            self.conn.commit()

            # step b: select item_type_id, brand_id, sales_group_id, and supplier_id to get their ids
            item_type_id = self.cursor.execute('''
            SELECT ItemTypeId FROM ItemType
            WHERE Name = ?
            ''', (item_type,))
            item_type_id = self.cursor.fetchone()[0]

            brand_id = self.cursor.execute('''
            SELECT BrandId FROM Brand
            WHERE Name = ?
            ''', (brand,))
            brand_id = self.cursor.fetchone()[0]

            sales_group_id = self.cursor.execute('''
            SELECT SalesGroupId FROM SalesGroup
            WHERE Name = ?
            ''', (sales_group,))
            sales_group_id = self.cursor.fetchone()[0]

            supplier_id = self.cursor.execute('''
            SELECT SupplierId FROM Supplier
            WHERE Name = ?
            ''', (supplier,))
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
            )''', (barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id,
                barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))
            self.conn.commit()

            # step d:
            # select item_id to get its id
            item_id = self.cursor.execute('''
            SELECT ItemId FROM Item
            WHERE Barcode = ? AND Name = ? AND ExpireDt = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?
            ''', (barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))
            item_id = self.cursor.fetchone()[0]

            # select promo_id to get its id
            new_promo_id = self.cursor.execute('''
            SELECT PromoId FROM Promo
            WHERE Name = ? AND PromoType = ? AND DiscountPercent = ?
            ''', (promo_name, promo_type, discount_percent))
            new_promo_id = self.cursor.fetchone()[0]

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
            )''', (item_id, cost, sell_price, end_dt,
                item_id, cost, sell_price, end_dt))
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
            )''', (item_id, cost, new_sell_price, new_promo_id, discount_value, start_dt,
                item_id, cost, new_sell_price, promo_id, discount_value, start_dt))
            self.conn.commit()
        elif promo_id != 0 and promo_name != 'No promo':
            self.cursor.execute('''
            UPDATE Item
            SET Barcode = ?, Name = ?, ExpireDt = ?
            WHERE ItemId = ?
            ''', (barcode, item_name, expire_dt, item_id))
            self.conn.commit()

        if stock_id == 0 and inventory_tracking == 'Enabled':
            self.cursor.execute('''
            INSERT INTO Stock (ItemId, Available, OnHand)
            SELECT ?, ?, ?
            WHERE NOT EXISTS(
            SELECT 1 FROM Stock
            WHERE
                ItemId = ? AND
                Available = ? AND
                OnHand = ?
            )''', (item_id, available_stock, on_hand_stock,
                item_id, available_stock, on_hand_stock))
            self.conn.commit()
            pass
        elif stock_id != 0 and inventory_tracking == 'Disabled':
            self.cursor.execute('''
            DELETE FROM Stock
            WHERE StockId = ? AND ItemId = ?
            ''', (stock_id, item_id))
            self.conn.commit()
            pass
        elif stock_id != 0 and inventory_tracking == 'Enabled':
            self.cursor.execute('''
            UPDATE Stock
            SET Available = ?, OnHand = ?
            WHERE ItemId = ? AND StockId = ?
            ''', (available_stock, on_hand_stock, item_id, stock_id))
            self.conn.commit()
            pass

    def delete_selected_product(self, promo_id, stock_id, item_id):
        self.cursor.execute('''
        DELETE FROM ItemPrice
        WHERE PromoId = ? AND EffectiveDt > CURRENT_DATE
        ''', (promo_id,))
        self.conn.commit()

        # region -- TO REVIEW!!! ---
        self.cursor.execute('''
        DELETE FROM Stock
        WHERE StockId = ? AND ItemId = ?
        ''', (stock_id, item_id))
        self.conn.commit()
        # endregion -- TO REVIEW!!! ---

    def list_product(self, text_filter='', page_number=1, page_size=30):
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
                SalesGroup.Name LIKE ? OR 
                Supplier.Name LIKE ? OR
                InventoryTracking LIKE ?) AND
                (ItemPrice.UpdateTs >= CURRENT_DATE)
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
    
    def list_item_type(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM ItemType
        ORDER BY UpdateTs DESC
        ''')
            
        item_type = self.cursor.fetchall()

        return item_type
        pass
    def list_brand(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Brand
        ORDER BY UpdateTs DESC
        ''')
            
        brand = self.cursor.fetchall()

        return brand 
        pass
    def list_supplier(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Supplier
        ORDER BY UpdateTs DESC
        ''')
            
        supplier = self.cursor.fetchall()

        return supplier 
        pass
    def list_promo(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Promo
        ORDER BY UpdateTs DESC
        ''')
            
        promo = self.cursor.fetchall()

        return promo 
        pass

    def list_promo_type_and_discount_percent(self, promo_name):
        self.cursor.execute('''
        SELECT DISTINCT PromoType, DiscountPercent FROM Promo
        WHERE Name = ?
        ORDER BY PromoId DESC, UpdateTs DESC                
        ''', (promo_name,))
        
        data = self.cursor.fetchall()
        
        return data

# CHECKPOINT!!!


    def count_product(self):
        self.create_product_table()

        self.cursor.execute('''
        SELECT COUNT(*) FROM Item
        ''')
        count = self.cursor.fetchone()[0]
        
        return count
