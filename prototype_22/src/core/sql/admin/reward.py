import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyRewardSchema:
    def __init__(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.sales_conn = sqlite3.connect(database=self.sales_file)
        self.sales_cursor = self.sales_conn.cursor()

        self.create_reward_table()

    def create_reward_table(self):
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Reward (
                RewardId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Unit DECIMAL,
                Points DECIMAL,
                Description TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.sales_conn.commit()

    def insert_reward_data(self, reward_name='', reward_unit=0, reward_points=0, reward_desc=''):
        self.sales_cursor.execute(f"""
            INSERT INTO Reward (Name, Unit, Points, Description)
            SELECT 
                "{reward_name}", 
                '{reward_unit}', 
                {reward_points}, 
                '{reward_desc}'
            WHERE NOT EXISTS (
                SELECT 1 FROM Reward
                WHERE
                    Name = "{reward_name}" AND
                    Unit = '{reward_unit}' AND
                    Points = {reward_points} AND
                    Description = '{reward_desc}'
            )
        """)

        self.sales_conn.commit()

    def select_data_as_display(self, text='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
            SELECT 
                Name, 
                Unit, 
                Points, 
                Description,
                UpdateTs
            FROM Reward
            WHERE
                Name LIKE '%{text}%' OR
                Unit LIKE '%{text}%' OR
                Points LIKE '%{text}%' OR
                Description LIKE '%{text}%'
            ORDER BY RewardId DESC, UpdateTs DESC
            LIMIT {page_size}
            OFFSET {offset}
        """)

        reward_data = self.sales_cursor.fetchall()

        return reward_data
        pass
    def select_reward_data(self, reward_name='', reward_unit=0):
        self.sales_cursor.execute(f"""
            SELECT
                Name, 
                Unit, 
                Points, 
                Description,
                RewardId
            FROM Reward
            WHERE
                Name = "{reward_name}" AND
                Unit = '{reward_unit}'
            ORDER BY RewardId DESC, UpdateTs DESC
        """)

        reward_data = self.sales_cursor.fetchall()

        return reward_data
    def select_reward_data_total_page_count(self, text='', page_size=30):
        self.sales_cursor.execute(f"""
            SELECT COUNT(*) FROM Reward
            WHERE
                Name LIKE '%{text}%' OR
                Unit LIKE '%{text}%' OR
                Points LIKE '%{text}%' OR
                Description LIKE '%{text}%'
        """)

        total_reward_data_count = self.sales_cursor.fetchone()[0]
        total_page_count = (total_reward_data_count - 1) // page_size + 1

        return total_page_count
    def select_reward_unit_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT Unit FROM Reward
            ORDER BY RewardId DESC, UpdateTs DESC
        """)

        reward_unit = self.sales_cursor.fetchall()

        return reward_unit

    def update_reward_data(self, reward_name='', reward_unit=0, reward_points=0, reward_desc='', reward_id=0):
        self.sales_cursor.execute(f"""
            UPDATE Reward
            SET
                Name = "{reward_name}",
                Unit = '{reward_unit}',
                Points = {reward_points},
                Description = '{reward_desc}'
            WHERE RewardId = {reward_id}
        """)

        self.sales_conn.commit()

    def delete_reward_data(self, reward_id=0):
        self.sales_cursor.execute(f"""
            DELETE FROM Reward
            WHERE RewardId = {reward_id}
        """)

        self.sales_conn.commit()
