import sys, os
import subprocess
import pandas as pd
import shutil
import gspread
import pandas as pd
import traceback
import inspect
import textwrap
import urllib.request
from typing import *
from datetime import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

cwd = os.getcwd() # get current working dir
sys.path.append(os.path.join(cwd))

try:
    from src.gui.login.login import *
    from src.gui.login.updater import *
except:
    from _internal.src.gui.login.login import *
    from _internal.src.gui.login.updater import *


app = QApplication(sys.argv)

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
    with open(f"main_error_log.txt", 'a') as file: 
        file.write(error_layout)

def create_req_folders():
    base_dir = 'G:/My Drive/'
    folders = ['csv', 'dashboard', 'live_db', 'receipt/saved', 'sito']

    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder}' created.")
        else:
            print(f"Folder '{folder}' already exists.")

def create_sito_form():
    try:
        shutil.copyfile(os.path.join(cwd,'template','sito','pos_entry_form_2023.html'), 'G:/My Drive/sito/pos_entry_form_2023.html')
    except:
        shutil.copyfile(os.path.join(cwd,'_internal','pos_entry_form_2023.html'), 'G:/My Drive/sito/pos_entry_form_2023.html')

def export_gsheet_as_csv():
    try:
        file_path = os.path.join(cwd,'src','core','smpos-403608-aa14a49badc1.json')

        google_console = gspread.service_account(filename=file_path)
        spreadsheet = google_console.open_by_url('https://docs.google.com/spreadsheets/d/1v7EvAov0Pwcly5j824NgAt141SnSt9Xh1jEL0FN_WNA/edit#gid=0')
        worksheet = spreadsheet.get_worksheet(0) 
        data = worksheet.get_all_records()

        data_frame = pd.DataFrame(data)
        data_frame.to_csv('G:/My Drive/csv/product.csv', index=False)
    except Exception as error_exception:
        error_tracer(error_exception)
    pass
def run_pos_app():
    try:
        open('app_running.flag', 'w').close()

        updater_window = MyUpdaterWindow()
        updater_window.run()
        app.exec()
        
        while True:
            login_window = MyLoginWindow()
            login_window.run()
            app.exec()

            print('info::', login_window.c.user_id, login_window.c.user_name, login_window.c.user_password, login_window.c.user_phone, login_window.c.user_level)

            if login_window.c.user_id > 0 and login_window.c.user_level <= 2:
                login_window.v.close()

                cashier_window = MyCashierWindow(
                    str(login_window.c.user_name),
                    str(login_window.c.user_password),
                    str(login_window.c.user_phone),
                    int(login_window.c.user_level)
                )
                cashier_window.run()

                app.exec()

                if not os.path.exists('app_running.flag'): break

                pass
            elif login_window.c.user_id > 0 and login_window.c.user_level == 3:
                login_window.v.close()

                admin_window = MyAdminWindow(
                    str(login_window.c.user_name),
                    str(login_window.c.user_password),
                    str(login_window.c.user_phone),
                    int(login_window.c.user_level)
                )
                admin_window.run()

                app.exec()

                if not os.path.exists('app_running.flag'): break


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

def is_connected():
    try:
        urllib.request.urlopen('http://google.com', timeout=1)
        
        create_sito_form()
        create_req_folders()
        export_gsheet_as_csv()
        run_pos_app()
        copy_live_db_to_reports_db()

    except urllib.request.URLError:
        confirm_a = QMessageBox.warning(None, 'Confirm', 'Continue internet connection?.', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm_a is QMessageBox.StandardButton.Yes:
            confirm_b = QMessageBox.warning(None, 'Confirm', 'The database might not be updated. Proceed?.', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm_b is QMessageBox.StandardButton.Yes:
                create_sito_form()
                create_req_folders()
                export_gsheet_as_csv()
                run_pos_app()
                copy_live_db_to_reports_db()
            else:
                sys.exit()
        elif QMessageBox.StandardButton.No:
            sys.exit()


        

is_connected()
