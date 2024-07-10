import threading
import time
from gpiozero import Motor

import blt_sub

def setup():
	"""
	motorを使うときに必要な初期化を行う関数
	"""
	global motor_r, motor_l
	Rpin1, Rpin2 = 23, 18
	Lpin1, Lpin2 = 16, 26
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

def move(strength_l, strength_r, t_moving):
	"""
	一定時間モータを動かすための関数
	strengthは-100~100
	t_movingはモータを動かす時間
	"""
	motor_move(strength_l, strength_r, t_moving)
	if abs(strength_l) == abs(strength_r) and strength_l * strength_r < 0:
		motor_stop(0.1)
	else:
		deceleration(strength_l, strength_r)

def motor_continue(strength_l, strength_r):
    """
    モータを連続的に動かすための関数
    引数は-100~100
    """
    strength_l = strength_l / 100
    strength_r = strength_r / 100
    if strength_r >= 0 and strength_l >= 0:
        motor_r.forward(strength_r)
        motor_l.forward(strength_l)
    # 後進
    elif strength_r < 0 and strength_l < 0:
        motor_r.backward(abs(strength_r))
        motor_l.backward(abs(strength_l))
    # 右回転
    elif strength_r >= 0 and strength_l < 0:
        motor_r.forward(abs(strength_r))
        motor_l.backward(abs(strength_l))
    # 左回転
    elif strength_r < 0 and strength_l >= 0:
        motor_r.backward(abs(strength_r))
        motor_l.forward(abs(strength_l))

def test():
	
	setup()
	move(30,30,30)

def main():
    thread1 = threading.Thread(target = test())
    thread2 = threading.Thread(target = blt_sub.blt())

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()