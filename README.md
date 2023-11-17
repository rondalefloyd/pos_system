## POS system
POS System Development for Phoebe M. Santos

## Introduction

## Installation
1. Type this command in terminal/cmd/powershell: pyinstaller --add-data "template;template" --add-data "src;src" --noconsole --name=POS main.py
2. Go to 'dist' folder and move the src and template along with the 'POS.exe'.

## Key features
1. POS.bat
    a. Timeout for 30 sec. to wait for wifi connection after turning on the computer

2. Main
    a. Execute initial task
        - Get data from spreadsheet via Google API (export .gsheet file to .csv file)
        - Use SQLite3 to perform INSERT query (extract data from .csv using Pandas and use INSERT query)
        - Run login.py

3. Login
    a. Username and password entry
        - Input the registered user (show the page depending on the user's access level)

4. Admin (show if level 3 users)
    a. Product management
        - Filter product
            - Can be filtered by 
        - Manage product
            - Add product
            - Edit product
            - View product
            - Delete product
        - Product table

    b. Inventory management
        - Filter product
            - Can be filtered by
        - Manage inventory
            - Edit available and on hand stock
            - Stop inventory tracking

    c. Promo management
        - Filter promo
            - Can be filtered by
        - Manage promo
            - Add promo
            - Edit promo
            - View promo
            - Delete promo
        - Promo table

    d. Reward management
        - Filter reward
            - Can be filtered by
        - Manage reward
            - Add reward
            - Edit reward
            - View reward
            - Delete reward
        - Reward table

    e. Customer management
        - Filter customer
            - Can be filtered by
        - Manage customer
            - Add customer
            - Edit customer
            - View customer
            - Delete customer
        - Customer table

    f. User management
        - Filter user
            - Can be filtered by
        - Manage user
            - Add user
            - Edit user
            - View user
            - Delete user
        - User table

    g. Logout

5. Cashier (show if level 1 or 2 users)
    a. Sales Management (POS)
        - Filter product
        - Add order
            - Retail (creates separate tab for retail orders)
            - Wholesale (creates separate tab for wholesale orders)
            - Dual (creates two (2) separate linked tabs for retail and wholesale orders)

        - Set customer for selected order
            - Show list of customer names
            - Show points of  selected customer 

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

    c. Product management (for level 2 users only)

    d. Customer management (for level 2 users only)

    e. Logout











    