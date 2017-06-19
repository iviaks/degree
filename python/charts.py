# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Saykov Max


import serial
from PyQt5.QtChart import QChart, QChartView, QSplineSeries, QValueAxis
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDialog, QFileDialog,
                             QGridLayout, QHBoxLayout, QMainWindow,
                             QMessageBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QTabWidget, QVBoxLayout,
                             QWidget)

from datetime import datetime

READING_MODE = 1  # 0
AVAILABLE_SERIAL_PORT = '/dev/ttyACM0'


class CustomChartView(QChartView):
    def __init__(self, *args, **kwargs):
        return super(CustomChartView, self).__init__(*args, **kwargs)

    def setWidget(self, widget=None):
        self.widget = widget

    def get_from_serial(self, ser):
        s = ''
        ch = ser.read()

        while ch != b'\n':
            s += ch.decode('utf-8')
            ch = ser.read()

        return float(s)

    def get_from_file(self, file):
        return (
            int(file.readline()),
            float(file.readline()),
            float(file.readline())
        )

    def timerEvent(self, *args):
        if READING_MODE == 1:
            with open('input.txt') as file:
                self.widget.addPoint(*self.get_from_file(file))
                self.widget.addPoint(*self.get_from_file(file))
        elif READING_MODE == 0:
            with serial.Serial(port=AVAILABLE_SERIAL_PORT) as ser:
                ser.flush()
                self.widget.addPoint(0, self.get_from_serial(ser))
                self.widget.addPoint(1, self.get_from_serial(ser))


