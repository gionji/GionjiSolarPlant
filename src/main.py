

import os
import json
import datetime
import time

import currentMonitor
import relayBox
import database
import sensors
import chargeController




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
    database.init()
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


        ## send data to losant
    #    try:
    #        sendDataToLosant(data)
    #    except Exception as e:
    #        print( e )

        ## Pack data to db
        #  To use the data in the sqlite query has to be parsed to tuples
        data = packToDb( data )


        ## Add data to db
        database.add_data( data )

        ## select all data
        #database.select_data_all()

        time.sleep( DELAY )




if __name__ == "__main__":
    #application.listen(8888)
    #tornado.ioloop.IOLoop.instance().start()
    main()
