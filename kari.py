import threading

import gps
import pra_reception


thread1 = threading.Thread(target = gps.test)
thread2 = threading.Thread(target = pra_reception.main)


thread1.start()
thread2.start()


thread1.join()
thread2.join()