class TestWindow(QMainWindow):
    timer_id = None

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.series = [QSplineSeries() for index in range(2)]
        self.data = [[] for index in range(len(self.series))]
        self.series[0].setPen(QPen(Qt.red))
        self.series[1].setPen(QPen(Qt.blue))
        # self.series[1].setPen(QPen(Qt.blue))
        # self.series[3].setPen(QPen(Qt.yellow))

        for series in self.series:
            series.setUseOpenGL(True)

        self.view = CustomChartView()
        self.chart = QChart()
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
        # self.view.startTimer(200)
        self.view.setChart(self.chart)

    def setupSerialPanel(self):
        # cbSerial1 = QCheckBox('Serial 1')
        # cbSerial2 = QCheckBox('Serial 2')
        # cbSerial3 = QCheckBox('Serial 3')
        # cbSerial4 = QCheckBox('Serial 4')

        self.cbType = QComboBox()
        self.cbType.addItems(['Temperature', 'Humidity'])
        self.cbType.currentIndexChanged.connect(self.change_label)

        glSerial = QVBoxLayout()

        # glSerial.addWidget(cbSerial1)
        # glSerial.addWidget(cbSerial2)
        # glSerial.addWidget(cbSerial3)
        # glSerial.addWidget(cbSerial4)
        glSerial.addWidget(self.cbType)

        self.glMain.addLayout(glSerial, 0, 1)

    def setupButtons(self):
        pbStart = QPushButton('Start')
        pbStop = QPushButton('Stop')
        pbClear = QPushButton('Clear')
        pbResults = QPushButton('Results')
        pbClose = QPushButton('Close')

        pbStart.clicked.connect(self.start_getting)
        pbStop.clicked.connect(self.stop_getting)
        pbClear.clicked.connect(self.clear_data)
        pbClose.clicked.connect(self.close)
        pbResults.clicked.connect(self.show_results)

        glButtons = QHBoxLayout()

        glButtons.addWidget(pbStart)
        glButtons.addWidget(pbStop)
        glButtons.addWidget(pbResults)
        glButtons.addWidget(pbClear)
        glButtons.addWidget(pbClose)

        self.glMain.addLayout(glButtons, 1, 0, 1, 2)

    def start_getting(self):
        if self.timer_id is None:
            self.timer_id = self.view.startTimer(200)

    def stop_getting(self):
        if self.timer_id is not None:
            self.view.killTimer(self.timer_id)

        self.timer_id = None

    def clear_data(self):
        for index in range(len(self.series)):
            self.series[index].clear()

        self.axisX.setRange(0, 20)

    def change_label(self):

        self.stop_getting()
        # self.clear_data()

        if self.cbType.currentText() == 'Temperature':
            self.chart.setTitle("Temperature graph")
            self.axisY.setRange(-40, 40)
            self.axisY.setTitleText("Temperature, °C")

        elif self.cbType.currentText() == 'Humidity':
            self.chart.setTitle("Humidity graph")
            self.axisY.setRange(0, 100)
            self.axisY.setTitleText("Humidity, %")

    def show_results(self):
        dialog = QDialog()
        dialog.setModal(True)

        pbSave = QPushButton('Save')
        pbSave.clicked.connect(lambda: dialog.accept())
        pbClose = QPushButton('Close')
        pbClose.clicked.connect(lambda: dialog.reject())

        wTemperature = QWidget()
        twTemperature = QTableWidget()
        twTemperature.setColumnCount(3)
        glTemperature = QGridLayout()
        glTemperature.addWidget(twTemperature, 0, 0)
        wTemperature.setLayout(glTemperature)

        wHumidity = QWidget()
        twHumidity = QTableWidget()
        twHumidity.setColumnCount(3)
        glHumidity = QGridLayout()
        glHumidity.addWidget(twHumidity, 0, 0)
        wHumidity.setLayout(glHumidity)

        if len(self.data):
            twTemperature.setRowCount(len(self.data[0]))
            twHumidity.setRowCount(len(self.data[0]))

        for column in range(len(self.data)):
            for row, data in enumerate(self.data[column]):

                tempDate = QTableWidgetItem()
                tempDate.setText(data['date'].strftime('%d-%m-%Y %H:%M:%S'))
                humDate = QTableWidgetItem()
                humDate.setText(data['date'].strftime('%d-%m-%Y %H:%M:%S'))
                twTemperature.setItem(row, 0, tempDate)
                twHumidity.setItem(row, 0, humDate)

                temperature = QTableWidgetItem()
                temperature.setText(str(data['temperature']))
                humidity = QTableWidgetItem()
                humidity.setText(str(data['humidity']))
                twTemperature.setItem(row, column + 1, temperature)
                twHumidity.setItem(row, column + 1, humidity)

        twTemperature.resizeColumnsToContents()
        twHumidity.resizeColumnsToContents()
        twTemperature.setHorizontalHeaderLabels(['Time', '1', '2'])
        twHumidity.setHorizontalHeaderLabels(['Time', '1', '2'])

        tabs = QTabWidget()
        tabs.addTab(wTemperature, 'Temperature')
        tabs.addTab(wHumidity, 'Humidity')

        # twResults = QTableWidget()
        # twResults.setColumnCount(3)

        glMain = QGridLayout()
        glMain.addWidget(tabs, 0, 0, 1, 2)
        glMain.addWidget(pbSave, 1, 0)
        glMain.addWidget(pbClose, 1, 1)

        dialog.setLayout(glMain)

        if dialog.exec():
            pass
        else:
            pass

    def setup(self):
        self.axisX = self.getXAxis(0, 20)
        self.chart.setTitle("Temperature graph")
        self.chart.addAxis(self.axisX, Qt.AlignBottom)

        self.axisY = self.getYAxis()
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        for series in self.series:
            self.chart.addSeries(series)
            series.attachAxis(self.axisX)
            series.attachAxis(self.axisY)

    def addPoint(self, index, temperature, humidity):
        self.data[index].append({
            'temperature': temperature,
            'humidity': humidity,
            'date': datetime.now()
        })
        self.setLine(index)

    def setLine(self, index):
        if self.cbType.currentText() == 'Temperature':
            self.series[index].append(
                QPointF(
                    len(self.series[index]),
                    self.data[index][-1]['temperature']
                )
            )

        elif self.cbType.currentText() == 'Humidity':
            self.series[index].append(
                QPointF(
                    len(self.series[index]),
                    self.data[index][-1]['humidity']
                )
            )

        if not len(self.series[index]) % 20:
            self.axisX.setRange(
                len(self.series[index]) // 20 * 20,
                (len(self.series[index]) // 20 + 1) * 20
            )

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
        axisY.setRange(-40, 40)
        axisY.setTitleText("Temperature, °C")
        return axisY


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = TestWindow()
    window.setWindowTitle("Getting data from Arduino")
    window.show()
    # window.resize(500, 400)

    sys.exit(app.exec_())