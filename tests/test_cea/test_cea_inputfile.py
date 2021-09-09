import unittest
import os
from hybridrd.inputfile import CEAInputFile


class CEAInputFileTestCase(unittest.TestCase):
    def setUp(self):
        self.inputfile = CEAInputFile()

    def test_set_fuel_name(self):
        self.inputfile.set_fuel('fuel name', 1.0, 298.1)
        self.assertEqual(self.inputfile.fuel.name, 'fuel name', 'incorrect fuel name')

    def test_set_fuel_temperature(self):
        self.inputfile.set_fuel('fuel_name', 1.0, 298.1)
        self.assertEqual(self.inputfile.fuel.temperature, 298.1, 'incorrect fuel temperature')

    def test_set_fuel_amount(self):
        self.inputfile.set_fuel('fuel_name', 1.0, 298.1)
        self.assertEqual(self.inputfile.fuel.amount, 1.0, 'incorrect fuel amount')

    def test_set_oxidant_name(self):
        self.inputfile.set_oxidant('oxidant name', 1.0, 298.2)
        self.assertEqual(self.inputfile.oxidant.name, 'oxidant name', 'incorrect oxidant name')

    def test_set_oxidant_temperature(self):
        self.inputfile.set_oxidant('oxidant name', 1.0, 298.2)
        self.assertEqual(self.inputfile.oxidant.temperature, 298.2, 'incorrect oxidant temperature')

    def test_set_oxidant_amount(self):
        self.inputfile.set_oxidant('oxidant name', 1.0, 298.2)
        self.assertEqual(self.inputfile.oxidant.amount, 1.0, 'incorrect oxidant amount')

    def test_set_chamber_pressure(self):
        self.inputfile.set_chamber_pressure(11)
        self.assertEqual(self.inputfile.chamber_pressure, 11, 'incorrect pressure chamber')

    def test_set_pressure_ratio(self):
        self.inputfile.set_pressure_ratio(8)
        self.assertEqual(self.inputfile.chamber_atmospheric_pressure_ratio, 8, 'incorrect pressure ratio')

    def test_set_oxid_fuel_ratio(self):
        self.inputfile.set_oxid_fuel_ratio(7)
        self.assertEqual(self.inputfile.oxid_fuel_ratio, 7, 'incorrect oxid-fuel ratio')

    def test_set_filepath(self):
        self.inputfile.set_filepath('new file path')
        self.assertEqual(self.inputfile.filepath, 'new file path', 'incorrect file path')


class LoadCEAInputFileTestCase(unittest.TestCase):
    def setUp(self):
        folderpath = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(folderpath, 'auxiliar', 'test.inp')
        self.inputfile = CEAInputFile(filepath)

    def test_set_fuel_name_from_file(self):
        self.assertEqual(self.inputfile.fuel.name, 'PMMA', 'incorrect fuel name')

    def test_set_fuel_temperature_from_file(self):
        self.assertEqual(self.inputfile.fuel.temperature, 298.15, 'incorrect fuel temperature')

    def test_set_oxidant_name_from_file(self):
        self.assertEqual(self.inputfile.oxidant.name, 'O2', 'incorrect oxidant name')

    def test_set_oxidant_temperature_from_file(self):
        self.assertEqual(self.inputfile.oxidant.temperature, 298.15, 'incorrect oxidant temperature')

    def test_set_chamber_pressure_from_file(self):
        self.assertEqual(self.inputfile.chamber_pressure, 10, 'incorrect chamber pressure')

    def test_set_pressure_ratio_from_file(self):
        self.assertEqual(self.inputfile.chamber_atmospheric_pressure_ratio, 10.42, 'incorrect pressure ratio')

    def test_set_oxid_fuel_ratio(self):
        self.assertEqual(self.inputfile.oxid_fuel_ratio, 2.0, 'incorrect oxid-fuel ratio')


