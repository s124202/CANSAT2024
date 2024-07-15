#2024/07/15 生川

#standard
import time
from collections import deque

#src
import src.gps as gps
import src.bmx055 as bmx055
import src.motor as motor
from src.main_const import *

#run
import run.calibration as calibration
import run.gps_navigate as gps_navigate
import run.stuck as stuck

#send
import send.mode3 as mode3
import send.send as send

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


#PID
def PID_control(theta, theta_array: list, Kp=0.1, Ki=0.04, Kd=2.5):
    #-----PID制御-----#
    
    #-----初期設定-----# array_numは積分区間の設定
    #array = make_theta_array(array, array_num)

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

    Parameters
    ----------
    target_theta : float
        ローバーを向かせたい方位角
    '''

    #パラメータの設定
    Kp = 0.4
    Kd_ = 3
    Ki_ = 0.03

    count = 0
    
    print('PID_adjust_direction')

    t_adj_start = time.time()

    while True:
        #if time.time() - t_adj_start > 1 and error_theta <= 75: #1秒経過したら強制的に終了する
        #    break
        #elif time.time() - t_adj_start > 1 and error_theta > 75: #スタック回避を行う
        #    print('Stuck Avoid')
        #    stuck.stuck_avoid()

        if count < 25:
            Ki = 0
            Kd = Kd_
        else:
            Ki = Ki_
            Kd = 5

        #-----角度の取得-----#
        error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)

        #-----thetaの値を蓄積する-----#
        theta_array = latest_theta_array(error_theta, theta_array)

        #-----PID制御-----#
        #パラメータが0の場合それは含まれない
        m = PID_control(error_theta, theta_array, Kp, Ki, Kd)

        #-----モータの出力-----#

        m = min(m, 80)
        m = max(m, -80)

        pwr_l = -m
        pwr_r = m

        print(f"{error_theta=}")
        print('left', pwr_l, 'right', pwr_r)

        #-----モータの操作-----#
        motor.motor_move(pwr_l, pwr_r, 0.01)

        time.sleep(0.04)

        #-----角度の取得-----#
        # magdata = bmx055.mag_dataRead()
        # mag_x = magdata[0]
        # mag_y = magdata[1]
        # rover_angle = calibration.angle(mag_x, mag_y, magx_off, magy_off)

        error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)

        # check = 0
        bool_com = True
        for i in range(len(theta_array)):
            if abs(theta_array[i]) > 15:
                bool_com = False
                break
        if bool_com:
            break

        count += 1

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
    #-----パラメータの設定-----#
    Kp = 0.4
    Kd_ = 3
    Ki_ = 0.03

    count = 0
    
    print('PID_drive')

    #-----相対角度の取得-----#
    error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
    print('error theta = ' + str(error_theta))

    theta_array.append(error_theta)

    #-----制御処理-----#
    for _ in range(loop_num): #1秒間の間に20回ループが回る

        if count < 25:
            Ki = 0
            Kd = Kd_
        else:
            Ki = Ki_
            Kd = 5

        #-----相対角度の取得-----#
        error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)

        #-----thetaの値を蓄積する-----#
        theta_array = latest_theta_array(error_theta, theta_array)

        #-----PID制御-----#
        #パラメータが0の場合それは含まれない
        m = PID_control(error_theta, theta_array, Kp, Ki, Kd)

        #-----モータの出力-----#

        #直進補正分(m=0のとき直進するように設定するため)
        s_r = 40
        s_l = 40

        #モータ出力の最大値と最小値を設定
        m = min(m, 20)
        m = max(m, -10)

        #モーター出力の決定
        pwr_l = -m + s_l
        pwr_r = m + s_r

        #-----モータの操作-----#
        motor.motor_move(pwr_l, pwr_r, 0.05)

        time.sleep(0.05)

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

    #-----初期設定-----#
    #stuck_count = 1
    isReach_dest = 0
    #control = 0

    #-----キャリブレーション-----#
    time.sleep(1)
    print("ready")
    time.sleep(3)
    magx_off, magy_off = calibration.cal(80,-80,3)

    #-----目標地点への角度を取得-----#
    direction = calibration.calculate_direction(lon2=lon_dest, lat2=lat_dest)
    target_azimuth, distance_to_dest = direction["azimuth1"], direction["distance"]

    #-----PID制御による角度調整-----#
    theta_array = [0]*5
    PID_adjust_direction(target_azimuth, magx_off, magy_off, theta_array)

    #-----現在のローバーの情報取得-----#
    magdata = bmx055.mag_dataRead()
    mag_x = magdata[0]
    mag_y = magdata[1]
    #lat_old, lon_old = gps.location() #最初のスタックチェック用の変数の設定
    rover_azimuth = calibration.angle(mag_x, mag_y, magx_off, magy_off) #戻り値

    theta_array = [0]*5
    t_run_start = time.time() #GPS走行開始前の時刻

    print('###---GPS走行---###')

    while time.time() - t_run_start <= t_cal:
        lat_now, lon_now = gps.location()
        direction = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
        distance_to_dest, target_azimuth = direction["distance"], direction["azimuth1"]
        print("緯度、経度 = ", lat_now, lon_now)
        print("距離、角度 = ", distance_to_dest, target_azimuth)

        #-----スタックチェック-----#
        #if stuck_count % 25 == 0:
        #    lat_new, lon_new = lat_now, lon_now
        #    if stuck.stuck_jug(lat_old, lon_old, lat_new, lon_new, thd=STUCK_JUDGE_THD_DISTANCE):
        #        pass
        #    else:
        #        stuck.stuck_avoid()
        #        pass
        #    lat_old, lon_old = gps.location()

        #-----PID制御による走行-----#
        if distance_to_dest > thd_distance:
            PID_run(target_azimuth, magx_off, magy_off, theta_array, loop_num)
        else:
            isReach_dest = 1 #ゴール判定用のフラグ

        #stuck_count += 1 #25回に一回スタックチェックを行う

        if isReach_dest == 1:
            break

    motor.motor_stop(1)

    return lat_now, lon_now, distance_to_dest, rover_azimuth, isReach_dest



if __name__ == "__main__":

    lat_test = 35.918636
    lon_test = 139.908348

    mode3.mode3_change()
    #lat_test,lon_test = gps.gps_med()

    #-----セットアップ-----#
    motor.setup()
    bmx055.bmx055_setup()

    #-----初期設定-----#
    theta_differential_array = []
    theta_array = [0]*5
    direction = calibration.calculate_direction(lon2=lon_test, lat2=lat_test)
    distance_to_goal = direction["distance"]

    send.log("pid_run_start")
    
    while True:
        lat_now, lon_now, distance_to_dest, rover_azimuth, isReach_dest = drive(lon_dest=lon_test, lat_dest=lat_test, thd_distance=THD_DISTANCE_DEST, t_cal=T_CAL, loop_num=LOOP_NUM)
        
        print('isReach_dest = ', isReach_dest)

        if isReach_dest == 1: #ゴール判定
            print('Goal')
            send.log("end_gps_running")
            break
        else:
            print("not_Goal", "distance=",distance_to_dest)
            send.log("distance=" + str(distance_to_dest))