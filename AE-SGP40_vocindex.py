import time
import board
import adafruit_sgp40
from adafruit_sgp40.voc_algorithm import (
            VOCAlgorithm,
        )

i2c = board.I2C()
sgp = adafruit_sgp40.SGP40(i2c)

_voc_algorithm = VOCAlgorithm()
_voc_algorithm.vocalgorithm_init()

while True:
    raw = sgp.raw

    print("VOC Index:", raw)
    print("")
    time.sleep(1)