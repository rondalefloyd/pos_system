
import sys, os
from typing import *
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(''))

from src.core.csv_to_db_importer import MyDataImportThread
from src.gui.widget.my_widget import *
from src.core.sql.admin.product import *


product_schema = MyProductSchema()

class MyUpdaterModel:
    def __init__(self):
        pass

    def set_import_data_entry(self, csv_file_path):
        self.progress_count = 0
        self.progress_percent = 100

        self.data_import_thread = MyDataImportThread(data_name='product', csv_file_path=csv_file_path)

        self.data_import_thread.start()

class MyUpdaterView(MyDialog):
    def __init__(self, model: MyUpdaterModel):
        super().__init__(object_name='MyLoginView', window_title='Login')

        self.m = model

    def set_progress_dialog(self):
        self.progress_bar = MyProgressBar()
        self.progress_label = MyLabel(object_name='progress_label', text='Please wait...')
        self.other_label_a = MyLabel(object_name='other_label_a', text='Please wait while updating database')
        self.progress_dialog = MyDialog(object_name='updater_progress_dialog', window_title='99% complete')
        self.progress_layout = MyVBoxLayout()
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.other_label_a)
        self.progress_dialog.setLayout(self.progress_layout)
        pass

class MyUpdaterController:
    def __init__(self, model: MyUpdaterModel, view: MyUpdaterView):
        self.v = view
        self.m = model

    def set_data_import_thread_conn(self):
        self.m.data_import_thread.update.connect(self.on_data_import_thread_update)
        self.m.data_import_thread.cancelled.connect(self.on_data_import_thread_cancelled)
        self.m.data_import_thread.finished.connect(self.on_data_import_thread_finished)
        self.m.data_import_thread.invalid.connect(self.on_data_import_thread_invalid)
        pass
    def on_data_import_thread_update(self, total_data_count, current_data):
        self.m.progress_count += 1
        print(self.m.progress_count)
        self.m.progress_percent = int((self.m.progress_count / total_data_count) * 100)
        self.v.progress_dialog.setWindowTitle(f"{self.m.progress_percent}% complete")
        self.v.progress_bar.setValue(self.m.progress_percent)
        self.v.progress_label.setText(current_data)
        pass
    def on_data_import_thread_cancelled(self):
        QMessageBox.information(self.v, 'Cancelled', 'Import cancelled.')
        pass
    def on_data_import_thread_finished(self):
        QMessageBox.information(self.v, 'Success', 'Import complete.')
        self.v.progress_dialog.close()
        pass
    def on_data_import_thread_invalid(self):
        QMessageBox.critical(self.v, 'Error', 'An error occurred during import.')
        self.v.progress_dialog.close()


class MyUpdaterWindow:
    def __init__(self):
        self.model = MyUpdaterModel()
        self.view = MyUpdaterView(self.model)
        self.controller = MyUpdaterController(self.model, self.view)

    def run(self):
        csv_file_path = (qss.csv_folder_path + qss.product_csv_name)

        self.view.set_progress_dialog()
        self.model.set_import_data_entry(csv_file_path)
        self.controller.set_data_import_thread_conn()

        self.view.progress_dialog.show()
        # if self.view.progress_dialog.close(): self.model.data_import_thread.stop()

    pass

if __name__ == ('__main__'):
    app = QApplication(sys.argv)
    updater_window = MyUpdaterWindow()

    updater_window.run()

    sys.exit(app.exec())