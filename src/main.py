import os
import json
import datetime
import time

import sys
sys.path.insert(0, "..")
import logging
import random
from opcua import ua, Server, uamethod

import EpeverChargeController as cc
import relayBox as rb
import currentMonitor
import sensors

DUMMY_DATA    = False
OPC_ENDPOINT  = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
OPC_NAMESPACE = "http://examples.freeopcua.github.io"

'''
username = os.environ['MY_USER']
password = os.environ['MY_PASS']
docker run -e MY_USER=test -e MY_PASS=12345 ... <image-name> ...
'''

if 'DELAY' in os.environ:
    DELAY = os.environ['DELAY']
else:
    DELAY = 1.0

#RELAY_STATE = [False, False, False, False]

######### da spostare in neogpio.py ####################

INPUT = 'in'
OUTPUT = 'out'
HIGH = '1'
LOW = '0'
PATH_GPIO = '/sys/class/gpio/'

def exportGpio( gpio ):
    try:
        f = open(PATH_GPIO + 'export' ,'w')
        f.write(str(gpio))
        f.flush()
        f.close()
    except Exception as e:
        print("Error exporting gpio " + str(gpio) )

    return 0


def setDirection( gpio, direction ):
    try:
        f = open(PATH_GPIO + 'gpio' + str(gpio) + '/direction' ,'w')
        f.write( str(direction) )
        f.flush()
        f.close()
    except Exception as e:
        print("Error setting gpio direction " + str(gpio) )

    return 0


def readValue( gpio ):
    value = None
    try:
        f = open(PATH_GPIO + 'gpio' + str(gpio) + '/value' ,'r')
        value = f.read( )
        f.close()
    except Exception as e:
        print("Error reading gpio value " + str(gpio) )

    return value

def setValue( gpio, value ):
    try:
        f = open(PATH_GPIO + 'gpio' + str(gpio) + '/value' ,'w')
        f.write( str(value) )
        f.flush()
        f.close()
    except Exception as e:
        print("Error setting gpio value " + str(gpio) )

    return 0
######################################################


LED_13_GPIO_NUMBER = 102

def initializeLed13():
    exportGpio( LED_13_GPIO_NUMBER )
    setDirection( LED_13_GPIO_NUMBER , OUTPUT )

def turnOnLed():
    setValue(LED_13_GPIO_NUMBER , HIGH)

def turnOffLed():
    setValue(LED_13_GPIO_NUMBER , LOW)

def blinkLed( howLong, howMany):
    for i in range(0, howMany):
        turnOnLed()
        time.sleep(howLong)
        turnOffLed()
        time.sleep(howLong)

#####################################################

def calibrateCurrentSensors():
    try:
        currentMonitor.calculateCurrentBias( currentMonitor.PLUG_1 )
        currentMonitor.calculateCurrentBias( currentMonitor.PLUG_2 )
        currentMonitor.calculateCurrentBias( currentMonitor.INVERTER )
    except Exception as e:
        print( e )








def init():
    initializeLed13()
    # blinkLed(0.05, 4)

    calibrateCurrentSensors()
    # blinkLed(0.05, 4)




relay_box = None

## method to be exposed through server
def set_plug_state(parent, args):
    ret = False

    plug = args.Value[0].Value
    state = args.Value[1].Value

    if plug in range(0,4):
        print("Plug: " + str(plug) + "  to state: " + str(state) )
        ret = relay_box.setRelayState(plug, state)
    else:
        print("PlugId is wrong, has to be integer in range 0 ... 3 . not " + str(plug) )

    print("opc method answer: " + str(ret))
    return [ua.Variant(ret, ua.VariantType.Boolean )]






