from sys import argv, exit
from widget.plot import PlotWidget

from PyQt5.QtWidgets import QWidget, QApplication, QSplitter, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.__widget_left = PlotWidget()
        self.__widget_right = PlotWidget()

        self.__splitter = QSplitter(Qt.Horizontal)
        self.__splitter.addWidget(self.__widget_left)
        self.__splitter.addWidget(self.__widget_right)

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.__splitter)
        self.setLayout(self.__layout)

app = QApplication(argv)
window = MainWindow()
window.setWindowTitle("test")
window.show()
exit(app.exec_())
