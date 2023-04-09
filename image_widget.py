import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import pygame
import sys

class ImageWidget(QWidget):
    def __init__(self,surface,parent=None):
        super(ImageWidget,self).__init__(parent)
        self.w=surface.get_width()
        self.h=surface.get_height()
        self.data=surface.get_buffer().raw
        self.image=QImage(self.data,self.w,self.h,QImage.Format_RGB32)

    def update(self, surface):
        self.data = surface.get_buffer().raw
        self.image = QImage(self.data, self.w, self.h, QImage.Format_RGB32)

    def paintEvent(self,event):
        qp=QPainter()
        qp.begin(self)
        qp.drawImage(0,0,self.image)
        qp.end()

class MemoryViewer(QtWidgets.QDialog):
    def __init__(self,surface,parent=None):
        super(MemoryViewer,self).__init__(parent)
        self.setFixedWidth(300)
        self.setFixedHeight(900)
        self.surface=surface
        self.img=ImageWidget(self.surface)

        layout = QVBoxLayout()
        layout.addWidget(self.img)
        self.setLayout(layout)
        
        self.button = QPushButton('PyQt5 button', self)
        self.button.setToolTip('This is an example button')
        self.button.move(800, 70)

        self.button.clicked.connect(self.hagoAlgo)
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.hagoAlgo)
        #self.startTimer()

        self.mu=0

    def upd(self):
        s = pygame.Surface((640, 480))
        s.fill((64, 128, 192, 224))
        pygame.draw.circle(s, (55, 11, 55, 111), (self.mu, self.mu), 50)
        self.img.update(s)
        #self.img = ImageWidget(self.surface)

    def hagoAlgo(self):
        print("hago")
        self.mu += 1
        print(self.mu)
        self.upd()
        self.update()

    def startTimer(self):
        self.timer.start(1000)

    def endTimer(self):
        self.timer.stop()

if __name__ == '__main__':
    pygame.init()

    s = pygame.Surface((640, 480))
    s.fill((64, 128, 192, 224))
    pygame.draw.circle(s, (255, 255, 255, 255), (100, 100), 50)

    app = QApplication(sys.argv)
    w = MemoryViewer(s)
    w.show()
    app.exec_()