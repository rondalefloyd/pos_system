import gspread
import pandas as pd

# Path to your local Google Sheets file
file_path = r"C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/src/core/smpos-403608-aa14a49badc1.json"

# Authenticate with your Google account (Make sure you have gspread OAuth2 credentials set up)
gc = gspread.service_account(filename=file_path)

# Open the local Google Sheets file by its title or URL
# Replace 'My Spreadsheet' with the actual title or URL of your Google Sheets file
spreadsheet = gc.open('test_product_list')

# Select a specific worksheet
worksheet = spreadsheet.get_worksheet(0)  # Replace 0 with the index of your desired worksheet

# Get the worksheet data as a list of dictionaries
data = worksheet.get_all_records()

# Export the data to a CSV file using pandas
df = pd.DataFrame(data)
df.to_csv('G:/My Drive/csv/product.csv', index=False)


# import os
# import pygsheets
# from google.oauth2.service_account import Credentials


# # Authenticate using the local Google Sheets file
# credentials = Credentials.from_service_account_file(r"G:/My Drive/sito/test_product_list.gsheet")
# gc = pygsheets.authorize(custom_credentials=credentials)

# # Open the local Google Sheets file
# spreadsheet = gc.open_by_key('1NzDOaFMnEoKNILh6yDjFUjalj3stZxi0mZ7QjvVooXY')

# # Select a specific worksheet
# worksheet = spreadsheet.product  # Replace 'product' with the name of your worksheet

# # Export the worksheet as a Pandas DataFrame
# df = worksheet.get_as_df()

# # Export the DataFrame to a CSV file
# df.to_csv('output.csv', index=False)



# import gspread
# import pygsheets
# import pandas as pd

# # Authenticate with your service account JSON key
# gc = pygsheets.authorize(service_file='C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/src/core/smpos-403608-aa14a49badc1.json')

# # Open the Google Sheets file by its title or URL
# # Replace 'My Spreadsheet' with the actual title or URL of your Google Sheets file
# spreadsheet = gc.open('G:/My Drive/scan-it-to-office/test_product_list.gsheet')

# # Select a specific worksheet
# worksheet = spreadsheet.test_product_list  # Replace 'sheet1' with the name of your worksheet

# # Export the worksheet as a Pandas DataFrame
# df = worksheet.get_as_df()

# # Export the DataFrame to a CSV file
# df.to_csv('output.csv', index=False)

# print('sucess')
