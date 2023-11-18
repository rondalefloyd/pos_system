## POS System Development for Phoebe M. Santos

## Introduction

## Installation
1. Change the current working directory to the directory of 'main.py'
2. Type this command in terminal/cmd/powershell: 
  ```bash
  pyinstaller --onefile --add-data "template;template" --add-data "src;src" --noconsole --name=POS main.py
  ```
3. To run the 'POS.exe', make sure the computer has the following:
  a. Google Drive for desktop
    - The Gmail account's Google Drive should contain the following folders:
      - csv
        - product.csv ('item_list.gsheet' exported as 'product.csv') 
      - dashboard
      - live_db
        - accounts.db
        - sales.db
        - syslib.db
        - txn.db
      - receipt
        - saved (printed receipt)
      - sito ('Scan-IT to Office' files)
        - item_list.gsheet
  b. Microsoft Word (any version) (used for printing receipts)

## Key features

1. Main
  a. Execute initial task
    - Get data from spreadsheet via Google API (export .gsheet file to .csv file)
    - Use SQLite3 to perform INSERT query (extract data from ..csv using Pandas and use INSERT query)
    - Run login.py

2. Login
  a. Username and password entry
    - Input the registered user (show the page depending on the user's access level)

3. Admin (show if level 3 users)
  a. Product management
    - Filter product
      - Can be filtered by item barcode, item name, item expiredt, itemtype name, brand name, salesgroup name, supplier name, itemprice updatets
    - Manage product
      - Add product
      - Edit product
      - View product
      - Delete product
    - Product table

  b. Promo management
    - Filter promo
      - Can be filtered by name, promo type, discount percent, description
    - Manage promo
      - Add promo
      - Edit promo
      - View promo
      - Delete promo
    - Promo table

  c. Reward management
    - Filter reward
      - Can be filtered by name, unit, points, description
    - Manage reward
      - Add reward
      - Edit reward
      - View reward
      - Delete reward
    - Reward table

  d. Customer management
    - Filter customer
      - Can be filtered by name, address, barrio, town, phone, age, gender, marital status
    - Manage customer
      - Add customer
      - Edit customer
      - View customer
      - Delete customer
    - Customer table

  e. User management
    - Filter user
      - Can be filtered by name, password, accesslevel, phone
    - Manage user
      - Add user
      - Edit user
      - View user
      - Delete user
    - User table

  f. Logout

4. Cashier (show if level 1 or 2 users)
  a. Sales Management (POS)
    - Filter product
      - Can be filtered by item barcode, item name, itemtype name, brand name
    - Add order
      - Retail (creates separate tab for retail orders)
      - Wholesale (creates a separate tab for wholesale orders)
      - Dual (creates two (2) separate linked tabs for retail and wholesale orders)

    - Set customer for selected order
      - Show list of customer names
      - Show points of selected customer 

    - Add product to order
      - Add product with custom qty
      - Add product with fixed qty (1)   
      - Add product with fixed qty (1) via barcode
      - Edit product qty
      - Drop product with fixed qty (1)
      - Drop all product qty

    - Complete order
      - 
  b. Transaction management
    - Filter product
      - Can be filtered by user name, customer name, item name, total amount, void, reason, referencenumber, updatets
    - Reprint (reprint receipt)
    - Manage transaction
      - Void transaction

  c. Product management (for level 2 users only)
    - Filter product
      - Can be filtered by item barcode, item name, item expiredt, itemtype name, brand name, salesgroup name, supplier name, itemprice updatets
    - Manage product
      - Add product
      - Edit product
      - View product
      - Delete product
    - Product table

  d. Customer management (for level 2 users only)
    - Filter customer
      - Can be filtered by name, address, barrio, town, phone, age, gender, marital status
    - Manage customer
      - Add customer
      - Edit customer
      - View customer
      - Delete customer
    - Customer table

  e. Logout
