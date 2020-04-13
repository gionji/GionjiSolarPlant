

## tet adc
def readAdc(pinPath):
    f = open(pinPath, 'r')
    data = int(f.read())
    f.close()
    return data


HOST_ADC_PATH = '/sys/bus/iio/devices/'
CONTAINER_ADC_PATH = '/var/adc/'

ADC_0_FILE = 'iio:device0/in_voltage0_raw'

ADC_0 = HOST_ADC_PATH + ADC_0_FILE 

print( "ADC0 file :  " + str(ADC_0) )

adc0 = readAdc( ADC_0 )

print( adc0 )


## test gpio export
HOST_GPIO_PATH =  '/sys/class/gpio/'
CONTAINER_GPIO_PATH = '/var/gpio/'

GPIO_ROOT = HOST_GPIO_PATH


GPIO_EXPORT     = GPIO_ROOT +  'export'
GPIO_PATH       = GPIO_ROOT +  'gpio'

LED_13_GPIO_NUMBER = '102'


print("Gpios export file: " + str( GPIO_EXPORT ) )

try:
    f = open(GPIO_EXPORT, 'w') 
    f.write( LED_13_GPIO_NUMBER )
    f.flush()
    f.close()
except Exception as e:
    print("Error exporting GPIO " + str(  LED_13_GPIO_NUMBER )+ " . " + str(e) )



## test gpio set direction
gpioDirection = GPIO_PATH + str( LED_13_GPIO_NUMBER ) + '/direction'

try:
    f = open( gpioDirection , 'w')
    f.write( 'in' )
    f.flush()
    f.close()
except Exception as e:
    print("Error changing direction GPIO " + str(  LED_13_GPIO_NUMBER )+ " . " + str(e) )


## tesst gpio read
gpio = GPIO_PATH + str( LED_13_GPIO_NUMBER ) + '/value'
gpioValue = readAdc( gpio )
print( gpioValue )



import time
## test pio write

gpioDirection = GPIO_PATH + str( LED_13_GPIO_NUMBER ) + '/direction'
f = open( gpioDirection , 'w')
f.write( 'out' )
f.flush()
f.close()



print( gpio )

f = open( gpio , 'w')

for i in range(0, 10):
    try:
        f.write( '1' )
        f.flush()

        time.sleep(0.1)
    except:
        print("Error vontrolling GPIO")

    try:
        f.write( '0' )
        f.flush()

        time.sleep(0.1)
    except:
        print("Error vontrolling GPIO")










