
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

data = dict()

import tornado.ioloop
import tornado.web

class Hello(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world by Gionji solar Plant: " + str() )

class User(tornado.web.RequestHandler):

    def get(self):
        form = """<form method="post">
        <input type="text" name="username"/>
        <input type="text" name="designation"/>
        <input type="submit"/>
        </form>"""
        self.write(form)

    def post(self):
        username = self.get_argument('username')
        designation = self.get_argument('designation')
        self.write("Wow " + username + " you're a " + designation)

application = tornado.web.Application([
    (r"/", Hello),
    (r"/user/", User),
])


ACCESS_KEY = 'eed2fd5b-8219-4b18-a858-cdf345185cd6'
ACCESS_SECRET = '1d8c634d39551e13a6da838bfdc152cdc43e10362bca3a888cbfc2a411020dd3'
DEVICE_ID = '5e2ec7308eb4af0006ecd530'


DELAY = 1.0


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


def main():
    print('c')
    connectToLosant()

    currentMonitor.calculateCurrentBias( currentMonitor.PLUG_1 )
    currentMonitor.calculateCurrentBias( currentMonitor.PLUG_2 )
    currentMonitor.calculateCurrentBias( currentMonitor.INVERTER )


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

        try:
            sendDataToLosant(data)
        except Exception as e:
            print( e )

        data = packToDb( data )

        print( data )

        time.sleep( DELAY )




if __name__ == "__main__":
    application.listen(8888)
   
    #tornado.ioloop.IOLoop.instance().start()
    
    main()
