import sys
import time

GPIO_EXPORT   = '/sys/class/gpio/export'
OS_PATH       = '/sys/class/gpio/gpio'
UDUBUNTU_PATH = '/gpio/gpio'

RELAY_PCB_PIN  = [24, 25, 26, 27]
RELAY_GPIO_NUM = [25, 22, 14, 15]


GPIO      = RELAY_GPIO_NUM 
GPIO_PATH = OS_PATH

RELAY = [ GPIO_PATH + str( GPIO[0] ) + '/',
               GPIO_PATH + str( GPIO[1] ) + '/',
               GPIO_PATH + str( GPIO[2] ) + '/',
               GPIO_PATH + str( GPIO[3] ) + '/', ]
               
HIGH = '0'
LOW  = '1'

INVERTER = RELAY[0]
EXTERNAL_POWER = RELAY[1]
PLUG_B = RELAY[2]
PLUG_A = RELAY[3]



def setupGpioDirection(gpios, gpiosNum):
    
    for elem in gpiosNum:
        f = open(GPIO_EXPORT, 'w+')
        f.write( elem )
        f.flush()
        f.close()
    
    for elem in gpios:
        f = open( elem + 'direction' , "w+")
        f.write('out')
        f.flush()
        f.close()


def turnOnSwitch(*relay):
    for elem in relay:
        f = open( elem + 'value' , "w+")
        f.write( HIGH )
        f.flush()
        f.close()


def turnOffSwitch(*relay):
    for elem in relay:    
        f = open( elem + 'value' , "w+")
        f.write( LOW )
        f.flush()
        f.close()

def enableExternalPower():
    turnOnSwitch(EXTERNAL_POWER)

def disableExternalPower():
    turnOffSwitch(EXTERNAL_POWER)

def enableInverter():
    turnOnSwitch(INVERTER)

def disableInverter():
    turnOffSwitch(INVERTER)


def main():
    #setupGpioDirection( RELAY, GPIO )

    turnOffSwitch(RELAY[0], RELAY[1], RELAY[2], RELAY[3] ) 
    
    time.sleep(1)
    
    turnOnSwitch(PLUG_A)
    enableInverter()

if __name__== "__main__":
    main()
