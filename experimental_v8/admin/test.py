import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Window at Bottom-Right Corner')
        self.setGeometry(0, 0, 400, 300)  # Set initial size (optional)

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Calculate the top-left corner position for the bottom-right placement
        top_left_x = screen_geometry.right() - self.width()
        top_left_y = screen_geometry.bottom() - self.height()

        self.move(top_left_x, top_left_y)
        self.setFixedHeight(screen_geometry.height())  # Set window height to screen's height

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())