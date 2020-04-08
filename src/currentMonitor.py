import time
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import platform
import math

import adc

ADC        = [ adc.A0, adc.A1, adc.A2, adc.A3 ]
IRRADIANCE = adc.A5

CURRENT_BIAS  = [      2123.0 ,      2135.0 ,  2088.0 , 0, 0 , 0 ]
CURRENT_SCALE = [ 0.000356589 , 0.000356589 ,     155 , 1, 1 , 1 ]


PLUG_1   = 0
PLUG_2   = 1
INVERTER = 2


def calculateCurrentBias(pin):
    # enableInverter()
    # turnOffRelay()

    size = adc.DEFAULT_BURST_SIZE

    pinPath = ADC[pin]
    data = adc.readBurst(pinPath, size)
    mean = 0

    for i in data:
        mean = mean + i

    mean = mean / size

    global CURRENT_BIAS
    CURRENT_BIAS[pin] = mean

    return mean



def calculateCurrentCC(pin, size=adc.DEFAULT_BURST_SIZE):
    mean = 0
    data = adc.readBurst(ADC[pin], size)
    for i in data:
        mean = mean + i

    mean = mean / size
    res = (mean - CURRENT_BIAS[pin]) / CURRENT_SCALE[pin]

    return res



def calculateCurrentIrms(pin, size=adc.DEFAULT_BURST_SIZE):
    mean = 0
    data = adc.readBurst( ADC[pin], size )
    data = [x - CURRENT_BIAS[pin] for x in data]

    #print("Current bias = " + str(CURRENT_BIAS[pin]))

    for d in data:
        mean = mean + (d * d)

    irms = CURRENT_SCALE[pin] * math.sqrt(mean)

    return irms


def getCurrentPlug1():
    return calculateCurrentIrms( PLUG_1 )


def getCurrentPlug2():
    return calculateCurrentIrms( PLUG_2 )


def getCurrentInverter():
    return calculateCurrentCC( INVERTER )

'''
while(True):
    meanPlug1 = calculateCurrentBias( PLUG_1 )
#    meanPlug2 = calculateCurrentBias( PLUG_2 )

    currentPlug1 = calculateCurrentIrms( PLUG_1 )
#    currentPlug2 = calculateCurrentIrms( PLUG_2 )

    currentDcAc = calculateCurrentCC( INVERTER )

    irr = getIrradiation()

    print(meanPlug1, currentPlug1,  currentDcAc, irr)
'''
