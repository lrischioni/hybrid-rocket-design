from PyQt5 import QtWidgets
import math


def launchLoadInputFileConfirmationScreen(parent=None):
    """
    Launch a message box confirming that the input file was
    imported.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.setText('File imported successfully.')
    msg_box.setWindowTitle('Import File')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def _closeWindow(window_box):
    window_box.close()


def launchInputFileNotValidWarning(parent=None):
    """
    Launch a message box warning that the input file is
    not valid.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    msg_box.setText('Input file is not valid.')
    msg_box.setWindowTitle('Import File Error')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchInputInconsistentDataWarning(parent=None):
    """
    Launch a message box warning that the input data is
    inconsistent.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    msg_box.setText('Saving changes failed. Input data is inconsistent.')
    msg_box.setWindowTitle('Saving Changes Error')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchInputFileNotImportedWarning(parent=None):
    """
    Launch a message box warning that the input file was
    not imported.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    msg_box.setText('Input File is not imported. Please import it first.')
    msg_box.setWindowTitle('Run Cea Error')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchStudyPerformedSuccessfullyWarning(parent=None):
    """
    Launch a message box confirming that the propellant analysis was
    executed successfully.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.setText("Propellant analysis performed successfully!")
    msg_box.setWindowTitle('Propellant Analysis')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchStartingValueBiggerThanFinalValueWarning(parent=None):
    """
    Launch a message box warning that the initial misture ratio
    value is larger than the final value.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    msg_box.setText("Starting o/f value can't be larger than the final value.")
    msg_box.setWindowTitle('Perform Propellant Analysis Error')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchStudyNotPerformedWarning(parent=None):
    """
    Launch a message box warning that the propellant analysis
    was not executed.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    msg_box.setText("You need to perform a propellant analysis first.")
    msg_box.setWindowTitle('Select Starting Point Error')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchBurnSimulationInconsistentDataWarning(parent=None):
    """
    Launch a message box warning that the input data for
    the burn simulation is inconsistent.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    msg_box.setText("Error during burn simulation execution. Input data is inconsistent.")
    msg_box.setWindowTitle('Simulating Burn Error')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchBurnSimulatedSuccessfullyConfirmationScreen(parent=None):
    """
    Launch a message box warning that the burn simulation was
    was executed successfully.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.setText("Burn simulated successfully.")
    msg_box.setWindowTitle('Burn Simulation')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchGrainInnerDiameterInvalidWarning(nozzle_throat_diameter, grain_inner_diameter, parent=None):
    """
    Launch a message box warning that the ratio Ac/At
    is invalid.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    message = """
    The grain initial inner diameter ({:.2f} mm) is too small.
    Note that the relation Ac/At > 6 needs to be satisfied. The
    minimum diameter under the current conditions is {:.2f} mm.""".format(grain_inner_diameter, math.sqrt(6) * nozzle_throat_diameter)
    msg_box.setText(message)
    msg_box.setWindowTitle('Simulating Burn Error')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()


def launchExportResultsConfirmationScreen(parent=None):
    """
    Launch a message box confirming that the results were
    exported successfully.

    Args:
        parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
    """
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.setText('Results exported successfully.')
    msg_box.setWindowTitle('Export Results')
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.buttonClicked.connect(lambda: _closeWindow(msg_box))
    msg_box.exec_()
