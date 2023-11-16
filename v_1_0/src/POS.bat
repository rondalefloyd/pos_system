@echo off
setlocal enabledelayedexpansion

:: Add a 30 seconds delay
timeout /t 30

:: Get IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4 Address"') do (
    set ip=%%a
    set ip=!ip:~1!
)

:: Set directory path
set "dirPath=G:\My Drive\ip"
set "fileName=desktop_1.txt"

:: Create directory if it doesn't exist
if not exist "%dirPath%" mkdir "%dirPath%"

:: Delete existing desktop_1.txt file if it exists
if exist "%dirPath%\%fileName%" del "%dirPath%\%fileName%"

:: Create new desktop_1.txt file with the IP address
echo %ip% > "%dirPath%\%fileName%"

echo IP address has been saved to "%dirPath%\%fileName%"

:: Change directory
cd C:\Users\feebee store\Documents\GitHub\pos_system\prototype_22\src\

:: Run python script
python main.py

exit /b
