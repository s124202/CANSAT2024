import time

import gps
import gps_navigate
import bmx055
import motor
import PID
import calibration
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

def main(magx_off: float, magy_off: float, add_pwr: float):
	'''
	Parameters
	----------
	lat_dest : float
		目的地の緯度
	lon_dest : float
		目的地の経度
	thd_distance_goal : float
		画像誘導の範囲設定
	thd_red_area : float
		画面を占める赤色の割合の閾値 この割合を超えるとゴールしたと判定する
	'''

	area_ratio = 0
	angle = 0
	target_azimuth = 0
	isReach_goal = 0

	LAT_GOAL = 35.918273
	LON_GOAL = 139.908573
	T_CAL = 60 #キャリブレーションを行う間隔時間[sec]
	LOOP_NUM = 20 #0.05秒ごとに9軸センサを取得するので、20回のとき1秒間隔でGPSを取得する
	THD_DISTANCE_GOAL = 5 #画像誘導の範囲設定
	THD_RED_RATIO = 80 #画面を占める赤色の割合の閾値

	###-----ゴールまでの距離を測定-----###
	lat_now, lon_now = gps.location()
	goal_info = gps_navigate.vincenty_inverse(lat_now, lon_now, lat2 = LAT_GOAL, lon2 = LON_GOAL)
	distance_to_goal = goal_info['distance']
	print(f'{distance_to_goal}m')

	###-----画像誘導モードの範囲内にいた場合の処理-----###
	if distance_to_goal <= THD_DISTANCE_GOAL:
		print('画像誘導モードの範囲内にいます\n画像誘導を行います')
		area_ratio, angle = red_detection.detect_goal()
		print(area_ratio, angle)
		time.sleep(5)
		mag_data = bmx055.mag_dataRead()
		mag_x, mag_y = mag_data[0], mag_data[1]
		rover_azimuth = calibration.angle(mag_x, mag_y, magx_off, magy_off)
		rover_azimuth = standarize_angle(rover_azimuth)
		
		###-----撮像した画像の中にゴールが映っていた場合の処理-----###
		if area_ratio >= THD_RED_RATIO:
			isReach_goal = 1
		elif 0 < area_ratio < THD_RED_RATIO:
			###-----ゴールが真正面にあるときの処理-----###
			if angle == 2:
				# rover_azimuth はそのまま使用
				target_azimuth = rover_azimuth
			###------ゴールが真正面にないときの処理------###
			###-----目標角度を少しずらす-----###
			elif angle == 1:
				target_azimuth = rover_azimuth - 15
			elif angle == 3:
				target_azimuth = rover_azimuth + 15
				
			###-----PID制御により前進-----###
			theta_array = [0]*5
			PID.PID_run(target_azimuth, magx_off, magy_off, theta_array=theta_array, loop_num=20)
			motor.deceleration(20, 20)
			motor.motor_stop(0.5)

		###-----撮像した画像の中にゴールが映っていない場合の処理-----###
		elif area_ratio == 0:
			print('Lost Goal')
			pwr_unfound = 40 + add_pwr
			motor.motor_move(pwr_unfound, -pwr_unfound, 0.15)
			motor.motor_stop(0.5)
			target_azimuth = 000 #見つかっていない場合
	
	###-----画像誘導モードの範囲外にいた場合の処理-----###
	else:
		print('ゴールから遠すぎます\nGPS誘導を行います')
		PID.drive(lon_dest=LON_GOAL, lat_dest=LAT_GOAL, thd_distance=THD_DISTANCE_GOAL, t_cal=T_CAL, loop_num=LOOP_NUM)
		target_azimuth = 000 #見つかっていない場合

	###-----ゴールした場合の処理-----###
	if isReach_goal == 1:
		print('Goal')

	return isReach_goal

if __name__ == '__main__':
	gps.open_gps()
	motor.setup()
	bmx055.bmx055_setup()

	add_pwr = 0

	magx_off, magy_off = calibration.cal(40, -40, 30)

	print('Goal Detection Start')

	while True:
		isReach_goal = main(magx_off, magy_off, add_pwr)
		
		if isReach_goal == 1:
			break