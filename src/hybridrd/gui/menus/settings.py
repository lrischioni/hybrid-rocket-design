from PyQt5 import QtWidgets


class SettingsMenu(QtWidgets.QMenu):
    """
    This class represents the settings menu from the menu bar.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor method. All arguments accepted by the :class: `QtWidgets.QMenu` can
        be passed.
        """
        super().__init__(*args, **kwargs)
        self.setTitle('Settings')
        self._setupSubMenus()

    def _setupSubMenus(self):
        self.appearance = _Appearance(self)
        self.addMenu(self.appearance)


class _Appearance(QtWidgets.QMenu):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle('Appearance')
        self._setupActions()

    def _setupActions(self):
        self.dark_theme = QtWidgets.QAction('Dark theme', self)
        self.light_theme = QtWidgets.QAction('Light theme', self)
        self.addAction(self.dark_theme)
        self.addAction(self.light_theme)
