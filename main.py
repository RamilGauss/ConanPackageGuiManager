
import sys
from PySide6.QtCore import Qt
from Frontend.MainWindow import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())