import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyRewardSchema():
    def __init__(self):
        super().__init__()

        self.setup_sales_conn()

        self.create_reward_table()

    def setup_sales_conn(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.sales_file)
        self.cursor = self.conn.cursor()

    def create_reward_table(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Reward (
            RewardId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Description TEXT,
            Unit FLOAT,
            Points FLOAT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()
    
    def insert_new_reward_data(self, reward_name='', reward_description='', reward_unit=0, reward_points=0):
        self.cursor.execute(f"""
        INSERT INTO Reward (Name, Description, Unit, Points)
        SELECT '{reward_name}', '{reward_description}', {reward_unit}, {reward_points}
        WHERE NOT EXISTS(
            SELECT 1 FROM Reward
            WHERE
                Name = '{reward_name}' AND
                Description = '{reward_description}' AND
                Unit = {reward_unit} AND
                Points = {reward_points} 
            )
        """)
        self.conn.commit()
        pass
    def update_selected_reward_data(self, reward_name='', reward_description='', reward_unit=0, reward_points=0, reward_id=0):
        self.cursor.execute(f"""
        UPDATE Reward
        SET 
            Name = '{reward_name}',
            Description = '{reward_description}',
            Unit = {reward_unit},
            Points = {reward_points}
        WHERE RewardId = {reward_id}
        """)
        self.conn.commit()
    def delete_selected_reward_data(self, reward_id=0):
        self.cursor.execute(f"""
        DELETE FROM Reward
        WHERE RewardId = {reward_id}
        """)
        self.conn.commit()

    def select_reward_data(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_reward_table()

        self.cursor.execute(f"""
        SELECT 
            COALESCE(NULLIF(Name, ''), '[no data]') AS Name,
            COALESCE(NULLIF(Description, ''), '[no data]') AS Description,
            COALESCE(NULLIF(Unit, ''), 0) AS Unit,
            COALESCE(NULLIF(Points, ''), 0) AS Points,
            UpdateTs,
            RewardId 
        FROM Reward
        WHERE
            Name LIKE '%{text_filter}%' OR
            Description LIKE '%{text_filter}%' OR
            Unit LIKE '%{text_filter}%' OR
            Points LIKE '%{text_filter}%' OR
            UpdateTs LIKE '%{text_filter}%'
        ORDER BY RewardId DESC, UpdateTs DESC
        LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
        """)
        
        reward = self.cursor.fetchall()
        
        return reward

    def select_reward_count(self):
        self.create_reward_table()

        self.cursor.execute(f"""
        SELECT COUNT(*) FROM Reward
        """)
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def select_reward_total_pages_count(self, page_size=30):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM Reward
            """)

        total_reward = self.cursor.fetchone()[0]
        total_pages = (total_reward - 1) // page_size + 1

        return total_pages
    