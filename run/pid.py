import time
from collections import deque

import gps_navigate
import gps
import calibration
import src.bmx055 as bmx055
import stuck
import src.motor as motor
import basics
from main_const import *


def get_theta_dest_gps(lon_dest, lat_dest, magx_off, magy_off):
    '''
    目標地点(dest)との相対角度を算出する関数
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

    rover_angle = calibration.angle(mag_x, mag_y, magx_off, magy_off)
    direction = calibration.calculate_direction(lon_dest, lat_dest)
    azimuth = direction["azimuth1"]

    #-----目標地点との相対角度を算出-----#
    #ローバーが向いている角度を0度としたときの、目的地への相対角度。このとき時計回りを正とする。
    theta_dest = rover_angle - azimuth

    #-----相対角度の範囲を-180~180度にする-----#
    theta_dest = basics.standarize_angle(theta_dest)

    return theta_dest

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
    theta_dest = basics.standarize_angle(theta_dest)

    return theta_dest

theta_array = []
theta_differential_array = []

    
def make_theta_array(array: list, array_num: int):
    '''
    クソコでした by 田口 8/28 -> [0]*5で可能
    '''
    #-----決められた数の要素を含む空配列の作成-----#

    for i in range(array_num):
        array.append(0)
    
    return array

def latest_theta_array(theta, array:list):
    #-----thetaの値を蓄積する-----#

    #古い要素を消去
    del array[0]

    #新しい要素を追加
    array.append(theta)

    return array

def proportional_control(Kp, theta_array :list):
    #-----P制御-----#
    
    #-----最新のthetaの値を取得-----#
    theta_deviation = theta_array[-1]

    mp = Kp * theta_deviation

    return mp

def integral_control(Ki, theta_array: list):
    #I制御

    #積分係数の設定
    #Ki = 0.5

    #thetaの積分処理
    theta_integral = sum(theta_array)

    mi = Ki * theta_integral

    return mi

def differential_control(Kd, theta_array: list):
    #D制御

    #微分係数の設定
    #Kd = 0.5

    #thetaの微分処理
    for i in range(len(theta_array)):
        theta_differential_value = theta_array[i] - theta_array[i-1]
        theta_differential_array.append(theta_differential_value)

    #最新のthetaの微分値を取得
    theta_differential = theta_differential_array[-1]

    md = Kd * theta_differential

    return md

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

def PID_adjust_direction(target_azimuth, magx_off, magy_off, theta_array: list):
    '''
    目標角度に合わせて方向調整を行う関数
    最終version

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
    # controller = PID_Controller(kp=0.4, ki=0.03, kd=3, target=target_theta, num_log=5, validate_ki=25)
    
    print('PID_adjust_direction')

    #-----ローバーの角度の取得-----#
    # error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)

    # # output = controller.get_output(theta)
    # # print(controller.kp)
    
    # print('error theta = ' + str(error_theta))

    # theta_array.append(error_theta)

    #-----制御処理-----#
    #while abs(theta_array[-1]) > 5:

    t_adj_start = time.time()

    while True:
        if time.time() - t_adj_start > 1 and error_theta <= 75: #5秒経過したら強制的に終了する
            break
        elif time.time() - t_adj_start > 1 and error_theta > 75: #スタック回避を行う
            print('Stuck Avoid')
            stuck.stuck_avoid()

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

        m = min(m, 40)
        m = max(m, -40)

        pwr_l = -m
        pwr_r = m

        print(f"{error_theta=}")
        print('left', pwr_l, 'right', pwr_r)

        #-----モータの操作-----#
        motor.motor_move(pwr_l, pwr_r, 0.01)
        #motor.move(pwr_l, pwr_r, 0.2)

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
    #Kp = 0.4
    Kp = 0.25
    #Kd_ = 3
    Kd_ = 5 
    #Ki_ = 0.03
    Ki_ = 0.02

    count = 0
    
    # print('PID_drive')

    #-----相対角度の取得-----#
    error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
    print('error theta = ' + str(error_theta))

    theta_array.append(error_theta)

    #-----制御処理-----#
    for _ in range(loop_num): #1秒間の間に20回ループが回る

        if count < 10: #25から15に変更 by 田口 8/23 15から10に変更 by 田口 8/31
            Ki = 0
            Kd = Kd_
        else:
            Ki = Ki_
            Kd = 5

        #-----相対角度の取得-----#
        error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
        if _ == 0:
            control = -error_theta

        #-----thetaの値を蓄積する-----#
        theta_array = latest_theta_array(error_theta, theta_array)

        #-----PID制御-----#
        #パラメータが0の場合それは含まれない
        m = PID_control(error_theta, theta_array, Kp, Ki, Kd)

        #-----モータの出力-----#

        #直進補正分(m=0のとき直進するように設定するため) # 35から25に変更 by 田口 8/28
        s_r = 35
        s_l = 35

        # モータ出力の最大値と最小値を設定
        m = min(m, 15)
        m = max(m, -15)

        pwr_l = -m + s_l
        pwr_r = m + s_r

        # print(f"{error_theta=}")
        # print(f'{error_theta}=')
        # print('left', pwr_l, 'right', pwr_r)

        #-----モータの操作-----#
        motor.motor_move(pwr_l, pwr_r, 0.01)

        time.sleep(0.04)

        count += 1

    return control


