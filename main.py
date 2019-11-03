from sys import argv, exit
from widget.plot import PlotWidget
from widget.game import GameWidget
from game import Game
from pygame import init as pygame_init

from PyQt5.QtWidgets import QWidget, QApplication, QSplitter, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox, QGroupBox, QSlider
from PyQt5.QtCore import Qt

from model.one_dimension import OneDimensionalModelWrapper
from model.one_dimension import OneDimensionalModelWrapper2

class MainWindow(QWidget):
    def __init__(self, game):
        super().__init__()

        self.__model = None
        self.__game = game
        self.__game_widget = GameWidget(game)
        self.__game_widget.setSizePolicy(QSizePolicy(
            QSizePolicy.Expanding, 
            QSizePolicy.Expanding
        ))
        game.start(self.__game_widget)

        self.__models = [
            OneDimensionalModelWrapper(),
            OneDimensionalModelWrapper2(),
            OneDimensionalModelWrapper(),
        ]

        self.__model_plot = PlotWidget()

        self.__model_label = QLabel("Model")
        self.__model_selector = QComboBox(self)

        self.__amplitude_label = QLabel("Amplitude")
        self.__amplitude_slider = QSlider(Qt.Horizontal)

        self.__config_layout = QGridLayout(self)
        self.__config_layout.setColumnStretch(1, 2)
        self.__config_layout.setColumnStretch(1, 2)
        self.__config_layout.addWidget(self.__model_label)
        self.__config_layout.addWidget(self.__model_selector)
        self.__config_layout.addWidget(self.__amplitude_label)
        self.__config_layout.addWidget(self.__amplitude_slider)
        self.__config_widget = QGroupBox(self)
        self.__config_widget.setLayout(self.__config_layout)

        self.__left_side_layout = QVBoxLayout(self)
        self.__left_side_layout.addWidget(self.__config_widget)
        self.__left_side_layout.addWidget(self.__game_widget)
        self.__left_side_widget = QWidget(self)
        self.__left_side_widget.setLayout(self.__left_side_layout)

        self.__splitter = QSplitter(Qt.Horizontal)
        self.__splitter.addWidget(self.__left_side_widget)
        self.__splitter.addWidget(self.__model_plot)

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.__splitter)
        self.setLayout(self.__layout)

        self.__amplitude_slider.valueChanged.connect(self.amplitude_changed)
        self.__amplitude_slider.setValue(75)
        self.__model_selector.currentIndexChanged.connect(self.model_changed)
        for model in self.__models:
            self.__model_selector.addItem(model.get_name())

    def model_changed(self, index):
        model = self.__models[index]
        model.clear_points()
        self.__model = model
        self.__model_plot.set_model(model)
        self.__model.set_amplitude_factor(self.__amplitude_slider.value() / 100)
        self.__game.set_model(model)

    def amplitude_changed(self, value):
        if self.__model is None:
            return

        self.__model.set_amplitude_factor(value / 100)

pygame_init()
game = Game()

app = QApplication(argv)
window = MainWindow(game)
window.setWindowTitle("test")
window.show()

app.exec_()
game.stop()
