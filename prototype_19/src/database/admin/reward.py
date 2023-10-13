import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class RewardSchema():
    def __init__(self):
        super().__init__()
        # Creates folder for the db file
        dir_path = 'G:' + f"/My Drive/database/"
        self.db_file_path = os.path.abspath(dir_path + '/sales.db')
        os.makedirs(os.path.abspath(dir_path), exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

        self.create_reward_table()

    def create_reward_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reward (
            RewardId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Description TEXT,
            PointsRate FLOAT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()
    
    def add_new_reward(self, reward_name, description, points_rate):
        # region -- assign values if empty string
        reward_name = '[no data]' if reward_name == '' else reward_name
        description = '[no data]' if description == '' else description
        points_rate = 0 if points_rate == '' else points_rate
        # endregion -- assign values if empty string

        self.cursor.execute('''
        INSERT INTO Reward (Name, Description, PointsRate)
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

    def edit_selected_reward(self, reward_name, description, points_rate, reward_id):
        # region -- assign values if empty string
        reward_name = '[no data]' if reward_name == '' else reward_name
        description = '[no data]' if description == '' else description
        points_rate = 0 if points_rate == '' else points_rate
        # endregion -- assign values if empty string
            
        self.cursor.execute('''
        UPDATE Reward
        SET Name = ?, Description = ?, PointsRate = ?
        WHERE RewardId = ?
        ''', (reward_name, description, points_rate, reward_id))
        self.conn.commit()

    def delete_selected_reward(self, reward_id):
        self.cursor.execute('''
        DELETE FROM Reward
        WHERE RewardId = ?
        ''', (reward_id,))
        self.conn.commit()

    def list_reward(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_reward_table()

        self.cursor.execute('''
        SELECT Name, Description, PointsRate, UpdateTs, RewardId FROM Reward
        WHERE
            Name LIKE ? OR
            Description LIKE ? OR
            PointsRate LIKE ? OR
            UpdateTs LIKE ?
        ORDER BY RewardId DESC, UpdateTs DESC
        LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
        ''', (
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            page_size,  # Limit
            offset     # Offset
        ))
        
        reward = self.cursor.fetchall()
        
        return reward

    def count_reward(self):
        self.create_reward_table()

        self.cursor.execute('''
        SELECT COUNT(*) FROM Reward
        ''')
        count = self.cursor.fetchone()[0]
        
        return count