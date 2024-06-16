import threading
import bluetooth

import gps
import pra_send
import send

thread1 = threading.Thread(target = gps.test)
thread2 = threading.Thread(target = pra_send.blt)
#thread3 = threading.Thread(target = send.main)


thread1.start()
thread2.start()
#thread3.start()


thread1.join()
thread2.join()
#thread3.start()

