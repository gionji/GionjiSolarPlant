
from losantmqtt import Device
import os
import json
import datetime
import time

import currentMonitor
import relayBox
import database
import sensors
import chargeController


ACCESS_KEY    = 'eed2fd5b-8219-4b18-a858-cdf345185cd6'
ACCESS_SECRET = '1d8c634d39551e13a6da838bfdc152cdc43e10362bca3a888cbfc2a411020dd3'
DEVICE_ID     = '5e2ec7308eb4af0006ecd530'

DELAY = 1.0

## docker
# docker run -e MY_USER=test -e MY_PASS=12345 ... <image-name> ...
username = os.environ['MY_USER']
password = os.environ['MY_PASS']



# Construct Losant device
device = Device(DEVICE_ID, ACCESS_KEY, ACCESS_SECRET)

def sendDataToLosant(data):
    print("Sending to Losant...")
    device.send_state(data)

def connectToLosant():
    # Connect to Losant and leave the connection open
    global device
    device.connect(blocking=False)



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




def init():
    database.init()


def calibrateCurrentSensors():
    currentMonitor.calculateCurrentBias( currentMonitor.PLUG_1 )
    currentMonitor.calculateCurrentBias( currentMonitor.PLUG_2 )
    currentMonitor.calculateCurrentBias( currentMonitor.INVERTER )



data = dict()


def main():
    print('Gionji Solar Plant')

    connectToLosant()
    
    database.init()

    while(True):
        global data
        data = dict()

        data = chargeController.readAll()

        try:
            data['irradiation']      = sensors.getIrradiation()
        except Exception as e:
            data['irradiation']      = None 
            print( e )

        try:
            data['plug_1_current']   = currentMonitor.getCurrentPlug1()
            data['plug_2_current']   = currentMonitor.getCurrentPlug2()
            data['inverter_current'] = currentMonitor.getCurrentInverter()    
        except Exception as e:
            data['plug_1_current']   = None
            data['plug_2_current']   = None
            data['inverter_current'] = None
            print( e )


        ## send data to losant
        try:
            sendDataToLosant(data)
        except Exception as e:
            print( e )

        ## Pack data to db
        #  To use the data in the sqlite query has to be
        #  parsed to tuples
        data = packToDb( data )

        ## Add data to db
        database.add_data( data )
        
        ## select all data
        #database.select_data_all()

        time.sleep( DELAY )



if __name__ == "__main__":
    # application.listen(8888)
    # tornado.ioloop.IOLoop.instance().start()
    main()



