import time

A0 =  '/sys/bus/iio/devices/iio:device0/in_voltage0_raw'
A1 =  '/sys/bus/iio/devices/iio:device0/in_voltage1_raw'
A2 =  '/sys/bus/iio/devices/iio:device0/in_voltage2_raw'
A3 =  '/sys/bus/iio/devices/iio:device0/in_voltage3_raw'
A4 =  '/sys/bus/iio/devices/iio:device1/in_voltage0_raw'
A5 =  '/sys/bus/iio/devices/iio:device1/in_voltage1_raw'


BURST_SIZE = 2000;

def readAdc(pin):
    f = open(pin, 'r')
    data = int(f.read())
    f.close()
    return data


def readBurst(pin, size):
    data = list()
    for i in range( 0, int(size) ):
        data.append( readAdc(pin) )
    return data


start = time.time()

dataAdc = readBurst( A0, BURST_SIZE )
print(dataAdc[100:110])

dataAdc = readBurst( A1, BURST_SIZE )
print(dataAdc[100:110])

dataAdc = readBurst( A2, BURST_SIZE )
print(dataAdc[100:110])

dataAdc = readBurst( A3, BURST_SIZE )
print(dataAdc[100:110])

dataAdc = readBurst( A4, BURST_SIZE )
print(dataAdc[100:110])

dataAdc = readBurst( A5, BURST_SIZE )
print(dataAdc[100:110])



end = time.time()

interval = end - start


print( str(1/(interval*5 / BURST_SIZE)) + ' sampling frequency (Hz) ')
