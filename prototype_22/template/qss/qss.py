import os, sys

class MyQSSConfig:
    db_file_path = 'G:' + f"/My Drive/database/"

    csv_folder_path = 'G:' + f"/My Drive/csv/"    

    accounts_file_name = 'accounts.db'
    sales_file_name = 'sales.db'
    txn_file_name = 'txn.db'
    syslib_file_name = 'syslib.db'

    product_csv_name = 'product.csv'

    inv_field_indicator = "<font color='red'>invalid</font>"
    req_field_indicator = "<font color='red'>required</font>"
    valid_points_indicator = "<font color='red'>required</font>"

    product_icon = os.path.abspath("template/icon/pos/product.png")
    promo_indicator_icon = os.path.abspath("template/icon/pos/promo_indicator.png")
    out_of_stock_indicator_icon = os.path.abspath("template/icon/pos/out_of_stock_indicator.png")
    
    retail_icon = os.path.abspath("template/icon/pos/retail.png")
    wholesale_icon = os.path.abspath("template/icon/pos/wholesale.png")
    dual_icon = os.path.abspath("template/icon/pos/dual.png")

    drop_all_qty_icon = os.path.abspath("template/icon/pos/drop_all_qty.png")
    drop_qty_icon = os.path.abspath("template/icon/pos/drop_qty.png")
    add_qty_icon = os.path.abspath("template/icon/pos/add_qty.png")
    edit_qty_icon = os.path.abspath("template/icon/pos/edit_qty.png")