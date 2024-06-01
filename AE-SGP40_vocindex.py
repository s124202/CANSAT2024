import time
import board
import adafruit_sgp40
import BME280

i2c = board.I2C()  # uses board.SCL and board.SDA
sgp = adafruit_sgp40.SGP40(i2c)
BME280.bme280_calib_param()
BME280.bme280_setup()

while True:
    a = BME280.bme280_read()
    temperature = a[0]
    humidity = a[3]

    compensated_raw_gas = sgp.measure_raw(
        temperature=temperature, relative_humidity=humidity
    )
    
    print("Raw Data:", compensated_raw_gas)
    print("")
    time.sleep(1)