from time import sleep
from random import randint

from PyQt5.QtChart import QChart, QChartView, QSplineSeries, QValueAxis
from PyQt5.QtCore import (QPointF, QRunnable, Qt, QThread, QThreadPool, QTimer,
                          QTimerEvent, pyqtSlot)
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QGridLayout,
                             QHBoxLayout, QMainWindow, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        view = QChartView()

        glMain = QGridLayout()
        glMain.addWidget(view, 0, 0)
        glMain.addLayout(self.getSerialPanel(4), 0, 1)
        glMain.addLayout(self.getButtonsPanel(), 1, 0, 1, 2)

        wCenter = QWidget()
        wCenter.setLayout(glMain)
        self.setCentralWidget(wCenter)

    def getSeries(self, count):
        _series = []
        for index in range(count):
            series = QSplineSeries()
            series.setPen(QColor.fromRgb(
                randint(0, 255),
                randint(0, 255),
                randint(0, 255)
            ))
            series.setUseOpenGL(True)
            _series.append(series)
        return _series

    def getSerialPanel(self, count):
        glSerial = QVBoxLayout()

        for index in range(count):
            cb = QCheckBox('Serial {index}'.format(index=index + 1))
            glSerial.addWidget(cb)

        cbType = QComboBox()
        cbType.addItems(['Temperature', 'Humidity'])

        glSerial.addWidget(cbType)

        return glSerial

    def getButtonsPanel(self):
        pbStart = QPushButton('&Start')
        pbStop = QPushButton('&Stop')
        pbClear = QPushButton('&Clear')
        pbSave = QPushButton('&Save')
        pbClose = QPushButton('&Close')

        glButtons = QHBoxLayout()

        glButtons.addWidget(pbStart)
        glButtons.addWidget(pbStop)
        glButtons.addWidget(pbSave)
        glButtons.addWidget(pbClear)
        glButtons.addWidget(pbClose)

        return glButtons
