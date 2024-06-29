#送受信モード

import RPi.GPIO as GPIO

def mode0_change():

    M0_pin = 5
    M1_pin = 6

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # set output
    GPIO.setup(M0_pin, GPIO.OUT)
    GPIO.setup(M1_pin, GPIO.OUT)

    # set M0=high,M1=high
    GPIO.output(M0_pin, False)
    GPIO.output(M1_pin, False)

if __name__ == '__main__':
	mode0_change()