import sys
import time


##########################################################3
class BoardType:
    NEO = 0x01
    C23 = 0x02

class OsType:
    UBUNTU_1804 = 0x11
    UDUBUNTU_1404 = 0x12
    DOCKER = 0x13

###########################################################
# Relay numbers
PLUG_A_RELAY_NUMBER         = 3
PLUG_B_RELAY_NUMBER         = 2
EXTERNAL_POWER_RELAY_NUMBER = 1
INVERTER_RELAY_NUMBER       = 0

osType = OsType.UBUNTU_1804
boardType = BoardType.NEO
###############################################################3

PATH_GPIO_UBUNTU    = '/sys/class/gpio/'
PATH_GPIO_UDOOBUNTU = '/gpio/'
PATH_GPIO_CONTAINER = '/var/gpio/'

GPIO_EXPORT_FILE     = 'export'
GPIO_FOLDER_BASENAME = 'gpio'

# pins numbers printend on the Udoo Neo PCB
RELAY_PCB_NUMBER_NEO  = [24, 25, 26, 27]
# correspondent gpio kernel numbers
RELAY_GPIO_NUMBER_NEO = [25, 22, 14, 15]

# gpios output or input values
HIGH = True
LOW  = False

# on and of states
ON  = HIGH
OFF = LOW

# string literal label for each relay
PLUG_A_ID          = 'a'
PLUG_B_ID          = 'b'
INVERTER_ID        = 'i'
EXTERNAL_SOURCE_ID = 's'

###################################################

if osType == OsType.UBUNTU_1804:
    PATH_GPIO = PATH_GPIO_UBUNTU
elif osType == OsType.UDUBUNTU_1404:
    PATH_GPIO = PATH_GPIO_UDOOBUNTU
elif osType == OsType.DOCKER:
    PATH_GPIO = PATH_GPIO_CONTAINER

if boardType == BoardType.NEO:
    RELAY_GPIO_NUMBER = RELAY_GPIO_NUMBER_NEO


# Array with correspondant gpio number for each relay
GPIO      = RELAY_GPIO_NUMBER

# gpio path plus folder basename
GPIO_PATH   = PATH_GPIO + GPIO_FOLDER_BASENAME
GPIO_EXPORT = PATH_GPIO + GPIO_EXPORT_FILE

## gpio files paths for each relay
# a RELAY is identified with its gpio folder path
RELAY_FOLDER_PATH = [
    GPIO_PATH + str( GPIO[0] ) + '/',
    GPIO_PATH + str( GPIO[1] ) + '/',
    GPIO_PATH + str( GPIO[2] ) + '/',
    GPIO_PATH + str( GPIO[3] ) + '/',
]

# realy function associated with gpio os path
INVERTER       = RELAY_FOLDER_PATH[ INVERTER_RELAY_NUMBER ]
EXTERNAL_POWER = RELAY_FOLDER_PATH[ EXTERNAL_POWER_RELAY_NUMBER ]
PLUG_B         = RELAY_FOLDER_PATH[ PLUG_B_RELAY_NUMBER ]
PLUG_A         = RELAY_FOLDER_PATH[ PLUG_A_RELAY_NUMBER ]




