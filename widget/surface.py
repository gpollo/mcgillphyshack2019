from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPainter

class SurfaceWidget(QWidget):
    def __init__(self, surface):
        super().__init__()

        self.__surface = surface

    def paintEvent(self,event):
        w = self.__surface.get_width()
        h = self.__surface.get_height()       
        data = self.__surface.get_buffer().raw
        image = QImage(data, w, h, QImage.Format_ARGB32)

        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, image)
        painter.end()
