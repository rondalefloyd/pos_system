import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ComboBox Visibility Example")
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        self.combo_box = QComboBox()
        self.combo_box.addItem("Option 1")
        self.combo_box.addItem("Option 2")
        self.combo_box.addItem("Option 3")
        self.combo_box.addItem("Option 4")
        self.combo_box.currentIndexChanged.connect(self.handle_combo_box_change)

        self.label = QLabel("Widget to Toggle")
        self.label.hide()  # Initially hide the widget

        layout.addWidget(self.combo_box)
        layout.addWidget(self.label)

    def handle_combo_box_change(self):
        current_text = self.combo_box.currentText()
        if current_text != 'Option 1':
            self.label.show()
        else:
            self.label.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
