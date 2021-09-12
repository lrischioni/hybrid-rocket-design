import os
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from hybridrd.analysis import CEA
from hybridrd.utils import PlotDictEnUs, PlotDictPtBr, BurnSimulationPlotDictYAxis
import hybridrd.gui as gui
import hybridrd.gui.resources_rc
from hybridrd.gui import launchwindows


MESSAGE_TIMEOUT = 2000
WORK_DIR = os.getcwd()


class MainWindow(QtWidgets.QMainWindow):
    """
    This class represents the GUI main window, responsible for all the
    interface operation.
    """
    def __init__(self):
        """
        Constructor method.
        """
        super().__init__()
        self.theme = 'dark theme'
        self.theme = 'light theme'
        self.cea = CEA()
        self._setupUi()
        self._loadStyleSheet()

    def _setupUi(self):
        name = QtWidgets.qApp.applicationName()
        version = QtWidgets.qApp.applicationVersion()
        self.setWindowTitle(name + ' ' + str(version))
        self.setWindowIcon(QtGui.QIcon(":/icons/logo.png"))
        self.width = 840
        self.height = 630
        self.setFixedSize(self.width, self.height)
        self._setupLocale()
        self._setupTabWidget()
        self._setupStatusBar()
        self._setupMenuBar()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def _setupLocale(self):
        self._locale_en_us = QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates)
        self._locale_pt_br = QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil)

    def _setupTabWidget(self):
        self.tabWidget = gui.AppTabWidget(self)
        self.setCentralWidget(self.tabWidget)
        self._setupClickConnections()

    def _setupClickConnections(self):
        self.tabWidget.input_file_tab.import_cea_file_btn.clicked.connect(lambda: self._importCeaInputFile())
        self.tabWidget.input_file_tab.save_changes_btn.clicked.connect(lambda: self._saveCeaInputFile())
        self.tabWidget.input_file_tab.run_cea_btn.clicked.connect(lambda: self._runCea())
        self.tabWidget.propellant_analysis_tab.perform_analysis_btn.clicked.connect(lambda: self._performAnalysis())
        self.tabWidget.propellant_analysis_tab.generate_plot_btn.clicked.connect(lambda: self._generatePropellantAnalysisResultsPlot())
        self.tabWidget.burn_simulation_tab.select_starting_point_btn.clicked.connect(lambda: self._selectInitialPoint())
        self.tabWidget.burn_simulation_tab.insert_regression_parameters_btn.clicked.connect(lambda: self._insertRegressionParameters())
        self.tabWidget.burn_simulation_tab.simulate_burn_btn.clicked.connect(lambda: self._simulateBurn())
        self.tabWidget.burn_results_tab.results_tab.export_results_btn.clicked.connect(lambda: self._exportBurnSimulationResults())
        self.tabWidget.burn_results_tab.plots_tab.generate_plot_btn.clicked.connect(lambda: self._generateBurnSimulationPlots())

    def _importCeaInputFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        inputfile_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file:', WORK_DIR, options=options)
        if inputfile_path != '':
            if self._inputFileIsValid(inputfile_path):
                self.cea.import_cea_inputfile(inputfile_path)
                self.statusbar.showMessage('CEA input file imported.', MESSAGE_TIMEOUT)
                self._loadInputFileIntoUi()
                launchwindows.launchLoadInputFileConfirmationScreen(self)
                self.tabWidget.propellant_analysis_tab.setEnabled(True)
                self.tabWidget.input_file_tab.run_cea_btn.setEnabled(True)
                self.tabWidget.input_file_tab.save_changes_btn.setEnabled(False)
            else:
                launchwindows.launchInputFileNotValidWarning(self)

    def _inputFileIsValid(self, inputfile_path):
        return inputfile_path.split('.')[-1] == 'inp'

    def _loadInputFileIntoUi(self):
        self._loadPropellantInformationIntoUi()
        self._loadChamberInformationIntoUi()

    def _loadPropellantInformationIntoUi(self):
        self.tabWidget.input_file_tab.fuel_name.setText(self.cea.inputfile.fuel.name)
        self.tabWidget.input_file_tab.fuel_amount.setText(str(self.cea.inputfile.fuel.amount))
        self.tabWidget.input_file_tab.fuel_temperature.setText(str(self.cea.inputfile.fuel.temperature))
        if hasattr(self.cea.inputfile.fuel, 'energy_h'):
            self.tabWidget.input_file_tab.fuel_energy.setText(str(self.cea.inputfile.fuel.energy_h))
            self.tabWidget.input_file_tab.fuel_chemical_formula.setText(self.cea.inputfile.fuel.formula)
        self.tabWidget.input_file_tab.oxidant_name.setText(self.cea.inputfile.oxidant.name)
        self.tabWidget.input_file_tab.oxidant_amount.setText(str(self.cea.inputfile.oxidant.amount))
        self.tabWidget.input_file_tab.oxidant_temperature.setText(str(self.cea.inputfile.oxidant.temperature))
        if hasattr(self.cea.inputfile.oxidant, 'energy_h'):
            self.tabWidget.input_file_tab.oxidant_energy.setText(str(self.cea.inputfile.oxidant.energy_h))
            self.tabWidget.input_file_tab.oxidant_chemical_formula.setText(self.cea.inputfile.oxidant.formula)

    def _loadChamberInformationIntoUi(self):
        self.tabWidget.input_file_tab.chamber_pressure.setText(str(self.cea.inputfile.chamber_pressure))
        self.tabWidget.input_file_tab.pressure_ratio.setText(str(self.cea.inputfile.chamber_atmospheric_pressure_ratio))
        self.tabWidget.input_file_tab.misture_ratio.setText(str(self.cea.inputfile.oxid_fuel_ratio))
        method = self.cea.inputfile.method
        if method == 'equilibrium':
            self.tabWidget.input_file_tab.equilibrium_checkbox.setChecked(True)
            self.tabWidget.input_file_tab.freezing_point.setEnabled(False)
        else:
            self.tabWidget.input_file_tab.frozen_checkbox.setChecked(True)
            self.tabWidget.input_file_tab.freezing_point.setCurrentIndex(self.cea.inputfile.freezing_point - 1)
            self.tabWidget.input_file_tab.freezing_point.setEnabled(True)

    def _saveCeaInputFile(self):
        if hasattr(self.cea, 'inputfile'):
            self.tabWidget.input_file_tab.save_changes_btn.setEnabled(False)
            self.tabWidget.burn_simulation_tab.setEnabled(False)
            self.tabWidget.burn_results_tab.setEnabled(False)
            self.statusbar.showMessage('Saving CEA Input Data...')
            try:
                self._setPropellantInformationInCeaInputFile()
                self._setChamberInformationInCeaInputFile()
                self.cea.inputfile.save()
                self.statusbar.showMessage('Saving complete.', MESSAGE_TIMEOUT)
            except Exception:
                self.statusbar.showMessage('Saving changes failed.', MESSAGE_TIMEOUT)
                launchwindows.launchInputInconsistentDataWarning(self)
        else:
            launchwindows.launchInputFileNotImportedWarning(self)

    def _setPropellantInformationInCeaInputFile(self):
        fuel_name = self.tabWidget.input_file_tab.fuel_name.text()
        fuel_amount = float(self.tabWidget.input_file_tab.fuel_amount.text())
        fuel_temperature = float(self.tabWidget.input_file_tab.fuel_temperature.text())
        if self.tabWidget.input_file_tab.fuel_energy.text() != '':
            fuel_energy = float(self.tabWidget.input_file_tab.fuel_energy.text())
            fuel_formula = self.tabWidget.input_file_tab.fuel_chemical_formula.text()
            self.cea.inputfile.set_fuel(fuel_name, fuel_amount, fuel_temperature, fuel_energy, fuel_formula)
        else:
            self.cea.inputfile.set_fuel(fuel_name, fuel_amount, fuel_temperature)
        oxidant_name = self.tabWidget.input_file_tab.oxidant_name.text()
        oxidant_amount = float(self.tabWidget.input_file_tab.oxidant_amount.text())
        oxidant_temperature = float(self.tabWidget.input_file_tab.oxidant_temperature.text())
        if self.tabWidget.input_file_tab.oxidant_energy.text() != '':
            oxidant_energy = float(self.tabWidget.input_file_tab.oxidant_energy.text())
            oxidant_formula = self.tabWidget.input_file_tab.oxidant_chemical_formula.text()
            self.cea.inputfile.set_oxidant(oxidant_name, oxidant_amount, oxidant_temperature, oxidant_energy, oxidant_formula)
        else:
            self.cea.inputfile.set_oxidant(oxidant_name, oxidant_amount, oxidant_temperature)
        oxid_fuel_ratio = float(self.tabWidget.input_file_tab.misture_ratio.text())
        self.cea.inputfile.set_oxid_fuel_ratio(oxid_fuel_ratio)

    def _setChamberInformationInCeaInputFile(self):
        chamber_pressure = float(self.tabWidget.input_file_tab.chamber_pressure.text())
        pressure_ratio = float(self.tabWidget.input_file_tab.pressure_ratio.text())
        self.cea.inputfile.set_chamber_pressure(chamber_pressure)
        self.cea.inputfile.set_pressure_ratio(pressure_ratio)
        if self.tabWidget.input_file_tab.equilibrium_checkbox.isChecked():
            method = 'equilibrium'
            self.cea.inputfile.set_method(method)
        else:
            method = 'frozen'
            freezing_point = self.tabWidget.input_file_tab.freezing_point.currentIndex() + 1
            self.cea.inputfile.set_method(method, freezing_point)

    def _runCea(self):
        self.tabWidget.input_file_tab.run_cea_btn.setEnabled(False)
        if self.cea.is_inputfile_loaded():
            self.statusbar.showMessage('Running CEA...')
            self.cea.run_cea()
            self.statusbar.showMessage('CEA ran successfully.', MESSAGE_TIMEOUT)
            self._displayOutput()
        else:
            launchwindows.launchInputFileNotImportedWarning(self)
        self.tabWidget.input_file_tab.run_cea_btn.setEnabled(True)

    def _displayOutput(self):
        gui.DisplayOutputFileWindow(self.cea.output_path, self)

    def _performAnalysis(self):
        self.tabWidget.propellant_analysis_tab.perform_analysis_btn.setEnabled(False)
        self._resetBurnSimulationStartingPoint()
        if self.cea.is_inputfile_loaded():
            starting_of, final_of = self._getOFRange()
            self.cea.set_cf_nozzle_correction(self._getCfNozzleCorrection())
            if self._inputRangeIsValid(starting_of, final_of):
                self.statusbar.setupProgressBar()
                self.statusbar.showMessage('Performing analysis...')
                self.cea.perform_propellant_analysis(starting_of, final_of, self.statusbar.progressBar)
                self._restoreCeaInputFileOriginalInformation()
                self.statusbar.showMessage('Analysis completed successfully.', MESSAGE_TIMEOUT)
                self.tabWidget.propellant_analysis_tab.analysis_results_plot_widget.clear()
                launchwindows.launchStudyPerformedSuccessfullyWarning(self)
                self.statusbar.removeProgressBar()
                self.tabWidget.propellant_analysis_tab.generate_plot_btn.setEnabled(True)
                self.tabWidget.burn_simulation_tab.setEnabled(True)
            else:
                launchwindows.launchStartingValueBiggerThanFinalValueWarning(self)
        else:
            launchwindows.launchInputFileNotImportedWarning(self)
        self.tabWidget.propellant_analysis_tab.perform_analysis_btn.setEnabled(True)

    def _resetBurnSimulationStartingPoint(self):
        self.tabWidget.burn_simulation_tab.initial_of.setText('')
        self.tabWidget.burn_simulation_tab.initial_cstar.setText('')
        self.tabWidget.burn_simulation_tab.initial_cf.setText('')
        self.tabWidget.burn_simulation_tab.aeat_ratio.setText('')

    def _getOFRange(self):
        starting_of = self.tabWidget.propellant_analysis_tab.starting_of.value()
        final_of = self.tabWidget.propellant_analysis_tab.final_of.value()
        return starting_of, final_of

    def _getCfNozzleCorrection(self):
        cf_correction = self.tabWidget.propellant_analysis_tab.cf_correction.value()
        return cf_correction

    def _inputRangeIsValid(self, starting_of, final_of):
        return starting_of < final_of

    def _restoreCeaInputFileOriginalInformation(self):
        try:
            self._setChamberInformationInCeaInputFile()
            self._setPropellantInformationInCeaInputFile()
            self.cea.inputfile.save()
        except Exception:
            pass

    def _generatePropellantAnalysisResultsPlot(self):
        x_axis = self.tabWidget.propellant_analysis_tab.variable_x_axis.currentText()
        y_axis = self.tabWidget.propellant_analysis_tab.variable_y_axis.currentText()
        locale = self.tabWidget.propellant_analysis_tab.plot_locale.currentText()
        x_data = self.cea.propellant_analysis_results[x_axis]
        y_data = self.cea.propellant_analysis_results[y_axis]
        if locale == 'en_US':
            plot_dict = PlotDictEnUs()
            self.tabWidget.propellant_analysis_tab.setLocale(self._locale_en_us)
        else:
            plot_dict = PlotDictPtBr()
            self.tabWidget.propellant_analysis_tab.setLocale(self._locale_pt_br)
        self.tabWidget.propellant_analysis_tab.analysis_results_plot_widget.clear()
        plot_item = self.tabWidget.propellant_analysis_tab.analysis_results_plot_widget.addPlot()
        if self.theme == 'dark theme':
            plot_item.plot(x_data, y_data, pen=pg.mkPen(color=(101, 82, 68), width=4.))
            styles = {'font-size': '15px'}
            plot_item.setTitle(y_axis + ' vs ' + x_axis, color='w', size='16pt')
            plot_item.setLabel('left', plot_dict.get(y_axis), **styles)
            plot_item.setLabel('bottom', plot_dict.get(x_axis), **styles)
            plot_item.getAxis('left').setTextPen('w')
            plot_item.getAxis('bottom').setTextPen('w')
        else:
            plot_item.plot(x_data, y_data, pen=pg.mkPen(color=(0, 0, 255)))
            styles = {'font-size': '15px'}
            plot_item.setTitle(y_axis + ' vs ' + x_axis, color='k', size='16pt')
            plot_item.setLabel('left', plot_dict.get(y_axis), **styles)
            plot_item.setLabel('bottom', plot_dict.get(x_axis), **styles)
            plot_item.getAxis('left').setTextPen('k')
            plot_item.getAxis('bottom').setTextPen('k')

    def _selectInitialPoint(self):
        self.tabWidget.burn_simulation_tab.select_starting_point_btn.setEnabled(False)
        if self._containsPropellantAnalysisResults():
            selected_point = gui.SelectStartingPoint(self)
            if hasattr(selected_point, 'initial_of_value'):
                self.tabWidget.burn_simulation_tab.initial_of.setText(selected_point.initial_of_value)
                self.tabWidget.burn_simulation_tab.initial_cf.setText(selected_point.initial_cf_value)
                self.tabWidget.burn_simulation_tab.aeat_ratio.setText(selected_point.aeat_ratio_value)
                self.tabWidget.burn_simulation_tab.initial_cstar.setText(selected_point.initial_cstar_value)
                self.tabWidget.burn_simulation_tab.simulate_burn_btn.setEnabled(True)
        else:
            launchwindows.launchStudyNotPerformedWarning(self)
        self.tabWidget.burn_simulation_tab.select_starting_point_btn.setEnabled(True)

    def _containsPropellantAnalysisResults(self):
        return hasattr(self.cea, 'propellant_analysis_results')

    def _insertRegressionParameters(self):
        self.tabWidget.burn_simulation_tab.insert_regression_parameters_btn.setEnabled(False)
        gui.InsertRegressionParameters(self)
        self.tabWidget.burn_simulation_tab.insert_regression_parameters_btn.setEnabled(True)

    def _simulateBurn(self):
        self.tabWidget.burn_simulation_tab.simulate_burn_btn.setEnabled(False)
        self._clearPreviousPlots()
        self.statusbar.setupProgressBar()
        self.statusbar.showMessage('Simulating burn...')
        self._simulateBurnBasedOnMethodSelected()
        self.statusbar.removeProgressBar()
        self.tabWidget.burn_simulation_tab.simulate_burn_btn.setEnabled(True)

    def _clearPreviousPlots(self):
        try:
            self.tabWidget.burn_results_tab.plots_tab.plot_widget.clear()
            self.tabWidget.burn_results_tab.setCurrentIndex(0)
        except Exception:
            pass

    def _simulateBurnBasedOnMethodSelected(self):
        try:
            simulation_method = str(self.tabWidget.burn_simulation_tab.method.currentText())
            self._storeInitialValuesBasedOnMethodSelected(simulation_method)
            try:
                self.cea.perform_burn_simulation(simulation_method, self.statusbar.progressBar)
                self.tabWidget.addTab(self.tabWidget.burn_results_tab, 'Burn Simulation Results')
                self._passBurnSimulationResultsToResultsTab()
                self._restoreCeaInputFileOriginalInformation()
                self.statusbar.showMessage('Burn simulation completed successfully.', MESSAGE_TIMEOUT)
                launchwindows.launchBurnSimulatedSuccessfullyConfirmationScreen(self)
                self.tabWidget.burn_results_tab.setEnabled(True)
            except Exception as diameter_values:
                self._restoreCeaInputFileOriginalInformation()
                nozzle_throat_diameter, grain_inner_diameter = diameter_values.args
                self.statusbar.showMessage('Burn simulation failed.', MESSAGE_TIMEOUT)
                launchwindows.launchGrainInnerDiameterInvalidWarning(nozzle_throat_diameter, grain_inner_diameter, self)
        except Exception:
            self.statusbar.showMessage('Burn simulation failed.', MESSAGE_TIMEOUT)
            launchwindows.launchBurnSimulationInconsistentDataWarning(self)

    def _storeInitialValuesBasedOnMethodSelected(self, simulation_method):
        initial_of = float(self.tabWidget.burn_simulation_tab.initial_of.text())
        fuel_density = float(self.tabWidget.burn_simulation_tab.fuel_density.text())
        a = float(self.tabWidget.burn_simulation_tab.regression_parameter_a_si)
        n = float(self.tabWidget.burn_simulation_tab.regression_parameter_n.text())
        initial_thrust = float(self.tabWidget.burn_simulation_tab.initial_thrust.text())
        cf_correction = float(self.tabWidget.burn_simulation_tab.cf_correction.text())
        burn_duration = float(self.tabWidget.burn_simulation_tab.burn_duration.text())
        if simulation_method == 'Inner diameter known':
            inner_diameter = float(self.tabWidget.burn_simulation_tab.grain_inner_diameter.text())
            self.cea.set_grain_inner_diameter(inner_diameter)
        elif simulation_method == 'Outer diameter known':
            outer_diameter = float(self.tabWidget.burn_simulation_tab.grain_outer_diameter.text())
            self.cea.set_grain_outer_diameter(outer_diameter)
        elif simulation_method == 'Length known':
            grain_length = float(self.tabWidget.burn_simulation_tab.grain_length.text())
            self.cea.set_grain_length(grain_length)
        self.cea.set_start_point(initial_of)
        self.cea.set_initial_thrust(initial_thrust)
        self.cea.set_regression_rate_parameters(a, n)
        self.cea.set_grain_density(fuel_density)
        self.cea.set_cf_nozzle_correction(cf_correction)
        self.cea.set_burn_time(burn_duration)

    def _passBurnSimulationResultsToResultsTab(self):
        self._passStartingBurnValuesToResultsTab()
        self._passEndingBurnValuesToResultsTab()
        self._passMotorGeometryValuesToResultsTab()

    def _passStartingBurnValuesToResultsTab(self):
        mass_flow_rate = str(round(self.cea.burn_simulation_initial_results['Mass_Flow_Rate'], 2)) + ' g/s'
        fuel_mass_flow_rate = str(round(self.cea.burn_simulation_initial_results['Fuel_Mass_Flow_Rate'], 2)) + ' g/s'
        oxidant_mass_flow_rate = str(round(self.cea.burn_simulation_initial_results['Oxidant_Mass_Flow_Rate'], 2)) + ' g/s'
        misture_ratio = str(round(self.cea.burn_simulation_initial_results['o/f'], 2))
        regression_rate = str(round(self.cea.burn_simulation_initial_results['Regression_Rate'], 2)) + ' mm/s'
        grain_inner_diameter = str(round(self.cea.burn_simulation_initial_results['Grain_Inner_Diameter'], 2)) + ' mm'
        gox = str(round(self.cea.burn_simulation_initial_results['Gox'], 2)) + ' g/(cm².s)'
        self.tabWidget.burn_results_tab.results_tab.mass_flow_rate.setText(mass_flow_rate)
        self.tabWidget.burn_results_tab.results_tab.fuel_mass_flow_rate.setText(fuel_mass_flow_rate)
        self.tabWidget.burn_results_tab.results_tab.oxid_mass_flow_rate.setText(oxidant_mass_flow_rate)
        self.tabWidget.burn_results_tab.results_tab.misture_ratio.setText(misture_ratio)
        self.tabWidget.burn_results_tab.results_tab.start_regression_rate.setText(regression_rate)
        self.tabWidget.burn_results_tab.results_tab.start_inner_diameter.setText(grain_inner_diameter)
        self.tabWidget.burn_results_tab.results_tab.start_gox.setText(gox)

    def _passEndingBurnValuesToResultsTab(self):
        grain_inner_diameter = str(round(self.cea.burn_simulation_results['Grain_Inner_Diameter'].values[-1], 2)) + ' mm'
        regression_rate = str(round(self.cea.burn_simulation_results['Regression_Rate'].values[-1], 2)) + ' mm/s'
        gox = str(round(self.cea.burn_simulation_results['Gox'].values[-1], 2)) + ' g/(cm².s)'
        self.tabWidget.burn_results_tab.results_tab.end_inner_diameter.setText(grain_inner_diameter)
        self.tabWidget.burn_results_tab.results_tab.end_regression_rate.setText(regression_rate)
        self.tabWidget.burn_results_tab.results_tab.end_gox.setText(gox)

    def _passMotorGeometryValuesToResultsTab(self):
        nozzle_throat_area = str(round(self.cea.burn_simulation_initial_results['Nozzle_Throat_Area'], 2)) + ' mm²'
        nozzle_exit_area = str(round(self.cea.burn_simulation_initial_results['Nozzle_Exit_Area'], 2)) + ' mm²'
        nozzle_throat_diameter = str(round(self.cea.burn_simulation_initial_results['Nozzle_Throat_Diameter'], 2)) + ' mm'
        nozzle_exit_diameter = str(round(self.cea.burn_simulation_initial_results['Nozzle_Exit_Diameter'], 2)) + ' mm'
        grain_length = str(round(self.cea.burn_simulation_initial_results['Grain_Length'], 2)) + ' cm'
        self.tabWidget.burn_results_tab.results_tab.nozzle_throat_area.setText(nozzle_throat_area)
        self.tabWidget.burn_results_tab.results_tab.nozzle_exit_area.setText(nozzle_exit_area)
        self.tabWidget.burn_results_tab.results_tab.nozzle_throat_diameter.setText(nozzle_throat_diameter)
        self.tabWidget.burn_results_tab.results_tab.nozzle_exit_diameter.setText(nozzle_exit_diameter)
        self.tabWidget.burn_results_tab.results_tab.grain_length.setText(grain_length)

    def _exportBurnSimulationResults(self):
        self.tabWidget.burn_results_tab.results_tab.export_results_btn.setEnabled(False)
        save_file_dialog = QtWidgets.QFileDialog(self)
        save_file_dialog.setFilter(save_file_dialog.filter() | QtCore.QDir.Hidden)
        save_file_dialog.setDefaultSuffix('csv')
        save_file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        save_file_dialog.setNameFilters(['Comma-separated file (*.csv)'])
        save_file_dialog.DontUseNativeDialog
        save_file_dialog.setDirectory(WORK_DIR)
        if save_file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            savepath = save_file_dialog.selectedFiles()[0]
            self.cea.export_burn_simulation_results(savepath)
            launchwindows.launchExportResultsConfirmationScreen(self)
        self.tabWidget.burn_results_tab.results_tab.export_results_btn.setEnabled(True)

    def _generateBurnSimulationPlots(self):
        self.tabWidget.burn_results_tab.plots_tab.plot_widget.clear()
        y_axis = self.tabWidget.burn_results_tab.plots_tab.variable_y_axis.currentText()
        locale = self.tabWidget.burn_results_tab.plots_tab.plot_locale.currentText()
        x_data = self.cea.burn_simulation_results['Time'].values
        y_data = self.cea.burn_simulation_results[BurnSimulationPlotDictYAxis().get(y_axis)].values
        if locale == 'en_US':
            plot_dict = PlotDictEnUs()
            self.tabWidget.burn_results_tab.plots_tab.setLocale(self._locale_en_us)
        else:
            plot_dict = PlotDictPtBr()
            self.tabWidget.burn_results_tab.plots_tab.setLocale(self._locale_pt_br)
        plot_item = self.tabWidget.burn_results_tab.plots_tab.plot_widget.addPlot()
        if self.theme == 'dark theme':
            plot_item.plot(x_data, y_data, pen=pg.mkPen(color=(101, 82, 68), width=4.))
            styles = {'font-size': '15px'}
            plot_item.setTitle(y_axis + ' vs Time', color='w', size='16pt')
            plot_item.setLabel('left', plot_dict.get(y_axis), **styles)
            plot_item.setLabel('bottom', plot_dict.get('Time'), **styles)
            plot_item.getAxis('left').setTextPen('w')
            plot_item.getAxis('bottom').setTextPen('w')
        else:
            plot_item.plot(x_data, y_data, pen=pg.mkPen(color=(0, 0, 255)))
            styles = {'font-size': '15px'}
            plot_item.setTitle(y_axis + ' vs Time', color='k', size='16pt')
            plot_item.setLabel('left', plot_dict.get(y_axis), **styles)
            plot_item.setLabel('bottom', plot_dict.get('Time'), **styles)
            plot_item.getAxis('left').setTextPen('k')
            plot_item.getAxis('bottom').setTextPen('k')

    def _setupStatusBar(self):
        self.statusbar = hybridrd.gui.StatusBar(self)

    def _setupMenuBar(self):
        self.menubar = hybridrd.gui.MenuBar(self)
        self._connectMenuBarActions()

    def _connectMenuBarActions(self):
        self.menubar.settings.appearance.dark_theme.triggered.connect(lambda: self._loadStyleSheet('dark theme'))
        self.menubar.settings.appearance.light_theme.triggered.connect(lambda: self._loadStyleSheet('light theme'))

    def _loadStyleSheet(self, theme='dark theme'):
        if theme == 'dark theme':
            theme_style = QtCore.QFile(":/stylesheets/darktheme.qss")
            self.theme = 'dark theme'
        else:
            theme_style = QtCore.QFile(":/stylesheets/lighttheme.qss")
            self.theme = 'light theme'
        if theme_style.open(QtCore.QIODevice.ReadOnly):
            self.setStyleSheet(theme_style.readAll().data().decode('utf8'))
        try:
            self._adjustPreviouslyPlots()
        except Exception:
            pass

    def _adjustPreviouslyPlots(self):
        self.tabWidget.propellant_analysis_tab.analysis_results_plot_widget.clear()
        self.tabWidget.propellant_analysis_tab.analysis_results_plot_widget.setBackground(None)
        self._generatePropellantAnalysisResultsPlot()
        self.tabWidget.burn_results_tab.plots_tab.plot_widget.clear()
        self.tabWidget.burn_results_tab.plots_tab.plot_widget.setBackground(None)
        self._generateBurnSimulationPlots()