class SaveCEAInputFileFromPreviousFileTestCase(unittest.TestCase):
    def setUp(self):
        folderpath = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(folderpath, 'auxiliar', 'test.inp')
        self.inputfile = CEAInputFile(filepath)
        self.savepath = os.path.join(folderpath, 'auxiliar', 'save_test.inp')

    def test_save_file(self):
        self.inputfile.save(self.savepath)
        self.assertTrue(os.path.isfile(self.savepath), 'file not saved')

    def test_save_file_content_fuel_name(self):
        self.inputfile.set_fuel('otherName', self.inputfile.fuel.amount, self.inputfile.fuel.temperature)
        self.inputfile.save(self.savepath)
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.fuel.name, self.saved_inputfile.fuel.name, 'incorrect saved fuel name')

    def test_save_file_content_fuel_temperature(self):
        self.inputfile.set_fuel(self.inputfile.fuel.name, self.inputfile.fuel.amount, 276.23)
        self.inputfile.save(self.savepath)
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.fuel.temperature, self.saved_inputfile.fuel.temperature, 'incorrect saved fuel temperature')

    def test_save_file_content_oxidant_name(self):
        self.inputfile.set_oxidant('anotherName', self.inputfile.oxidant.amount, self.inputfile.oxidant.temperature)
        self.inputfile.save(self.savepath)
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.oxidant.name, self.saved_inputfile.oxidant.name, 'incorrect saved oxidant name')

    def test_save_file_content_oxidant_temperature(self):
        self.inputfile.set_oxidant(self.inputfile.oxidant.name, self.inputfile.oxidant.amount, 278.23)
        self.inputfile.save(self.savepath)
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.oxidant.temperature, self.saved_inputfile.oxidant.temperature, 'incorrect saved oxidant temperature')

    def test_save_file_content_chamber_pressure(self):
        self.inputfile.set_chamber_pressure(5)
        self.inputfile.save(self.savepath)
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.chamber_pressure, self.saved_inputfile.chamber_pressure, 'incorrect saved chamber pressure')

    def test_save_file_content_pressure_ratio(self):
        self.inputfile.set_pressure_ratio(2.6)
        self.inputfile.save(self.savepath)
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.chamber_atmospheric_pressure_ratio, self.saved_inputfile.chamber_atmospheric_pressure_ratio, 'incorrect saved pressure ratio')

    def test_save_file_content_oxid_fuel_ratio(self):
        self.inputfile.set_oxid_fuel_ratio(1.5)
        self.inputfile.save(self.savepath)
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.oxid_fuel_ratio, self.saved_inputfile.oxid_fuel_ratio, 'incorrect saved oxid-fuel ratio')

    def tearDown(self):
        if os.path.isfile(self.savepath):
            os.remove(self.savepath)


class SaveCEAInputFileFromTemplateTestCase(unittest.TestCase):
    def setUp(self):
        self.inputfile = CEAInputFile()
        self.inputfile.set_oxidant('oxidant', 1.0, 298.74)
        self.inputfile.set_fuel('fuel', 1.0, 295.47)
        self.inputfile.set_chamber_pressure(6)
        self.inputfile.set_pressure_ratio(8)
        self.inputfile.set_oxid_fuel_ratio(1.47)
        folderpath = os.path.dirname(os.path.abspath(__file__))
        self.savepath = os.path.join(folderpath, 'auxiliar', 'save_test_template.inp')
        self.inputfile.save(self.savepath)

    def test_save_file(self):
        self.assertTrue(os.path.isfile(self.savepath), 'file not saved')

    def test_save_file_content_fuel_name(self):
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.fuel.name, self.saved_inputfile.fuel.name, 'incorrect saved fuel name')

    def test_save_file_content_fuel_temperature(self):
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.fuel.temperature, self.saved_inputfile.fuel.temperature, 'incorrect saved fuel temperature')

    def test_save_file_content_oxidant_name(self):
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.oxidant.name, self.saved_inputfile.oxidant.name, 'incorrect saved oxidant name')

    def test_save_file_content_oxidant_temperature(self):
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.oxidant.temperature, self.saved_inputfile.oxidant.temperature, 'incorrect saved oxidant temperature')

    def test_save_file_content_chamber_pressure(self):
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.chamber_pressure, self.saved_inputfile.chamber_pressure, 'incorrect saved chamber pressure')

    def test_save_file_content_pressure_ratio(self):
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.chamber_atmospheric_pressure_ratio, self.saved_inputfile.chamber_atmospheric_pressure_ratio, 'incorrect saved pressure ratio')

    def test_save_file_content_oxid_fuel_ratio(self):
        self.saved_inputfile = CEAInputFile(self.savepath)
        self.assertEqual(self.inputfile.oxid_fuel_ratio, self.saved_inputfile.oxid_fuel_ratio, 'incorrect saved oxid-fuel ratio')

    def tearDown(self):
        if os.path.isfile(self.savepath):
            os.remove(self.savepath)


if __name__ == '__main__':
    unittest.main()
