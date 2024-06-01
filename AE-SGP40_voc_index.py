import time
import board
import adafruit_sgp40
import BME280

i2c = board.I2C()  # uses board.SCL and board.SDA
sgp = adafruit_sgp40.SGP40(i2c)
BME280.bme280_calib_param()
BME280.bme280_setup()

def measure_index(
        temperature: float = 25, relative_humidity: float = 50
    ) -> int:
        
        from adafruit_sgp40.voc_algorithm import (
            VOCAlgorithm,
        )

        sraw = sgp.measure_raw(temperature, relative_humidity)
        if sraw < 0:
            return -1
        voc_index = _voc_algorithm.vocalgorithm_process(sraw)
        return voc_index

while True:
	data = BME280.bme280_read()
	temperature = data[0]
	humidity = data[3]

	voc_index = measure_index(
	temperature=temperature, relative_humidity=humidity)

	print("VOC Index:", voc_index)
	print("")
	time.sleep(1)