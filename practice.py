import threading

import gps
import pra_send


thread1 = threading.Thread(target = gps.test)
thread2 = threading.Thread(target = pra_send.test)


thread1.start()
thread2.start()


thread1.join()
thread2.join()


