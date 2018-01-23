"""Newport 1830C v 1.0

This module is designed to control the Newport 1830-C Optical Power
Meter using GPIB communication.

Developed by Hayden Jones for usage in QuIN Lab.
"""

from time import sleep
import visa
rm = visa.ResourceManager()

class Newport1830C:
    """The Newport 1830-C optical power meter object.

    Parameters
    ----------
    gpib_addr : int
        The GPIB address number of the optical power meter.

    Methods
    -------
    open
        Opens the device at the given address.
    close
        Closes the currently active device.
    device_status
        Returns the status of the device connection.
    attenuator_off
        Turns off the attenuator of the photodetector.
    attenuator_on
        Turns on the attenuator of the photodetector.
    attenuator_status
        Returns the current status of the attenuator.
    beeper_off
        Turns off audio output.
    beeper_on
        Turns on audio output.
    beeper_status
        Returns the current status of the audio output.
    clear_status_register
        Clears the status byte register.
    get_power
        Returns the power level of the input signal.
    set_slow_display_filter
        Sets the display output to slow filtering mode.
    set_med_display_filter
        Sets the display output to medium filtering mode.
    set_no_display_filter
        Sets the display output to have no filtering.
    display_filter_status
        Returns the display filter status.
    disable_reading
        Stops power meter from taking new readings and parameters.
    enable_reading
        Enables power meter to take new readings and parameters.
    reading_status
        Returns the current status of the reading mode.
    backlight_off
        Turns the front panel backlight off.
    backlight_med
        Sets the front panel backlight to medium intensity.
    backlight_high
        Sets the front panel backlight to high intensity.
    backlight_status
        Returns the status of the front panel backlight intensity.
    local_lockout_off
        Disables the local lockout of the front panel.
    local_lockout_on
        Enables the local lockout of the front panel.
    local_lockout_status
        Returns the status of the local lockout of the front panel.
    status_byte
        Returns the status byte of the optical power meter.
    set_range
        Sets the signal range of the power meter.
    range_status
        Returns the current range signal setting.
    store_reference
        Stores the current input signal as the reference level.
    set_unit_watts
        Sets the current measurement unit to Watts.
    set_unit_db
        Sets the current measurement unit to dB.
    set_unit_dbm
        Sets the current measurement unit to dBm.
    set_unit_rel
        Sets the current measurement unit to REL.
    current_unit
        Returns the current unit of measurement being used.
    set_wavelength
        Sets the current wavelength of the input signal.
    get_wavelength
        Returns the current wavelength setting for the input signal.
    zero_off
        Turn off the zero function of the optical power meter.
    zero_on
        Zero the optical power meter with the next input signal.
    zero_status
        Returns the status of the zero function.

    """
    def __init__(self, gpib_addr):
        self._device = rm.open_resource("GPIB0::{0}::INSTR".format(gpib_addr))
        self._is_open = True

    def open(self, gpib_addr):
        """Opens the device at the given address.
        
        Parameters
        ----------
        gpib_addr : int
            The GPIB address number of the optical power meter.
        
        """
        if self._is_open is True:
            return
        self._device = rm.open_resource("GPIB0::{0}::INSTR".format(gpib_addr))
        self._is_open = True
        
    def close(self):
        """Closes the currently active device."""
        if self._is_open is False:
            return
        self._device.close()
        self._is_open = False
        
    def device_status(self):
        """Returns the status of the device connection.
        
        Returns
        -------
        int
            The status of being open (1) or closed (0).
        """
        return int(self._is_open)
        
    def attenuator_off(self):
        """Turns off the attenuator of the photodetector."""
        self._device.write("A0")

    def attenuator_on(self):
        """Turns on the attenuator of the photodetector."""
        self._device.write("A1")

    def attenuator_status(self):
        """Returns the current status of the attenuator.

        Returns
        -------
        int
            The state of on (1) or off (0).

        """
        self._device.write("A?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            status = self.attenuator_status()
        return status

    def beeper_off(self):
        """Turns off audio output."""
        self._device.write("B0")

    def beeper_on(self):
        """Turns on audio output."""
        self._device.write("B1")

    def beeper_status(self):
        """Returns the current status of the audio output.

        Returns
        -------
        int
            The state of on (1) or off (0).

        """
        self._device.write("B?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            status = self.beeper_status()
        return status

    def clear_status_register(self):
        """Clears the status byte register."""
        self._device.write("C")

    def get_power(self):
        """Returns the power level of the input signal.

        Returns
        -------
        float
            Power reading from the input signal.

        """
        self._device.write("D?")
        sleep(0.1)
        power = self._device.read().rstrip('\n')
        try:
            power = float(power)
        except ValueError:
            power = self.get_power()
        return power

    def set_slow_display_filter(self):
        """Sets the display output to slow filtering mode.

        The slow display filter outputs the average of the last 16
        measurements from the input signal.

        """
        self._device.write("F1")

    def set_med_display_filter(self):
        """Sets the display output to medium filtering mode.

        The medium display filter outputs the average of the last 4
        measurements from the input signal.

        """
        self._device.write("F2")

    def set_no_display_filter(self):
        """Sets the display output to have no filtering."""
        self._device.write("F3")

    def display_filter_status(self):
        """Returns the display filter status.

        Returns
        -------
        int
            The status of the filtering mode. 1 for slow filtering, 2
            for medium filtering, 3 for no filtering.

        """
        self._device.write("F?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            status = self.display_filter_status()
        return status

    def disable_reading(self):
        """Stops power meter from taking new readings and parameters."""
        self._device.write("G0")

    def enable_reading(self):
        """Enables power meter to take new readings and parameters."""
        self._device.write("G1")

    def reading_status(self):
        """Returns the current status of the reading mode.

        Returns
        -------
        int
            The state of enabled (1), or disabled (0).

        """
        self._device.write("G?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            status = self.reading_status()
        return status

    def backlight_off(self):
        """Turns the front panel backlight off."""
        self._device.write("K0")

    def backlight_med(self):
        """Sets the front panel backlight to medium intensity."""
        self._device.write("K1")

    def backlight_high(self):
        """Sets the front panel backlight to high intensity."""
        self._device.write("K2")

    def backlight_status(self):
        """Returns the status of the front panel backlight intensity.

        Returns
        -------
        int
            The status of the backlight intensity. 0 for backlight off,
            1 for medium intensity, 2 for high intensity.

        """
        self._device.write("K?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            status = self.backlight_status()
        return status

    def local_lockout_off(self):
        """Disables the local lockout of the front panel."""
        self._device.write("L0")

    def local_lockout_on(self):
        """Enables the local lockout of the front panel."""
        self._device.write("L1")

    def local_lockout_status(self):
        """Returns the status of the local lockout of the front panel.

        Returns
        -------
        int
            The state of the local lockout, on (1) or off (0).

        """
        self._device.write("L?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            status = self.local_lockout_status()
        return status

    def status_byte(self):
        """Returns the status byte of the optical power meter.

        Returns
        -------
        list of int
            The list of ints representing the status byte in binary.
            Bit 0 is a parameter error.
            Bit 1 is a command error.
            Bit 2 is an input signal saturation error.
            Bit 3 is an input signal exceeds maximum range error.
            Bit 4 signifies a response is available.
            Bit 5 signifies the optical power meter is in an
                auto-ranging or power up state.
            Bit 7 signifies a new power reading is abailable.

        """
        self._device.write("Q?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            return self.status_byte()
        binary_status = bin(int(status))
        return [int(x) for x in binary_status[2:]]

    def set_range(self, setting):
        """Sets the signal range of the power meter.

        Parameters
        ----------
        setting : int
            The setting for the signal range. 0 corresponds to the auto
            range setting. 1 is the lowest setting, 8 is the highest.
            Each time the signal range is incremented by 1, the signal
            gain decreases by a decade.

        """
        self._device.write("R{0}".format(setting))

    def range_status(self):
        """Returns the current range signal setting.

        Returns
        -------
        int
            The setting for the signal range. 1 is the lowest setting,
            8 is the highest. Everytime the signal range is incremented
            by 1, the signal decreases by a decade.

        """
        self._device.write("R?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            status = self.range_status()
        return status

    def store_reference(self):
        """Stores the current input signal as the reference level."""
        self._device.write("S")

    def set_unit_watts(self):
        """Sets the current measurement unit to Watts."""
        self._device.write("U1")

    def set_unit_db(self):
        """Sets the current measurement unit to dB."""
        self._device.write("U2")

    def set_unit_dbm(self):
        """Sets the current measurement unit to dBm."""
        self._device.write("U3")

    def set_unit_rel(self):
        """Sets the current measurement unit to REL."""
        self._device.write("U4")

    def current_unit(self):
        """Returns the current unit of measurement being used.

        Returns
        -------
        int
            The current measurement unit setting. 1 is W, 2 is dB, 3 is
            dBm, and 4 is REL.

        """
        self._device.write("U?")
        sleep(0.1)
        try:
            unit = int(self._device.read().rstrip('\n'))
        except ValueError:
            unit = self.current_unit()
        return unit

    def set_wavelength(self, wavelength):
        """Sets the current wavelength of the input signal.

        Parameters
        ----------
        wavelength : int
            The wavelength of the input signal from 0-9999 nm.

        """
        self._device.write("W{0}".format(wavelength))

    def get_wavelength(self):
        """Returns the current wavelength setting for the input signal.

        Returns
        -------
        int
            The wavelength setting in nm.

        """
        self._device.write("W?")
        sleep(0.1)
        try:
            wavelength = int(self._device.read().rstrip('\n'))
        except ValueError:
            wavelength = self.get_wavelength()
        return wavelength

    def zero_off(self):
        """Turn off the zero function of the optical power meter."""
        self._device.write("Z0")

    def zero_on(self):
        """Zero the optical power meter with the next input signal."""
        self._device.write("Z1")

    def zero_status(self):
        """Returns the status of the zero function.

        Returns
        -------
        int
            The state of on (1) or off (0).

        """
        self._device.write("Z?")
        sleep(0.1)
        try:
            status = int(self._device.read().rstrip('\n'))
        except ValueError:
            status = self.zero_status()
        return status
