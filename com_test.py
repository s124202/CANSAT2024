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

#aux_setup
#GPIO.setup(aux, GPIO.OUT)
#GPIO.output(aux, True)

#time.sleep(0.5)

#debug
#read_aux = GPIO.input(aux)
#print("aux_pin is",read_aux)

#send
#send.send_main(result)

#GPIO.output(aux, False)

#debug
#read_aux = GPIO.input(aux)
#print("aux_pin is",read_aux)

#while True:
#    if GPIO.input(aux) == True:
#        print("finish")
#        break

#send
send.send_main(result)