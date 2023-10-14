@echo off
cd /d "C:\Users\Janjan\Documents\GitHub\pos_system\prototype_18\src\core\"
python automatic_csv_import_alert.py

REM Wait for a few seconds (adjust as needed)
timeout /t 5

python automatic_csv_importer.py