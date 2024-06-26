import threading

import com_test
import motor


thread1 = threading.Thread(target = com_test.main)
thread2 = threading.Thread(target = motor.motor_test)


thread1.start()
thread2.start()


thread1.join()
thread2.join()