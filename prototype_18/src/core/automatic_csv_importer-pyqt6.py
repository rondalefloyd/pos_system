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

from core.manual_csv_importer import *
from gui.promo import *

class ScheduledCSVImporter(QThread):
    status_signal = pyqtSignal(str)  # Signal for passing messages to the GUI
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)

    def __init__(
        # region -- params
        self,
        promo_import=None
        # endregion -- params
    ):
        super().__init__()
        self.promo_import = promo_import
        self.scheduled_import_progress_dialog = MyProgressDialog()
        
        self.running = True  # Flag to control the thread's execution
        self.update_date = date.today()

    def run(self):
        sc.every(5).seconds.do(self.import_promo_csv)

        while self.running:  # Check the running flag in the loop
            sc.run_pending()
            tm.sleep(5)  # 1800 secs = 30 mins

    def stop(self):
        self.running = False  # Set the flag to stop the thread

        self.promo_import.setText("<font color='red'>None</font>")

    def import_promo_csv(self):
        self.csv_file = os.path.abspath('G:' + f'\My Drive\data\promo-{date.today()}.csv')

        if os.path.exists(self.csv_file):
            self.status_signal.emit(f"<font color='green'>Running</font>")  # Emit a message to the GUI

            try:
                self.promo_schema = PromoSchema()

                # Load the CSV file into a Pandas DataFrame
                self.csv_file_name = os.path.basename(self.csv_file)
                data_frame = pd.read_csv(self.csv_file, encoding='utf-8-sig', keep_default_na=False, header=None)

                self.total_rows = len(data_frame) 

                progress_min_range = 1

                count_row_data = 0

                for row in data_frame.itertuples(index=False):
                    (self.promo_name,
                    self.promo_type,
                    self.discount_percent,
                    self.description) = row[:4]

                    if '' in [
                        self.promo_name,
                        self.promo_type,
                        self.discount_percent
                    ]:
                        pass
                    else:
                        promo_name = str(self.promo_name)
                        promo_type = str(self.promo_type)
                        discount_percent = float(self.discount_percent)
                        description = str(self.description)

                        self.promo_schema.add_new_promo(
                            promo_name=promo_name,
                            promo_type=promo_type,
                            discount_percent=discount_percent,
                            description=description
                        )

                    progress_min_range += 1
                    self.progress_signal.emit(progress_min_range)

                    
                    count_row_data += 1
                    print(count_row_data)

            except Exception as error_message:
                print(error_message)
                
        else:
            self.status_signal.emit(f"<font color='orange'>Idle</font>") 
        pass
    
    def update_promo_import_status_label(self, message):
        print('Status B: ', message)
        self.promo_import.setText(f"{message}")

    def update_progress(self, progress):
        self.current_row = progress - 1
        percentage = int((self.current_row / self.total_rows) * 100)

        self.scheduled_import_progress_dialog.setWindowTitle(f"{percentage}% complete ({self.current_row} out of {self.total_rows})")
        self.scheduled_import_progress_dialog.setValue(percentage)
        pass

    def import_finished(self):
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
#             self.auto_import_thread.status_signal.connect(self.update_promo_import_status_label)
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
