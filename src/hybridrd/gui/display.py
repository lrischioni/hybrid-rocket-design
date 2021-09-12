from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np


class DisplayOutputFileWindow(QtWidgets.QWidget):
    """
    This class represents the window that displays
    the CEA output file.
    """
    def __init__(self, filepath, *args, **kwargs):
        """
        Constructor method. All arguments accepted by
        the :class: `QtWidgets.QWidget` can be passed.

        Args:
            filepath (str): Path to the CEA output file
        """
        super().__init__(*args, **kwargs)
        self._setupUi(filepath)

    def _setupUi(self, filepath):
        TextFile = QtWidgets.QDialog(self)
        TextFile.resize(683, 531)
        TextFile.setWindowTitle('CEA Output')
        self.scrollArea = QtWidgets.QScrollArea(TextFile)
        self.scrollArea.setGeometry(QtCore.QRect(10, 20, 661, 501))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.scrollArea)
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 661, 501))
        self.textEdit.setCurrentFont(QtGui.QFont('Monospace', 10))
        with open(filepath, 'r') as f:
            self.textEdit.setText(f.read())
        TextFile.exec_()


class SelectStartingPoint(QtWidgets.QDialog):
    """
    This class represents the window that displays the plot of
    Isp vs misture ratio, and asks the user to select the starting
    point of the burn simulation.
    """
    def __init__(self, mainWindow, *args, **kwargs):
        """
        Constructor method. All arguments accepted by the
        :class: `QtWidgets.QDialog` can be passed.

        Args:
            mainWindow (QtWidgets.QMainWindow): Reference to Main Window from the GUI. It is passed
            as parent to the :class: `QtWidgets.QDialog`
        """
        super().__init__(mainWindow, *args, **kwargs)
        self._ceaResults = mainWindow.cea.propellant_analysis_results
        self._mainWindow = mainWindow
        self._setupUi()

    def _setupUi(self):
        self.resize(683, 531)
        self.setWindowTitle('Select Starting Point')
        self._setupPlot()
        self.exec_()

    def _setupPlot(self):
        self._getDataFromCeaResults()
        self._configDisplayInfo()
        self._configPlot()
        self._adjustLayout()

    def _getDataFromCeaResults(self):
        self._of_ratio = self._ceaResults['o/f'].values
        self._cstar = self._ceaResults['c*'].values
        self._cf = self._ceaResults['Cf'].values
        self._aeat = self._ceaResults['Ae/At'].values

    def _configDisplayInfo(self):
        self._initial_of = QtWidgets.QLabel('Initial o/f:')
        self._initial_cstar = QtWidgets.QLabel('Initial c*:')
        self._initial_cf = QtWidgets.QLabel('Initial Cf:')
        self._aeat_ratio = QtWidgets.QLabel('Ae/At Ratio:')
        self._confirm_btn = QtWidgets.QPushButton('Confirm')
        self._confirm_btn.clicked.connect(lambda: self._storeSelectedValues())

    def _storeSelectedValues(self):
        self.initial_of_value = self._initial_of.text().replace('Initial o/f: ', '')
        self.initial_cstar_value = self._initial_cstar.text().replace('Initial c*: ', '').replace(' m/s', '')
        self.initial_cf_value = self._initial_cf.text().replace('Initial Cf: ', '')
        self.aeat_ratio_value = self._aeat_ratio.text().replace('Ae/At Ratio: ', '')
        self.close()

    def _configPlot(self):
        self.graphWidget = pg.GraphicsWindow()
        self._plot_item = self.graphWidget.addPlot()
        self.graphWidget.setBackground(None)
        if self._initial_value_is_set():
            initial_value = float(self._mainWindow.tabWidget.burn_simulation_tab.initial_of.text())
        else:
            initial_value = np.mean(self._of_ratio)
        if self._mainWindow.theme == 'dark theme':
            styles = {'font-size': '15px'}
            self._plot_item.plot(self._of_ratio, self._cstar, pen=pg.mkPen(color=(101, 82, 68), width=4.))
            self._plot_item.setTitle('Misture Ratio Influence on c*', color='w', size='16pt')
            self._plot_item.setLabel('left', 'c* (m/s)', **styles)
            self._plot_item.setLabel('bottom', 'Misture Ratio o/f', **styles)
            self._plot_item.getAxis('left').setTextPen('w')
            self._plot_item.getAxis('bottom').setTextPen('w')
            self._line = pg.InfiniteLine(pos=initial_value, movable=True, pen=pg.mkPen(color=(55, 78, 74), width=2.))
        else:
            styles = {'font-size': '15px'}
            self._plot_item.plot(self._of_ratio, self._cstar, pen=pg.mkPen(color=(0, 0, 255)))
            self._plot_item.setTitle('Misture Ratio Influence on c*', color='k', size='16pt')
            self._plot_item.setLabel('left', 'c* (m/s)', **styles)
            self._plot_item.setLabel('bottom', 'Misture Ratio o/f', **styles)
            self._plot_item.getAxis('left').setTextPen('k')
            self._plot_item.getAxis('bottom').setTextPen('k')
            self._line = pg.InfiniteLine(pos=initial_value, movable=True, pen=pg.mkPen(color=(255, 0, 0)))
        self._line.setBounds((np.min(self._of_ratio), np.max(self._of_ratio)))
        self._line.sigPositionChanged.connect(lambda: self._updateDisplayValues())
        self._plot_item.addItem(self._line)
        self._updateDisplayValues()

    def _initial_value_is_set(self):
        return self._mainWindow.tabWidget.burn_simulation_tab.initial_of.text() != ''

    def _updateDisplayValues(self):
        of_value_selected = self._line.value()
        array_idx = self._find_nearest(self._of_ratio, of_value_selected)
        cstar_value_selected = np.round(self._cstar[array_idx], 3)
        cf_value_selected = np.round(self._cf[array_idx], 3)
        aeat_value_selected = np.round(self._aeat[array_idx], 3)
        self._initial_of.setText('Initial o/f: ' + str(round(of_value_selected, 3)))
        self._initial_cstar.setText('Initial c*: ' + str(cstar_value_selected) + ' m/s')
        self._initial_cf.setText('Initial Cf: ' + str(cf_value_selected))
        self._aeat_ratio.setText('Ae/At Ratio: ' + str(aeat_value_selected))

    def _find_nearest(self, search_array, value):
        search_array = np.asarray(search_array)
        idx = (np.abs(search_array - value)).argmin()
        return idx

    def _adjustLayout(self):
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.graphWidget, 1, 2, 3, 4)
        self.layout.addWidget(self._initial_of, 5, 1, 2, 6)
        self.layout.addWidget(self._initial_cstar, 7, 1, 2, 6)
        self.layout.addWidget(self._initial_cf, 9, 1, 2, 6)
        self.layout.addWidget(self._aeat_ratio, 11, 1, 2, 6)
        self.layout.addWidget(self._confirm_btn, 13, 5, 1, 2)