def drive3(lon_dest :float, lat_dest: float, thd_distance: int, t_cal: float, loop_num: int, report_log):
    '''
    任意の地点までPID制御により走行する関数
    最終version これを使う
    
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

    #-----PID制御用のパラメータの設定-----#
    # KP = 0.4
    # KD = 3
    # KI = 0.03

    #-----初期設定-----#
    stuck_count = 1
    isReach_dest = 0
    report_count = 0
    control = 0

    #-----キャリブレーション-----#
    time.sleep(1)
    magx_off, magy_off = calibration.cal(40, -40, 30)

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
    lat_old, lon_old = gps.location() #最初のスタックチェック用の変数の設定
    rover_azimuth = calibration.angle(mag_x, mag_y, magx_off, magy_off) #戻り値

    theta_array = [0]*5
    t_run_start = time.time() #GPS走行開始前の時刻

    print('###---GPS走行---###')

    while time.time() - t_run_start <= t_cal:
        lat_now, lon_now = gps.location()
        direction = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
        distance_to_dest, target_azimuth = direction["distance"], direction["azimuth1"]
        print(lat_now, lon_now)

        #-----スタックチェック-----#
        if stuck_count % 25 == 0:
            lat_new, lon_new = lat_now, lon_now
            if stuck.stuck_jug(lat_old, lon_old, lat_new, lon_new, thd=STUCK_JUDGE_THD_DISTANCE):
                pass
            else:
                stuck.stuck_avoid()
                pass
            lat_old, lon_old = gps.location()

        #-----PID制御による走行-----#
        if distance_to_dest > thd_distance:
            control = PID_run(target_azimuth, magx_off, magy_off, theta_array, loop_num)
        else:
            isReach_dest = 1 #ゴール判定用のフラグ

        #-Log-#
        if report_count % 5 == 0: #30から20回に一回ログをとることにした
            report_log.save_log(lat_now, lon_now, target_azimuth, control)

        stuck_count += 1 #25回に一回スタックチェックを行う
        report_count += 1

        if isReach_dest == 1:
            break

    motor.motor_stop(1)

    return lat_now, lon_now, distance_to_dest, rover_azimuth, isReach_dest



if __name__ == "__main__":

    lat_test = 40.893549
    lon_test = -119.109417

    #-----セットアップ-----#
    motor.setup()
    bmx055.bmx055_setup()
    #-----初期設定-----#
    theta_differential_array = []

    #-----要素数5の空配列の作成-----#
    theta_array = [0]*5

    #-----オフセットの取得-----#
    #-----キャリブレーション-----#
    # print('Start Calibration')
    # magx_off, magy_off = calibration.cal(30, -30, 40)　<-これがあるせいでおそらく2回キャリブレーションをしていた。

    #-----PID制御-----#

    # while True:
    #     input_azimuth = float(input('目標角度は？'))
    #     PID_adjust_direction(input_azimuth, magx_off, magy_off, theta_array)

    # PID_adjust_direction(180, magx_off, magy_off, theta_array)

    # time.sleep(1)

    # PID_adjust_direction(0, magx_off, magy_off, theta_array)

    # time.sleep(1)

    # PID_adjust_direction(90, magx_off, magy_off, theta_array)

    # time.sleep(1)

    # PID_adjust_direction(270, magx_off, magy_off, theta_array)

    # time.sleep(4)

    #-----PID制御によるGPS走行-----#
    #-----目標地点の設定-----#
    # lat_goal = 35.9242411
    # lon_goal = 139.9120618



    # drive(lon_dest=lon_goal, lat_dest=lat_goal, thd_distance=5, t_run=60, log_path='/home/dendenmushi/cansat2023/sequence/log/gpsrunningLog.txt')

    #-Log Set Up-#

    # pid_test_log = log.Logger(dir='', filename='pid_test', t_start=time.time(), columns=['lat', 'lon', 'distance', 'rover_azimuth', 'isReach_dest'])


    direction = calibration.calculate_direction(lon2=lon_test, lat2=lat_test)
    distance_to_goal = direction["distance"]

    while True: #1ループおおよそT_CAL秒
        #-T_CALごとに以下の情報を取得-#
        lat_now, lon_now, distance_to_dest, rover_azimuth, isReach_dest = drive3(lon_dest=lon_test, lat_dest=lat_test, thd_distance=THD_DISTANCE_DEST, t_cal=T_CAL, loop_num=LOOP_NUM)
        
        print('isReach_dest = ', isReach_dest)

        # pid_test_log.save_log(lat_now, lon_now, distance_to_dest, rover_azimuth, isReach_dest)
        #-Log-#
        # gps_running_goal_log.save_log(lat_now, lon_now, distance_to_dest, rover_azimuth, isReach_dest)    
            
        if isReach_dest == 1: #ゴール判定
            print('Goal')
            break