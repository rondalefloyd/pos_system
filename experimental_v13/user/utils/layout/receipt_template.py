import sqlite3
import sys, os
import fitz  # PyMuPDF
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ReceiptTemplate():
    data_saved = pyqtSignal()

    def __init__(self, printer, subtotal, discount, tax, total):
        super().__init__()


        # Load content from the PDF file
        pdf_document = fitz.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../layout/document.pdf')))
        pdf_page = pdf_document.load_page(0)  # Adjust page number as needed

        # Extract text from the PDF page
        pdf_text = pdf_page.get_text()

        print(pdf_text)

        self.setPlainText(pdf_text)
        self.setDocumentMargin(20)
        self.setTextWidth(340.0) # -- exact width for 80mm width paper

        painter = QPainter(printer)
        self.drawContents(painter)
        painter.end()

