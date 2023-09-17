import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class InventoryManagementSchema():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    # INVENTORY MANAGEMENT
    # -- for adding
    def addNewStock(self, item_id, available_stock, on_hand_stock):
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

    # -- for editing
    def editSelectedStock(self, available_stock, on_hand_stock, item_id, stock_id):
        self.cursor.execute('''
        UPDATE Stock
        SET OnHand = ?, Available = ?
        WHERE ItemId = ? OR StockId = ?
        ''', (available_stock, on_hand_stock, item_id, stock_id))
        self.conn.commit()

    # -- for removing
    def removeSelectedStock(self, stock_id):
        self.cursor.execute('''
        DELETE FROM Stock
        WHERE StockId = ?
        ''', (stock_id,))
        self.conn.commit()

    # -- for populating
    def listStock(self, text):
        self.cursor.execute('''
        SELECT
            COALESCE(Item.ItemName, 'unk'),
            Stock.OnHand,
            Stock.Available,
            Stock.ItemId,
            StockId
        FROM Stock
            LEFT JOIN Item ON Stock.ItemId = Item.ItemId
        WHERE
            Item.ItemName LIKE ? OR
            Stock.OnHand LIKE ? OR
            Stock.Available LIKE ?
        ORDER BY Item.ItemName, Item.UpdateTs DESC
                            
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        stock = self.cursor.fetchall()
        
        return stock

