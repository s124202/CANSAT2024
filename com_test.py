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

#debug
GPIO.setup(aux, GPIO.OUT)
read_aux = GPIO.input(aux)
print("aux_pin is",read_aux)

time.sleep(0.5)

#read_aux = GPIO.input(aux)
#print(read_aux)

#while True
#
#    if GPIO.input(aux) == True
#        break


#send
send.send_main(result)