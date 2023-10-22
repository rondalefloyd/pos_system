import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

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

        self.sales_conn.commit()

    def insert_customer_data(self, customer_name='', customer_address='', customer_barrio='', customer_town='', customer_phone='', customer_age=0, customer_gender='', customer_marstat=''):
        self.sales_cursor.execute(f"""
            INSERT INTO Customer (Name, Address, Barrio, Town, Phone, Age, Gender, MaritalStatus)
            SELECT 
                '{customer_name}', 
                '{customer_address}', 
                '{customer_barrio}', 
                '{customer_town}',
                '{customer_phone}',
                '{customer_age}',
                '{customer_gender}',
                '{customer_marstat}'
            WHERE NOT EXISTS (
                SELECT 1 FROM Customer
                WHERE
                    Name = '{customer_name}' AND
                    Address = '{customer_address}' AND
                    Barrio = '{customer_barrio}' AND
                    Town = '{customer_town}' AND
                    Phone = '{customer_phone}' AND
                    Age = '{customer_age}' AND
                    Gender = '{customer_gender}' AND
                    MaritalStatus = '{customer_marstat}'
            )
        """)

        self.sales_conn.commit()

    def select_data_as_display(self, text='', page_number=1, page_size=30):
        offset = (page_number - 1) * page_size

        self.sales_cursor.execute(f"""
            SELECT 
                Name, 
                Address, 
                Barrio, 
                Town,
                Phone,
                Age,
                Gender,
                MaritalStatus,
                UpdateTs
            FROM Customer
            WHERE
                Name LIKE '%{text}%' OR
                Address LIKE '%{text}%' OR
                Barrio LIKE '%{text}%' OR
                Town LIKE '%{text}%' OR
                Phone LIKE '%{text}%' OR
                Age LIKE '%{text}%' OR
                Gender LIKE '%{text}%' OR
                MaritalStatus LIKE '%{text}%'
            ORDER BY CustomerId DESC, UpdateTs DESC
            LIMIT {page_size}
            OFFSET {offset}
        """)

        customer_data = self.sales_cursor.fetchall()

        return customer_data
        pass
    def select_customer_data(self, customer_name='', customer_town='', customer_phone='', customer_age=0):
        self.sales_cursor.execute(f"""
            SELECT
                Name, 
                Address, 
                Barrio, 
                Town,
                Phone,
                Age,
                Gender,
                MaritalStatus,
                CustomerId
            FROM Customer
            WHERE
                Name = '{customer_name}' AND
                Town = '{customer_town}' AND
                Phone = '{customer_phone}' AND
                Age = '{customer_age}'
            ORDER BY CustomerId DESC, UpdateTs DESC
        """)

        customer_data = self.sales_cursor.fetchall()

        return customer_data
    def select_customer_data_total_page_count(self, page_size=30):
        self.sales_cursor.execute(f"SELECT COUNT(*) FROM Customer")

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

    def update_customer_data(self, customer_name='', customer_address='', customer_barrio='', customer_town='', customer_phone='', customer_age=0, customer_gender='', customer_marstat='', customer_id=0):
        self.sales_cursor.execute(f"""
            UPDATE Customer
            SET
                Name = '{customer_name}',
                Address = '{customer_address}',
                Barrio = '{customer_barrio}',
                Town = '{customer_town}',
                Phone = '{customer_phone}',
                Age = '{customer_age}',
                Gender = '{customer_gender}',
                MaritalStatus = '{customer_marstat}'
            WHERE CustomerId = {customer_id}
        """)

        self.sales_conn.commit()

    def delete_customer_data(self, customer_id=0):
        self.sales_cursor.execute(f"""
            DELETE FROM Customer
            WHERE CustomerId = {customer_id}
        """)

        self.sales_conn.commit()
