#import threading
#
#import com_test
#import motor
#
#
#thread1 = threading.Thread(target = com_test.main)
#thread2 = threading.Thread(target = motor.motor_test)
#
#
#thread1.start()
#thread2.start()
#
#
#thread1.join()
#thread2.join()

import RPi.GPIO as GPIO

import gps
import send
import mode0
import mode3
import motor

def main():
    #motor
    motor.motor_test()
    
    #change_mode3
    mode3.mode3_change()

    #Get_Gps
    result = gps.gps_main()

    #change_mode0
    mode0.mode0_change()

    #send
    send.send_main(result)

    #motor
    motor.motor_test()

if __name__ == '__main__':
	main()