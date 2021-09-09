import hybridrd
import os
import platform
import subprocess
from hybridrd.inputfile import CEAInputFile


class CEA(object):
    """
    """
    def __init__(self):
        folderpath = os.path.dirname(os.path.abspath(__file__))
        path_to_cea = os.path.abspath(os.path.join(folderpath, os.pardir, 'CEA'))
        self._set_path_to_cea(path_to_cea)

    def _set_path_to_cea(self, path_to_cea):
        self._path_to_cea = path_to_cea

    def import_cea_inputfile(self, inputfile_path):
        self.inputfile = CEAInputFile(inputfile_path)

    def is_inputfile_loaded(self):
        return hasattr(self, 'inputfile')

    def set_fuel(self, fuel_name, fuel_temperature):
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_fuel(fuel_name, fuel_temperature)

    def set_oxidant(self, oxidant_name, oxidant_temperature):
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_fuel(oxidant_name, oxidant_temperature)

    def set_chamber_pressure(self, chamber_pressure):
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_chamber_pressure(chamber_pressure)

    def set_pressure_ratio(self, pressure_ratio):
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_pressure_ratio(pressure_ratio)

    def set_oxid_fuel_ratio(self, oxid_fuel_ratio):
        if not hasattr(self, 'inputfile'):
            self.inputfile = CEAInputFile()
        self.inputfile.set_oxid_fuel_ratio(oxid_fuel_ratio)

    def run_cea(self):
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
        propellant_analysis = hybridrd.analysis.CEAPropellantAnalysis(self.inputfile)
        propellant_analysis.perform_propellant_analysis(oxid_fuel_ratio_start, oxid_fuel_ratio_end, self._cf_correction, progress_bar)
        self.propellant_analysis_results = propellant_analysis.generate_results()

    def set_start_point(self, starting_of):
        self._starting_of_point = starting_of

    def set_initial_thrust(self, initial_thrust):
        self._initial_thrust = initial_thrust

    def set_regression_rate_parameters(self, a, n):
        self._a = a
        self._n = n

    def set_grain_density(self, rho):
        self._rho = rho

    def set_cf_nozzle_correction(self, cf_correction):
        self._cf_correction = cf_correction

    def set_grain_inner_diameter(self, inner_diameter):
        self._grain_inner_diameter = inner_diameter

    def set_grain_length(self, grain_length):
        self._grain_length = grain_length

    def set_grain_outer_diameter(self, outer_diameter):
        self._grain_outer_diameter = outer_diameter

    def set_burn_time(self, burn_time):
        self._burn_time = burn_time

    def perform_burn_simulation(self, method, progress_bar):
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
        self.burn_simulation_results.to_csv(savepath, index=False)
