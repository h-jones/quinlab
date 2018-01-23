import wx
from wx.lib.masked import NumCtrl
from meadowlark_d3050_controller import MeadowlarkD3050Controller
from pylightfield import LightField
from lightfield_control_panel import LightFieldControlPanel
from zaber_linear_actuator import ZaberLinearActuator
from zaber_control_panel import ZaberControlPanel
import spe2pngraw
import _thread
import glob
import os
from time import sleep


class SpectroscopyGUI(wx.Frame):

    def __init__(self,
                 parent=None,
                 title="QuIN Lab Spectroscopy"):
        super(SpectroscopyGUI, self).__init__(parent,
                                              title=title,
                                              size=(1340, 690))
        self._filedir = os.getcwd() + "\\"
        self._truefilename = ""
        self._filename = ""
        self._lcvr_init = False
        self._zaber_init = False
        self._lcvr_swp = True
        self._zaber_swp = True

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        input_nb = wx.Notebook(main_panel)

        common_panel = wx.Panel(input_nb)
        common_sizer = wx.GridBagSizer()
        lcvr_swp_txt = wx.StaticText(
            common_panel, label="LCVR Mode:",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._lcvr_swp_val = wx.Choice(
            common_panel, size=(-1, 20), choices=["Sweep", "Fixed"])
        self._lcvr_swp_val.Bind(wx.EVT_CHOICE, self._lcvr_swp_sel)
        zaber_swp_txt = wx.StaticText(
            common_panel, label="Zaber Mode:",
            size=(130, 20), style=wx.ALIGN_RIGHT)
        self._zaber_swp_val = wx.Choice(
            common_panel, size=(-1, 20), choices=["Sweep", "Fixed"])
        self._zaber_swp_val.Bind(wx.EVT_CHOICE, self._zaber_swp_sel)
        lcvr_label = wx.StaticText(
            common_panel, label="LCVR COM Port:", 
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._lcvr_val = NumCtrl(
            common_panel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._lcvr_val.SetAllowNegative(False)
        self._lcvr_val.SetBounds(1, 99)
        self._lcvr_val.SetFractionWidth(0)
        self._lcvr_val.SetIntegerWidth(2)
        self._lcvr_val.SetValue(6)
        self._lcvr_val.SetLimitOnFieldChange(True)
        self._lcvr_val.Bind(wx.EVT_KILL_FOCUS, self._lcvr_entry)
        lcvr_chan = wx.StaticText(
            common_panel, label="LCVR Channel:", 
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._lcvr_ch = wx.Choice(
            common_panel, size=(-1, 20), choices=["1", "2", "3", "4"])
        zaber_txt = wx.StaticText(
            common_panel, label="Zaber COM Port:",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._zaber_val = NumCtrl(
            common_panel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._zaber_val.SetAllowNegative(False)
        self._zaber_val.SetBounds(1, 99)
        self._zaber_val.SetFractionWidth(0)
        self._zaber_val.SetIntegerWidth(2)
        self._zaber_val.SetValue(9)
        self._zaber_val.SetLimitOnFieldChange(True)
        self._zaber_val.Bind(wx.EVT_KILL_FOCUS, self._zaber_entry)
        wavelength_label = wx.StaticText(
            common_panel, label="Laser Wavelength (nm):",
            size=(130, 20), style=wx.ALIGN_RIGHT)
        self._wavelength_val = NumCtrl(
            common_panel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._wavelength_val.SetAllowNegative(False)
        self._wavelength_val.SetBounds(400, 1100)
        self._wavelength_val.SetFractionWidth(0)
        self._wavelength_val.SetIntegerWidth(4)
        self._wavelength_val.SetValue(780)
        self._wavelength_val.SetLimitOnFieldChange(True)
        pow_label = wx.StaticText(
            common_panel, label="Laser Power (mW):",
            size=(130, 20), style=wx.ALIGN_RIGHT)
        self._pow_val = NumCtrl(
            common_panel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._pow_val.SetAllowNegative(False)
        self._pow_val.SetBounds(0, 1000)
        self._pow_val.SetFractionWidth(2)
        self._pow_val.SetIntegerWidth(4)
        self._pow_val.SetValue(0)
        self._pow_val.SetLimitOnFieldChange(True)
        od_label = wx.StaticText(
            common_panel, label="OD:", size=(130, 20), style=wx.ALIGN_RIGHT)
        self._od_val = wx.Choice(
            common_panel, size=(-1, 20), 
            choices=["0", "0.5", "1", "1.5", "2", "2.5", 
                     "3", "3.5", "4", "4.5", "5"])
        self._start_volt_txt = wx.StaticText(
            common_panel, label="Start Voltage (V):",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._start_volt_val = NumCtrl(
            common_panel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._start_volt_val.SetAllowNegative(False)
        self._start_volt_val.SetBounds(0, 10)
        self._start_volt_val.SetFractionWidth(2)
        self._start_volt_val.SetIntegerWidth(2)
        self._start_volt_val.SetValue(10)
        self._start_volt_val.SetLimitOnFieldChange(True)
        end_volt_label = wx.StaticText(
            common_panel, label="End Voltage (V):",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._end_volt_val = NumCtrl(
            common_panel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._end_volt_val.SetAllowNegative(False)
        self._end_volt_val.SetBounds(0, 10)
        self._end_volt_val.SetFractionWidth(2)
        self._end_volt_val.SetIntegerWidth(2)
        self._end_volt_val.SetValue(0)
        self._end_volt_val.SetLimitOnFieldChange(True)
        step_volt_label = wx.StaticText(
            common_panel, label="Absolute Step Voltage (V):",
            size=(140, 20), style=wx.ALIGN_RIGHT)
        self._step_volt_val = NumCtrl(
            common_panel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._step_volt_val.SetAllowNegative(False)
        self._step_volt_val.SetBounds(0, 10)
        self._step_volt_val.SetFractionWidth(2)
        self._step_volt_val.SetIntegerWidth(2)
        self._step_volt_val.SetValue(0.1)
        self._step_volt_val.SetLimitOnFieldChange(True)
        self._dir_button = wx.Button(
            common_panel, label="Choose Save Location", size=(130, 20))
        self._dir_button.Bind(wx.EVT_BUTTON, self._dir_select)
        self._file_button = wx.Button(
            common_panel, label="Choose Save Filename", size=(130, 20))
        self._file_button.Bind(wx.EVT_BUTTON, self._file_select)
        self._go_button = wx.Button(
            common_panel, label="Start", size=(130, 20))
        self._go_button.SetForegroundColour(wx.Colour("GREEN"))
        self._go_button.Bind(wx.EVT_BUTTON, self._go)
        self._stop_button = wx.Button(
            common_panel, label="Stop", size=(130, 20))
        self._stop_button.Bind(wx.EVT_BUTTON, self._stop)
        self._stop_button.SetForegroundColour(wx.Colour("RED"))
        self._resume_button = wx.Button(
            common_panel, label="Resume", size=(130, 20))
        self._resume_button.Bind(wx.EVT_BUTTON, self._resume)
        self._pause_button = wx.Button(
            common_panel, label="Pause", size=(130, 20))
        self._pause_button.Bind(wx.EVT_BUTTON, self._pause)
        curr_dir_txt = wx.StaticText(
            common_panel, label="Current Directory:",
            size=(-1, 20), style=wx.ALIGN_RIGHT)
        self._curr_dir_disp = wx.StaticText(
            common_panel, label=self._filedir, size=(-1, 20))
        curr_file_txt = wx.StaticText(
            common_panel, label="Current Filename:",
            size=(-1, 20), style=wx.ALIGN_RIGHT)
        self._curr_file_disp = wx.StaticText(
            common_panel, label=self._filename, size=(-1, 20))
        common_sizer.Add(lcvr_label, (0,0))
        common_sizer.Add(self._lcvr_val, (0, 1))
        common_sizer.Add(lcvr_chan, (1, 0))
        common_sizer.Add(self._lcvr_ch, (1, 1))
        common_sizer.Add(self._start_volt_txt, (2, 0))
        common_sizer.Add(self._start_volt_val, (2, 1))
        common_sizer.Add(end_volt_label, (3, 0))
        common_sizer.Add(self._end_volt_val, (3, 1))
        common_sizer.Add(step_volt_label, (4, 0))
        common_sizer.Add(self._step_volt_val, (4, 1))
        common_sizer.Add(zaber_txt, (5, 0))
        common_sizer.Add(self._zaber_val, (5, 1))
        common_sizer.Add(wavelength_label, (0, 2))
        common_sizer.Add(self._wavelength_val, (0, 3))
        common_sizer.Add(pow_label, (1, 2))
        common_sizer.Add(self._pow_val, (1, 3))
        common_sizer.Add(od_label, (2, 2))
        common_sizer.Add(self._od_val, (2, 3))
        common_sizer.Add(self._dir_button, (3, 2))
        common_sizer.Add(self._file_button, (3, 3))
        common_sizer.Add(self._go_button, (4, 2))
        common_sizer.Add(self._stop_button, (4, 3))
        common_sizer.Add(self._resume_button, (5, 2))
        common_sizer.Add(self._pause_button, (5, 3))
        common_sizer.Add(lcvr_swp_txt, (6, 0))
        common_sizer.Add(self._lcvr_swp_val, (6, 1))
        common_sizer.Add(zaber_swp_txt, (6, 2))
        common_sizer.Add(self._zaber_swp_val, (6, 3))
        common_sizer.Add(curr_dir_txt, (7, 0))
        common_sizer.Add(self._curr_dir_disp, (7, 1), wx.GBSpan(1, 3))
        common_sizer.Add(curr_file_txt, (8, 0))
        common_sizer.Add(self._curr_file_disp, (8, 1), wx.GBSpan(1, 3))
        common_panel.SetSizer(common_sizer)
        self._stop_button.Disable()
        self._pause_button.Disable()
        self._resume_button.Disable()
        
        self._zaber = ZaberLinearActuator()
        self._zaber_pnl = ZaberControlPanel(self._zaber, input_nb)
        self._zaber_pnl.disable_ui()

        self._lf = LightField("",True)
        self._lf.set_export(True)
        
        self._lfcontrol = LightFieldControlPanel(self._lf, input_nb)

        input_nb.InsertPage(0, common_panel, "Common Settings")
        input_nb.InsertPage(1, self._zaber_pnl, "Zaber Settings")
        input_nb.InsertPage(2, self._lfcontrol, "LightField Settings")

        copyright_str = "\u00a9 2016 QuIN Lab "
        copyright_str += "Developed by Hayden Jones"
        copyright_text = wx.StaticText(main_panel, label=copyright_str)

        self._img = wx.Image(1340, 400, True).ConvertToBitmap()
        self._display = wx.StaticBitmap(
            main_panel, -1, self._img,
            wx.DefaultPosition, wx.Size(1340, 400))
        self._display.SetBitmap(self._img)
        
        self._set_filename()
        self.update_file_display()

        main_sizer.Add(input_nb, 0, wx.ALL, 0)
        main_sizer.Add(self._display, 0, wx.ALL, 0)
        main_sizer.Add(copyright_text, 0, wx.ALL, 0)

        main_panel.SetSizer(main_sizer)
        main_panel.Layout()

        self.Bind(wx.EVT_CLOSE, self._on_close)

        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE
                            ^ wx.RESIZE_BORDER
                            ^ wx.MAXIMIZE_BOX)
        self.Show()

    def _on_close(self, evt):
        if self._lcvr_init is True:
            self._lcvr.close()
        self._lf.close_lightfield()
        self._lf.close_matlab()
        evt.Skip()

    def disable_ui(self):
        self._zaber_val.Disable()
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
        self._zaber_pnl.disable_ui()
        self._lfcontrol.disable_ui()

    def enable_ui(self):
        self._zaber_val.Enable()
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
        self._zaber_pnl.enable_ui()
        self._lfcontrol.enable_ui()

    def get_od(self):
        return float(self._od_val.GetCurrentSelection() / 2)

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

    def get_lcvr_ch(self):
        return self._lcvr_ch.GetCurrentSelection() + 1
        
    def update_dir_display(self):
        self._curr_dir_disp.SetLabel(self._filedir)
        
    def update_file_display(self):
        self._curr_file_disp.SetLabel(self._filename)
        
    def _lcvr_swp_sel(self, evt):
        if self._lcvr_swp_val.GetCurrentSelection() == 0:
            self._lcvr_swp = True
        else:
            self._lcvr_swp = False
    
    def _zaber_swp_sel(self, evt):
        if self._zaber_swp_val.GetCurrentSelection() == 0:
            self._zaber_swp = True
        else:
            self._zaber_swp = False

    def _invalid_lcvr_warn(self):
        warning_message = "Invalid LCVR Controller Address/Connection!"
        warning = wx.GenericMessageDialog(
            None, warning_message, "Warning!", wx.OK, wx.DefaultPosition)
        warning.ShowModal()
        warning.Destroy()

    def _lcvr_entry(self, evt):
        if self._lcvr_init is True:
            return
        try:
            com_port = self._lcvr_val.GetValue()
            self._lcvr = MeadowlarkD3050Controller(com_port)
        except Exception:
            self._invalid_lcvr_warn()
            evt.Skip()
            return
        self._lcvr_init = True
        evt.Skip()
        
    def _invalid_zaber_warn(self):
        warning_message = "Invalid Zaber Address/Connection!"
        warning = wx.GenericMessageDialog(
            None, warning_message, "Warning!", wx.OK, wx.DefaultPosition)
        warning.ShowModal()
        warning.Destroy()

    def _zaber_entry(self, evt):
        if self._zaber_init is True:
            return
        try:
            com_port = self._zaber_val.GetValue()
            self._zaber.open(com_port)
        except Exception:
            self._invalid_zaber_warn()
            evt.Skip()
            return
        self._zaber_pnl.enable_ui()
        self._zaber_init = True
        evt.Skip()
        
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
        self.update_dir_display()
        dir_dialog.Destroy()

    def _file_select(self, evt):
        file_dialog = wx.TextEntryDialog(self,
                                         "Enter the file name...",
                                         "File Name Selection Dialog",
                                         self._truefilename)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self._truefilename = file_dialog.GetValue()
        self._set_filename()
        self.update_file_display()
        file_dialog.Destroy()

    def _go(self, evt):
        self._lcvr_entry(wx.EVT_BUTTON)
        self._zaber_entry(wx.EVT_BUTTON)
        if self._lcvr_init is False:
            self._invalid_lcvr_warn()
            return
        if self._zaber_init is False:
            self._invalid_zaber_warn()
            return
        self.disable_ui()
        self._kill_automation = False
        self._pause_automation = False
        _thread.start_new_thread(self._automation, (self.get_lcvr_ch(),))
        
    def _stop(self, evt):
        self._kill_automation = True
        self._pause_automation = False
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
        self._lf.set_directory(self._filedir.rstrip("\\"))
        start_volt = self.get_start_volt()
        if self._lcvr_swp is True:
            end_volt = self.get_end_volt()
        else:
            end_volt = start_volt
        if start_volt > end_volt:
            step_volt = -self.get_step_volt()
        else:
            step_volt = self.get_step_volt()
        self._zaber.goto_pos(0, 324000)
        start_zaber = self._zaber_pnl.get_start()
        if self._zaber_swp is True:
            end_zaber = self._zaber_pnl.get_end()
            self._zaber.goto_pos(0, start_zaber)
        else:
            end_zaber = start_zaber
        if start_zaber > end_zaber:
            step_zaber = -self._zaber_pnl.get_step()
        else:
            step_zaber = self._zaber_pnl.get_step()
        self._lcvr.set_voltage(channel, start_volt)
        overlap_holder = []
        for i in range(int(start_volt*1000), int((end_volt*1000)+1), int(step_volt*1000)):
            if self._kill_automation is True:
                break
            if self._pause_automation is True:
                i = overlap_holder[0]
                while self._pause_automation is True:
                    if self._kill_automation is True:
                        break
            overlap_holder.append(i)
            if len(overlap_holder) > 5:
                overlap_holder.pop(0)
            v = float(i/1000)
            self._set_filename()
            self._lcvr.set_voltage(channel, v)
            self._filename += "_" + str(v) + "V"
            self._lf.set_filename(self._filename)
            for j in range(start_zaber, end_zaber+1, step_zaber):
                if self._kill_automation is True:
                    break
                if self._pause_automation is True:
                    while self._pause_automation is True:
                        if self._kill_automation is True:
                            break
                self._filename += "_" + str(j) + "zaber"
                self._zaber.goby_dist(0, step_zaber)
                self._lf.set_filename(self._filename)
                self._lf.acquire(60)
                self._lf.set_filename(self._filename)
                newest_spe = max(glob.iglob(self._filedir + '*.spe'), key=os.path.getctime)
                spe2pngraw.spe2pngraw(self._filedir, newest_spe)
                newest_png = newest_spe.rstrip('.spe') + '.png'
                self._img = wx.Image(newest_png, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                wx.CallAfter(self._display.SetBitmap, self._img)
            sleep(1)
        wx.CallAfter(self._stop, wx.EVT_BUTTON)

if __name__ == '__main__':
    app = wx.App(redirect=True)
    GUI = SpectroscopyGUI()
    app.MainLoop()