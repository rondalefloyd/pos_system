import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class MyDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(MyDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, index)
        painter.setPen(QColor('red'))  # set the color
        painter.drawRect(option.rect)  # draw a rectangle at the top and bottom of the cell

class PromoManagementLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.createLayout()
    
    def showPanelA(self):
        self.panel_a = QGroupBox()
        hbox_layout = QHBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(5)
        self.table.setShowGrid(False)
        self.table.setItemDelegateForRow(0, MyDelegate())
        self.table.setStyleSheet("""
            QTableWidget::item {
                border-bottom: 1px solid black;
            }
        """)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.verticalHeader().setVisible(False)



        text = QLabel('texttexttexttexttexttexttexttext')
        self.table.setCellWidget(0,0,text)
        

        hbox_layout.addWidget(self.table)

        self.panel_a.setLayout(hbox_layout)

    def createLayout(self):
        grid_layout = QGridLayout()

        self.showPanelA()

        grid_layout.addWidget(self.panel_a,0,0)

        self.setLayout(grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoManagementLayout()
    window.show()
    sys.exit(pos_app.exec())
