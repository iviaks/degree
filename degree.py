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

from PyQt5.QtChart import (QChart, QChartView, QDateTimeAxis, QSplineSeries,
                           QValueAxis)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtWidgets import QMainWindow


class TestWindow(QMainWindow):
    def __init__(self, parent=None, app=None):
        super(TestWindow, self).__init__(parent=parent)
        self.series = QSplineSeries()
        self.view = QChartView()
        self.data = []
        self.app = app
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        self.setup()

    def setup(self, start=0, end=10):
        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("QT Charts example")

        axisX = self.getXAxis(start, end)
        chart.addAxis(axisX, Qt.AlignBottom)
        self.series.attachAxis(axisX)

        axisY = self.getYAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        self.series.attachAxis(axisY)
        self.view.setChart(chart)

    def addPoint(self, x, y):
        self.data.append(QPointF(x, y))
        self.series.replace(self.data)
        print(len(self.data) % 10 * 10)
        self.setup(len(self.data) // 10 * 10, (len(self.data) // 10 + 1) * 10)
        self.app.processEvents()
        sleep(0.1)

    def getXAxis(self, start=0, end=10):
        axisX = QValueAxis()
        axisX.setLabelFormat("%i")
        axisX.setRange(start, end)
        axisX.setTitleText("Date")
        return axisX

    def getYAxis(self):
        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTickCount(10)
        axisY.setTitleText("Money")
        return axisY


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = TestWindow(app=app)
    window.setWindowTitle("Simple performance example")
    window.show()
    window.resize(500, 400)

    from random import randint

    for index in range(200):
        window.addPoint(index, randint(0, 100))

    sys.exit(app.exec_())
