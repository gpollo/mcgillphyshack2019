from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QObject, pyqtSlot
from pygame import transform

class GameWidget(QWidget):
    def __init__(self, game):
        super().__init__()

        self.__game = game

    def resizeEvent(self, event):
        (w, h) = (event.size().width(), event.size().height())
        self.__game.resize_surface(w, h)
        return super(GameWidget, self).resizeEvent(event)

    def paintEvent(self,event):
        surface = self.__game.get_surface()

        w = surface.get_width()
        h = surface.get_height()       
        data = surface.get_buffer().raw
        image = QImage(data, w, h, QImage.Format_ARGB32)

        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, image)
        painter.end()

    @pyqtSlot(QObject)
    def change_model(self, model):
        self.__game.set_model(model)
        
