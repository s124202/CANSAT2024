import time
import board
import adafruit_sgp40
import bme280

i2c = board.I2C() 
sgp = adafruit_sgp40.SGP40(i2c)
bme280.bme280_calib_param()
bme280.bme280_setup()

try:
	while True:
		data = bme280.bme280_read()
		temperature = data[0]
		humidity = data[2]

		compensated_raw_gas = sgp.measure_raw(
			temperature=temperature, relative_humidity=humidity
		)

		print("Raw Data:", compensated_raw_gas)
		print("")
		time.sleep(1)
except KeyboardInterrupt:
	print("\r\n")
except Exception as e:
	print(e)