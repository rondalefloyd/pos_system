import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class RewardManagementSchema():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    # REWARD MANAGEMENT
    # -- for adding
    def addNewReward(self, reward_name, description, points_rate):
        self.cursor.execute('''
        INSERT INTO Reward (
            Name,
            Description,
            PointsRate
        )
        SELECT ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Reward
        WHERE
            Name = ? AND
            Description = ? AND
            PointsRate = ?
        )''', (reward_name, description, points_rate,
              reward_name, description, points_rate))
        self.conn.commit()

    # -- for editing
    def editSelectedReward(self, reward_name, description, points_rate, customer_id):
        self.cursor.execute('''
        UPDATE Reward
        SET 
            Name = ?,
            Description = ?,
            PointsRate = ?
        WHERE RewardId = ?
        ''', (reward_name, description, points_rate, customer_id))
        self.conn.commit()

    # -- for removing
    def removeSelectedReward(self, customer_id):
        self.cursor.execute('''
        DELETE FROM Reward
        WHERE RewardId = ?
        ''', (customer_id,))
        self.conn.commit()

    # -- for populating
    def listReward(self, text):
        self.cursor.execute('''
        SELECT
            Name,
            Description,
            PointsRate,
            RewardId
        FROM Reward
        WHERE
            Name LIKE ? OR
            Description LIKE ? OR
            PointsRate LIKE ?
        ORDER BY RewardId DESC, UpdateTs DESC
                            
        ''', (
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%'))
        
        reward = self.cursor.fetchall()
        
        return reward
    
    # -- for filling combo box
    def fillRewardComboBox(self):
        self.cursor.execute('''
        SELECT DISTINCT
            Name,
            Description,
            PointsRate,
            RewardId
        FROM Reward
        ORDER BY RewardId DESC, UpdateTs DESC                
        ''')
        
        reward = self.cursor.fetchall()
        
        return reward
