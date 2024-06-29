#設定モード

import RPi.GPIO as GPIO

def mode3_change():

    M0_pin = 5
    M1_pin = 6

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # set output
    GPIO.setup(M0_pin, GPIO.OUT)
    GPIO.setup(M1_pin, GPIO.OUT)

    # set M0=high,M1=high
    GPIO.output(M0_pin, True)
    GPIO.output(M1_pin, True)

if __name__ == '__main__':
	mode3_change()