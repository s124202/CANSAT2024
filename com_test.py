import RPi.GPIO as GPIO

import gps
import send
import mode0
import mode3
import pullD

send_pin = 14
receive_pin = 15

def main():
    #change_mode3
    mode3.mode3_change()

    #Get_Gps
    result = gps.gps_test()#10sec

    #change_mode0
    mode0.mode0_change()

    #setup
    #pullD.setup_gpio_out(send_pin)
    #pullD.setup_gpio_in(receive_pin)

    #send
    send.send_main(result)
    #GPIO.cleanup()

if __name__ == '__main__':
	main()