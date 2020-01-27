from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from losantmqtt import Device
import os
import json
import datetime
import time

ACCESS_KEY = 'eed2fd5b-8219-4b18-a858-cdf345185cd6'
ACCESS_SECRET = '1d8c634d39551e13a6da838bfdc152cdc43e10362bca3a888cbfc2a411020dd3'
DEVICE_ID = '5e2ec7308eb4af0006ecd530'

BAUDRATE = 115200
PORT = '/dev/ttyUSB0'

# Construct Losant device
device = Device(DEVICE_ID, ACCESS_KEY, ACCESS_SECRET)

def readModbus():
    data = dict()

    print("Connect modbus...")
    client = ModbusClient(method='rtu', port=PORT, baudrate=BAUDRATE)
    client.connect()
    # print( client)
    result = client.read_input_registers(0x3100, 15, unit=1)
    result1 = client.read_input_registers(0x3300, 14, unit=1)
    result2 = client.read_input_registers(0x3110, 2, unit=1)
    # result3 = client.read_input_registers(0x311,15,unit=1)
    # result4 = client.read_input_registers(0x3200,15,unit=1)
    # print (result)
    
#data['date'] = datetime.datetime.now()
    data['panelVoltage'] = float(result.registers[0] / 100.0)
    data['panelCurrent'] = float(result.registers[1] / 100.0)
    data['batteryVoltage'] = float(result.registers[4] / 100.0)
    data['batteryCurrent'] = float(result.registers[5] / 100.0)
    data['loadVoltage'] = float(result.registers[12] / 100.0)
    data['loadCurrent'] = float(result.registers[13] / 100.0)
    data['inPower'] =  data['panelVoltage'] * data['panelCurrent'] 
    data['outPower'] =  data['loadVoltage'] * data['loadCurrent']
    #data['batteryTemperature'] = float(result2.registers[0] / 100)
    # bateryCapacity = float(result3.registers[10] /100)
    # bateryStatus = (result4.registers[0])

    return data

def sendDataToLosant(data):
    print("Sending to Losant...")
    device.send_state(data)

def connectToLosant():
    # Connect to Losant and leave the connection open
    global device
    device.connect(blocking=False)



def main():
    print('c')
    connectToLosant()
    
    while(True):
        try:
            data = readModbus()
            print(data)
            sendDataToLosant(data)
        except Exception as e:
            print( e )

        time.sleep(1)

if __name__ == "__main__":
    main()
