import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class CustomerManagementSQL():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()


    def selectAllCustomerData(self, text):
        self.cursor.execute('''
        SELECT CustomerName, Address, Barrio, Town, Phone, Age, Gender, MaritalStatus FROM Customer
        WHERE 
            CustomerName LIKE ? OR 
            Address LIKE ? OR 
            Barrio LIKE ? OR
            Town LIKE ? OR
            Phone LIKE ? OR
            Age LIKE ? OR
            Gender LIKE ? OR
            MaritalStatus LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        all_data = self.cursor.fetchall()

        return all_data

    def selectAllFilteredCustomerData(self, text):
        self.cursor.execute('''
        SELECT CustomerName, Address, Barrio, Town, Phone, Age, Gender, MaritalStatus FROM Customer
        WHERE 
            CustomerName LIKE ? OR 
            Address LIKE ? OR 
            Barrio LIKE ? OR
            Town LIKE ? OR
            Phone LIKE ? OR
            Age LIKE ? OR
            Gender LIKE ? OR
            MaritalStatus LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        all_data = self.cursor.fetchall()

        return all_data
    
    def insertCustomerData(self, customer_name, address, barrio, town, phone, age, gender, marital_status):
        self.cursor.execute('''
        INSERT INTO Customer (CustomerName, Address, Barrio, Town, Phone, Age, Gender, MaritalStatus)
        SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM Customer WHERE CustomerName = ?)
        ''', (customer_name, address, barrio, town, phone, age, gender, marital_status, customer_name))
        self.conn.commit()

    def updateCustomerData(self, customer_name, address, barrio, town, phone, age, gender, marital_status):
        self.cursor.execute('''
        UPDATE Customer 
        SET Address = ?,
            Barrio = ?,
            Town = ?,
            Phone = ?,
            Age = ?,
            Gender = ?,
            MaritalStatus = ?,
            UpdateTs =  CURRENT_TIMESTAMP                
        WHERE CustomerName = ?                                                                                                                   
        ''', (address, barrio, town, phone, age, gender, marital_status, customer_name))
        self.conn.commit()
