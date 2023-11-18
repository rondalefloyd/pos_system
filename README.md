## Introduction

Welcome to the POS System developed for Phoebe M. Santos! This Point of Sale (POS) system is designed to streamline the management of products, transactions, and user interactions in a retail environment. Whether you're an administrator with access to comprehensive product and user management tools or a cashier processing orders with a user-friendly interface, this POS system aims to provide a seamless and efficient experience.

## Installation
To get started with the POS System, follow these installation steps:

1. **Change Directory:**
   - Change the current working directory to the location of the 'main.py' file.

2. **PyInstaller Command:**
   - Open a terminal/cmd/powershell window and type the following command:
     ```bash
     pyinstaller --onefile --add-data "template;template" --add-data "src;src" --noconsole --name=POS main.py
     ```

3. **Requirements:**
   - Ensure that the computer has the following prerequisites:
     3.1. Google Drive for desktop:
         - The Gmail account's Google Drive should contain specific folders with necessary files.
     3.2. Microsoft Word (any version):
         - This is required for printing receipts.

## Key Features
Explore the key features of the POS System:

1. **Main:**
   1.1. Execute Initial Task:
       - Fetch data from a spreadsheet via Google API, utilizing SQLite3 to perform INSERT queries, and running the 'login.py' script.

2. **Login:**
   2.1. Username and Password Entry:
       - Input your registered user credentials to access the system, with different pages displayed based on user access levels.

3. **Admin (for level 3 users):**
   Manage various aspects of the system, including:
   3.1. Product, Promo, Reward, Customer, and User Management.

4. **Cashier (for level 1 or 2 users):**
   Process sales efficiently with features like:
   4.1. Sales Management (POS), Transaction Management, and Product/Customer Management (for level 2 users only).

Feel free to explore the detailed documentation for each section to make the most out of the POS System for Phoebe M. Santos.
