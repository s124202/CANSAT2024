import time
import board
import adafruit_sgp40
import bme280
#import csv

i2c = board.I2C() 
sgp = adafruit_sgp40.SGP40(i2c)
bme280.bme280_calib_param()
bme280.bme280_setup()

def voc_index_read():
	while True:
		data = bme280.bme280_read()
		temperature = data[0]
		humidity = data[2]

		compensated_raw_gas = sgp.measure_raw(
			temperature=temperature, relative_humidity=humidity
		)

		voc_index = sgp.measure_index(
		temperature=temperature, relative_humidity=humidity)

		print("voc_index:" + str(voc_index) + "\t" + "raw_gas:" + str(compensated_raw_gas) + "\t" + "tem:" + str(temperature) + "\t" + "hum: " + str(humidity))
		print("")
		time.sleep(1)


def test():
	data = bme280.bme280_read()
	temperature = data[0]
	humidity = data[2]

	compensated_raw_gas = sgp.measure_raw(
		temperature=temperature, relative_humidity=humidity
	)

	voc_index = sgp.measure_index(
	temperature=temperature, relative_humidity=humidity)

	time.sleep(1)

	return voc_index, compensated_raw_gas, temperature, humidity


if __name__ == '__main__':
	voc_index_read()