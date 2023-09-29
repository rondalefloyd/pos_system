import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class PleaseWaitSleeper(QThread):
    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog

    def run(self):
        tm.sleep(1)  # Sleep for 5 seconds
        print('running')
        self.dialog.hide()  # Close the dialog