class PlotDictEnUs(dict):
    """
    This class is an auxiliary dictionary used to plot the results in english
    on the GUI application.
    """
    def __init__(self):
        """
        Constructor method
        """
        super().__init__()
        self['o/f'] = 'Misture Ratio o/f'
        self['Misture Ratio o/f'] = 'Misture Ratio o/f'
        self['c*'] = 'c* (m/s)'
        self['Gamma'] = 'Gamma'
        self['Ae/At'] = 'Ae/At'
        self['Cf'] = 'Cf'
        self['Isp'] = 'Isp (m/s)'
        self['Time'] = 'Time (s)'
        self['Gox'] = 'Gox (g/(cm².s))'
        self['Grain Inner Diameter'] = 'Grain Inner Diameter (mm)'
        self['Regression Rate'] = 'Regression Rate (mm/s)'
        self['Fuel Mass Flow Rate'] = 'Fuel Mass Flow Rate (g/s)'
        self['Thrust'] = 'Thrust (N)'


class PlotDictPtBr(dict):
    """
    This class is an auxiliary dictionary used to plot the results in portuguese
    on the GUI application.
    """
    def __init__(self):
        """
        Constructor method
        """
        super().__init__()
        self['o/f'] = 'Razão de Mistura o/f'
        self['Misture Ratio o/f'] = 'Razão de Mistura o/f'
        self['c*'] = 'c* (m/s)'
        self['Gamma'] = 'Gamma'
        self['Ae/At'] = 'Ae/At'
        self['Cf'] = 'Cf'
        self['Isp'] = 'Isp (m/s)'
        self['Time'] = 'Tempo (s)'
        self['Gox'] = 'Gox (g/(cm².s))'
        self['Grain Inner Diameter'] = 'Diâmetro Interno do Grão (mm)'
        self['Regression Rate'] = 'Taxa de Regressão (mm/s)'
        self['Fuel Mass Flow Rate'] = 'Fluxo de Massa de Combustível (g/s)'
        self['Thrust'] = 'Empuxo (N)'


class BurnSimulationPlotDictYAxis(dict):
    """
    This class is an auxiliary dictionary used to plot the results from the
    burn simulation on the GUI application.
    """
    def __init__(self):
        """
        Constructor method
        """
        super().__init__()
        self['Misture Ratio o/f'] = 'o/f'
        self['c*'] = 'c*'
        self['Cf'] = 'Cf'
        self['Isp'] = 'Isp'
        self['Gox'] = 'Gox'
        self['Grain Inner Diameter'] = 'Grain_Inner_Diameter'
        self['Regression Rate'] = 'Regression_Rate'
        self['Fuel Mass Flow Rate'] = 'Fuel_Mass_Flow_Rate'
        self['Thrust'] = 'Thrust'
