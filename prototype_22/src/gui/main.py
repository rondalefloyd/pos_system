import sys, os
from PyQt6.QtCore import *

sys.path.append(os.path.abspath(''))

from src.gui.login.login import *

if __name__ == ('__main__'):
    login_app = QApplication(sys.argv)
    
    model = MyLoginModel()
    view = MyLoginView(model)
    controller = MyLoginController(model, view)
    
    view.show()

    sys.exit(login_app.exec())
