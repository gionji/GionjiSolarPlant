import sys
import time


PATH_GPIO_UBUNTU    = '/sys/class/gpio/'
PATH_GPIO_UDOOBUNTU = '/gpio/'
PATH_GPIO_CONTAINER = '/var/gpio/'

GPIO_EXPORT_FILE = 'export'
GPIO_FOLDER_BASENAME = 'gpio'

PATH_GPIO = PATH_GPIO_UBUNTU


# pins numbers printend on the Udoo Neo PCB
RELAY_PCB_NUMBER  = [24, 25, 26, 27]
# correspondent gpio kernel numbers
RELAY_GPIO_NUMBER = [25, 22, 14, 15]


# Array with correspondant gpio number for each relay
GPIO      = RELAY_GPIO_NUMBER

# gpio path plus folder basename
GPIO_PATH   = PATH_GPIO + GPIO_FOLDER_BASENAME
GPIO_EXPORT = PATH_GPIO + GPIO_EXPORT_FILE  

## gpio files paths for each relay
# a RELAY is identified with its gpio folder path
RELAY = [ 
    GPIO_PATH + str( GPIO[0] ) + '/',
    GPIO_PATH + str( GPIO[1] ) + '/',
    GPIO_PATH + str( GPIO[2] ) + '/',
    GPIO_PATH + str( GPIO[3] ) + '/', 
]
               
# gpios output or input values
HIGH = '0'
LOW  = '1'

# relay associated with names
INVERTER       = RELAY[0]
EXTERNAL_POWER = RELAY[1]
PLUG_B         = RELAY[2]
PLUG_A         = RELAY[3]

# string literal label for each relay
PLUG_A_ID          = 'a'
PLUG_B_ID          = 'b'
INVERTER_ID        = 'i'
EXTERNAL_SOURCE_ID = 's'

# Relay numbers
PLUG_A_RELAY_NUMBER         = 3
PLUG_B_RELAY_NUMBER         = 2
EXTERNAL_POWER_RELAY_NUMBER = 1
INVERTER_RELAY_NUMBER       = 0

# on and of states
ON  = HIGH
OFF = LOW



## Relays status
RELAY_STATUS = [OFF, OFF, OFF, OFF]



def setupGpioDirection(gpiosNum):
    
    # export all the relaybox gpios
    for elem in gpiosNum:
        try:
            f = open(GPIO_EXPORT, 'w+')
            f.write( elem )
            f.flush()
            f.close()
        except:
            print( 'Error exporting gpio ' + str(elem) )
    
    # set the gpios in output
    for elem in gpiosNum:
        try:
            f = open( GPIO_PATH + str(elem) + '/direction' , "w+")
            f.write('out')
            f.flush()
            f.close()
        except:
            print( 'Error setting direction gpio ' + str(elem) )



def __turnOnSwitch(*relay):
    for elem in relay:
        f = open( elem + 'value' , "w+")
        f.write( HIGH )
        f.flush()
        f.close()



def __turnOffSwitch(*relay):
    for elem in relay:    
        f = open( elem + 'value' , "w+")
        f.write( LOW )
        f.flush()
        f.close()




def turnOffAllRelays():
    for i in range(0,3):
        try:
            f = open( RELAY[i] + 'value' , "w+")
            f.write( LOW )
            f.flush()
            f.close()
            RELAY_STATUS[ i ] = OFF
        except Exception as e:
            print("Error switching relay: " +str(e))



def turnOnAllRelays():
    for i in range(0,3):
        try:
            f = open( RELAY[i] + 'value' , "w+")
            f.write( HIGH )
            f.flush()
            f.close()
            RELAY_STATUS[ i ] = ON
        except Exception as e:
            print("Error switching relay: " +str(e))





def enablePlugA():
    try:
        __turnOnSwitch(PLUG_A)
        RELAY_STATUS[ PLUG_A_RELAY_NUMBER ] = ON
    except Exception as e:
        print("Error enabling plug A")


def disablePlugA():
    try:
        __turnOffSwitch(PLUG_A)
        RELAY_STATUS[ PLUG_A_RELAY_NUMBER ] = OFF
    except Exception as e:
        print("Error disabling plug A")
        


def enablePlugB():
    try:
        __turnOnSwitch(PLUG_B)
        RELAY_STATUS[ PLUG_B_RELAY_NUMBER ] = ON
    except Exception as e:
        print("Error enabling plug B")


def disablePlugB():
    try:
        __turnOffSwitch(PLUG_B)
        RELAY_STATUS[ PLUG_B_RELAY_NUMBER ] = OFF
    except Exception as e:
        print("Error disabling plug B")



def enableExternalPower():
    try:
        __turnOnSwitch(EXTERNAL_POWER)
        RELAY_STATUS[ EXTERNAL_POWER_RELAY_NUMBER ] = ON    
    except Exception as e:
        print("Error enabling External Power")


def disableExternalPower():
    try:
        __turnOffSwitch(EXTERNAL_POWER)
        RELAY_STATUS[ EXTERNAL_POWER_RELAY_NUMBER ] = OFF
    except Exception as e:
        print("Error disbling External Power")


def enableInverter():
    try:
        __turnOnSwitch(INVERTER)
        RELAY_STATUS[ INVERTER_RELAY_NUMBER ] = ON
    except Exception as e:
        print("Error enabling Inverter")


def disableInverter():
    try:
        __turnOffSwitch(INVERTER)
        RELAY_STATUS[ INVERTER_RELAY_NUMBER ] = OFF
    except Exception as e:
        print("Error disbling Inverter")




def init():

    print("Initialize GPIOs. Export and set direction ...")
    setupGpioDirection( GPIO )
    
    ## set initial relay states
    print("Switch off all the relays ...")
    turnOffAllRelays( )
    time.sleep(1)

    print("Set relays in their default states")
    enablePlugA( )
    enableInverter()

    print("Relaybox initilazation COMPLETE.")


