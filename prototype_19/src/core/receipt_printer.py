import os
import random
import time as tm
import pythoncom
import uuid
import machineid
from datetime import *
from docx2pdf import *
import win32com.client
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class ReceiptGenerator(QThread):
    # update = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, cust_order_item_data=[], cust_order_summary_data=[], customer_id=0, current_user='', action=''):
        super().__init__()

        self.action = action

        self.cust_order_item_data = cust_order_item_data
        self.cust_order_summary_data = cust_order_summary_data
        self.customer_id = customer_id
        self.customer_id = 0 if customer_id == None else self.customer_id
        self.current_user = current_user
        print('self.cust_order_item_data:', self.cust_order_item_data)
        print('self.cust_order_summary_data:', self.cust_order_summary_data)
        self.default_init()

    def default_init(self):
        self.ref_number = ''
        self.min = ''

    def run(self):
        self.print_receipt()
        self.finished.emit()
        self.convert_receipt_to_pdf()


    def print_receipt(self):
        pythoncom.CoInitialize()
        # Specify the path to the DOCX file

        if self.action == 'print_receipt':
            docx_file = os.path.abspath('G:' + '/My Drive/receipt/receipt.docx')
            self.table_e_index = 4
            pass
        elif self.action == 'print_invoice':
            docx_file = os.path.abspath('G:' + '/My Drive/receipt/invoice.docx')
            self.table_e_index = 5
            pass

        # Initialize Word application
        word = win32com.client.Dispatch('Word.Application')

        # Open the DOCX file
        self.doc = word.Documents.Open(docx_file)

        print('cust_order_item_data:', self.cust_order_item_data)
        print('cust_order_summary_data:', self.cust_order_summary_data)

        self.ref_number_generator()
        self.tin_generator()
        self.min_generator()

        self.process_table_a()
        self.process_table_b()
        self.process_table_c()
        self.process_table_d()
        self.process_table_e()

        # Save the modified document
        self.doc.SaveAs(os.path.abspath('G:' + f'/My Drive/receipt/saved/{self.ref_number}.docx'))  # Save with the same file path to overwrite the original

        # Specify the path to the DOCX file
        self.updated_docx_file = os.path.abspath('G:' + f'/My Drive/receipt/saved/{self.ref_number}.docx')

        # Open the DOCX file
        self.updated_doc = word.Documents.Open(self.updated_docx_file)
        
        # Print the document
        # self.updated_doc.PrintOut()

        word.Quit()

        pythoncom.CoInitialize()

    def convert_receipt_to_pdf(self):
        pdf_file = self.updated_docx_file.replace('.docx','.pdf')
        convert(self.updated_docx_file, pdf_file)

        if os.path.exists(self.updated_docx_file): 
            os.remove(self.updated_docx_file)

        print('CONVERTED!')

    def ref_number_generator(self):

        sales_group_id = f'{1:02}'
        customer_id = f'{self.customer_id:05}'
        update_ts = f"{datetime.today().strftime('%y%m%d%H%M')}"
        
        print('receipt_customer_id:', customer_id)

        self.ref_number = f"{sales_group_id}-{customer_id}-{update_ts}"
    def tin_generator(self):
        self.tin = f'40567264400000'
    def min_generator(self):
        # uuid_value = uuid.uuid4()
        # self.min = str(uuid_value)[:8]
        self.min = f'{machineid.id()}'
        pass

    def process_table_a(self):
        # Access the first table in the document (assuming it's the only table)
        table_a = self.doc.tables[0] 

        # Define placeholders and values
        table_a_placeholders = {
            '{address}': 'Zone 1 Liboro, Ragay, Camarines Sur',
            '{transaction_date}': f'{date.today()}',
            '{transaction_reference}': f'{self.ref_number}',
            '{tin}': f'{self.tin}',
            '{min}': f'{self.min}'
        }

        # Replace table_a_placeholders with values
        for row in table_a.Rows:
            for cell in row.Cells:
                for placeholder, value in table_a_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        pass
    def process_table_b(self):
        cust_order_item_data = self.cust_order_item_data

        print('cust_order_item_data:', cust_order_item_data)

        # sample data
        qtys = [item[2] for item in cust_order_item_data] # remove 'x' from quantities
        item_names = [item[3] for item in cust_order_item_data]
        prices = [item[4] for item in cust_order_item_data] # remove '₱' from

        # Access the second table (Table B) in the document
        table_b = self.doc.Tables[1]  # Assuming Table B is the second table in the document

        # Define placeholders for Table B
        placeholders_b = {
            '{qty}': '',
            '{item_name}': '',
            '{price}': ''
        }

        # Add rows to Table B and populate with item names and prices
        for qty, item_name, price in zip(qtys, item_names, prices):
            # Add a new row to the table
            row = table_b.Rows.Add()

            # Replace placeholders with values for the new row in Table B
            for cell in row.Cells:
                for placeholder, value in placeholders_b.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value)

            # Populate the cells with item name and price
            row.Cells[0].Range.Text = qty + 'x'
            row.Cells[1].Range.Text = item_name
            row.Cells[2].Range.Text = '₱' + price

        table_b.Rows[1].Delete()

        pass
    def process_table_c(self):
        cust_order_summary_data = self.cust_order_summary_data

        subtotal = cust_order_summary_data[0][0]
        discount = cust_order_summary_data[0][1]
        tax = cust_order_summary_data[0][2]
        total = cust_order_summary_data[0][3]

        # Access the first table in the document (assuming it's the only table)
        table_c = self.doc.tables[2] 

        # Define placeholders and values
        table_c_placeholders = {
            '{subtotal}': f'{subtotal:,.2f}',
            '{discount}': f'{discount:,.2f}',
            '{tax}': f'{tax:,.2f}',
            '{total}': f'{total:,.2f}'
        }

        # Replace table_c_placeholders with values
        for row in table_c.Rows:
            for cell in row.Cells:
                for placeholder, value in table_c_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = '₱' + cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        pass
    def process_table_d(self):
        cust_order_summary_data = self.cust_order_summary_data

        amount_tendered = cust_order_summary_data[0][4]
        change = cust_order_summary_data[0][5]

        # Access the first table in the document (assuming it's the only table)
        table_d = self.doc.tables[3] 

        # Define placeholders and values
        table_d_placeholders = {
            '{amount_tendered}': f'{amount_tendered:,.2f}',
            '{change}': f'{change:,.2f}'
        }

        # Replace table_d_placeholders with values
        for row in table_d.Rows:
            for cell in row.Cells:
                for placeholder, value in table_d_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = '₱' + cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        pass
    def process_table_e(self):
        # Access the first table in the document (assuming it's the only table)
        
        table_e = self.doc.tables[self.table_e_index] 

        # Define placeholders and values
        table_e_placeholders = {
            '{cashier}': f'{self.current_user}',
            '{phone}': '+1234567890',
        }

        # Replace table_e_placeholders with values
        for row in table_e.Rows:
            for cell in row.Cells:
                for placeholder, value in table_e_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')
        pass

# class SampleLayout(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.receipt_generator = ReceiptGenerator()

#         self.form_layout = QFormLayout()

#         self.print_button = QPushButton('Print')
#         self.ref_number = QPushButton('Show TIN')
#         self.print_button.clicked.connect(self.print_receipt_button)
#         self.ref_number.clicked.connect(self.show_tin)

#         self.form_layout.addRow(self.print_button)
#         self.form_layout.addRow(self.ref_number)

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
