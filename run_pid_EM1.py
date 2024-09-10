#2024/07/29 生川
#VOC基盤 両モーター回転逆で作成　2024/07/26
#CO2基盤 右モーター回転逆で作成　2024/07/29

#standard
import time
import bluetooth
import threading
from queue import Queue
import csv

#src
import gps
import bmx055
import run_following_EM1
import calibration
import gps_navigate
import board
import adafruit_sgp40
import stuck

import send.send_10 as send_10

from main_const import *

def blt():
	global send
	global receive
	global synchro

	send = 1
	receive = "1"
	synchro = 0

	try:
		server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		port = 1
		server_sock.bind(("",port))
		server_sock.listen(1)
		server_sock.settimeout(10)
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
				time.sleep(0.5)
				client_sock.send(str(send))
			except KeyboardInterrupt:
				print("finish")
				break
			except bluetooth.btcommon.BluetoothError as err:
				print("close")
				break
		client_sock.close()
		server_sock.close()
		print("try reconnect")

	except:
		print("finish")
		try:
			server_sock.close()
			client_sock.close()
		except:
			pass


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
		run_following_EM1.motor_move_default(pwr_l, pwr_r, 0.01)
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

	run_following_EM1.motor_stop_default(1)


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
	global receive

	#const
	Kp = 2
	Kd = 0.5
	Ki = 0


	#main
	for _ in range(loop_num): #1秒間の間に20回ループが回る
		#get theta
		error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
		print("error_theta = ", error_theta)

		#PID
		m = PID_control(error_theta, theta_array, Kp, Ki, Kd)

		#limit m
		m = min(m, 5)
		m = max(m, -5)

		#param
		pwr_l = -m + RUN_PID_L
		pwr_r = m + RUN_PID_R

		#move
		run_following_EM1.motor_move_default(pwr_l, pwr_r, 0.1)
		time.sleep(0.1)

		if receive == str(10):
			print("wait")
			break


def drive(writer, lat_dest: float, lon_dest :float, thd_distance: int, stack_distance: float, t_cal: float, loop_num: int):
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

	global send
	global receive

	receive = "1"

	for i in range (100):
		if receive == str(0):
			break
		if receive == str(4) or i == 99:
			return 100,0
		time.sleep(1)
		if i % 15 == 14:
			run_following_EM1.move_default(ROTATE_PWR,-ROTATE_PWR,0.2)

	#子機を待たせる
	send = 1

	#cal
	magx_off, magy_off = calibration.cal(RUN_CAL,-RUN_CAL,60) 
	# while magx_off == 0 and magy_off == 0:
	# 	motor.motor_move(80, -75, 1)
	# 	magx_off, magy_off = calibration.cal(40,40,60) 

	#get param(mag)
	lat_old, lon_old = gps.location()

	#子機の発見待ち
	send = 2
	time.sleep(1)
	for i in range(100):
		time.sleep(1)
		if receive == str(1):
			break
		if receive == str(4) or i == 99:
			return 100,0
		if i % 15 == 14:
			run_following_EM1.move_default(ROTATE_PWR,-ROTATE_PWR,0.2)
	send = 0
	time.sleep(2.8)

	#init(time)
	theta_array = [0]*5
	t_run_start = time.time()

	#init(flag)
	isReach_dest = 0
	stuck_count = 1


	#main
	while time.time() - t_run_start <= t_cal:
		#get param(azimuth,distance)
		lat_now, lon_now = gps.location()
		direction = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
		distance_to_dest, target_azimuth = direction["distance"], direction["azimuth1"]
		error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
		print("distance = ", distance_to_dest, "arg = ", target_azimuth)
		writer.writerows([[lat_now, lon_now, error_theta]])

		#stuck check
		if stuck_count % 5 == 0:
			#yoko check
			yoko_count = stuck.yoko_jug()
			stuck.ue_jug()
			if yoko_count > 0:
				break

			if stuck.stuck_jug(lat_old, lon_old, lat_now, lon_old, thd=stack_distance):
				pass
			else:
				stuck.stuck_avoid()
				stuck.ue_jug()

			send_10.log("lat:" + str(lat_now) + "," + "lon:" + str(lon_now) + "," + "distance:" + str(distance_to_dest))
			lat_old, lon_old = gps.location()

		#run
		if distance_to_dest > thd_distance:
			PID_run(target_azimuth, magx_off, magy_off, theta_array, loop_num)
		else:
			isReach_dest = 1
			break

		if receive == str(10):
			break

		stuck_count += 1

	run_following_EM1.motor_stop_default(1)

	return distance_to_dest, isReach_dest


def test(lat,lon,q):
	global receive
	global synchro
	global send
	synchro = 0
	#target
	lat_test = (lat + RUN_LAT) / 2
	lon_test = (lon + RUN_LON) / 2

	#setup
	i2c = board.I2C() 
	sgp = adafruit_sgp40.SGP40(i2c)

	filename = "following_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	f = open(filename,"w")
	writer = csv.writer(f)
	filename2 = "raw_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	f2 = open(filename2,"w")
	writer2 = csv.writer(f2)

	#main
	while True:
		distance_to_dest, isReach_dest = drive(writer, lat_dest=lat_test, lon_dest=lon_test, thd_distance=PID_THD_DISTANCE_DEST, stack_distance=PID_STUCK_JUDGE_THD_DISTANCE, t_cal=PID_T_CAL, loop_num=PID_LOOP_NUM)
		print("Raw Gas: ", sgp.raw)
		writer2.writerows([[sgp.raw]])

		#check
		if receive == str(4):
			q.put(1)
			print("switch to autonomy")
			synchro = 1
			return
		
		if  distance_to_dest == 100 and isReach_dest == 0:
			q.put(1)
			print("switch to autonomy")
			synchro = 1
			return

		if isReach_dest == 1:
			print('end gps running')
			send_10.log("end gps running")
			q.put(0)
			send = 5
			time.sleep(3)
			synchro = 1
			return
		else:
			print("not Goal", "distance=",distance_to_dest)
			send_10.log("distance=" + str(distance_to_dest))

def main(lat,lon):
	q = Queue()

	thread1 = threading.Thread(target = blt)
	thread2 = threading.Thread(target = test, args=(lat,lon,q,))

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

	return q.get()


if __name__ == "__main__":
	#setup
	run_following_EM1.setup()
	bmx055.bmx055_setup()
	mode3.mode3_change()
	
	a = main(40,139)
	print(a)