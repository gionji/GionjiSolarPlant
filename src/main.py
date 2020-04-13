

import os
import json
import datetime
import time

import currentMonitor
import relayBox
import database
import sensors
import chargeController


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


def initializeLed13():
    exportGpio( 102 )
    setDirection( 102, OUTPUT )
    
def turnOnLed():
    setValue(102 , HIGH)

def turnOffLed():
    setValue(102, LOW)

def blink13( howLong, howMany):
    for i in range(0, howMany):
        turnOnLed()
        time.sleep(howLong)
        turnOffLed()
        time.sleep(howLong)


def packToDb(data):
    ret = (
        data['panelVoltage'],
        data['panelCurrent'],
        data['batteryVoltage'],
        data['batteryCurrent'],
        data['loadVoltage'],
        data['loadCurrent'],
        data['inPower'],
        data['outPower'],
        data['plug_1_current'],
        data['plug_2_current'],
        data['inverter_current'],
        data['irradiation']
            )
    return ret



def calibrateCurrentSensors():
    currentMonitor.calculateCurrentBias( currentMonitor.PLUG_1 )
    currentMonitor.calculateCurrentBias( currentMonitor.PLUG_2 )
    currentMonitor.calculateCurrentBias( currentMonitor.INVERTER )



def init():
    initializeLed13()
    database.init()
    relayBox.init()
    calibrateCurrentSensors()




data = dict()


def main():
    print('Gionji Solar Plant')
    
    init()

    while(True):
        global data
        data = dict()

        ## Read Charge Controller Data
        data = chargeController.readAll()

        ## Read Irradiation data
        try:
            data['irradiation']      = sensors.getIrradiation()
        except Exception as e:
            data['irradiation']      = None
            print( e )

        ## Read currents
        try:
            data['plug_1_current']   = currentMonitor.getCurrentPlug1()
            data['plug_2_current']   = currentMonitor.getCurrentPlug2()
            data['inverter_current'] = currentMonitor.getCurrentInverter()
        except Exception as e:
            data['plug_1_current']   = None
            data['plug_2_current']   = None
            data['inverter_current'] = None
            print( e )

        ## Pack data to db
        #  To use the data in the sqlite query has to be parsed to tuples
        data = packToDb( data )


        blinkLed(0.05, 4)

        ## Add data to db
        database.add_data( data )

        ## select all data
        #database.select_data_all()

        time.sleep( DELAY )




if __name__ == "__main__":
    #application.listen(8888)
    #tornado.ioloop.IOLoop.instance().start()
    main()
