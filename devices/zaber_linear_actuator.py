"""Zaber Linear Actuator

This module is designed to control the Zaber T-NA08A25 Linear Actuator
using RS232 serial communication.

Developed by Hayden Jones for usage in QuIN Lab.

"""

__authors__ = "Hayden Jones"
__copyright__ = "Copyright 2016, QuIN Lab"
__credits__ = ["Hayden Jones"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Hayden Jones"
__email__ = "h4jones@uwaterloo.ca"
__status__ = "Production"

import serial
import struct
import time
import operator


class ZaberLinearActuator:

    def __init__(self, com_port=None):
        self._is_open = False
        if com_port is not None:
            self.open(com_port)
            
    def open(self, com_port):
        if self._is_open is True:
            return
        self._device = serial.Serial("COM{0}".format(com_port),
                                     9600,
                                     8,
                                     'N',
                                     1,
                                     timeout=1)
        devices = self.renumber(0)
        self._num_devices = len(devices)
        self._is_open = True
        
    def close(self):
        if self._is_open is False:
            return
        self._device.close()
        self._is_open = False

    def _send(self, id_num, command, data):
        # send command and data to device id_num
        self._device.write(struct.pack('<BBl', id_num, command, data))
        
    def _receive(self):
        # get one response and return the device command and data
        reply_bits = [0, 0, 0, 0, 0, 0]
        for i in range(0, 6, 1):
            reply_bits[i] = ord(self._device.read())
        reply = ((256 ** 3 * reply_bits[5])
                 + (256 ** 2 * reply_bits[4])
                 + (256 * reply_bits[3])
                 + reply_bits[2])
        if reply_bits[5] > 127:
            reply -= 256 ** 4
        if reply_bits[1] == 255:
            self._error(reply)
        return [reply_bits[0], reply_bits[1], reply]
        
    def _flush(self):
        # flush serial
        self._device.flushInput()
        self._device.flushOutput()
        
    def _error(self, error_code):
        # raise an appropriate error for the error_code which was read
        errors = {
            1: "Cannot Home",
            2: "Device Number Invalid",
            14: "Voltage Low",
            15: "Voltage High",
            18: "Stored Position Invalid",
            20: "Absolute Position Invalid",
            21: "Relative Position Invalid",
            22: "Velocity Invalid",
            36: "Peripheral ID Invalid",
            37: "Resolution Invalid",
            38: "Run Current Invalid",
            39: "Hold Current Invalid",
            40: "Mode Invalid",
            41: "Home Speed Invalid",
            42: "Speed Invalid",
            43: "Acceleration Invalid",
            44: "Maximum Range Invalid",
            45: "Current Position Invalid",
            46: "Maximum Relative Move Invalid",
            47: "Offset Invalid",
            48: "Alias Invalid",
            49: "Lock State Invalid",
            53: "Setting Invalid",
            64: "Command Invalid",
            255: "Busy",
            1600: "Save Position Invalid",
            1601: "Save Position Not Homed",
            1700: "Return Position Invalid",
            1800: "Move Position Invalid",
            1801: "Move Position Not Homed",
            2146: "Relative Position Limited",
            3600: "Settings Locked",
            4008: "Disable Auto Home Invalid",
            4010: "Bit 10 Invalid",
            4012: "Home Switch Invalid",
            4013: "Bit 13 Invalid" 
        }
        raise Exception(errors[error_code])
    
    def reset(self, id_num):
        # id_num = 0 for all reset
        # simulate power cycling
        self._flush()
        self._send(id_num, 0, 0)
        
    def home(self, id_num):
        # home id_num, return final position
        self._flush()
        self._send(id_num, 1, 0)
        position = []
        while True:
            while self._device.inWaiting() != 0:
                reply = self._receive()
                position.append([reply[0], reply[2]])
            if id_num == 0 and len(position) == self._num_devices:
                break
            elif not id_num == 0 and len(position) != 0:
                break
        position.sort(key=operator.itemgetter(0))
        return position

    def renumber(self, id_num, number=0):
        # renumbers devices properly, return device ids
        # number is used if setting an id_num to a new number
        # number defaults to id_num if no number is given
        self._flush()
        if id_num != 0 and number == 0:
            number = id_num
        self._send(id_num, 2, number)
        time.sleep(1)
        numbering = True
        device_id = []
        while numbering is True:
            while self._device.inWaiting() != 0:
                reply = self._receive()
                device_id.append([reply[0], reply[2]])
            numbering = False
        device_id.sort(key=operator.itemgetter(0))
        return device_id
    
    def sto_curr_pos(self, id_num, address):
        # store current position, persistent after power cycling/reset
        # address of the register to save position, 0-15
        # return save address
        self._flush()
        self._send(id_num, 16, address)
        saving = True
        save_address = []
        while saving is True:
            while self._device.inWaiting() != 0:
                reply = self._receive()
                save_address.append([reply[0], reply[2]])
            if id_num == 0 and len(save_address) != self._num_devices:
                continue
            saving = False
        save_address.sort(key=operator.itemgetter(0))
        return save_address
        
    def get_sto_pos(self, id_num, address):
        # get the stored position at address
        self._flush()
        self._send(id_num, 17, address)
        reading = True
        position = []
        while reading is True:
            while self._device.inWaiting() != 0:
                reply = self._receive()
                position.append([reply[0], reply[2]])
            if id_num == 0 and len(position) != self._num_devices:
                continue
            reading = False
            position.sort(key=operator.itemgetter(0))
        return position

    def goto_sto_pos(self, id_num, address):
        # go to stored position at address
        # return final position
        self._flush()
        self._send(id_num, 18, address)
        idle = False
        position = []
        while idle is False:
            while self._device.inWaiting() != 0:
                reply = self._receive()
                position.append([reply[0], reply[2]])
            if id_num == 0 and len(position) != self._num_devices:
                continue
            idle = False
            position.sort(key=operator.itemgetter(0))
        return position
        
    def goto_pos(self, id_num, position):
        # go to position
        # return final position
        self._flush()
        self._send(id_num, 20, position)
        idle = False
        position = []
        while idle is False:
            while self._device.inWaiting() != 0:
                reply = self._receive()
                position.append([reply[0], reply[2]])
            if id_num == 0 and len(position) != self._num_devices:
                continue
            idle = True
            position.sort(key=operator.itemgetter(0))
        return position
        
    def goby_dist(self, id_num, distance):
        # move relative distance
        # return final position
        self._flush()
        self._send(id_num, 21, distance)
        idle = False
        while idle == False:
            if self._device.inWaiting() != 0:
                idle = True
        final_position = []
        if id_num == 0:
            while self._device.inWaiting() != 0:
                reply = self._receive()
                final_position.append([reply[0], reply[2]])
            final_position.sort(key=operator.itemgetter(0))
        else:
            reply = self._receive()
            final_position = reply[2]
        return final_position
      
    def get_status(self, id_num):
        # return status of device
        # 0 idle, 1 home, 10 manual move, 18 sto move, 20 goto, 21 goby, 22 gospeed, 23 stopping
        # flushing true or false, false if no flush before running command (useful in other commands)
        self._flush()
        self._send(id_num, 54, 0)
        time.sleep(0.02)
        status = []
        if id_num == 0:
            for i in range(0, self._num_devices, 1):
                status.append(self._receive())
            status.sort(key=operator.itemgetter(0))
        else:
            status = self._receive()
        return status

    def get_current_pos(self, id_num):
        """Return the current position of the device(s) specified.
        
        Parameters
        ----------
        id_num : int
            The id_num ID of the device to query, or 0 for all devices.
        """
        self._flush()
        self._send(id_num, 60, 0)
        position = []
        reading = True
        while reading is True:
            while self._device.inWaiting() != 0:
                reply = self._receive()
                position.append([reply[0], reply[2]])
            if id_num == 0 and len(position) != self._num_devices:
                continue
            reading = False
            position.sort(key=operator.itemgetter(0))
        return position
        
        