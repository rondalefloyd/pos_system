import sys, os
import subprocess
from PyQt6.QtCore import *


subprocess.run(['python', '-Xfrozen_modules=off', 'C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/src/gui/login/updater.py'])

open('app_running.flag', 'w').close()
while True:
    login = subprocess.run(['python', '-Xfrozen_modules=off', 'C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/src/gui/login/login.py'])

    if not os.path.exists('login_running.flag') and not os.path.exists('app_running.flag'):
        break


    print('login:', login)