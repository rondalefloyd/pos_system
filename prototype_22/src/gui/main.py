import sys, os
from PyQt6.QtCore import *

sys.path.append(os.path.abspath(''))

from src.gui.login.login import *

subprocess.run(['python', '-Xfrozen_modules=off', 'src/gui/login/updater.py'])

while True:
    login = subprocess.run(['python', '-Xfrozen_modules=off', 'src/gui/login/login.py'])