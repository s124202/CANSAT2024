import RPi.GPIO as GPIO
import time

send_pin = 14

def setup_gpio_out(pin_number):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)

    #pull_down
    GPIO.setup(pin_number, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

def setup_gpio_in(pin_number):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.IN)

    #pull_down
    GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_pin(pin_number):
    return GPIO.input(pin_number)

def test(pin_number):
    #pulldownしてgpioの入力を返す
    setup_gpio(pin_number)
    gpio_input = GPIO.input(pin_number)
    GPIO.cleanup()
    return gpio_input

def main():
    setup_gpio(send_pin)

    try:
        while(True):
            print("pin status:", read_pin(send_pin))
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        print("GPIO pulldown program is finished")



if __name__ == '__main__':
    main()