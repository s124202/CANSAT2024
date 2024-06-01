import time
import board
import adafruit_sgp40

i2c = board.I2C()
sgp = adafruit_sgp40.SGP40(i2c)

while True:
    voc_index = sgp.measure_index()

    print("VOC Index:", voc_index)
    print("")
    time.sleep(1)