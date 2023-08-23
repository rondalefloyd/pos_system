import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class InventoryManagementSQL():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

# for creating stock table
    def createStockTable(self):
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

# for storing item data
    def insertStockData(self, supplier_id, item_id, on_hand_stock, available_stock):
        self.cursor.execute('''
        INSERT INTO Stock (SupplierId, ItemId, OnHand, Available)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Stock
            INNER JOIN Item ON Stock.ItemId = Item.ItemId
            INNER JOIN Supplier ON Stock.SupplierId = Supplier.SupplierId
        WHERE
            Stock.SupplierId = ? AND
            Stock.ItemId = ? AND
            Stock.OnHand = ? AND
            Stock.Available = ?
        )''', (supplier_id, item_id, on_hand_stock, available_stock,
              supplier_id, item_id, on_hand_stock, available_stock))
        self.conn.commit()

# for editing items
    def updateStockData(self, on_hand_stock, available_stock, supplier_id, item_id):
        self.cursor.execute('''
        UPDATE Stock
        SET OnHand = ?, Available = ?
        WHERE SupplierId = ? AND ItemId = ?
        ''', (on_hand_stock, available_stock, supplier_id, item_id))
        self.conn.commit()

# for listing data
    def selectAllStockData(self, text):
        self.cursor.execute('''
        SELECT
            COALESCE(Supplier.Name, 'unk') AS Supplier,
            COALESCE(Item.ItemName, 'unk') AS ItemName, 
            Stock.OnHand,
            Stock.Available,
            Supplier.SupplierId,
            Item.ItemId     
        FROM ItemPrice
            LEFT JOIN Item
                ON ItemPrice.ItemId = Item.ItemId
            LEFT JOIN Supplier
                ON Item.SupplierId = Supplier.SupplierId
            LEFT JOIN Stock
                ON Stock.ItemId = Item.ItemId
        WHERE
            Stock.OnHand IS NOT NULL AND
            Stock.Available IS NOT NULL
        ORDER BY Item.ItemId DESC
        ''')
        
        all_data = self.cursor.fetchall()

        return all_data
    
    def selectAllFilteredStockData(self, text):
        self.cursor.execute('''
        SELECT
            COALESCE(Supplier.Name, 'unk') AS Supplier,
            COALESCE(Item.ItemName, 'unk') AS ItemName, 
            Stock.OnHand,
            Stock.Available  
        FROM ItemPrice
            LEFT JOIN Item
                ON ItemPrice.ItemId = Item.ItemId
            LEFT JOIN Supplier
                ON Item.SupplierId = Supplier.SupplierId
            LEFT JOIN Stock
                ON Stock.ItemId = Item.ItemId
        WHERE
            (Stock.OnHand IS NOT NULL AND Stock.Available IS NOT NULL) AND
            (Supplier.Name LIKE ? OR Item.ItemName LIKE ? OR Stock.OnHand LIKE ? OR Stock.Available LIKE ?)
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        stock = self.cursor.fetchall()

        return stock
