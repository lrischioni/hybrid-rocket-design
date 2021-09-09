import unittest
import os
from hybridrd.analysis import CEAResults


class CEAResultsTestCase(unittest.TestCase):
    def setUp(self):
        folderpath = os.path.dirname(os.path.abspath(__file__))
        output_file_path = os.path.join(folderpath, 'aux', 'output_test.out')
        self.results = CEAResults(output_file_path)

    def test_gamma_value(self):
        self.assertEqual(self.results.gamma, 1.1209, 'incorrect gamma value')

    def test_ae_at_ratio(self):
        self.assertEqual(self.results.ae_at_ratio, 2.2669, 'incorrect Ae/At value')

    def test_cstar_value(self):
        self.assertEqual(self.results.cstar, 1648.9, 'incorrect cstar value')

    def test_cf_value(self):
        self.assertEqual(self.results.cf, 1.2592, 'incorrect cf value')

    def test_isp_value(self):
        self.assertEqual(self.results.isp, 2076.4, 'incorrect isp value')


if __name__ == '__main__':
    unittest.main()
