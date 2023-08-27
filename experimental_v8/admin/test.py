import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class CustomLineEdit(QLineEdit):
    def __init__(self, default_text="0"):
        super().__init__(default_text)
        self.default_text = default_text
        self.default_text_entered = False
        self.setText(default_text)

    def keyPressEvent(self, event):
        if self.default_text_entered:
            super().keyPressEvent(event)
        else:
            self.clear()
            self.default_text_entered = True

            key = event.text()
            if key.isnumeric() or key == ".":
                super().keyPressEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        line_edit = CustomLineEdit()
        layout.addWidget(line_edit)

        self.setLayout(layout)
        self.setWindowTitle("Auto-Replace QLineEdit")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
