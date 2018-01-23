import wx
from wx.lib.masked import NumCtrl
from meadowlark_d3050_controller import MeadowlarkD3050Controller
from ccd_panel import CCDPanel
import _thread
from time import sleep


class PowerDependentGUI(wx.Frame):

    def __init__(self,
                 parent=None,
                 title="Power Dependent Imaging"):
        super(PowerDependentGUI, self).__init__(parent,
                                                title=title,
                                                size=(1000, 1000))
        self._filedir = ""
        self._truefilename = ""
        self._filename = ""
        self._lcvr_init = False

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        input_panel = wx.Panel(main_panel)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        common_panel = wx.Panel(input_panel)
        common_sizer = wx.FlexGridSizer(11, 2, 0, 0)
        lcvr_label = wx.StaticText(common_panel,
                                   -1,
                                   "LCVR COM Port: ",
                                   wx.DefaultPosition,
                                   wx.Size(125, 20),
                                   wx.ALIGN_RIGHT,
                                   "StaticTextNameStr")
        self._lcvr_val = NumCtrl(common_panel,
                                 -1,
                                 0,
                                 wx.DefaultPosition,
                                 wx.Size(125, 20),
                                 wx.TE_PROCESS_TAB
                                 | wx.TE_PROCESS_ENTER,
                                 wx.DefaultValidator,
                                 "masked.num")
        self._lcvr_val.SetAllowNegative(False)
        self._lcvr_val.SetBounds(1, 99)
        self._lcvr_val.SetFractionWidth(0)
        self._lcvr_val.SetIntegerWidth(2)
        self._lcvr_val.SetValue(6)
        self._lcvr_val.SetLimitOnFieldChange(True)
        self._lcvr_val.Bind(wx.lib.masked.EVT_NUM, self._lcvr_entry)
        lcvr_chan = wx.StaticText(common_panel,
                                  -1,
                                  "LCVR Channel: ",
                                  wx.DefaultPosition,
                                  wx.Size(125, 20),
                                  wx.ALIGN_RIGHT,
                                  "StaticTextNameStr")
        self._lcvr_ch = NumCtrl(common_panel,
                                -1,
                                0,
                                wx.DefaultPosition,
                                wx.Size(125, 20),
                                wx.TE_PROCESS_TAB
                                | wx.TE_PROCESS_ENTER,
                                wx.DefaultValidator,
                                "masked.num")
        self._lcvr_ch.SetAllowNegative(False)
        self._lcvr_ch.SetBounds(1, 4)
        self._lcvr_ch.SetFractionWidth(0)
        self._lcvr_ch.SetIntegerWidth(1)
        self._lcvr_ch.SetValue(1)
        self._lcvr_ch.SetLimitOnFieldChange(True)
        wavelength_label = wx.StaticText(common_panel,
                                     -1,
                                     "Laser Wavelength (nm):",
                                     wx.DefaultPosition,
                                     wx.Size(150, 20),
                                     wx.ALIGN_RIGHT,
                                     "StaticTextNameStr")
        self._wavelength_val = NumCtrl(common_panel,
                                       -1,
                                       0,
                                       wx.DefaultPosition,
                                       wx.Size(150, 20),
                                       wx.TE_PROCESS_TAB
                                       | wx.TE_PROCESS_ENTER,
                                       wx.DefaultValidator,
                                     "masked.num")
        self._wavelength_val.SetAllowNegative(False)
        self._wavelength_val.SetBounds(400, 1100)
        self._wavelength_val.SetFractionWidth(0)
        self._wavelength_val.SetIntegerWidth(4)
        self._wavelength_val.SetValue(780)
        self._wavelength_val.SetLimitOnFieldChange(True)
        pow_label = wx.StaticText(common_panel,
                                     -1,
                                     "Laser Power (mW):",
                                     wx.DefaultPosition,
                                     wx.Size(150, 20),
                                     wx.ALIGN_RIGHT,
                                     "StaticTextNameStr")
        self._pow_val = NumCtrl(common_panel,
                                -1,
                                0,
                                wx.DefaultPosition,
                                wx.Size(150, 20),
                                wx.TE_PROCESS_TAB
                                | wx.TE_PROCESS_ENTER,
                                wx.DefaultValidator,
                                     "masked.num")
        self._pow_val.SetAllowNegative(False)
        self._pow_val.SetBounds(0, 1000)
        self._pow_val.SetFractionWidth(2)
        self._pow_val.SetIntegerWidth(4)
        self._pow_val.SetValue(0)
        self._pow_val.SetLimitOnFieldChange(True)
        od_label = wx.StaticText(common_panel,
                                  -1,
                                  "OD:",
                                  wx.DefaultPosition,
                                  wx.Size(150, 20),
                                  wx.ALIGN_RIGHT,
                                  "StaticTextNameStr")
        self._od_val = NumCtrl(common_panel,
                                -1,
                                0,
                                wx.DefaultPosition,
                                wx.Size(150, 20),
                                wx.TE_PROCESS_TAB
                                | wx.TE_PROCESS_ENTER,
                                wx.DefaultValidator,
                                "masked.num")
        self._od_val.SetAllowNegative(False)
        self._od_val.SetBounds(0, 100)
        self._od_val.SetFractionWidth(0)
        self._od_val.SetIntegerWidth(4)
        self._od_val.SetValue(0)
        self._od_val.SetLimitOnFieldChange(True)
        start_volt_label = wx.StaticText(common_panel,
                                       -1,
                                       "Start Voltage (V):",
                                       wx.DefaultPosition,
                                       wx.Size(150, 20),
                                       wx.ALIGN_RIGHT,
                                       "StaticTextNameStr")
        self._start_volt_val = NumCtrl(common_panel,
                                -1,
                                0,
                                wx.DefaultPosition,
                                wx.Size(150, 20),
                                wx.TE_PROCESS_TAB
                                | wx.TE_PROCESS_ENTER,
                                wx.DefaultValidator,
                                "masked.num")
        self._start_volt_val.SetAllowNegative(False)
        self._start_volt_val.SetBounds(0, 10)
        self._start_volt_val.SetFractionWidth(2)
        self._start_volt_val.SetIntegerWidth(2)
        self._start_volt_val.SetValue(0)
        self._start_volt_val.SetLimitOnFieldChange(True)
        end_volt_label = wx.StaticText(common_panel,
                                       -1,
                                       "End Voltage (V):",
                                       wx.DefaultPosition,
                                       wx.Size(150, 20),
                                       wx.ALIGN_RIGHT,
                                       "StaticTextNameStr")
        self._end_volt_val = NumCtrl(common_panel,
                                     -1,
                                     0,
                                     wx.DefaultPosition,
                                     wx.Size(150, 20),
                                     wx.TE_PROCESS_TAB
                                     | wx.TE_PROCESS_ENTER,
                                     wx.DefaultValidator,
                                     "masked.num")
        self._end_volt_val.SetAllowNegative(False)
        self._end_volt_val.SetBounds(0, 10)
        self._end_volt_val.SetFractionWidth(2)
        self._end_volt_val.SetIntegerWidth(2)
        self._end_volt_val.SetValue(10)
        self._end_volt_val.SetLimitOnFieldChange(True)
        step_volt_label = wx.StaticText(common_panel,
                                       -1,
                                       "Absolute Step Voltage (V):",
                                       wx.DefaultPosition,
                                       wx.Size(150, 20),
                                       wx.ALIGN_RIGHT,
                                       "StaticTextNameStr")
        self._step_volt_val = NumCtrl(common_panel,
                                     -1,
                                     0,
                                     wx.DefaultPosition,
                                     wx.Size(150, 20),
                                     wx.TE_PROCESS_TAB
                                     | wx.TE_PROCESS_ENTER,
                                     wx.DefaultValidator,
                                     "masked.num")
        self._step_volt_val.SetAllowNegative(False)
        self._step_volt_val.SetBounds(0, 10)
        self._step_volt_val.SetFractionWidth(2)
        self._step_volt_val.SetIntegerWidth(2)
        self._step_volt_val.SetValue(0.1)
        self._step_volt_val.SetLimitOnFieldChange(True)
        self._dir_button = wx.Button(common_panel,
                                    -1,
                                    "Choose Save Location",
                                    wx.DefaultPosition,
                                    wx.Size(150, 20),
                                    0,
                                    wx.DefaultValidator,
                                      "ButtonNameStr")
        self._file_button = wx.Button(common_panel,
                                    -1,
                                    "Choose Save Filename",
                                    wx.DefaultPosition,
                                    wx.Size(150, 20),
                                    0,
                                    wx.DefaultValidator,
                                      "ButtonNameStr")
        self._go_button = wx.Button(common_panel,
                                    -1,
                                    "Start",
                                    wx.DefaultPosition,
                                    wx.Size(150, 20),
                                    0,
                                    wx.DefaultValidator,
                                      "ButtonNameStr")
        self._stop_button = wx.Button(common_panel,
                                    -1,
                                    "Stop",
                                    wx.DefaultPosition,
                                      wx.Size(150, 20),
                                    0,
                                    wx.DefaultValidator,
                                      "ButtonNameStr")

        self._resume_button = wx.Button(common_panel,
                                    -1,
                                    "Resume",
                                    wx.DefaultPosition,
                                    wx.Size(150, 20),
                                    0,
                                    wx.DefaultValidator,
                                      "ButtonNameStr")

        self._pause_button = wx.Button(common_panel,
                                    -1,
                                    "Pause",
                                    wx.DefaultPosition,
                                    wx.Size(150, 20),
                                    0,
                                    wx.DefaultValidator,
                                      "ButtonNameStr")
        self._dir_button.Bind(wx.EVT_BUTTON, self._dir_select)
        self._file_button.Bind(wx.EVT_BUTTON, self._file_select)
        self._go_button.Bind(wx.EVT_BUTTON, self._go)
        self._stop_button.Bind(wx.EVT_BUTTON, self._stop)
        self._resume_button.Bind(wx.EVT_BUTTON, self._resume)
        self._pause_button.Bind(wx.EVT_BUTTON, self._pause)
        common_sizer.AddMany([lcvr_label,
                              self._lcvr_val,
                              lcvr_chan,
                              self._lcvr_ch,
                              wavelength_label,
                              self._wavelength_val,
                              pow_label,
                              self._pow_val,
                              od_label,
                              self._od_val,
                              start_volt_label,
                              self._start_volt_val,
                              end_volt_label,
                              self._end_volt_val,
                              step_volt_label,
                              self._step_volt_val,
                              self._dir_button,
                              self._file_button,
                              self._go_button,
                              self._stop_button,
                              self._resume_button,
                              self._pause_button])
        common_panel.SetSizer(common_sizer)
        self._stop_button.Disable()
        self._pause_button.Disable()
        self._resume_button.Disable()

        input_sizer.Add(common_panel, 0, wx.ALL, 10)

        input_panel.SetSizer(input_sizer)

        self._ccd = CCDPanel("", "", title, main_panel)

        copyright_str = "\u00a9 2016 QuIN Lab"
        copyright_str += "Developed by Hayden Jones"
        copyright_text = wx.StaticText(
            main_panel, label=copyright_str)

        main_sizer.Add(input_panel, 0, wx.ALL, 0)
        main_sizer.Add(self._ccd, 0, wx.ALL, 0)
        main_sizer.Add(copyright_text, 0, wx.ALL, 0)

        main_panel.SetSizer(main_sizer)

        self.Bind(wx.EVT_CLOSE, self._on_close)

        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE
                            ^ wx.RESIZE_BORDER
                            ^ wx.MAXIMIZE_BOX)
        self.Show()

    def _on_close(self, evt):
        if self._lcvr_init is True:
            self._lcvr.close()
        evt.Skip()

    def disable_ui(self):
        self._lcvr_val.Disable()
        self._lcvr_ch.Disable()
        self._wavelength_val.Disable()
        self._pow_val.Disable()
        self._od_val.Disable()
        self._start_volt_val.Disable()
        self._end_volt_val.Disable()
        self._step_volt_val.Disable()
        self._dir_button.Disable()
        self._file_button.Disable()
        self._go_button.Disable()
        self._stop_button.Enable()
        self._resume_button.Disable()
        self._pause_button.Enable()

    def enable_ui(self):
        self._lcvr_val.Enable()
        self._lcvr_ch.Enable()
        self._wavelength_val.Enable()
        self._pow_val.Enable()
        self._od_val.Enable()
        self._start_volt_val.Enable()
        self._end_volt_val.Enable()
        self._step_volt_val.Enable()
        self._dir_button.Enable()
        self._file_button.Enable()
        self._go_button.Enable()
        self._stop_button.Disable()
        self._resume_button.Disable()
        self._pause_button.Disable()

    def get_od(self):
        return self._od_val.GetValue()

    def get_wavelength(self):
        return self._wavelength_val.GetValue()

    def get_power(self):
        return self._pow_val.GetValue()

    def get_start_volt(self):
        return self._start_volt_val.GetValue()

    def get_end_volt(self):
        return self._end_volt_val.GetValue()

    def get_step_volt(self):
        return self._step_volt_val.GetValue()

    def get_lcvr_addr(self):
        return self._lcvr_ch.GetValue()

    def _invalid_lcvr_warn(self):
        warning_message = "Invalid LCVR Controller Address/Connection!"
        warning = wx.GenericMessageDialog(None,
                                          warning_message,
                                          "Warning!",
                                          wx.OK,
                                          wx.DefaultPosition)
        warning.ShowModal()
        warning.Destroy()

    def _lcvr_entry(self, evt):
        if self._lcvr_init is True or self.get_lcvr_addr() < 1:
            return
        try:
            com_port = self._lcvr_val.GetValue()
            self._lcvr = MeadowlarkD3050Controller(com_port)
        except:
            self._invalid_lcvr_warn()
            return
        self._lcvr_init = True

    def _set_filename(self):
        self._filename = self._truefilename
        self._filename += "_OD" + str(self.get_od())
        self._filename += "_" + str(self.get_wavelength()) + "nm"
        self._filename += "_" + str(self.get_power()) + "mW"

    def _dir_select(self, evt):
        dir_dialog = wx.DirDialog(self,
                                    "Choose file save directory...",
                                    "",
                                  wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dir_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self._filedir = dir_dialog.GetPath() + "\\"
        dir_dialog.Destroy()

    def _file_select(self, evt):
        file_dialog = wx.TextEntryDialog(self,
                                         "Enter the file name...",
                                         "File Name Selection Dialog",
                                         self._truefilename)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self._truefilename = file_dialog.GetValue()
        file_dialog.Destroy()

    def _go(self, evt):
        if self._lcvr_init is False:
            return
        self.disable_ui()
        self._ccd.open_xcap()
        self._kill_automation = False
        self._pause_automation = False
        _thread.start_new_thread(self._automation, (self.get_lcvr_addr(),))

    def _stop(self, evt):
        self._kill_automation = True
        self._pause_automation = False
        self._ccd.close_xcap()
        self.enable_ui()

    def _resume(self, evt):
        self._od_val.Disable()
        self._resume_button.Disable()
        self._pause_button.Enable()
        self._pause_automation = False

    def _pause(self, evt):
        self._pause_automation = True
        self._od_val.Enable()
        self._resume_button.Enable()
        self._pause_button.Disable()

    def _automation(self, channel):
        start_volt = self.get_start_volt()
        end_volt = self.get_end_volt()
        if start_volt > end_volt:
            step = -self.get_step_volt()
        else:
            step = self.get_step_volt()
        overlap_holder = []
        self._ccd.set_work_dir(self._filedir)
        for i in range(int(start_volt*1000), int((end_volt+0.01)*1000), int(step*1000)):
            v = float(i/1000)
            if self._kill_automation is True:
                break
            if self._pause_automation is True:
                i = overlap_holder[0]
                while self._pause_automation is True:
                    if self._kill_automation is True:
                        break
            overlap_holder.append(i)
            self._lcvr.set_voltage(channel, v)
            if len(overlap_holder) > 5:
                overlap_holder.pop(0)
            self._set_filename()
            self._filename += "_" + str(v) + "V.jpg"
            self._ccd.set_filename(self._filename)
            self._ccd.grab_frame()
            sleep(5)
        wx.CallAfter(self._stop, wx.EVT_BUTTON)

if __name__ == '__main__':
    app = wx.App()
    GUI = PowerDependentGUI()
    app.MainLoop()