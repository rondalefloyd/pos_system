import os
from docx2pdf import *
import win32com.client
from PyQt5.QtCore import pyqtSignal

class ReceiptGenerator():
    data_saved = pyqtSignal()

    def __init__(self, filename=''):
        super().__init__()

        # Specify the path to the DOCX file
        docx_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../layout/raw_receipt.docx'))

        # Initialize Word application
        word = win32com.client.Dispatch('Word.Application')

        # Open the DOCX file
        doc = word.Documents.Open(docx_file)

        # Access the first table in the document (assuming it's the only table)
        table_a = doc.tables[0] 

        # Define placeholders and values
        table_a_placeholders = {
            '{address}': '123 Main St, City, Country',
            '{transaction_date}': '2023-09-09',
            '{transaction_reference}': 'TX123456',
            '{tin}': '123-45-6789',
            '{min}': '987654321'
        }

        # Replace table_a_placeholders with values
        for row in table_a.Rows:
            for cell in row.Cells:
                for placeholder, value in table_a_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        # sample data
        item_names = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']
        prices = ['10.00', '20.00', '15.00', '8.00', '12.00']

        # Access the second table (Table B) in the document
        table_b = doc.Tables[1]  # Assuming Table B is the second table in the document

        # Define placeholders for Table B
        placeholders_b = {
            '{item_name}': '',
            '{price}': ''
        }

        # Add rows to Table B and populate with item names and prices
        for item_name, price in zip(item_names, prices):
            # Add a new row to the table
            row = table_b.Rows.Add()

            # Replace placeholders with values for the new row in Table B
            for cell in row.Cells:
                for placeholder, value in placeholders_b.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value)

            # Populate the cells with item name and price
            row.Cells[0].Range.Text = item_name
            row.Cells[1].Range.Text = '₱' + price

        table_b.Rows[1].Delete()

        # Access the first table in the document (assuming it's the only table)
        table_c = doc.tables[2] 

        # Define placeholders and values
        table_c_placeholders = {
            '{subtotal}': '10.00',
            '{discount}': '20.00',
            '{tax}': '15.00',
            '{total}': '8.00',
            '{change}': '12.00'
        }

        # Replace table_c_placeholders with values
        for row in table_c.Rows:
            for cell in row.Cells:
                for placeholder, value in table_c_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = '₱' + cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        # Access the first table in the document (assuming it's the only table)
        table_d = doc.tables[3] 

        # Define placeholders and values
        table_d_placeholders = {
            '{cashier}': 'Mary Jane',
            '{phone}': '+1234567890',
        }

        # Replace table_d_placeholders with values
        for row in table_d.Rows:
            for cell in row.Cells:
                for placeholder, value in table_d_placeholders.items():
                    if placeholder in cell.Range.Text:
                        cell.Range.Text = cell.Range.Text.replace(placeholder, value).replace('\r', '').replace('\n', '')

        # Save the modified document
        doc.SaveAs(os.path.abspath(os.path.join(os.path.dirname(__file__), '../layout/updated_receipt.docx')))  # Save with the same file path to overwrite the original

        # Specify the path to the DOCX file
        updated_docx_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../layout/updated_receipt.docx'))

        # Open the DOCX file
        updated_doc = word.Documents.Open(updated_docx_file)

        # Print the document
        updated_doc.PrintOut()

        # Optionally, close Word application when done
        word.Quit()

if __name__ == "__main__":
    # Instantiate ReceiptGenerator with a filename if needed
    receipt_generator = ReceiptGenerator()
