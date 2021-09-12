class RegressionRateEquationParameters(object):
    """
    This is a class that represents the parameters of the regression
    rate equation from a certain pair fuel/oxidant propellants.
    """
    def __init__(self, a, n):
        """
        Constructor method.

        Args:
            a (float): Regression rate coefficient
            n (float): Flux exponent
        """
        self.a = a
        self.n = n
