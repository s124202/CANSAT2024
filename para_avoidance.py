import time

import calibration
import gps
import motor
import bmx055
import PID
import red_detection

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

def main(lat_land, lon_land, lat_dest, lon_dest, check_count :int, add_pwr: int):

	'''
	lat_land : float
		着地地点の緯度
	lon_land : float
		着地地点の経度
	lat_dest : float
		目的地の緯度
	lon_dest : float
		目的地の経度
	check_count : int
		パラシュート回避用のカウンター
	'''

	isDistant_para = 0 #パラシュート回避用のフラグ
	red_area = 0

	PARA_PWR = 40 #パラシュートを見つけたときに回転するモーター出力
	T_ROTATE = 0.25 #パラシュートを見つけたときに回転する時間
	THD_AVOID_ANGLE = 30
	PARA_FORWARD_ANGLE = 45
	SHORT_THD_DIST = 3 #これ以上離れたときPID制御により走行する
	LONG_THD_DIST = 7 #これ以上離れたときPID制御により長く走行する
	PARA_RUN_SHORT = 3
	PARA_RUN_LONG = 10

	para_info = calibration.calculate_direction(lon2=lon_land, lat2=lat_land)
	para_dist = para_info['distance'] #パラシュートまでの距離を計算
	para_azimuth = para_info['azimuth1'] #パラシュートの方位角を計算
	print(f'{para_dist}m')

	if para_dist <= SHORT_THD_DIST:
		magx_off, magy_off = 192.5, -367.5
		print('Warning: Parachute is very close\nStarting Parachute Avoid Sequence')
		red_area = red_detection.detect_para()

		if red_area == 0:
			print("Move Forwward")
			mag_data = bmx055.mag_dataRead()
			mag_x, mag_y = mag_data[0], mag_data[1]
			rover_azimuth = calibration.angle(mag_x, mag_y, magx_off=magx_off, magy_off=magy_off)
			rover_azimuth = standarize_angle(rover_azimuth)
			target_azimuth = rover_azimuth

			#-run forward-#
			t_start_runf = time.time()
			theta_array = [0]*5
			while time.time() - t_start_runf <= 2: #2秒間前進
				PID.PID_run(target_azimuth, magx_off=magx_off, magy_off=magy_off, theta_array=theta_array, loop_num=20)
			motor.deceleration(15, 15)
			motor.motor_stop(0.2)
		else:
			print('Parachute Found\nTurning Around')
			para_pwr = PARA_PWR + add_pwr
			motor.move(para_pwr, -para_pwr, T_ROTATE)
	
	elif SHORT_THD_DIST < para_dist <= LONG_THD_DIST:
		print('Starting Calibration')
		magx_off, magy_off = calibration.cal(40, -40, 30) #キャリブレーション
		para_direction = calibration.calculate_direction(lon2=lon_land, lat2=lat_land) #パラシュート位置の取得
		para_azimuth = para_direction["azimuth1"]
		target_azimuth = para_azimuth + 180
		if target_azimuth >= 360:
			target_azimuth = target_azimuth % 360
		
		###-----パラシュートがある方向から180度の向きに走らせる-----###
		theta_array = [0]*5
		PID.PID_adjust_direction(target_azimuth=target_azimuth, magx_off=magx_off, magy_off=magy_off, theta_array=theta_array)
		theta_array = [0]*5

		red_area = red_detection.detect_para()    

		if red_area == 0:
			t_run_start = time.time()
			while time.time() - t_run_start <= PARA_RUN_SHORT:
				PID.PID_run(target_azimuth=target_azimuth, magx_off=magx_off, magy_off=magy_off,theta_array=theta_array, loop_num=20)
			motor.deceleration(15, 15)
			motor.motor_stop(1)
		else:
			target_azimuth = para_azimuth + 90
			if target_azimuth >= 360:
				target_azimuth = target_azimuth % 360
			red_area = red_detection.detect_para()
			if red_area == 0:
				t_run_start = time.time()
				while time.time() - t_run_start <= PARA_RUN_SHORT:
					PID.PID_run(target_azimuth=target_azimuth, magx_off=magx_off, magy_off=magy_off,theta_array=theta_array, loop_num=20)
				motor.deceleration(15, 15)
				motor.motor_stop(1)

	elif para_dist > LONG_THD_DIST: #これどうする？？
		goal_info = calibration.calculate_direction(lon2=lon_dest, lat2=lat_dest)
		goal_azimuth = goal_info['azimuth1']

		if abs(goal_azimuth - para_azimuth) < THD_AVOID_ANGLE:
			print('Parachute is on the way')
			target_azimuth = para_azimuth + PARA_FORWARD_ANGLE #パラシュートの方向から45度の方向に走らせる
			print("Heading " + str(target_azimuth) + " degrees")

			magx_off, magy_off = calibration.cal(40, -40, 30) #キャリブレーション

			t_run_start = time.time()
			while time.time() - t_run_start <= PARA_RUN_LONG:
				theta_array = [0]*5
				PID.PID_run(target_azimuth=target_azimuth, magx_off=magx_off, magy_off=magy_off, theta_array=theta_array,loop_num=20)
			motor.deceleration(15, 15)
			motor.motor_stop(1)
		else:
			isDistant_para = 1
	
	time.sleep(1)

	return isDistant_para

if __name__ == '__main__':
	gps.open_gps()
	motor.setup()
	bmx055.bmx055_setup()

	#print("Improving the rover's posture")
	#stuck_sato.correct_posture()

	print("#####-----Parachute Avoid Sequence: Start-----#####")

	print("Para Avoid Start")
	
	t_start = time.time()
	lat_land, lon_land = gps.location()
	red_area = red_detection.detect_para()

	PARA_THD_COVERED = 300000

	red_area = red_detection.detect_para()
	print(f'red_area : {red_area}')

	while True:
		if PARA_THD_COVERED < red_area:
			print("Parachute on top")
			motor.move(70, 70, 5)
		else:
			break

	if red_area > 1000:
		print("Move Backwward")
		motor.move(50, 50, 3) #徐々に減速するはず
		#motor.motor_stop(0.2)
	else:
		print("Move Forward")
		motor.move(-50, -50, 3) #徐々に減速するはず
		#motor.motor_stop(0.2)
	
	while True:
		isDistant_para = main()

		if isDistant_para == 1:
			break

	print("Para Avoid End")