class InsertRegressionParameters(QtWidgets.QDialog):
    """
    This class represents the window that asks the user to enter
    the regression rate equaiton parameters.
    """
    def __init__(self, mainWindow, *args, **kwargs):
        """
        Constructor method. All arguments accepted by the
        :class: `QtWidgets.QDialog` can be passed.

        Args:
            mainWindow (QtWidgets.QMainWindow): Reference to Main Window from the GUI. It is passed
            as parent to the :class: `QtWidgets.QDialog`
        """
        super().__init__(mainWindow, *args, **kwargs)
        self._mainWindow = mainWindow
        self._setupUi()

    def _setupUi(self):
        self.resize(280, 150)
        self.setWindowTitle('Insert Regression Parameters')
        self._setupRegressionInfo()
        self.exec_()

    def _setupRegressionInfo(self):
        self._setupRegressionParameters()
        self._setupGoxUnit()
        self._setupRegressionUnit()
        self._setupConfirmButton()
        self._setupRegressionInfoLayout()
        self._setupConnections()
        self._checkValuesPreviouslySetted()

    def _setupRegressionParameters(self):
        self._regression_parameter_a_label = QtWidgets.QLabel(self)
        self._regression_parameter_a_label.setText('Parameter a')
        self.regression_parameter_a = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regression_parameter_a.sizePolicy().hasHeightForWidth())
        self.regression_parameter_a.setSizePolicy(sizePolicy)
        self.regression_parameter_a.setProperty('error', True)
        self._regression_parameter_a_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._regression_parameter_n_label = QtWidgets.QLabel(self)
        self._regression_parameter_n_label.setText('Parameter n')
        self.regression_parameter_n = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regression_parameter_n.sizePolicy().hasHeightForWidth())
        self.regression_parameter_n.setSizePolicy(sizePolicy)
        self.regression_parameter_n.setProperty('error', True)
        self._regression_parameter_n_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupGoxUnit(self):
        self._gox_unit_label = QtWidgets.QLabel(self)
        self._gox_unit_label.setText('Gox Unit')
        self.gox_unit = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gox_unit.sizePolicy().hasHeightForWidth())
        self.gox_unit.setSizePolicy(sizePolicy)
        self.gox_unit.addItem('g/(cm².s)')
        self.gox_unit.addItem('g/(mm².s)')
        self.gox_unit.addItem('g/(m².s)')
        self.gox_unit.addItem('kg/(cm².s)')
        self.gox_unit.addItem('kg/(mm².s)')
        self.gox_unit.addItem('kg/(m².s)')
        self._gox_unit_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupRegressionUnit(self):
        self._regression_rate_unit_label = QtWidgets.QLabel(self)
        self._regression_rate_unit_label.setText('Regression Rate Unit')
        self.regression_rate_unit = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regression_rate_unit.sizePolicy().hasHeightForWidth())
        self.regression_rate_unit.setSizePolicy(sizePolicy)
        self.regression_rate_unit.addItem('mm/s')
        self.regression_rate_unit.addItem('cm/s')
        self.regression_rate_unit.addItem('m/s')
        self._regression_rate_unit_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupConfirmButton(self):
        self._left_spacer_confirm_btn = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.confirm_btn = QtWidgets.QPushButton(self)
        self.confirm_btn.setText('Confirm')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirm_btn.sizePolicy().hasHeightForWidth())
        self.confirm_btn.setSizePolicy(sizePolicy)
        self.confirm_btn.setEnabled(False)

    def _setupRegressionInfoLayout(self):
        hlayout_parameter_a = QtWidgets.QHBoxLayout()
        hlayout_parameter_a.addWidget(self.regression_parameter_a)
        hlayout_parameter_a.addItem(self._regression_parameter_a_spacer_item)
        hlayout_parameter_n = QtWidgets.QHBoxLayout()
        hlayout_parameter_n.addWidget(self.regression_parameter_n)
        hlayout_parameter_n.addItem(self._regression_parameter_n_spacer_item)
        hlayout_gox_unit = QtWidgets.QHBoxLayout()
        hlayout_gox_unit.addWidget(self.gox_unit)
        hlayout_gox_unit.addItem(self._gox_unit_spacer)
        hlayout_regression_unit = QtWidgets.QHBoxLayout()
        hlayout_regression_unit.addWidget(self.regression_rate_unit)
        hlayout_regression_unit.addItem(self._regression_rate_unit_spacer)
        formlayout = QtWidgets.QFormLayout()
        formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._regression_parameter_a_label)
        formlayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, hlayout_parameter_a)
        formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._regression_parameter_n_label)
        formlayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, hlayout_parameter_n)
        formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._gox_unit_label)
        formlayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, hlayout_gox_unit)
        formlayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._regression_rate_unit_label)
        formlayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, hlayout_regression_unit)
        hlayout_btn = QtWidgets.QHBoxLayout()
        hlayout_btn.addItem(self._left_spacer_confirm_btn)
        hlayout_btn.addWidget(self.confirm_btn)
        vmainlayout = QtWidgets.QVBoxLayout(self)
        vmainlayout.setContentsMargins(5, 5, 5, 5)
        vmainlayout.addLayout(formlayout)
        vmainlayout.addLayout(hlayout_btn)

    def _setupConnections(self):
        self.regression_parameter_a.textChanged.connect(lambda: self._activateConfirmButton(self.regression_parameter_a))
        self.regression_parameter_n.textChanged.connect(lambda: self._activateConfirmButton(self.regression_parameter_n))
        self.confirm_btn.clicked.connect(lambda: self._processRegressionParameters())

    def _activateConfirmButton(self, changedField):
        self._validateData(changedField)
        if self.regression_parameter_a.property('error') or self.regression_parameter_n.property('error'):
            self.confirm_btn.setEnabled(False)
        else:
            self.confirm_btn.setEnabled(True)

    def _validateData(self, field):
        try:
            field_value = float(field.text())
            if field_value < 0:
                field.setProperty('error', True)
            else:
                field.setProperty('error', False)
        except Exception:
            field.setProperty('error', True)
        field.setStyle(field.style())

    def _processRegressionParameters(self):
        a = self.regression_parameter_a.text()
        n = self.regression_parameter_n.text()
        gox_unit = self.gox_unit.currentText()
        regression_unit = self.regression_rate_unit.currentText()
        self._resetMainWindowLines()
        self._mainWindow.tabWidget.burn_simulation_tab.regression_parameter_a_si = self._convertRegressionParameter()
        self._mainWindow.tabWidget.burn_simulation_tab.gox_unit = gox_unit
        self._mainWindow.tabWidget.burn_simulation_tab.regression_unit = regression_unit
        self._mainWindow.tabWidget.burn_simulation_tab.regression_parameter_a.setText(a)
        self._mainWindow.tabWidget.burn_simulation_tab.regression_parameter_n.setText(n)
        self.close()

    def _resetMainWindowLines(self):
        self._mainWindow.tabWidget.burn_simulation_tab.regression_parameter_a.setText('')
        self._mainWindow.tabWidget.burn_simulation_tab.regression_parameter_n.setText('')

    def _convertRegressionParameter(self):
        try:
            a = float(self.regression_parameter_a.text())
            n = float(self.regression_parameter_n.text())
            gox_unit = self.gox_unit.currentText()
            regression_unit = self.regression_rate_unit.currentText()
            if gox_unit == 'g/(cm².s)':
                gox_converter = -1
            elif gox_unit == 'g/(mm².s)':
                gox_converter = -3
            elif gox_unit == 'g/(m².s)':
                gox_converter = 3
            elif gox_unit == 'kg/(cm².s)':
                gox_converter = -4
            elif gox_unit == 'kg/(mm².s)':
                gox_converter = -6
            elif gox_unit == 'kg/(m².s)':
                gox_converter = 0
            if regression_unit == 'm/s':
                regression_converter = 0
            elif regression_unit == 'cm/s':
                regression_converter = -2
            elif regression_unit == 'mm/s':
                regression_converter = -3
            a_si = a * (10**(regression_converter + gox_converter * n))
            return a_si
        except Exception:
            pass

    def _checkValuesPreviouslySetted(self):
        try:
            a = self._mainWindow.tabWidget.burn_simulation_tab.regression_parameter_a.text()
            n = self._mainWindow.tabWidget.burn_simulation_tab.regression_parameter_n.text()
            gox_unit = self._mainWindow.tabWidget.burn_simulation_tab.gox_unit
            regression_unit = self._mainWindow.tabWidget.burn_simulation_tab.regression_unit
            self.regression_parameter_a.setText(a)
            self.regression_parameter_n.setText(n)
            self.gox_unit.setCurrentText(gox_unit)
            self.regression_rate_unit.setCurrentText(regression_unit)
        except Exception:
            pass
