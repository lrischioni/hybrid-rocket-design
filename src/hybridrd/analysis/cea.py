import hybridrd
import os
import platform
import subprocess
from hybridrd.inputfile import CEAInputFile


class CEA(object):
    """
    This class concentrates all the operations from :class: `CEAInputFile`,
    :class: `CEAPropellantAnalysis` and :class: `CEABurnSimulation`. It is
    the main interface used by the GUI to perform all simulations and to
    obtain the results.
    """
    def __init__(self):
        """
        Constructor method
        """
        folderpath = os.path.dirname(os.path.abspath(__file__))
        path_to_cea = os.path.abspath(os.path.join(folderpath, os.pardir, 'CEA'))
        self._set_path_to_cea(path_to_cea)

    def _set_path_to_cea(self, path_to_cea):
        self._path_to_cea = path_to_cea

    def import_cea_inputfile(self, inputfile_path):
        """
        Import the CEA input file using the :class: `CEAInputFile`.

        Args:
            inputfile_path (str): Path to the input file
        """
        self.inputfile = CEAInputFile(inputfile_path)

    def is_inputfile_loaded(self):
        """
        Return if the input file is imported

        Returns:
            bool: Input file is imported
        """
        return hasattr(self, 'inputfile')

    def set_fuel(self, fuel_name, fuel_amount, fuel_temperature, energy_h=None, formula=None):
        """
        Set the fuel on the :class: `CEAInputFIle`.

        Args:
            fuel_name (str): Name of the propellant
            fuel_amount (float): Amount that this propellant represents overall considering
                all fuels or all oxidants
            fuel_temperature (float): Temperature of the propellant in Kelvin
            energy_h (float, optional): Enthalpy energy of the propellant. This must
                be provided only if the propellant is not on the CEA database. Defaults to None.
            formula (str, optional): Chemical formula of the propellant. This must be provided
                only if the propellant is not on the CEA database. Defaults to None.
        """
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_fuel(fuel_name, fuel_amount, fuel_temperature, energy_h=None, formula=None)

    def set_oxidant(self, oxidant_name, oxidant_amount, oxidant_temperature, energy_h=None, formula=None):
        """
        Set the oxidant on the :class: `CEAInputFIle`.

        Args:
            oxidant_name (str): Name of the propellant
            oxidant_amount (float): Amount that this propellant represents overall considering
                all fuels or all oxidants
            oxidant_temperature (float): Temperature of the propellant in Kelvin
            energy_h (float, optional): Enthalpy energy of the propellant. This must
                be provided only if the propellant is not on the CEA database. Defaults to None.
            formula (str, optional): Chemical formula of the propellant. This must be provided
                only if the propellant is not on the CEA database. Defaults to None.
        """
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_fuel(oxidant_name, oxidant_amount, oxidant_temperature, energy_h=None, formula=None)

    def set_chamber_pressure(self, chamber_pressure):
        """
        Set the chamber pressure on the :class: `CEAInputFile`.

        Args:
            chamber_pressure (float): Chamber pressure in bar
        """
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_chamber_pressure(chamber_pressure)

    def set_pressure_ratio(self, pressure_ratio):
        """
        Set the pressure ratio between the chamber and the atmosphere on the
        :class: `CEAInputFile`.

        Args:
            pressure_ratio (float): Pressure ratio
        """
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_pressure_ratio(pressure_ratio)

    def set_oxid_fuel_ratio(self, oxid_fuel_ratio):
        """
        Set the misture ratio between oxidant and fuel on the :class: `CEAInputFile`.

        Args:
            oxid_fuel_ratio (float): Misture ratio
        """
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_oxid_fuel_ratio(oxid_fuel_ratio)

    def run_cea(self):
        """
        Run the CEA application.
        """
        self.inputfile.save()
        PROGRAM_NAME = 'FCEA2.exe'
        process_path = os.path.join(self._path_to_cea, PROGRAM_NAME)
        os.chdir(self._path_to_cea)
        self._run_process(process_path)

    def _run_process(self, process_path):
        filename_without_extension = self._get_filename_without_extension()
        if platform.system() == 'Windows':
            command = process_path
        elif platform.system() == 'Linux':
            command = 'wine ' + process_path
        proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
        proc.communicate((filename_without_extension + '\n').encode())
        self.output_path = filename_without_extension + '.out'

    def _get_filename_without_extension(self):
        return self.inputfile.filepath.split('.')[-2]

    def perform_propellant_analysis(self, oxid_fuel_ratio_start, oxid_fuel_ratio_end, progress_bar):
        """
        Creates an instance of the :class: `CEAPropellantAnalysis` and executes CEA varying the values
        of misture ratio, storing the results on the attribute ``propellant_analysis_results``.

        Args:
            oxid_fuel_ratio_start (float): Initial misture ratio
            oxid_fuel_ratio_end (float): Final misture ratio
            progress_bar (QtWidgets.QProgressBar): Reference to the :class: `QtWidgets.QProgressBar`
        """
        propellant_analysis = hybridrd.analysis.CEAPropellantAnalysis(self.inputfile)
        propellant_analysis.perform_propellant_analysis(oxid_fuel_ratio_start, oxid_fuel_ratio_end, self._cf_correction, progress_bar)
        self.propellant_analysis_results = propellant_analysis.generate_results()

    def set_start_point(self, starting_of):
        """
        Set the misture ratio at the starting point on the burn simulation.

        Args:
            starting_of (float): Initial misture ratio
        """
        self._starting_of_point = starting_of

    def set_initial_thrust(self, initial_thrust):
        """
        Set the initial thrust at the starting point on the burn simulation.

        Args:
            initial_thrust (float): Initial thrust
        """
        self._initial_thrust = initial_thrust

    def set_regression_rate_parameters(self, a, n):
        """
        Set the parameters of the regression rate equation.

        Args:
            a (float): Regression rate coefficient
            n (float): Flux exponent
        """
        self._a = a
        self._n = n

    def set_grain_density(self, rho):
        """
        Set the grain density in g/cm³.

        Args:
            rho (float): Grain density
        """
        self._rho = rho

    def set_cf_nozzle_correction(self, cf_correction):
        """
        Set the nozzle correction for the Cf parameter.

        Args:
            cf_correction (float): Correction value
        """
        self._cf_correction = cf_correction

    def set_grain_inner_diameter(self, inner_diameter):
        """
        Set the initial grain inner diameter in mm.

        Args:
            inner_diameter (float): Grain inner diameter
        """
        self._grain_inner_diameter = inner_diameter

    def set_grain_length(self, grain_length):
        """
        Set the grain length in cm.

        Args:
            grain_length (float): Grain length
        """
        self._grain_length = grain_length

    def set_grain_outer_diameter(self, outer_diameter):
        """
        Set the grain outer diameter in mm.

        Args:
            outer_diameter (float): Grain outer diameter
        """
        self._grain_outer_diameter = outer_diameter

    def set_burn_time(self, burn_time):
        """
        Set the burn duration time in seconds.

        Args:
            burn_time (float): Burn duration time
        """
        self._burn_time = burn_time

    def perform_burn_simulation(self, method, progress_bar):
        """
        Creates an instance of the :class: `CEABurnSimulation` and perform an iterative process
        to simulate the burn, storing the results on the attribute ``burn_simulation_results``.

        Args:
            method (str): Chosen method to simulate the burn ('Inner diameter known',
                'Outer diameter known', 'Length known')
            progress_bar (QtWidgets.QProgressBar): Reference to the QtWidget from the GUi application
                to update the progress bar

        Raises:
            Exception: If Ac/At ratio is not satisfied
        """
        burn_simulation = hybridrd.analysis.CEABurnSimulation(self.inputfile, method)
        burn_simulation.set_initial_thrust(self._initial_thrust)
        burn_simulation.set_chamber_pressure(self.inputfile.chamber_pressure)
        burn_simulation.set_regression_rate_parameters(self._a, self._n)
        burn_simulation.set_grain_density(self._rho)
        burn_simulation.set_cf_nozzle_correction(self._cf_correction)
        burn_simulation.set_burn_time(self._burn_time)
        if method == 'Inner diameter known':
            burn_simulation.set_grain_inner_diameter(self._grain_inner_diameter)
        elif method == 'Outer diameter known':
            burn_simulation.set_grain_outer_diameter(self._grain_outer_diameter)
        elif method == 'Length known':
            burn_simulation.set_grain_length(self._grain_length)
        burn_simulation.set_initial_parameters(self._starting_of_point)
        if burn_simulation.is_ac_at_ratio_valid():
            burn_simulation.compute_values_over_time(progress_bar)
            self.burn_simulation_initial_results = burn_simulation.initial_results
            self.burn_simulation_results = burn_simulation.generate_results()
        else:
            nozzle_throat_diameter = burn_simulation.initial_results['Nozzle_Throat_Diameter']
            grain_inner_diameter = burn_simulation.initial_results['Grain_Inner_Diameter']
            raise Exception(nozzle_throat_diameter, grain_inner_diameter)

    def export_burn_simulation_results(self, savepath):
        """
        Exports the simulation results in the .csv format.

        Args:
            savepath (str): Savepath
        """
        self.burn_simulation_results.to_csv(savepath, index=False)