class RelayBox:

    ## Relays status
    relay_status = [OFF, OFF, ON, ON]

    def __init__(self, boardType = BoardType.NEO, osType = OsType.UBUNTU_1804):

        print("Initialize GPIOs. Export and set direction ...")
        self.setupGpioDirection( GPIO )

        self.__setLocalPaths(boardType, osType)

        ## set initial relay states
        print("Switch off all the relays ...")
        self.turnOffAllRelays( )
        time.sleep(1)

        print("Set relays in their default states")

        print("Relaybox initilazation COMPLETE.")


    def __setLocalPaths(self, boardType, osType):
        if osType == OsType.UBUNTU_1804:
            PATH_GPIO = PATH_GPIO_UBUNTU
        elif osType == OsType.UDUBUNTU_1404:
            PATH_GPIO = PATH_GPIO_UDOOBUNTU
        elif osType == OsType.DOCKER:
            PATH_GPIO = PATH_GPIO_CONTAINER

        if boardType == BoardType.NEO:
            RELAY_GPIO_NUMBER = RELAY_GPIO_NUMBER_NEO



    def setupGpioDirection(self, gpiosNum):

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



    def __turnOnSwitch(self, *relay):
        for elem in relay:
            f = open( elem + 'value' , "w+")
            f.write( HIGH )
            f.flush()
            f.close()



    def __turnOffSwitch(self, *relay):
        for elem in relay:
            f = open( elem + 'value' , "w+")
            f.write( LOW )
            f.flush()
            f.close()


    def turnOffAllRelays(self):
        for i in range(0,3):
            try:
                f = open( RELAY_FOLDER_PATH[i] + 'value' , "w+")
                f.write( LOW )
                f.flush()
                f.close()
                self.relay_status[ i ] = OFF
            except Exception as e:
                print("Error switching relay: " +str(e))
        return self.relay_status


    def turnOnAllRelays(self):
        for i in range(0,3):
            try:
                f = open( RELAY_FOLDER_PATH[i] + 'value' , "w+")
                f.write( HIGH )
                f.flush()
                f.close()
                self.relay_status[ i ] = ON
            except Exception as e:
                print("Error switching relay: " +str(e))
        return self.relay_status


    def setRelayState(self, relay_id, state):
        if state:
            state = ON
        else:
            state = OFF

        try:
            f = open( RELAY_FOLDER_PATH[relay_id] + 'value' , "w+")
            f.write( state )
            f.flush()
            f.close()
            self.relay_status[ relay_id ] = state
            print('RelayBox: ' + str(self.relay_status))
        except Exception as e:
            print("Error switching...")
        finally:
            return self.relay_status


    def enablePlugA(self):
        try:
            __turnOnSwitch(PLUG_A)
            self.relay_status[ PLUG_A_RELAY_NUMBER ] = ON
        except Exception as e:
            print("Error enabling plug A")

        return self.relay_status


    def disablePlugA(self):
        try:
            __turnOffSwitch(PLUG_A)
            self.relay_status[ PLUG_A_RELAY_NUMBER ] = OFF
        except Exception as e:
            print("Error disabling plug A")

        return self.relay_status



    def enablePlugB(self):
        try:
            __turnOnSwitch(PLUG_B)
            self.relay_status[ PLUG_B_RELAY_NUMBER ] = ON
        except Exception as e:
            print("Error enabling plug B")

        return self.relay_status


    def disablePlugB(self):
        try:
            __turnOffSwitch(PLUG_B)
            self.relay_status[ PLUG_B_RELAY_NUMBER ] = OFF
        except Exception as e:
            print("Error disabling plug B")

        return self.relay_status



    def enableExternalPower(self):
        try:
            __turnOnSwitch(EXTERNAL_POWER)
            self.relay_status[ EXTERNAL_POWER_RELAY_NUMBER ] = ON
        except Exception as e:
            print("Error enabling External Power")

        return self.relay_status


    def disableExternalPower(self):
        try:
            __turnOffSwitch(EXTERNAL_POWER)
            self.relay_status[ EXTERNAL_POWER_RELAY_NUMBER ] = OFF
        except Exception as e:
            print("Error disbling External Power")

        return self.relay_status


    def enableInverter(self):
        try:
            __turnOnSwitch(INVERTER)
            self.relay_status[ INVERTER_RELAY_NUMBER ] = ON
        except Exception as e:
            print("Error enabling Inverter")

        return self.relay_status


    def disableInverter(self):
        try:
            __turnOffSwitch( INVERTER )
            self.relay_status[ INVERTER_RELAY_NUMBER ] = OFF
        except Exception as e:
            print("Error disbling Inverter")

        return self.relay_status
