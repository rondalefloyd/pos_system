@echo off
setlocal enabledelayedexpansion

:: Add a 30 seconds delay
timeout /t 30


:: Change directory
cd %USERPROFILE%\Documents\GitHub\pos_system\v_1_0

:: Run python script
python main.py

exit /b
