import smbus
import time


class TemperatureBrick(object):

    LM75_ADDRESS = 0x48
    LM75_TEMP_REGISTER = 0
    LM75_CONF_REGISTER = 1
    LM75_THYST_REGISTER = 2
    LM75_TOS_REGISTER = 3
    LM75_CONF_SHUTDOWN = 0
    LM75_CONF_OS_COMP_INT = 1
    LM75_CONF_OS_POL = 2
    LM75_CONF_OS_F_QUE = 3

    def __init__(self, mode=LM75_CONF_OS_COMP_INT, address=LM75_ADDRESS, busnum=1):
        self._mode = mode
        self._address = address
        self._bus = smbus.SMBus(busnum)

    def regdata2float (self, regdata):
        return (regdata / 32.0) / 8.0

    def toFah(self, temp):
        return (temp * (9.0/5.0)) + 32.0

    def getTemperature(self):
        raw = self._bus.read_word_data(self._address, LM75_TEMP_REGISTER) & 0xFFFF
        raw = ((raw << 8) & 0xFF00) + (raw >> 8)
        return self.regdata2float(raw)




class LightBrick(object):

    I2C_ADDR = 0x29

    def __init__(self, address=I2C_ADDR, busnum=1):
        self._address = address
        self._bus = smbus.SMBus(busnum)

        self._bus.write_byte_data(self._address, 0x00 | 0x80, 0x03)
        self._bus.write_byte_data(self._address, 0x01 | 0x80, 0x02)

        time.sleep(0.5)



    def getFullSpectrum(self):
        data = self._bus.read_i2c_block_data(self._address, 0x0C | 0x80, 2)
        data1 = self._bus.read_i2c_block_data(self._address, 0x0E | 0x80, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]

        return ch0



    def getInfraredSpectrum(self):
        data = self._bus.read_i2c_block_data(self._address, 0x0C | 0x80, 2)
        data1 = self._bus.read_i2c_block_data(self._address, 0x0E | 0x80, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]

        return ch1



    def getVisibleSpectrum():
        data = self._bus.read_i2c_block_data(self._address, 0x0C | 0x80, 2)
        data1 = self._bus.read_i2c_block_data(self._address, 0x0E | 0x80, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]

        return ch0 - ch1




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
        altitude = tHeight / 16.0

        return altitude


    def getTemperature(self):
        self._bus.write_byte_data(self._address, 0x26, 0xB9)
        self._bus.write_byte_data(self._address, 0x13, 0x07)
        self._bus.write_byte_data(self._address, 0x26, 0xB9)

        time.sleep(0.1)

        data = self._bus.read_i2c_block_data(self._address, 0x00, 6)

        # Convert the data to 20-bits
        temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        cTemp = temp / 16.0
        #fTemp = cTemp * 1.8 + 32

        return cTemp


    def getPressure(self):
        self._bus.write_byte_data(self._address, 0x26, 0x39)

        time.sleep(0.1)

        data = self._bus.read_i2c_block_data(self._address, 0x00, 4)

        # Convert the data to 20-bits
        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000

        return pressure
