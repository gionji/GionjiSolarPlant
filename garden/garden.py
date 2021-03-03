import Neo


DEFAULT_TIME = 5 # sec

class Garden(object):

    def __init__(self):
        self.charge_controller = None
        self.neo = None
        pass

    # Actuators
    def turnOnPump(self, time=DEFAULT_TIME):
        pass

    def turnOffPump(self):
        pass

    def turnOnLight(self):
        pass

    def turnOffLight(self):
        pass

    def turnOnHeater(self):
        pass

    def turnOffHEater(self):
        pass

    # Sensors
    def getMoisture(self):
        pass

    def getGas1Value(self):
        pass

    def getGas2Value(self):
        pass

    def getGas3Value(self):
        pass

    def getWeaterForecast(self):
        pass

    def getTemperature(self):
        pass

    def getLight(self):
        pass

    def getPressure(self):
        pass

    def getBaroTemperature(self):
        pass

    # get Energy informations
    def getPanelVoltage(self):
        pass

    def getPanelCurrent(self):
        pass

    def getBatteryVoltage(self):
        pass

    def getBatteryCurrent(self):
        pass

    def getOutputVoltage(self):
        pass

    def getOutputCurrent(self):
        pass

    def getInputPower(self):
        pass

    def getOutputPower(self):
        pass

    def getPowerConsumption(self):
        pass

def main():
    return 0


if __name__ == "__main__":
    main()
