import os, sys
from datetime import *
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema.inventory_management_schema import *

class ProductManagementSchema():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        self.inventory_management_schema = InventoryManagementSchema()
        
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    # -- for adding
    def add_new_product(
            self,
            barcode='<no data>',
            item_name='<no data>',
            expire_dt='9999-12-31',
            item_type='<no data>',
            brand='<no data>',
            sales_group='<no data>',
            supplier='<no data>',
            cost=0,
            sell_price=0,
            effective_dt=date.today(),
            promo_name='No promo',
            promo_type='<no data>',
            discount_percent=0,
            discount_value=0,
            new_sell_price=0,
            start_dt=date.today(),
            end_dt=date.today(),
            inventory_tracking='Disabled',
            available_stock=0,
            on_hand_stock=0
    ):        
        # step a: insert item_type, brand, sales_group, and supplier into their respective tables
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

        # step d: select item_id to get its id
        item_id = self.cursor.execute('''
        SELECT ItemId FROM Item
        WHERE Barcode = ? AND Name = ? AND ExpireDt = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?
        ''', (barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))
        item_id = self.cursor.fetchone()[0]

        # step e: insert item_price data depending on the conditions
        # -- condition 1
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

        # -- condition 2
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
        
        # step e: insert stock data depending on the conditions
        if inventory_tracking == 'Enabled':
            self.inventory_management_schema.addNewStock(item_id, available_stock, on_hand_stock)
        else:
            pass

        # self.conn.rollback()

    def delete_all_data(self):
        # Execute a DELETE statement without specifying conditions to remove all data
        self.cursor.execute("DELETE FROM ItemType")
        self.cursor.execute("DELETE FROM Brand")
        self.cursor.execute("DELETE FROM SalesGroup")
        self.cursor.execute("DELETE FROM Supplier")
        self.cursor.execute("DELETE FROM Item")
        self.cursor.execute("DELETE FROM ItemPrice")
        self.cursor.execute("DELETE FROM Stock")

        # Commit the changes to save the deletion
        self.conn.commit()
        
    def count_total_product(self):
        self.cursor.execute('''
        SELECT COUNT(*) FROM Item
        ''')
   
        count = self.cursor.fetchone()[0]

        return count      
    
    # -- for populating
    def list_product(self, text_filter='', page_number=1, page_size=30):
        # Calculate the offset to skip rows based on page number and page size
        offset = (page_number - 1) * page_size

        self.cursor.execute('''
            SELECT
                COALESCE(NULLIF(Item.Barcode, ''), '<no data>') AS Barcode,
                COALESCE(NULLIF(Item.Name, ''), '<no data>') AS Item,
                COALESCE(NULLIF(Item.ExpireDt, ''), '<no data>') AS ExpireDt,
                COALESCE(NULLIF(ItemType.Name, ''), '<no data>') AS ItemType, 
                COALESCE(NULLIF(Brand.Name, ''), '<no data>') AS Brand, 
                COALESCE(NULLIF(SalesGroup.Name, ''), '<no data>') AS SalesGroup, 
                COALESCE(NULLIF(Supplier.Name, ''), '<no data>') AS Supplier,
                COALESCE(NULLIF(ItemPrice.Cost, ''), '<no data>') AS Cost,
                COALESCE(NULLIF(ItemPrice.SellPrice, ''), '<no data>') AS SellPrice,
                COALESCE(NULLIF(ItemPrice.EffectiveDt, ''), '<no data>') AS EffectiveDt,
                CASE WHEN Promo.Name IS NOT NULL THEN Promo.Name ELSE 'No promo' END AS Promo,
                COALESCE(NULLIF(ItemPrice.DiscountValue, ''), '<no data>') AS DiscountValue,
                CASE WHEN Stock.StockId <> 0 THEN 'Enabled' ELSE 'Disabled' END AS InventoryTracking,
                COALESCE(NULLIF(Stock.Available, ''), '<no data>') AS Available,
                COALESCE(NULLIF(Stock.OnHand, ''), '<no data>') AS OnHand,
                ItemPrice.UpdateTs,
                                
                ItemPrice.ItemId,
                ItemPrice.ItemPriceId,
                ItemPrice.PromoId      
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


    def getPromoTypeAndDiscountPercent(self, promo_name):
        self.cursor.execute('''
        SELECT DISTINCT PromoType, DiscountPercent FROM Promo
        WHERE Name = ?
        ''', (promo_name,))
        data = self.cursor.fetchall()
        
        return data
    
    # def getNewSellPrice(self):
    #     pass

    # -- for editing
    def editSelectedItem(
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
            new_sell_price,
            promo_name,
            promo_type,
            discount_percent,
            discount_value,
            start_dt,
            end_dt,
            effective_dt,
            item_id,
            item_price_id,
            promo_id
    ):
        # edit without promo and no promo name
        if str(promo_id) == '0' and promo_name == 'No promo':
            self.cursor.execute('''
            UPDATE Item
            SET Barcode = ?, Name = ?, ExpireDt = ?
            WHERE ItemId = ?
            ''', (barcode, item_name, expire_dt, item_id))
            self.conn.commit()

            self.cursor.execute('''
            UPDATE ItemPrice
            SET Cost = ?, SellPrice = ?, EffectiveDt = ?
            WHERE ItemPriceId = ? AND EffectiveDt > CURRENT_DATE
            ''', (cost, sell_price, effective_dt, item_price_id))
            self.conn.commit()
        
        # edit without promo but has promo name
        elif str(promo_id) == '0' and promo_name != 'No promo':
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

        # edit with promo and promo name
        elif str(promo_id) != '0' and promo_name != 'No promo':
            self.cursor.execute('''
            UPDATE Item
            SET Barcode = ?, Name = ?, ExpireDt = ?
            WHERE ItemId = ?
            ''', (barcode, item_name, expire_dt, item_id))
            self.conn.commit()

    # -- for removing
    def removeSelectedItem(self, item_price_id):
        self.cursor.execute('''
        DELETE FROM ItemPrice
        WHERE ItemPriceId = ? AND EffectiveDt > CURRENT_DATE
        ''', (item_price_id,))
        self.conn.commit()
        
    # -- for populating
    def listItem(self, text):
        self.cursor.execute('''
        SELECT
            COALESCE(Item.Barcode, 'unk') AS Barcode,
            COALESCE(Item.Name, 'unk') AS Name,
            COALESCE(Item.ExpireDt, 'unk') AS ExpireDt, 
            COALESCE(ItemType.Name, 'unk') AS ItemType, 
            COALESCE(Brand.Name, 'unk') AS Brand, 
            COALESCE(SalesGroup.Name, 'unk') AS SalesGroup, 
            COALESCE(Supplier.Name, 'unk') AS Supplier, 
            COALESCE(ItemPrice.Cost, 0.00) AS Cost, 
            COALESCE(ItemPrice.SellPrice, 0.00) AS SellPrice,
            COALESCE(ItemPrice.DiscountValue, 0.00) AS DiscountValue, 
            COALESCE(ItemPrice.EffectiveDt, 'unk') AS EffectiveDt,
            CASE WHEN Promo.Name IS NOT NULL THEN Promo.Name ELSE 'N/A' END AS Promo,
            CASE WHEN Stock.StockId <> 0 THEN 'Enabled' ELSE 'Disabled' END AS InventoryTracking, -- 12
            Promo.PromoType,
            Promo.DiscountPercent,
            ItemPrice.ItemId, --15
            ItemPrice.ItemPriceId,
            ItemPrice.PromoId
                            
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
            Item.ExpireDt LIKE ? OR 
            ItemType.Name LIKE ? OR 
            Brand.Name LIKE ? OR 
            SalesGroup.Name LIKE ? OR 
            Supplier.Name LIKE ? OR 
            ItemPrice.Cost LIKE ? OR 
            ItemPrice.SellPrice LIKE ? OR
            ItemPrice.DiscountValue LIKE ? OR 
            ItemPrice.EffectiveDt LIKE ? OR
            Promo LIKE ? OR
            InventoryTracking LIKE ?
                            
        ORDER BY Item.ItemId DESC, ItemPrice.EffectiveDt DESC, Item.UpdateTs DESC
                            
        ''', (
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',))
   
        item = self.cursor.fetchall()

        return item       

    # -- for filling combo box
    def fillItemComboBox(self):
        self.cursor.execute('''
        SELECT DISTINCT
            COALESCE(Item.Name, 'unk') AS Name,
            COALESCE(ItemType.Name, 'unk') AS ItemType, 
            COALESCE(Brand.Name, 'unk') AS Brand, 
            COALESCE(Supplier.Name, 'unk') AS Supplier
                            
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
    
        ORDER BY Item.ItemId DESC, ItemPrice.EffectiveDt DESC, Item.UpdateTs DESC
        ''')
            
        item = self.cursor.fetchall()

        return item   
    