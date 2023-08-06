from sitcom.st import Ui_MainWindow
from sitcom.st import Load_Window
from PyQt5 import QtWidgets,QtGui
import time

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    movie=QtGui.QMovie('load/sitcom.gif')
    QtGui.QFontDatabase.addApplicationFont('font/lato/Lato-Semibold.ttf')
    splash = Load_Window(movie)
    splash.show()
    splash.movie.start()
    start = time.time()
    while movie.state() == QtGui.QMovie.Running and time.time() < start + 4:
        app.processEvents()
    MainWindow = QtWidgets.QMainWindow()
    splash.finish(MainWindow)
    splash.close()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
