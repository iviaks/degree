# processEvents


# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with
a high number of points, using OpenGL accelerated series
"""

import numpy as np
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtWidgets import QMainWindow
from time import sleep


def series_to_polyline(xdata, ydata):
    """Convert series data to QPolygon(F) polyline

    This code is derived from PythonQwt's function named
    `qwt.plot_curve.series_to_polyline`"""
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size-1)*2+1:2] = xdata
    memory[1:(size-1)*2+2:2] = ydata
    return polyline


class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.view = QChartView()
        self.series = QLineSeries()
        self.view.chart().legend().hide()
        self.view.chart().addSeries(self.series)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)

    def add_point(self, x, y):
        self.series.append(x, y)
        self.view.chart().createDefaultAxes()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = TestWindow()
    window.setWindowTitle("Simple performance example")
    window.show()
    window.resize(500, 400)

    for index in range(200):
        window.add_point(index, index)
        app.processEvents()

    sys.exit(app.exec_())
