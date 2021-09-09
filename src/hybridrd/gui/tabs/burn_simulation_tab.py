import math
from PyQt5 import QtCore, QtWidgets


class BurnSimulationTab(QtWidgets.QWidget):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setupUi()

    def _setupUi(self):
        self._setupStartingPointInfoWidget()
        self._setupPropellantInfoWidget()
        self._setupGrainInfoWidget()
        self._setupCombustionInfoWidget()
        self._setupNozzleGeometryInfoWidget()
        self._setupBurnSimulationTabButtons()
        self._setupConnections()

    def _setupStartingPointInfoWidget(self):
        self._starting_point_info_widget = QtWidgets.QGroupBox(self)
        self._starting_point_info_widget.setGeometry(QtCore.QRect(80, 10, 291, 171))
        self._starting_point_info_widget.setTitle('Starting Point')
        self._setupInitialOf()
        self._setupInitialCstar()
        self._setupInitialCf()
        self._setupAeAtRatio()
        self._setupStartingPointButton()
        self._setupStartingPointInfoLayout()

    def _setupInitialOf(self):
        self._initial_of_label = QtWidgets.QLabel(self._starting_point_info_widget)
        self._initial_of_label.setText('Initial o/f')
        self.initial_of = QtWidgets.QLineEdit(self._starting_point_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initial_of.sizePolicy().hasHeightForWidth())
        self.initial_of.setSizePolicy(sizePolicy)
        self.initial_of.setReadOnly(True)
        self._initial_of_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupInitialCstar(self):
        self._initial_cstar_label = QtWidgets.QLabel(self._starting_point_info_widget)
        self._initial_cstar_label.setText('Initial c*')
        self._initial_cstar_unit = QtWidgets.QLabel(self._starting_point_info_widget)
        self._initial_cstar_unit.setText('m/s')
        self.initial_cstar = QtWidgets.QLineEdit(self._starting_point_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initial_cstar.sizePolicy().hasHeightForWidth())
        self.initial_cstar.setSizePolicy(sizePolicy)
        self.initial_cstar.setReadOnly(True)

    def _setupInitialCf(self):
        self._initial_cf_label = QtWidgets.QLabel(self._starting_point_info_widget)
        self._initial_cf_label.setText('Initial Cf')
        self.initial_cf = QtWidgets.QLineEdit(self._starting_point_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initial_cf.sizePolicy().hasHeightForWidth())
        self.initial_cf.setSizePolicy(sizePolicy)
        self.initial_cf.setReadOnly(True)
        self._initial_cf_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupAeAtRatio(self):
        self._aeat_ratio_label = QtWidgets.QLabel(self._starting_point_info_widget)
        self._aeat_ratio_label.setText('Ae/At Ratio')
        self.aeat_ratio = QtWidgets.QLineEdit(self._starting_point_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aeat_ratio.sizePolicy().hasHeightForWidth())
        self.aeat_ratio.setSizePolicy(sizePolicy)
        self.aeat_ratio.setReadOnly(True)
        self._aeat_ratio_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupStartingPointButton(self):
        self._left_spacer_starting_point_btn = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.select_starting_point_btn = QtWidgets.QPushButton(self)
        self.select_starting_point_btn.setText('Select Starting Point')

    def _setupStartingPointInfoLayout(self):
        hlayout_of = QtWidgets.QHBoxLayout()
        hlayout_of.addWidget(self.initial_of)
        hlayout_of.addItem(self._initial_of_spacer_item)
        hlayout_cstar = QtWidgets.QHBoxLayout()
        hlayout_cstar.addWidget(self.initial_cstar)
        hlayout_cstar.addWidget(self._initial_cstar_unit)
        hlayout_cf = QtWidgets.QHBoxLayout()
        hlayout_cf.addWidget(self.initial_cf)
        hlayout_cf.addItem(self._initial_cf_spacer_item)
        hlayout_aeat = QtWidgets.QHBoxLayout()
        hlayout_aeat.addWidget(self.aeat_ratio)
        hlayout_aeat.addItem(self._aeat_ratio_spacer_item)
        hlayout_select_btn = QtWidgets.QHBoxLayout()
        hlayout_select_btn.addItem(self._left_spacer_starting_point_btn)
        hlayout_select_btn.addWidget(self.select_starting_point_btn)
        formlayout = QtWidgets.QFormLayout()
        formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._initial_of_label)
        formlayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, hlayout_of)
        formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._initial_cstar_label)
        formlayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, hlayout_cstar)
        formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._initial_cf_label)
        formlayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, hlayout_cf)
        formlayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._aeat_ratio_label)
        formlayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, hlayout_aeat)
        vmainlayout = QtWidgets.QVBoxLayout(self._starting_point_info_widget)
        vmainlayout.setContentsMargins(5, 5, 5, 5)
        vmainlayout.addLayout(formlayout)
        vmainlayout.addLayout(hlayout_select_btn)

    def _setupPropellantInfoWidget(self):
        self._propellant_info_widget = QtWidgets.QGroupBox(self)
        self._propellant_info_widget.setGeometry(QtCore.QRect(80, 200, 291, 145))
        self._propellant_info_widget.setTitle('Propellant')
        self._setupFuelDensity()
        self._setupRegressionParameters()
        self._setupInsertRegressionParametersButton()
        self._setupPropellantInfoLayout()

    def _setupFuelDensity(self):
        self._fuel_density_label = QtWidgets.QLabel(self._propellant_info_widget)
        self._fuel_density_label.setText('Fuel Density')
        self._fuel_density_unit = QtWidgets.QLabel(self._propellant_info_widget)
        self._fuel_density_unit.setText('g/cm³')
        self.fuel_density = QtWidgets.QLineEdit(self._propellant_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fuel_density.sizePolicy().hasHeightForWidth())
        self.fuel_density.setSizePolicy(sizePolicy)

    def _setupRegressionParameters(self):
        self._regression_parameter_a_label = QtWidgets.QLabel(self._propellant_info_widget)
        self._regression_parameter_a_label.setText('Parameter a')
        self.regression_parameter_a = QtWidgets.QLineEdit(self._propellant_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regression_parameter_a.sizePolicy().hasHeightForWidth())
        self.regression_parameter_a.setSizePolicy(sizePolicy)
        self.regression_parameter_a.setReadOnly(True)
        self._regression_parameter_a_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._regression_parameter_n_label = QtWidgets.QLabel(self._propellant_info_widget)
        self._regression_parameter_n_label.setText('Parameter n')
        self.regression_parameter_n = QtWidgets.QLineEdit(self._propellant_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regression_parameter_n.sizePolicy().hasHeightForWidth())
        self.regression_parameter_n.setSizePolicy(sizePolicy)
        self.regression_parameter_n.setReadOnly(True)
        self._regression_parameter_n_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupInsertRegressionParametersButton(self):
        self._left_spacer_regression_btn = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.insert_regression_parameters_btn = QtWidgets.QPushButton(self._propellant_info_widget)
        self.insert_regression_parameters_btn.setText('Insert Regression Parameters')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.insert_regression_parameters_btn.sizePolicy().hasHeightForWidth())
        self.insert_regression_parameters_btn.setSizePolicy(sizePolicy)

    def _setupPropellantInfoLayout(self):
        hlayout_fuel_density = QtWidgets.QHBoxLayout()
        hlayout_fuel_density.addWidget(self.fuel_density)
        hlayout_fuel_density.addWidget(self._fuel_density_unit)
        hlayout_parameter_a = QtWidgets.QHBoxLayout()
        hlayout_parameter_a.addWidget(self.regression_parameter_a)
        hlayout_parameter_a.addItem(self._regression_parameter_a_spacer_item)
        hlayout_parameter_n = QtWidgets.QHBoxLayout()
        hlayout_parameter_n.addWidget(self.regression_parameter_n)
        hlayout_parameter_n.addItem(self._regression_parameter_n_spacer_item)
        hlayout_btn = QtWidgets.QHBoxLayout()
        hlayout_btn.addItem(self._left_spacer_regression_btn)
        hlayout_btn.addWidget(self.insert_regression_parameters_btn)
        formlayout = QtWidgets.QFormLayout()
        formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._fuel_density_label)
        formlayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, hlayout_fuel_density)
        formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._regression_parameter_a_label)
        formlayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, hlayout_parameter_a)
        formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._regression_parameter_n_label)
        formlayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, hlayout_parameter_n)
        vmainlayout = QtWidgets.QVBoxLayout(self._propellant_info_widget)
        vmainlayout.setContentsMargins(5, 5, 5, 5)
        vmainlayout.addLayout(formlayout)
        vmainlayout.addLayout(hlayout_btn)

    def _setupGrainInfoWidget(self):
        self._grain_info_widget = QtWidgets.QGroupBox(self)
        self._grain_info_widget.setGeometry(QtCore.QRect(450, 10, 301, 171))
        self._grain_info_widget.setTitle('Grain')
        self._setupCalculationMethod()
        self._setupInnerDiameter()
        self._setupOuterDiameter()
        self._setupLength()
        self._setupGrainInfoLayout()

    def _setupCalculationMethod(self):
        self._method_label = QtWidgets.QLabel(self._grain_info_widget)
        self._method_label.setText('Method')
        self.method = QtWidgets.QComboBox(self._grain_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.method.sizePolicy().hasHeightForWidth())
        self.method.setSizePolicy(sizePolicy)
        self.method.addItem('Inner diameter known')
        self.method.addItem('Outer diameter known')
        self.method.addItem('Length known')

    def _setupInnerDiameter(self):
        self._grain_inner_diameter_label = QtWidgets.QLabel(self._grain_info_widget)
        self._grain_inner_diameter_label.setText('Inner Diameter')
        self._grain_inner_diameter_unit = QtWidgets.QLabel(self._grain_info_widget)
        self._grain_inner_diameter_unit.setText('mm')
        self.grain_inner_diameter = QtWidgets.QLineEdit(self._grain_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grain_inner_diameter.sizePolicy().hasHeightForWidth())
        self.grain_inner_diameter.setSizePolicy(sizePolicy)

    def _setupOuterDiameter(self):
        self._grain_outer_diameter_label = QtWidgets.QLabel(self._grain_info_widget)
        self._grain_outer_diameter_label.setText('Outer Diameter')
        self._grain_outer_diameter_unit = QtWidgets.QLabel(self._grain_info_widget)
        self._grain_outer_diameter_unit.setText('mm')
        self.grain_outer_diameter = QtWidgets.QLineEdit(self._grain_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grain_outer_diameter.sizePolicy().hasHeightForWidth())
        self.grain_outer_diameter.setSizePolicy(sizePolicy)
        self.grain_outer_diameter.setEnabled(False)

    def _setupLength(self):
        self._grain_length_label = QtWidgets.QLabel(self._grain_info_widget)
        self._grain_length_label.setText('Length')
        self._grain_length_unit = QtWidgets.QLabel(self._grain_info_widget)
        self._grain_length_unit.setText('cm')
        self.grain_length = QtWidgets.QLineEdit(self._grain_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grain_length.sizePolicy().hasHeightForWidth())
        self.grain_length.setSizePolicy(sizePolicy)
        self.grain_length.setEnabled(False)

    def _setupGrainInfoLayout(self):
        hlayout_inner = QtWidgets.QHBoxLayout()
        hlayout_inner.addWidget(self.grain_inner_diameter)
        hlayout_inner.addWidget(self._grain_inner_diameter_unit)
        hlayout_outer = QtWidgets.QHBoxLayout()
        hlayout_outer.addWidget(self.grain_outer_diameter)
        hlayout_outer.addWidget(self._grain_outer_diameter_unit)
        hlayout_length = QtWidgets.QHBoxLayout()
        hlayout_length.addWidget(self.grain_length)
        hlayout_length.addWidget(self._grain_length_unit)
        formlayout = QtWidgets.QFormLayout(self._grain_info_widget)
        formlayout.setContentsMargins(5, 5, 5, 5)
        formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._method_label)
        formlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.method)
        formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._grain_inner_diameter_label)
        formlayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, hlayout_inner)
        formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._grain_outer_diameter_label)
        formlayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, hlayout_outer)
        formlayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._grain_length_label)
        formlayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, hlayout_length)

    def _setupCombustionInfoWidget(self):
        self._combustion_info_widget = QtWidgets.QGroupBox(self)
        self._combustion_info_widget.setGeometry(QtCore.QRect(450, 200, 301, 145))
        self._combustion_info_widget.setTitle('Combustion')
        self._setupInitialThrust()
        self._setupBurnDuration()
        self._setupChamberPressure()
        self._setupCombustionInfoLayout()

    def _setupInitialThrust(self):
        self._initial_thrust_label = QtWidgets.QLabel(self._combustion_info_widget)
        self._initial_thrust_label.setText('Initial Thrust')
        self._initial_thrust_unit = QtWidgets.QLabel(self._combustion_info_widget)
        self._initial_thrust_unit.setText('N')
        self.initial_thrust = QtWidgets.QLineEdit(self._combustion_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initial_thrust.sizePolicy().hasHeightForWidth())
        self.initial_thrust.setSizePolicy(sizePolicy)

    def _setupBurnDuration(self):
        self._burn_duration_label = QtWidgets.QLabel(self._combustion_info_widget)
        self._burn_duration_label.setText('Burn Duration')
        self._burn_duration_unit = QtWidgets.QLabel(self._combustion_info_widget)
        self._burn_duration_unit.setText('s')
        self.burn_duration = QtWidgets.QLineEdit(self._combustion_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.burn_duration.sizePolicy().hasHeightForWidth())
        self.burn_duration.setSizePolicy(sizePolicy)

    def _setupChamberPressure(self):
        self._chamber_pressure_label = QtWidgets.QLabel(self._combustion_info_widget)
        self._chamber_pressure_label.setText('Chamber Pressure')
        self._chamber_pressure_unit = QtWidgets.QLabel(self._combustion_info_widget)
        self._chamber_pressure_unit.setText('bar')
        self.chamber_pressure = QtWidgets.QLineEdit(self._combustion_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chamber_pressure.sizePolicy().hasHeightForWidth())
        self.chamber_pressure.setSizePolicy(sizePolicy)
        self.chamber_pressure.setEnabled(False)

    def _setupCombustionInfoLayout(self):
        hlayout_thrust = QtWidgets.QHBoxLayout()
        hlayout_thrust.addWidget(self.initial_thrust)
        hlayout_thrust.addWidget(self._initial_thrust_unit)
        hlayout_burn = QtWidgets.QHBoxLayout()
        hlayout_burn.addWidget(self.burn_duration)
        hlayout_burn.addWidget(self._burn_duration_unit)
        hlayout_chamber = QtWidgets.QHBoxLayout()
        hlayout_chamber.addWidget(self.chamber_pressure)
        hlayout_chamber.addWidget(self._chamber_pressure_unit)
        formlayout = QtWidgets.QFormLayout(self._combustion_info_widget)
        formlayout.setContentsMargins(5, 5, 5, 5)
        formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._initial_thrust_label)
        formlayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, hlayout_thrust)
        formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._burn_duration_label)
        formlayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, hlayout_burn)
        formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._chamber_pressure_label)
        formlayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, hlayout_chamber)

    def _setupNozzleGeometryInfoWidget(self):
        self._nozzle_geometry_info_widget = QtWidgets.QGroupBox(self)
        self._nozzle_geometry_info_widget.setGeometry(QtCore.QRect(80, 370, 671, 91))
        self._nozzle_geometry_info_widget.setTitle('Nozzle Geometry Information')
        self._setupNozzleCfCorrection()
        self._setupNozzleThroatArea()
        self._setupNozzleThroatDiameter()
        self._setupAcAtRatio()
        self._setupNozzleGeometryInfoLayout()

    def _setupNozzleCfCorrection(self):
        self._cf_correction_label = QtWidgets.QLabel(self._nozzle_geometry_info_widget)
        self._cf_correction_label.setText('Nozzle Cf Correction')
        self.cf_correction = QtWidgets.QLineEdit(self._nozzle_geometry_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cf_correction.sizePolicy().hasHeightForWidth())
        self.cf_correction.setSizePolicy(sizePolicy)
        self.cf_correction.setEnabled(False)
        self.cf_correction.setText('1.000')
        self._cf_correction_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupNozzleThroatArea(self):
        self._nozzle_throat_area_label = QtWidgets.QLabel(self._nozzle_geometry_info_widget)
        self._nozzle_throat_area_label.setText('Nozzle Throat Area')
        self._nozzle_throat_area_unit = QtWidgets.QLabel(self._nozzle_geometry_info_widget)
        self._nozzle_throat_area_unit.setText('mm²')
        self.nozzle_throat_area = QtWidgets.QLineEdit(self._nozzle_geometry_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nozzle_throat_area.sizePolicy().hasHeightForWidth())
        self.nozzle_throat_area.setSizePolicy(sizePolicy)
        self.nozzle_throat_area.setEnabled(False)

    def _setupNozzleThroatDiameter(self):
        self._nozzle_throat_diameter_label = QtWidgets.QLabel(self._nozzle_geometry_info_widget)
        self._nozzle_throat_diameter_label.setText('Nozzle Throat Diameter')
        self._nozzle_throat_diameter_unit = QtWidgets.QLabel(self._nozzle_geometry_info_widget)
        self._nozzle_throat_diameter_unit.setText('mm')
        self.nozzle_throat_diameter = QtWidgets.QLineEdit(self._nozzle_geometry_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nozzle_throat_diameter.sizePolicy().hasHeightForWidth())
        self.nozzle_throat_diameter.setSizePolicy(sizePolicy)
        self.nozzle_throat_diameter.setEnabled(False)

    def _setupAcAtRatio(self):
        self._ac_at_ratio_label = QtWidgets.QLabel(self._nozzle_geometry_info_widget)
        self._ac_at_ratio_label.setText('Ac/At Ratio')
        self.ac_at_ratio = QtWidgets.QLineEdit(self._nozzle_geometry_info_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ac_at_ratio.sizePolicy().hasHeightForWidth())
        self.ac_at_ratio.setSizePolicy(sizePolicy)
        self.ac_at_ratio.setEnabled(False)
        self._ac_at_ratio_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupNozzleGeometryInfoLayout_old(self):
        hlayout_cf = QtWidgets.QHBoxLayout()
        hlayout_cf.addWidget(self.cf_correction)
        hlayout_cf.addItem(self._cf_correction_spacer)
        hlayout_throat = QtWidgets.QHBoxLayout()
        hlayout_throat.addWidget(self.nozzle_throat_area)
        hlayout_throat.addWidget(self._nozzle_throat_area_unit)
        hlayout_throat_diameter = QtWidgets.QHBoxLayout()
        hlayout_throat_diameter.addWidget(self.nozzle_throat_diameter)
        hlayout_throat_diameter.addWidget(self._nozzle_throat_diameter_unit)
        hlayout_acat = QtWidgets.QHBoxLayout()
        hlayout_acat.addWidget(self.ac_at_ratio)
        hlayout_acat.addItem(self._ac_at_ratio_spacer)
        formlayout = QtWidgets.QFormLayout(self._nozzle_geometry_info_widget)
        formlayout.setContentsMargins(5, 5, 5, 5)
        formlayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._cf_correction_label)
        formlayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, hlayout_cf)
        formlayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._nozzle_throat_area_label)
        formlayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, hlayout_throat)
        formlayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._nozzle_throat_diameter_label)
        formlayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, hlayout_throat_diameter)
        formlayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._ac_at_ratio_label)
        formlayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, hlayout_acat)

    def _setupNozzleGeometryInfoLayout(self):
        hlayout_cf = QtWidgets.QHBoxLayout()
        hlayout_cf.addWidget(self.cf_correction)
        hlayout_cf.addItem(self._cf_correction_spacer)
        hlayout_throat = QtWidgets.QHBoxLayout()
        hlayout_throat.addWidget(self.nozzle_throat_area)
        hlayout_throat.addWidget(self._nozzle_throat_area_unit)
        hlayout_throat_diameter = QtWidgets.QHBoxLayout()
        hlayout_throat_diameter.addWidget(self.nozzle_throat_diameter)
        hlayout_throat_diameter.addWidget(self._nozzle_throat_diameter_unit)
        hlayout_acat = QtWidgets.QHBoxLayout()
        hlayout_acat.addWidget(self.ac_at_ratio)
        hlayout_acat.addItem(self._ac_at_ratio_spacer)
        formlayout_left = QtWidgets.QFormLayout()
        formlayout_left.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._cf_correction_label)
        formlayout_left.setLayout(0, QtWidgets.QFormLayout.FieldRole, hlayout_cf)
        formlayout_left.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._nozzle_throat_area_label)
        formlayout_left.setLayout(1, QtWidgets.QFormLayout.FieldRole, hlayout_throat)
        formlayout_right = QtWidgets.QFormLayout()
        formlayout_right.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._nozzle_throat_diameter_label)
        formlayout_right.setLayout(2, QtWidgets.QFormLayout.FieldRole, hlayout_throat_diameter)
        formlayout_right.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._ac_at_ratio_label)
        formlayout_right.setLayout(3, QtWidgets.QFormLayout.FieldRole, hlayout_acat)
        spacer_between_forms = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        mainhlayout = QtWidgets.QHBoxLayout(self._nozzle_geometry_info_widget)
        mainhlayout.setContentsMargins(5, 5, 5, 5)
        mainhlayout.addLayout(formlayout_left)
        mainhlayout.addItem(spacer_between_forms)
        mainhlayout.addLayout(formlayout_right)

    def _setupBurnSimulationTabButtons(self):
        self.simulate_burn_btn = QtWidgets.QPushButton(self)
        self.simulate_burn_btn.setGeometry(QtCore.QRect(365, 490, 101, 23))
        self.simulate_burn_btn.setText('Simulate Burn')
        self.simulate_burn_btn.setEnabled(False)

    def _setupConnections(self):
        self._setupDataValidationConnections()
        self.method.currentIndexChanged.connect(lambda: self._changeBurnSimulationMethod())
        self.initial_cstar.textChanged.connect(lambda: self._updateNozzleThroatAreaField())
        self.initial_thrust.textChanged.connect(lambda: self._updateNozzleThroatAreaField())
        self.nozzle_throat_area.textChanged.connect(lambda: self._updateNozzleThroatDiameterField())
        self.fuel_density.textChanged.connect(lambda: self._updateAcAtRatioField())
        self.regression_parameter_a.textChanged.connect(lambda: self._updateAcAtRatioField())
        self.regression_parameter_n.textChanged.connect(lambda: self._updateAcAtRatioField())
        self.burn_duration.textChanged.connect(lambda: self._updateAcAtRatioField())
        self.nozzle_throat_diameter.textChanged.connect(lambda: self._updateAcAtRatioField())
        self.grain_inner_diameter.textChanged.connect(lambda: self._updateAcAtRatioField())
        self.grain_outer_diameter.textChanged.connect(lambda: self._updateAcAtRatioField())
        self.grain_length.textChanged.connect(lambda: self._updateAcAtRatioField())

    def _setupDataValidationConnections(self):
        self.fuel_density.textChanged.connect(lambda: self._validateData(self.fuel_density))
        self.grain_inner_diameter.textChanged.connect(lambda: self._validateData(self.grain_inner_diameter))
        self.grain_outer_diameter.textChanged.connect(lambda: self._validateData(self.grain_outer_diameter))
        self.grain_length.textChanged.connect(lambda: self._validateData(self.grain_length))
        self.initial_thrust.textChanged.connect(lambda: self._validateData(self.initial_thrust))
        self.burn_duration.textChanged.connect(lambda: self._validateData(self.burn_duration))
        self.chamber_pressure.textChanged.connect(lambda: self._validateData(self.chamber_pressure))
        self.ac_at_ratio.textChanged.connect(lambda: self._validateAcAtData(self.ac_at_ratio))

    def _validateData(self, field):
        try:
            field_value = float(field.text())
            if field_value < 0:
                field.setProperty('error', True)
            else:
                field.setProperty('error', False)
        except Exception:
            if field.text() == '':
                field.setProperty('error', False)
            else:
                field.setProperty('error', True)
        field.setStyle(field.style())

    def _validateAcAtData(self, field):
        try:
            field_value = float(field.text())
            if field_value < 6:
                field.setProperty('error', True)
            else:
                field.setProperty('error', False)
        except Exception:
            if field.text() == '':
                field.setProperty('error', False)
            else:
                field.setProperty('error', True)
        field.setStyle(field.style())

    def _changeBurnSimulationMethod(self):
        if str(self.method.currentText()) == 'Inner diameter known':
            self.grain_inner_diameter.setEnabled(True)
            self.grain_length.setText('')
            self.grain_outer_diameter.setText('')
            self.grain_length.setEnabled(False)
            self.grain_outer_diameter.setEnabled(False)
        elif str(self.method.currentText()) == 'Outer diameter known':
            self.grain_outer_diameter.setEnabled(True)
            self.grain_inner_diameter.setText('')
            self.grain_length.setText('')
            self.grain_inner_diameter.setEnabled(False)
            self.grain_length.setEnabled(False)
        else:
            self.grain_length.setEnabled(True)
            self.grain_inner_diameter.setText('')
            self.grain_outer_diameter.setText('')
            self.grain_inner_diameter.setEnabled(False)
            self.grain_outer_diameter.setEnabled(False)

    def _updateNozzleThroatAreaField(self):
        try:
            initial_thrust = float(self.initial_thrust.text())
            initial_cstar = float(self.initial_cstar.text())
            initial_cf = float(self.initial_cf.text())
            chamber_pressure = float(self.chamber_pressure.text()) * (10**5)
            initial_m_dot = initial_thrust / (initial_cstar * initial_cf)
            throat_area = (initial_m_dot * initial_cstar / chamber_pressure) * (10**6)
            self.nozzle_throat_area.setText(str(round(throat_area, 3)))
        except Exception:
            self.nozzle_throat_area.setText('')

    def _updateNozzleThroatDiameterField(self):
        try:
            throat_area = float(self.nozzle_throat_area.text())
            throat_diameter = math.sqrt(4 * throat_area / math.pi)
            self.nozzle_throat_diameter.setText(str(round(throat_diameter, 3)))
        except Exception:
            self.nozzle_throat_diameter.setText('')

    def _updateAcAtRatioField(self):
        chosen_method = self.method.currentText()
        try:
            throat_area = float(self.nozzle_throat_area.text())
            if chosen_method == 'Inner diameter known':
                inner_diameter = float(self.grain_inner_diameter.text())
                inner_area = math.pi * (inner_diameter**2) / 4
            elif chosen_method == 'Outer diameter known':
                a = self.regression_parameter_a_si
                n = float(self.regression_parameter_n.text())
                burn_time = float(self.burn_duration.text())
                outer_diameter = float(self.grain_outer_diameter.text())
                outer_radius = (outer_diameter / 2) / 1000  # mm to m
                of_ratio = float(self.initial_of.text())
                initial_thrust = float(self.initial_thrust.text())
                initial_cstar = float(self.initial_cstar.text())
                initial_cf = float(self.initial_cf.text())
                initial_m_dot = initial_thrust / (initial_cstar * initial_cf)
                initial_m_dot_fuel = (initial_m_dot) / (1 + of_ratio)
                m_dot_oxid = initial_m_dot_fuel * of_ratio
                inner_radius = ((outer_radius**(2 * n + 1)) - a * (2 * n + 1) * ((m_dot_oxid / math.pi)**n) * burn_time)**(1 / (2 * n + 1))
                inner_radius = inner_radius * 1000  # m to mm
                inner_area = math.pi * ((inner_radius)**2)
            elif chosen_method == 'Length known':
                a = self.regression_parameter_a_si
                n = float(self.regression_parameter_n.text())
                rho = float(self.fuel_density.text()) * 1000  # g/cm³ to kg/m³
                grain_length = float(self.grain_length.text()) / 100  # cm to m
                of_ratio = float(self.initial_of.text())
                initial_thrust = float(self.initial_thrust.text())
                initial_cstar = float(self.initial_cstar.text())
                initial_cf = float(self.initial_cf.text())
                initial_m_dot = initial_thrust / (initial_cstar * initial_cf)
                initial_m_dot_fuel = (initial_m_dot) / (1 + of_ratio)
                m_dot_oxid = initial_m_dot_fuel * of_ratio
                inner_radius = (initial_m_dot_fuel / (2 * grain_length * rho * a * (m_dot_oxid**n) * (math.pi**(1 - n))))**(1 / (1 - 2 * n))
                inner_radius = inner_radius * 1000  # m to mm
                inner_area = math.pi * ((inner_radius)**2)
            ac_at_ratio = inner_area / throat_area
            if isinstance(ac_at_ratio, complex):
                self.ac_at_ratio.setText(str(complex(round(ac_at_ratio.real, 2), round(ac_at_ratio.imag, 2))))
            else:
                self.ac_at_ratio.setText(str(round(ac_at_ratio, 3)))
        except Exception:
            self.ac_at_ratio.setText('')
