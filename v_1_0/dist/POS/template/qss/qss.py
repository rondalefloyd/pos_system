import os, sys

cwd = os.getcwd() # get current working dir
sys.path.append(os.path.join(cwd))

class MyQSSConfig:
    def __init__(self):
        self.file_paths()    

        self.file_names()
        self.field_indicator()
        self.color_scheme()
        self.main_icon()
        self.field_icon()
        self.nav_icon()
        self.act_icon()
        self.pos_icon()
        self.font_family()

    def font_family(self):
        self.global_font = 'Bahnschrift'

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
        self.main_color = '#2F3C7E'
        self.main_color_alt = '#dd2F3C7E'
        self.secondary_color = '#FBEAEB'
        self.secondary_color_alt = '#ddFBEAEB'
        self.main_txt_color = '#fff'
        self.default_panel_color = '#fff'
        self.default_line_color = '#ccc'
        self.secondary_txt_color = '#222'
        self.disabled_bg_color = '#aaa'

        self.navbar_bg_color = '#222'
        self.navbar_btn_txt_color = '#fff'
        self.navbar_btn_bg_color_alt = '#22ffffff'

        self.act_btn_txt_color = '#222'
        self.act_btn_bg_color = '#ddd'
        self.act_btn_bg_color_alt = '#33000000'

        self.act_neg_txt_color = '#fff'
        self.act_neg_bg_color = '#e60000'
        self.act_neg_bg_color_alt = '#aae60000'

        self.act_pos_txt_color = '#fff'
        self.act_pos_bg_color = '#32a852'
        self.act_pos_bg_color_alt = '#dd32a852'

        self.act_pas_txt_color = '#fff'
        self.act_pas_bg_color = '#33ffffff'
        self.act_pas_bg_color_alt = '#33000000'

        self.act_sm_neg_txt_color = '#fff'
        self.act_sm_neg_bg_color = '#eb9e34'
        self.act_sm_neg_bg_color_alt = '#aaeb9e34'

        self.act_clr_txt_color = '#fff'
        self.act_clr_bg_color = '#cf9500'
        self.act_clr_bg_color_alt = '#aacf9500'

    def main_icon(self):
        self.app_icon = os.path.join(cwd,'template','icon','app.ico')

    def field_icon(self):
        self.main_drop_down_arrow_icon = os.path.join(cwd,'template','icon','fields','main_drop_down_arrow.png')
        self.secondary_drop_down_arrow_icon = os.path.join(cwd,'template','icon','fields','secondary_drop_down_arrow.png')


    def nav_icon(self):
        self.nav_product_icon = os.path.join(cwd,'template','icon','nav','nav_product.png')
        self.nav_promo_icon = os.path.join(cwd,'template','icon','nav','nav_promo.png')
        self.nav_reward_icon = os.path.join(cwd,'template','icon','nav','nav_reward.png')
        self.nav_customer_icon = os.path.join(cwd,'template','icon','nav','nav_customer.png')
        self.nav_user_icon = os.path.join(cwd,'template','icon','nav','nav_user.png')

        self.nav_pos_icon = os.path.join(cwd,'template','icon','nav','nav_pos.png')
        self.nav_transaction_icon = os.path.join(cwd,'template','icon','nav','nav_transaction.png')

        self.nav_logout_icon = os.path.join(cwd,'template','icon','nav','nav_logout.png')

    def act_icon(self):
        self.filter_icon = os.path.join(cwd,'template','icon','act','filter_text.png')
        self.sync_icon = os.path.join(cwd,'template','icon','act','sync.png')
        self.add_data_icon = os.path.join(cwd,'template','icon','act','add_data.png')
        self.import_data_icon = os.path.join(cwd,'template','icon','act','import_data.png')

        self.act_edit_icon = os.path.join(cwd,'template','icon','act','act_edit.png')
        self.act_view_icon = os.path.join(cwd,'template','icon','act','act_view.png')
        self.act_delete_icon = os.path.join(cwd,'template','icon','act','act_delete.png')
        self.act_void_icon = os.path.join(cwd,'template','icon','act','act_void.png')

    def pos_icon(self):
        self.toggle_barcode_scanner_icon = os.path.join(cwd,'template','icon','act','untoggled_barcode_scan.png')
        self.untoggle_barcode_scanner_icon = os.path.join(cwd,'template','icon','act','toggled_barcode_scan.png')

        self.add_order_icon = os.path.join(cwd,'template','icon','act','add_order.png')

        self.add_products_icon = os.path.join(cwd,'template','icon','act','add_products.png')

        self.clear_table_icon = os.path.join(cwd,'template','icon','act','clear_table.png')

        self.locked_icon = os.path.join(cwd,'template','icon','act','locked.png')
        self.unlocked_icon = os.path.join(cwd,'template','icon','act','unlocked.png')
        self.pay_order_icon = os.path.join(cwd,'template','icon','act','pay_order.png')

        self.product_icon = os.path.join(cwd,'template','icon','pos','product.png')
        self.product_promo_indicator_icon = os.path.join(cwd,'template','icon','pos','promo_indicator.png')
        self.out_of_stock_indicator_icon = os.path.join(cwd,'template','icon','pos','out_of_stock_indicator.png')

        self.retail_icon = os.path.join(cwd,'template','icon','pos','retail.png')
        self.wholesale_icon = os.path.join(cwd,'template','icon','pos','wholesale.png')
        self.dual_icon = os.path.join(cwd,'template','icon','pos','dual.png')

        self.drop_all_qty_icon = os.path.join(cwd,'template','icon','pos','drop_all_qty.png')
        self.drop_qty_icon = os.path.join(cwd,'template','icon','pos','drop_qty.png')
        self.add_qty_icon = os.path.join(cwd,'template','icon','pos','add_qty.png')
        self.edit_qty_icon = os.path.join(cwd,'template','icon','pos','edit_qty.png')

        self.toggle_numpad_icon = os.path.join(cwd,'template','icon','act','toggled_numpad.png')
        self.untoggle_numpad_icon = os.path.join(cwd,'template','icon','act','untoggled_numpad.png')

        self.pay_cash_points_icon = os.path.join(cwd,'template','icon','pos','pay_cash_points.png')
        self.pay_points_icon = os.path.join(cwd,'template','icon','pos','pay_points.png')
        self.pay_cash_icon = os.path.join(cwd,'template','icon','pos','pay_cash.png')

        self.print_receipt_icon = os.path.join(cwd,'template','icon','act','print_receipt.png')