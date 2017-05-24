# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Saykov Max


from time import sleep

from PyQt5.QtChart import QChart, QChartView, QSplineSeries, QValueAxis
from PyQt5.QtCore import (QPointF, QRunnable, Qt, QThread, QThreadPool, QTimer,
                          QTimerEvent, pyqtSlot)
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QGridLayout,
                             QHBoxLayout, QMainWindow, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)


def recieve_data():
    with open('input.txt') as file:
        return int(file.readline())


class CustomChartView(QChartView):
    def __init__(self, *args, **kwargs):
        self.index = 0
        return super(CustomChartView, self).__init__(*args, **kwargs)

    def setWidget(self, widget=None):
        self.widget = widget

    def timerEvent(self, *args):
        self.widget.addPoint(self.index, recieve_data())
        self.index += 1


class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.series = [QSplineSeries() for index in range(4)]
        self.series[0].setPen(QPen(Qt.red))
        self.series[1].setPen(QPen(Qt.green))
        self.series[2].setPen(QPen(Qt.blue))
        self.series[3].setPen(QPen(Qt.yellow))
        for series in self.series:
            series.setUseOpenGL(True)
        self.view = CustomChartView()
        self.glMain = QGridLayout()

        self.glMain.addWidget(self.view, 0, 0)
        self.setupSerialPanel()
        self.setupButtons()

        wCenter = QWidget()
        wCenter.setLayout(self.glMain)

        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(wCenter)
        self.setup()

        self.view.setWidget(self)
        self.view.startTimer(1000)

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

    def setPoints(self):
        from random import randint
        for i, series in enumerate(self.series):
            arr = [QPointF(index, 50) for index in range(21)]
            if i == 0:
                arr[10] = QPointF(10, 53)
                # arr[11] = QPointF(11, randint(24, 26))
                arr[11] = QPointF(11, 70)
            series.replace(arr)

    def setup(self, start=0, end=20):
        chart = QChart()
        axisX = self.getXAxis(start, end)
        chart.setTitle("Humidity graph")
        chart.addAxis(axisX, Qt.AlignBottom)

        axisY = self.getYAxis()
        chart.addAxis(axisY, Qt.AlignLeft)

        for series in self.series:
            chart.addSeries(series)
            series.attachAxis(axisX)
            series.attachAxis(axisY)

        self.view.setChart(chart)

    def addPoint(self, x, y):
        self.series[0].append(QPointF(x, y))
        self.setup(
            start=self.series[0].count() // 20 * 20,
            end=(self.series[0].count() // 20 + 1) * 20
        )

    def recieve_data(self):
        file = open('input.txt')
        number = int(file.readline())
        file.close()
        self.addPoint(self.series[0].count(), number)

    def getXAxis(self, start=0, end=20):
        axisX = QValueAxis()
        axisX.setLabelFormat("%i")
        axisX.setTickCount(20)
        axisX.setRange(start, end)
        axisX.setTitleText("Time, s")
        return axisX

    def getYAxis(self):
        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTickCount(10)
        axisY.setRange(0, 100)
        axisY.setTitleText("Humidity, %")
        return axisY


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = TestWindow()
    window.setWindowTitle("Getting data from Arduino")
    window.show()
    window.resize(500, 400)

    sys.exit(app.exec_())
