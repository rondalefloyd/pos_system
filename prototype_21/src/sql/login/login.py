import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

sys.path.append(os.path.abspath(''))

from templates.qss.qss_config import *

qss = QSSConfig()

class MyLoginSchema():
    def __init__(self):
        super().__init__()
        self.accounts_file_path = os.path.abspath(qss.db_file_path + qss.accounts_file_name)
        os.makedirs(os.path.abspath(qss.db_file_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.accounts_file_path)
        self.cursor = self.conn.cursor()

    def get_user_id(self, name, password):
        try:
            user_id = self.cursor.execute("""
                SELECT UserId FROM User
                WHERE Name = ? AND Password = ?
            """, (name, password))

            user_id = self.cursor.fetchone()[0]
            pass
        except Exception as e:
            user_id = 0

        return user_id
    
    def get_user_data(self, user_id):
        try:
            user_data = self.cursor.execute("""
                SELECT Name, Password, AccessLevel, Phone FROM User
                WHERE UserId = ?
            """, (user_id,))

            user_data = self.cursor.fetchone()
            pass
        except Exception as e:
            user_data = []

        return user_data