import threading

import bme280
import bmx055


bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()

thread1 = threading.Thread(target = bme280.bme280_csv)
thread2 = threading.Thread(target = bmx055.bmx055_csv)

thread1.start()
thread2.start()

thread1.join()
thread2.join()