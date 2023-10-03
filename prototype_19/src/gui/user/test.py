import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLineEdit

class Tab(QWidget):
    def __init__(self):
        super().__init__()

        self.name = QLineEdit(self)
        self.phone = QLineEdit(self)
        self.button = QPushButton('Print', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.name)
        layout.addWidget(self.phone)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.print_values)

    def print_values(self):
        print(f"Name: {self.name.text()}, Phone: {self.phone.text()}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget(self)
        self.add_tab_button = QPushButton('Add Tab', self)

        self.add_tab_button.clicked.connect(self.addTab)

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.add_tab_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)

    def addTab(self):
        tab = Tab()
        self.tab_widget.addTab(tab, f"Tab {self.tab_widget.count()+1}")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
