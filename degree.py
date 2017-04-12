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
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtWidgets import QMainWindow


class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.series = QLineSeries()
        self.view = QChartView()
        self.data = []
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        self.setup()

    def setup(self):
        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("QT Charts example")

        axisX = self.getXAxis()
        chart.addAxis(axisX, Qt.AlignBottom)
        self.series.attachAxis(axisX)

        axisY = self.getYAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        self.series.attachAxis(axisY)
        self.view.setChart(chart)

    def addPoint(self, x, y):
        self.data[0:10] = self.data[0:9] + [QPointF(x, y)]
        print(len(self.data))
        self.series.replace(self.data)
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

    from random import randint

    for index in range(0, 20):
        window.addPoint(index, randint(0, 10))
        app.processEvents()

    sys.exit(app.exec_())
