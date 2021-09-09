from PyQt5 import QtWidgets


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, MainWindow):
        super().__init__(MainWindow)
        self.setObjectName("statusbar")
        MainWindow.setStatusBar(self)

    def setupProgressBar(self):
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setMaximumWidth(300)
        self.addPermanentWidget(self.progressBar)

    def removeProgressBar(self):
        self.removeWidget(self.progressBar)
        delattr(self, 'progressBar')
