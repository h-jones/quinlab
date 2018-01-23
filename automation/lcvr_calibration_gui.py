import csv
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
from meadowlark_d3050_controller import MeadowlarkD3050Controller
from newport_1830c import Newport1830C
import numpy as np
from time import sleep
from time import strftime
import _thread
import visa
import wx
from wx.lib.masked import NumCtrl
rm = visa.ResourceManager()


class LCVRCalibrationGUI(wx.Frame):

    def __init__(self, parent=None, title="LCVR Calibration"):
        super(LCVRCalibrationGUI, self).__init__(
            parent, title=title, size=(815, 520),
            style= wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        self._max = "Not yet tested."
        self._min = "Not yet tested."
        self._pm_init = False
        self._lcvr_init = False
        self._data_set = []
        self._filename = "LCVR Calibration.csv"
        self._kill_calibration = True
        self._saved_data = True

        # make panel for frame
        overall_panel = wx.Panel(self)
        overall_sizer = wx.GridBagSizer()
        
        # make panel for top
        top_panel = wx.Panel(overall_panel)
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # make panel for main stuff
        main_panel = wx.Panel(top_panel)
        main_sizer = wx.FlexGridSizer(11, 2, 0, 0)

        newport_label = wx.StaticText(
            main_panel, label="Newport GPIB Port: ",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._newport_val = NumCtrl(
            main_panel, size=(140, 20), style=wx.TE_PROCESS_ENTER)
        self._newport_val.SetAllowNegative(False)
        self._newport_val.SetBounds(1, 99)
        self._newport_val.SetFractionWidth(0)
        self._newport_val.SetIntegerWidth(2)
        self._newport_val.SetValue(4)
        self._newport_val.SetLimitOnFieldChange(True)

        meadowlark_label = wx.StaticText(
            main_panel, label="Meadowlark COM Port: ",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._meadowlark_val = NumCtrl(
            main_panel, size=(140, 20), style=wx.TE_PROCESS_ENTER)
        self._meadowlark_val.SetAllowNegative(False)
        self._meadowlark_val.SetBounds(1, 99)
        self._meadowlark_val.SetFractionWidth(0)
        self._meadowlark_val.SetIntegerWidth(2)
        self._meadowlark_val.SetValue(6)
        self._meadowlark_val.SetLimitOnFieldChange(True)

        meadowlark_chan = wx.StaticText(
            main_panel, label="Meadowlark Channel: ",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._meadowlark_ch =  wx.Choice(
            main_panel, size=(140, 20), 
            choices=["1", "2", "3", "4"])

        laser_label = wx.StaticText(
            main_panel, label="Laser Wavelength (nm): ",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._laser_lambda = NumCtrl(
            main_panel, size=(140, 20), style=wx.TE_PROCESS_ENTER)
        self._laser_lambda.SetAllowNegative(False)
        self._laser_lambda.SetBounds(400, 1100)
        self._laser_lambda.SetFractionWidth(0)
        self._laser_lambda.SetIntegerWidth(4)
        self._laser_lambda.SetValue(780)
        self._laser_lambda.SetLimitOnFieldChange(True)
        
        start_volt_label = wx.StaticText(
            main_panel, label="Start Voltage (V):",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._start_volt_val = NumCtrl(
            main_panel, size=(140, 20), style=wx.TE_PROCESS_ENTER)
        self._start_volt_val.SetAllowNegative(False)
        self._start_volt_val.SetBounds(0, 10)
        self._start_volt_val.SetFractionWidth(2)
        self._start_volt_val.SetIntegerWidth(2)
        self._start_volt_val.SetValue(10)
        self._start_volt_val.SetLimitOnFieldChange(True)
        end_volt_label = wx.StaticText(
            main_panel, label="End Voltage (V):",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._end_volt_val = NumCtrl(
            main_panel, size=(150, 20), style=wx.TE_PROCESS_ENTER)
        self._end_volt_val.SetAllowNegative(False)
        self._end_volt_val.SetBounds(0, 10)
        self._end_volt_val.SetFractionWidth(2)
        self._end_volt_val.SetIntegerWidth(2)
        self._end_volt_val.SetValue(0)
        self._end_volt_val.SetLimitOnFieldChange(True)
        step_volt_label = wx.StaticText(
            main_panel, label="Absolute Step Voltage (V):",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._step_volt_val = NumCtrl(
            main_panel, size=(140, 20), style=wx.TE_PROCESS_ENTER)
        self._step_volt_val.SetAllowNegative(False)
        self._step_volt_val.SetBounds(0, 10)
        self._step_volt_val.SetFractionWidth(2)
        self._step_volt_val.SetIntegerWidth(2)
        self._step_volt_val.SetValue(0.1)
        self._step_volt_val.SetLimitOnFieldChange(True)

        self._run_button = wx.Button(
            main_panel, label="Run Calibration", size=(140, 20))
        self._run_button.SetForegroundColour(wx.Colour("GREEN"))

        self._stop_button = wx.Button(
            main_panel, label="Stop Calibration", size=(140, 20))
        self._stop_button.SetForegroundColour(wx.Colour("RED"))
        self._stop_button.Disable()

        max_label = wx.StaticText(
            main_panel, label="Max Power Setting (V): ",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._max_value = wx.StaticText(
            main_panel, label=self._max, size=(140, 20), style=wx.ALIGN_LEFT)
        min_label = wx.StaticText(
            main_panel, label="Min Power Setting (V): ",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._min_value = wx.StaticText(
            main_panel, label=self._min, size=(140, 20), style=wx.ALIGN_LEFT)

        self._newport_val.Bind(wx.EVT_KILL_FOCUS, self._newport_entry)
        self._meadowlark_val.Bind(wx.EVT_KILL_FOCUS, self._meadowlark_entry)
        self._laser_lambda.Bind(wx.EVT_KILL_FOCUS, self._lambda_entry)

        self._save_button = wx.Button(
            main_panel, label="Save Values", size=(140, 20))
        self._load_button = wx.Button(
            main_panel, label="Load Values", size=(140, 20))

        self._save_button.Bind(wx.EVT_BUTTON, self._save_press)
        self._load_button.Bind(wx.EVT_BUTTON, self._load_press)
        self._run_button.Bind(wx.EVT_BUTTON, self._run_press)
        self._stop_button.Bind(wx.EVT_BUTTON, self._stop_press)

        main_sizer.AddMany(
            [newport_label, self._newport_val, 
             meadowlark_label, self._meadowlark_val,
             meadowlark_chan, self._meadowlark_ch,
             laser_label, self._laser_lambda,
             start_volt_label, self._start_volt_val,
             end_volt_label, self._end_volt_val,
             step_volt_label, self._step_volt_val,
             self._run_button, self._stop_button,
             max_label, self._max_value,
             min_label, self._min_value,
             self._save_button, self._load_button])
        main_panel.SetSizer(main_sizer)
        self.Bind(wx.EVT_CLOSE, self._on_close)

        self._output_display = wx.TextCtrl(
            top_panel, size=(280, 180),
            style=wx.TE_MULTILINE | wx.TE_READONLY)

        top_sizer.Add(main_panel, 0, wx.ALL, 10)
        top_sizer.Add(self._output_display, 0, wx.ALL, 10)
        top_panel.SetSizer(top_sizer)
        
        plt_panel = wx.Panel(overall_panel, size=(500, 500))
        plt_sizer = wx.BoxSizer()
        self._live_plt = Figure()
        self._live_plt.set_facecolor('w')
        axes_dim = [0.125, 0.125, 0.8, 0.8]
        self._live_plt_axes = self._live_plt.add_axes(axes_dim)
        self._live_plt_canvas = FigureCanvasWxAgg(
            plt_panel, -1, self._live_plt)
        plot_title = "Laser Power (mW) vs. LCVR Voltage (V)"
        self._live_plt_axes.set_title(plot_title)
        self._live_plt_axes.set_ylabel("Power (mW)")
        self._live_plt_axes.set_xlabel("Voltage (V)")
        self._live_plt_axes.grid(True)
        plt_sizer.Add(self._live_plt_canvas)
        plt_panel.SetSizer(plt_sizer)
        
        copyright_str = "\u00a9 2016 QuIN Lab "
        copyright_str += "Developed by Hayden Jones"
        copyright = wx.StaticText(
            overall_panel, label=copyright_str, style=wx.ALIGN_RIGHT)
        
        overall_sizer.Add(top_panel, (0, 0))
        overall_sizer.Add(plt_panel, (0, 1), (2, 1))
        overall_sizer.Add(copyright, (1, 0))
        overall_panel.SetSizer(overall_sizer)
        overall_panel.Layout()
        self.Show()

    def _on_close(self, evt):
        if self._lcvr_init is True:
            self._lcvr.close()
        if self._pm_init is True:
            self._pm.close()
        if self._saved_data is False:
            if self._dataloss_warn() == wx.ID_NO:
                return
        evt.Skip()

    def disable_ui(self):
        self._newport_val.Disable()
        self._meadowlark_val.Disable()
        self._meadowlark_ch.Disable()
        self._laser_lambda.Disable()
        self._run_button.Disable()
        self._stop_button.Enable()
        self._save_button.Disable()
        self._load_button.Disable()

    def enable_ui(self):
        self._newport_val.Enable()
        self._meadowlark_val.Enable()
        self._meadowlark_ch.Enable()
        self._laser_lambda.Enable()
        self._run_button.Enable()
        self._stop_button.Disable()
        self._save_button.Enable()
        self._load_button.Enable()

    def get_pm_addr(self):
        return self._newport_val.GetValue()

    def get_lcvr_addr(self):
        return self._meadowlark_val.GetValue()

    def get_lcvr_ch(self):
        channels = {
            0: 1,
            1: 2,
            2: 3,
            3: 4
        }
        return channels[self._meadowlark_ch.GetCurrentSelection()]

    def get_wavelength(self):
        return self._laser_lambda.GetValue()
        
    def get_start_volt(self):
        return self._start_volt_val.GetValue()
        
    def get_end_volt(self):
        return self._end_volt_val.GetValue()
        
    def get_step_volt(self):
        return self._step_volt_val.GetValue()

    def get_max(self):
        return self._max

    def get_min(self):
        return self._min

    def set_max(self):
        if self._max == self._min:
            return
        self._max_value.SetLabel(str(self._max))

    def set_min(self):
        if self._min == self._max:
            return
        self._min_value.SetLabel(str(self._min))

    def _invalid_pm_warn(self):
        warning_message = "Invalid Power Meter Address/Connection!"
        warning = wx.GenericMessageDialog(None,
                                          warning_message,
                                          "Warning!",
                                          wx.OK,
                                          wx.DefaultPosition)
        warning.ShowModal()
        warning.Destroy()

    def _invalid_lcvr_warn(self):
        warning_message = "Invalid LCVR Controller Address/Connection!"
        warning = wx.GenericMessageDialog(None,
                                          warning_message,
                                          "Warning!",
                                          wx.OK,
                                          wx.DefaultPosition)
        warning.ShowModal()
        warning.Destroy()

    def _overwrite_warn(self):
        warning_message = "Do you want to overwrite previous calibration?"
        warning = wx.GenericMessageDialog(None,
                                          warning_message,
                                          "Warning!",
                                          wx.YES_NO,
                                          wx.DefaultPosition)
        result = warning.ShowModal()
        warning.Destroy()
        return result
        
    def _dataloss_warn(self):
        warning_message = "Do you want to exit without saving data?"
        warning = wx.GenericMessageDialog(None,
                                          warning_message,
                                          "Warning!",
                                          wx.YES_NO,
                                          wx.DefaultPosition)
        result = warning.ShowModal()
        warning.Destroy()
        return result

    def _newport_entry(self, evt):
    # change line 308 to turn off attenuator
        if self._pm_init is True:
            return
        try:
            self._pm = Newport1830C(self.get_pm_addr())
        except:
            self._invalid_pm_warn()
            return
        self._pm_init = True
        self._pm.attenuator_on()
        evt.Skip()

    def _meadowlark_entry(self, evt):
        if self._lcvr_init is True:
            return
        try:
            com_port = self._meadowlark_val.GetValue()
            self._lcvr = MeadowlarkD3050Controller(com_port)
        except:
            self._invalid_lcvr_warn()
            evt.Skip()
            return
        self._lcvr_init = True
        evt.Skip()

    def _lambda_entry(self, evt):
        if self._laser_lambda.IsInBounds() is False:
            return
        if self._pm_init is True:
            self._pm.set_wavelength(self.get_wavelength())
        evt.Skip()

    def _run_press(self, evt):
        if self._data_set != []:
            if self._overwrite_warn() == wx.ID_NO:
                return
        self._meadowlark_entry(wx.EVT_BUTTON)
        self._newport_entry(wx.EVT_BUTTON)
        if self._pm_init is False:
            return
        if self._lcvr_init is False:
            return
        self.disable_ui()
        self._kill_calibration = False
        self._saved_data = False
        self._data_set = []
        self._output_display.Clear()
        _thread.start_new_thread(self._calibration,
                                 (self.get_lcvr_ch(),))

    def _stop_press(self, evt):
        self.enable_ui()
        self._kill_calibration = True

    def _save_press(self, evt):
        file_type = "Comma Separated Values file (*.csv)|*.csv"
        save_dialog = wx.FileDialog(self,
                                    "Save calibration data as...",
                                    "",
                                    self._filename,
                                    file_type,
                                    wx.FD_SAVE)
        if save_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self._filename = save_dialog.GetPath()
        save_dialog.Destroy()
        with open(self._filename, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(["Date:", strftime("_%Y_%m_%d_%H-%M-%S")])
            writer.writerow(["Wavelength:", self.get_wavelength()])
            writer.writerows(self._data_set)
        self._saved_data = True

    def _load_press(self, evt):
        file_type = "Comma Separated Values file (*.csv)|*.csv"
        open_dialog = wx.FileDialog(self,
                                    "Open calibration data...",
                                    "",
                                    self._filename,
                                    file_type,
                                    wx.FD_OPEN)
        if open_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self._filename = open_dialog.GetPath()
        open_dialog.Destroy()
        with open(self._filename, 'r') as f:
            reader = csv.reader(f)
            reader = list(reader)
            self._laser_lambda.SetValue(int(reader[1][1]))
            self._data_set = reader[2:]
        self._data_set = [[float(x[0]), float(x[1])] for x in self._data_set]
        self._start_volt_val.SetValue(self._data_set[0][0])
        self._end_volt_val.SetValue(self._data_set[-1][0])
        self._step_volt_val.SetValue(abs(self._data_set[1][0] 
                                         - self._data_set[0][0]))
        for item in self._data_set:
            v = round(item[0], 3)
            p = round(item[1], 6)
            data_string = "Voltage (V):{0} Power (W):{1}\n".format(v, p)
            self._output_display.AppendText(data_string)
        self._analyze()
        self.set_max()
        self.set_min()
        self._update_plt(self._data_set)

    def _clear_plt(self):
        self._live_plt_axes.clear()
        plot_title = "Laser Power (mW) vs. LCVR Voltage (V)"
        self._live_plt_axes.set_title(plot_title)
        self._live_plt_axes.set_ylabel("Power (mW)")
        self._live_plt_axes.set_xlabel("Voltage (V)")
        self._live_plt_axes.grid(True)

    def _update_plt(self, data):
        self._clear_plt()
        x_data = np.array([])
        y_data = np.array([])
        for item in data:
            x_data = np.append(x_data, [item[0]])
            y_data = np.append(y_data, [item[1]*1000])
        min_power = y_data.min() - y_data.min()/20
        max_power = y_data.max() + y_data.max()/100
        start_v = self.get_start_volt()
        end_v = self.get_end_volt()
        if start_v > end_v:
            temp = end_v
            end_v = start_v
            start_v = temp
        self._live_plt_axes.axis(
            [start_v, end_v, min_power, max_power])
        self._live_plt_axes.plot(x_data, y_data, 'rx')
        self._live_plt_canvas.draw()
        
    def _calibration(self, channel):
        start_v = self.get_start_volt()
        end_v = self.get_end_volt()
        if start_v > end_v:
            step = -self.get_step_volt()
        else:
            step = self.get_step_volt()
        for i in range(int(start_v*1000), int((end_v+0.01)*1000), int(step*1000)):
            if self._kill_calibration is True:
                break
            v = i/1000
            self._lcvr.set_voltage(channel, v)
            sleep(0.1)
            p = self._pm.get_power()
            self._data_set.append([v, p])
            v = round(v, 3)
            p = round(p, 6)
            data_string = "Voltage (V):{0} Power (W):{1}\n".format(v, p)
            wx.CallAfter(self._output_display.AppendText, data_string)
            wx.CallAfter(self._update_plt, self._data_set)
        wx.CallAfter(self._stop_press, wx.EVT_BUTTON)
        wx.CallAfter(self._analyze)

    def _analyze(self):
        # Uses median absolute deviation (MAD) to remove outliers
        pow_arr = np.array([x[1] for x in self._data_set])
        d = np.abs(pow_arr - np.median(pow_arr))
        mdev = np.median(d)
        s = d/mdev if mdev else 0
        pow_arr = list(pow_arr[s<20])
        min_index = pow_arr.index(min(pow_arr))
        max_index = pow_arr.index(max(pow_arr))
        self._min = self._data_set[min_index][0]
        self._max = self._data_set[max_index][0]
        self.set_max()
        self.set_min()

if __name__ == '__main__':
    app = wx.App()
    GUI = LCVRCalibrationGUI()
    app.MainLoop()
