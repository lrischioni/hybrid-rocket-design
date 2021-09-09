class Propellant(object):
    """
    """
    def __init__(self, name, amount, temperature, energy_h=None, formula=None):
        self.name = name
        self.amount = amount
        self.temperature = temperature
        if energy_h:
            self.energy_h = energy_h
        if formula:
            self.formula = formula
