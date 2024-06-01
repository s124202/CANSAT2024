import time
import board
import adafruit_sgp40
import adafruit_bme280

i2c = board.I2C()  # uses board.SCL and board.SDA
sgp = adafruit_sgp40.SGP40(i2c)
bme280 = adafruit_bme280.Adafruit_BME280(i2c)

while True:
    temperature = bme280.temperature
    humidity = bme280.relative_humidity

    voc_index = sgp.measure_index(
    temperature=temperature, relative_humidity=humidity)

    print("VOC Index:", voc_index)
    print("")
    time.sleep(1)