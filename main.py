from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import PyQt5
from functools import partial
import typing
import sys

from main_window import Ui_MainWindow
from image_widget import MemoryViewer
import parsing_api

from pygame_visualizer import *

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
        self.ui.codeTextEdit.setText("int main() {\n int a;\n a = 5;\n int *b = &a; \n int *c = malloc(5);\n"
                                     "*(c + 2) = 69;\n free(c);\n }") # postavlja text
        # print(self.ui.codeTextEdit.toPlainText()) # uzima text

        # buttons
        self.ui.button1.clicked.connect(partial(self.start))
        self.ui.button2.clicked.connect(partial(self.next_line))
        self.ui.button3.clicked.connect(partial(self.prev_line))
        self.ui.button4.clicked.connect(partial(self.openMemoryViewer))

        # variable viewer
        self.ui.varsTextView.setText("")

        # self.currline = None

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

        print(curr_state2[3], curr_state2)
        self.render_code_view(curr_state2[3])
        self.update_variblae_view()

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

        print(curr_state2[3],  curr_state2)
        self.render_code_view(curr_state2[3])
        self.update_variblae_view()

        # 1 1 2 2 2 3 3 3 3 3 3 4 4 4 4 4

    def get_state(self):
        return curr_state2[0], curr_state2[1], curr_state2[2]

    def update_variblae_view(self):
        text = ""
        memory, names, heap = self.get_state()
        for name in names:
            text += f"{names[name][2]} {name}, {names[name][0]}\n"
        self.ui.varsTextView.setText(text)

    def render_code_view(self, currline=None):
        if not currline:
            return
        currline = int(currline)
        text = self.ui.codeTextEdit.toPlainText()
        text = text.replace('➡️','')
        lines = [line for line in text.split('\n')]
        print(lines)
        lines[currline-1] = '➡️' + lines[currline-1]
        self.ui.codeTextEdit.setText('\n'.join(lines))

    def openMemoryViewer(self):
        print('Opening memory visualizer')
        v = Visualizer(self.get_state())
        v.mainloop()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PointerExplorer()
    window.show()

    sys.exit(app.exec())
