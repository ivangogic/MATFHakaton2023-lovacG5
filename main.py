from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import PyQt5
from functools import partial
import typing
import sys
import pygame

from main_window import Ui_MainWindow
from image_widget import MemoryViewer

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

class PointerExplorer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # buttons
        self.ui.button1.clicked.connect(partial(print, "start clicked"))
        self.ui.button2.clicked.connect(partial(print, "next line clicked"))
        self.ui.button3.clicked.connect(partial(self.openMemoryViewer))

        # code editor
        self.ui.codeTextEdit.setText("linija 1\nlinija 2") # postavlja text
        print(self.ui.codeTextEdit.toPlainText()) # uzima text

        # variable viewer
        self.ui.varsTextView.setText("a = 5")

    def openMemoryViewer(self):
        print("START")
        s = pygame.Surface((640, 480))
        s.fill((64, 128, 192, 224))
        pygame.draw.circle(s, (255, 255, 255, 255), (100, 100), 50)
        self.w = MemoryViewer(s)
        self.w.show()
        # s = pygame.Surface((640, 480))
        # s.fill((64, 128, 192, 224))
        # pygame.draw.circle(s, (255, 255, 255, 255), (100, 100), 50)
        # dialog.ui = MemoryViewer(s)
        # # dialog.ui.setupUi()
        # dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PointerExplorer()
    window.show()

    sys.exit(app.exec())
