#2024/07/08 生川

#standard
import numpy as np
import math
import time

#src
import src.bmx055 as bmx055
import src.gps as gps
import src.motor as motor

#run
import run.stuck as stuck


def get_data():
    """
    BMX055からデータを得る
    """
    try:
        magData = bmx055.mag_dataRead()
    except KeyboardInterrupt:
        print()
    except Exception as e:
        print()
        print(e)
    # --- get magnet sensor data ---#
    magx = magData[0]
    magy = magData[1]
    magz = magData[2]
    return magx, magy, magz


def get_data_offset(magx_off, magy_off, magz_off):
    """
        BMX055からオフセットを考慮して磁気データを得る関数
        """
    try:
        magData = bmx055.mag_dataRead()
    except KeyboardInterrupt:
        print()
    except Exception as e:
        print()
        print(e)
    # --- get magnet sensor data ---#
    magx = magData[0] - magx_off
    magy = magData[1] - magy_off
    magz = magData[2] - magz_off
    return magx, magy, magz


def magdata_matrix(l, r, n):
    """
        キャリブレーション用の地磁気データを得るための関数。
        モータを連続的に動かして回転して地磁気データを得る。
        """
    try:
        stuck.ue_jug()
        magx, magy, magz = get_data()
        magdata = np.array([[magx, magy, magz]])
        for _ in range(n - 1):
            motor.motor_continue(l, r)
            magx, magy, magz = get_data()
            print(magx, magy)
            # --- multi dimension matrix ---#
            magdata = np.append(magdata, np.array(
                [[magx, magy, magz]]), axis=0)
            time.sleep(0.03)

        motor.deceleration(l, r)
    except KeyboardInterrupt:
        print('Interrupt')

    return magdata


def magdata_matrix_hand():
    """
        キャリブレーション用の磁気値を手持ちで得るための関数
        """
    try:
        magx, magy, magz = get_data()
        magdata = np.array([[magx, magy, magz]])
        for i in range(60):
            print('少し回転')
            time.sleep(0.05)
            print(f'{i + 1}回目')
            magx, magy, magz = get_data()
            # --- multi dimension matrix ---#
            magdata = np.append(magdata, np.array(
                [[magx, magy, magz]]), axis=0)
    except KeyboardInterrupt:
        print('Interrupt')
    except Exception as e:
        print(e.message())
    return magdata


def magdata_matrix_offset(l, r, t, magx_off, magy_off, magz_off):
    """
        オフセットを考慮したデータセットを取得するための関数
        """
    try:
        magx, magy, magz = get_data_offset(magx_off, magy_off, magz_off)
        magdata = np.array([[magx, magy, magz]])
        for _ in range(20):
            motor(l, r, t)
            magx, magy, magz = get_data_offset(magx_off, magy_off, magz_off)
            # --- multi dimension matrix ---#
            magdata = np.append(magdata, np.array(
                [[magx, magy, magz]]), axis=0)
    except KeyboardInterrupt:
        print('Interrupt') #log
    except Exception as e:
        print(e.message()) #log
    return magdata


def calculate_offset(magdata):
    """
    オフセットを計算する関数
    """
    # --- manage each element sepalately ---#
    magx_array = magdata[:, 0]
    magy_array = magdata[:, 1]
    magz_array = magdata[:, 2]

    # --- find maximam gps value and minimam gps value respectively ---#
    magx_max = magx_array[np.argmax(magx_array)]
    magy_max = magy_array[np.argmax(magy_array)]
    magz_max = magz_array[np.argmax(magz_array)]

    magx_min = magx_array[np.argmin(magx_array)]
    magy_min = magy_array[np.argmin(magy_array)]
    magz_min = magz_array[np.argmin(magz_array)]

    # --- calucurate offset ---#
    magx_off = (magx_max + magx_min) / 2
    magy_off = (magy_max + magy_min) / 2
    magz_off = (magz_max + magz_min) / 2

    return magx_array, magy_array, magz_array, magx_off, magy_off, magz_off


def cal(l, r, n):
    magdata = magdata_matrix(l, r, n)
    _, _, _, magx_off, magy_off, _ = calculate_offset(magdata)
    print('magx_off:', magx_off, 'magy_off:', magy_off)
    return magx_off, magy_off


#手動キャリブレーション
def cal2():
    magdata = magdata_matrix_hand()
    _, _, _, magx_off, magy_off, _ = calculate_offset(magdata)
    print('magx_off:', magx_off, 'magy_off:', magy_off)
    return magx_off, magy_off

#ちゃんと北をむいてる確認する
def angle(magx, magy, magx_off=0, magy_off=0):
    '''
    ローバーが向いている方位角を計算する関数
    '''

    if magy - magy_off == 0:
        magy += 0.000001
    if magx - magx_off == 0:
        magx += 0.000001
    theta = math.degrees(math.atan((magy - magy_off) / (magx - magx_off)))

    if magx - magx_off > 0 and magy - magy_off > 0:  # First quadrant
        pass  # 0 <= theta <= 90
    elif magx - magx_off < 0 and magy - magy_off > 0:  # Second quadrant
        theta = theta + 180  # 90 <= theta <= 180
    elif magx - magx_off < 0 and magy - magy_off < 0:  # Third quadrant
        theta = theta + 180  # 180 <= theta <= 270
    elif magx - magx_off > 0 and magy - magy_off < 0:  # Fourth quadrant
        theta = theta + 360  # 270 <= theta <= 360

    theta += 180 #センサの傾きを考慮する場合？？
    theta  = theta % 360

    return theta


if __name__ == "__main__":
    
    n = int(input("motor？"))
    motor.setup()
    bmx055.bmx055_setup()
    magx_off, magy_off = cal(n,-n,40)