import RPi.GPIO as GPIO

import gps
#import send


result = gps.gps_main()


#mode_0
#M0_pin = 5
#M1_pin = 6

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)

#GPIO.setup(M0_pin, GPIO.OUT)
#GPIO.setup(M1_pin, GPIO.OUT)

#GPIO.output(M0_pin, False)
#GPIO.output(M1_pin, False)


#send.send_main(result)