import unittest
from hybridrd.propellant import Propellant


class PropellantTestCase(unittest.TestCase):
    def setUp(self):
        self.propellant = Propellant('name', 1.0, 298.15)

    def test_propellant_name(self):
        self.assertEqual(self.propellant.name, 'name', 'incorrect name')

    def test_propellant_temperature(self):
        self.assertEqual(self.propellant.temperature, 298.15, 'incorrect temperature')


if __name__ == '__main__':
    unittest.main()
