#standard
import time
import bluetooth
import threading

#src
import gps
import bmx055
import motor
import calibration
import gps_navigate
import stuck

#send
import send.mode3 as mode3
import send.send_11 as send_11

def blt():
    global send
    global receive
    global synchro

    send = 0
    receive = "0"
    synchro = 0
    
    try:
        server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 1
        server_sock.bind(("",port))
        server_sock.listen(1)
        client_sock,address = server_sock.accept()
        client_sock.settimeout(10)
        print("Accepted connection from ",address)

        while True:
            if synchro == 1:
                print("synchro")
                break
            try:
                data = client_sock.recv(1024)
                receive = data.decode()
                print(receive)
                time.sleep(1)
                client_sock.send(str(send))
            except KeyboardInterrupt:
                print("finish")
                break
            except bluetooth.btcommon.BluetoothError as err:
                print("close")
                break
        client_sock.close()
        server_sock.close()

    except KeyboardInterrupt:
        print("finish")
        client_sock.close()
        server_sock.close()
    

#angle correction
def standarize_angle(angle):
    '''
    角度を-180～180度に収める関数
    '''
    angle = angle % 360
    
    if angle >180:
        angle -= 360
    elif angle < -180:
        angle += 360

    return angle


#return theta_dest
def get_theta_dest(target_azimuth, magx_off, magy_off):
    '''
    #ローバーから目標地点までの方位角が既知の場合に目標地点(dest)との相対角度を算出する関数
    ローバーが向いている角度を基準に、時計回りを正とする。

    theta_dest = 60 のとき、目標地点はローバーから見て右手60度の方向にある。

    -180 < theta_dest < 180

    Parameters
    ----------
    lon2 : float
        目標地点の経度
    lat2 : float
        目標地点の緯度
    magx_off : int
        地磁気x軸オフセット
    magy_off : int
        地磁気y軸オフセット

    '''
    #-----ローバーの角度を取得-----#
    magdata= bmx055.mag_dataRead()
    mag_x, mag_y = magdata[0], magdata[1]

    rover_azimuth = calibration.angle(mag_x, mag_y, magx_off, magy_off)

    #-----目標地点との相対角度を算出-----#
    #ローバーが向いている角度を0度としたときの、目的地への相対角度。このとき時計回りを正とする。
    theta_dest = rover_azimuth - target_azimuth

    #-----相対角度の範囲を-180~180度にする-----#
    theta_dest = standarize_angle(theta_dest)

    return theta_dest


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


#I
def integral_control(Ki, theta_array: list):
    #I制御

    #thetaの積分処理
    theta_integral = sum(theta_array)

    mi = Ki * theta_integral

    return mi


#D
def differential_control(Kd, theta_array: list):
    #D制御

    #thetaの微分処理
    for i in range(len(theta_array)):
        theta_differential_value = theta_array[i] - theta_array[i-1]
        theta_differential_array.append(theta_differential_value)

    #最新のthetaの微分値を取得
    theta_differential = theta_differential_array[-1]

    md = Kd * theta_differential

    return md


#これはどう？D
#len(theta_array)をtheta_array[]の中に入れるとエラー吐きそうだから二行に分割
def differential_controlkai(Kd, theta_array: list):
    #D制御

    num = len(theta_array)
    theta_differential = theta_array[num-1] - theta_array[num-2]

    md = Kd * theta_differential

    return md


#PID
def PID_control(theta, theta_array: list, Kp=0.1, Ki=0.04, Kd=2.5):
    #-----PID制御-----#

    #-----thetaの値を蓄積する-----#
    theta_array = latest_theta_array(theta, theta_array)

    #-----P制御-----#
    mp = proportional_control(Kp, theta_array)

    #-----I制御-----#
    mi = integral_control(Ki, theta_array)

    #-----D制御-----#
    md = differential_control(Kd, theta_array)

    #-----PID制御-----#
    m = mp + mi - md

    return m


#direction_adjust
def PID_adjust_direction(target_azimuth, magx_off, magy_off, theta_array: list):
    '''
    目標角度に合わせて方向調整を行う関数
    '''

    #const
    Kp = 0.4
    Kd = 3
    Ki = 0

    t_adj_start = time.time()


    while True:

        #get theta
        error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
        print("error_theta = ", error_theta)

        #PID
        m = PID_control(error_theta, theta_array, Kp, Ki, Kd)

        #limit m
        if m < 0:
            if abs(m) < 10:
                m = -10
            elif abs(m) > 25:
                m = -25
            else:
                pass
        else:
            if m < 10:
                m = 10
            elif m > 25:
                m = 25
            else:
                pass

        #param
        pwr_l = -m
        pwr_r = m

        #move
        motor.motor_move(pwr_l, pwr_r, 0.01)
        time.sleep(0.04)

        #check
        bool_com = True
        for i in range(len(theta_array)):
            if abs(theta_array[i]) > 20:
                bool_com = False
                break
        if bool_com:
            break

        #timeout
        if time.time() - t_adj_start > 1:
            break

    motor.motor_stop(1)


