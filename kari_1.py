from gpiozero import Motor

import time
import cv2
import numpy as np
import threading
 
def motor_setup():
	"""
	motorを使うときに必要な初期化を行う関数
	"""
	global motor_r, motor_l
	Rpin1, Rpin2 = 16, 26
	Lpin1, Lpin2 = 23, 18
	motor_r = Motor(Rpin1, Rpin2)
	motor_l = Motor(Lpin1, Lpin2)

def motor_move(strength_l, strength_r, t_moving):
	"""
	引数は左のmotorの強さ、右のmotorの強さ、走る時間。
	strength_l、strength_rは-1~1で表す。負の値だったら後ろ走行。
	必ずmotor_stop()セットで用いる。めんどくさかったら下にあるmotor()を使用
	"""
	strength_l = strength_l / 100
	strength_r = strength_r / 100
	# 前進するときのみスタック判定
	if strength_r >= 0 and strength_l >= 0:
		motor_r.forward(strength_r)
		motor_l.forward(strength_l)
		time.sleep(t_moving)
	# 後進
	elif strength_r < 0 and strength_l < 0:
		motor_r.backward(abs(strength_r))
		motor_l.backward(abs(strength_l))
		time.sleep(t_moving)
	# 右回転
	elif strength_r >= 0 and strength_l < 0:
		motor_r.forward(abs(strength_r))
		motor_l.backward(abs(strength_l))
		time.sleep(t_moving)
    # 左回転
	elif strength_r < 0 and strength_l >= 0:
		motor_r.backward(abs(strength_r))
		motor_l.forward(abs(strength_l))
		time.sleep(t_moving)

def motor_stop(x=1):
	"""
	motor_move()とセットで使用
	"""
	motor_r.stop()
	motor_l.stop()
	time.sleep(x)

def deceleration(strength_l, strength_r):
	"""
	穏やかに減速するための関数
	"""
	for i in range(10):
		coefficient_power = 10 - i
		coefficient_power /= 10
		motor_move(strength_l * coefficient_power, strength_r * coefficient_power, 0.1)
		if i == 9:
			motor_stop(0.1)
        
        

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域1
    #hsv_min = np.array([40,64,50])
    #hsv_max = np.array([90,255,255])
    #mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # 黄色のHSVの値域1
    #hsv_min = np.array([20,64,100])
    #hsv_max = np.array([30,255,255])
    #mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # オレンジ色のHSVの値域1
    hsv_min = np.array([10,100,100])
    hsv_max = np.array([25,255,255])
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域1
    #hsv_min = np.array([0,100,100])
    #hsv_max = np.array([5,255,255])
    #mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    #hsv_min = np.array([174,100,100])
    #hsv_max = np.array([179,255,255])
    #mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    #mask = mask1 + mask2

    return mask

def get_largest_red_object(mask):
    # 最小領域の設定
    minarea = 300
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    if nlabels > 1:
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        center = centroids[largest_label]
        size = stats[largest_label,cv2.CC_STAT_AREA]
        if size > minarea:
            return center, size
        return None, None
    else:
        return None, None

def main_detect():

    default_l = 43
    default_r= default_l - 20

    lose = 0
    discover = 1
    old_center = [320,0]
    count = 0
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()
        if not ret:
            print("fail")
            continue
        frame = cv2.resize(frame, (640,320))
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # 赤色検出
        mask = red_detect(frame)

        # 最大の赤色物体の中心を取得
        center, size = get_largest_red_object(mask)

        if center is None:
            center = old_center
            lose += 1
            discover = 1
            count += 1
        else:
             discover += 1
             lose = 0
             count = 0
        
        if size is None:
             size = 5000
        
        #-100 ~ 100 の範囲で設定
        mp = (int(center[0]) - 320) / 3.2   
        mp = mp / 22

        md = (center[0] - old_center[0]) / 100

        m = mp - md

        if size < 1000:
            s = 0
        else:
            s = size / 2000 + 5
             
        if count == 60:
            print("out")
            deceleration(strength_l,strength_r)
            break

        strength_l = default_l - s + m
        strength_r = default_r - s - m

        motor_move(strength_l,strength_r, 0.05)

        #print(old_center[0]-center[0])
        old_center = center

    cap.release()
    cv2.destroyAllWindows()
  

if __name__ == '__main__':
    motor_setup()
    main_detect()