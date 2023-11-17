import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

cwd = os.getcwd() # get current working dir
sys.path.append(os.path.join(cwd))

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

current_date = str(date.today())

class MyPOSSchema:
    def __init__(self):
        self.setup_sales_db_conn()
        self.setup_txn_db_conn()
        self.setup_accounts_db_conn()
        self.setup_syslib_db_conn()

        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.create_transaction_table()

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
    def setup_syslib_db_conn(self):
        self.syslib_file = os.path.abspath(qss.db_file_path + qss.syslib_file_name)
        self.syslib_conn = sqlite3.connect(database=self.syslib_file)
        self.syslib_cursor = self.syslib_conn.cursor()
        pass
    
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

    def select_product_data_as_display(self, text='', order_type='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
            WITH RankedProduct AS (
                SELECT DISTINCT
                    Item.Name, 
                    Brand.Name,     
                    Item.Barcode, 
                    ItemPrice.SellPrice, 
                    ItemPrice.DiscountValue, 
                    ItemPrice.EffectiveDt, 
                    Stock.OnHand,
                    Item.ItemId,

                    SalesGroup.SalesGroupId, 
                    ItemPrice.ItemPriceId,
                    ItemPrice.ItemId,   
                    Promo.PromoId, 
                    Stock.StockId,
                                  
                    ROW_NUMBER() OVER(PARTITION BY Item.Name ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC) AS RowNumber
                FROM ItemPrice
                LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
                WHERE
                    (Item.Barcode LIKE "%{text}%" OR
                    Item.Name LIKE "%{text}%" OR
                    ItemType.Name LIKE "%{text}%" OR
                    Brand.Name LIKE "%{text}%") AND
                    SalesGroup.Name = "{order_type}" AND
                    ItemPrice.EffectiveDt <= CURRENT_DATE
                ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC
            )
            SELECT * FROM RankedProduct 
            WHERE RowNumber = 1 
            LIMIT {page_size} OFFSET {offset}

        """)

        product_data = self.sales_cursor.fetchall()


        return product_data
        pass
    def select_product_data_with_barcode(self, barcode='', order_type=''):
        try:
            self.sales_cursor.execute(f"""
                WITH RankedProduct AS (
                    SELECT DISTINCT
                        Item.Name, 
                        ItemPrice.ItemPriceId,
                        ItemPrice.ItemId,
                                    
                        ROW_NUMBER() OVER(PARTITION BY Item.Name ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC) AS RowNumber
                    FROM ItemPrice
                    LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                    LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                    LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
                    LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
                    LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                    LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
                    LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
                    WHERE
                        Item.Barcode = "{barcode}" AND
                        SalesGroup.Name = "{order_type}" AND
                        ItemPrice.EffectiveDt <= CURRENT_DATE
                    ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC
                )
                SELECT * FROM RankedProduct 
                WHERE RowNumber = 1
            """)

            product_data  = self.sales_cursor.fetchall()[0]

        except ValueError as e:
            product_data = ['',0,0]
            pass

        return product_data
        pass
    
    def select_product_data_for_view_dialog(self, product_name, product_barcode):
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
                Promo.Name, 
                ItemPrice.DiscountValue, 
                        
                CASE WHEN Stock.StockId > 0 THEN 'Enabled' ELSE 'Disabled' END AS StockStatus,
                Stock.OnHand,
                
                ItemPrice.UpdateTs
            FROM ItemPrice
                LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
            WHERE Item.Name = "{product_name}" AND Item.Barcode = "{product_barcode}" AND ItemPrice.EffectiveDt <= CURRENT_DATE
            ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC, ItemPrice.EffectiveDt DESC
            LIMIT 1
        """)

        product_data = self.sales_cursor.fetchall()

        return product_data[0]
        pass

    def select_product_data_for_order_table(self, product_price_id=0, product_id=0):
        try:
            self.sales_cursor.execute(f"""
                SELECT 
                    Item.Name, 
                    ItemPrice.SellPrice, 
                    ItemPrice.DiscountValue, 

                    Item.ItemId,    
                    ItemPrice.ItemPriceId,    
                    Stock.StockId
                FROM ItemPrice
                    LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                    LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
                WHERE ItemPrice.ItemPriceId = {product_price_id} AND ItemPrice.ItemId = {product_id} AND ItemPrice.EffectiveDt <= CURRENT_DATE
                ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC, ItemPrice.EffectiveDt DESC
                LIMIT 1
            """)

            product_data = self.sales_cursor.fetchall()

            return product_data[0]
        except Exception as e:
            with open(f"{current_date}_log.txt", 'a') as file: file.write(f"[{str(datetime.today())}] [{e}]\n")

    def select_product_data_total_page_count(self, text='', order_type='', page_size=30):
        try:
            self.sales_cursor.execute(f"""
                WITH RankedProduct AS (
                    SELECT 
                        Item.Name, 
                        Brand.Name,     
                        Item.Barcode, 
                        ItemPrice.SellPrice, 
                        ItemPrice.DiscountValue, 
                        ItemPrice.EffectiveDt, 
                        Stock.OnHand,
                        Item.ItemId,
                        SalesGroup.SalesGroupId, 
                        ItemPrice.ItemPriceId,
                        ItemPrice.ItemId,   
                        Promo.PromoId, 
                        Stock.StockId,
                        ROW_NUMBER() OVER(PARTITION BY Item.Name ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC) AS RowNumber
                    FROM ItemPrice
                    LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                    LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                    LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
                    LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
                    LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                    LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
                    LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
                    WHERE
                        (Item.Barcode LIKE "%{text}%" OR
                        Item.Name LIKE "%{text}%" OR
                        ItemType.Name LIKE "%{text}%" OR
                        Brand.Name LIKE "%{text}%") AND
                        SalesGroup.Name = "{order_type}" AND
                        ItemPrice.EffectiveDt <= CURRENT_DATE
                )
                SELECT COUNT(*) FROM RankedProduct 
                WHERE RowNumber = 1 
            """)

            total_product_data_count = self.sales_cursor.fetchone()[0]
            total_page_count = (total_product_data_count - 1) // page_size + 1

            return total_page_count
        except Exception as e:
            return 0


        pass

    def select_customer_data_with_customer_reward_data(self, customer_name):
        try:
            self.sales_cursor.execute(f"""
                SELECT Customer.Name, Customer.Phone, CustomerReward.Points FROM Customer
                LEFT JOIN CustomerReward ON Customer.CustomerId = CustomerReward.CustomerId
                WHERE Customer.Name = "{customer_name}"
            """)

            customer_data = self.sales_cursor.fetchall()

            return customer_data[0]
        except Exception as e:
            return ['N/A','N/A',0]
        pass
    def select_customer_name_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT DISTINCT Name FROM Customer
            ORDER BY CustomerId DESC, UpdateTs DESC
        """)

        customer_name = self.sales_cursor.fetchall()

        return customer_name

    def select_customer_id_by_name(self, customer_name):
        try:
            self.sales_cursor.execute(f"""
                SELECT CustomerId FROM Customer
                WHERE Name = "{customer_name}"
            """)
            customer_id = self.sales_cursor.fetchone()[0]
            
            return customer_id
            pass
        except Exception as e:
            return 0

        pass
    def select_sales_group_id_by_name(self, sales_group_name):
        try:
            self.sales_cursor.execute(f"""
                SELECT SalesGroupId FROM SalesGroup
                WHERE Name = "{sales_group_name}"
            """)
            sales_group_id = self.sales_cursor.fetchone()[0]
            
            return sales_group_id
            pass
        except Exception as e:
            return 0

        pass
    def select_product_id_by_name(self, product_name):
        try:
            self.sales_cursor.execute(f"""
                SELECT ItemId FROM Item
                WHERE Name = "{product_name}"
            """)
            product_id = self.sales_cursor.fetchone()[0]
            
            return product_id
            pass
        except Exception as e:
            return 0
        pass
    def select_product_price_id_by_product_id(self, product_id):
        try:
            self.sales_cursor.execute(f"""
                SELECT ItemPriceId FROM ItemPrice
                WHERE ItemId = {product_id} AND EffectiveDt <= CURRENT_DATE
                ORDER BY ItemPriceId DESC, UpdateTs DESC, EffectiveDt DESC
            """)
            product_price_id = self.sales_cursor.fetchone()[0]
            
            return product_price_id
            pass
        except Exception as e:
            return 0
        pass
    def select_stock_id_by_item_id(self, product_id):
        try:
            self.sales_cursor.execute(f"""
                SELECT StockId FROM Stock
                WHERE ItemId = {product_id}
            """)
            stock_id = self.sales_cursor.fetchone()[0]
            
            return stock_id
            pass
        except Exception as e:
            return 0
        pass  
    def select_user_id_by_name(self, user_name, user_password):
        # try:
        self.accounts_cursor.execute(f"""
            SELECT UserId FROM User
            WHERE Name = "{user_name}" AND Password = "{user_password}"
        """)
        user_id = self.accounts_cursor.fetchone()[0]
        
        print('user_id:', user_id)
        return user_id
        #     pass
        # except Exception as e:
        #     return 0
        pass  
    def select_date_id_by_date_value(self, current_date):
        try:
            self.syslib_cursor.execute(f"""
                SELECT DateId FROM Calendar
                WHERE DateValue = "{current_date}"
            """)
            date_id = self.syslib_cursor.fetchone()[0]
            
            return date_id
            pass
        except Exception as e:
            return 0

        pass
    def select_reward_for_reward_selection(self, order_total):
        self.sales_cursor.execute(f"""
            SELECT 
                Unit, 
                Points
            FROM Reward
            WHERE {order_total} >= Unit
            ORDER BY Unit DESC
            -- LIMIT 1
        """)

        unit_points_data = self.sales_cursor.fetchall()

        return unit_points_data


    def insert_item_sold_data(
            self,
            date_id=0,
            customer_id=0,
            product_price_id=0,
            product_stock_id=0,
            user_id=0,
            reason='N/A',
            product_qty=0,
            product_amount=0,
            void=0,
            reference_number=0,
    ):
        self.txn_cursor.execute(f"""
            INSERT INTO ItemSold (
                DateId,
                CustomerId,
                ItemPriceId,
                StockId,
                UserId,
                Reason,
                Quantity,
                TotalAmount,
                Void,
                ReferenceNumber
            )
            SELECT
                {date_id},
                {customer_id},
                {product_price_id},
                {product_stock_id},
                {user_id},
                "{reason}",
                {product_qty},
                {product_amount},
                {void},
                "{reference_number}"
            WHERE NOT EXISTS (
                SELECT 1 FROM ItemSold
                WHERE
                    DateId = {date_id} AND
                    CustomerId = {customer_id} AND
                    ItemPriceId = {product_price_id} AND
                    StockId = {product_stock_id} AND
                    UserId = {user_id} AND
                    Reason = "{reason}" AND
                    Quantity = {product_qty} AND
                    TotalAmount = {product_amount} AND
                    Void = {void} AND
                    ReferenceNumber = "{reference_number}"
            )
        """)

        self.txn_conn.commit()
        pass
    
    def update_customer_reward_points_by_increment(self, customer_id, order_total):
        # try:
        unit_points_data = self.select_reward_for_reward_selection(order_total=order_total)

        print('unit_points_data:', unit_points_data)

        calculated_points = 0
        used_order_units = 0
        remaining_order_total = order_total

        for unit, points in unit_points_data:
            calculated_points = (remaining_order_total // unit) * points
            used_order_units = (remaining_order_total // unit) * unit
            remaining_order_total = (remaining_order_total - used_order_units)

            print('calculated_points:', calculated_points)
            print('used_order_units:', used_order_units)
            print('remaining_order_total:', remaining_order_total)

            self.sales_cursor.execute(f"""
            UPDATE CustomerReward
            SET 
                Points = Points + {calculated_points},
                UpdateTs = CURRENT_TIMESTAMP
            WHERE CustomerId = {customer_id}
            """)

            self.sales_conn.commit()
        # except Exception as e:
        #     pass
        # pass
    def update_customer_reward_points_by_decrement(self, customer_id, order_total):
        try:
            self.sales_cursor.execute(f"""
            UPDATE CustomerReward
            SET 
                Points = Points - {order_total},
                UpdateTs = CURRENT_TIMESTAMP		
            WHERE CustomerId = {customer_id}
            """)

            self.sales_conn.commit()
        except Exception as e:
            pass
        pass
    def update_stock_on_hand(self, product_id, product_stock_id, product_qty):
        try:
            self.sales_cursor.execute(f"""
            UPDATE Stock
            SET 
                OnHand = CASE 
                    WHEN (OnHand - {product_qty}) < 0 THEN 0 
                    ELSE (OnHand - {product_qty}) 
                END
            WHERE 
                ItemId = {product_id} AND 
                StockId = {product_stock_id}
            """)
            
            self.sales_conn.commit()
        except Exception as e:
            pass

    def update_promo_data(self, promo_name='', promo_type='', promo_percent=0, promo_desc='', promo_id=0):
        self.sales_cursor.execute(f"""
            UPDATE Promo
            SET
                Name = "{promo_name}",
                PromoType = "{promo_type}",
                DiscountPercent = {promo_percent},
                Description = "{promo_desc}"
            WHERE PromoId = {promo_id}
        """)

        self.sales_conn.commit()

    def delete_promo_data(self, promo_id=0):
        self.sales_cursor.execute(f"""
            DELETE FROM Promo
            WHERE PromoId = {promo_id}
        """)

        self.sales_conn.commit()
