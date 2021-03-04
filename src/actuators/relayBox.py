import sys
import time


##########################################################3
class BoardType:
    NEO = 0x01
    C23 = 0x02

class OsType:
    UBUNTU_1804   = 0x11
    UDUBUNTU_1404 = 0x12
    DOCKER        = 0x13

###########################################################


osType = OsType.UBUNTU_1804
boardType = BoardType.NEO


###############################################################3

PATH_GPIO_UBUNTU    = '/sys/class/gpio/'
PATH_GPIO_UDOOBUNTU = '/gpio/'
PATH_GPIO_CONTAINER = '/var/gpio/'


NEO_GPIOS = [
                (24, 25),
                (25, 22),
                (26, 14),
                (27, 15),        
            ]


# pins numbers printend on the Udoo Neo PCB
RELAY_PCB_NUMBER_NEO  = [24, 25, 26, 27]
# correspondent gpio kernel numbers
RELAY_GPIO_NUMBER_NEO = [25, 22, 14, 15]

###################################################

if osType == OsType.UBUNTU_1804:
    PATH_GPIO = PATH_GPIO_UBUNTU
elif osType == OsType.UDUBUNTU_1404:
    PATH_GPIO = PATH_GPIO_UDOOBUNTU
elif osType == OsType.DOCKER:
    PATH_GPIO = PATH_GPIO_CONTAINER

if boardType == BoardType.NEO:
    RELAY_GPIO_NUMBER = RELAY_GPIO_NUMBER_NEO


class Relay:

    name               = None
    id                 = None

    gpio_kernel_number = None
    export_path        = None
    gpio_path          = None

    state              = False

    def __init__( self , name : str, id : int, gpio_kernel_number : int, gpio_path_basename : str ):
        self.name = name
        self.id   = id

        self.gpio_kernel_number = gpio_kernel_number
        self.export_path        = gpio_path_basename + 'export'
        self.gpio_path          = gpio_path_basename + 'gpio/' + str(self.gpio_kernel_number) + '/'

        self.initialize_hardware()


    def initialize_hardware(self):
        try:
            f = open( self.export_path, 'w+')
            f.write( str(self.gpio_kernel_number) )
            f.flush()
            f.close()
        except:
            print( 'Error exporting gpio ' + str(self.gpio_kernel_number) )

        try:
            f = open( self.gpio_path + 'direction' , "w+")
            f.write('out')
            f.flush()
            f.close()
        except:
            print( 'Error setting direction gpio ' + str( self.gpio_kernel_number ) )


    def get_state(self):
        return self.state

    def turn_on(self):
        try:
            f = open( self.gpio_path + 'value' , "w+")
            f.write('1')
            f.flush()
            f.close()
            self.state = True
        except:
            print( 'Error setting value gpio ' + str( self.gpio_kernel_number ) )

        return self.state


    def turn_off(self):
        try:
            f = open( self.gpio_path + 'value' , "w+")
            f.write('0')
            f.flush()
            f.close()
            self.state = False
        except:
            print( 'Error setting value gpio ' + str( self.gpio_kernel_number ) )

        return self.state


    def set_state(self, state : bool):
        if state:
            val = '1'
        else:
            val = '0'
        
        try:
            f = open( self.gpio_path + 'value' , "w+")
            f.write('val')
            f.flush()
            f.close()
            self.state = state
        except:
            print( 'Error setting value gpio ' + str( self.gpio_kernel_number ) )

        return self.state





class RelayBox:

    ## Relays status
    relays    = None
    gpio_path = None


    def __init__(self, boardType = BoardType.NEO, osType = OsType.UBUNTU_1804):
        self.__setLocalPaths(boardType, osType)
        self.relays = dict()


    def add_relay(self, name : str, id : int,  gpio_number : int):
        relay  = Relay ( name , 
                                id, 
                                gpio_kernel_number = gpio_number, 
                                gpio_path_basename = str(self.gpio_path) 
                              )
        self.relays[ name ] = relay



    def __setLocalPaths(self, boardType, osType):
        if osType == OsType.UBUNTU_1804:
            self.gpio_path = PATH_GPIO_UBUNTU
        elif osType == OsType.UDUBUNTU_1404:
            self.gpio_path = PATH_GPIO_UDOOBUNTU
        elif osType == OsType.DOCKER:
            self.gpio_path = PATH_GPIO_CONTAINER

        if boardType == BoardType.NEO:
            None

    def turn_on(self, name):
        try:
            return self.relays[ name ].turn_on()
        except Exception as e:
            return None
            print( e )

    def turn_off(self, name):
        try:
            return self.relays[ name ].turn_off()
        except Exception as e:
            return None
            print( e )

    def get_relays(self):
        return self.relays


    def remove_all_relays(self):
        self.relays = dict()



#################################################################################

      

#################################################################################
    '''
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

    '''
