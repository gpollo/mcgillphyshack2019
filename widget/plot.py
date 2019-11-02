from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from bintrees import AVLTree
from math import sqrt

class LineMapper(object):
    def __init__(self, series):
        self.__x_tree = AVLTree()
        self.__y_tree = AVLTree()
        self.__mapping = {}
        
        for (line, (xs, ys)) in enumerate(series):
            for (point, (x, y)) in enumerate(zip(xs, ys)):
                self.__x_tree.insert(x, x)
                self.__y_tree.insert(y, y)

                if self.__mapping.get(x) is None:
                    self.__mapping[x] = {}

                if self.__mapping[x].get(y) is None:
                    self.__mapping[x][y] = []

                self.__mapping[x][y].append((line, point, x, y))

    def __euclidean_distance(self, x1, y1, x2, y2):
        return sqrt((x2-x1)**2 + (y2-y1)**2)

    def get_closests(self, x, y, radius=None):
        try:
            x_floor = self.__x_tree.floor_item(x)[0]
        except KeyError:
            x_floor = None

        try:
            y_floor = self.__y_tree.floor_item(y)[0]
        except KeyError:
            y_floor = None

        try:
            x_ceiling = self.__x_tree.ceiling_item(x)[0]
        except KeyError:
            x_ceiling = None

        try:
            y_ceiling = self.__y_tree.ceiling_item(y)[0]
        except KeyError:
            y_ceiling = None

        points = [
            (x_floor,   y_floor  ),
            (x_floor,   y_ceiling),
            (x_ceiling, y_floor  ),
            (x_ceiling, y_ceiling),
        ]
        points = filter(lambda p: p[0] is not None and p[1] is not None, points)
        points = filter(lambda p: self.__mapping.get(p[0]) != None, points)
        points = filter(lambda p: self.__mapping[p[0]].get(p[1]) != None, points)

        distances = [(self.__euclidean_distance(x, y, *p), *p) for p in points]
        if radius is not None:
            distances = filter(lambda d: d[0] < radius, distances)

        distances = list(distances)
        if len(distances) == 0:
            return None

        (x, y) = min(distances, key=lambda p: p[0])[1:]
        return self.__mapping[x][y]

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.__canvas.setStyleSheet("background-color:transparent;")
        self.__axes = self.__canvas.figure.subplots()
        self.__axes.plot([0,1,2,3,4], [0,1,0,1,0])

        self.__axes.figure.patch.set_alpha(0.5)
        self.__axes.figure.set_facecolor("None")
        self.__axes.patch.set_alpha(0.0)

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.__canvas)
        self.setLayout(self.__layout)

        # TODO: add signals for selection
        # TODO: add slots when changing plot data
