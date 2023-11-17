import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


cwd = os.getcwd()
path = os.path.join(cwd, 'src')

print('path::', path)

class MyLoginWindow:
    def __init__(self):
        self.view = QWidget()
        self.layout = QVBoxLayout()
        self.label = QLabel(f'path:: {path}')
        self.layout.addWidget(self.label)
        self.view.setLayout(self.layout)

    def run(self):
        self.view.show()
    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    login_window = MyLoginWindow()

    login_window.run()

    sys.exit(app.exec())