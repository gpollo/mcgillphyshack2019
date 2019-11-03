from matplotlib.pyplot import cm
from numpy import linspace

class AbstractModel(object):
    def __init__(self):
        self._points = set()
        self._indices = set()
        self.__amplitude_factor = 1
        self.__colors = [
            (int(c[0]*255), int(c[1]*255), int(c[2]*255))
            for c in cm.rainbow(linspace(0, 1, 10))
        ]

    def get_colors(self):
        return self.__colors

    def get_name(self):
        raise NotImplementedError

    def get_config_widgets(self):
        raise NotImplementedError

    def get_series(self):
        raise NotImplementedError

    def get_r(self):
        raise NotImplementedError

    def set_amplitude_factor(self, value):
        self.__amplitude_factor = value

    def get_amplitude_factor(self):
        return self.__amplitude_factor

    def add_point(self, i, p):
        self._points.add(p)
        self._indices.add(i)

    def remove_point(self, i, p):
        try:
            self._points.remove(p)
        except KeyError:
            pass

        try:
            self._indices.remove(i)
        except KeyError:
            pass

    def clear_points(self):
        points = set(self._points)
        for p in points:
            self.remove_point(p)

    def draw(self, surface, time):
        raise NotImplementedError
