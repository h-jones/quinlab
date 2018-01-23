import wx
import autoit
from time import sleep


class CCDPanel(wx.Panel):

    def __init__(self, working_dir, filename, gui_title, *args):
        wx.Panel.__init__(self, *args)
        self._work_dir = working_dir
        self._filename = filename
        self._gui_title = gui_title

        subpanel = wx.Panel(self)
        sp_sizer = wx.BoxSizer()

        wx.InitAllImageHandlers()
        self._img = wx.Image(720, 480, True).ConvertToBitmap()
        self._display = wx.StaticBitmap(
            self, -1, self._img, wx.DefaultPosition, wx.Size(720, 480))
        self._display.SetBitmap(self._img)

        sp_sizer.Add(self._display, 0, wx.ALL, 10)
        subpanel.SetSizer(sp_sizer)

        overall_sizer = wx.BoxSizer(wx.HORIZONTAL)
        overall_sizer.Add(subpanel)
        self.SetSizer(overall_sizer)
        self.SetSize(720, 480)
        
        autoit.auto_it_set_option("WinTitleMatchMode", 2)

    def set_filename(self, filename):
        self._filename = filename

    def set_gui_title(self, title):
        self._gui_title = title

    def set_work_dir(self, directory):
        self._work_dir = directory

    def open_xcap(self):
        xcap = "C:\\Program Files\\EPIX\\XCAP"
        xcap += "\\program\\xcapwxx.exe -Xmx128M -myjava"
        autoit.run(xcap, "C:\\Users\\Public\\Documents\\EPIX\\XCAP")
        autoit.win_wait_active("EPIX")
        autoit.send("{TAB}")
        sleep(0.05)
        autoit.send("{ENTER}")
        sleep(0.05)
        autoit.win_wait_active("View #")
        autoit.win_activate(self._gui_title)

    def grab_frame(self):
        autoit.win_activate("View #")
        autoit.send("^s")
        sleep(0.05)
        autoit.send("{ALT}")
        sleep(0.05)
        autoit.send("{ENTER}")
        sleep(0.05)
        autoit.send("{ENTER}")
        sleep(1)
        autoit.send("{TAB}")
        sleep(0.05)
        autoit.send("{ENTER}")
        sleep(0.5)
        for i in range(0, 10, 1):
            autoit.send("{TAB}")
            sleep(0.05)
        autoit.send(self._work_dir
                    + self._filename)
        for i in range(0, 6, 1):
            autoit.send("{TAB}")
            sleep(0.05)
        autoit.send("{ENTER}")
        self._img = wx.Image(
            self._work_dir + self._filename, wx.BITMAP_TYPE_ANY)
        self._img = self._img.ConvertToBitmap()
        self._display.SetBitmap(self._img)
        autoit.win_activate(self._gui_title)

    def close_xcap(self):
        autoit.win_activate("EPIX")
        autoit.win_close("EPIX")
        sleep(0.2)
        autoit.win_activate("EPIX")
        autoit.win_close("EPIX")
        sleep(0.2)
        autoit.win_activate("EPIX")
        autoit.win_close("EPIX")
        sleep(0.2)
        autoit.win_activate("EPIX")
        autoit.win_close("EPIX")
        autoit.win_activate(self._gui_title)
        sleep(5)
