import wx
from wx.lib.masked import NumCtrl
import pylightfield


class LightFieldControlPanel(wx.Panel):
    
    def __init__(self, lightfield, *args):
        wx.Panel.__init__(self, *args)
        self._lf = lightfield
        
        subpanel = wx.Panel(self)
        sp_sizer = wx.FlexGridSizer(6, 4, 0, 0)
        
        exp_txt = wx.StaticText(
            subpanel, label="Exposure Time (ms):", 
            size=(115, 20), style=wx.ALIGN_RIGHT)
        self._exp_val = NumCtrl(
            subpanel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._exp_val.SetAllowNegative(False)
        self._exp_val.SetFractionWidth(0)
        self._exp_val.SetIntegerWidth(9)
        self._exp_val.SetValue(100)
        self._exp_val.Bind(wx.EVT_KILL_FOCUS, self._exp_entry)
        
        frames_txt = wx.StaticText(
            subpanel, label="Number of Frames:", 
            size=(-1, 20), style=wx.ALIGN_RIGHT)
        self._frames_val = NumCtrl(
            subpanel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._frames_val.SetAllowNegative(False)
        self._frames_val.SetFractionWidth(0)
        self._frames_val.SetIntegerWidth(9)
        self._frames_val.SetValue(1)
        self._frames_val.Bind(wx.EVT_KILL_FOCUS, self._frames_entry)
        
        adcqlty_txt = wx.StaticText(
            subpanel, label="ADC Quality:", 
            size=(-1, 20), style=wx.ALIGN_RIGHT)
        self._adcqlty_val = wx.Choice(
            subpanel, size=(-1, 20), style=wx.CB_SORT,
            choices=["High Capacity", "Low Noise"])
        self._adcqlty_val.Bind(wx.EVT_CHOICE, self._adcqlty_entry)
                
        adcspeed_txt = wx.StaticText(
            subpanel, label="ADC Speed:", size=(-1, 20), 
            style=wx.ALIGN_RIGHT)
        self._adcspeed_val = wx.Choice(
            subpanel, size=(-1, 20),
            choices=["4 MHz", "2 MHz", "1 MHz", "500 kHz", "200 kHz",
                     "100 kHz", "50 kHz"])
        self._adcspeed_val.Bind(wx.EVT_CHOICE, self._adcspeed_entry)
        
        adcgain_txt = wx.StaticText(
            subpanel, label="ADC Analog Gain:", size=(-1, 20), 
            style=wx.ALIGN_RIGHT)
        self._adcgain_val = wx.Choice(
            subpanel, size=(-1, 20), choices=["High", "Medium", "Low"])
        self._adcgain_val.Bind(wx.EVT_CHOICE, self._adcgain_entry)
        
        adcbits_txt = wx.StaticText(
            subpanel, label="ADC Bit Depth:", size=(-1, 20), 
            style=wx.ALIGN_RIGHT)
        bitdepth = self._lf.get_adcbitdepth()
        adcbits_val = wx.StaticText(
            subpanel, label="{0} bits".format(bitdepth), size=(-1, 20), 
            style=wx.ALIGN_LEFT)
            
        width_txt = wx.StaticText(
            subpanel, label="Sensor Bin Width:", size=(-1, 20), 
            style=wx.ALIGN_RIGHT)
        self._width_val = NumCtrl(
            subpanel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._width_val.SetAllowNegative(False)
        self._width_val.SetBounds(1, 1340)
        self._width_val.SetFractionWidth(0)
        self._width_val.SetIntegerWidth(4)
        self._width_val.SetValue(1)
        self._width_val.SetLimitOnFieldChange(True)
        self._width_val.Bind(wx.EVT_KILL_FOCUS, self._width_entry)
                    
        height_txt = wx.StaticText(
            subpanel, label="Sensor Bin Height:", size=(-1, 20), 
            style=wx.ALIGN_RIGHT)
        self._height_val = NumCtrl(
            subpanel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._height_val.SetAllowNegative(False)
        self._height_val.SetBounds(1, 400)
        self._height_val.SetFractionWidth(0)
        self._height_val.SetIntegerWidth(4)
        self._height_val.SetValue(1)
        self._height_val.SetLimitOnFieldChange(True)
        self._height_val.Bind(wx.EVT_KILL_FOCUS, self._height_entry)
        
        roi_txt = wx.StaticText(
            subpanel, label="Sensor Mode:", size=(-1, 20), 
            style=wx.ALIGN_RIGHT)
        self._roi_val = wx.Choice(
            subpanel, size=(-1, 20), 
            choices=["Full Sensor", "Line Sensor", "Binned Sensor"])
        self._roi_val.Bind(wx.EVT_CHOICE, self._roi_entry)
     
        grating_txt = wx.StaticText(
            subpanel, label="Grating Density:", size=(-1, 20), 
            style=wx.ALIGN_RIGHT)
        self._grating_val = wx.Choice(
            subpanel, size=(-1, 20), 
            choices=["300 g/mm", "1200 g/mm", "1800 g/mm"])
        self._grating_val.Bind(wx.EVT_CHOICE, self._grating_entry)
        
        lambda_txt = wx.StaticText(
            subpanel, label="Center Wavelength (nm):", 
            size=(135, 20), style=wx.ALIGN_RIGHT)
        self._lambda_val = NumCtrl(
            subpanel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._lambda_val.SetAllowNegative(False)
        self._lambda_val.SetFractionWidth(3)
        self._lambda_val.SetIntegerWidth(4)
        self._lambda_val.SetValue(780)
        self._lambda_val.Bind(wx.EVT_KILL_FOCUS, self._lambda_entry)
        
        slit_txt = wx.StaticText(
            subpanel, label="Slit Width (\u03BCm):", size=(-1, 20), 
            style=wx.ALIGN_RIGHT)
        self._slit_val = NumCtrl(
            subpanel, size=(-1, 20), style=wx.TE_PROCESS_ENTER)
        self._slit_val.SetAllowNegative(False)
        self._slit_val.SetBounds(10, 3000)
        self._slit_val.SetFractionWidth(0)
        self._slit_val.SetIntegerWidth(4)
        self._slit_val.SetValue(100)
        self._slit_val.SetLimitOnFieldChange(True)
        self._slit_val.Bind(wx.EVT_KILL_FOCUS, self._slit_entry)
        
        sp_sizer.AddMany(
            [exp_txt, self._exp_val, width_txt, self._width_val,
             frames_txt, self._frames_val, height_txt, self._height_val,
             adcqlty_txt, self._adcqlty_val, roi_txt, self._roi_val,
             adcspeed_txt, self._adcspeed_val, grating_txt, self._grating_val,
             adcgain_txt, self._adcgain_val, lambda_txt, self._lambda_val,
             adcbits_txt, adcbits_val, slit_txt, self._slit_val])
        subpanel.SetSizer(sp_sizer)
        
        overall_sizer = wx.BoxSizer()
        overall_sizer.Add(subpanel, 0, wx.ALL, 10)
        self.SetSizer(overall_sizer)
        
    def disable_ui(self):
        self._exp_val.Disable()
        self._frames_val.Disable()
        self._adcqlty_val.Disable()
        self._adcspeed_val.Disable()
        self._adcgain_val.Disable()
        self._width_val.Disable()
        self._height_val.Disable()
        self._roi_val.Disable()
        self._grating_val.Disable()
        self._lambda_val.Disable()
        self._slit_val.Disable()
        
    def enable_ui(self):
        self._exp_val.Enable()
        self._frames_val.Enable()
        self._adcqlty_val.Enable()
        self._adcspeed_val.Enable()
        self._adcgain_val.Enable()
        self._width_val.Enable()
        self._height_val.Enable()
        self._roi_val.Enable()
        self._grating_val.Enable()
        self._lambda_val.Enable()
        self._slit_val.Enable()

    def _exp_entry(self, evt):
        if self._exp_val.GetValue() < 1:
            return
        self._lf.set_exposure(self._exp_val.GetValue())
        evt.Skip()
        
    def _frames_entry(self, evt):
        if self._frames_val.GetValue() < 1:
            return
        self._lf.set_frames(self._frames_val.GetValue())
        evt.Skip()
    
    def _adcqlty_entry(self, evt):
        if self._adcqlty_val.GetCurrentSelection() == 0:
            self._lf.set_adcquality(2)
        else:
            self._lf.set_adcquality(1)
            
    def _adcspeed_entry(self, evt):
        speeds = {
            0: 4,
            1: 2,
            2: 1,
            3: 0.5,
            4: 0.2,
            5: 0.1,
            6: 0.05
        }
        self._lf.set_adcspeed(
            speeds[self._adcspeed_val.GetCurrentSelection()])
            
    def _adcgain_entry(self, evt):
        if self._adcgain_val.GetCurrentSelection() == 0:
            self._lf.set_adcanaloggain(3)
        elif self._adcgain_val.GetCurrentSelection() == 1:
            self._lf.set_adcanaloggain(2)
        else:
            self._lf.set_adcanaloggain(1)
            
    def _width_entry(self, evt):
        if self._width_val.GetValue() < 1:
            return
        self._lf.set_binwidth(self._width_val.GetValue())
        evt.Skip()
        
    def _height_entry(self, evt):
        if self._height_val.GetValue() < 1:
            return
        self._lf.set_binheight(self._height_val.GetValue())
        evt.Skip()
        
    def _roi_entry(self, evt):
        if self._roi_val.GetCurrentSelection() == 0:
            self._lf.set_roiselection(1)
        elif self._roi_val.GetCurrentSelection() == 1:
            self._lf.set_roiselection(3)
        else:
            self._lf.set_roiselection(2)
    
    def _grating_entry(self, evt):
        if self._grating_val.GetCurrentSelection() == 0:
            self._lf.set_grating(300)
        elif self._grating_val.GetCurrentSelection() == 1:
            self._lf.set_grating(1200)
        else:
            self._lf.set_grating(1800)
            
    def _lambda_entry(self, evt):
        if self._lambda_val.GetValue() < 1:
            return
        self._lf.set_centerwavelength(self._lambda_val.GetValue())
        evt.Skip()
        
    def _slit_entry(self, evt):
        if self._slit_val.GetValue() < 1:
            return
        self._lf.set_slitwidth(self._slit_val.GetValue())
        evt.Skip()
        