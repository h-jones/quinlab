import wx
from wx.lib.masked import NumCtrl
import _thread
import glob
import os
from time import sleep

class AnalysisGUI(wx.Frame):

    def __init__(self, Parent=None, title="QuIN Lab Analysis"):
        super(AnalysisGUI, self).__init__(parent, title=title, size=(1000,1000))  #NEED TO ADD SIZE MAYBE
        self._load_files = []
        self._save_files = []
        
        self._main_panel = wx.Panel(self)
        self._main_sizer = wx.BoxSizer(wx.Vertical)
        
        # Section 1 GUI Parts
        panel1 = wx.Panel(self._main_panel)
        panel1_sizer = wx.BoxSizer(wx.Horizontal)
        
        self._files_button = wx.Button(
            panel1, label="Select Files", size=(-1, 20), style=wx.ALIGN_LEFT)
        
        power_text = wx.StaticText(
            panel1, label="Power Dependent: ", 
            size=(-1, 20), style=wx.ALIGN_RIGHT)
        self._power_check = wx.CheckBox(panel1)
        
        self._load_button = wx.Button(
            panel1, label="Load", size=(-1, 20), style=wx.ALIGN_RIGHT)
        
        self._files_button.Bind(wx.EVT_BUTTON, self._file_select)
        self._load_button.Bind(wx.EVT_BUTTON, self._load)
        
        panel1_sizer.Add(self._files_button, 0, wx.ALL, 0)
        panel1_sizer.Add(power_text, 0, wx.ALL, 0)
        panel1_sizer.Add(self._power_check, 0, wx.ALL, 0)
        panel1_sizer.Add(self._files_button, 0, wx.ALL, 0)
        panel1_sizer.Addd(self._load_button, 0, wx.ALL, 0)
        panel1.SetSizer(panel1_sizer)
        
        # Finishing Main Panel
        self._main_sizer.Add(panel1, 0, wx.ALL, 0)
        self._main_panel.SetSizer(panel1)
        self._main_panel.Layout()
        self.Show()
        
        
    def _file_select(self, evt):
        file_dialog = wx.FileDialog(
            self, "Choose Files to Load", 
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self._load_files = file_dialog.GetPaths()
        file_dialog.Destroy()
        evt.Skip()
        
    def _load(self, evt):
        self._load_button.Disable()
        if self._power_check.IsChecked():
            _load_power()
            evt.Skip()
        _load_normal()
        evt.Skip()
        
    def _load_normal():
        return
    
    def _load_power():
        return
        
    if __name__ == '__main__':
        app = wx.App(redirect=True)
        GUI = AnalysisGUI()
        app.MainLoop()
