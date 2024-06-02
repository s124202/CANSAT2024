import time
import board
import adafruit_sgp40

i2c = board.I2C() 
sgp = adafruit_sgp40.SGP40(i2c)

while True:
	print("Raw Gas: ", sgp.raw)
	print("")
	time.sleep(1)