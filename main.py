from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import PyQt5
from functools import partial
import typing
import sys
import pygame

from main_window import Ui_MainWindow
from image_widget import MemoryViewer
import parsing_api

all_states2 = []
curr_state2 = []
curr_state_cnt2 = 0
curr_line2 = -1


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

        # code editor
        self.ui.codeTextEdit.setText("int main() {\n    int a;\n a = 5;\n int *b = &a; \n int *c = malloc(5);\n"
                                     "*(c + 2) = 69;\n free(c);\n }") # postavlja text
        # print(self.ui.codeTextEdit.toPlainText()) # uzima text

        # buttons
        self.ui.button1.clicked.connect(partial(self.start))
        self.ui.button2.clicked.connect(partial(self.next_line))
        self.ui.button3.clicked.connect(partial(self.prev_line))
        self.ui.button4.clicked.connect(partial(self.openMemoryViewer))

        # variable viewer
        self.ui.varsTextView.setText("a = 5")

    def start(self):
        global all_states2, curr_state2, curr_state_cnt2
        all_states2.clear()
        curr_state2.clear()
        curr_state_cnt2 = 0
        code = self.ui.codeTextEdit.toPlainText()
        json2 = parsing_api.get_json_from_textarea(code)
        all_states2 = parsing_api.get_all_states1(json2)

    def next_line(self):
        global curr_state2, curr_state_cnt2, curr_line2
        if curr_state_cnt2 == len(all_states2):
            print("Nema vise stanja")
            return

        curr_state2 = all_states2[curr_state_cnt2]
        curr_state_cnt2 += 1
        curr_line2 = curr_state2[3]

        while curr_state_cnt2 < len(all_states2) \
                and all_states2[curr_state_cnt2][3] == curr_line2:
            curr_state2 = all_states2[curr_state_cnt2]
            curr_state_cnt2 += 1
            curr_line2 = curr_state2[3]

        print(curr_state2)

    def prev_line(self):
        global curr_state2, curr_state_cnt2, curr_line2
        if curr_state_cnt2 == 0:
            print("Dosli ste do pocetka programa")
            return

        curr_state_cnt2 -= 1

        curr_line2 = curr_state2[3]

        while curr_state_cnt2 >= 0 \
                and all_states2[curr_state_cnt2][3] == curr_line2:
            curr_state_cnt2 -= 1

        if curr_state_cnt2 < 0:
            curr_state_cnt2 = 0
            print("Dosli ste do pocetka programa")
            return

        curr_state2 = all_states2[curr_state_cnt2]

        curr_state_cnt2 += 1

        print(curr_state2)

        # 1 1 2 2 2 3 3 3 3 3 3 4 4 4 4 4

    def get_state(self):
        return curr_state2[0], curr_state2[1], curr_state2[2]


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
