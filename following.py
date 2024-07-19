from gpiozero import Motor

import time
import cv2
import numpy as np
import threading
import bluetooth
 
def blt():
    global send
    global receive
    global synchro

    bd_addr = "B8:27:EB:1B:C5:BF" # サーバー側のデバイスアドレスを入力
    port = 1
    while True:
        send = 0
        receive = "0"
        synchro = 0
        
        while True:
            try:
                sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((bd_addr, port))
                sock.settimeout(10)
                print("connect success")
                break
            except KeyboardInterrupt:
                print("finish")
                break
            except:
                print("try again")
                time.sleep(3)
                pass

        while True:
            if synchro == 1:
                print("synchro")
                break
            try:
                time.sleep(1)
                sock.send(str(send))
                data = sock.recv(1024)
                receive = data.decode()
                print(receive)
            except KeyboardInterrupt:
                print("finish")
                break
            except bluetooth.btcommon.BluetoothError as err:
                print("close")
                break

        sock.close()
        if synchro == 1:
            break
        print("try reconnect")

def motor_setup():
	"""
	motorを使うときに必要な初期化を行う関数
	"""
	global motor_r, motor_l
	Rpin1, Rpin2 = 16,26
	Lpin1, Lpin2 = 23,18
	motor_r = Motor(Rpin1, Rpin2)
	motor_l = Motor(Lpin1, Lpin2)

def motor_move():
	
    global strength_l
    global strength_r
    global t_moving

    """
    引数は左のmotorの強さ、右のmotorの強さ、走る時間。
    strength_l、strength_rは-1~1で表す。負の値だったら後ろ走行。
    必ずmotor_stop()セットで用いる。めんどくさかったら下にあるmotor()を使用
    """
    local_strength_l = strength_l / 100
    local_strength_r = strength_r / 100
    # 前進
    if local_strength_r >= 0 and local_strength_l >= 0:
        motor_r.forward(local_strength_r)
        motor_l.forward(local_strength_l)
        time.sleep(t_moving)
    # 後進
    elif local_strength_r < 0 and local_strength_l < 0:
        motor_r.backward(abs(local_strength_r))
        motor_l.backward(abs(local_strength_l))
        time.sleep(t_moving)

def motor_stop(x=1):
	"""
	motor_move()とセットで使用
	"""
	motor_r.stop()
	motor_l.stop()
	time.sleep(x)

def deceleration():
    global strength_l
    global strength_r

    local_strength_l = strength_l
    local_strength_r = strength_r   
    """
    穏やかに減速するための関数
    """
    for i in range(10):
        coefficient_power = 10 - i
        coefficient_power /= 10
        motor_r.forward((local_strength_r / 100) * coefficient_power)
        motor_l.forward((local_strength_l /100) * coefficient_power)
        time.sleep(0.1)
        if i == 9:
        	motor_stop(0.1)

def move():
    """
    一定時間モータを動かすための関数
    strengthは-100~100
    t_movingはモータを動かす時間
    """
    time_start = time.time()
    time.sleep(5)

    while True:
        motor_move()
        time_finish = time.time()
        if time_finish - time_start > 60:
            break
    
    deceleration()
        
		

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域1
    #hsv_min = np.array([40,64,50])
    #hsv_max = np.array([90,255,255])
    #mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 黄色のHSVの値域1
    hsv_min = np.array([20,64,100])
    hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 紫色のHSVの値域1
    #hsv_min = np.array([110,100,50])
    #hsv_max = np.array([170,255,255])
    #mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1

def get_largest_red_object(mask):
    # 最小領域の設定
    minarea = 500
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

def main_detect():

    global blt_send

    global strength_l
    global strength_r

    lose = 0
    discover = 1
    old_center = [320,0]
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640,640))
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # 赤色検出
        mask = red_detect(frame)

        # 最大の赤色物体の中心を取得
        center, size = get_largest_red_object(mask)

        if center is None:
            center = old_center
            lose += 1
            discover = 1
        else:
             discover += 1
             lose = 0
        
        if size is None:
             size = 1000

        oldsize = size
        
        #-100 ~ 100 の範囲で設定
        strength = (int(center[0]) - 320) / 3.2
    
        strength = strength / 7

        if size < 2000:
             default_l = 28
             default_r = 35

        elif size < 4000:
             default_l = 25
             default_r = 32

        elif size < 6000:
             default_l = 20
             default_r = 27

        elif size < 20000:
            default_l = 5
            default_r = 6

        else:
             default_l = 0
        
        strength_l = default_l + strength
        strength_r = default_r - strength

        old_center = center

        if lose == 90:
             deceleration()
             blt_send = 1
             time.sleep(5)
             break
        
        elif discover % 30 == 0:
             blt_send = 0
             discover = 1        


        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    

if __name__ == '__main__':

    blt_send = 0
	
    strength_l = 25
    strength_r = 32
    t_moving = 0.05
	
    thread1 = threading.Thread(target = main_detect)
    thread2 = threading.Thread(target = move)

    motor_setup()
    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()