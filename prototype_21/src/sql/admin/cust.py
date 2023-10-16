import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyCustSchema():
    def __init__(self):
        super().__init__()

        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.sales_file)
        self.cursor = self.conn.cursor()

        self.create_cust_table()

    def create_cust_table(self):
        self.cursor.execute('''
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
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS CustomerReward (
            CustomerId INTEGER,
            RewardId INTEGER,
            Points INTEGER,  
            CurrencyAmount FLOAT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

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

    def add_new_cust(self, cust_name='', cust_address='', cust_barrio='', cust_town='', cust_phone='', cust_age='', cust_gender='', cust_marital_status='', cust_points=''):
        cust_name = '[no data]' if cust_name == '' else cust_name
        cust_address = '[no data]' if cust_address == '' else cust_address
        cust_barrio = '[no data]' if cust_barrio == '' else cust_barrio
        cust_town = '[no data]' if cust_town == '' else cust_town
        cust_phone = '[no data]' if cust_phone == '' else cust_phone
        cust_age = '[no data]' if cust_age == '' else cust_age
        cust_gender = '[no data]' if cust_gender == '' else cust_gender
        cust_marital_status = '[no data]' if cust_marital_status == '' else cust_marital_status
        cust_points == 0 if cust_points == '' else cust_points

        self.cursor.execute('''
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
        SELECT ?, ?, ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Customer
        WHERE
            Name = ? AND
            Address = ? AND
            Barrio = ? AND
            Town = ? AND
            Phone = ? AND
            Age = ? AND
            Gender = ? AND
            MaritalStatus = ?
        )''', (cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status,
              cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status))

        cust_id = self.cursor.execute('''
        SELECT CustomerId FROM Customer
        WHERE 
            Name = ? AND
            Address = ? AND
            Barrio = ? AND
            Town = ? AND
            Phone = ? AND
            Age = ? AND
            Gender = ? AND
            MaritalStatus = ?
        ''', (cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status))
        cust_id = self.cursor.fetchone()[0]

        self.cursor.execute('''
        INSERT INTO CustomerReward (CustomerId, Points)
        SELECT ?, ?
        WHERE NOT EXISTS(
            SELECT 1 FROM CustomerReward
            WHERE
                CustomerId = ? AND
                Points = ?
        )''', (cust_id, cust_points,
              cust_id, cust_points))
        self.conn.commit()
        pass
    def edit_selected_cust(self, cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status, cust_points, cust_id, reward_id):
        cust_name = '[no data]' if cust_name == '' else cust_name
        cust_address = '[no data]' if cust_address == '' else cust_address
        cust_barrio = '[no data]' if cust_barrio == '' else cust_barrio
        cust_town = '[no data]' if cust_town == '' else cust_town
        cust_phone = '[no data]' if cust_phone == '' else cust_phone
        cust_age = '[no data]' if cust_age == '' else cust_age
        cust_gender = '[no data]' if cust_gender == '' else cust_gender
        cust_marital_status = '[no data]' if cust_marital_status == '' else cust_marital_status
        cust_points == 0 if cust_points == '' else cust_points

        self.cursor.execute('''
        UPDATE Customer
        SET 
            Name = ?,
            Address = ?,
            Barrio = ?,
            Town = ?,
            Phone = ?,
            Age = ?,
            Gender = ?,
            MaritalStatus = ?
        WHERE CustomerId = ?
        ''', (cust_name, cust_address, cust_barrio, cust_town, cust_phone, cust_age, cust_gender, cust_marital_status, cust_id))

        self.cursor.execute('''
        UPDATE CustomerReward
        SET Points = ?
        WHERE CustomerId = ?
        ''', (cust_points, cust_id))
        self.conn.commit()
        pass
    def delete_selected_cust(self, cust_id, reward_id):
        self.cursor.execute('''
        DELETE FROM Customer
        WHERE CustomerId = ?
        ''', (cust_id,))
        self.conn.commit()

        self.cursor.execute('''
        DELETE FROM CustomerReward
        WHERE CustomerId = ? AND RewardId = ?
        ''', (cust_id, reward_id))
        self.conn.commit()

    def list_all_cust_col(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.cursor.execute('''
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
            CustomerName LIKE ? OR
            Address LIKE ? OR
            Barrio LIKE ? OR
            Town LIKE ? OR
            Phone LIKE ? OR
            Age LIKE ? OR
            Gender LIKE ? OR
            MaritalStatus LIKE ? OR
            CustomerRewardPoints LIKE ? OR
            DateTimeCreated LIKE ?
        ORDER BY Customer.CustomerId DESC, Customer.UpdateTs DESC
        LIMIT ? OFFSET ?  -- Apply pagination limits and offsets
        ''', (
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            '%' + str(text_filter) + '%',
            page_size,  # Limit
            offset     # Offset
        ))
        
        cust = self.cursor.fetchall()
        
        return cust
    def list_barrio_col(self):
        self.cursor.execute('''
        SELECT DISTINCT Barrio FROM Customer
        ORDER BY CustomerId DESC, UpdateTs DESC                
        ''')
        
        barrio = self.cursor.fetchall()
        
        return barrio
        pass
    def list_town_col(self):
        self.cursor.execute('''
        SELECT DISTINCT Town FROM Customer
        ORDER BY CustomerId DESC, UpdateTs DESC                
        ''')
        
        town = self.cursor.fetchall()
        
        return town
    def list_reward_col(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Reward
        ORDER BY RewardId DESC, UpdateTs DESC                
        ''')
        
        reward = self.cursor.fetchall()
        
        return reward

    def count_all_cust(self):
        self.cursor.execute('''
        SELECT COUNT(*) FROM Customer
        ''')
        count = self.cursor.fetchone()[0]
        
        return count
        pass
    def count_cust_list_total_pages(self, page_size=30):
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM Customer
            ''')

        total_cust = self.cursor.fetchone()[0]
        total_pages = (total_cust - 1) // page_size + 1

        return total_pages
    