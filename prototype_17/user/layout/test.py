import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtCore import Qt

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QWidget as the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a QLineEdit widget for barcode input
        self.barcode_input = QLineEdit()
        self.barcode_input.returnPressed.connect(self.handle_barcode_scanned)

        # Create a QPushButton for manual product addition (for testing)
        add_product_button = QPushButton("Add Product Manually")
        add_product_button.clicked.connect(self.add_product_manually)

        # Create a QTableWidget to display the added products
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(4)  # Added a "Qty" column
        self.product_table.setHorizontalHeaderLabels(["Barcode", "Product Name", "Price", "Qty"])  # Updated headers

        # Create a QLabel to display the total price
        self.total_price_label = QLabel("Total Price: $0.00")

        # Initialize a list to store added products as tuples (barcode, name, price, qty)
        self.products = []

        # Add widgets to the layout
        layout.addWidget(self.barcode_input)
        layout.addWidget(add_product_button)
        layout.addWidget(self.product_table)
        layout.addWidget(self.total_price_label)

    def handle_barcode_scanned(self):
        # This function will be called when the Enter key is pressed after scanning
        scanned_barcode = self.barcode_input.text()
        self.add_product_from_barcode(scanned_barcode)
        self.barcode_input.clear()  # Clear the input field for the next s  can

    def add_product_from_barcode(self, barcode):
        # Implement logic to add the product based on the scanned barcode
        # For example, you can retrieve product information from a database
        # Here, we'll add a sample product for demonstration
        product_name = "Sample Product"
        product_price = 10.00  # Updated to a numeric value

        # Check if the product already exists in the list
        for index, product in enumerate(self.products):
            if product[0] == barcode:
                # Increment the quantity if the product already exists
                updated_product = (barcode, product[1], product[2], product[3] + 1)  # Added a quantity field
                self.products[index] = updated_product
                break
        else:
            # Add the product to the list with a quantity of 1
            new_product = (barcode, product_name, product_price, 1)
            self.products.append(new_product)

        self.update_product_table()

    def add_product_manually(self):
        # Implement manual product addition logic (for testing)
        manual_product_name = "Manually Added Product"
        manual_product_price = 15.00  # Updated to a numeric value
        manual_product_barcode = "123456"  # A unique barcode for manual products

        # Check if the product already exists in the list
        for index, product in enumerate(self.products):
            if product[0] == manual_product_barcode:
                # Increment the quantity if the product already exists
                updated_product = (manual_product_barcode, product[1], product[2], product[3] + 1)  # Added a quantity field
                self.products[index] = updated_product
                break
        else:
            # Add the product to the list with a quantity of 1
            new_product = (manual_product_barcode, manual_product_name, manual_product_price, 1)
            self.products.append(new_product)

        self.update_product_table()

    def update_product_table(self):
        # Clear the table
        self.product_table.setRowCount(0)

        # Initialize total price
        total_price = 0.0

        # Iterate over the products list and populate the table
        for barcode, product_name, product_price, product_qty in self.products:
            row_position = self.product_table.rowCount()
            self.product_table.insertRow(row_position)

            # Calculate the subtotal for each product
            subtotal = product_price * product_qty
            total_price += subtotal

            self.product_table.setItem(row_position, 0, QTableWidgetItem(barcode))
            self.product_table.setItem(row_position, 1, QTableWidgetItem(product_name))
            self.product_table.setItem(row_position, 2, QTableWidgetItem(f"${product_price:.2f}"))
            self.product_table.setItem(row_position, 3, QTableWidgetItem(str(product_qty)))

        # Update the total price label
        self.total_price_label.setText(f"Total Price: ${total_price:.2f}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())
