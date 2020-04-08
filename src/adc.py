
A0 =  '/sys/bus/iio/devices/iio:device0/in_voltage0_raw'
A1 =  '/sys/bus/iio/devices/iio:device0/in_voltage1_raw'
A2 =  '/sys/bus/iio/devices/iio:device0/in_voltage2_raw'
A3 =  '/sys/bus/iio/devices/iio:device0/in_voltage3_raw'
A4 =  '/sys/bus/iio/devices/iio:device1/in_voltage0_raw'
A5 =  '/sys/bus/iio/devices/iio:device1/in_voltage1_raw'

DEFAULT_BURST_SIZE = 1024;


def readAdc(pinPath):
    f = open(pinPath, 'r')
    data = int(f.read())
    f.close()
    return data


def readBurst(pinPath, size=DEFAULT_BURST_SIZE):
    data = list()
    for i in range( 0, int(size) ):
        data.append( readAdc(pinPath) )
    return data
