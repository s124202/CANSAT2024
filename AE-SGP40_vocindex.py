import time
import board
import adafruit_sgp40
import BME280

i2c = board.I2C()  # uses board.SCL and board.SDA
sgp = adafruit_sgp40.SGP40(i2c)
bme280 = BME280
bme280.bme280_read()

while True:
    temperature = bme280.value[2]
    humidity = bme280.value[3]

    voc_index = sgp.measure_index(
    temperature=temperature, relative_humidity=humidity)

    print("VOC Index:", voc_index)
    print("")
    time.sleep(1)