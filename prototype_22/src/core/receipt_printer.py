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
    update = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(
            self,
            transaction_info,
            final_order_table,
            final_order_summary,
            cashier_info,
            action,
    ):
        super().__init__()

        self.transaction_info = transaction_info
        self.final_order_table = final_order_table
        self.final_order_summary = final_order_summary
        self.cashier_info = cashier_info
        self.action = action # if print or save

    def run(self):
        self.print_receipt()
        
        if self.action == 'save':
            self.convert_receipt_to_pdf()

        self.finished.emit()

    def print_receipt(self):
        pythoncom.CoInitialize()

        docx_file = os.path.abspath('G:' + '/My Drive/receipt/receipt.docx')
        word = win32com.client.Dispatch('Word.Application')
        self.doc = word.Documents.Open(docx_file)

        ref_number = self.transaction_info[1]

        self.process_table_a()
        self.process_table_b()
        self.process_table_c()
        self.process_table_d()
        self.process_table_e()

        # Save the modified document
        self.doc.SaveAs(os.path.abspath('G:' + f'/My Drive/receipt/saved/{ref_number}.docx'))  # Save with the same file path to overwrite the original

        # Specify the path to the DOCX file
        self.updated_docx_file = os.path.abspath('G:' + f'/My Drive/receipt/saved/{ref_number}.docx')

        # Open the DOCX file
        self.updated_doc = word.Documents.Open(self.updated_docx_file)
        
        if self.action == 'print':
            print('IM PRINTING!!!!!')
            # Print the document
            # self.updated_doc.PrintOut()

        word.Quit()

        self.update.emit(6)

        pythoncom.CoInitialize()

    def convert_receipt_to_pdf(self):
        self.update.emit(7)
        
        pdf_file = self.updated_docx_file.replace('.docx','.pdf')
        convert(self.updated_docx_file, pdf_file)

        print('IM SAVVIIINGGG')

        if os.path.exists(self.updated_docx_file): 
            os.remove(self.updated_docx_file)


        print('CONVERTED!')

    def process_table_a(self):
        # Access the first table in the document (assuming it's the only table)
        transaction_date = self.transaction_info[0]
        ref_number = self.transaction_info[1]
        tin_number = self.transaction_info[2]
        min_number = self.transaction_info[3]

        table_a = self.doc.tables[0] 

        # Define placeholders and values
        table_a_placeholders = {
            '{address}': 'Zone 1 Liboro, Ragay, Camarines Sur',
            '{transaction_date}': f"{transaction_date}",
            '{transaction_reference}': f"{ref_number}",
            '{tin}': f"{tin_number}",
            '{min}': f"{min_number}"
        }

        # Replace table_a_placeholders with values
        for row in table_a.Rows:
            for cell in row.Cells:
                for placeholder, value in table_a_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        self.update.emit(1)

        pass
    def process_table_b(self):
        final_order_table = self.final_order_table

        # sample data
        final_qty = [item[0] for item in final_order_table] # remove 'x' from quantities
        final_product = [item[1] for item in final_order_table]
        final_total_amount = [item[2] for item in final_order_table] # remove '₱' from

        # Access the second table (Table B) in the document
        table_b = self.doc.Tables[1]  # Assuming Table B is the second table in the document

        # Define placeholders for Table B
        table_b_placeholders = {
            '{qty}': '',
            '{item_name}': '',
            '{price}': ''
        }

        # Add rows to Table B and populate with item names and prices
        for qty, item_name, price in zip(final_qty, final_product, final_total_amount):
            # Add a new row to the table
            row = table_b.Rows.Add()

            # Replace placeholders with values for the new row in Table B
            for cell in row.Cells:
                for placeholder, value in table_b_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value)

            # Populate the cells with item name and price
            row.Cells[0].Range.Text = qty
            row.Cells[1].Range.Text = item_name
            row.Cells[2].Range.Text = price

        table_b.Rows[1].Delete()

        self.update.emit(2)

        pass
    def process_table_c(self):
        final_subtotal = self.final_order_summary[0]
        final_discount = self.final_order_summary[1]
        final_tax = self.final_order_summary[2]
        final_total = self.final_order_summary[3]

        # Access the first table in the document (assuming it's the only table)
        table_c = self.doc.tables[2] 

        # Define placeholders and values
        table_c_placeholders = {
            '{subtotal}': f'{final_subtotal:,.2f}',
            '{discount}': f'{final_discount:,.2f}',
            '{tax}': f'{final_tax:,.2f}',
            '{total}': f'{final_total:,.2f}'
        }

        # Replace table_c_placeholders with values
        for row in table_c.Rows:
            for cell in row.Cells:
                for placeholder, value in table_c_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = '₱' + cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        self.update.emit(3)

        pass
    def process_table_d(self):
        final_order = self.final_order_summary[4]
        final_change = self.final_order_summary[5]

        # Access the first table in the document (assuming it's the only table)
        table_d = self.doc.tables[3] 

        # Define placeholders and values
        table_d_placeholders = {
            '{amount_tendered}': f'{final_order:,.2f}',
            '{change}': f'{final_change:,.2f}'
        }

        # Replace table_d_placeholders with values
        for row in table_d.Rows:
            for cell in row.Cells:
                for placeholder, value in table_d_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = '₱' + cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        self.update.emit(4)

        pass
    def process_table_e(self):
        # Access the first table in the document (assuming it's the only table)
        cashier_name = self.cashier_info[0]
        cashier_phone = self.cashier_info[1]

        table_e = self.doc.tables[5] 

        # Define placeholders and values
        table_e_placeholders = {
            '{cashier}': f'{cashier_name}',
            '{phone}': f'{cashier_phone}',
        }

        # Replace table_e_placeholders with values
        for row in table_e.Rows:
            for cell in row.Cells:
                for placeholder, value in table_e_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')
        
        self.update.emit(5)

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
