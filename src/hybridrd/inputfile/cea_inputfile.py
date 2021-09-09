import os.path
import sys
from jinja2 import Environment, FileSystemLoader
from hybridrd.propellant import Propellant


class CEAInputFile(object):
    """
    """
    def __init__(self, filepath=''):
        if self._file_exists(filepath):
            self.filepath = filepath
            self._load_input_file_information(filepath)

    def _file_exists(self, filepath):
        return os.path.isfile(filepath)

    def _load_input_file_information(self, filepath):
        try:
            with open(filepath, 'r') as input_file:
                self._content = input_file.readlines()
                for idx, line in enumerate(self._content):
                    self._load_line_information(idx, line)
                delattr(self, '_content')
        except OSError as error:
            print('File {:s} failed'.format(error.filename))
            sys.exit()

    def _load_line_information(self, idx, line):
        if 'fuel=' in line:
            self._set_fuel_from_file(idx, line)
        elif 'oxid=' in line:
            self._set_oxidant_from_file(idx, line)
        elif 'p,bar=' in line:
            self._set_chamber_pressure_from_file(line)
        elif 'pi/p=' in line:
            self._set_pressure_ratio_from_file(line)
        elif 'o/f=' in line:
            self._set_oxid_fuel_ratio_from_file(line)
        elif 'equilibrium' in line:
            self._set_equilibrium_method_from_file(line)
        elif 'frozen' in line:
            self._set_frozen_method_from_file(line)

    def _set_fuel_from_file(self, idx, line):
        words = line.split()
        fuel_name = words[0].replace('fuel=', '')
        fuel_amount = float(words[1].replace('wt=', ''))
        fuel_temperature = float(words[2].replace('t,k=', ''))
        if 'h,kj/mol=' in self._content[idx + 1]:
            words_next_line = self._content[idx + 1].split()
            energy_h = words_next_line[0].replace('h,kj/mol=', '')
            formula = self._getFormulaFromSpacedLetters(words_next_line[1:])
            self.set_fuel(fuel_name, fuel_amount, fuel_temperature, energy_h, formula)
        else:
            self.set_fuel(fuel_name, fuel_amount, fuel_temperature)

    def _getFormulaFromSpacedLetters(self, letters):
        formula = ''
        for letter in letters:
            formula = formula + letter
        return formula

    def _set_oxidant_from_file(self, idx, line):
        words = line.split()
        oxidant_name = words[0].replace('oxid=', '')
        oxidant_amount = float(words[1].replace('wt=', ''))
        oxidant_temperature = float(words[2].replace('t,k=', ''))
        if 'h,kj/mol=' in self._content[idx + 1]:
            words_next_line = self._content[idx + 1].split()
            energy_h = words_next_line[0].replace('h,kj/mol=', '')
            formula = self._getFormulaFromSpacedLetters(words_next_line[1:])
            self.set_oxidant(oxidant_name, oxidant_amount, oxidant_temperature, energy_h, formula)
        else:
            self.set_oxidant(oxidant_name, oxidant_amount, oxidant_temperature)

    def _set_chamber_pressure_from_file(self, line):
        words = line.split()
        chamber_pressure = float(words[0].replace('p,bar=', '').replace(',', ''))
        self.set_chamber_pressure(chamber_pressure)

    def _set_pressure_ratio_from_file(self, line):
        words = line.split()
        pressure_ratio = float(words[0].replace('pi/p=', '').replace(',', ''))
        self.set_pressure_ratio(pressure_ratio)

    def _set_oxid_fuel_ratio_from_file(self, line):
        words = line.split()
        oxid_fuel_ratio = float(words[1].replace('o/f=', '').replace(',', ''))
        self.set_oxid_fuel_ratio(oxid_fuel_ratio)

    def _set_equilibrium_method_from_file(self):
        method = 'equilibrium'
        self.set_method(method)

    def _set_frozen_method_from_file(self, line):
        words = line.split()
        freezing_point = float(words[2].replace('nfz=', ''))
        method = 'frozen'
        self.set_method(method, freezing_point)

    def set_fuel(self, fuel_name, fuel_amount, fuel_temperature, energy_h=None, formula=None):
        self.fuel = Propellant(fuel_name, fuel_amount, fuel_temperature, energy_h, formula)

    def set_oxidant(self, oxidant_name, oxidant_amount, oxidant_temperature, energy_h=None, formula=None):
        self.oxidant = Propellant(oxidant_name, oxidant_amount, oxidant_temperature, energy_h, formula)

    def set_chamber_pressure(self, chamber_pressure):
        self.chamber_pressure = chamber_pressure

    def set_pressure_ratio(self, chamber_atmospheric_pressure_ratio):
        self.chamber_atmospheric_pressure_ratio = chamber_atmospheric_pressure_ratio

    def set_oxid_fuel_ratio(self, oxid_fuel_ratio):
        self.oxid_fuel_ratio = oxid_fuel_ratio

    def set_method(self, method, freezing_point=None):
        self.method = method
        if freezing_point:
            self.freezing_point = freezing_point

    def set_filepath(self, new_filepath):
        self.filepath = new_filepath

    def save(self, savepath=None):
        if savepath is None:
            savepath = self._get_tmp_savepath_from_filepath()
        if hasattr(self, 'filepath'):
            self._write_file_from_previous_file(savepath)
            if self._is_tmp_savepath():
                self._remove_old_file()
                self._rename_new_file_to_old_filepath()
            else:
                self.set_filepath(savepath)
        else:
            self._write_file_from_template(savepath)
            self.set_filepath(savepath)

    def _get_tmp_savepath_from_filepath(self):
        filepath_without_extension = self.filepath.split('.')[-2]
        self.tmp_savepath = filepath_without_extension + '_.inp'
        return self.tmp_savepath

    def _write_file_from_previous_file(self, savepath):
        try:
            with open(self.filepath, 'r') as input_file, open(savepath, 'w') as saved_file:
                self._adapt_old_file_to_saved_file(input_file, saved_file)
        except OSError as error:
            print('File {:s} failed'.format(error.filename))
            sys.exit()

    def _adapt_old_file_to_saved_file(self, input_file, saved_file):
        content = input_file.readlines()
        line_iter = iter(content)
        for line in line_iter:
            modified_line = self._modify_line_information(line)
            if self._lineIsPropellantInfoContinuation(modified_line):
                line_iter.__next__()
            saved_file.write(modified_line)

    def _lineIsPropellantInfoContinuation(self, line):
        return 'h,kj/mol=' in line

    def _modify_line_information(self, line):
        words = line.split()
        if 'fuel=' in line:
            modified_line = self._set_fuel_in_file(words)
        elif 'oxid=' in line:
            modified_line = self._set_oxidant_in_file(words)
        elif 'p,bar=' in line:
            modified_line = self._set_chamber_pressure_in_file(words)
        elif 'pi/p=' in line:
            modified_line = self._set_pressure_ratio_in_file(words)
        elif 'o/f=' in line:
            modified_line = self._set_oxid_fuel_ratio_in_file(words)
        elif 'equilibrium' in line or 'frozen' in line:
            modified_line = self._set_method_in_file(words)
        else:
            modified_line = line
        return self._format_line(modified_line)

    def _set_fuel_in_file(self, words):
        words[0] = words[0][0:5] + self.fuel.name
        words[1] = words[1][0:3] + str(self.fuel.amount)
        words[2] = words[2][0:4] + str(self.fuel.temperature)
        if hasattr(self.fuel, 'energy_h'):
            energy_h = str(self.fuel.energy_h)
            formula = ' '.join(self.fuel.formula)
            next_line = '    h,kj/mol=' + energy_h + '  ' + formula + '\n'
            return self._join_words(words) + next_line
        else:
            return self._join_words(words)

    def _set_oxidant_in_file(self, words):
        words[0] = words[0][0:5] + self.oxidant.name
        words[1] = words[1][0:3] + str(self.oxidant.amount)
        words[2] = words[2][0:4] + str(self.oxidant.temperature)
        if hasattr(self.oxidant, 'energy_h'):
            energy_h = str(self.oxidant.energy_h)
            formula = ' '.join(self.oxidant.formula)
            next_line = '    h,kj/mol=' + energy_h + '  ' + formula + '\n'
            return self._join_words(words) + next_line
        else:
            return self._join_words(words)

    def _set_chamber_pressure_in_file(self, words):
        words[0] = words[0][0:6] + str(self.chamber_pressure) + ','
        return self._join_words(words)

    def _set_pressure_ratio_in_file(self, words):
        words[0] = words[0][0:5] + str(self.chamber_atmospheric_pressure_ratio) + ','
        return self._join_words(words)

    def _set_oxid_fuel_ratio_in_file(self, words):
        words[1] = words[1][0:4] + str(self.oxid_fuel_ratio) + ','
        return self._join_words(words)

    def _set_method_in_file(self, words):
        words[1] = self.method
        if self.method == 'frozen':
            if len(words) == 3:
                words[2] = words[2][0:4] + str(self.freezing_point)
            else:
                words[1] = words[1] + '  nfz=' + str(self.freezing_point)
        else:
            if len(words) == 3:
                words[2] = ''
        return self._join_words(words)

    def _join_words(self, words):
        modified_line = ''
        for word in words:
            modified_line = modified_line + word + ' '
        modified_line = modified_line + '\n'
        return modified_line

    def _format_line(self, line):
        if 'fuel=' in line:
            formatted_line = '  ' + line
        elif 'oxid=' in line:
            formatted_line = '  ' + line
        elif 'p,bar=' in line:
            formatted_line = '  ' + line
        elif 'pi/p=' in line:
            formatted_line = '  ' + line
        elif 'equilibrium' in line or 'frozen' in line:
            formatted_line = '      ' + line
        else:
            formatted_line = line
        return formatted_line

    def _is_tmp_savepath(self):
        return hasattr(self, 'tmp_savepath')

    def _remove_old_file(self):
        os.remove(self.filepath)

    def _rename_new_file_to_old_filepath(self):
        os.rename(self.tmp_savepath, self.filepath)
        delattr(self, 'tmp_savepath')

    def _write_file_from_template(self, savepath):
        folderpath = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.abspath(os.path.join(folderpath, os.pardir, 'templates'))
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template('template_cea_input.j2')
        parsed_template = template.render(oxid_fuel_ratio=self.oxid_fuel_ratio,
                                          chamber_pressure=self.chamber_pressure,
                                          pressure_ratio=self.chamber_atmospheric_pressure_ratio,
                                          oxidant_name=self.oxidant.name,
                                          oxidant_temperature=self.oxidant.temperature,
                                          fuel_name=self.fuel.name,
                                          fuel_temperature=self.fuel.temperature)
        try:
            with open(savepath, 'w') as f:
                f.write(parsed_template)
        except OSError as error:
            print('File {:s} failed'.format(error.filename))
            sys.exit()
