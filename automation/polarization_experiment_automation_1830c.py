"""Polarization Experiment Automation 1830c v 1.0

This module is designed as the main control of the automation,
including augmenting features of the GUI. This is a variation which
uses the Newport 1830-C optical power meter.

Developed by Hayden Jones for usage with the laser polarization
experiment automation.

"""

__authors__ = "Hayden Jones"
__copyright__ = "Copyright 2016, QuIN Lab"
__credits__ = ["Hayden Jones", "Mats Powlowski"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Hayden Jones"
__email__ = "h4jones@uwaterloo.ca"
__status__ = "Production"

import csv
import newport_1830c as newportlib
import polarization_experiment_gui as guilib
import random
import thorlabs_apt as aptlib
import _thread
import time
import wx

serial = 10000000  # ThorLabs Controller Serial Number
power_meter = newportlib.Newport1830C(4)
apt_motor = None
apt_motor_init = False  # Flag to check if motor initialised
kill_automation = False  # Flag to kill automation thread


def apt_device_check(serial_num):
    """Checks if the given serial number is a valid APT device serial.

    Parameters:
        serial_num: int
            The serial number which is going to be verified.

    Returns:
        True if it is a valid device serial, False if it is not valid.

    """
    device_list = aptlib.list_available_devices()
    for i in range(0, len(device_list), 1):
        if serial_num == device_list[i][1] and device_list[i][0] == 31:
            return True
    return False


def serial_warn():
    """Warning message dialog on invalid serial number input."""
    warning_message = "Invalid serial!"
    warning = wx.GenericMessageDialog(None, warning_message, "Warning!",
                                      wx.OK, wx.DefaultPosition)
    warning.ShowModal()
    warning.Destroy()


def range_warn():
    """Warning message dialog on invalid angle range input."""
    warning_message = "Invalid angle range!"
    warning = wx.GenericMessageDialog(None, warning_message, "Warning!",
                                      wx.OK, wx.DefaultPosition)
    warning.ShowModal()
    warning.Destroy()


def zero_warn():
    """Warning message dialog if optical power meter is not zeroed."""
    warning_message = "Power meter not zeroed!"
    warning = wx.GenericMessageDialog(None, warning_message, "Warning!",
                                      wx.OK, wx.DefaultPosition)
    warning.ShowModal()
    warning.Destroy()


def step_warn():
    """Warning message dialog box if the step size is 0."""
    warning_message = "Step size cannot be 0!"
    warning = wx.GenericMessageDialog(None, warning_message, "Warning!",
                                      wx.OK, wx.DefaultPosition)
    warning.ShowModal()
    warning.Destroy()

def go_home():
    """Blocking function to home the motor to 0 position.

    Due to an error in the thorlabs_apt library, the built in homing
    function is broken. Additionally, moving the motor to a position
    which it is already in results in an error and the motor being
    locked in an active state. Thus, this function moves to the 0
    position which may not actually be homed correctly. To home the
    motor correctly the user must use the supplied ThorLabs Kinesis
    software before running this automation.

    """
    global apt_motor_init
    if apt_motor_init is False:
        serial_warn()
        return
    # 'near_zero' represents a random position near 0. This avoids
    # moving to the same location consecutively.
    near_zero = random.randint(0, 10)
    # A hardware timout error occurs during long motions (t > ~20s).
    # To avoid this we build in our own blocking function.
    try:
        apt_motor.move_to(near_zero, True)
    except:
        pass
    while apt_motor.is_in_motion is True:
        time.sleep(0.1)
    try:
        apt_motor.move_to(0, True)
    except:
        pass
    while apt_motor.is_in_motion is True:
        time.sleep(0.1)


class AutomationGUI(guilib.PolarizationExperimentGUI):
    """Subclass of PolarizationExperimentGUI, adding functionality.

    Adds additional functionality in that it actually runs the
    automation and overrides the methods which are bound to elements
    of the GUI. The automation is run in a separate thread to the main
    GUI thread, in order to maintain functionality of the Stop button
    which terminates the automation as soon as it is pressed.

    Parameters
    ----------
    parent : wx.Parent
        Parent for superclass wx.Frame, None for most cases.
    title : str
        The title for the frame of the GUI.

    Methods
    -------
    serial_entry
        When a serial is entered, initialises the motor if possible.
        Otherwise creates a warning to the user.
    home_press
        "Homes" the motor when the Home Stage button is pressed,
        unless motor has been previously "homed".
    zero_press
        Zeroes the optical power meter.
    start_press
        Starts the thread for the automation of the experiment using
        the input parameters from the GUI.
    stop_press
        Kills the thread for the automation.
    update_ui
        Updates the GUI with the current readings from the experiment.
    automation
        Runs the experiment automation using the parameters given.

    """
    def __init__(self, parent=None, 
                 title="Laser Polarization Detection Experiment"):
        self._power_meter_zero = False
        self._is_homed = False
        super(AutomationGUI, self).__init__(parent, title)

    def serial_entry(self, evt):
        """Verifies serial input and initialises the motor if possible.

        Called on data entry into the serial number field. Verifies
        the entered serial and gives a warning if it is not valid. If
        it is valid, initialises `apt_motor` with the serial, sets
        `serial` to be the serial input which was validated, and uses
        the `apt_motor_init` flag to state the motor was initialised.

        Parameters
        ----------
        evt : wx.Event
            The source event which called the method.

        """
        # Don't attempt to verify if the entry is not 8 digits
        if self.get_serial() < 10000000:
            return
        # Disable the UI while blocking is occurring
        self.disable_ui()
        if apt_device_check(self.get_serial()) is False:
            serial_warn()
            self.enable_ui()
            return
        global serial
        serial = self.get_serial()
        global apt_motor
        apt_motor = aptlib.Motor(serial)
        apt_motor.enable()
        global apt_motor_init
        apt_motor_init = True
        self.enable_ui()

    def home_press(self, evt):
        """Homes the stage unless previously homed.

        Called when the Home Stage button is pressed. Uses the
        `_is_homed` flag to avoid homing multiple times consecutively.

        Parameters
        ----------
        evt : wx.Event
            The event which called the method.

        """
        if self._is_homed is False:
            self.disable_ui()
            self.set_moving()
            go_home()
            self._is_homed = True
            self.enable_ui()
            self.set_moving()

    def zero_press(self, evt):
        """Zeroes the optical power meter.

        Called when the Zero Power Meter button is pressed. Uses the
        `_power_meter_zero` flag to make sure the power meter has been
        zeroed at least once before running the automation.

        Parameters
        ----------
        evt : wx.Event
            The event which called the method.

        """
        try:
            power_meter.zero_on()
            self._power_meter_zero = True
        except:
            pass

    def start_press(self, evt):
        """Starts new experiment automation thread, disables GUI input.

        Called on a press of the Start button. Uses `apt_motor_init` to
        check that there is a valid motor. If not, a serial warning is
        produced and the automation is not started. Uses the
        `kill_automation` flag as a kill switch to the automation
        thread, and sets it's value to False because we just started
        the automation. Automatically homes the stage and zeroes the
        optical power meter unless they have already been homed and
        zeroed. Disables GUI inputs. Clears plot. Starts the automation
        in a separate thread, using GUI inputs as parameters.

        Parameters
        ----------
        evt : wx.Event
            The event which called the method.

        """
        global apt_motor_init
        if apt_motor_init is False:
            serial_warn()
            return
        if self.get_end_angle() < self.get_start_angle():
            range_warn()
            return
        if self.get_step_size() == 0:
            step_warn()
            return
        global kill_automation
        kill_automation = False
        self.home_press(wx.EVT_BUTTON)
        if self._power_meter_zero is False:
            zero_warn()
        self.disable_ui()
        self.clear_plt()
        _thread.start_new_thread(self.automation,
                                 (self.get_start_angle(),
                                  self.get_end_angle(),
                                  self.get_step_size(),
                                  self.get_iter_val(),
                                  self.get_speed()))

    def stop_press(self, evt):
        """Kills the automation thread and restores the GUI input.

        Called on press of Stop button. Uses the `kill_automation` flag
        to kill the automation thread. Restores the input of the GUI.

        Parameters
        ----------
        evt : wx.Event
            The event which called this method

        """
        global kill_automation
        kill_automation = True
        self.enable_ui()
        self.update_ui(0, None)

    def update_ui(self, iteration, data):
        """Updates GUI with the current experimental measurements.

        Uses the optical power meter reading to update the current
        power displayed. Uses the position reading to update the
        current position displayed. Uses `iteration` to update the
        current iteration displayed. Uses the motor velocity parameters
        to update the current max speed displayed. Sets the motor
        motion status. Updates the live plot using `data`.

        Parameters
        ----------
        iteration : int
            The iteration value to be displayed.
        data : list of tuple of float
            The list of tuples [measurement angle, power] for the plot.

        """
        global power_meter
        global apt_motor
        self.set_pow_val(float(power_meter.get_power()))
        self.set_curr_angle_val(apt_motor.position)
        self.set_curr_iter(iteration)
        self.set_speed(apt_motor.get_velocity_parameters()[2])
        self.set_moving()
        if data is not None:
            self.update_plt(data)

    def automation(self, start_angle, end_angle, step_size, num_iter, speed):
        """The automation of the experiment.

        Takes the input parameters and uses them to run the experiment.
        Outputs experimental data to a csv file.

        Parameters
        ----------
        start_angle : float
            The start angle of the rotation range.
        end_angle : float
            The end angle of the rotation range.
        step_size : float
            The step size for moving through the rotation range.
        num_iter : int
            The number of iterations over the range to take place.
        speed : int
            The maximum speed setting of the rotation.

        """
        global apt_motor
        global power_meter
        global kill_automation
        apt_motor.set_velocity_parameters(0, 10, speed)
        filename = "output" + str(random.randint(0, 9999)) + ".csv"
        measurements = []
        with open(filename, "w", newline='') as output:
            writer = csv.writer(output, lineterminator='\n')
            for i in range(0, num_iter, 1):
                if kill_automation is True:
                    break
                apt_motor.move_to(5, True)
                curr_iter = i + 1
                # Use one digit of precision to describe the motion.
                for j in range(int(start_angle*10),
                               int(end_angle*10),
                               int(step_size*10)):
                    if kill_automation is True:
                        break
                    apt_motor.move_to(float(j/10), True)
                    time.sleep(1)
                    try:
                        power = float(power_meter.get_power())
                        measurements.append([apt_motor.position, power])
                    except:
                        measurements.append(["ERROR", "ERROR"])
                    writer.writerow(measurements[-1])
                    wx.CallAfter(self.update_ui, curr_iter, measurements)
        self._is_homed = False
        wx.CallAfter(self.stop_press, wx.EVT_BUTTON)

if __name__ == "__main__":
    app = wx.App()
    gui = AutomationGUI()
    app.MainLoop()
