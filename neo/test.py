import neo


board = neo.UdooNeo()

#board.unexport_all_gpios()

board.gpio.export_all_gpios()


#board.export_pwm( 3 )

temp = board.temperature_brick.getTemperature()
print("Temperature " + str(temp))

light = board.light_brick.getVisibleSpectrum()
print("Visible " + str(light) )

light = board.light_brick.getInfraredSpectrum()
print("IR "  + str(light ))

light = board.light_brick.getFullSpectrum()
print("Full spectrum: " + str(light) )

baro = board.barometric_brick.getAltitude()
print ("Altitude " + str(baro))

baro = board.barometric_brick.getPressure()
print ("Pressure " + str(baro))

baro = board.barometric_brick.getTemperature()
print ("Temperature " + str(baro))

adc0 = board.analog.analogRead( neo.A0 )
adc1 = board.analog.analogRead( neo.A1 )
adc2 = board.analog.analogRead( neo.A2 )
adc3 = board.analog.analogRead( neo.A3 )
adc4 = board.analog.analogRead( neo.A4 )
adc5 = board.analog.analogRead( neo.A5 )

print(adc0, adc1, adc2, adc3, adc4, adc5)
