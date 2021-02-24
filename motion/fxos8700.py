# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

try:
    import ustruct as struct
except ImportError:
    import struct

import smbus


# Register addresses and other constants:
_FXOS8700_ADDRESS = 0x1E  # 0011111
_FXOS8700_ID = 0xC7  # 1100 0111
_FXOS8700_REGISTER_STATUS = 0x00
_FXOS8700_REGISTER_OUT_X_MSB = 0x01
_FXOS8700_REGISTER_OUT_X_LSB = 0x02
_FXOS8700_REGISTER_OUT_Y_MSB = 0x03
_FXOS8700_REGISTER_OUT_Y_LSB = 0x04
_FXOS8700_REGISTER_OUT_Z_MSB = 0x05
_FXOS8700_REGISTER_OUT_Z_LSB = 0x06
_FXOS8700_REGISTER_WHO_AM_I = 0x0D  # 11000111   r
_FXOS8700_REGISTER_XYZ_DATA_CFG = 0x0E
_FXOS8700_REGISTER_CTRL_REG1 = 0x2A  # 00000000   r/w
_FXOS8700_REGISTER_CTRL_REG2 = 0x2B  # 00000000   r/w
_FXOS8700_REGISTER_CTRL_REG3 = 0x2C # 00000000   r/w
_FXOS8700_REGISTER_CTRL_REG4 = 0x2D  # 00000000   r/w
_FXOS8700_REGISTER_CTRL_REG5 = 0x2E  # 00000000   r/w
_FXOS8700_REGISTER_MSTATUS = 0x32
_FXOS8700_REGISTER_MOUT_X_MSB = 0x33
_FXOS8700_REGISTER_MOUT_X_LSB = 0x34
_FXOS8700_REGISTER_MOUT_Y_MSB = 0x35
_FXOS8700_REGISTER_MOUT_Y_LSB = 0x36
_FXOS8700_REGISTER_MOUT_Z_MSB = 0x37
_FXOS8700_REGISTER_MOUT_Z_LSB = 0x38
_FXOS8700_REGISTER_MCTRL_REG1 = 0x5B  # 00000000   r/w
_FXOS8700_REGISTER_MCTRL_REG2 = 0x5C  # 00000000   r/w
_FXOS8700_REGISTER_MCTRL_REG3 = 0x5D  # 00000000   r/w
_ACCEL_MG_LSB_2G = 0.000244
_ACCEL_MG_LSB_4G = 0.000488
_ACCEL_MG_LSB_8G = 0.000976
_MAG_UT_LSB = 0.1
_SENSORS_GRAVITY_STANDARD = 9.80665

# User-facing constants/module-level globals:
ACCEL_RANGE_2G = 0x00
ACCEL_RANGE_4G = 0x01
ACCEL_RANGE_8G = 0x02


def _twos_comp(val, bits):
    if val & (1 << (bits - 1)) != 0:
        return val - (1 << bits)
    return val


