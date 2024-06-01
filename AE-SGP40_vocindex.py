import time
import board
import adafruit_sgp40

i2c = board.I2C()
sgp = adafruit_sgp40.SGP40(i2c)

while True:
    raw = sgp.raw
    voc_index = vocalgorithm_process(raw)

    print("VOC Index:", voc_index)
    print("")
    time.sleep(1)