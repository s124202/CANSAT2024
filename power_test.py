import time
import cv2

import motor

motor.setup()
cap = cv2.VideoCapture(0)

time_start = time.time()
count = 0

while time.time() - time_start < 9000:
    time_start_sub = time.time()
    while time.time() - time_start_sub < 180:
        motor.motor_move(30,30,0.05)
        ret, frame = cap.read()
        if frame is None:
            print("camera error")
            print(time.time() - time_start)
            break
    motor.deceleration(30,30)
    time.sleep(10)

    time_start_sub = time.time()
    while time.time() - time_start_sub < 2:
        motor.motor_move(30,-30,0.05)

    motor.deceleration(30,-30)
    time.sleep(3)

    count += 1
    print("cycle : " + str(count))
    print(time.time()-time_start)

print("finish")

