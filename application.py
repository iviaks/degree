if __name__ == '__main__':
    import sys
    from form import MainWindow
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("Getting data from Arduino")
    window.show()
    window.resize(500, 400)

    sys.exit(app.exec_())
