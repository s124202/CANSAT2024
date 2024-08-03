import time

import calibration
import gps
import motor
import bmx055
import PID
import red_detection
import gps_navigate
import stuck
import straight

def main():
	PARA_THD_COVERED = 300000
	PARA_TIMEOUT = 300
	LAT_DEST = 35.924582
	LON_DEST = 139.911343

	red_area = 0
	goal_azimuth = 0

	stuck.ue_jug()

	red_area = red_detection.detect_para()
	print(f'red_area : {red_area}')

	while True:
		if PARA_THD_COVERED < red_area:
			print("Parachute on top")
			time.sleep(PARA_TIMEOUT)
			straight(motor_pwr = 70, move_time = 2)
		else:
			break

	if red_area > 100:
		print("Move Backwward")
		straight(motor_pwr = -40, move_time = 2)
		#motor.motor_stop(0.2)

	else:
		print("Move Forward")
		straight(motor_pwr = 40, move_time = 2)
		#motor.motor_stop(0.2)
	
	while True:
		print('Starting Calibration')
		magx_off, magy_off = calibration.cal(40, -40, 30)
		lat_now, lon_now = gps.location()
		goal_info = gps_navigate.vincenty_inverse(lat_now, lon_now, lat2 = LAT_DEST, lon2 = LON_DEST)
		goal_azimuth = goal_info['azimuth1']
		theta_array = [0]*5
		PID.PID_adjust_direction(target_azimuth=goal_azimuth, magx_off=magx_off, magy_off=magy_off, theta_array=theta_array)
		red_area = red_detection.detect_para()
		print(f'red_area : {red_area}')
		if red_area > 0:
			motor(30, -30, 0.3)
			motor.motor_stop(0.5)
			straight(motor_pwr = 30, move_time = 7)
		else:
			break
	
	print("Last Move Forwward")
	straight(motor_pwr = 30, move_time = 5)

#PID直進が使えないとき
def main2():
	PARA_THD_COVERED = 300000
	PARA_TIMEOUT = 300

	red_area = 0

	stuck.ue_jug()

	red_area = red_detection.detect_para()
	print(f'red_area : {red_area}')

	while True:
		if PARA_THD_COVERED < red_area:
			print("Parachute on top")
			time.sleep(PARA_TIMEOUT)
			motor.move(70, 70, 2)
		else:
			break
	
	if red_area > 100:
		print("Move Backwward")
		motor.move(-40, -40, 2)
		#motor.motor_stop(0.2)

	else:
		print("Move Forward")
		motor.move(40, 40, 2)
		#motor.motor_stop(0.2)
	
	while True:
		red_area = red_detection.detect_para()
		print(f'red_area : {red_area}')
		if red_area > 0:
			motor.motor_move(30, -30, 0.3)
			motor.motor_stop(0.5)
		else:
			motor.move(30, 30, 8)
			break
	
	print("Last Move Forwward")
	motor.motor_move(30, 30, 5)

#ちょっとPID
def main3():
	PARA_THD_COVERED = 300000
	PARA_TIMEOUT = 300
	LAT_DEST = 35.924582
	LON_DEST = 139.911343

	red_area = 0
	goal_azimuth = 0

	stuck.ue_jug()

	red_area = red_detection.detect_para()
	print(f'red_area : {red_area}')

	while True:
		if PARA_THD_COVERED < red_area:
			print("Parachute on top")
			time.sleep(PARA_TIMEOUT)
			motor.motor_move(70, 70, 2)
		else:
			break

	if red_area > 100:
		print("Move Backwward")
		motor.motor_move(-30, -34, 2)
		#motor.motor_stop(0.2)

	else:
		print("Move Forward")
		motor.motor_move(30, 34, 2)
		#motor.motor_stop(0.2)
	
	while True:
		print('Starting Calibration')
		magx_off, magy_off = calibration.cal(30, 34, 30)
		lat_now, lon_now = gps.location()
		goal_info = gps_navigate.vincenty_inverse(lat_now, lon_now, lat2 = LAT_DEST, lon2 = LON_DEST)
		goal_azimuth = goal_info['azimuth1']
		theta_array = [0]*5
		PID.PID_adjust_direction(target_azimuth=goal_azimuth, magx_off=magx_off, magy_off=magy_off, theta_array=theta_array)
		red_area = red_detection.detect_para()
		print(f'red_area : {red_area}')
		if red_area > 0:
			motor(30, -34, 0.3)
			motor.motor_stop(0.5)
		else:
			motor.motor_move(30, 34, 5)
			break
	
	print("Last Move Forwward")
	motor.motor_move(30, 34, 5)






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

