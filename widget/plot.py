from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QHBoxLayout

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.__axes = self.__canvas.figure.subplots()
        self.__axes.plot([0,1,2,3,4], [0,1,0,1,0])

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.__canvas)
        self.setLayout(self.__layout)

        # TODO: add signals for selection
        # TODO: add slots when changing plot data
