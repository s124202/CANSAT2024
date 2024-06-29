import RPi.GPIO as GPIO
import time

import gps
import send
import mode0
import mode3

def main():
    #change_mode3
    mode3.mode3_change()

    #Get_Gps
    result = gps.gps_test(5)
    #result = gps.gps_csv(10)

    #change_mode0
    mode0.mode0_change()

    #sleep
    print("wait 3sec...")
    time.sleep(3)

    #test
    result = 20030127

    #send
    send.send_log(result)

if __name__ == '__main__':
	main()