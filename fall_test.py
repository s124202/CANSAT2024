import threading

import bmx055
import bme280


thread1 = threading.Thread(target = bmx055.bmx055_csv)
thread2 = threading.Thread(target = bme280.bme280_csv)


thread1.start()
thread2.start()


thread1.join()
thread2.join()