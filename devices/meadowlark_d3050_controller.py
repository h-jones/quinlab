"""Meadowlark D3050 Controller v 1.0

This module is designed to control the Meadowlark D3050 Controller
using RS232 serial communication.

Developed by Hayden Jones for usage in QuIN Lab.
"""

import serial


class MeadowlarkD3050Controller:
    """The Meadowlark D3050 Controller object.

    Parameters
    ----------
    com_port : int
        The COM port number used for communication with the controller.

    Methods
    -------
    open
        Opens the controller connection at the given COM port.
    close
        Closes the controller connection.
    is_open
        Returns the communication status of the communication.
    set_voltage
        Set the voltage of the specified channel of the controller.
    get_voltage
        Get the voltage of the specified channel of the controller.
    set_all_voltage
        Set the voltage of all the channels of the controller.
    get_all_voltage
        Get the voltage of all the channels of the controller.
    set_tne
        Set TNE mode with given parameters on the specified channel.
    get_tne
        Get the TNE settings of the specified channel.
    sync_pulse
        Send a sync pulse to the front panel sync connector.
    external_input
        Enable external input control on the specified channels.
    get_temperature
        Get current temperature of temperature controlled LC device.
    set_temperature_setpoint
        Set temperature setpoint for temperature control.
    get_temperature_setpoint
        Get current temperature setpoint for temperature control.
    get_firmware
        Get controller firmware version and copyright string.

    """
    def __init__(self, com_port):
        self._device = serial.Serial("COM{0}".format(com_port),
                                     38400,
                                     8,
                                     'N',
                                     1,
                                     timeout=1)
        self._is_open = True
        
    def open(self, com_port):
        """Opens the controller connection at the given COM port.
        
        Parameters
        ----------
        com_port : int
            The COM port number used for controller communication.
        """
        if self._is_open is True:
            return
        self._device = serial.Serial("COM{0}".format(com_port),
                                     38400,
                                     8,
                                     'N',
                                     1,
                                     timeout=1)
        self._is_open = True
        
    def close(self):
        """Closes the controller connection."""
        if self._is_open is False:
            return
        self._device.close()
        self._is_open = False
        
    def is_open(self):
        """Returns the communication status of the communication.
        
        Returns
        -------
        bool
            The communication status open (True) or closed (False).
            
        """
        return self._is_open

    def set_voltage(self, channel, voltage):
        """Set the voltage of the specified channel of the controller.

        Parameters
        ----------
        channel : int
            Channel of the controller from 1-4.
        voltage : float
            Voltage setting from 0-10 V.
        """
        conv_voltage = int(voltage * 6553.5)
        command_str = "ld:{0},{1}\r".format(channel, conv_voltage)
        self._device.write(command_str.encode())
        self._device.readline()

    def get_voltage(self, channel):
        """Get the voltage of the specified channel of the controller.

        Parameters
        ----------
        channel : int
            Channel of the controller from 1-4.

        Returns
        -------
        float
            The voltage of the specified channel.

        """
        command_str = "ld:{0},?\r".format(channel)
        self._device.write(command_str.encode())
        voltage = self._device.readline().decode().split(':')[1]
        voltage = voltage.split(',')[1].rstrip('\r\n')
        return float(int(voltage) / 6553.5)

    def set_all_voltage(self, v1, v2, v3, v4):
        """Set the voltage of all the channels of the controller.

        Parameters
        ----------
        v1, v2, v3, v4 : float
            Voltage setting from 0-10 V.
            `v1` setting for channel 1. `v2` setting for channel 2.
            `v3` setting for channel 3. `v4` setting for channel 4.

        """
        conv_v1 = int(v1 * 6553.5)
        conv_v2 = int(v2 * 6553.5)
        conv_v3 = int(v3 * 6553.5)
        conv_v4 = int(v4 * 6553.5)
        command_str = "ldd:{0},{1},{2},{3}\r".format(conv_v1, conv_v2, conv_v3, conv_v4)
        self._device.write(command_str.encode())
        self._device.readline()

    def get_all_voltage(self):
        """Get the voltage of all the channels of the controller.

        Returns
        -------
        list of float
            Returns list of floats representing the voltage from each
            channel. The list is sorted according to channel number,
            where the first item is channel 1, and the last item is
            channel 4.

        """
        self._device.write(b"ldd:?\r")
        voltage = self._device.readline().decode()
        voltage = voltage.split(':')[1].rstrip('\r\n')
        return [float(int(x) / 6553.5) for x in voltage.split(',') if x.isdigit()]

    def set_tne(self, channel, duration, amplitude):
        """Set TNE mode with given parameters on the specified channel.

        Parameters
        ----------
        channel : int
            Channel of the controller from 1-4.
        duration : int
            Duration of the pulse, from 0-255 ms. A 0 ms time setting
            turns off TNE.
        amplitude : float
            Amplitude of the pulse, from 0-10 V.

        """
        conv_amplitude = int(amplitude * 6553.5)
        command_str = "tne:{0},{1},{2}\r".format(channel, duration, conv_amplitude)
        self._device.write(command_str.encode())
        self._device.readline()

    def get_tne(self, channel):
        """Get the TNE settings of the specified channel.

        Parameters
        ----------
        channel : int
            Channel of the controller from 1-4.

        Returns
        -------
        list of int, float
            Returns the duration of the TNE pulse in ms at index 0, and
            returns the amplitude of the TNE pulse in V at index 1.

        """
        # channel 1-4
        command_str = "tne:{0},?\r".format(channel)
        self._device.write(command_str.encode())
        tne = self._device.readline().decode().split(':')[1].rstrip('\r\n')
        tne = [int(x) for x in tne[1:].split(',') if x.isdigit()]
        tne[1] = float(tne[1] / 6553.5)
        return tne

    def sync_pulse(self):
        """Send a sync pulse to the front panel sync connector."""
        self._device.write(b"sout:\r")
        self._device.readline()

    def external_input(self, channel):
        """Enable external input control on the specified channels.

        Parameters
        ----------
        channel : int
            Integer from 0-15 representing the channels to enable
            external input on.
            Bit 0 is channel 1, Bit 1 is channel 2, etc.
            For example: 0 is no channels, 15 is all channels.

        """
        command_str = "extin:{0}\r".format(channel)
        self._device.write(command_str.encode())
        self._device.readline()

    def get_temperature(self):
        """Get current temperature of temperature controlled LC device.

        Returns
        -------
        float
            Temperature reading in Kelvin from the device.

        """
        self._device.write(b"tmp:?\r")
        temp = self._device.readline().decode().split(':')[1].rstrip('\r\n')
        return float((int(temp) * 500) / 65535)

    def set_temperature_setpoint(self, temperature):
        """Set temperature setpoint for temperature control.

        Parameters
        ----------
        temperature : float
            Temperature setpoint setting from 0-500 Kelvin.
        """
        conv_temperature = int((temperature * 16383) / 500)
        command_str = "tsp:{0}\r".format(conv_temperature)
        self._device.write(command_str.encode())
        self._device.readline()

    def get_temperature_setpoint(self):
        """Get current temperature setpoint for temperature control.

        Returns
        -------
        float
            Current temperature setpoint setting in Kelvin.

        """
        # return 0-500 K
        self._device.write(b"tsp:?\r")
        temp = self._device.readline().decode().split(':')[1].rstrip('\r\n')
        return float((int(temp) * 500) / 16383)

    def get_firmware(self):
        """Get controller firmware version and copyright string.

        Returns
        -------
        str
            Controller firmware version and copyright string.

        """
        self._device.write(b"ver:?\r")
        return self._device.readline().decode().rstrip('\r\n')
