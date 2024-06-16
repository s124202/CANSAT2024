import threading
import bluetooth

import gps
import pra_send

thread1 = threading.Thread(target = gps.test)
thread2 = threading.Thread(target = pra_send.blt)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
