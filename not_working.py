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

from PyQt5.QtChart import QChart, QChartView, QSplineSeries, QValueAxis
from PyQt5.QtCore import QPointF, Qt, QRunnable, pyqtSlot, QThreadPool, QTimer
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QGridLayout, QHBoxLayout,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget)


class Worker(QRunnable):
    def __init__(self, application=None):
        super(Worker, self).__init__()
        self.application = application

    @pyqtSlot()
    def run(self):
        index = 0

        while True:
            with open('input.txt') as file:
                number = int(file.readline())
                self.application.addPoint(index, number)

            index += 1
            sleep(0.1)


class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)

        self.glMain = QGridLayout()
        wCenter = QWidget()
        wCenter.setLayout(self.glMain)

        self.series = QSplineSeries()

        pen = QPen(Qt.green)
        pen.setWidth(1)
        self.series.setPen(pen)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("QT Charts example")

        axisX = self.getXAxis()
        self.chart.setAxisX(axisX)
        self.series.attachAxis(axisX)

        axisY = self.getYAxis()
        self.chart.setAxisY(axisY)
        self.series.attachAxis(axisY)

        view = QChartView()
        view.setRenderHint(QPainter.Antialiasing)
        view.setChart(self.chart)

        self.glMain.addWidget(view, 0, 0)
        self.setupSerialPanel()
        self.setupButtons()

        self.setCentralWidget(wCenter)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.recieve_data)
        self.timer.start()

    def setupSerialPanel(self):
        cbSerial1 = QCheckBox('Serial 1')
        cbSerial2 = QCheckBox('Serial 2')
        cbSerial3 = QCheckBox('Serial 3')
        cbSerial4 = QCheckBox('Serial 4')

        cbType = QComboBox()
        cbType.addItems(['Temperature', 'Humidity'])

        glSerial = QVBoxLayout()

        glSerial.addWidget(cbSerial1)
        glSerial.addWidget(cbSerial2)
        glSerial.addWidget(cbSerial3)
        glSerial.addWidget(cbSerial4)
        glSerial.addWidget(cbType)

        self.glMain.addLayout(glSerial, 0, 1)

    def setupButtons(self):
        pbStart = QPushButton('Start')
        pbStop = QPushButton('Stop')
        pbClear = QPushButton('Clear')
        pbSave = QPushButton('Save')
        pbClose = QPushButton('Close')

        glButtons = QHBoxLayout()

        glButtons.addWidget(pbStart)
        glButtons.addWidget(pbStop)
        glButtons.addWidget(pbSave)
        glButtons.addWidget(pbClear)
        glButtons.addWidget(pbClose)

        self.glMain.addLayout(glButtons, 1, 0, 1, 2)

    def setup(self, start=0, end=20):
        # self.chart.scroll(start, 0)
        axisX = self.getXAxis(start, end)
        self.chart.setAxisX(axisX)

    def addPoint(self, x, y):
        if self.series.count() == 19:
            self.series.replace([QPointF(x, y)])
        else:
            self.series.append(QPointF(x, y))

        self.setup(
            start=self.series.count() // 20 * 20,
            end=(self.series.count() // 20 + 1) * 20
        )

    def recieve_data(self):
        with open('input.txt') as file:
            number = int(file.readline())
            self.addPoint(self.series.count(), number)

    def getXAxis(self, start=0, end=20):
        axisX = QValueAxis()
        axisX.setLabelFormat("%i")
        axisX.setTickCount(20)
        axisX.setRange(start, end)
        axisX.setTitleText("Date")
        return axisX

    def getYAxis(self):
        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTickCount(10)
        axisY.setRange(0, 100)
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

    # threadpool = QThreadPool()
    # worker = Worker(application=window)
    # threadpool.start(worker)

    sys.exit(app.exec_())
