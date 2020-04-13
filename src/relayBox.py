import sys
import time

GPIO_EXPORT   = '/sys/class/gpio/export'
OS_PATH       = '/sys/class/gpio/gpio'
UDUBUNTU_PATH = '/gpio/gpio'
DOCKER_PATH  = '/var/gpio'

RELAY_PCB_PIN  = [24, 25, 26, 27]
RELAY_GPIO_NUM = [25, 22, 14, 15]


GPIO      = RELAY_GPIO_NUM 
GPIO_PATH = DOCKER_PATH


## gpio files paths for each relay
RELAY = [ GPIO_PATH + str( GPIO[0] ) + '/',
               GPIO_PATH + str( GPIO[1] ) + '/',
               GPIO_PATH + str( GPIO[2] ) + '/',
               GPIO_PATH + str( GPIO[3] ) + '/', ]
               
HIGH = '0'
LOW  = '1'

INVERTER       = RELAY[0]
EXTERNAL_POWER = RELAY[1]
PLUG_B         = RELAY[2]
PLUG_A         = RELAY[3]

PLUG_A_ID          = 'a'
PLUG_B_ID          = 'b'
INVERTER_ID        = 'i'
EXTERNAL_SOURCE_ID = 's'

PLUG_A_RELAY_NUMBER         = 3
PLUG_B_RELAY_NUMBER         = 2
EXTERNAL_POWER_RELAY_NUMBER = 1
INVERTER_RELAY_NUMBER       = 0



STATE_ON = '1'
STATE_OFF = '0'

RELAY_STATUS = [STATE_OFF, STATE_OFF, STATE_ON, STATE_ON]


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



def enablePlugA():
    RELAY_STATUS[ PLUG_A_RELAY_NUMBER ] = STATE_ON
    turnOnSwitch(PLUG_A)

def disablePlugA():
    RELAY_STATUS[ PLUG_A_RELAY_NUMBER ] = STATE_OFF
    turnOffSwitch(PLUG_A)

def enablePlugB():
    RELAY_STATUS[ PLUG_B_RELAY_NUMBER ] = STATE_ON
    turnOnSwitch(PLUG_B)

def disablePlugB():
    RELAY_STATUS[ PLUG_B_RELAY_NUMBER ] = STATE_OFF
    turnOffSwitch(PLUG_B)



def enableExternalPower():
    RELAY_STATUS[ EXTERNAL_POWER_RELAY_NUMBER ] = STATE_ON
    turnOnSwitch(EXTERNAL_POWER)

def disableExternalPower():
    RELAY_STATUS[ EXTERNAL_POWER_RELAY_NUMBER ] = STATE_OFF
    turnOffSwitch(EXTERNAL_POWER)

def enableInverter():
    RELAY_STATUS[ INVERTER_RELAY_NUMBER ] = STATE_ON
    turnOnSwitch(INVERTER)

def disableInverter():
    RELAY_STATUS[ INVERTER_RELAY_NUMBER ] = STATE_OFF
    turnOffSwitch(INVERTER)




def main():
    #setupGpioDirection( RELAY, GPIO )

    turnOffSwitch(RELAY[0], RELAY[1], RELAY[2], RELAY[3] ) 
    
    time.sleep(1)
    
    turnOnSwitch(PLUG_A)
    enableInverter()



if __name__== "__main__":
    main()
