import time
from math import*
import motor


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


def PD_run(s_l=35, s_r=35):
    #const
    Kp = 0.4
    Kd = 3

    #theta
    error_theta = 1 #ここ要調整
    theta_array = latest_theta_array(error_theta, theta_array)

    #PD
    m = PD_control(error_theta, theta_array, Kp, Kd)

    #m調整
    m = min(m, 7)
    m = max(m, -7)

    #モーター出力の決定
    pwr_l = -m + s_l
    pwr_r = m + s_r

    return pwr_l,pwr_r


if __name__ == "__main__":
    #const
    theta_differential_array = []
    theta_array = [0]*5
    Kp = 0.4
    Kd = 3
    #直進成分
    s_r = 30
    s_l = s_r + 7

    while True:
        error_theta = 1 #ここ調整
        theta_array = latest_theta_array(error_theta, theta_array)

        m = PD_control(error_theta, theta_array)

        #m調整
        m = min(m, 7)
        m = max(m, -7)

        #モーター出力の決定
        pwr_l = -m + s_l
        pwr_r = m + s_r

        motor.motor_move(pwr_l, pwr_r, 0.01)
        time.sleep(0.04)