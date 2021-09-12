from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg


class BurnSimulationResultsTab(QtWidgets.QTabWidget):
    """
    This class represents the 'Burn Simulation Results' tab from the GUI.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor method. All arguments accepted by the
        :class: `QtWidgets.QWidget` can be passed.
        """
        super().__init__(*args, **kwargs)
        self.setObjectName('SimulationResults')
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.results_tab = _ResultsTab(self)
        self.addTab(self.results_tab, 'Results')
        self.plots_tab = _PlotsTab(self)
        self.addTab(self.plots_tab, 'Plots')


class _ResultsTab(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setupUi()

    def _setupUi(self):
        self._setupStartOfBurningInfoWidget()
        self._setupEndOfBurningInfoWidget()
        self._setupMotorGeometryInfoWidget()
        self._setupResultsTabButtons()

    def _setupStartOfBurningInfoWidget(self):
        self._start_burning_info_widget = QtWidgets.QGroupBox(self)
        self._start_burning_info_widget.setGeometry(QtCore.QRect(10, 20, 261, 291))
        self._start_burning_info_widget.setTitle('Start of Burning')
        self._setupMassFlowRate()
        self._setupFuelMassFlowRate()
        self._setupOxidantMassFlowRate()
        self._setupMistureRatio()
        self._setupStartRegressionRate()
        self._setupStartInnerDiameter()
        self._setupStartGox()
        self._setupStartOfBurningInfoLayout()

    def _setupMassFlowRate(self):
        self._mass_flow_rate_label = QtWidgets.QLabel(self._start_burning_info_widget)
        self._mass_flow_rate_label.setText('Mass flow rate')
        self.mass_flow_rate = QtWidgets.QLabel(self._start_burning_info_widget)
        self.mass_flow_rate.setText('')

    def _setupFuelMassFlowRate(self):
        self._fuel_mass_flow_rate_label = QtWidgets.QLabel(self._start_burning_info_widget)
        self._fuel_mass_flow_rate_label.setText('Fuel mass flow rate')
        self.fuel_mass_flow_rate = QtWidgets.QLabel(self._start_burning_info_widget)
        self.fuel_mass_flow_rate.setText('')

    def _setupOxidantMassFlowRate(self):
        self._oxid_mass_flow_rate_label = QtWidgets.QLabel(self._start_burning_info_widget)
        self._oxid_mass_flow_rate_label.setText('Oxidant mass flow rate')
        self.oxid_mass_flow_rate = QtWidgets.QLabel(self._start_burning_info_widget)
        self.oxid_mass_flow_rate.setText('')

    def _setupMistureRatio(self):
        self._misture_ratio_label = QtWidgets.QLabel(self._start_burning_info_widget)
        self._misture_ratio_label.setText('Misture ratio o/f')
        self.misture_ratio = QtWidgets.QLabel(self._start_burning_info_widget)
        self.misture_ratio.setText('')

    def _setupStartRegressionRate(self):
        self._start_regression_rate_label = QtWidgets.QLabel(self._start_burning_info_widget)
        self._start_regression_rate_label.setText('Regression rate')
        self.start_regression_rate = QtWidgets.QLabel(self._start_burning_info_widget)
        self.start_regression_rate.setText('')

    def _setupStartInnerDiameter(self):
        self._start_inner_diameter_label = QtWidgets.QLabel(self._start_burning_info_widget)
        self._start_inner_diameter_label.setText('Grain inner diameter')
        self.start_inner_diameter = QtWidgets.QLabel(self._start_burning_info_widget)
        self.start_inner_diameter.setText('')

    def _setupStartGox(self):
        self._start_gox_label = QtWidgets.QLabel(self._start_burning_info_widget)
        self._start_gox_label.setText('Gox')
        self.start_gox = QtWidgets.QLabel(self._start_burning_info_widget)
        self.start_gox.setText('')

    def _setupStartOfBurningInfoLayout(self):
        mainlayout = QtWidgets.QFormLayout(self._start_burning_info_widget)
        mainlayout.setVerticalSpacing(12)
        mainlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._mass_flow_rate_label)
        mainlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._fuel_mass_flow_rate_label)
        mainlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.mass_flow_rate)
        mainlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fuel_mass_flow_rate)
        mainlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._oxid_mass_flow_rate_label)
        mainlayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._misture_ratio_label)
        mainlayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self._start_regression_rate_label)
        mainlayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self._start_inner_diameter_label)
        mainlayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self._start_gox_label)
        mainlayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.oxid_mass_flow_rate)
        mainlayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.misture_ratio)
        mainlayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.start_regression_rate)
        mainlayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.start_inner_diameter)
        mainlayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.start_gox)

    def _setupEndOfBurningInfoWidget(self):
        self._end_burning_info_widget = QtWidgets.QGroupBox(self)
        self._end_burning_info_widget.setGeometry(QtCore.QRect(280, 20, 251, 291))
        self._end_burning_info_widget.setTitle('End of Burning')
        self._setupEndInnerDiameter()
        self._setupEndRegressionRate()
        self._setupEndGox()
        self._setupEndOfBurningInfoLayout()

    def _setupEndInnerDiameter(self):
        self._end_inner_diameter_label = QtWidgets.QLabel(self._end_burning_info_widget)
        self._end_inner_diameter_label.setText('Grain inner diameter')
        self.end_inner_diameter = QtWidgets.QLabel(self._end_burning_info_widget)
        self.end_inner_diameter.setText('')

    def _setupEndRegressionRate(self):
        self._end_regression_rate_label = QtWidgets.QLabel(self._end_burning_info_widget)
        self._end_regression_rate_label.setText('Regression rate')
        self.end_regression_rate = QtWidgets.QLabel(self._end_burning_info_widget)
        self.end_regression_rate.setText('')

    def _setupEndGox(self):
        self._end_gox_label = QtWidgets.QLabel(self._end_burning_info_widget)
        self._end_gox_label.setText('Gox')
        self.end_gox = QtWidgets.QLabel(self._end_burning_info_widget)
        self.end_gox.setText('')

    def _setupEndOfBurningInfoLayout(self):
        mainlayout = QtWidgets.QFormLayout(self._end_burning_info_widget)
        mainlayout.setVerticalSpacing(12)
        mainlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._end_inner_diameter_label)
        mainlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.end_inner_diameter)
        mainlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._end_regression_rate_label)
        mainlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.end_regression_rate)
        mainlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._end_gox_label)
        mainlayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.end_gox)

    def _setupMotorGeometryInfoWidget(self):
        self._motor_geometry_info_widget = QtWidgets.QGroupBox(self)
        self._motor_geometry_info_widget.setGeometry(QtCore.QRect(540, 20, 251, 291))
        self._motor_geometry_info_widget.setTitle('Motor Geometry')
        self._setupNozzleThroatArea()
        self._setupNozzleThroatDiameter()
        self._setupNozzleExitArea()
        self._setupNozzleExitDiameter()
        self._setupGrainLength()
        self._setupMotorGeometryInfoLayout()

    def _setupNozzleThroatArea(self):
        self._nozzle_throat_area_label = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self._nozzle_throat_area_label.setText('Nozzle throat area')
        self.nozzle_throat_area = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self.nozzle_throat_area.setText('')

    def _setupNozzleThroatDiameter(self):
        self._nozzle_throat_diameter_label = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self._nozzle_throat_diameter_label.setText('Nozzle throat diameter')
        self.nozzle_throat_diameter = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self.nozzle_throat_diameter.setText('')

    def _setupNozzleExitArea(self):
        self._nozzle_exit_area_label = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self._nozzle_exit_area_label.setText('Nozzle exit area')
        self.nozzle_exit_area = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self.nozzle_exit_area.setText('')

    def _setupNozzleExitDiameter(self):
        self._nozzle_exit_diameter_label = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self._nozzle_exit_diameter_label.setText('Nozzle exit diameter')
        self.nozzle_exit_diameter = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self.nozzle_exit_diameter.setText('')

    def _setupGrainLength(self):
        self._grain_length_label = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self._grain_length_label.setText('Grain length')
        self.grain_length = QtWidgets.QLabel(self._motor_geometry_info_widget)
        self.grain_length.setText('')

    def _setupMotorGeometryInfoLayout(self):
        mainlayout = QtWidgets.QFormLayout(self._motor_geometry_info_widget)
        mainlayout.setVerticalSpacing(12)
        mainlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._nozzle_throat_area_label)
        mainlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._nozzle_throat_diameter_label)
        mainlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._nozzle_exit_area_label)
        mainlayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._nozzle_exit_diameter_label)
        mainlayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self._grain_length_label)
        mainlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nozzle_throat_area)
        mainlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.nozzle_throat_diameter)
        mainlayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.nozzle_exit_area)
        mainlayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.nozzle_exit_diameter)
        mainlayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.grain_length)

    def _setupResultsTabButtons(self):
        self.export_results_btn = QtWidgets.QPushButton(self)
        self.export_results_btn.setGeometry(QtCore.QRect(355, 330, 101, 23))
        self.export_results_btn.setText('Export Results')


