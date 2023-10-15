import os, sys
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
from datetime import *

class MyLoginSchema():
    def __init__(self):
        super().__init__()
        dir_path = 'G:' + f"/My Drive/database/"
        self.db_file_path = os.path.abspath(dir_path + '/sales.db')
        os.makedirs(os.path.abspath(dir_path), exist_ok=True)

        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()


    def get_user_id(self, name, password):
        try:
            user_id = self.cursor.execute("""
                SELECT UserId FROM User
                WHERE Name = ? AND Password = ?
            """, (name, password))

            user_id = self.cursor.fetchone()[0]
        except Exception as e:
            user_id = 0
            print('User not found')
            print(e)

        return user_id