# processEvents


# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with
a high number of points, using OpenGL accelerated series
"""

from time import sleep

from PyQt5.QtChart import (QChart, QChartView, QDateTimeAxis, QLineSeries,
                           QValueAxis)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtWidgets import QMainWindow


class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.last = (0, 0)
        self.series = QLineSeries()
        self.view = QChartView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        self.setup()

    def setup(self):
        chart = QChart()
        chart.setTitle("QT Charts example")
        chart.addSeries(self.series)

        axisX = self.getXAxis()
        axisY = self.getYAxis()

        self.series.attachAxis(axisX)
        chart.addAxis(axisX, Qt.AlignBottom)

        self.series.attachAxis(axisY)
        chart.addAxis(axisY, Qt.AlignLeft)

        self.view.setChart(chart)

    def add_point(self):
        self.last = (self.last[0] + 1, self.last[1] + 2)
        self.series.append(*self.last)
        self.setup()

    def getXAxis(self):
        axisX = QDateTimeAxis()
        axisX.setTickCount(10)
        axisX.setFormat("MMM yyyy")
        axisX.setTitleText("Date")
        return axisX

    def getYAxis(self):
        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTitleText("Money")
        return axisY


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = TestWindow()
    window.setWindowTitle("Simple performance example")
    window.show()
    window.resize(500, 400)

    # for _ in range(10):
    #     window.add_point()
    #     app.processEvents()

    sys.exit(app.exec_())