class _PlotsTab(QtWidgets.QWidget):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setupUi()

    def _setupUi(self):
        self._setupPlotInfo()
        self._setupPlotWidget()
        self._setupPlotTabLayout()

    def _setupPlotInfo(self):
        self._plot_info_widget = QtWidgets.QWidget(self)
        self._plot_info_widget.setGeometry(QtCore.QRect(10, 0, 791, 80))
        self._setupYVariable()
        self._setupLocale()
        self._setupGeneratePlotButton()

    def _setupYVariable(self):
        self._variable_y_axis_label = QtWidgets.QLabel(self._plot_info_widget)
        self._variable_y_axis_label.setText('Variable of Interest(Y-Axis)')
        self.variable_y_axis = QtWidgets.QComboBox(self._plot_info_widget)
        self.variable_y_axis.addItem('Grain Inner Diameter')
        self.variable_y_axis.addItem('Fuel Mass Flow Rate')
        self.variable_y_axis.addItem('Misture Ratio o/f')
        self.variable_y_axis.addItem('Regression Rate')
        self.variable_y_axis.addItem('c*')
        self.variable_y_axis.addItem('Cf')
        self.variable_y_axis.addItem('Isp')
        self.variable_y_axis.addItem('Gox')
        self.variable_y_axis.addItem('Thrust')

    def _setupLocale(self):
        self._plot_locale_label = QtWidgets.QLabel(self._plot_info_widget)
        self._plot_locale_label.setText('Locale')
        self.plot_locale = QtWidgets.QComboBox(self._plot_info_widget)
        self.plot_locale.addItem('en_US')
        self.plot_locale.addItem('pt_BR')

    def _setupGeneratePlotButton(self):
        self.generate_plot_btn = QtWidgets.QPushButton(self._plot_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generate_plot_btn.sizePolicy().hasHeightForWidth())
        self.generate_plot_btn.setSizePolicy(sizePolicy)
        self.generate_plot_btn.setText('Generate Plot')
        self._left_spacer_generate_plot_btn = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._right_spacer_generate_plot_btn = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupPlotWidget(self):
        self.plot_widget = pg.GraphicsLayoutWidget(self)
        self.plot_widget.setGeometry(QtCore.QRect(0, 90, 810, 470))
        self.plot_widget.setBackground(None)

    def _setupPlotTabLayout(self):
        formlayout = QtWidgets.QFormLayout()
        formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._variable_y_axis_label)
        formlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.variable_y_axis)
        hlayout_locale = QtWidgets.QHBoxLayout()
        hlayout_locale.addWidget(self._plot_locale_label)
        hlayout_locale.addWidget(self.plot_locale)
        info_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        hlayout_info = QtWidgets.QHBoxLayout()
        hlayout_info.addLayout(formlayout)
        hlayout_info.addItem(info_spacer)
        hlayout_info.addLayout(hlayout_locale)
        hlayout_btn = QtWidgets.QHBoxLayout()
        hlayout_btn.addItem(self._left_spacer_generate_plot_btn)
        hlayout_btn.addWidget(self.generate_plot_btn)
        hlayout_btn.addItem(self._right_spacer_generate_plot_btn)
        vmainlayout = QtWidgets.QVBoxLayout(self._plot_info_widget)
        vmainlayout.setContentsMargins(0, 5, 5, 5)
        vmainlayout.setSpacing(5)
        vmainlayout.addLayout(hlayout_info)
        vmainlayout.addLayout(hlayout_btn)
