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
    else:
        motor_stop(0.05)


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

    global synchro
    time.sleep(5)

    while True:
        try:
            motor_move()
            if synchro == 1:
                break
            deceleration()
        except KeyboardInterrupt:
            deceleration()
        
#theta_array Max5
def latest_theta_array(theta, array:list):
    #-----thetaの値を蓄積する-----#

    #古い要素を消去
    del array[0]

    #新しい要素を追加
    array.append(theta)

    return array


#P
def proportional_control(Kp, theta_array :list):
    #-----P制御-----#
    
    #-----最新のthetaの値を取得-----#
    theta_deviation = theta_array[-1]

    mp = Kp * theta_deviation

    return mp


#D
def differential_control(Kd, theta_array: list):
    #D制御

    theta_differential_array = []
    #thetaの微分処理
    for i in range(len(theta_array)):
        theta_differential_value = theta_array[i] - theta_array[i-1]
        theta_differential_array.append(theta_differential_value)

    #最新のthetaの微分値を取得
    theta_differential = theta_differential_array[-1]

    md = Kd * theta_differential

    return md


#PD
def PD_control(theta, theta_array: list, Kp=0.1, Kd=2.5):
    #-----PD制御-----#
    #-----thetaの値を蓄積する-----#
    theta_array = latest_theta_array(theta, theta_array)

    #-----P制御-----#
    mp = proportional_control(Kp, theta_array)

    #-----D制御-----#
    md = differential_control(Kd, theta_array)

    #-----PID制御-----#
    m = mp - md

    return m	

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

    global blt_send
    global synchro

    global strength_l
    global strength_r

    #const
    theta_array = [0]*5
    Kp = 0.4
    Kd = 3
    #直進成分
    default_l = 30
    default_r= default_l + 7

    lose = 0
    discover = 1
    old_center = [320,0]

    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        try:
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
                 size = 100000

            #-180 ~ 180 の範囲で設定
            error_theta = (int(center[0]) - 320) / 1.77
            theta_array = latest_theta_array(error_theta, theta_array)

            m = PD_control(error_theta, theta_array, Kp, Kd)
            m = min(m, 7)
            m = max(m, -7)
            if size < 3000:
                s = 0
            elif size < 8000:
                s = 5
            else:
                s = 10

            if lose == 30:
                print("out")
                synchro = 1
                break

            strength_l = default_l - s - m
            strength_r = default_r - s + m

            old_center = center

            #if lose == 90:
            #     deceleration()
            #     blt_send = 1
            #     time.sleep(5)
            #     break
            #
            #elif discover % 30 == 0:
            #     blt_send = 0
            #     discover = 1 
        except KeyboardInterrupt:
            break

        cap.release()
        cv2.destroyAllWindows()

    

if __name__ == '__main__':

    blt_send = 0
    synchro = 0
	
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