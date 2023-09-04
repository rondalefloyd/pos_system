import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class CustomerManagementSchema():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'w
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    # CUSTOMER MANAGEMENT
    # -- for adding
    def addNewCustomer(self, customer_name, address, barrio, town, phone, age, gender, marital_status):
        self.cursor.execute('''
        INSERT INTO Customer (
            CustomerName,
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
            CustomerName = ? AND
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

    # -- for editing
    def editSelectedCustomer(self, customer_name, address, barrio, town, phone, age, gender, marital_status, customer_id):
        self.cursor.execute('''
        UPDATE Customer
        SET 
            CustomerName = ?,
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

    # -- for removing
    def removeSelectedCustomer(self, customer_id):
        self.cursor.execute('''
        DELETE FROM Customer
        WHERE CustomerId = ?
        ''', (customer_id,))
        self.conn.commit()

    # -- for populating
    def listCustomer(self, text):
        self.cursor.execute('''
        SELECT
            CustomerName,
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
            CustomerName LIKE ? OR
            Address LIKE ? OR
            Barrio LIKE ? OR
            Town LIKE ? OR
            Phone LIKE ? OR
            Age LIKE ? OR
            Gender LIKE ? OR
            MaritalStatus LIKE ?
        ORDER BY CustomerId DESC, UpdateTs DESC
                            
        ''', (
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%',
            '%' + text + '%'))
        
        customer = self.cursor.fetchall()
        
        return customer
    
    # -- for filling combo box
    def fillCustomerComboBox(self):
        self.cursor.execute('''
        SELECT DISTINCT CustomerName, Barrio, Town FROM Customer
        ORDER BY CustomerId DESC, UpdateTs DESC                
        ''')
        
        customer = self.cursor.fetchall()
        
        return customer

