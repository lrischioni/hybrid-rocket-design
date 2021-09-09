import math
import numpy as np
import os
import pandas as pd
import platform
import subprocess
import sys
from hybridrd.propellant import RegressionRateEquationParameters


class CEAResults(object):
    """
    """
    def __init__(self, output_file_path):
        self._read_output_file(output_file_path)

    def _read_output_file(self, output_file_path):
        try:
            with open(output_file_path, 'r') as output_file:
                for line in output_file.readlines():
                    self._get_line_information(line)
        except OSError as error:
            print('File {:s} failed'.format(error.filename))
            sys.exit()

    def _get_line_information(self, line):
        try:
            words = line.split()
            if 'o/f=' in words[1]:
                self.oxid_fuel_ratio = self._get_oxid_fuel_ratio_from_output(words[1])
            if words[0] == 'GAMMAs':
                self.gamma = float(words[1])
            if words[0] == 'Ae/At':
                self.ae_at_ratio = float(words[2])
            if words[0] == 'CSTAR,':
                self.cstar = float(words[2])
            if words[0] == 'CF':
                self.cf = float(words[2])
            if words[0] == 'Isp,':
                self.isp = float(words[3])
        except Exception:
            pass

    def _get_oxid_fuel_ratio_from_output(self, word):
        return float(word.replace('o/f=', '').replace(',', ''))


class CEAPropellantAnalysis(object):
    """
    """
    def __init__(self, cea_input_file):
        self._input_file = cea_input_file
        self._oxid_fuel_ratio = list()
        self._gamma = list()
        self._ae_at_ratio = list()
        self._cstar = list()
        self._cf = list()
        self._isp = list()
        folderpath = os.path.dirname(os.path.abspath(__file__))
        self._path_to_cea = os.path.abspath(os.path.join(folderpath, os.pardir, 'CEA'))
        self.LINSPACE_SIZE = 100

    def perform_propellant_analysis(self, oxid_fuel_ratio_start, oxid_fuel_ratio_end, cf_nozzle_correction, progress_bar):
        self._cf_correction = cf_nozzle_correction
        for idx, of_ratio in enumerate(np.linspace(oxid_fuel_ratio_start, oxid_fuel_ratio_end, self.LINSPACE_SIZE)):
            self._input_file.set_oxid_fuel_ratio(of_ratio)
            self._run_cea()
            self._append_results(self._get_cea_results())
            progress_bar.setValue((idx + 1) * 100 / self.LINSPACE_SIZE)

    def _run_cea(self):
        self._input_file.save()
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
        self._output_path = filename_without_extension + '.out'

    def _get_filename_without_extension(self):
        return self._input_file.filepath.split('.')[-2]

    def _append_results(self, CEAResults):
        try:
            self._gamma.append(CEAResults.gamma)
            self._ae_at_ratio.append(CEAResults.ae_at_ratio)
            self._cstar.append(CEAResults.cstar)
            self._cf.append(CEAResults.cf * self._cf_correction)
            self._isp.append(CEAResults.isp)
            self._oxid_fuel_ratio.append(CEAResults.oxid_fuel_ratio)
        except Exception:
            pass

    def _get_cea_results(self):
        return CEAResults(self._output_path)

    def generate_results(self):
        results = {
            'o/f': self._oxid_fuel_ratio,
            'Gamma': self._gamma,
            'Ae/At': self._ae_at_ratio,
            'c*': self._cstar,
            'Cf': self._cf,
            'Isp': self._isp
        }
        return pd.DataFrame(results)


