from losantmqtt import Device

ACCESS_KEY    = 'eed2fd5b-8219-4b18-a858-cdf345185cd6'
ACCESS_SECRET = '1d8c634d39551e13a6da838bfdc152cdc43e10362bca3a888cbfc2a411020dd3'
DEVICE_ID     = '5e2ec7308eb4af0006ecd530'

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
