from Frontend.UiMainWindow import *
from PySide6.QtWidgets import QMainWindow, QFileDialog, QDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.openAction.triggered.connect(self.OnOpen)

    def OnOpen(self, s):
        dlg = QFileDialog(self)
        dlg.setNameFilter(self.tr("Conan package gui manager files (*.cpcpp)"))
        dlg.setFileMode(QFileDialog.ExistingFile)
        # dlg.setDirectory(".")
        if dlg.exec_():
            fileName = dlg.selectedFiles()
            
