#2024/07/22 生川

#standard
import time
import random

#src
import motor
import gps
import bmx055
import gps_navigate


def ue_jug():
    ue_count = 0
    
    #ローバーの状態を確認する関数
    #通常状態：True
    #逆さになってる：False
    #加速度センサZ軸の正負で判定するよ
    
    while 1:
        za = []
        for i in range(3):
            accdata = bmx055.acc_dataRead()
            za.append(accdata[2])
            time.sleep(0.2)
        z = max(za)
        
        if z > 3:
            print('上だよ')
            break
        else:
            print(f'下だよ{ue_count}')
            print(f'acc: {z}')
            if ue_count >= 2 and ue_count < 4:
                motor.move(40, 40, 0.08)
            elif ue_count >= 4 and ue_count < 6:
                motor.move(70, 70, 0.08)
            elif ue_count >= 6 and ue_count < 8:
                motor.move(100, 100, 0.5)
            else:
                motor.move(12, 12, 1)
            time.sleep(2)
            ue_count += 1


def yoko_jug():
    yoko_count = 0
    
    #ローバーの状態を確認する関数
    #加速度センサX軸の正負で判定するよ
    
    while 1:
        x_array = []
        for i in range(3):
            accdata = bmx055.acc_dataRead()
            x_array.append(abs(accdata[0]))
            time.sleep(0.2)
        x = max(x_array)
        
        if x < 9 or 15 < x:
            print('正常だよ')
            break
        else:
            print(f'横だよ{yoko_count}')
            print(f'abs(acc): {x}')
            if yoko_count % 2 == 0:
                motor.move(15, -15, 3)
            else:
                motor.move(-15, 15, 3)
            time.sleep(1)
            yoko_count += 1
    
    return yoko_count


def stuck_jug(lat1, lon1, lat2, lon2, thd=5.0):
    data_stuck = gps_navigate.vincenty_inverse(lat1, lon1, lat2, lon2)
    if data_stuck['distance'] <= thd:
        print(str(data_stuck['distance']) + '-----stucked')
        return False
    else:
        print(str(data_stuck['distance']) + '-----not stucked')
        return True


def random(a, b, k):
    ns = []
    while len(ns) < k:
        n = random.randint(a, b)
        if not n in ns:
            ns.append(n)
    return ns


def stuck_avoid_move(x):
    if x == 0:
        motor.move(-100, -100, 2)
        time.sleep(1)
        motor.move(-60, -60, 5)
        time.sleep(1)
    elif x == 1:
        motor.move(40, -40, 1)
        time.sleep(1)
        motor.move(80, 80, 5)
        time.sleep(1)
    elif x == 2:
        motor.move(-100, 100, 2)
        time.sleep(1)
        motor.move(80, 80, 5)
        time.sleep(1)
    elif x == 3:
        motor.move(100, -100, 2)
        time.sleep(1)
        motor.move(80, 80, 5)
        time.sleep(1)
    elif x == 4:
        motor.move(40, -40, 1)
        time.sleep(1)
        motor.move(-80, -80, 5)
        time.sleep(1)
    elif x == 5:
        motor.move(40, -40, 1)
        time.sleep(1)
        motor.move(-80, -80, 5)
        time.sleep(1)
    elif x == 6:
        motor.move(100, -100, 3)
        time.sleep(1)
        motor.move(80, 80, 3)
        time.sleep(1)

def stuck_avoid():
    print('start stuck  avoid')
    flag = False
    while 1:
        lat_old, lon_old = gps.location()
        # 0~6
        for i in range(7):
            stuck_avoid_move(i)
            lat_new, lon_new = gps.location()
            bool_stuck = stuck_jug(lat_old, lon_old, lat_new, lon_new, 0.5)
            if bool_stuck == True:
                flag = True
                break
        if flag:
            break
        # 3,2,1,0
        for i in range(7):
            stuck_avoid_move(7 - i)
            lat_new, lon_new = gps.location()
            bool_stuck = stuck_jug(lat_old, lon_old, lat_new, lon_new, 0.5)
            if bool_stuck == False:
                flag = True
                break
        if flag:
            break
        random = random(0, 6, 7)
        for i in range(7):
            stuck_avoid_move(random[i])
            lat_new, lon_new = gps.location()
            bool_stuck = stuck_jug(lat_old, lon_old, lat_new, lon_new, 0.5)
            if bool_stuck == False:
                flag = True
                break
        if flag:
            break
    time.sleep(10) #モータ休めるために停止
    print('complete stuck avoid')


if __name__ == '__main__':
    motor.setup()
    bmx055.bmx055_setup()
    yoko_count = yoko_jug()
    ue_jug()

    # while 1:
    #     a = int(input('出力入力しろ'))
    #     b = float(input('時間入力しろ'))
    #     motor.move(a, a, b)

    stuck_avoid()