#黄色ローバー（EM）
def main4():
	PARA_THD_COVERED = 300000
	PARA_TIMEOUT = 300
	LAT_DEST = 35.9243193
	LON_DEST = 139.9124873

	red_area = 0

	stuck.ue_jug()

	red_area = red_detection.detect_para()
	print(f'red_area : {red_area}')

	while True:
		if PARA_THD_COVERED < red_area:
			print("Parachute on top")
			time.sleep(PARA_TIMEOUT)
			motor.motor_move(55, 50, 3)
		else:
			break

	if red_area > 100:
		print("Move Backwward")
		motor.motor_move(-34, -30, 2)
		motor.motor_stop(0.2)

	else:
		print("Move Forward")
		motor.motor_move(34, 30, 2)
		motor.motor_stop(0.2)
	
	time.sleep(3)
	stuck.ue_jug()

	while True:
		print('Starting Calibration')
		magx_off, magy_off = run_calibration()
		adjust_direction(magx_off, magy_off, lat_dest = LAT_DEST, lon_dest = LON_DEST)
		red_area = red_detection.detect_para()
		print(f'red_area : {red_area}')
		if red_area > 100:
			motor.motor_move(30, -30, 0.25)
			motor.motor_stop(0.5)

			time.sleep(1)

			motor.motor_move(34, 30, 1)

			time.sleep(1)
			stuck.ue_jug()
		else:
			break
	
	print("Last Move Forwward")
	motor.motor_move(34, 30, 2)

#青色ローバー（EM）
def main5():
	PARA_THD_COVERED = 300000
	PARA_TIMEOUT = 300
	LAT_DEST = 35.9243193
	LON_DEST = 139.9124873

	red_area = 0

	stuck.ue_jug()

	red_area = red_detection.detect_para()
	print(f'red_area : {red_area}')

	while True:
		if PARA_THD_COVERED < red_area:
			print("Parachute on top")
			time.sleep(PARA_TIMEOUT)
			motor.motor_move(46, 40, 3)
		else:
			break

	if red_area > 100:
		print("Move Backwward")
		motor.motor_move(-33, -27, 1)
		motor.motor_stop(0.2)

	else:
		print("Move Forward")
		motor.motor_move(33, 27, 1)
		motor.motor_stop(0.2)
	
	time.sleep(3)
	stuck.ue_jug()

	while True:
		print('Starting Calibration')
		magx_off, magy_off = run_calibration()
		adjust_direction(magx_off, magy_off, lat_dest = LAT_DEST, lon_dest = LON_DEST)
		red_area = red_detection.detect_para()
		print(f'red_area : {red_area}')
		if red_area > 100:
			motor.motor_move(24, -24, 0.25)
			motor.motor_stop(0.5)

			time.sleep(1)

			motor.motor_move(33, 29, 1)

			time.sleep(1)
			stuck.ue_jug()
		else:
			break
	
	print("Last Move Forwward")
	motor.motor_move(33, 27, 2)

if __name__ == '__main__':
	gps.open_gps()
	motor.setup()
	bmx055.bmx055_setup()

	print("#####-----Parachute Avoid Sequence: Start-----#####")

	print("Para Avoid Start")
	
	main5()

	print("#####-----Parachute Avoid Sequence: Finish-----#####")