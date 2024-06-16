import threading

import send
import pra_send


thread1 = threading.Thread(target = pra_send.test)
thread2 = threading.Thread(target = send.test)


thread1.start()
thread2.start()


thread1.join()
thread2.join()