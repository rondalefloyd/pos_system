import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
import schedule as sc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class WarningMessageBox(QMessageBox):

    def __init__(self, csv_file=None):
        super().__init__()

        self.warning(None, 'Sample', 'This is a sampel warning.', QMessageBox.StandardButton.Ok)

        if QMessageBox.StandardButton.Ok:
            print('OK!')
            QApplication.quit()


if __name__ == '__main__':
    starter = QApplication(sys.argv)
    
    automatic_import = WarningMessageBox()


