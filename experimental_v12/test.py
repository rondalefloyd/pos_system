import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel

class PhoneNumberWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Philippine Mobile Number:")
        self.phone_line_edit = QLineEdit()
        self.phone_line_edit.setInputMask("63+99-999999999")
        self.phone_line_edit.setPlaceholderText("+63-123456789")
        self.phone_line_edit.textChanged.connect(self.validate_phone_number)

        layout.addWidget(label)
        layout.addWidget(self.phone_line_edit)

        self.setLayout(layout)

    def validate_phone_number(self):
        phone_number = self.phone_line_edit.text()
        if phone_number.startswith("+63-") and len(phone_number) == 14:
            self.phone_line_edit.setStyleSheet("")
        else:
            self.phone_line_edit.setStyleSheet("background-color: pink;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhoneNumberWidget()
    window.setWindowTitle("Philippine Mobile Number Input")
    window.show()
    sys.exit(app.exec())
