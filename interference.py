import RPi.GPIO as GPIO
import time

import gps
import send
import mode0
import mode3
import motor

counter = 0

for i in range(3):

    counter += 1

    #change_mode3
    mode3.mode3_change()

    #Get_Gps
    gps_data = gps.gps_main()

    #change_mode0
    mode0.mode0_change()

    #send
    send.send_main(gps_data)

    #motor
    motor.setup()
    motor.move(10, 10, 5)

    print(counter, "回目終了")