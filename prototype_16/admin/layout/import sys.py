import sys
import time
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class Worker(QThread):
    finished = pyqtSignal()  # Signal emitted when the task is finished

    def run(self):
        # Your time-consuming task goes here
        for i in range(1, 11):
            time.sleep(1)  # Simulate a time-consuming task (e.g., 10 seconds)
            print(f"Task progress: {i}/10")

        self.finished.emit()  # Emit the finished signal when done

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Threading Example")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Task not started")
        layout.addWidget(self.label)

        self.start_button = QPushButton("Start Task")
        self.start_button.clicked.connect(self.start_task)
        layout.addWidget(self.start_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.worker = Worker()
        self.worker.finished.connect(self.task_finished)

    def start_task(self):
        self.start_button.setEnabled(False)
        self.worker.start()
        self.label.setText("Task running...")

    def task_finished(self):
        self.label.setText("Task completed")
        self.start_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
