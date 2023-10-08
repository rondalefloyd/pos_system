import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CustomerSchema():
    def __init__(self):
        super().__init__()
        # Creates folder for the db file
        self.db_file_path = os.path.abspath('data/sales.db')
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/')), exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

        self.create_customer_table()

    def create_customer_table(self):
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
        self.conn.commit()

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

    def add_new_customer(
        # region > params
        self,
        customer_name='',
        address='',
        barrio='',
        town='',
        phone='',
        age='',
        gender='',
        marital_status='',
        reward_name=''
        # endregion
    ):
        # region -- assign values if empty string
        customer_name = '[no data]' if customer_name == '' else customer_name
        address = '[no data]' if address == '' else address
        barrio = '[no data]' if barrio == '' else barrio
        town = '[no data]' if town == '' else town
        phone = '[no data]' if phone == '' else phone
        age = '[no data]' if age == '' else age
        gender = '[no data]' if gender == '' else gender
        marital_status = '[no data]' if marital_status == '' else marital_status
        reward_name == 'No reward' if reward_name == '' else reward_name
        # endregion -- assign values if empty string

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
        )''', (customer_name, address, barrio, town, phone, age, gender, marital_status,
              customer_name, address, barrio, town, phone, age, gender, marital_status))
        self.conn.commit()

        # NEEDS TO ADD CUSTOMER REWARD !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def edit_selected_customer(self, customer_name, address, barrio, town, phone, age, gender, marital_status, reward_name, customer_id):
        # region -- assign values if empty string
        customer_name = '[no data]' if customer_name == '' else customer_name
        address = '[no data]' if address == '' else address
        barrio = '[no data]' if barrio == '' else barrio
        town = '[no data]' if town == '' else town
        phone = '[no data]' if phone == '' else phone
        age = '[no data]' if age == '' else age
        gender = '[no data]' if gender == '' else gender
        marital_status = '[no data]' if marital_status == '' else marital_status
        # endregion -- assign values if empty string
            
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
        ''', (customer_name, address, barrio, town, phone, age, gender, marital_status, customer_id))
        self.conn.commit()

        # NEEDS TO ADD CUSTOMER REWARD !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def delete_selected_customer(self, customer_id):
        self.cursor.execute('''
        DELETE FROM Customer
        WHERE CustomerId = ?
        ''', (customer_id,))
        self.conn.commit()

    def list_customer(self, text_filter='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.create_customer_table()

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
            CASE WHEN Reward.Name IS NOT NULL THEN Reward.Name ELSE 'No reward' END AS RewardName,
            Customer.UpdateTs,

            Customer.CustomerId, -- 10
            CustomerReward.CustomerId,
            CustomerReward.RewardId

        FROM Customer
            LEFT JOIN CustomerReward ON Customer.CustomerId = CustomerReward.CustomerId
            LEFT JOIN Reward ON CustomerReward.RewardId = Reward.RewardId
        WHERE
            Customer.Name LIKE ? OR
            Customer.Address LIKE ? OR
            Customer.Barrio LIKE ? OR
            Customer.Town LIKE ? OR
            Customer.Phone LIKE ? OR
            Customer.Age LIKE ? OR
            Customer.Gender LIKE ? OR
            Customer.MaritalStatus LIKE ? OR
            Reward.Name LIKE ? OR
            Customer.UpdateTs LIKE ?
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
        
        customer = self.cursor.fetchall()
        
        return customer
    
    def list_barrio(self):
        self.cursor.execute('''
        SELECT DISTINCT Barrio FROM Customer
        ORDER BY CustomerId DESC, UpdateTs DESC                
        ''')
        
        barrio = self.cursor.fetchall()
        
        return barrio
        pass
    def list_town(self):
        self.cursor.execute('''
        SELECT DISTINCT Town FROM Customer
        ORDER BY CustomerId DESC, UpdateTs DESC                
        ''')
        
        town = self.cursor.fetchall()
        
        return town
    def list_reward(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Reward
        ORDER BY RewardId DESC, UpdateTs DESC                
        ''')
        
        reward = self.cursor.fetchall()
        
        return reward

    def count_customer(self):
        self.create_customer_table()

        self.cursor.execute('''
        SELECT COUNT(*) FROM Customer
        ''')
        count = self.cursor.fetchone()[0]
        
        return count