import time

import bmx055
import motor

def correct_posture():
    """
    ローバーの状態を確認する関数
    通常状態:True
    逆さになってる:False
    加速度センサZ軸の正負で判定する
    """
    count = 0
    while 1:
        xa = []
        za = []
        for i in range(3):
            accData = bmx055.acc_dataRead()
            xa.append(accData[0])
            za.append(accData[2])
            time.sleep(0.2)
        x = max(xa)
        z = max(za)

        if z >= 7.5 and x > 0:
            print('上だよ')
            break
        else:
            print(f'下だよ{count}')
            print(f'acc: {z}')
            if count > 2:
                motor.move(85, -85, 0.1, False)
            elif count > 4:
                motor.move(90, -90, 0.1, False)
            elif count > 6:
                motor.move(95, -95, 0.1, False)
            elif count > 8:
                motor.move(99, -99, 0.1, False)
            else:
                motor.move(80, -80, 0.1, False)
            time.sleep(2)
            count += 1