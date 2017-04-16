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
from PyQt5.QtGui import QPainter
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
        self.data = []
        self.index = 0

        self.series = QSplineSeries()
        self.view = QChartView()
        self.glMain = QGridLayout()

        self.glMain.addWidget(self.view, 0, 0)
        self.setupSerialPanel()
        self.setupButtons()

        wCenter = QWidget()
        wCenter.setLayout(self.glMain)

        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(wCenter)
        self.setup()

        self.timer = QTimer()
        self.timer.setInterval(500)
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
        # print(len(self.data) % 10 * 10)
        self.setup(len(self.data) // 10 * 10, (len(self.data) // 10 + 1) * 10)

    def recieve_data(self):
        with open('input.txt') as file:
            number = int(file.readline())
            self.addPoint(self.index, number)
            self.index += 1

    def getXAxis(self, start=0, end=10):
        axisX = QValueAxis()
        axisX.setLabelFormat("%i")
        axisX.setTickCount(10)
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
