# カメラによる色検知
# 出力画面あり

import cv2
import numpy as np

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域1
    hsv_min = np.array([30,64,100])
    hsv_max = np.array([90,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 黄色のHSVの値域1
    #hsv_min = np.array([20,80,10])
    #hsv_max = np.array([50,255,255])
    #mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 紫色のHSVの値域1
    #hsv_min = np.array([110,100,50])
    #hsv_max = np.array([170,255,255])
    #mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1

def get_largest_red_object(mask):
    # 最小領域の設定
    minarea = 100
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    if nlabels > 1:
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        center = centroids[largest_label]
        size = stats[largest_label,cv2.CC_STAT_AREA]
        if size > minarea:
            return center, size
        return None, 0
    else:
        return None, 0

def main_movie():
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640,640))
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # フレームが正しく読み込まれていることを確認
        if frame is None:
            print("Failed to capture frame")
            break

        # 赤色検出
        mask = red_detect(frame)

        # 最大の赤色物体の中心を取得
        center, size = get_largest_red_object(mask)

        if center is not None:
            cv2.circle(frame, (int(center[0]), int(center[1])), 5, (255, 0, 0), -1)
            cv2.putText(frame, str(int(size)) + "," + str(int(center[0]) - 320), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # 結果表示
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main_image():
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)

    # フレームを取得
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640,640))
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # 赤色検出
    mask = red_detect(frame)

    # 最大の赤色物体の中心を取得
    center, size = get_largest_red_object(mask)

    cap.release()
    cv2.destroyAllWindows()

    if center is not None:
        return int(center)
    else:
        return 0.1

if __name__ == '__main__':
    main_movie()
