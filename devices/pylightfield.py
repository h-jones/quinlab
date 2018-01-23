import matlab.engine


class LightField:

    def __init__(self, options="", visible=False):
        self._eng = matlab.engine.start_matlab(options)
        self._eng.Setup_LightField_Environment(nargout=0)
        self._matlab_open = True
        self._lf = self._eng.lfm(visible)
        self._eng.set_grating(self._lf, 300, nargout=0)
        self._grating = 300
        self._lf_open = True

    def _lf_check(self):
        if self._lf_open is False:
            raise Exception("No LightField Session")

    def open_matlab(self, options):
        self._eng = matlab.engine.start_matlab(options)
        self._eng.Setup_LightField_Environment(nargout=0)
        self._matlab_open = True

    def close_matlab(self):
        self._eng.quit()
        self._matlab_open = False

    def open_lightfield(self, visible=False):
        if self._matlab_open is False:
            raise Exception("No MATLAB Session")
        self._lf = self._eng.lfm(visible)
        self._lf_open = True

    def close_lightfield(self):
        self._lf_check()
        self._eng.close(self._lf, nargout=0)
        self._lf_open = False

    def set_exposure(self, exposure):
        """exposure in ms"""
        self._lf_check()
        self._eng.set_exposure(self._lf, exposure, nargout=0)

    def get_exposure(self):
        """exposure in ms float"""
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_exposure(self._lf)
        return self._eng.eval("x")
    
    def set_frames(self, frames):
        """num frames"""
        self._lf_check()
        self._eng.set_frames(self._lf, frames, nargout=0)
        
    def get_frames(self):
        """num frames int"""
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_frames(self._lf)
        return self._eng.eval("x")
    
    def set_adcquality(self, quality):
        """quality is an int, 1 = lownoise, 2 = highcapacity"""
        self._lf_check()
        self._eng.set_adcquality(self._lf, quality, nargout=0)
        
    def get_adcquality(self):
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_adcquality(self._lf)
        return self._eng.eval("x")
    
    def set_adcspeed(self, speed):
        """speed in float MHz """
        self._lf_check()
        valid_speeds = [4, 2, 1, 0.5, 0.2, 0.1, 0.05]
        if speed not in valid_speeds:
            raise Exception("Invalid ADC Speed")
        self._eng.set_adcspeed(self._lf, speed, nargout=0)
        
    def get_adcspeed(self):
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_adcspeed(self._lf)
        return self._eng.eval("x")

    def set_adcanaloggain(self, gain):
        """int 1 low, 2 med, 3 high """
        self._lf_check()
        self._eng.set_adcanaloggain(self._lf, gain, nargout=0)

    def get_adcanaloggain(self):
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_adcanaloggain(self._lf)
        return self._eng.eval("x")

    def get_adcbitdepth(self):
        """ int bitdepth"""
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_adcbitdepth(self._lf)
        return self._eng.eval("x")

    def set_binwidth(self, width):
        """width of sensor expressed as divisor of maximum number of columns
           int 1-1340"""
        self._lf_check()
        self._eng.set_binwidth(self._lf, width, nargout=0)

    def get_binwidth(self):
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_binwidth(self._lf)
        return self._eng.eval("x")

    def set_binheight(self, height):
        """height of sensor expressed as divisor of maximum number of rows
            int 1-400"""
        self._lf_check()
        self._eng.set_binheight(self._lf, height, nargout=0)

    def get_binheight(self):
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_binheight(self._lf)
        return self._eng.eval("x")

    def set_roiselection(self, selection):
        """int 1 fullsensor, 2 binnedsensor,
            3 linesensor, 4 customregions"""
        self._lf_check()
        self._eng.set_roiselection(self._lf, selection, nargout=0)

    def get_roiselection(self):
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_roiselection(self._lf)
        return self._eng.eval("x")

    def set_grating(self, grating):
        """int 300 1200 or 1800"""
        self._lf_check()
        valid_grating = [300, 1200, 1800]
        if grating not in valid_grating:
            raise Exception("Invalid Grating")
        self._eng.set_grating(self._lf, grating, nargout=0)

    def get_grating(self):
        self._lf_check()
        return self._grating
    
    def set_centerwavelength(self, wavelength):
        """float center wavelength"""
        self._lf_check()
        self._eng.set_centerwavelength(self._lf, wavelength, nargout=0)

    def get_centerwavelength(self):
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_centerwavelength(self._lf)
        return self._eng.eval("x")
    
    def set_slitwidth(self, width):
        """int width in microns"""
        self._lf_check()
        if not 10 <= width <= 3000:
            raise Exception("Invalid slit width")
        self._eng.set_slitwidth(self._lf, width, nargout=0)

    def get_slitwidth(self):
        self._lf_check()
        self._eng.workspace["x"] = self._eng.get_slitwidth(self._lf)
        return self._eng.eval("x")

    def set_filename(self, filename):
        """file name to save, excluding directory """
        self._lf_check()
        self._eng.set_filename(self._lf, filename, nargout=0)

    def set_directory(self, directory):
        """ """
        self._lf_check()
        self._eng.set_directory(self._lf, directory, nargout=0)

    def set_filedate(self, include):
        """ """
        self._lf_check()
        self._eng.set_filedate(self._lf, include, nargout=0)

    def set_filetime(self, include):
        """ """
        self._lf_check()
        self._eng.set_filetime(self._lf, include, nargout=0)

    def set_fileincrement(self, include):
        """ """
        self._lf_check()
        self._eng.set_fileincrement(self._lf, include, nargout=0)
        
    def set_export(self, export):
        """true on, false off"""
        self._lf_check()
        self._eng.set_export(self._lf, export, nargout=0)
        
    def acquire(self, timeout):
        """timeout in seconds"""
        self._lf_check()
        self._eng.acquire(self._lf, timeout, nargout=0)
