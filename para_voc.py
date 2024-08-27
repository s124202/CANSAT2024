import purple_detection
import motor
import calibration
import gps_navigate
import bmx055
import gps
import stuck

import bluetooth
import threading
import time

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

def run_calibration():
	magx_off, magy_off = calibration.cal(25,-25,40) 
	while magx_off == 0 and magy_off == 0:
		motor.motor_move(50, 50, 1)
		magx_off, magy_off = calibration.cal(25,-25,40) 
	
	return magx_off, magy_off

def get_param(magx_off, magy_off, lat_dest, lon_dest):
	lat_now, lon_now = gps.location()
	direction = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
	distance_to_dest, target_azimuth = direction["distance"], direction["azimuth1"]
	error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
	print("distance = ", distance_to_dest, "error = ", error_theta)

	return error_theta, distance_to_dest, lat_now, lon_now

def adjust_direction(magx_off, magy_off, lat_dest, lon_dest):
	#init
	t_out = 30
	t_start = time.time()

	while time.time() - t_start < t_out:
		error_theta, direction, lat_now, lon_now = get_param(magx_off, magy_off, lat_dest, lon_dest)

		if error_theta < -10:
			motor.move(30,-30,0.1)
		elif error_theta > 10:
			motor.move(-30,30,0.1)
		else:
			break

		time.sleep(0.3)

	print("finish adjust")

def blt_adalt():
	global send
	global receive
	global synchro

	send = 0
	receive = "0"
	synchro = 0

	while True:
		
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

			print("try reconnect")
		except:
			print("finish")
			try:
				server_sock.close()
				client_sock.close()
			except:
				pass
			break
		if synchro == 1:
			break

def blt_child():
	global send
	global receive
	global synchro
	send = 0
	receive = "0"
	synchro = 0

	bd_addr = BLT_ADRESS # サーバー側のデバイスアドレスを入力

	port = 1

	for _ in range (10):
		try:
			sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			sock.connect((bd_addr, port))
			print("connect success")
			break
		except:
			print("try again")
			time.sleep(1)
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

		except KeyboardInterrupt:
			print("finish")
			break
		except bluetooth.btcommon.BluetoothError as err:
			print("close")
			break

	sock.close()


#下に続く並列の関数を使用
def para_adalt():
	PARA_THD_COVERED = 300000
	PARA_SLEEP = 300
	LAT_DEST = 35.9243193
	LON_DEST = 139.9124873
	PARA_BLT_TIMEOUT = 45

	global send
	global receive
	global synchro

	purple_area = 0

	stuck.ue_jug()

	try:
		purple_area = purple_detection.detect_para()
		print(f'purple_area : {purple_area}')

		while True:
				if PARA_THD_COVERED < purple_area:
					print("Parachute on top")
					time.sleep(PARA_SLEEP)
					motor.motor_move(70, 70, 3)
				else:
					break

		if purple_area > 100:
			print("Move Backward")
			motor.motor_move(-30, -30, 2)
			motor.motor_stop(0.2)

		else:
			print("Move Forward")
			motor.motor_move(30, 30, 2)
			motor.motor_stop(0.2)

		time.sleep(3)
		stuck.ue_jug()

		while True:
			print('Starting Calibration')
			magx_off, magy_off = run_calibration()
			adjust_direction(magx_off, magy_off, lat_dest = LAT_DEST, lon_dest = LON_DEST)
			purple_area = purple_detection.detect_para()
			print(f'purple_area : {purple_area}')
			if purple_area > 100:
				motor.motor_move(-30, 30, 0.25)
				motor.motor_stop(0.5)

				time.sleep(1)

				motor.motor_move(30, 30, 1)

				time.sleep(1)
				stuck.ue_jug()
			else:
				break
			
		print("Last Move Forwward")
		motor.motor_move(30, 30, 2)

		#子機のパラ回避待ち
		send = 1
		time_start = time.time()
		while True:
			confirm = receive
			if confirm == str(1):
				print("child para avoid finish")
				break
			elif time.time() - time_start > PARA_BLT_TIMEOUT:
				print("partner timeout")
				break
			else:
				print("child para avoid waiting...")
			time.sleep(3)
		synchro = 1
	
	except:
		print("Camera died")
		motor.motor_move(40, 40, 4)

		#子機のパラ回避待ち
		send = 1
		time_start = time.time()
		while True:
			confirm = receive
			if confirm == str(1):
				print("child para avoid finish")
				break
			elif time.time() - time_start > PARA_BLT_TIMEOUT:
				print("partner timeout")
				break
			else:
				print("child para avoid waiting...")
			time.sleep(3)
		synchro = 1

#下に続く並列の関数を使用
def para_child():
	PARA_THD_COVERED = 300000
	PARA_SLEEP = 300
	LAT_DEST = 35.9243193
	LON_DEST = 139.9124873
	PARA_BLT_TIMEOUT = 45

	global send
	global receive
	global synchro

	#親機のパラ回避待ち
	time_start = time.time()
	while True:
		confirm = receive
		if confirm == str(1):
			print("start para avoid")
			break
		elif time.time() - time_start > PARA_BLT_TIMEOUT:
			print("partner timeout")
			break
		else:
			print("adalt para avoid waiting...")
		time.sleep(3)

	purple_area = 0

	stuck.ue_jug()

	try:
		purple_area = purple_detection.detect_para()
		print(f'purple_area : {purple_area}')

		while True:
				if PARA_THD_COVERED < purple_area:
					print("Parachute on top")
					time.sleep(PARA_SLEEP)
					motor.motor_move(70, 70, 3)
				else:
					break

		if purple_area > 100:
			print("Move Backward")
			motor.motor_move(-30, -30, 2)
			motor.motor_stop(0.2)

		else:
			print("Move Forward")
			motor.motor_move(30, 30, 2)
			motor.motor_stop(0.2)

		time.sleep(3)
		stuck.ue_jug()

		while True:
			print('Starting Calibration')
			magx_off, magy_off = run_calibration()
			adjust_direction(magx_off, magy_off, lat_dest = LAT_DEST, lon_dest = LON_DEST)
			purple_area = purple_detection.detect_para()
			print(f'purple_area : {purple_area}')
			if purple_area > 100:
				motor.motor_move(30, -30, 0.25)
				motor.motor_stop(0.5)

				time.sleep(1)

				motor.motor_move(30, 30, 1)

				time.sleep(1)
				stuck.ue_jug()
			else:
				break
			
		print("Last Move Forwward")
		motor.motor_move(30, 30, 2)

		#親機に終了報告
		send = 1
		time.sleep(5)
		synchro = 1

	except:
		print("Camera died")
		motor.motor_move(40, 40, 4)

		#親機に終了報告
		send = 1
		time.sleep(5)
		synchro = 1

#パラ回避(親機)
def para_adalt_main():
	thread1 = threading.Thread(target = blt_adalt)
	thread2 = threading.Thread(target = para_adalt)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

#パラ回避(子機)
def para_child_main():
	thread1 = threading.Thread(target = blt_child)
	thread2 = threading.Thread(target = para_child)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

if __name__ == "__main__":
	gps.open_gps()
	motor.setup()
	bmx055.bmx055_setup()

	para_adalt_main()