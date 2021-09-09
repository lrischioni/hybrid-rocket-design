from PyQt5 import QtCore, QtWidgets


class InputFileTab(QtWidgets.QWidget):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setupUi()

    def _setupUi(self):
        self._setupPropellantWidget()
        self._setupCombustionChamberWidget()
        self._setupExitConditions()
        self._setupInputFileTabButtons()
        self._setupConnections()

    def _setupPropellantWidget(self):
        self._propellant_input_file_widget = QtWidgets.QGroupBox(self)
        self._propellant_input_file_widget.setGeometry(QtCore.QRect(20, 60, 791, 181))
        self._propellant_input_file_widget.setTitle('Propellant')
        self._setupTableLabels()
        self._setupFuel()
        self._setupOxidant()
        self._setupMistureRatio()
        self._setupPropellantLayout()

    def _setupTableLabels(self):
        self._setupName()
        self._setupAmount()
        self._setupTemperature()
        self._setupEnergy()
        self._setupChemicalFormula()
        self._setupFuelLabel()
        self._setupOxidantLabel()

    def _setupName(self):
        self._propellant_name_label = QtWidgets.QLabel(self._propellant_input_file_widget)
        self._propellant_name_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self._propellant_name_label.setText('Name')

    def _setupAmount(self):
        self._propellant_amount_label = QtWidgets.QLabel(self._propellant_input_file_widget)
        self._propellant_amount_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self._propellant_amount_label.setText('Amount')

    def _setupTemperature(self):
        self._propellant_temperature_label = QtWidgets.QLabel(self._propellant_input_file_widget)
        self._propellant_temperature_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self._propellant_temperature_label.setText('Temperature (K)')

    def _setupEnergy(self):
        self._propellant_energy_h_label = QtWidgets.QLabel(self._propellant_input_file_widget)
        self._propellant_energy_h_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self._propellant_energy_h_label.setText('Energy H (kJ/mol)')

    def _setupChemicalFormula(self):
        self._propellant_chemical_formula_label = QtWidgets.QLabel(self._propellant_input_file_widget)
        self._propellant_chemical_formula_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self._propellant_chemical_formula_label.setText('Chemical Formula')

    def _setupFuelLabel(self):
        self._propellant_fuel_label = QtWidgets.QLabel(self._propellant_input_file_widget)
        self._propellant_fuel_label.setText('Fuel')

    def _setupOxidantLabel(self):
        self._propellant_oxidant_label = QtWidgets.QLabel(self._propellant_input_file_widget)
        self._propellant_oxidant_label.setText('Oxidant')

    def _setupFuel(self):
        self._setupFuelName()
        self._setupFuelAmount()
        self._setupFuelTemperature()
        self._setupFuelEnergy()
        self._setupFuelChemicalFormula()

    def _setupFuelName(self):
        self.fuel_name = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupFuelAmount(self):
        self.fuel_amount = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupFuelTemperature(self):
        self.fuel_temperature = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupFuelEnergy(self):
        self.fuel_energy = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupFuelChemicalFormula(self):
        self.fuel_chemical_formula = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupOxidant(self):
        self._setupOxidantName()
        self._setupOxidantAmount()
        self._setupOxidantTemperature()
        self._setupOxidantEnergy()
        self._setupOxidantChemicalFormula()

    def _setupOxidantName(self):
        self.oxidant_name = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupOxidantAmount(self):
        self.oxidant_amount = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupOxidantTemperature(self):
        self.oxidant_temperature = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupOxidantEnergy(self):
        self.oxidant_energy = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupOxidantChemicalFormula(self):
        self.oxidant_chemical_formula = QtWidgets.QLineEdit(self._propellant_input_file_widget)

    def _setupMistureRatio(self):
        self._misture_ratio_label = QtWidgets.QLabel(self._propellant_input_file_widget)
        self._misture_ratio_label.setText('Misture Ratio o/f')
        self.misture_ratio = QtWidgets.QLineEdit(self._propellant_input_file_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.misture_ratio.sizePolicy().hasHeightForWidth())
        self.misture_ratio.setSizePolicy(sizePolicy)
        self._misture_ratio_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupPropellantLayout(self):
        gridlayout = QtWidgets.QGridLayout()
        gridlayout.setHorizontalSpacing(20)
        gridlayout.setVerticalSpacing(15)
        gridlayout.addWidget(self._propellant_chemical_formula_label, 0, 5, 1, 1)
        gridlayout.addWidget(self._propellant_energy_h_label, 0, 4, 1, 1)
        gridlayout.addWidget(self.oxidant_name, 2, 1, 1, 1)
        gridlayout.addWidget(self._propellant_fuel_label, 1, 0, 1, 1)
        gridlayout.addWidget(self.fuel_name, 1, 1, 1, 1)
        gridlayout.addWidget(self.fuel_chemical_formula, 1, 5, 1, 1)
        gridlayout.addWidget(self._propellant_oxidant_label, 2, 0, 1, 1)
        gridlayout.addWidget(self.oxidant_chemical_formula, 2, 5, 1, 1)
        gridlayout.addWidget(self.oxidant_amount, 2, 2, 1, 1)
        gridlayout.addWidget(self.oxidant_temperature, 2, 3, 1, 1)
        gridlayout.addWidget(self.oxidant_energy, 2, 4, 1, 1)
        gridlayout.addWidget(self.fuel_amount, 1, 2, 1, 1)
        gridlayout.addWidget(self.fuel_temperature, 1, 3, 1, 1)
        gridlayout.addWidget(self.fuel_energy, 1, 4, 1, 1)
        gridlayout.addWidget(self._propellant_name_label, 0, 1, 1, 1)
        gridlayout.addWidget(self._propellant_temperature_label, 0, 3, 1, 1)
        gridlayout.addWidget(self._propellant_amount_label, 0, 2, 1, 1)
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self._misture_ratio_label)
        hlayout.addWidget(self.misture_ratio)
        hlayout.addItem(self._misture_ratio_spacer_item)
        mainvlayout = QtWidgets.QVBoxLayout(self._propellant_input_file_widget)
        mainvlayout.setContentsMargins(5, 5, 5, 5)
        mainvlayout.addLayout(gridlayout)
        vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        mainvlayout.addItem(vertical_spacer)
        mainvlayout.addLayout(hlayout)

    def _setupCombustionChamberWidget(self):
        self._combustion_input_file_widget = QtWidgets.QGroupBox(self)
        self._combustion_input_file_widget.setGeometry(QtCore.QRect(20, 260, 281, 151))
        self._combustion_input_file_widget.setTitle('Combustion Chamber')
        self._setupChamberPressure()
        self._setupCombustionMethod()
        self._setupFreezingPoint()
        self._setupCombustionChamberLayout()

    def _setupChamberPressure(self):
        self._chamber_pressure_label = QtWidgets.QLabel(self._combustion_input_file_widget)
        self._chamber_pressure_label.setText('Chamber Pressure')
        self._chamber_pressure_unit = QtWidgets.QLabel(self._combustion_input_file_widget)
        self._chamber_pressure_unit.setText('bar')
        self.chamber_pressure = QtWidgets.QLineEdit(self._combustion_input_file_widget)
        self._chamber_pressure_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupCombustionMethod(self):
        self.equilibrium_checkbox = QtWidgets.QCheckBox(self._combustion_input_file_widget)
        self.equilibrium_checkbox.setText('Equilibrium')
        self.frozen_checkbox = QtWidgets.QCheckBox(self._combustion_input_file_widget)
        self.frozen_checkbox.setText('Frozen')
        self._button_group = QtWidgets.QButtonGroup()
        self._button_group.addButton(self.equilibrium_checkbox, 1)
        self._button_group.addButton(self.frozen_checkbox, 2)
        self.equilibrium_checkbox.setChecked(True)

    def _setupFreezingPoint(self):
        self._freezing_point_label = QtWidgets.QLabel(self._combustion_input_file_widget)
        self._freezing_point_label.setText('Freezing Point')
        self.freezing_point = QtWidgets.QComboBox(self._combustion_input_file_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freezing_point.sizePolicy().hasHeightForWidth())
        self.freezing_point.setSizePolicy(sizePolicy)
        self.freezing_point.setMinimumSize(QtCore.QSize(10, 0))
        self.freezing_point.addItem('Combustor')
        self.freezing_point.addItem('Throat')
        self.freezing_point.addItem('Exit1')
        self._freezing_point_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.freezing_point.setEnabled(False)

    def _setupCombustionChamberLayout(self):
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self._chamber_pressure_label)
        hlayout.addWidget(self.chamber_pressure)
        hlayout.addWidget(self._chamber_pressure_unit)
        hlayout.addItem(self._chamber_pressure_spacer_item)
        hlayout2 = QtWidgets.QHBoxLayout()
        hlayout2.addWidget(self._freezing_point_label)
        hlayout2.addWidget(self.freezing_point)
        hlayout2.addItem(self._freezing_point_spacer_item)
        mainvlayout = QtWidgets.QVBoxLayout(self._combustion_input_file_widget)
        mainvlayout.setContentsMargins(5, 5, 5, 5)
        mainvlayout.addLayout(hlayout)
        mainvlayout.addWidget(self.equilibrium_checkbox)
        mainvlayout.addWidget(self.frozen_checkbox)
        mainvlayout.addLayout(hlayout2)

    def _setupExitConditions(self):
        self._exit_input_file_widget = QtWidgets.QGroupBox(self)
        self._exit_input_file_widget.setGeometry(QtCore.QRect(530, 260, 281, 71))
        self._exit_input_file_widget.setTitle('Exit Conditions')
        self._setupPressureRatio()
        self._setupExitConditionsLayout()

    def _setupPressureRatio(self):
        self._pressure_ratio_label = QtWidgets.QLabel(self._exit_input_file_widget)
        self._pressure_ratio_label.setText('Pressure Ratio pi/p')
        self.pressure_ratio = QtWidgets.QLineEdit(self._exit_input_file_widget)

    def _setupExitConditionsLayout(self):
        hlayout = QtWidgets.QHBoxLayout(self._exit_input_file_widget)
        hlayout.setContentsMargins(5, 5, 5, 5)
        hlayout.addWidget(self._pressure_ratio_label)
        hlayout.addWidget(self.pressure_ratio)

    def _setupInputFileTabButtons(self):
        self.save_changes_btn = QtWidgets.QPushButton(self)
        self.save_changes_btn.setGeometry(QtCore.QRect(330, 460, 94, 23))
        self.save_changes_btn.setText('Save Changes')
        self.save_changes_btn.setEnabled(False)
        self.run_cea_btn = QtWidgets.QPushButton(self)
        self.run_cea_btn.setGeometry(QtCore.QRect(430, 460, 80, 23))
        self.run_cea_btn.setText('Run CEA')
        self.run_cea_btn.setEnabled(False)
        self.import_cea_file_btn = QtWidgets.QPushButton(self)
        self.import_cea_file_btn.setGeometry(QtCore.QRect(20, 20, 80, 23))
        self.import_cea_file_btn.setText('Import File')

    def _setupConnections(self):
        self._setupSaveChangesEventsSignals()
        self._setupCheckboxSelectionConnection()

    def _setupSaveChangesEventsSignals(self):
        self.fuel_name.textChanged.connect(lambda: self._activateSaveChangesButton())
        self.fuel_amount.textChanged.connect(lambda: self._validadeAmountRange(self.fuel_amount))
        self.fuel_temperature.textChanged.connect(lambda: self._validadeNonNegative(self.fuel_temperature))
        self.fuel_energy.textChanged.connect(lambda: self._validateData(self.fuel_energy))
        self.fuel_chemical_formula.textChanged.connect(lambda: self._activateSaveChangesButton())
        self.oxidant_name.textChanged.connect(lambda: self._activateSaveChangesButton())
        self.oxidant_amount.textChanged.connect(lambda: self._validadeAmountRange(self.oxidant_amount))
        self.oxidant_temperature.textChanged.connect(lambda: self._validadeNonNegative(self.oxidant_temperature))
        self.oxidant_energy.textChanged.connect(lambda: self._validateData(self.oxidant_energy))
        self.oxidant_chemical_formula.textChanged.connect(lambda: self._activateSaveChangesButton())
        self.chamber_pressure.textChanged.connect(lambda: self._validadeNonNegative(self.chamber_pressure))
        self.pressure_ratio.textChanged.connect(lambda: self._validadeNonNegative(self.pressure_ratio))
        self.misture_ratio.textChanged.connect(lambda: self._validadeNonNegative(self.misture_ratio))
        self.freezing_point.currentIndexChanged.connect(lambda: self._activateSaveChangesButton())

    def _activateSaveChangesButton(self):
        self.save_changes_btn.setEnabled(True)

    def _validadeAmountRange(self, field):
        try:
            field_value = float(field.text())
            if field_value < 0 or field_value > 1:
                field.setProperty('error', True)
            else:
                field.setProperty('error', False)
        except Exception:
            if field.text() == '':
                field.setProperty('error', False)
            else:
                field.setProperty('error', True)
        field.setStyle(field.style())
        self._activateSaveChangesButton()

    def _validadeNonNegative(self, field):
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
        self._activateSaveChangesButton()

    def _validateData(self, field):
        try:
            _ = float(field.text())
            field.setProperty('error', False)
        except Exception:
            if field.text() == '':
                field.setProperty('error', False)
            else:
                field.setProperty('error', True)
        field.setStyle(field.style())
        self._activateSaveChangesButton()

    def _setupCheckboxSelectionConnection(self):
        self._button_group.buttonClicked.connect(lambda: self._checkboxSelectionChanged())

    def _checkboxSelectionChanged(self):
        if self.frozen_checkbox.isChecked():
            self.freezing_point.setEnabled(True)
        else:
            self.freezing_point.setEnabled(False)
        self._activateSaveChangesButton()
