class AbstractModel(object):
    def __init__(self):
        self._points = set()
        self.__amplitude_factor = 1

    def get_name(self):
        raise NotImplementedError

    def get_series(self):
        raise NotImplementedError

    def get_r(self):
        raise NotImplementedError

    def set_amplitude_factor(self, value):
        self.__amplitude_factor = value

    def get_amplitude_factor(self):
        return self.__amplitude_factor

    def add_point(self, p):
        self._points.add(p)

    def remove_point(self, p):
        try:
            self._points.remove(p)
        except KeyError:
            pass

    def clear_points(self):
        points = set(self._points)
        for p in points:
            self.remove_point(p)

    def draw(self, surface, time):
        raise NotImplementedError
