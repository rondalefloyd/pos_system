import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyRewardSchema():
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
            Unit FLOAT,
            Points FLOAT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()
    
    def add_new_reward(self, reward_name, reward_description, reward_unit, reward_points):
        reward_name = '[no data]' if reward_name == '' else reward_name
        reward_description = '[no data]' if reward_description == '' else reward_description
        reward_unit = 0 if reward_unit == '' else reward_unit
        reward_points = 0 if reward_points == '' else reward_points

        self.cursor.execute('''
        INSERT INTO Reward (Name, Description, Unit, Points)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Reward
        WHERE
            Name = ? AND
            Description = ? AND
            Unit = ? AND
            Points = ? 
        )''', (reward_name, reward_description, reward_unit, reward_points,
              reward_name, reward_description, reward_unit, reward_points))
        self.conn.commit()
        pass
    def edit_selected_reward(self, reward_name, reward_description, reward_unit, reward_points, reward_id):
        reward_name = '[no data]' if reward_name == '' else reward_name
        reward_description = '[no data]' if reward_description == '' else reward_description
        reward_unit = 0 if reward_unit == '' else reward_unit
        reward_points = 0 if reward_points == '' else reward_points
            
        self.cursor.execute('''
        UPDATE Reward
        SET Name = ?, Description = ?, Unit = ?, Points = ?
        WHERE RewardId = ?
        ''', (reward_name, reward_description, reward_unit, reward_points, reward_id))
        self.conn.commit()
    def delete_selected_reward(self, reward_id):
        self.cursor.execute('''
        DELETE FROM Reward
        WHERE RewardId = ?
        ''', (reward_id,))
        self.conn.commit()

    def list_all_reward_col(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_reward_table()

        self.cursor.execute('''
        SELECT 
            COALESCE(NULLIF(Name, ''), '[no data]') AS Name,
            COALESCE(NULLIF(Description, ''), '[no data]') AS Description,
            COALESCE(NULLIF(Unit, ''), 0) AS Unit,
            COALESCE(NULLIF(Points, ''), 0) AS Points,
            UpdateTs,
            RewardId 
        FROM Reward
        WHERE
            Name LIKE ? OR
            Description LIKE ? OR
            Unit LIKE ? OR
            Points LIKE ? OR
            UpdateTs LIKE ?
        ORDER BY RewardId DESC, UpdateTs DESC
        LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
        ''', (
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            page_size,  # Limit
            offset     # Offset
        ))
        
        reward = self.cursor.fetchall()
        
        return reward

    def count_all_reward(self):
        self.create_reward_table()

        self.cursor.execute('''
        SELECT COUNT(*) FROM Reward
        ''')
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def count_reward_list_total_pages(self, page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM Reward
            ''')

        total_reward = self.cursor.fetchone()[0]
        total_pages = (total_reward - 1) // page_size + 1

        return total_pages
    