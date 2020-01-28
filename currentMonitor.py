import time
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import platform
import math

A0 =  '/sys/bus/iio/devices/iio:device0/in_voltage0_raw'
A1 =  '/sys/bus/iio/devices/iio:device0/in_voltage1_raw'
A2 =  '/sys/bus/iio/devices/iio:device0/in_voltage2_raw'
A3 =  '/sys/bus/iio/devices/iio:device0/in_voltage3_raw'
A4 =  '/sys/bus/iio/devices/iio:device1/in_voltage0_raw'
A5 =  '/sys/bus/iio/devices/iio:device1/in_voltage1_raw'

ADC = [A0, A1, A2, A3]

CURRENT_BIAS  = [ 2123.0, 2135.0, 0 , 2088.0 , 0 , 0 ]
CURRENT_SCALE = [ 1 , 1 , 1 , 155 , 1 , 1 ]

DEFAULT_BURST_SIZE = 2048;

PLUG_1   = 0
PLUG_2   = 1
INVERTER = 3


def readAdc(pinPath):
    f = open(pinPath, 'r')
    data = int(f.read())
    f.close()
    return data


def readBurst(pinPath, size):
    data = list()
    for i in range( 0, int(size) ):
        data.append( readAdc(pinPath) )
    return data


def calculateCurrentBias(pin):
    # enableInverter()
    # turnOffRelay()

    size = DEFAULT_BURST_SIZE

    pinPath = ADC[pin]
    data = readBurst(pinPath, size)
    mean = 0

    for i in data:
        mean = mean + i

    mean = mean / size
    
    global CURRENT_BIAS
    CURRENT_BIAS[pin] = mean

    return mean



def calculateCurrentCC(pin, size=DEFAULT_BURST_SIZE):
    mean = 0
    data = readBurst(ADC[pin], size)
    for i in data:
        mean = mean + i

    mean = mean / size
    res = (mean - CURRENT_BIAS[pin]) / CURRENT_SCALE[pin]

    return res



def calculateCurrentIrms(pin, size=DEFAULT_BURST_SIZE):
    mean = 0
    data = readBurst( ADC[pin], size )
    data = [x - CURRENT_BIAS[pin] for x in data]

    for d in data:
        mean = mean + (d * d)

    irms = CURRENT_SCALE[pin] * math.sqrt(mean) 

    return irms



while(True):
    meanPlug1 = calculateCurrentBias( PLUG_1 )
    meanPlug2 = calculateCurrentBias( PLUG_2 )

    currentPlug1 = calculateCurrentIrms( PLUG_1 )
    currentPlug2 = calculateCurrentIrms( PLUG_2 )

    currentDcAc = calculateCurrentCC( INVERTER )

    print(meanPlug1, meanPlug2, currentPlug1, currentPlug2, currentDcAc)

#print(dataA0)

#Yfft = fft(dataA0)


