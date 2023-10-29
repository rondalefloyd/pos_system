import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(r'C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22')

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()

class MyCustomerSchema:
    def __init__(self):
        self.sales_file = os.path.abspath(qss.db_file_path + qss.sales_file_name)
        
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.sales_conn = sqlite3.connect(database=self.sales_file)
        self.sales_cursor = self.sales_conn.cursor()

        self.create_customer_table()

    def create_customer_table(self):
        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Customer (
                CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Address TEXT,
                Barrio DECIMAL,
                Town TEXT,            
                Phone TEXT,
                Age INTEGER,
                Gender TEXT,
                MaritalStatus TEXT,
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.sales_cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS CustomerReward (
                CustomerId INTEGER,
                RewardId INTEGER,
                Points INTEGER, 
                UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

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

    def insert_customer_data(self, customer_name='', customer_address='', customer_barrio='', customer_town='', customer_phone='', customer_age=0, customer_gender='', customer_marstat=''):
        self.sales_cursor.execute(f"""
            INSERT INTO Customer (Name, Address, Barrio, Town, Phone, Age, Gender, MaritalStatus)
            SELECT 
                "{customer_name}", 
                "{customer_address}", 
                "{customer_barrio}", 
                "{customer_town}",
                "{customer_phone}",
                {customer_age},
                "{customer_gender}",
                "{customer_marstat}"
            WHERE NOT EXISTS (
                SELECT 1 FROM Customer
                WHERE
                    Name = "{customer_name}" AND
                    Address = "{customer_address}" AND
                    Barrio = "{customer_barrio}" AND
                    Town = "{customer_town}" AND
                    Phone = "{customer_phone}" AND
                    Age = {customer_age} AND
                    Gender = "{customer_gender}" AND
                    MaritalStatus = "{customer_marstat}"
            )
        """)

        customer_id = self.select_customer_id(
            customer_name,
            customer_town,
            customer_phone,
            customer_age
        )

        self.sales_cursor.execute(f"""
            INSERT INTO CustomerReward (CustomerId, RewardId, Points)
            SELECT
                {customer_id}, 0, 0
            WHERE NOT EXISTS (
                SELECT 1 FROM CustomerReward
                WHERE
                    CustomerId = {customer_id} AND
                    RewardId = 0 AND
                    Points = 0
            )
        """)

        self.sales_conn.commit()

    def select_data_as_display(self, text='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
            SELECT 
                Customer.Name, 
                Customer.Address, 
                Customer.Barrio, 
                Customer.Town,
                Customer.Phone,
                Customer.Age,
                Customer.Gender,
                Customer.MaritalStatus,
                CustomerReward.Points,
                Customer.UpdateTs
            FROM Customer
            LEFT JOIN CustomerReward ON Customer.CustomerId = CustomerReward.CustomerId
            LEFT JOIN Reward ON CustomerReward.RewardId = Reward.RewardId
            WHERE
                Customer.Name LIKE '%{text}%' OR
                Customer.Address LIKE '%{text}%' OR
                Customer.Barrio LIKE '%{text}%' OR
                Customer.Town LIKE '%{text}%' OR
                Customer.Phone LIKE '%{text}%' OR
                Customer.Age LIKE '%{text}%' OR
                Customer.Gender LIKE '%{text}%' OR
                Customer.MaritalStatus LIKE '%{text}%'
            ORDER BY Customer.CustomerId DESC, Customer.UpdateTs DESC
            LIMIT {page_size}
            OFFSET {offset}
        """)

        customer_data = self.sales_cursor.fetchall()

        return customer_data
        pass
    def select_customer_data(self, customer_name='', customer_town='', customer_phone='', customer_age=0):
        self.sales_cursor.execute(f"""
            SELECT
                Customer.Name, 
                Customer.Address, 
                Customer.Barrio, 
                Customer.Town,
                Customer.Phone,
                Customer.Age,
                Customer.Gender,
                Customer.MaritalStatus,
                CustomerReward.Points,
                Customer.CustomerId
            FROM Customer
            LEFT JOIN CustomerReward ON Customer.CustomerId = CustomerReward.CustomerId
            LEFT JOIN Reward ON CustomerReward.RewardId = Reward.RewardId
            WHERE
                Customer.Name = "{customer_name}" AND
                Customer.Town = "{customer_town}" AND
                Customer.Phone = "{customer_phone}" AND
                Customer.Age = {customer_age}
            ORDER BY Customer.CustomerId DESC, Customer.UpdateTs DESC
        """)

        customer_data = self.sales_cursor.fetchall()

        return customer_data
    def select_customer_data_total_page_count(self, text='', page_size=30):
        self.sales_cursor.execute(f"""
            SELECT COUNT(*) FROM Customer
            WHERE
                Customer.Name LIKE '%{text}%' OR
                Customer.Address LIKE '%{text}%' OR
                Customer.Barrio LIKE '%{text}%' OR
                Customer.Town LIKE '%{text}%' OR
                Customer.Phone LIKE '%{text}%' OR
                Customer.Age LIKE '%{text}%' OR
                Customer.Gender LIKE '%{text}%' OR
                Customer.MaritalStatus LIKE '%{text}%'
            """)

        total_customer_data_count = self.sales_cursor.fetchone()[0]
        total_page_count = (total_customer_data_count - 1) // page_size + 1

        return total_page_count
        pass
    def select_customer_barrio_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT Barrio FROM Customer
            ORDER BY CustomerId DESC, UpdateTs DESC
        """)

        customer_barrio = self.sales_cursor.fetchall()

        return customer_barrio
        pass
    def select_customer_town_for_combo_box(self):
        self.sales_cursor.execute(f"""
            SELECT Town FROM Customer
            ORDER BY CustomerId DESC, UpdateTs DESC
        """)

        customer_town = self.sales_cursor.fetchall()

        return customer_town
        pass

    def select_customer_id(self, customer_name, customer_town, customer_phone, customer_age):
        customer_id = self.sales_cursor.execute(f"""
            SELECT CustomerId FROM Customer
            WHERE
                Name = "{customer_name}" AND
                Town = "{customer_town}" AND
                Phone = "{customer_phone}" AND
                Age = {customer_age}
        """)

        customer_id = self.sales_cursor.fetchone()[0]

        return customer_id

    def update_customer_data(
            self, 
            customer_name='', 
            customer_address='', 
            customer_barrio='', 
            customer_town='', 
            customer_phone='', 
            customer_age=0, 
            customer_gender='', 
            customer_marstat='', 
            customer_points=0, 
            customer_id=0
    ):
        self.sales_cursor.execute(f"""
            UPDATE Customer
            SET
                Name = "{customer_name}",
                Address = "{customer_address}",
                Barrio = "{customer_barrio}",
                Town = "{customer_town}",
                Phone = "{customer_phone}",
                Age = {customer_age},
                Gender = "{customer_gender}",
                MaritalStatus = "{customer_marstat}"
            WHERE CustomerId = {customer_id}
        """)

        self.sales_cursor.execute(f"""
            UPDATE CustomerReward
            SET Points = {customer_points}
            WHERE CustomerId = {customer_id}
        """)  

        self.sales_conn.commit()

    def delete_customer_data(self, customer_id=0):
        self.sales_cursor.execute(f"""
            DELETE FROM Customer
            WHERE CustomerId = {customer_id}
        """)

        self.sales_conn.commit()
