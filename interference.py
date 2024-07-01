#モーターとgps>送信の並列

import threading

import com_test
import motor
import send
import mode0
import mode3

thread1 = threading.Thread(target = com_test.main)
thread2 = threading.Thread(target = motor.motor_test)

#motor_setup
motor.setup()

#gps_motor_start_10sec
thread1.start()
thread2.start()

thread1.join()
thread2.join()