def PID_run(target_azimuth: float, magx_off: float, magy_off: float, theta_array: list, loop_num: int=20):
    '''
    目標地点までの方位角が既知の場合にPID制御により走行する関数

    Parameters
    ----------
    target_azimuth : float
        ローバーを向かせたい方位角
    magx_off : float
        地磁気x軸オフセット
    magy_off : float
        地磁気y軸オフセット
    theta_array : list
        thetaの値を蓄積するリスト
    loop_num : int
        PID制御を行う回数 loop_num=20のとき1秒でこのプログラムが終了する
    '''

    #const
    Kp = 0.1
    Kd = 10
    Ki_ = 0.1

    count = 0


    #main
    for _ in range(loop_num): #1秒間の間に20回ループが回る

        if count < 10:
            Ki = 0
        else:
            Ki = Ki_

        #get theta
        error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
        print("error_theta = ", error_theta)

        #PID
        m = PID_control(error_theta, theta_array, Kp, Ki, Kd)

        #limit m
        m = min(m, 5)
        m = max(m, -5)

        #param
        s_r = 70
        s_l = 65
        pwr_l = -m + s_l
        pwr_r = m + s_r

        #move
        motor.motor_move(pwr_l, pwr_r, 0.02)
        time.sleep(0.08)

        count += 1


def drive(lon_dest :float, lat_dest: float, thd_distance: int, t_cal: float, loop_num: int):
    '''  
    Parameters
    ----------
    lon_dest : float
        目標地点の経度
    lat : float
        目標地点の緯度
    thd_distance : float
        目標地点に到達したと判定する距離（10mぐらいが望ましい？？短くしすぎるとうまく停止してくれない）
    t_cal : float
        キャリブレーションを行う間隔
    log_path : 
        ログの保存先
    t_start : float
        開始時間
    report_log :
        ログの保存先インスタンス
    '''

    global receive
    global send
    global synchro

    #init(flag)
    isReach_dest = 0
    stuck_count = 1

    #cal
    magx_off, magy_off = calibration.cal(40,-40,60) 
    while magx_off == 0 and magy_off == 0:
        motor.motor_move(80, 75, 3)
        magx_off, magy_off = calibration.cal(40,-40,60) 

    #get param(azimuth,distance)
    lat_now,lon_now = gps.location()
    direction = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
    target_azimuth, distance_to_dest = direction["azimuth1"], direction["distance"]

    #adj direction
    theta_array = [0]*5
    PID_adjust_direction(target_azimuth, magx_off, magy_off, theta_array)

    #get param(mag)
    magdata = bmx055.mag_dataRead()
    mag_x = magdata[0]
    mag_y = magdata[1]
    rover_azimuth = calibration.angle(mag_x, mag_y, magx_off, magy_off)
    lat_old, lon_old = gps.location()

    #init(time)
    theta_array = [0]*5
    t_run_start = time.time()


    #main
    while time.time() - t_run_start <= t_cal:
        #get param(azimuth,distance)
        lat_now, lon_now = gps.location()
        direction = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
        distance_to_dest, target_azimuth = direction["distance"], direction["azimuth1"]
        print("distance = ", distance_to_dest, "arg = ", target_azimuth)

        #stuck check
        if stuck_count % 10 == 0:
            #yoko check
            yoko_count = stuck.yoko_jug()
            if yoko_count > 0:
                break

            if stuck.stuck_jug(lat_old, lon_old, lat_now, lon_old, thd=STUCK_JUDGE_THD_DISTANCE):
                pass
            else:
                stuck.stuck_avoid()
            lat_old, lon_old = gps.location()

        #追従しているか確認
        if receive == str(1):
            print("no followed")
            synchro = 1
            break

        #run
        if distance_to_dest > thd_distance:
            PID_run(target_azimuth, magx_off, magy_off, theta_array, loop_num)
        else:
            isReach_dest = 1
            break

        stuck_count += 1

    motor.motor_stop(1)

    return lat_now, lon_now, distance_to_dest, rover_azimuth, isReach_dest

def main():

    #target
    lat_test = 35.924508
    lon_test = 139.911867

    #const
    LOOP_NUM = 20
    THD_DISTANCE_DEST = 5
    T_CAL = 60
    STUCK_JUDGE_THD_DISTANCE = 1

    #init
    theta_differential_array = []

    #setup
    motor.setup()
    bmx055.bmx055_setup()
    mode3.mode3_change()


    #main
    while True:
        lat_now, lon_now, distance_to_dest, rover_azimuth, isReach_dest = drive(lon_dest=lon_test, lat_dest=lat_test, thd_distance=THD_DISTANCE_DEST, t_cal=T_CAL, loop_num=LOOP_NUM)

        #check
        if isReach_dest == 1:
            print('end gps running')
            send_11.log("end gps running")
            break
        else:
            print("not Goal", "distance=",distance_to_dest)
            send_11.log("distance=" + str(distance_to_dest))


if __name__ == "__main__":
    thread1 = threading.Thread(target=main)
    thread2 = threading.Thread(target=blt)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


