import time
import cv2
import threading

import motor

def power_motor():
    motor.setup()
    time_start = time.time()
    count = 0


    while time.time() - time_start < 9000:
        motor.motor_move(30,30,120)
        motor.deceleration(30,30)

        time.sleep(10)

        motor.motor_move(-30,30,10)
        motor.deceleration(-30,30)

        time.sleep(3)

        count += 1
        print("cycle : " + str(count))
        print(int(time.time()-time_start))

    print("finish")

def camera():
    try:
        # カメラのキャプチャ
        cap = cv2.VideoCapture(0)

        while(cap.isOpened()):
            # フレームを取得
            ret, frame = cap.read()

            # フレームが正しく読み込まれていることを確認
            if frame is None:
                print("Failed to capture frame")

            time.sleep(1)
    except:
        print("pass")
        pass

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    thread1 = threading.Thread(target = power_motor)
    thread2 = threading.Thread(target = camera)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
