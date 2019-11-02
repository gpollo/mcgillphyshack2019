from sys import argv, exit
from widget.plot import PlotWidget
from widget.surface import SurfaceWidget
from game import Game
from pygame import init as pygame_init

from PyQt5.QtWidgets import QWidget, QApplication, QSplitter, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, game):
        super().__init__()

        self.__game = game
        self.__widget_left = SurfaceWidget(self.__game.get_surface())
        self.__widget_right = PlotWidget()
        self.__game.start(self.__widget_left)

        self.__splitter = QSplitter(Qt.Horizontal)
        self.__splitter.addWidget(self.__widget_left)
        self.__splitter.addWidget(self.__widget_right)

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.__splitter)
        self.setLayout(self.__layout)

pygame_init()
game = Game()

app = QApplication(argv)
window = MainWindow(game)
window.setWindowTitle("test")
window.show()

app.exec_()
game.stop()
