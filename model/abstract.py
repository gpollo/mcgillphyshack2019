class AbstractModel(object):
    def __init__(self):
        self._points = set()

    def get_name(self):
        raise NotImplementedError

    def get_series(self):
        raise NotImplementedError

    def add_point(self, p):
        self._points.add(p)

    def remove_point(self, p):
        try:
            self._points.remove(p)
        except KeyError:
            pass

    def draw(self, surface, time):
        raise NotImplementedError
