import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class SalesDatabaseSetup():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def createDatabaseTable(self):
        # ItemType
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

        # Brand
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

        # SalesGroup
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS SalesGroup (
            SalesGroupId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        # Supplier
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        # Item
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            Barcode TEXT,
            ItemName TEXT,
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

        # ItemPrice
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ItemPrice (
            ItemPriceId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemId INTEGER DEFAULT 0,
            EffectiveDt DATETIME,
            PromoId INTEGER DEFAULT 0,
            Cost DECIMAL(15, 2),
            Discount DECIMAL(15, 2),
            SellPrice DECIMAL(15, 2),
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (ItemId) REFERENCES Item(ItemId),
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)
        );
        ''')
        self.conn.commit()

        # Stock
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            StockId INTEGER PRIMARY KEY AUTOINCREMENT,
            SupplierId INTEGER DEFAULT 0,
            ItemId INTEGER DEFAULT 0,
            OnHand INTEGER,
            Available INTEGER,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId),
            FOREIGN KEY (ItemId) REFERENCES Item(ItemId)
        );
        ''')
        self.conn.commit()

        # Customer
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerName TEXT,
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

        # Promo
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Promo (
            PromoId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoTyp TEXT,
            Description TEXT,
            DaysToExp INTEGER,
            LessPerc INTEGER,
            StartDt DATETIME,
            EndDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()