import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

from utils.widget.transact_widget import *

class TransactWindow(CustomGroupBox):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setTransactWindow()

    def showPanelC(self):
        self.panel_c = CustomGroupBox(reference='panel_c')
        self.panel_c_layout = QFormLayout()

        self.current_cart_table = CustomTableWidget()
        self.tendered_amount = CustomLineEdit()
        self.pre_amount_option = QGridLayout()
        self.option_a = CustomPushButton(text='5')
        self.option_b = CustomPushButton(text='10')
        self.option_c = CustomPushButton(text='20')
        self.option_d = CustomPushButton(text='50')
        self.option_e = CustomPushButton(text='100')
        self.option_f = CustomPushButton(text='200')
        self.option_g = CustomPushButton(text='500')
        self.option_h = CustomPushButton(text='1000')

        self.pre_amount_option.addWidget(self.option_a,0,0) 
        self.pre_amount_option.addWidget(self.option_b,0,1) 
        self.pre_amount_option.addWidget(self.option_c,0,2) 
        self.pre_amount_option.addWidget(self.option_d,0,3) 
        self.pre_amount_option.addWidget(self.option_e,1,0) 
        self.pre_amount_option.addWidget(self.option_f,1,1) 
        self.pre_amount_option.addWidget(self.option_g,1,2) 
        self.pre_amount_option.addWidget(self.option_h,1,3) 

        self.panel_c_layout.addRow(self.current_cart_table)
        self.panel_c_layout.addRow('tendered_amount', self.tendered_amount)
        self.panel_c_layout.addRow(self.pre_amount_option)

        self.panel_c.setLayout(self.panel_c_layout)

    def onPayTransactionButtonClicked(self):
        self.panel_b.hide()
        self.panel_c.show()

    def onCancelTransactionButtonClicked(self):
        self.transaction_tab.removeTab(self.transaction_tab.currentIndex())

    def onNewTransactionButtonClicked(self, transaction_name=''):
        name = 'Transaction' if transaction_name == '' else transaction_name

        self.showSubPanelA()
        self.transaction_tab.addTab(self.sub_panel_a, name)

    def showSubPanelA(self):
        self.sub_panel_a = CustomWidget()
        self.sub_panel_a_layout = QGridLayout()

        self.cart_table = CustomTableWidget(reference='cart_table')

        self.amount_list = QFormLayout()
        self.sub_total = CustomLabel(text='0.00')
        self.discount = CustomLabel(text='0.00')
        self.tax = CustomLabel(text='0.00')
        self.total = CustomLabel(text='0.00')

        self.amount_list.addRow('Subtotal:', self.sub_total)
        self.amount_list.addRow('Discount:', self.discount)
        self.amount_list.addRow('Tax:', self.tax)
        self.amount_list.addRow('Total:', self.total)

        self.pay_button = CustomPushButton(text='PAY')
        self.pay_button.clicked.connect(self.onPayTransactionButtonClicked)
        self.cancel_button = CustomPushButton(text='CANCEL')
        self.cancel_button.clicked.connect(self.onCancelTransactionButtonClicked)


        self.sub_panel_a_layout.addWidget(self.cart_table,0,0)
        self.sub_panel_a_layout.addLayout(self.amount_list,1,0)
        self.sub_panel_a_layout.addWidget(self.pay_button,2,0)
        self.sub_panel_a_layout.addWidget(self.cancel_button,3,0)

        self.sub_panel_a.setLayout(self.sub_panel_a_layout)

    def showPanelB(self): 
        self.panel_b = CustomGroupBox(reference='panel_b')
        self.panel_b_layout = QGridLayout()

        self.transaction_tab = CustomTabWidget()
        self.transaction_name = CustomLineEdit(placeholderText='Transaction Name')
        self.new_transaction_button = CustomPushButton(text='ADD')
        self.new_transaction_button.clicked.connect(lambda: self.onNewTransactionButtonClicked(str(self.transaction_name.text())))

        self.showSubPanelA()
        self.onNewTransactionButtonClicked()

        self.panel_b_layout.addWidget(self.new_transaction_button,0,0)
        self.panel_b_layout.addWidget(self.transaction_name,0,1)
        self.panel_b_layout.addWidget(self.transaction_tab,1,0,1,2)

        self.panel_b.setLayout(self.panel_b_layout)
        
    def showPanelA(self):
        self.panel_a = CustomGroupBox(reference='panel_a')
        self.panel_a_layout = QVBoxLayout()

        self.filter_field = CustomLineEdit(placeholderText='Filter item by...')
        self.list_table = CustomTableWidget()

        self.panel_a_layout.addWidget(self.filter_field)
        self.panel_a_layout.addWidget(self.list_table)

        self.panel_a.setLayout(self.panel_a_layout)

    def setTransactWindow(self):
        self.main_layout = QGridLayout()

        self.showPanelA()
        self.showPanelB()
        self.showPanelC()

        self.main_layout.addWidget(self.panel_a,0,0)
        self.main_layout.addWidget(self.panel_b,0,1)
        self.main_layout.addWidget(self.panel_c,0,2)

        self.setLayout(self.main_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = TransactWindow()
    window.show()
    sys.exit(pos_app.exec())

