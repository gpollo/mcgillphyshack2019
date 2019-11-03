from sys import argv, exit
from widget.plot import PlotWidget
from widget.game import GameWidget
from game import Game
from pygame import init as pygame_init

from PyQt5.QtWidgets import QWidget, QApplication, QSplitter, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt, pyqtSlot

from model.one_dimension import OneDimensionalModelWrapper
from model.one_dimension import OneDimensionalModelWrapper2

class MainWindow(QWidget):
    def __init__(self, game):
        super().__init__()

        self.__game = game
        self.__widget_game = GameWidget(game)
        game.start(self.__widget_game)

        self.__selected_model = None
        self.__models = [
            OneDimensionalModelWrapper(),
            OneDimensionalModelWrapper2(),
            OneDimensionalModelWrapper(),
        ]
        self.__widget_plot = PlotWidget()
        self.__widget_model = QComboBox(self)
        self.__widget_model.currentIndexChanged.connect(self.model_changed)
        for model in self.__models:
            self.__widget_model.addItem(model.get_name())
        self.__widget_plot.point_selected.connect(self.point_selected)
        self.__widget_plot.point_unselected.connect(self.point_unselected)

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
        self.__selected_model = self.__models[index]
        self.__widget_plot.set_data_series(self.__selected_model.get_series())
        self.__game.set_model(self.__selected_model)

    def point_selected(self, x, y):
        if self.__selected_model is None:
            return
        self.__selected_model.add_point((x, y))

    def point_unselected(self, x, y):
        if self.__selected_model is None:
            return
        self.__selected_model.remove_point((x, y))

pygame_init()
game = Game()

app = QApplication(argv)
window = MainWindow(game)
window.setWindowTitle("test")
window.show()

app.exec_()
game.stop()
