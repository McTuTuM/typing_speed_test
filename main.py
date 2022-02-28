from PyQt5 import QtWidgets
from typing_speed_test import Window
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.show()
    sys.exit(app.exec_())