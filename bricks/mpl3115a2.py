# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MPL3115A2
# This code is designed to work with the MPL3115A2_I2CS I2C Mini Module

import smbus
import time


class BarometricBrick(object):
    def __init__(self, address=0x60, busnum=1):
        self._address = address
        self._bus = smbus.SMBus(busnum)    


    def getAltitude(self):
        self._bus.write_byte_data(self._address, 0x26, 0xB9)
        self._bus.write_byte_data(self._address, 0x13, 0x07)
        self._bus.write_byte_data(self._address, 0x26, 0xB9)

        time.sleep(0.1)

        data = self._bus.read_i2c_block_data(self._address, 0x00, 6)

        # Convert the data to 20-bits
        tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        altitude = tHeight / 16.0
        cTemp = temp / 16.0
        fTemp = cTemp * 1.8 + 32

        return altitude


    def getTemperature(self):
        self._bus.write_byte_data(self._address, 0x26, 0xB9)
        self._bus.write_byte_data(self._address, 0x13, 0x07)
        self._bus.write_byte_data(self._address, 0x26, 0xB9)

        time.sleep(0.1)

        data = self._bus.read_i2c_block_data(self._address, 0x00, 6)

        # Convert the data to 20-bits
        tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        altitude = tHeight / 16.0
        cTemp = temp / 16.0
        fTemp = cTemp * 1.8 + 32

        return cTemp


    def getPressure(self):
        self._bus.write_byte_data(self._address, 0x26, 0x39)

        time.sleep(0.1)

        data = self._bus.read_i2c_block_data(self._address, 0x00, 4)

        # Convert the data to 20-bits
        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000

        return pressure