class CEABurnSimulation(object):
    """
    """
    def __init__(self, cea_input_file, method):
        self._input_file = cea_input_file
        self._method = method
        self.LINSPACE_SIZE = 100
        folderpath = os.path.dirname(os.path.abspath(__file__))
        self._path_to_cea = os.path.abspath(os.path.join(folderpath, os.pardir, 'CEA'))
        self.grain_inner_diameter_over_time = list()
        self.regression_rate_over_time = list()
        self.m_dot_fuel_over_time = list()
        self.oxid_fuel_ratio_over_time = list()
        self.cstar_over_time = list()
        self.cf_over_time = list()
        self.isp_over_time = list()
        self.gamma_over_time = list()
        self.gox_over_time = list()

    def set_initial_thrust(self, initial_thrust):
        self._initial_thrust = initial_thrust

    def set_chamber_pressure(self, chamber_pressure):
        self._chamber_pressure = chamber_pressure * (10**5)  # bar to Pa

    def set_regression_rate_parameters(self, a, n):
        self._regression_rate_parameters = RegressionRateEquationParameters(a, n)

    def set_grain_density(self, rho):
        self._rho = rho

    def set_cf_nozzle_correction(self, cf_correction):
        self._cf_correction = cf_correction

    def set_burn_time(self, burn_time):
        self._burn_time = burn_time

    def set_grain_inner_diameter(self, inner_diameter):
        self._grain_inner_diameter = inner_diameter

    def set_grain_outer_diameter(self, outer_diameter):
        self._grain_outer_diameter = outer_diameter

    def set_grain_length(self, grain_length):
        self._grain_length = grain_length

    def set_initial_parameters(self, starting_of):
        self._input_file.set_oxid_fuel_ratio(starting_of)
        self._run_cea()
        cea_initial_results = self._get_cea_results()
        starting_gamma = cea_initial_results.gamma
        starting_ae_at = cea_initial_results.ae_at_ratio
        starting_cstar = cea_initial_results.cstar
        starting_cf = cea_initial_results.cf * self._cf_correction
        starting_isp = cea_initial_results.isp
        self.initial_parameters = {
            'o/f': starting_of,
            'Gamma': starting_gamma,
            'Ae/At': starting_ae_at,
            'c*': starting_cstar,
            'Cf': starting_cf,
            'Isp': starting_isp
        }

    def _run_cea(self):
        self._input_file.save()
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
        self._output_path = filename_without_extension + '.out'

    def _get_filename_without_extension(self):
        return self._input_file.filepath.split('.')[-2]

    def _get_cea_results(self):
        return CEAResults(self._output_path)

    def compute_values_over_time(self, progress_bar):
        self.time = np.linspace(0, self._burn_time, self.LINSPACE_SIZE)
        for idx, _ in enumerate(self.time):
            if self.time[idx] == 0:
                self._compute_initial_values()
            else:
                self._update_values(idx)
            self._append_results_over_time()
            progress_bar.setValue((idx + 1) * 100 / self.LINSPACE_SIZE)
        self.thrust_over_time = self._get_thrust_over_time()

    def _compute_initial_values(self):
        self._oxid_fuel_ratio = self._compute_initial_oxid_fuel_ratio()
        self._initial_m_dot = self._compute_initial_mass_flow_rate()  # kg/s
        self._at = self._compute_nozzle_throat_area()  # mm²
        self._ae = self._compute_nozzle_exit_area()  # mm²
        self._nozzle_exit_diameter = self._compute_nozzle_exit_diameter()  # mm
        self._nozzle_throat_diameter = self._compute_nozzle_throat_diameter()  # mm
        self._m_dot_fuel = self._compute_initial_fuel_mass_flow_rate()  # g/s
        self._m_dot_oxid = self._compute_initial_oxid_mass_flow_rate()  # g/s
        self._grain_inner_diameter = self._compute_initial_grain_inner_diameter()  # mm
        self._regression_rate = self._compute_initial_regression_rate()  # mm/s
        self._gox = self._compute_initial_gox()  # g/(cm².s)
        if self._method != 'Length known':
            self._grain_length = self._compute_grain_length()  # cm
        self._generate_initial_values_results()

    def _compute_initial_oxid_fuel_ratio(self):
        initial_oxid_fuel_ratio = self.initial_parameters['o/f']
        return initial_oxid_fuel_ratio

    def _compute_initial_mass_flow_rate(self):
        initial_m_dot = self._initial_thrust / (self.initial_parameters['Cf'] * self.initial_parameters['c*'])
        return initial_m_dot

    def _compute_nozzle_throat_area(self):
        throat_area = (self._initial_m_dot * self.initial_parameters['c*'] / self._chamber_pressure) * (10**6)
        return throat_area

    def _compute_nozzle_exit_area(self):
        exit_area = self._at * self.initial_parameters['Ae/At']
        return exit_area

    def _compute_nozzle_exit_diameter(self):
        exit_diameter = math.sqrt(4 * self._ae / math.pi)
        return exit_diameter

    def _compute_nozzle_throat_diameter(self):
        throat_diameter = math.sqrt(4 * self._at / math.pi)
        return throat_diameter

    def _compute_initial_fuel_mass_flow_rate(self):
        initial_m_dot_fuel = (self._initial_m_dot * (10**3)) / (1 + self.initial_parameters['o/f'])
        return initial_m_dot_fuel

    def _compute_initial_oxid_mass_flow_rate(self):
        initial_m_dot_oxid = self.initial_parameters['o/f'] * (self._initial_m_dot * (10**3)) / (1 + self.initial_parameters['o/f'])
        return initial_m_dot_oxid

    def _compute_initial_grain_inner_diameter(self):
        if self._method == 'Inner diameter known':
            return self._grain_inner_diameter
        elif self._method == 'Outer diameter known':
            a = self._regression_rate_parameters.a
            n = self._regression_rate_parameters.n
            m_dot_oxid = self._m_dot_oxid / 1000  # g/s to kg/s
            burn_time = self._burn_time
            outer_radius = (self._grain_outer_diameter / 2) / 1000  # mm to m
            initial_inner_radius = ((outer_radius**(2 * n + 1)) - a * (2 * n + 1) * ((m_dot_oxid / math.pi)**n) * burn_time)**(1 / (2 * n + 1))
            initial_inner_diameter = 2 * initial_inner_radius * 1000  # m to mm
            return initial_inner_diameter
        elif self._method == 'Length known':
            a = self._regression_rate_parameters.a
            n = self._regression_rate_parameters.n
            m_dot_oxid = self._m_dot_oxid / 1000  # g/s to kg/s
            m_dot_fuel = self._m_dot_fuel / 1000  # g/s to kg/s
            grain_length = self._grain_length / 100  # cm to m
            rho = self._rho * 1000  # g/cm³ to kg/m³
            initial_inner_radius = (m_dot_fuel / (2 * grain_length * rho * a * (m_dot_oxid**n) * (math.pi**(1 - n))))**(1 / (1 - 2 * n))
            initial_inner_diameter = 2 * initial_inner_radius * 1000  # m to mm
            return initial_inner_diameter

    def _compute_initial_regression_rate(self):
        grain_inner_diameter = self._grain_inner_diameter / 1000  # mm to m
        m_dot_oxid = self._m_dot_oxid / 1000  # g/s to kg/s
        initial_regression_rate = self._regression_rate_parameters.a * ((m_dot_oxid / (math.pi * ((grain_inner_diameter / 2)**2)))**self._regression_rate_parameters.n)
        initial_regression_rate = initial_regression_rate * 1000  # m/s to mm/s
        return initial_regression_rate

    def _compute_grain_length(self):
        grain_length = self._m_dot_fuel / (math.pi * (self._grain_inner_diameter / 10) * (self._regression_rate / 10) * self._rho)
        return grain_length

    def _compute_initial_gox(self):
        initial_gox = self._m_dot_oxid / (math.pi * (((self._grain_inner_diameter / 2) / 10)**2))
        return initial_gox

    def _generate_initial_values_results(self):
        self.initial_results = {
            'Mass_Flow_Rate': (self._initial_m_dot * 1000),
            'Fuel_Mass_Flow_Rate': self._m_dot_fuel,
            'Oxidant_Mass_Flow_Rate': self._m_dot_oxid,
            'Regression_Rate': self._regression_rate,
            'o/f': self.initial_parameters['o/f'],
            'Grain_Inner_Diameter': self._grain_inner_diameter,
            'Gox': self._gox,
            'Nozzle_Throat_Area': self._at,
            'Nozzle_Throat_Diameter': self._nozzle_throat_diameter,
            'Nozzle_Exit_Area': self._ae,
            'Nozzle_Exit_Diameter': self._nozzle_exit_diameter,
            'Grain_Length': self._grain_length
        }

    def _update_values(self, idx):
        self._update_grain_inner_diameter(idx)
        self._update_regression_rate()
        self._update_fuel_mass_flow_rate()
        self._update_oxid_fuel_ratio()
        self._update_gox()

    def _update_grain_inner_diameter(self, idx):
        if self._method == 'Outer diameter known':
            a = self._regression_rate_parameters.a
            n = self._regression_rate_parameters.n
            m_dot_oxid = self._m_dot_oxid / 1000  # g/s to kg/s
            burn_time = self._burn_time
            outer_radius = (self._grain_outer_diameter / 2) / 1000  # mm to m
            initial_inner_radius = ((outer_radius**(2 * n + 1)) - a * (2 * n + 1) * ((m_dot_oxid / math.pi)**n) * burn_time)**(1 / (2 * n + 1))
            current_inner_radius = (initial_inner_radius**(2 * n + 1) + a * (2 * n + 1) * ((m_dot_oxid / math.pi)**n) * self.time[idx])**(1 / (2 * n + 1))
            self._grain_inner_diameter = 2 * current_inner_radius * 1000  # m to mm
        else:
            elapsed_time = self.time[idx] - self.time[idx - 1]
            self._grain_inner_diameter = self._grain_inner_diameter + 2 * self._regression_rate * elapsed_time

    def _update_regression_rate(self):
        a = self._regression_rate_parameters.a
        n = self._regression_rate_parameters.n
        grain_inner_diameter = self._grain_inner_diameter / 1000  # mm to m
        m_dot_oxid = self._m_dot_oxid / 1000  # g/s to kg/s
        regression_rate = a * ((m_dot_oxid / (math.pi * ((grain_inner_diameter / 2)**2)))**n)
        regression_rate = regression_rate * 1000  # m/s to mm/s
        self._regression_rate = regression_rate

    def _update_fuel_mass_flow_rate(self):
        self._m_dot_fuel = math.pi * (self._grain_inner_diameter / 10) * self._grain_length * self._rho * (self._regression_rate / 10)

    def _update_oxid_fuel_ratio(self):
        self._oxid_fuel_ratio = self._m_dot_oxid / self._m_dot_fuel

    def _update_gox(self):
        self._gox = self._m_dot_oxid / (math.pi * (((self._grain_inner_diameter / 2) / 10)**2))

    def _append_results_over_time(self):
        self.grain_inner_diameter_over_time.append(self._grain_inner_diameter)
        self.regression_rate_over_time.append(self._regression_rate)
        self.m_dot_fuel_over_time.append(self._m_dot_fuel)
        self.oxid_fuel_ratio_over_time.append(self._oxid_fuel_ratio)
        self.gox_over_time.append(self._gox)
        self._input_file.set_oxid_fuel_ratio(self._oxid_fuel_ratio)
        self._run_cea()
        cea_results = self._get_cea_results()
        self.cstar_over_time.append(cea_results.cstar)
        self.cf_over_time.append(cea_results.cf * self._cf_correction)
        self.isp_over_time.append(cea_results.isp)
        self.gamma_over_time.append(cea_results.gamma)

    def _get_thrust_over_time(self):
        return np.array(self.cf_over_time) * self._at * self._chamber_pressure * (10**(-6))

    def generate_results(self):
        results = {
            'Time': self.time,
            'Grain_Inner_Diameter': self.grain_inner_diameter_over_time,
            'Regression_Rate': self.regression_rate_over_time,
            'Fuel_Mass_Flow_Rate': self.m_dot_fuel_over_time,
            'Gox': self.gox_over_time,
            'o/f': self.oxid_fuel_ratio_over_time,
            'c*': self.cstar_over_time,
            'Cf': self.cf_over_time,
            'Isp': self.isp_over_time,
            'Gamma': self.gamma_over_time,
            'Thrust': self.thrust_over_time
        }
        return pd.DataFrame(results)

    def is_ac_at_ratio_valid(self):
        self._compute_initial_values()
        return self._grain_inner_diameter >= math.sqrt(6) * self._nozzle_throat_diameter
