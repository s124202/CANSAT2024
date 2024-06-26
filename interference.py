import threading

import gps
import motor
import send
import mode0
import mode3

thread1 = threading.Thread(target = gps.gps_test)
thread2 = threading.Thread(target = motor.motor_test)

#change_mode3
mode3.mode3_change()

#motor_setup
motor.setup()

#gps_motor_start_10sec
gps_data = thread1.start()
thread2.start()

thread1.join()
thread2.join()

#change_mode0
mode0.mode0_change()

#send
send.send_main(gps_data)