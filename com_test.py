import RPi.GPIO as GPIO
import time

import gps
import send
import mode0
import mode3

aux = 25

#change_mode3
mode3.mode3_change()

#Get_Gps
result = gps.gps_main()

#change_mode0
mode0.mode0_change()

#send
send.send_main(result)