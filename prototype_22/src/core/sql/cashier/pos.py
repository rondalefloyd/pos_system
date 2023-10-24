import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

current_date = str(date.today())

class MyPOSSchema:
    def __init__(self):
        self.setup_sales_db_conn()
        self.setup_txn_db_conn()
        self.setup_accounts_db_conn()

        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.create_promo_table()


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
    

    def create_promo_table(self):
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
                ReferenceId TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ItemPriceId) REFERENCES ItemPrice(ItemPriceId),
                FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId),
                FOREIGN KEY (StockId) REFERENCES Stocks(StockId)
            )
        """)

        self.txn_conn.commit()

    def select_product_data_as_display(self, text='', order_type='Retail', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
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
                Promo.PromoId, 
                Stock.StockId
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
                SalesGroup.Name LIKE "%{order_type}%"
            ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC
            LIMIT {page_size}
            OFFSET {offset}
        """)

        product_data = self.sales_cursor.fetchall()

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
                  
                ItemPrice.UpdateTs
            FROM ItemPrice
                LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
                LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
                LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
                LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                LEFT JOIN Promo ON ItemPrice.PromoId = Promo.PromoId
                LEFT JOIN Stock ON Item.ItemId = Stock.ItemId
            WHERE Item.Name = "{product_name}" AND Item.Barcode = "{product_barcode}"
            ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC
            LIMIT 1
        """)

        product_data = self.sales_cursor.fetchall()

        return product_data[0]
        pass

    def select_product_data_for_order_table(self, product_name, product_barcode):
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
                WHERE Item.Name = "{product_name}" AND Item.Barcode = "{product_barcode}"
                ORDER BY ItemPrice.ItemPriceId DESC, ItemPrice.UpdateTs DESC
                LIMIT 1
            """)

            product_data = self.sales_cursor.fetchall()

            return product_data[0]
        except Exception as e:
            with open(f"{current_date}_log.txt", 'a') as file: file.write(f"[{str(datetime.today())}] [{e}]\n")

    def select_product_data_total_page_count(self, order_type='', page_size=30):
        try:
            self.sales_cursor.execute(f"""
                SELECT COUNT(*) FROM ItemPrice
                    LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
                    LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
                WHERE SalesGroup.Name = "{order_type}"
            """)

            total_product_data_count = self.sales_cursor.fetchone()[0]
            total_page_count = (total_product_data_count - 1) // page_size + 1

            return total_page_count
            pass
        except Exception as e:
            return 0

        pass
    
    def select_customer_name_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT DISTINCT Name FROM Customer
            ORDER BY CustomerId DESC, UpdateTs DESC
        """)

        customer_name = self.sales_cursor.fetchall()

        return customer_name

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
