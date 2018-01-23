import wx
from wx.lib.masked import NumCtrl


class ZaberControlPanel(wx.Panel):

    def __init__(self, zaber, *args):
        wx.Panel.__init__(self, *args)
        self._zaber = zaber
        
        self._home_button = wx.Button(
            self, label="Home Zaber", size=(100, 24))
        self._home_button.Bind(wx.EVT_BUTTON, self._home)
        self._center_button = wx.Button(
            self, label="Center Zaber", size=(100, 24))
        self._center_button.Bind(wx.EVT_BUTTON, self._center)
        
        self._start_txt = wx.StaticText(
            self, label="Start Position:",
            size=(100, 24), style=wx.ALIGN_RIGHT)
        self._start_val = NumCtrl(
            self, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._start_val.SetAllowNegative(False)
        self._start_val.SetBounds(0, 640000)
        self._start_val.SetFractionWidth(0)
        self._start_val.SetIntegerWidth(6)
        self._start_val.SetValue(294000)
        
        self._end_txt = wx.StaticText(
            self, label="End Position:",
            size=(100, 24), style=wx.ALIGN_RIGHT)
        self._end_val = NumCtrl(
            self, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._end_val.SetAllowNegative(False)
        self._end_val.SetBounds(0, 640000)
        self._end_val.SetFractionWidth(0)
        self._end_val.SetIntegerWidth(6)
        self._end_val.SetValue(354000)
        
        self._step_txt = wx.StaticText(
            self, label="Absolute Step Size:",
            size=(100, 24), style=wx.ALIGN_RIGHT)
        self._step_val = NumCtrl(
            self, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._step_val.SetAllowNegative(False)
        self._step_val.SetBounds(0, 640000)
        self._step_val.SetFractionWidth(0)
        self._step_val.SetIntegerWidth(6)
        self._step_val.SetValue(1500)
        
        self._go_abs_button = wx.Button(
            self, label="Go to Position \u2192", size=(100, 24))
        self._go_abs_button.Bind(wx.EVT_BUTTON, self._go_abs)
        self._goto_val = NumCtrl(
            self, size=(100, 20), style=wx.TE_PROCESS_ENTER)
        self._goto_val.SetBounds(0, 640000)
        self._goto_val.SetAllowNegative(False)
        self._goto_val.SetFractionWidth(0)
        self._goto_val.SetIntegerWidth(6)
        self._goto_val.SetValue(0)
        self._goto_val.SetLimitOnFieldChange(True)
        
        self._go_rel_button = wx.Button(
            self, label="Go by Distance \u2192", size=(100,24))
        self._go_rel_button.Bind(wx.EVT_BUTTON, self._go_rel)
        self._goby_val = NumCtrl(
            self, size=(100, 20), style=wx.TE_PROCESS_ENTER)
        self._goby_val.SetBounds(-640000, 640000)
        self._goby_val.SetAllowNegative(True)
        self._goby_val.SetFractionWidth(0)
        self._goby_val.SetIntegerWidth(6)
        self._goby_val.SetValue(0)
        self._goby_val.SetLimitOnFieldChange(True)
        
        self._pos_txt = wx.StaticText(
            self, label="Current Position:", 
            size=(-1, 24), style=wx.ALIGN_RIGHT)
        self._pos_val = wx.StaticText(self, label="0", size=(-1, 24))

        sizer = wx.GridBagSizer(5, 5)
        sizer.Add(self._home_button, (0, 2))
        sizer.Add(self._center_button, (0, 3))
        sizer.Add(self._start_txt, (0, 0))
        sizer.Add(self._start_val, (0, 1))
        sizer.Add(self._end_txt, (1, 0))
        sizer.Add(self._end_val, (1, 1))
        sizer.Add(self._step_txt, (2, 0))
        sizer.Add(self._step_val, (2, 1))
        sizer.Add(self._go_abs_button, (1, 2))
        sizer.Add(self._goto_val, (1, 3))
        sizer.Add(self._go_rel_button, (2, 2))
        sizer.Add(self._goby_val, (2, 3))
        sizer.Add(self._pos_txt, (3, 1))
        sizer.Add(self._pos_val, (3, 2))
        self.SetSizer(sizer)

    def disable_ui(self):
        self._home_button.Disable()
        self._center_button.Disable()
        self._start_val.Disable()
        self._end_val.Disable()
        self._step_val.Disable()
        self._go_abs_button.Disable()
        self._goto_val.Disable()
        self._go_rel_button.Disable()
        self._goby_val.Disable()
        
    def enable_ui(self):
        self._home_button.Enable()
        self._center_button.Enable()
        self._start_val.Enable()
        self._end_val.Enable()
        self._step_val.Enable()
        self._go_abs_button.Enable()
        self._goto_val.Enable()
        self._go_rel_button.Enable()
        self._goby_val.Enable()
        
    def get_start(self):
        return self._start_val.GetValue()
        
    def get_end(self):
        return self._end_val.GetValue()
        
    def get_step(self):
        return self._step_val.GetValue()
        
    def update_pos(self):
        self._pos_val.SetLabel(str(self._zaber.get_current_pos(0)[0][1]))
        
    def _home(self, evt):
        self._zaber.home(0)
        self.update_pos()
        
    def _center(self, evt):
        self._zaber.goto_pos(0, 324000)
        self.update_pos()

    def _go_abs(self, evt):
        self._zaber.goto_pos(0, self._goto_val.GetValue())
        self.update_pos()  

    def _go_rel(self, evt):
        curr_pos = int(self._pos_val.GetLabel())
        if curr_pos + self._goby_val.GetValue() > 640000:
            return
        self._zaber.goby_dist(0, self._goby_val.GetValue())
        self.update_pos()
