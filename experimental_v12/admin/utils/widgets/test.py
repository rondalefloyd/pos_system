import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class TabExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTabBar Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a QTabWidget to hold the tabs
        tab_widget = QTabWidget(self)
        tab_widget.setGeometry(10, 10, 780, 580)

        # Create a QTabBar and set its position
        tab_bar = QTabBar()
        tab_bar.setTabsClosable(True)  # Allow closing tabs
        tab_widget.setTabBar(tab_bar)

        # Connect signals for tab closing
        tab_bar.tabCloseRequested.connect(self.close_tab)

        # Create and add tabs
        for i in range(5):
            tab_widget.addTab(self.create_tab_content(i), f"Tab {i + 1}")

    def create_tab_content(self, index):
        # Create a QWidget to be used as the content of the tab
        tab_content = QWidget()

        layout = QVBoxLayout()
        label = QLabel(f"This is the content of Tab {index + 1}")
        layout.addWidget(label)

        tab_content.setLayout(layout)
        return tab_content

    def close_tab(self, index):
        # Handle tab closing
        tab_widget = self.centralWidget()
        if index >= 0 and index < tab_widget.count():
            tab_widget.removeTab(index)

def main():
    app = QApplication(sys.argv)
    window = TabExample()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()