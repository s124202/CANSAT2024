import threading

import gps
import motor
import send
import mode0
import mode3

kari = "message"

thread1 = threading.Thread(target = gps.gps_test)
thread2 = threading.Thread(target = motor.motor_test)

#change_mode3
mode3.mode3_change()

#gps_motor_start_10sec
thread1.start()
thread2.start()

thread1.join()
thread2.join()

#change_mode0
mode0.mode0_change()

#send
send.send_main(kari)

#import RPi.GPIO as GPIO
#
#import gps
#import send
#import mode0
#import mode3
#import motor
#
#def main():
#    #motor
#    motor.setup()
#    motor.motor_test()
#
#    #change_mode3
#    mode3.mode3_change()
#
#    #Get_Gps
#    result = gps.gps_main()
#
#    #change_mode0
#    mode0.mode0_change()
#
#    #send
#    send.send_main(result)
#
#    #motor
#    motor.motor_test()
#
#if __name__ == '__main__':
#	main()