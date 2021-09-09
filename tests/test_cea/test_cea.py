import unittest
import os
from hybridrd.analysis import CEA


class CEATestCase(unittest.TestCase):
    def setUp(self):
        self.cea = CEA()
        folderpath = os.path.dirname(os.path.abspath(__file__))
        inputfile_path = os.path.join(folderpath, 'aux', 'test.inp')
        self.cea.import_cea_inputfile(inputfile_path)
        self.cea.run_cea()

    def test_run_cea_generate_output(self):
        self.assertTrue(os.path.isfile(self.cea.output_path), 'output not generated')

    def tearDown(self):
        if os.path.isfile(self.cea.output_path):
            os.remove(self.cea.output_path)


if __name__ == '__main__':
    unittest.main()
