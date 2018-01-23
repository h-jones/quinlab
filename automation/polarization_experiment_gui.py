"""Polarization Experiment GUI v 1.0

This module is the GUI for the laser polarization experiment.

Developed by Hayden Jones for usage with the laser polarization
experiment automation.

"""

__authors__ = "Hayden Jones"
__copyright__ = "Copyright 2016, QuIN Lab"
__credits__ = ["Hayden Jones"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Hayden Jones"
__email__ = "h4jones@uwaterloo.ca"
__status__ = "Production"

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
import numpy as np
import wx
from wx.lib.masked import NumCtrl

class PolarizationExperimentGUI(wx.Frame):
    """The base object for the Polarization Experiment GUI.

    Parameters
    ----------
    parent : wx.Parent
        Parent for the superclass wx.Frame, usually None in most cases.
    title : str
        The title for the frame of the GUI.

    Methods
    -------
    disable_ui
        Disables the input on the UI, except enables the stop button.
    enable_ui
        Enables the input on the UI, except disables the stop button.
    serial_entry
        Intended for override by subclass, this is bound to the event
        on data entry into the serial number field.
    home_press
        Intended for override by subcless, this is bound to the event
        on pressing the Home Stage button.
    zero_press
        Intended for override by subclass, this is bound to the event
        on pressing the Zero Power Meter button.
    start_press
        Intended for override by subclass, this is bound to the event
        on pressing the Start button.
    stop_press
        Intended for override by subclass, this is bound to the event
        on pressing the Stop button.
    get_serial
        Return the value of the serial number input.
    set_pow_val
        Set value of current power reading.
    set_curr_angle_val
        Set value of current angle reading.
    get_start_angle
        Return start angle input value.
    get_end_angle
        Return end angle input value.
    get_step_size
        Return step size input value.
    set_curr_iter
        Set current iteration value.
    get_iter_val
        Return iteration input value.
    set_speed
        Set current speed value.
    set_moving
        Sets the motion status.
    get_speed
        Get speed input value.

    """
    def __init__(self,
                 parent=None,
                 title="Laser Polarization Detection Experiment"):
        # Creation of objects to be used only within the class
        # '_is_disabled' refers to whether the UI is disabled or enabled
        self._is_disabled = False
        self._program_font = wx.Font(
            13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, 
            wx.FONTWEIGHT_NORMAL, False, "", wx.FONTENCODING_SYSTEM)
        self._title_font = wx.Font(
            15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, True, "", wx.FONTENCODING_SYSTEM)
        self._serial_val = wx.Object()
        self._curr_pow_val = wx.Object()
        self._curr_angle_val = wx.Object()
        self._start_angle_val = wx.Object()
        self._end_angle_val = wx.Object()
        self._step_size_val = wx.Object()
        self._curr_iter_val = wx.Object()
        self._set_iter_val = wx.Object()
        self._moving_val = wx.Object()
        self._curr_speed_val = wx.Object()
        self._set_speed_val = wx.Object()
        self._home_button = wx.Object()
        self._zero_button = wx.Object()
        self._start_button = wx.Object()
        self._stop_button = wx.Object()
        self._live_plt = Figure()
        self._live_plt.set_facecolor('w')
        axes_dim = [0.125, 0.125, 0.8, 0.8]
        # self._live_plt_axes = self._live_plt.add_axes(axes_dim)
        self._live_plt_axes = self._live_plt.add_axes(axes_dim, polar=True)
        self._live_plt_canvas = 0

        # Initialise the frame with title and fixed size
        super(PolarizationExperimentGUI, self).__init__(parent, 
                                                        title=title,
                                                        size=(1200, 600))
        self.SetWindowStyle(
            wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        self._generate_dynamic_ui()
        self.Show()

    def _generate_dynamic_ui(self):
        """Create the elements for the interface."""
        # Create the panel for the widgets to be placed on
        program_panel = wx.Panel(self)
        program_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create the panel for the controls
        control_panel = wx.Panel(program_panel)
        control_panel.SetSize(wx.Size(400, 600))
        control_panel.SetBackgroundColour(wx.WHITE)

        # Set the control panel sizer to be a vertical BoxSizer
        control_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title object
        title_label = wx.StaticText(
            control_panel, -1, "Experiment Parameters", wx.DefaultPosition,
            wx.DefaultSize, wx.ALIGN_CENTER, "StaticTextNameStr")
        title_label.SetFont(self._title_font)

        # Serial panel objects
        serial_panel = wx.Panel(control_panel)
        serial_sizer = wx.FlexGridSizer(1, 2, 0, 0)

        serial_label = wx.StaticText(
            serial_panel, -1, "ThorLabs Serial: ", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_RIGHT, "StaticTextNameStr")
        serial_label.SetFont(self._program_font)
        self._serial_val =  wx.Choice(
            serial_panel, size=(200, 20), 
            choices=["83843569", "83846179", "83845569"])
        serial_sizer.AddMany([serial_label, self._serial_val])
        serial_panel.SetSizer(serial_sizer)

        # Power panel objects
        power_panel = wx.Panel(control_panel)
        power_sizer = wx.FlexGridSizer(1, 2, 0, 0)

        curr_power_label = wx.StaticText(
            power_panel, -1, "Current Power (W): ", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_RIGHT, "StaticTextNameStr")
        curr_power_label.SetFont(self._program_font)
        self._curr_pow_val = wx.StaticText(
            power_panel, -1, "", wx.DefaultPosition, wx.Size(200, 20),
            wx.ALIGN_LEFT, "StaticTextNameStr")
        self._curr_pow_val.SetFont(self._program_font)
        power_sizer.AddMany([curr_power_label, self._curr_pow_val])
        power_panel.SetSizer(power_sizer)

        # Angle panel objects
        angle_panel = wx.Panel(control_panel)
        angle_sizer = wx.FlexGridSizer(6, 2, 0, 0)
        curr_angle_label = wx.StaticText(
            angle_panel, -1, "Current Angle (\xb0): ", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_RIGHT, "StaticTextNameStr")
        curr_angle_label.SetFont(self._program_font)
        self._curr_angle_val = wx.StaticText(
            angle_panel, -1, "", wx.DefaultPosition, wx.Size(200, 20),
            wx.ALIGN_LEFT, "StaticTextNameStr")
        self._curr_angle_val.SetFont(self._program_font)
        start_angle_label = wx.StaticText(
            angle_panel, -1, "Start Angle (\xb0): ", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_RIGHT, "StaticTextNameStr")
        start_angle_label.SetFont(self._program_font)
        self._start_angle_val = NumCtrl(
            angle_panel, -1, 0, wx.DefaultPosition, wx.Size(-1, 20),
            wx.TE_PROCESS_TAB | wx.TE_PROCESS_ENTER, wx.DefaultValidator,
            "masked.num")
        self._start_angle_val.SetAllowNegative(False)
        self._start_angle_val.SetBounds(0, 359.9)
        self._start_angle_val.SetFractionWidth(1)
        self._start_angle_val.SetIntegerWidth(3)
        self._start_angle_val.SetValue(0)
        self._start_angle_val.SetLimited(True)
        self._start_angle_val.SetFont(self._program_font)
        end_angle_label = wx.StaticText(
            angle_panel, -1, "End Angle (\xb0): ", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_RIGHT, "StaticTextNameStr")
        end_angle_label.SetFont(self._program_font)
        self._end_angle_val = NumCtrl(
            angle_panel, -1, 0, wx.DefaultPosition, wx.Size(-1, 20),
            wx.TE_PROCESS_TAB | wx.TE_PROCESS_ENTER, wx.DefaultValidator,
            "masked.num")
        self._end_angle_val.SetAllowNegative(False)
        self._end_angle_val.SetBounds(0, 360)
        self._end_angle_val.SetFractionWidth(1)
        self._end_angle_val.SetIntegerWidth(3)
        self._end_angle_val.SetValue(360)
        self._end_angle_val.SetLimited(True)
        self._end_angle_val.SetFont(self._program_font)
        step_size_label = wx.StaticText(
            angle_panel, -1, "Step Size (\xb0): ", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_RIGHT, "StaticTextNameStr")
        step_size_label.SetFont(self._program_font)
        self._step_size_val = NumCtrl(
            angle_panel, -1, 0, wx.DefaultPosition, wx.Size(200, 20),
            wx.TE_PROCESS_TAB | wx.TE_PROCESS_ENTER, wx.DefaultValidator,
            "masked.num")
        self._step_size_val.SetAllowNegative(False)
        self._step_size_val.SetBounds(0, 360)
        self._step_size_val.SetFractionWidth(1)
        self._step_size_val.SetIntegerWidth(3)
        self._step_size_val.SetValue(1)
        self._step_size_val.SetLimited(True)
        self._step_size_val.SetFont(self._program_font)
        curr_iter_label = wx.StaticText(
            angle_panel, -1, "Current Iteration: ", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_RIGHT, "StaticTextNameStr")
        curr_iter_label.SetFont(self._program_font)
        self._curr_iter_val = wx.StaticText(
            angle_panel, -1, "Not currently testing!", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_LEFT, "StaticTextNameStr")
        self._curr_iter_val.SetFont(self._program_font)
        set_iter_label = wx.StaticText(
            angle_panel, -1, "Iterations: ", wx.DefaultPosition,
            wx.Size(200, 20), wx.ALIGN_RIGHT, "StaticTextNameStr")
        set_iter_label.SetFont(self._program_font)
        self._set_iter_val = NumCtrl(
            angle_panel, -1, 0, wx.DefaultPosition, wx.Size(200, 20),
            wx.TE_PROCESS_TAB | wx.TE_PROCESS_ENTER, wx.DefaultValidator,
            "masked.num")
        self._set_iter_val.SetAllowNegative(False)
        self._set_iter_val.SetBounds(1, 99)
        self._set_iter_val.SetFractionWidth(0)
        self._set_iter_val.SetIntegerWidth(2)
        self._set_iter_val.SetValue(10)
        self._set_iter_val.SetLimited(True)
        self._set_iter_val.SetFont(self._program_font)
        angle_sizer.AddMany(
            [curr_power_label, self._curr_angle_val, start_angle_label,
             self._start_angle_val, end_angle_label, self._end_angle_val,
             step_size_label, self._step_size_val, curr_iter_label,
             self._curr_iter_val, set_iter_label, self._set_iter_val])
        angle_panel.SetSizer(angle_sizer)

        # Velocity panel objects
        velocity_panel = wx.Panel(control_panel)
        velocity_sizer = wx.FlexGridSizer(3, 2, 0, 0)
        curr_speed_label = wx.StaticText(
            velocity_panel, -1, "Current Max Speed (\xb0/s): ",
            wx.DefaultPosition, wx.Size(200, 20), wx.ALIGN_RIGHT, 
            "StaticTextNameStr")
        curr_speed_label.SetFont(self._program_font)
        self._curr_speed_val = wx.StaticText(velocity_panel,
                                             -1,
                                             "",
                                             wx.DefaultPosition,
                                             wx.Size(200, 20),
                                             wx.ALIGN_LEFT,
                                             "StaticTextNameStr")
        self._curr_speed_val.SetFont(self._program_font)
        moving_label = wx.StaticText(velocity_panel,
                                     -1,
                                     "Tracking: ",
                                     wx.DefaultPosition,
                                     wx.Size(200, 20),
                                     wx.ALIGN_RIGHT,
                                     "StaticTextNameStr")
        moving_label.SetFont(self._program_font)
        self._moving_val = wx.StaticText(velocity_panel,
                                         -1,
                                         "Resting",
                                         wx.DefaultPosition,
                                         wx.Size(200, 20),
                                         wx.ALIGN_LEFT,
                                         "StaticTextNameStr")
        self._moving_val.SetFont(self._program_font)
        set_speed_label = wx.StaticText(velocity_panel,
                                        -1,
                                        "Max Speed (\xb0/s): ",
                                        wx.DefaultPosition,
                                        wx.Size(200, 20),
                                        wx.ALIGN_RIGHT,
                                        "StaticTextNameStr")
        set_speed_label.SetFont(self._program_font)
        self._set_speed_val = NumCtrl(velocity_panel,
                                      -1,
                                      0,
                                      wx.DefaultPosition,
                                      wx.Size(200, 20),
                                      wx.TE_PROCESS_TAB | wx.TE_PROCESS_ENTER,
                                      wx.DefaultValidator,
                                      "masked.num")
        self._set_speed_val.SetAllowNegative(False)
        self._set_speed_val.SetBounds(0.01, 25)
        self._set_speed_val.SetFractionWidth(2)
        self._set_speed_val.SetIntegerWidth(2)
        self._set_speed_val.SetValue(10)
        self._set_speed_val.SetLimited(True)
        self._set_speed_val.SetFont(self._program_font)
        velocity_sizer.AddMany([curr_speed_label,
                                self._curr_speed_val,
                                moving_label,
                                self._moving_val,
                                set_speed_label,
                                self._set_speed_val])
        velocity_panel.SetSizer(velocity_sizer)

        # Button panel
        button_panel = wx.Panel(control_panel)
        button_sizer = wx.FlexGridSizer(2, 2, 0, 0)
        self._home_button = wx.Button(button_panel,
                                      -1,
                                      "Home Stage",
                                      wx.DefaultPosition,
                                      wx.Size(200, 26),
                                      0,
                                      wx.DefaultValidator,
                                      "ButtonNameStr")
        self._home_button.SetFont(self._program_font)
        self._zero_button = wx.Button(button_panel,
                                      -1,
                                      "Zero Power Meter",
                                      wx.DefaultPosition,
                                      wx.Size(200, 26),
                                      0,
                                      wx.DefaultValidator,
                                      "ButtonNameStr")
        self._zero_button.SetFont(self._program_font)
        self._start_button = wx.Button(button_panel,
                                       -1,
                                       "Start",
                                       wx.DefaultPosition,
                                       wx.Size(200, 26),
                                       0,
                                       wx.DefaultValidator,
                                       "ButtonNameStr")
        self._start_button.SetFont(self._program_font)
        self._start_button.SetForegroundColour(wx.Colour("GREEN"))
        self._stop_button = wx.Button(button_panel,
                                      -1,
                                      "Stop",
                                      wx.DefaultPosition,
                                      wx.Size(200, 26),
                                      0,
                                      wx.DefaultValidator,
                                      "ButtonNameStr")
        self._stop_button.SetFont(self._program_font)
        self._stop_button.SetForegroundColour(wx.Colour("RED"))
        self._stop_button.Disable()
        button_sizer.AddMany([self._home_button,
                              self._zero_button,
                              self._start_button,
                              self._stop_button])
        button_panel.SetSizer(button_sizer)

        # Bind events to the buttons and the serial input
        self._serial_val.Bind(wx.EVT_CHOICE, self.serial_entry)
        self._home_button.Bind(wx.EVT_BUTTON, self.home_press)
        self._zero_button.Bind(wx.EVT_BUTTON, self.zero_press)
        self._start_button.Bind(wx.EVT_BUTTON, self.start_press)
        self._stop_button.Bind(wx.EVT_BUTTON, self.stop_press)

        # Add the objects/panels to the control panel
        control_sizer.Add(title_label,
                          0,
                          wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM,
                          44)
        control_sizer.Add(serial_panel, 0, wx.BOTTOM, 33)
        control_sizer.Add(power_panel, 0, wx.BOTTOM, 32)
        control_sizer.Add(angle_panel, 0, wx.BOTTOM, 32)
        control_sizer.Add(velocity_panel, 0, wx.BOTTOM, 32)
        control_sizer.Add(button_panel, 0, wx.BOTTOM, 0)
        control_panel.SetSizer(control_sizer)

        # Create the blank live plot canvas
        self._live_plt_canvas = FigureCanvasWxAgg(program_panel,
                                                  -1,
                                                  self._live_plt)
        plot_title = "Laser Power (mW) vs. Polarizing Filter Angle (\xb0)"
        self._live_plt_axes.set_title(plot_title)
        # self._live_plt_axes.set_ylabel("Power (mW)")
        # self._live_plt_axes.set_xlabel("Angle (\xb0)")
        # self._live_plt_axes.grid(True)

        # Add the control panel and live plot to the main program panel
        program_sizer.Add(control_panel)
        program_sizer.Add(self._live_plt_canvas, 1, wx.EXPAND)

        # Set program panel sizer to display control and graph panels
        program_panel.SetSizer(program_sizer)

    def disable_ui(self):
        """Disable the inputs of the GUI, but enable the stop button."""
        self._serial_val.Disable()
        self._start_angle_val.Disable()
        self._end_angle_val.Disable()
        self._step_size_val.Disable()
        self._set_iter_val.Disable()
        self._set_speed_val.Disable()
        self._home_button.Disable()
        self._zero_button.Disable()
        self._start_button.Disable()
        self._stop_button.Enable()
        self._is_disabled = True

    def enable_ui(self):
        """Enable the inputs of the GUI, but disable the stop button."""
        self._serial_val.Enable()
        self._start_angle_val.Enable()
        self._end_angle_val.Enable()
        self._step_size_val.Enable()
        self._set_iter_val.Enable()
        self._set_speed_val.Enable()
        self._home_button.Enable()
        self._zero_button.Enable()
        self._start_button.Enable()
        self._stop_button.Disable()
        self._is_disabled = False

    def serial_entry(self, evt):
        """Intended for override by subclass, this is bound to the event
        on data entry into the serial number field.

        Parameters
        ----------
        evt : wx.Event
            The event which called this method.

        """
        print(self.get_serial())
        evt.Skip()

    def home_press(self, evt):
        """Intended for override by subcless, this is bound to the event
        on pressing the Home Stage button.
        Parameters
        ----------
        evt : wx.Event
            The event which called this method.

        """
        evt.Skip()

    def zero_press(self, evt):
        """Intended for override by subclass, this is bound to the event
        on pressing the Zero Power Meter button.

        Parameters
        ----------
        evt : wx.Event
            The event which called this method.

        """
        evt.Skip()

    def start_press(self, evt):
        """Intended for override by subclass, this is bound to the event
        on pressing the Start button.

        Parameters
        ----------
        evt : wx.Event
            The event which called this method.

        """
        evt.Skip()

    def stop_press(self, evt):
        """Intended for override by subclass, this is bound to the event
        on pressing the Stop button.

        Parameters
        ----------
        evt : wx.Event
            The event which called this method.

        """
        evt.Skip()

    def get_serial(self):
        """Return the value of the serial number input.

        Returns
        -------
        int
            The serial number input value.

        """
        serials = {
            0: 83843569, 
            1: 83846179,
            2: 83845569
        }
        return serials[self._serial_val.GetCurrentSelection()]

    def set_pow_val(self, power):
        """Set the value of the current power display.

        Parameters
        ----------
        power
            The power value to be displayed.

        """
        self._curr_pow_val.SetLabel(str(power))

    def set_curr_angle_val(self, angle):
        """Set the value of the current angle display.

        Parameters
        ----------
        angle
            The angle to be displayed.

        """
        self._curr_angle_val.SetLabel(str(angle))

    def get_start_angle(self):
        """Return the value of the start angle input.

        Returns
        -------
        float
            The start angle input value.

        """
        return self._start_angle_val.GetValue()

    def get_end_angle(self):
        """Return the value of the end angle input.

        Returns
        -------
        float
            The end angle input value.

        """
        return self._end_angle_val.GetValue()

    def get_step_size(self):
        """Return the value of the step size input.

        Returns
        -------
        float
            The step size input value.

        """
        return self._step_size_val.GetValue()

    def set_curr_iter(self, iteration):
        """Set the value of the current iteration display.

        If the GUI is currently disabled, "Not currently testing!"
        will be displayed instead of `iteration`.

        Parameters
        ----------
        iteration
            The iteration value to be displayed.

        """
        if self._is_disabled is False:
            self._curr_iter_val.SetLabel("Not currently testing!")
        else:
            self._curr_iter_val.SetLabel(str(iteration))

    def get_iter_val(self):
        """Return the value of the number of iterations input.

        Returns
        -------
        int
            The number of iterations input value.

        """
        return self._set_iter_val.GetValue()

    def set_speed(self, speed):
        """Set the value of the current maximum speed.

        Parameters
        ----------
        speed
            The speed to be displayed.

        """
        self._curr_speed_val.SetLabel(str(speed))

    def set_moving(self):
        """Set the value of whether or not the motor is moving."""
        if self._is_disabled is True:
            self._moving_val.SetLabel("Tracking")
        else:
            self._moving_val.SetLabel("Resting")

    def get_speed(self):
        """Return the value of the maximum speed input.

        Returns
        -------
        float
            The value of the maximum speed input.

        """
        return self._set_speed_val.GetValue()

    def clear_plt(self):
        """Clears the live plot."""
        self._live_plt_axes.clear()
        plot_title = "Laser Power (mW) vs. Polarizing Filter Angle (\xb0)"
        self._live_plt_axes.set_title(plot_title)
        # self._live_plt_axes.set_ylabel("Power (mW)")
        # self._live_plt_axes.set_xlabel("Angle (\xb0)")
        # self._live_plt_axes.grid(True)

    def old_update_plt(self, data):
        """Updates the plot using 'data' for x and y values.

        Parameters
        ----------
        data : list of tuple of float
            The data set of [x, y] tuples to be plotted.

        """
        x_data = np.array([])
        y_data = np.array([])
        for item in data:
            x_data = np.append(x_data, [item[0]])
            y_data = np.append(y_data, [item[1]*1000])
        min_power = y_data.min() - 50
        max_power = y_data.max() + 50
        self._live_plt_axes.axis([self.get_start_angle(),
                                  self.get_end_angle(),
                                  min_power,
                                  max_power])
        self._live_plt_axes.plot(x_data[-1], y_data[-1], 'rx')
        self._live_plt_canvas.draw()
        
    def update_plt(self, data):
        """Updates the plot using 'data' for angle and r values.

        Parameters
        ----------
        data : list of tuple of float
            The data set of [angle, r] tuples to be plotted.

        """
        angle_data = np.array([])
        r_data = np.array([])
        for item in data:
            angle_data = np.append(angle_data, [item[0]])
            r_data = np.append(r_data, [item[1]*1000])
        min_power = r_data.min() - 50
        max_power = r_data.max() + 50
        self._live_plt_axes.set_ylim([min_power, max_power])
        self._live_plt_axes.plot(x_data[-1], y_data[-1], 'rx')
        self._live_plt_canvas.draw()

if __name__ == '__main__':
    app = wx.App()
    GUI = PolarizationExperimentGUI()
    app.MainLoop()
