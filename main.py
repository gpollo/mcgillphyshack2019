from sys import argv, exit
from widget.plot import PlotWidget
from widget.game import GameWidget
from game import Game
from pygame import init as pygame_init

from PyQt5.QtWidgets import QWidget, QApplication, QSplitter, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt

from model.one_dimension import OneDimensionalModelWrapper

class MainWindow(QWidget):
    def __init__(self, game):
        super().__init__()

        self.__game = game
        self.__widget_game = GameWidget(game)
        game.start(self.__widget_game)

        self.__models = [
            OneDimensionalModelWrapper(),
            OneDimensionalModelWrapper(),
            OneDimensionalModelWrapper(),
        ]
        self.__widget_plot = PlotWidget()
        self.__widget_model = QComboBox(self)
        self.__widget_model.currentIndexChanged.connect(self.model_changed)
        for model in self.__models:
            self.__widget_model.addItem(model.get_name())

        self.__layout_vertical = QVBoxLayout(self)
        self.__layout_vertical.addWidget(self.__widget_model)
        self.__layout_vertical.addWidget(self.__widget_plot)
        self.__widget_right = QWidget(self)
        self.__widget_right.setLayout(self.__layout_vertical)

        self.__splitter = QSplitter(Qt.Horizontal)
        self.__splitter.addWidget(self.__widget_game)
        self.__splitter.addWidget(self.__widget_right)

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.__splitter)
        self.setLayout(self.__layout)

    def model_changed(self, index):
        model = self.__models[index]
        model.clear_points()
        self.__widget_plot.set_model(model)
        self.__game.set_model(model)

pygame_init()
game = Game()

app = QApplication(argv)
window = MainWindow(game)
window.setWindowTitle("test")
window.show()

app.exec_()
game.stop()