class FXOS8700:

    _BUFFER = bytearray(13)

    def __init__(self, i2c_channel=3, address=_FXOS8700_ADDRESS, accel_range=ACCEL_RANGE_2G):
        assert accel_range in (ACCEL_RANGE_2G, ACCEL_RANGE_4G, ACCEL_RANGE_8G)
        self._accel_range = accel_range
        self._address = address
        self._bus = smbus.SMBus(i2c_channel)

        # Check for chip ID value.
        if self._read_u8(_FXOS8700_REGISTER_WHO_AM_I) != _FXOS8700_ID:
            raise RuntimeError("Failed to find FXOS8700, check wiring!")

        # Set to standby mode (required to make changes to this register)
        self._write_u8(_FXOS8700_REGISTER_CTRL_REG1, 0)
        if accel_range == ACCEL_RANGE_2G:
            self._write_u8(_FXOS8700_REGISTER_XYZ_DATA_CFG, 0x00)
        elif accel_range == ACCEL_RANGE_4G:
            self._write_u8(_FXOS8700_REGISTER_XYZ_DATA_CFG, 0x01)
        elif accel_range == ACCEL_RANGE_8G:
            self._write_u8(_FXOS8700_REGISTER_XYZ_DATA_CFG, 0x02)

        # High resolution
        self._write_u8(_FXOS8700_REGISTER_CTRL_REG2, 0x02)
        # Active, Normal Mode, Low Noise, 100Hz in Hybrid Mode
        self._write_u8(_FXOS8700_REGISTER_CTRL_REG1, 0x15)

        # Configure the magnetometer
        # Hybrid Mode, Over Sampling Rate = 16
        self._write_u8(_FXOS8700_REGISTER_MCTRL_REG1, 0x1F)
        # Jump to reg 0x33 after reading 0x06
        self._write_u8(_FXOS8700_REGISTER_MCTRL_REG2, 0x20)

    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        res = self._bus.read_byte_data( self._address , address)
        return res

    def _write_u8(self, address, val):
        # Write an 8-bit unsigned value to the specified 8-bit address.
        self._bus.write(self._address, address, val)


    def read_raw_accel_mag(self):
        """Read the raw accelerometer and magnetometer readings.  Returns a
        2-tuple of 3-tuples:

        - Accelerometer X, Y, Z axis 14-bit signed raw values
        - Magnetometer X, Y, Z axis 16-bit signed raw values

        If you want the acceleration or magnetometer values in friendly units
        consider using the accelerometer and magnetometer properties!
        """
        # Read accelerometer data from sensor.
        res = self._bus.read_i2c_block_data(self._address, _FXOS8700_REGISTER_OUT_X_MSB, 8)
        accel_raw_x = struct.unpack_from(">H", res[0:2])[0]
        accel_raw_y = struct.unpack_from(">H", res[2:4])[0]
        accel_raw_z = struct.unpack_from(">H", res[4:6])[0]
        # Convert accelerometer data to signed 14-bit value from 16-bit
        # left aligned 2's compliment value.
        accel_raw_x = _twos_comp(accel_raw_x >> 2, 14)
        accel_raw_y = _twos_comp(accel_raw_y >> 2, 14)
        accel_raw_z = _twos_comp(accel_raw_z >> 2, 14)
        # Read magnetometer data from sensor.  No need to convert as this is
        # 16-bit signed data so struct parsing can handle it directly.
        res = self._bus.read(self._address, _FXOS8700_REGISTER_MOUT_X_MSB, 8)
        mag_raw_x = struct.unpack_from(">h", self._BUFFER[0:2])[0]
        mag_raw_y = struct.unpack_from(">h", self._BUFFER[2:4])[0]
        mag_raw_z = struct.unpack_from(">h", self._BUFFER[4:6])[0]
        return (
            (accel_raw_x, accel_raw_y, accel_raw_z),
            (mag_raw_x, mag_raw_y, mag_raw_z),
        )

    @property
    def accelerometer(self):
        """Read the acceleration from the accelerometer and return its X, Y, Z axis values as a
        3-tuple in m/s^2.
        """
        accel_raw, _ = self.read_raw_accel_mag()
        # Convert accel values to m/s^2
        factor = 0
        if self._accel_range == ACCEL_RANGE_2G:
            factor = _ACCEL_MG_LSB_2G
        elif self._accel_range == ACCEL_RANGE_4G:
            factor = _ACCEL_MG_LSB_4G
        elif self._accel_range == ACCEL_RANGE_8G:
            factor = _ACCEL_MG_LSB_8G
        return [x * factor * _SENSORS_GRAVITY_STANDARD for x in accel_raw]

    @property
    def magnetometer(self):
        """
        Read the magnetometer values and return its X, Y, Z axis values as a 3-tuple in uTeslas.
        """
        _, mag_raw = self.read_raw_accel_mag()
        # Convert mag values to uTesla
        return [x * _MAG_UT_LSB for x in mag_raw]
