# カメラによる色検知
# 色検知できたらbluetoothで1を送信、できなかったら0を送信

import numpy as np
import time
import threading
import bluetooth
import cv2


def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0,100,100])
    hsv_max = np.array([5,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([174,100,100])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1 + mask2

def get_largest_red_object(mask):
    global center
    center = None
    # 最小領域の設定
    minarea = 10
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    if nlabels > 1:
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        center = centroids[largest_label]
        if stats[largest_label,cv2.CC_STAT_AREA] > minarea:
            return center
        return None
    else:
        return None

def main():

    global center
    center = None
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()

        # 赤色検出
        mask = red_detect(frame)

        # # 最大の赤色物体の中心を取得
        center = get_largest_red_object(mask)
        # if center is not None:
        #     cv2.circle(frame, (int(center[0]), int(center[1])), 5, (255, 0, 0), -1)
        #     if center[0] < 200:
        #         width = 'left'
        #     elif center[0] < 440:
        #         width = 'center'
        #     else:
        #         width = 'right'
        #     cv2.putText(frame, width, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # # 結果表示
        # cv2.imshow("Frame", frame)
        # cv2.imshow("Mask", mask)

        # # qキーが押されたら途中終了
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()



def blt():
    global center
    center = None

    bd_addr = "B8:27:EB:A9:5B:64"
    port = 1

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    for i in range (30):
        if center is not None:
            sock.send("1")
        else:
            sock.send("0")

        time.sleep(1)
    
    sock.close()

def test():
    thread1 = threading.Thread(target = main)
    thread2 = threading.Thread(target = blt)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


if __name__ == "__main__":

    test()