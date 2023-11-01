import sys, os
import subprocess
import shutil
import gspread
import pandas as pd
import traceback
import inspect
import textwrap
from datetime import *
from PyQt6.QtCore import *

def error_tracer(error_exception):
    error_traceback = traceback.format_exc().splitlines()[-1]
    error_line_number = inspect.currentframe().f_lineno
    timestamp = datetime.today().strftime("%a-%b-%d-%Y-%I:%M%p")
    error_layout = textwrap.dedent(f"""\
        TIME_STAMP: {timestamp}, 
        ERROR_LINE_NO: {error_line_number}, 
        EXCEPTION: {error_exception}, 
        ERROR_TRACEBACK: {error_traceback}

    """)
    with open(f"main_{date.today()}_error_log.txt", 'a') as file: 
        file.write(error_layout)

def export_gsheet_as_csv():
    try:
        file_path = r"C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22/src/core/smpos-403608-aa14a49badc1.json"

        google_console = gspread.service_account(filename=file_path)
        spreadsheet = google_console.open('test_product_list')
        worksheet = spreadsheet.get_worksheet(0) 
        data = worksheet.get_all_records()

        data_frame = pd.DataFrame(data)
        data_frame.to_csv('G:/My Drive/csv/product.csv', index=False)
    except Exception as error_exception:
        error_tracer(error_exception)
    pass
def run_pos_app():
    try:
        subprocess.run(['python', '-Xfrozen_modules=off', 'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22/src/gui/login/updater.py']) # for loading database

        open('app_running.flag', 'w').close()
        while True:
            login = subprocess.run(['python', '-Xfrozen_modules=off', 'C:/Users/feebee store/Documents/GitHub/pos_system/prototype_22/src/gui/login/login.py'])

            if not os.path.exists('login_running.flag') and not os.path.exists('app_running.flag'):
                break

            print('login:', login)
    except Exception as error_exception:
        error_tracer(error_exception)
    pass
def copy_live_db_to_reports_db():
    try:
        shutil.copyfile('G:/My Drive/live_db/sales.db', 'G:/My Drive/reports_db/sales.db')
        shutil.copyfile('G:/My Drive/live_db/txn.db', 'G:/My Drive/reports_db/txn.db')
        shutil.copyfile('G:/My Drive/live_db/syslib.db', 'G:/My Drive/reports_db/syslib.db')
        shutil.copyfile('G:/My Drive/live_db/accounts.db', 'G:/My Drive/reports_db/accounts.db')
    except Exception as error_exception:
        error_tracer(error_exception)
    pass

# export_gsheet_as_csv()
run_pos_app()
copy_live_db_to_reports_db()