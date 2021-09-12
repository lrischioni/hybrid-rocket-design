import sys
from PyQt5 import QtWidgets
from hybridrd.mainwindow import MainWindow


QtWidgets.QApplication.setApplicationName('Hybrid Rocket Design')
QtWidgets.QApplication.setApplicationVersion('0.1')


class HybridRDApp():
    """
    This class is responsible for starting the GUI application.
    """
    def __init__(self):
        """
        Constructor method.
        """
        app = QtWidgets.QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()
        sys.exit(app.exec_())
