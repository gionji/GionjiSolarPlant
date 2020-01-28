import sys
import time

GPIO_PATH = '/gpio/gpio'

RELAY_1_PIN = 24
RELAY_2_PIN = 25
RELAY_3_PIN = 26
RELAY_4_PIN = 27

HIGH = '1'
LOW  = '0'

RELAY_1_PATH = GPIO_PATH + str( RELAY_1_PIN ) + '/' 
RELAY_2_PATH = GPIO_PATH + str( RELAY_2_PIN ) + '/'
RELAY_3_PATH = GPIO_PATH + str( RELAY_3_PIN ) + '/'
RELAY_4_PATH = GPIO_PATH + str( RELAY_4_PIN ) + '/'

SWITCH_1 = RELAY_1_PATH
SWITCH_2 = RELAY_2_PATH
SWITCH_3 = RELAY_2_PATH
SWITCH_4 = RELAY_2_PATH



def setupGpioDirection(*gpios):
    for elem in gpios:
        f = open( elem + 'direction' , "w+")
        f.write('out')
        f.flush()
        f.close()


def turnOnSwitch(relayId):
    f = open( elem + 'value' , "w+")
    f.write( HIGH )
    f.flush()
    f.close()


def turnOffSwitch(relayId):
    f = open( elem + 'value' , "w+")
    f.write( LOW )
    f.flush()
    f.close()


def main():
    setupGpioDirection(SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4)

    turnOnSwitch(SWITCH_1)
    time.sleep(1)
    turnOffSwitch(SWITCH_1)


if __name__== "__main__":
    main()
