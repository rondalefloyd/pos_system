import sqlite3
import sys, os
import pandas as pd
import threading
import time as tm
import schedule as sc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.csv_importer import *

class ScheduledCSVImporter(QThread):
    import_data_signal = pyqtSignal(str)  # Signal for passing messages to the GUI

    def __init__(
        # region -- params
        self, 
        product_import=None,
        promo_import=None,
        customer_import=None,
        user_import=None
        # endregion -- params
    ):
        super().__init__()
        self.product_import = product_import
        self.promo_import = promo_import
        self.customer_import = customer_import
        self.user_import = user_import
        
        self.running = True  # Flag to control the thread's execution
        self.update_date = date.today()

    def run(self):
        sc.every(5).seconds.do(self.import_product_csv)
        sc.every(5).seconds.do(self.import_promo_csv)
        sc.every(5).seconds.do(self.import_customer_csv)
        sc.every(5).seconds.do(self.import_user_csv)

        while self.running:  # Check the running flag in the loop
            sc.run_pending()
            tm.sleep(5)  # 1800 secs = 30 mins

    def stop(self):
        self.running = False  # Set the flag to stop the thread

        self.product_import.setText("<font color='red'>None</font>")
        self.promo_import.setText("<font color='red'>None</font>")
        self.customer_import.setText("<font color='red'>None</font>")
        self.user_import.setText("<font color='red'>None</font>")

    def import_product_csv(self):
        pass
    def import_promo_csv(self):
        csv_file = os.path.abspath('G:' + f'\My Drive\data\promo-{date.today()}.csv')

        self.csv_file_name = os.path.basename(csv_file)

        if os.path.exists(csv_file):
            data_frame = pd.read_csv(csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)
            total_rows = len(data_frame)

            self.update_date = date.today()

            self.import_data_signal.emit(f"<font color='green'>Importing</font>")  # Emit a message to the GUI

            self.import_thread = PromoCSVImporter(csv_file=csv_file)
            self.import_thread.start()
        else:
            self.import_data_signal.emit(f"<font color='orange'>Idle</font>") 
        pass
    def import_customer_csv(self):
        print('Importing customer csv...')
        # checkpoint !!!
        pass
    def import_user_csv(self):
        print('Importing user csv...')
        # checkpoint !!!
        pass
    
    def update_product_import_status_label(self, message):
        self.product_import.setText(f"{message}")
        pass
    def update_promo_import_status_label(self, message):
        self.promo_import.setText(f"{message}")
        pass
    def update_customer_import_status_label(self, message):
        self.customer_import.setText(f"{message}")
        pass
    def update_user_import_status_label(self, message):
        self.user_import.setText(f"{message}")
        pass

# class YourMainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Create a button to start the ScheduledCSVImporter thread
#         self.start_auto_import_button = QPushButton("Start Auto Import")
#         self.start_auto_import_button.clicked.connect(self.on_start_auto_import_button_clicked)

#         # Create a button to stop/disable the ScheduledCSVImporter thread
#         self.stop_auto_import_button = QPushButton("Stop Auto Import")
#         self.stop_auto_import_button.clicked.connect(self.on_stop_auto_import_button_clicked)

#         # Create a label to display messages from the ScheduledCSVImporter thread
#         self.status_label = QLabel("Status: Idle")

#         # Layout setup
#         layout = QVBoxLayout()
#         layout.addWidget(self.start_auto_import_button)
#         layout.addWidget(self.stop_auto_import_button)
#         layout.addWidget(self.status_label)
#         self.setLayout(layout)

#         self.auto_import_thread = None

#     def on_start_auto_import_button_clicked(self):
#         if self.auto_import_thread is None or not self.auto_import_thread.isRunning():
#             # Only create and start a new thread if it doesn't exist or is not running
#             self.auto_import_thread = ScheduledCSVImporter()
#             self.auto_import_thread.import_data_signal.connect(self.update_promo_import_status_label)
#             self.auto_import_thread.start()
#         else:
#             self.status_label.setText("Status: Auto Import is already running.")

#     def on_stop_auto_import_button_clicked(self):
#         if self.auto_import_thread and self.auto_import_thread.isRunning():
#             self.auto_import_thread.stop()
#             self.auto_import_thread.wait()  # Wait for the thread to finish
#             self.status_label.setText("Status: Stopped")
#         else:
#             self.status_label.setText("Status: Auto Import is not running.")

#     def update_promo_import_status_label(self, message):
#         self.status_label.setText(f"Status: {message}")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = YourMainWindow()
#     window.show()
#     sys.exit(app.exec())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScheduledCSVImporter()
    window.start()
    sys.exit(app.exec())