def main():
    print('Gionji Solar Plant')

    global relay_box
    relay_box = rb.RelayBox()
    relay_box.add_relay('cane', 0, 25)
    init()

    # setup our server
    server = Server()
    server.set_endpoint( OPC_ENDPOINT )

    # setup our own namespace, not really necessary but should as spec
    server_namespace =  OPC_NAMESPACE
    address_space = server.register_namespace(server_namespace)

    # get Objects node, this is where we should put our custom stuff
    objects_node = server.get_objects_node()

    # populating our address space
    ChargeControllerObject = objects_node.add_object(address_space, "ChargeController")
    RelayBoxObject         = objects_node.add_object(address_space, "RelayBox")

    opc_variables = dict()

    panelVoltage       = ChargeControllerObject.add_variable(address_space, "panelVoltage", 0.0)
    panelCurrent       = ChargeControllerObject.add_variable(address_space, "panelCurrent", 0.0)
    batteryVoltage     = ChargeControllerObject.add_variable(address_space, "batteryVoltage", 0.0)
    batteryCurrent     = ChargeControllerObject.add_variable(address_space, "batteryCurrent", 0.0)
    loadVoltage        = ChargeControllerObject.add_variable(address_space, "loadVoltage", 0.0)
    loadCurrent        = ChargeControllerObject.add_variable(address_space, "loadCurrent", 0.0)
    inPower            = ChargeControllerObject.add_variable(address_space, "inPower", 0.0)
    outPower           = ChargeControllerObject.add_variable(address_space, "outPower", 0.0)
    batteryStatus      = ChargeControllerObject.add_variable(address_space, "batteryStatus", "")
    batteryCapacity    = ChargeControllerObject.add_variable(address_space, "batteryCapacity", 0.0)
    batteryTemperature = ChargeControllerObject.add_variable(address_space, "batteryTemperature", 0.0)

    plug1Current       = RelayBoxObject.add_variable(address_space, "plug_1_current", 0.0)
    plug2Current       = RelayBoxObject.add_variable(address_space, "plug_2_current", 0.0)
    inverterCurrent    = RelayBoxObject.add_variable(address_space, "inverter_current", 0.0)

    irradiation =  ChargeControllerObject.add_variable(address_space, "irradiation", 0.0)



    inverter_control_node = RelayBoxObject.add_method( address_space,
                                                       "set_plug_state",
                                                       set_plug_state,
                                                       [ ua.VariantType.Int32, ua.VariantType.Boolean ],
                                                       [ ua.VariantType.Boolean, ua.VariantType.Boolean,ua.VariantType.Boolean,ua.VariantType.Boolean ]
                                                      )

    # starting!
    server.start()
    print("Server starting ...")

    # creating my machinery objects
    chargeController = cc.EpeverChargeController(produce_dummy_data=DUMMY_DATA)

    while(True):

        print( relay_box.get_relays() )

        data = dict()

        ## Read data from hardware machines
        try:
            data = chargeController.readAllData()
            panelVoltage.set_value(data['panelVoltage'])
            panelCurrent.set_value(data['panelCurrent'])
            batteryVoltage.set_value(data['batteryVoltage'])
            batteryCurrent.set_value(data['batteryCurrent'])
            loadVoltage.set_value(data['loadVoltage'])
            loadCurrent.set_value(data['loadCurrent'])
            inPower.set_value(data['inPower'])
            outPower.set_value(data['outPower'])
            # batteryStatus.set_value(data['batteryStatus'])
            # batteryCapacity.set_value(data['batteryCapacity'])
            batteryTemperature.set_value(data['batteryTemperature'])
        except Exception as e:
            print( e )
        
        ## Read Irradiation data
        try:
            data['irradiation']      = sensors.getIrradiation()
            irradiation.set_value(data['irradiation'])
        except Exception as e:
            print( e )

        ## Read currents
        try:
            data['plug_1_current']   = currentMonitor.getCurrentPlug1()
            data['plug_2_current']   = currentMonitor.getCurrentPlug2()
            data['inverter_current'] = currentMonitor.getCurrentInverter()
            plug1Current.set_value(data['plug_1_current'])
            plug2Current.set_value(data['plug_2_current'])
            inverterCurrent.set_value(data['inverter_current'])
        except Exception as e:
            print( e )


        print( json.dumps(data) )

        #blinkLed(0.05, 2)
        
        time.sleep( DELAY )




if __name__ == "__main__":
    #application.listen(8888)
    #tornado.ioloop.IOLoop.instance().start()
    main()
