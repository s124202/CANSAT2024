import time
import board
import adafruit_sgp40

i2c = board.I2C() 
sgp = adafruit_sgp40.SGP40(i2c)

try:
	while True:
		print("Raw Gas: ", sgp.raw)
		print("")
		time.sleep(1)
except KeyboardInterrupt:
	print("\r\n")
except Exception as e:
	print(e)