import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os, sys

sys.path.append(os.path.abspath(''))

from template.qss.qss import MyQSSConfig

qss = MyQSSConfig()


class MySysLibSchema:
	def __init__(self):
		self.syslib_file = os.path.abspath(qss.db_file_path + qss.syslib_file_name)
		self.syslib_conn = sqlite3.connect(database=self.syslib_file)
		self.syslib_cursor = self.syslib_conn.cursor()
		
	def run(self):
		self.syslib_cursor.execute('''
			DROP TABLE IF EXISTS Calendar;
			''')
		self.syslib_conn.commit()

		self.syslib_cursor.execute('''
			CREATE TABLE IF NOT EXISTS Calendar (
				DateId INTEGER PRIMARY KEY AUTOINCREMENT,
				DateValue date UNIQUE NOT NULL,
				Dayofweek INT NOT NULL,
				Weekday TEXT NOT NULL,
				Quarter INT NOT NULL,
				Year INT NOT NULL,
				Month INT NOT NULL,
				MonthName TEXT NOT NULL,
				Day INT NOT NULL,
				IsHoliday BIT DEFAULT 0
				);
			''')
		self.syslib_conn.commit()

		self.syslib_cursor.execute('''
			INSERT OR ignore INTO Calendar (DateValue, dayofweek, weekday, quarter, year, month, monthname, day)
			SELECT *
			FROM (
			WITH RECURSIVE dates(DateValue) AS (
				VALUES('1980-01-01')
				UNION ALL
				SELECT date(DateValue, '+1 day')
				FROM dates
				WHERE DateValue < '3000-01-01'
			)
			SELECT DateValue,
				(CAST(strftime('%w', DateValue) AS INT) + 6) % 7 AS dayofweek,
				CASE
					(CAST(strftime('%w', DateValue) AS INT) + 6) % 7
					WHEN 0 THEN 'Monday'
					WHEN 1 THEN 'Tuesday'
					WHEN 2 THEN 'Wednesday'
					WHEN 3 THEN 'Thursday'
					WHEN 4 THEN 'Friday'
					WHEN 5 THEN 'Saturday'
					ELSE 'Sunday'
				END AS weekday,
				CASE
					WHEN CAST(strftime('%m', DateValue) AS INT) BETWEEN 1 AND 3 THEN 1
					WHEN CAST(strftime('%m', DateValue) AS INT) BETWEEN 4 AND 6 THEN 2
					WHEN CAST(strftime('%m', DateValue) AS INT) BETWEEN 7 AND 9 THEN 3
					ELSE 4
				END AS quarter,
				CAST(strftime('%Y', DateValue) AS INT) AS year,
				CAST(strftime('%m', DateValue) AS INT) AS month,
				CASE
					WHEN CAST(strftime('%m', DateValue) AS INT) = 1 THEN 'Jan'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 2 THEN 'Feb'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 3 THEN 'Mar'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 4 THEN 'Apr'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 5 THEN 'May'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 6 THEN 'Jun'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 7 THEN 'Jul'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 8 THEN 'Aug'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 9 THEN 'Sep'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 10 THEN 'Oct'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 11 THEN 'Nov'
					WHEN CAST(strftime('%m', DateValue) AS INT) = 12 THEN 'Dec'         
				END AS monthname,
				CAST(strftime('%d', DateValue) AS INT) AS day
			FROM dates
			);
			''')
		self.syslib_conn.commit()


		self.syslib_cursor.execute('''
			UPDATE calendar
			SET IsHoliday = 1
				WHERE   
					(month = 1 and day = 1) OR
					(month = 11 and day between 29 and 30) OR
					(month = 12 and day between 24 and 31);   
			''')
		self.syslib_conn.commit()