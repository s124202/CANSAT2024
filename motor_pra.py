#2024/07/19 生川

import time
import src.motor as motor

def main():
    #setup
    motor.setup()
    try:
        while True:
            n = float(input('出力は？'))
            
            time.sleep(1)
            motor.move(n, 0, 5)
            time.sleep(0.1)
            motor.move(-n, 0, 5)

    except KeyboardInterrupt:
        print("end code")