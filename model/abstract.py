from matplotlib.pyplot import cm
from numpy import linspace
from PyQt5.QtWidgets import QLabel, QSlider
from PyQt5.QtCore import Qt

class AbstractModel(object):
    def __init__(self):
        self._points = set()
        self._indices = set()
        self.__amplitude_factor = 1
        self.__colors = [
            (int(c[0]*255), int(c[1]*255), int(c[2]*255))
            for c in cm.rainbow(linspace(0, 1, 30))
        ]
        self.__model_changing_count = 0
        self.model_changing_callback = None

        self.__amplitude_factor_label = QLabel("Amplitude")
        self.__amplitude_factor_slider = QSlider(Qt.Horizontal)
        self.__amplitude_factor_slider.setMinimum(0)
        self.__amplitude_factor_slider.setMaximum(100)
        self.__amplitude_factor_slider.valueChanged.connect(self.amplitude_factor_changed)
        self.__amplitude_factor_slider.setValue(75)

    def get_colors(self):
        return self.__colors

    def get_name(self):
        raise NotImplementedError

    def get_config_widgets(self):
        return [
            self.__amplitude_factor_label,
            self.__amplitude_factor_slider,
        ]

    def get_series(self):
        raise NotImplementedError

    def get_r(self):
        raise NotImplementedError

    def get_x_limits(self):
        raise NotImplementedError

    def get_x_ticks(self):
        raise NotImplementedError

    def get_x_ticklabels(self):
        raise NotImplementedError

    def get_vertical_lines(self):
        raise NotImplementedError

    def amplitude_factor_changed(self, value):
        self.__amplitude_factor = value / 100

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

    def model_changing_push(self):
        self.__model_changing_count += 1
        if self.model_changing_callback is not None:
            self.model_changing_callback(self, True)

    def model_changing_pop(self):
        self.__model_changing_count -= 1
        if self.__model_changing_count == 0:
            if self.model_changing_callback is not None:
                self.model_changing_callback(self, False)
