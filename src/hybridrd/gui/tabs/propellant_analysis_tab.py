from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg


class PropellantAnalysisTab(QtWidgets.QWidget):
    """
    This class represents the 'Propellant Analysis' tab from the GUI.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor method. All arguments accepted by the
        :class: `QtWidgets.QWidget` can be passed.
        """
        super().__init__(*args, **kwargs)
        self._setupUi()

    def _setupUi(self):
        self._mainwidget = QtWidgets.QFrame(self)
        self._mainwidget.setGeometry(QtCore.QRect(0, 10, 831, 130))
        self._setupStartingInfo()
        self._setupPlotInfo()
        self._setupPlotWidget()
        self._setupPropellantAnalysisLayout()

    def _setupStartingInfo(self):
        self._setupStartingOfRange()
        self._setupFinalOfRange()
        self._setupCfNozzleCorrection()
        self._setupPerformAnalysisButton()

    def _setupStartingOfRange(self):
        self._starting_of_label = QtWidgets.QLabel(self._mainwidget)
        self._starting_of_label.setText('Starting o/f')
        self.starting_of = QtWidgets.QDoubleSpinBox(self._mainwidget)
        self.starting_of.setRange(0.001, 19.999)
        self.starting_of.setSingleStep(0.001)
        self.starting_of.setValue(0.800)
        self.starting_of.setDecimals(3)
        self.starting_of.setLocale(QtCore.QLocale())

    def _setupFinalOfRange(self):
        self._final_of_label = QtWidgets.QLabel(self._mainwidget)
        self._final_of_label.setText('Final o/f')
        self.final_of = QtWidgets.QDoubleSpinBox(self._mainwidget)
        self.final_of.setRange(0.001, 20.000)
        self.final_of.setSingleStep(0.001)
        self.final_of.setValue(1.200)
        self.final_of.setDecimals(3)
        self.final_of.setLocale(QtCore.QLocale())

    def _setupCfNozzleCorrection(self):
        self._cf_nozzle_correction_label = QtWidgets.QLabel(self._mainwidget)
        self._cf_nozzle_correction_label.setText('Nozzle Cf Correction')
        self.cf_correction = QtWidgets.QDoubleSpinBox(self._mainwidget)
        self.cf_correction.setGeometry(QtCore.QRect(130, 80, 113, 23))
        self.cf_correction.setRange(0.001, 1.000)
        self.cf_correction.setSingleStep(0.001)
        self.cf_correction.setValue(1)
        self.cf_correction.setDecimals(3)
        self.cf_correction.setLocale(QtCore.QLocale())

    def _setupPerformAnalysisButton(self):
        self._left_spacer_analysis_btn = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.perform_analysis_btn = QtWidgets.QPushButton(self._mainwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.perform_analysis_btn.sizePolicy().hasHeightForWidth())
        self.perform_analysis_btn.setSizePolicy(sizePolicy)
        self.perform_analysis_btn.setText('Perform Analysis')

    def _setupPlotInfo(self):
        self._setupXVariable()
        self._setupYVariable()
        self._setupLocale()
        self._setupGeneratePlotButton()

    def _setupXVariable(self):
        self._variable_x_axis_label = QtWidgets.QLabel(self._mainwidget)
        self._variable_x_axis_label.setText('Variable of Interest (X-Axis)')
        self.variable_x_axis = QtWidgets.QComboBox(self._mainwidget)
        self.variable_x_axis.addItem('o/f')
        self.variable_x_axis.addItem('Isp')
        self.variable_x_axis.addItem('c*')
        self.variable_x_axis.addItem('Gamma')
        self.variable_x_axis.addItem('Ae/At')
        self.variable_x_axis.addItem('Cf')

    def _setupYVariable(self):
        self._variable_y_axis_label = QtWidgets.QLabel(self._mainwidget)
        self._variable_y_axis_label.setText('Variable of Interest (Y-Axis)')
        self.variable_y_axis = QtWidgets.QComboBox(self._mainwidget)
        self.variable_y_axis.addItem('Isp')
        self.variable_y_axis.addItem('c*')
        self.variable_y_axis.addItem('Gamma')
        self.variable_y_axis.addItem('Ae/At')
        self.variable_y_axis.addItem('Cf')
        self.variable_y_axis.addItem('o/f')

    def _setupLocale(self):
        self._plot_locale_label = QtWidgets.QLabel(self._mainwidget)
        self._plot_locale_label.setText('Locale')
        self.plot_locale = QtWidgets.QComboBox(self._mainwidget)
        self.plot_locale.addItem('en_US')
        self.plot_locale.addItem('pt_BR')

    def _setupGeneratePlotButton(self):
        self._left_spacer_plot_btn = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.generate_plot_btn = QtWidgets.QPushButton(self._mainwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generate_plot_btn.sizePolicy().hasHeightForWidth())
        self.generate_plot_btn.setSizePolicy(sizePolicy)
        self.generate_plot_btn.setText('Generate Plot')
        self.generate_plot_btn.setEnabled(False)

    def _setupPlotWidget(self):
        self.analysis_results_plot_widget = pg.GraphicsLayoutWidget(self)
        self.analysis_results_plot_widget.setGeometry(QtCore.QRect(0, 160, 840, 401))
        self.analysis_results_plot_widget.setBackground(None)

    def _setupPropellantAnalysisLayout(self):
        formlayout_starting_info = QtWidgets.QFormLayout()
        formlayout_starting_info.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._starting_of_label)
        formlayout_starting_info.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.starting_of)
        formlayout_starting_info.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._final_of_label)
        formlayout_starting_info.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.final_of)
        formlayout_starting_info.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._cf_nozzle_correction_label)
        formlayout_starting_info.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cf_correction)
        hlayout_perform_analysis_btn = QtWidgets.QHBoxLayout()
        hlayout_perform_analysis_btn.addItem(self._left_spacer_analysis_btn)
        hlayout_perform_analysis_btn.addWidget(self.perform_analysis_btn)
        vlayout_starting_info = QtWidgets.QVBoxLayout()
        vlayout_starting_info.addLayout(formlayout_starting_info)
        vlayout_starting_info.addLayout(hlayout_perform_analysis_btn)
        formlayout_plot_info = QtWidgets.QFormLayout()
        formlayout_plot_info.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        formlayout_plot_info.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._variable_x_axis_label)
        formlayout_plot_info.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.variable_x_axis)
        formlayout_plot_info.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._variable_y_axis_label)
        formlayout_plot_info.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.variable_y_axis)
        formlayout_plot_info.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._plot_locale_label)
        formlayout_plot_info.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.plot_locale)
        hlayout_generate_plot_btn = QtWidgets.QHBoxLayout()
        hlayout_generate_plot_btn.addItem(self._left_spacer_plot_btn)
        hlayout_generate_plot_btn.addWidget(self.generate_plot_btn)
        vlayout_plot_info = QtWidgets.QVBoxLayout()
        vlayout_plot_info.addLayout(formlayout_plot_info)
        vlayout_plot_info.addLayout(hlayout_generate_plot_btn)
        mainhlayout = QtWidgets.QHBoxLayout(self._mainwidget)
        mainhlayout.setContentsMargins(50, 5, 50, 5)
        mainhlayout.addLayout(vlayout_starting_info)
        info_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        mainhlayout.addItem(info_spacer_item)
        mainhlayout.addLayout(vlayout_plot_info)
