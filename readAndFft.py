import time
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt

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



SCALE = 1
BIAS = 0

def currentCC(pin, size):
    mean = 0
    data = readBurst(pin, size)
    for i in data:
        mean = mean + i

    mean = mean / size

    res = (mean * SCALE) - BIAS
    return res


print(currentCC(A3, 128))



#print(dataA0)

#Yfft = fft(dataA0)


