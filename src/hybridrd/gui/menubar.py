from hybridrd.gui.menus import SettingsMenu
from PyQt5 import QtCore, QtWidgets


class MenuBar(QtWidgets.QMenuBar):
    """
    """
    def __init__(self, MainWindow, *args, **kwargs):
        super().__init__(MainWindow, *args, **kwargs)
        self.setEnabled(True)
        self.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self._setupMenuBarFile()
        self._setupMenuBarEdit()
        self._setupMenuBarView()
        self._setupMenuBarSettings()
        self._setupMenuBarHelp()
        MainWindow.setMenuBar(self)

    def _setupMenuBarFile(self):
        self.file = QtWidgets.QMenu(self)
        self.file.setTitle("File")
        self.addAction(self.file.menuAction())

    def _setupMenuBarEdit(self):
        self.edit = QtWidgets.QMenu(self)
        self.edit.setTitle("Edit")
        self.addAction(self.edit.menuAction())

    def _setupMenuBarView(self):
        self.view = QtWidgets.QMenu(self)
        self.view.setTitle("View")
        self.addAction(self.view.menuAction())

    def _setupMenuBarSettings(self):
        self.settings = SettingsMenu(self)
        self.addAction(self.settings.menuAction())

    def _setupMenuBarHelp(self):
        self.help = QtWidgets.QMenu(self)
        self.help.setTitle("Help")
        self.addAction(self.help.menuAction())
