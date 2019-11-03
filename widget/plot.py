from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from bintrees import AVLTree
from math import sqrt
from numpy import pi

rcParams["text.usetex"] = True
rcParams["font.family"] = "serif"
rcParams["font.weight"] = "bold"
rcParams["text.latex.preamble"] = [
    "\\usepackage[utf8]{inputenc}",
    "\\usepackage{amsmath}"
]

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

        self.__lines = []
        self.__mapper = None
        self.__model = None

        self.__canvas = FigureCanvas(Figure())
        self.__canvas.setStyleSheet("background-color:transparent;")
        self.__axes = self.__canvas.figure.subplots()
        self.__axes.figure.tight_layout(rect=(0.07, 0.06, 1.00, 1.00))
        self.__axes.figure.patch.set_alpha(0.5)
        self.__axes.figure.set_facecolor("None")
        self.__axes.set_xlabel(r"$k$", fontsize=20)
        self.__axes.set_ylabel(r"$\omega$", fontsize=20)
        self.__axes.patch.set_alpha(1.0)

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.__canvas)
        self.setLayout(self.__layout)

        self.__selected_points = {}
        self.__hovered_point = None

        self.__canvas.mpl_connect("button_press_event", self.__on_button_press)
        self.__canvas.mpl_connect("figure_leave_event", self.__on_figure_leave)
        self.__canvas.mpl_connect("motion_notify_event", self.__on_motion_notify)

    def set_model(self, model):
        self.__model = model
        self.__clear_selection()

        for line in self.__lines:
            line.remove()
        self.__lines.clear()

        for line in model.get_vertical_lines():
            self.__axes.axvline(x=line, color="black", linewidth=0.8, zorder=0)

        for (x, y) in model.get_series():
            line = self.__axes.scatter(x, y, zorder=1)
            self.__lines.append(line)

        self.__axes.set_xlim(*model.get_x_limits())
        self.__axes.set_xticks(model.get_x_ticks())
        self.__axes.set_xticklabels(model.get_x_ticklabels())

        self.__mapper = LineMapper(model.get_series())
        self.__canvas.draw()

    def __select_point(self, index, point):
        if (index, point) in self.__selected_points:
            return

        (x, y) = point
        self.__selected_points[(index, point)] = self.__axes.scatter(
            [x], [y], marker='o', s=50, color="blue"
        )
        self.__model.add_point(index, point)
        self.__canvas.draw()

    def __unselect_point(self, index, point):
        if (index, point) not in self.__selected_points:
            return

        self.__selected_points[(index, point)].remove()
        del self.__selected_points[(index, point)]
        self.__model.remove_point(index, point)
        self.__canvas.draw()

    def __clear_selection(self):
        points = dict(self.__selected_points)
        for (index, point) in points:
            self.__unselect_point(index, point)

    def __toggle_point(self, index, point):
        if (index, point) not in self.__selected_points:
            self.__select_point(index, point)
        else:
            self.__unselect_point(index, point)

    def __remove_hovered_point(self, draw=True):
        if self.__hovered_point is not None:
            self.__hovered_point.remove()
            self.__hovered_point = None
        if draw:
            self.__canvas.draw()

    def __set_hovered_point(self, point):
        (x, y) = point
        self.__remove_hovered_point(draw=False)
        self.__hovered_point = self.__axes.scatter([x], [y], marker='o', s=50, color="red")
        self.__canvas.draw()

    def __get_point_from_event(self, event):
        if self.__mapper is None:
            return (None, None)

        (x, y) = (event.xdata, event.ydata)
        if x is None or y is None:
            return (None, None)

        point = self.__mapper.get_closests(x, y, radius=1)
        if point is None:
            return (None, None)

        (_, index, x, y) = point[0]
        return (index, (x, y))

    def __on_button_press(self, event):
        (index, point) = self.__get_point_from_event(event)
        if point is None:
            return

        self.__toggle_point(index, point)

    def __on_figure_leave(self, event):
        self.__remove_hovered_point()       

    def __on_motion_notify(self, event):
        (_, point) = self.__get_point_from_event(event)
        if point is None:
            self.__remove_hovered_point()
            return

        self.__set_hovered_point(point)
