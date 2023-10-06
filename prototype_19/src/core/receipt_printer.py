import os
import random
import time as tm
import pythoncom
from datetime import *
from docx2pdf import *
import win32com.client
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class ReceiptGenerator(QThread):
    finished = pyqtSignal()

    def __init__(self, cart_list_data=[], bill_summary_data=[]):
        super().__init__()

        self.cart_list_data = cart_list_data
        self.bill_summary_data = bill_summary_data
        self.default_init()

    def default_init(self):
        self.tin = ''

    def run(self):
        self.print_receipt()
        # self.convert_receipt_to_pdf()

    def print_receipt(self):
        pythoncom.CoInitialize()
        # Specify the path to the DOCX file
        docx_file = os.path.abspath('G:' + '/My Drive/receipt/raw_receipt.docx')

        # Initialize Word application
        word = win32com.client.Dispatch('Word.Application')

        # Open the DOCX file
        self.doc = word.Documents.Open(docx_file)

        print('cart_list_data:', self.cart_list_data)
        print('bill_summary_data:', self.bill_summary_data)

        self.process_table_a()
        self.process_table_b()
        self.process_table_c()
        self.process_table_d()

        self.tin_generator()
        # Save the modified document
        self.doc.SaveAs(os.path.abspath('G:' + f'/My Drive/receipt/saved/{self.tin}.docx'))  # Save with the same file path to overwrite the original

        # Specify the path to the DOCX file
        self.updated_docx_file = os.path.abspath('G:' + f'/My Drive/receipt/saved/{self.tin}.docx')

        # Open the DOCX file
        self.updated_doc = word.Documents.Open(self.updated_docx_file)
        
        # Print the document
        self.updated_doc.PrintOut()

        word.Quit()

        pythoncom.CoInitialize()

    def convert_receipt_to_pdf(self):
        pdf_file = self.updated_docx_file.replace('.docx','.pdf')
        convert(self.updated_docx_file, pdf_file)

        if os.path.exists(self.updated_docx_file): 
            os.remove(self.updated_docx_file)

        print('CONVERTED!')
        self.finished.emit()

    def tin_generator(self):
        update_ts = datetime.today()
        number = random.randint(100000000, 999999999)
        self.tin = f"{number}_{update_ts.strftime('%m%d%Y')}"

    def process_table_a(self):
        # Access the first table in the document (assuming it's the only table)
        table_a = self.doc.tables[0] 

        # Define placeholders and values
        table_a_placeholders = {
            '{address}': 'Zone 1 Liboro, Ragay, Camarines Sur',
            '{transaction_date}': f'{date.today()}',
            '{transaction_reference}': f'{self.tin}',
            '{tin}': '123-45-6789',
            '{min}': '987654321'
        }

        # Replace table_a_placeholders with values
        for row in table_a.Rows:
            for cell in row.Cells:
                for placeholder, value in table_a_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        pass
    def process_table_b(self):
        cart_list_data = self.cart_list_data

        # sample data
        qtys = [item[0] for item in cart_list_data] # remove 'x' from quantities
        item_names = [item[1] for item in cart_list_data]
        prices = [item[2] for item in cart_list_data] # remove '₱' from

        # Access the second table (Table B) in the document
        table_b = self.doc.Tables[1]  # Assuming Table B is the second table in the document

        # Define placeholders for Table B
        placeholders_b = {
            '{qty}': '',
            '{item_name}': '',
            '{price}': ''
        }

        # Add rows to Table B and populate with item names and prices
        for qty, item_name, price in zip(item_names, qtys, prices):
            # Add a new row to the table
            row = table_b.Rows.Add()

            # Replace placeholders with values for the new row in Table B
            for cell in row.Cells:
                for placeholder, value in placeholders_b.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value)

            # Populate the cells with item name and price
            row.Cells[0].Range.Text = qty
            row.Cells[1].Range.Text = item_name
            row.Cells[2].Range.Text = '₱' + price

        table_b.Rows[1].Delete()

        pass
    def process_table_c(self):
        bill_summary_data = self.bill_summary_data

        subtotal = bill_summary_data[0][0]
        discount = bill_summary_data[0][1]
        tax = bill_summary_data[0][2]
        total = bill_summary_data[0][3]
        change = bill_summary_data[0][4]

        # Access the first table in the document (assuming it's the only table)
        table_c = self.doc.tables[2] 

        # Define placeholders and values
        table_c_placeholders = {
            '{subtotal}': f'{subtotal:.2f}',
            '{discount}': f'{discount:.2f}',
            '{tax}': f'{tax:.2f}',
            '{total}': f'{total:.2f}',
            '{change}': f'{change:.2f}'
        }

        # Replace table_c_placeholders with values
        for row in table_c.Rows:
            for cell in row.Cells:
                for placeholder, value in table_c_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = '₱' + cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        pass

    def process_table_d(self):
        # Access the first table in the document (assuming it's the only table)
        table_d = self.doc.tables[3] 

        # Define placeholders and values
        table_d_placeholders = {
            '{cashier}': 'Angie',
            '{phone}': '+1234567890',
        }

        # Replace table_d_placeholders with values
        for row in table_d.Rows:
            for cell in row.Cells:
                for placeholder, value in table_d_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')
        pass

# class SampleLayout(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.receipt_generator = ReceiptGenerator()

#         self.form_layout = QFormLayout()

#         self.print_button = QPushButton('Print')
#         self.tin = QPushButton('Show TIN')
#         self.print_button.clicked.connect(self.print_receipt_button)
#         self.tin.clicked.connect(self.show_tin)

#         self.form_layout.addRow(self.print_button)
#         self.form_layout.addRow(self.tin)

#         self.setLayout(self.form_layout)

#     def print_receipt_button(self):
#         confirmation = QMessageBox.warning(self, 'Confirm', 'Print receipt?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

#         if confirmation == QMessageBox.StandardButton.Yes:
#             self.receipt_generator.print_receipt()
#         elif confirmation == QMessageBox.StandardButton.No:
#             pass

#     def show_tin(self):
#         print('TIN:', self.receipt_generator.tin)
#         self.receipt_generator.convert_receipt_to_pdf()

# if __name__ == ('__main__'):
#     pos_app = QApplication(sys.argv)
#     window = SampleLayout()
#     window.show()
#     sys.exit(pos_app.exec())
