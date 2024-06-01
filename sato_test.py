import time
import board
import adafruit_sgp40
import BME280

i2c = board.I2C()  # uses board.SCL and board.SDA
sgp = adafruit_sgp40.SGP40(i2c)
BME280.bme280_calib_param()
BME280.bme280_setup()


data = BME280.bme280_read()
temperature = data[0]
humidity = data[3]
temperature=temperature
relative_humidity=humidity

def measure_index(
        temperature: float = 25, relative_humidity: float = 50
    ) -> int:
        
        raw = measure_raw(temperature, relative_humidity)
        if raw < 0:
            return -1
        else:
            return raw
        
if __name__ == '__main__':
    try:
        a = measure_index()
        print(a)

    except Exception as e:
        print()
        print(e.message)