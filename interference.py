#モーターとgps>送信の並列

import threading

import com_test
import motor
import send
import mode0
import mode3

thread1 = threading.Thread(target = com_test.main)
thread2 = threading.Thread(target = motor.motor_test)

#change_mode3
mode3.mode3_change()

#motor_setup
motor.setup()

#gps_motor_start_10sec
thread1.start()
thread2.start()

thread1.join()
thread2.join()

#change_mode0
#mode0.mode0_change()

#send
#send.send_main(gps_data)