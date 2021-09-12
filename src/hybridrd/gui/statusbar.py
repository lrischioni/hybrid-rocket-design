from PyQt5 import QtWidgets


class StatusBar(QtWidgets.QStatusBar):
    """
    This class represents the status bar from the GUI.
    """
    def __init__(self, MainWindow, *args, **kwargs):
        """
        Constructor method. All arguments accepted by the
        :class: `QtWidgets.QStatusBar` can be passed.

        Args:
            MainWindow (QtWidgets.QMainWindow): Reference to Main Window from the GUI. It is passed
            as parent to the :class: `QtWidgets.QStatusBar`
        """
        super().__init__(MainWindow, *args, **kwargs)
        self.setObjectName("statusbar")
        MainWindow.setStatusBar(self)

    def setupProgressBar(self):
        """
        Create a QtWidgets.QProgressBar and add it to the status bar.
        """
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setMaximumWidth(300)
        self.addPermanentWidget(self.progressBar)

    def removeProgressBar(self):
        """
        Remove the QtWidgets.QProgressBar from the status bar.
        """
        self.removeWidget(self.progressBar)
        delattr(self, 'progressBar')
