class Propellant(object):
    """
    This is a class that represents the propellant that will be used by the
    :class: `CEAInputFile`. It can represent either the fuel or the oxidant.
    """
    def __init__(self, name, amount, temperature, energy_h=None, formula=None):
        """
        Constructor method.

        Args:
            name (str): Name of the propellant
            amount (float): Amount that this propellant represents overall considering
                all fuels or all oxidants
            temperature (float): Temperature of the propellant in Kelvin
            energy_h (float, optional): Enthalpy energy of the propellant. This must
                be provided only if the propellant is not on the CEA database. Defaults to None.
            formula (str, optional): Chemical formula of the propellant. This must be provided
                only if the propellant is not on the CEA database. Defaults to None.
        """
        self.name = name
        self.amount = amount
        self.temperature = temperature
        if energy_h:
            self.energy_h = energy_h
        if formula:
            self.formula = formula
