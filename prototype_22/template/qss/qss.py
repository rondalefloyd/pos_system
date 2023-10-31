import os, sys

class MyQSSConfig:
    def __init__(self):
        self.file_paths()    

        self.file_names()
        self.field_indicator()
        self.color_scheme()
        self.nav_icon()
        self.act_icon()
        self.pos_icon()



    def file_paths(self):
        self.db_file_path = 'G:/My Drive/live_db/'

        self.csv_folder_path = 'G:/My Drive/csv/'

    def file_names(self):
        self.accounts_file_name = 'accounts.db'
        self.sales_file_name = 'sales.db'
        self.txn_file_name = 'txn.db'
        self.syslib_file_name = 'syslib.db'

        self.product_csv_name = 'product.csv'

    def field_indicator(self):
        self.inv_field_indicator = "<font color='red'>invalid</font>"
        self.req_field_indicator = "<font color='red'>required</font>"
        self.valid_points_indicator = "<font color='red'>required</font>"

    def color_scheme(self):
        self.main_color = '#ee4e34'
        self.main_color_alt = '#ddee4e34'
        self.secondary_color = '#fcedda'
        self.secondary_color_alt = '#ddfcedda'
        self.main_text_color = '#fff'
        self.secondary_text_color = '#222'

        self.navbar_bg_color = '#222'
        self.navbar_btn_txt_color = '#fff'
        self.navbar_btn_bg_color_alt = '#22ffffff'

        self.act_btn_txt_color = '#222'
        self.act_btn_bg_color = '#ddd'
        self.act_btn_bg_color_alt = '#33000000'

        self.act_neg_txt_color = '#fff'
        self.act_neg_bg_color = '#eb4034'
        self.act_neg_bg_color_alt = '#ddeb4034'

        self.act_pos_txt_color = '#fff'
        self.act_pos_bg_color = '#32a852'
        self.act_pos_bg_color_alt = '#dd32a852'

    def nav_icon(self):
        self.nav_product_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/nav/nav_product.png"
        self.nav_promo_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/nav/nav_promo.png"
        self.nav_reward_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/nav/nav_reward.png"
        self.nav_customer_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/nav/nav_customer.png"
        self.nav_user_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/nav/nav_user.png"

        self.nav_pos_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/nav/nav_pos.png"
        self.nav_transaction_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/nav/nav_transaction.png"

        self.nav_logout_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/nav/nav_logout.png"

    def act_icon(self):
        self.filter_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/filter_text.png"
        self.add_data_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/add_data.png"
        self.import_data_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/import_data.png"

        self.act_edit_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/act_edit.png"
        self.act_view_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/act_view.png"
        self.act_delete_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/act_delete.png"
        self.act_void_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/act_void.png"


    def pos_icon(self):
        self.toggle_barcode_scanner_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/untoggled_barcode_scan.png"
        self.untoggle_barcode_scanner_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/toggled_barcode_scan.png"

        self.add_products_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/act/add_products.png"


        self.product_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/product.png"
        self.promo_indicator_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/promo_indicator.png"
        self.out_of_stock_indicator_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/out_of_stock_indicator.png"

        self.retail_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/retail.png"
        self.wholesale_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/wholesale.png"
        self.dual_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/dual.png"

        self.drop_all_qty_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/drop_all_qty.png"
        self.drop_qty_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/drop_qty.png"
        self.add_qty_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/add_qty.png"
        self.edit_qty_icon = "C:/Users/Janjan/Documents/GitHub/pos_system/prototype_22/template/icon/pos/edit_qty.png"
