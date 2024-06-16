import threading

import gps
import send


thread1 = threading.Thread(target = gps.test)
thread2 = threading.Thread(target = send.main)


thread1.start()
thread2.start()


thread1.join()
thread2.join()
