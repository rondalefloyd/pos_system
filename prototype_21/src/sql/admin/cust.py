import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyCustSchema():
    def __init__(self):
        super().__init__()

        self.setup_sales_conn()

        self.create_cust_table()

    def setup_sales_conn(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.sales_file)
        self.cursor = self.conn.cursor()

    def create_cust_table(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Address TEXT,
            Barrio TEXT,
            Town TEXT,
            Phone TEXT,
            Age INTEGER,
            Gender TEXT,
            MaritalStatus TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS CustomerReward (
            CustomerId INTEGER,
            RewardId INTEGER,
            Points INTEGER,  
            CurrencyAmount FLOAT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

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

    def insert_new_cust_data(self, cust_name='', cust_address='', cust_barrio='', cust_town='', cust_phone=0, cust_age=0, cust_gender='', cust_marital_status='', cust_points=0):
        self.cursor.execute(f"""
        INSERT INTO Customer (
            Name,
            Address,
            Barrio,
            Town,
            Phone,
            Age,
            Gender,
            MaritalStatus
        )
        SELECT 
            '{cust_name}', 
            '{cust_address}', 
            '{cust_barrio}', 
            '{cust_town}', 
            {cust_phone}, 
            {cust_age}, 
            '{cust_gender}', 
            '{cust_marital_status}'
        WHERE NOT EXISTS(
            SELECT 1 FROM Customer
            WHERE
                Name = '{cust_name}' AND
                Address = '{cust_address}' AND
                Barrio = '{cust_barrio}' AND
                Town = '{cust_town}' AND
                Phone = {cust_phone} AND
                Age = {cust_age} AND
                Gender = '{cust_gender}' AND
                MaritalStatus = '{cust_marital_status}'
            )
        """)

        cust_id = self.select_cust_id(cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status)

        self.insert_new_cust_reward_data(cust_points, cust_id)

        self.conn.commit()
        pass
    def insert_new_cust_reward_data(self, cust_points, cust_id):
        self.cursor.execute(f"""
        INSERT INTO CustomerReward (CustomerId, Points)
        SELECT {cust_id}, {cust_points}
        WHERE NOT EXISTS(
            SELECT 1 FROM CustomerReward
            WHERE
                CustomerId = {cust_id} AND
                Points = {cust_points}
            )
        """)
        self.conn.commit()


    def update_selected_cust_data(self, cust_name='', cust_address='', cust_barrio='', cust_town='', cust_phone=0, cust_age=0, cust_gender='', cust_marital_status='', cust_points=0, cust_id=0):
        self.cursor.execute(f"""
        UPDATE Customer
        SET 
            Name = '{cust_name}' AND
            Address = '{cust_address}' AND
            Barrio = '{cust_barrio}' AND
            Town = '{cust_town}' AND
            Phone = {cust_phone} AND
            Age = {cust_age} AND
            Gender = '{cust_gender}' AND
            MaritalStatus = '{cust_marital_status}'
        WHERE CustomerId = {cust_id}
        """)

        self.cursor.execute(f"""
        UPDATE CustomerReward
        SET Points = {cust_points}
        WHERE CustomerId = {cust_id}
        """)
        self.conn.commit()
        pass
    def delete_selected_cust_data(self, cust_id, reward_id=0):
        self.cursor.execute(f"""
        DELETE FROM Customer
        WHERE CustomerId = {cust_id}
        """)
        self.conn.commit()

        self.cursor.execute(f"""
        DELETE FROM CustomerReward
        WHERE CustomerId = {cust_id} AND RewardId = {reward_id}
        """)
        self.conn.commit()

    def select_cust_data(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.cursor.execute(f"""
        SELECT 
            COALESCE(NULLIF(Customer.Name, ''), '[no data]') AS CustomerName,
            COALESCE(NULLIF(Customer.Address, ''), '[no data]') AS Address,
            COALESCE(NULLIF(Customer.Barrio, ''), '[no data]') AS Barrio,
            COALESCE(NULLIF(Customer.Town, ''), '[no data]') AS Town,
            COALESCE(NULLIF(Customer.Phone, ''), '[no data]') AS Phone,
            COALESCE(NULLIF(Customer.Age, ''), '[no data]') AS Age,
            COALESCE(NULLIF(Customer.Gender, ''), '[no data]') AS Gender,
            COALESCE(NULLIF(Customer.MaritalStatus, ''), '[no data]') AS MaritalStatus,
            COALESCE(NULLIF(CustomerReward.Points, ''), 0) AS CustomerRewardPoints,
            Customer.UpdateTs AS DateTimeCreated,

            Customer.CustomerId, -- 10
            CustomerReward.RewardId

        FROM Customer
            LEFT JOIN CustomerReward ON Customer.CustomerId = CustomerReward.CustomerId
            LEFT JOIN Reward ON CustomerReward.RewardId = Reward.RewardId
        WHERE
            CustomerName LIKE '%{text_filter}%' OR
            Address LIKE '%{text_filter}%' OR
            Barrio LIKE '%{text_filter}%' OR
            Town LIKE '%{text_filter}%' OR
            Phone LIKE '%{text_filter}%' OR
            Age LIKE '%{text_filter}%' OR
            Gender LIKE '%{text_filter}%' OR
            MaritalStatus LIKE '%{text_filter}%' OR
            CustomerRewardPoints LIKE '%{text_filter}%' OR
            DateTimeCreated LIKE '%{text_filter}%'
        ORDER BY Customer.CustomerId DESC, Customer.UpdateTs DESC
        LIMIT {page_size} OFFSET {offset}  -- Apply pagination limits and offsets
        """)
        
        cust = self.cursor.fetchall()
        
        return cust
        pass
    def select_barrio(self):
        self.cursor.execute(f"""
        SELECT DISTINCT Barrio FROM Customer
        ORDER BY CustomerId DESC, UpdateTs DESC                
        """)
        
        barrio = self.cursor.fetchall()
        
        return barrio
        pass
    def select_town(self):
        self.cursor.execute(f"""
        SELECT DISTINCT Town FROM Customer
        ORDER BY CustomerId DESC, UpdateTs DESC                
        """)
        
        town = self.cursor.fetchall()
        
        return town
        pass
    def select_reward(self):
        self.cursor.execute(f"""
        SELECT DISTINCT Name FROM Reward
        ORDER BY RewardId DESC, UpdateTs DESC                
        """)
        
        reward = self.cursor.fetchall()
        
        return reward
    def select_cust_id(self, cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status):
        try: 
            cust_id = self.cursor.execute(f"""
            SELECT CustomerId FROM Customer
            WHERE 
                Name = '{cust_name}' AND
                Address = '{cust_address}' AND
                Barrio = '{cust_barrio}' AND
                Town = '{cust_town}' AND
                Phone = {cust_phone} AND
                Age = {cust_age} AND
                Gender = '{cust_gender}' AND
                MaritalStatus = '{cust_marital_status}'
            """)
            cust_id = self.cursor.fetchone()[0]
            pass
        except Exception as e:
            cust_id = 0

        return cust_id
    
    def select_cust_count(self):
        self.cursor.execute(f"""
        SELECT COUNT(*) FROM Customer
        """)
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def select_cust_count_total_pages(self, page_size=30):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM Customer
            """)

        total_cust = self.cursor.fetchone()[0]
        total_pages = (total_cust - 1) // page_size + 1

        return total_pages
    