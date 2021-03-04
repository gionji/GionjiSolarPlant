from lm75 import TemperatureBrick 
from mpl3115a2 import BarometricBrick
from tsl2561 import LightBrick


baro = BarometricBrick()
alt = baro.getAltitude()
press = baro.getPressure()
tempB = baro.getTemperature()


tempbrick = TemperatureBrick()
temp = tempbrick.getTemperature()

light = LightBrick()
lux = light.getFullSpectrum()



print(alt, press, tempB, temp, lux )
