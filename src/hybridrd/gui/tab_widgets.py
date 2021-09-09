from PyQt5 import QtCore, QtWidgets
from hybridrd.gui.tabs import InputFileTab, PropellantAnalysisTab, BurnSimulationTab, BurnSimulationResultsTab


class AppTabWidget(QtWidgets.QTabWidget):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.input_file_tab = InputFileTab(self)
        self.propellant_analysis_tab = PropellantAnalysisTab(self)
        self.burn_simulation_tab = BurnSimulationTab(self)
        self.burn_results_tab = BurnSimulationResultsTab()
        self.addTab(self.input_file_tab, 'CEA Input File')
        self.addTab(self.propellant_analysis_tab, 'Propellant Analysis')
        self.addTab(self.burn_simulation_tab, 'Burn Simulation')
        self.propellant_analysis_tab.setEnabled(False)
        self.burn_simulation_tab.setEnabled(False)
        self._setupConnections()

    def _setupConnections(self):
        self.input_file_tab.chamber_pressure.textChanged.connect(lambda: self._copyChamberPressureFromInputTabToBurnTab())
        self.propellant_analysis_tab.cf_correction.valueChanged.connect(lambda: self._copyCfCorrectionToBurnSimulationTab())

    def _copyChamberPressureFromInputTabToBurnTab(self):
        chamberPressure = self.input_file_tab.chamber_pressure.text()
        self.burn_simulation_tab.chamber_pressure.setText(chamberPressure)

    def _copyCfCorrectionToBurnSimulationTab(self):
        cf_correction = self.propellant_analysis_tab.cf_correction.value()
        self.burn_simulation_tab.cf_correction.setText(str(cf_correction))
