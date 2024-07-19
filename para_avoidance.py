<<<<<<< HEAD
=======
import cv2
import numpy as np
import time

def detect_red(img):
	# HSV色空間に変換
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# 赤色のHSVの値域1
	hsv_min = np.array([0,100,100])
	hsv_max = np.array([5,255,255])
	mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

	# 赤色のHSVの値域2
	hsv_min = np.array([174,100,100])
	hsv_max = np.array([179,255,255])
	mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

	mask = mask1 + mask2

	return mask

#def get_larger_red_object(mask):
#	# 最小領域の設定
#	minarea = 50
#	nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
#	if nlabels > 1:
#		largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
#		center = centroids[largest_label]
#		size = stats[largest_label,cv2.CC_STAT_AREA]
#		if size > minarea:
#			return center, size
#		return None, 0
#	else:
#		return None, 0

def mosaic(img, ratio):
	small_img = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
	return cv2.resize(small_img, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def get_max_contour(mask, img):
	try:
		contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		#最大の輪郭を抽出
		max_contour = max(contours, key = cv2.contourArea)

		cv2.drawContours(img, [max_contour], -1, (0, 255, 0), thickness=2)

	except:
		max_contour = 0
	
	return img, max_contour

def get_para_area(max_contour):
	try:
		#輪郭の面積を計算
		area = cv2.contourArea(max_contour)
	except:
		area = 0

	return area

def detect_para_movie():
	# カメラのキャプチャ
	cap = cv2.VideoCapture(0)

	while(cap.isOpened()):
		# フレームを取得
		ret, frame = cap.read()

		frame = mosaic(frame, ratio=0.8)

		# 赤色検出
		mask = detect_red(frame)

		frame, max_contour = get_max_contour(mask, frame)

		frame = cv2.resize(frame, (640,640))
		frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)   #カメラ表示を90度回転

		red_area = get_para_area(max_contour)
		#print(red_area)

		cv2.putText(frame, str(int(red_area)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

		# 結果表示
		cv2.imshow("Frame", frame)
		cv2.imshow("Mask", mask)

		# qキーが押されたら途中終了
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

def detect_para():
	# カメラのキャプチャ
	cap = cv2.VideoCapture(0)

	# フレームを取得
	ret, frame = cap.read()

	frame = mosaic(frame, ratio=0.8)

	# 赤色検出
	mask = detect_red(frame)

	frame, max_contour = get_max_contour(mask, frame)

	frame = cv2.resize(frame, (640,640))
	frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)   #カメラ表示を90度回転

	red_area = get_para_area(max_contour)

	return red_area

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

	para_info = calibration.calculate_direction(lon2=lon_land, lat2=lat_land)
	para_dist = para_info['distance'] #パラシュートまでの距離を計算
	para_azimuth = para_info['azimuth1'] #パラシュートの方位角を計算
	print(f'{para_dist}m')
	
	lat_now, lon_now = gps.location()

	if para_dist <= SHORT_THD_DIST:
		magx_off, magy_off = -830, -980
		print('Warning: Parachute is very close\nStarting Parachute Avoid Sequence')
		red_area = red_detection()
		if red_area > PARA_THD_COVERED:
			print('Parachute on top')
			time.sleep(5)
		elif red_area == 0 and check_count == 0:
			print('Parachute Not Found\nChecking Around')
			para_pwr = PARA_PWR + add_pwr
			motor.move(para_pwr, -para_pwr, T_CHECK)
		elif red_area == 0 and check_count > 0:
			print("Move Forwward")
			# motor.move(PARA_PWR, PARA_PWR, T_FORWARD)
			mag_data = bmx055.mag_dataRead()
			mag_x, mag_y = mag_data[0], mag_data[1]
			rover_azimuth = calibration.angle(mag_x, mag_y, magx_off=magx_off, magy_off=magy_off)
			rover_azimuth = basics.standarize_angle(rover_azimuth)
			target_azimuth = rover_azimuth

			#-run forward-#
			t_start_runf = time.time()
			theta_array = [0]*5
			while time.time() - t_start_runf <= 2: #2秒間前進
				PID.PID_run(target_azimuth, magx_off=magx_off, magy_off=magy_off, theta_array=theta_array, loop_num=20)
			motor.deceleration(15, 15)
			motor.motor_stop(0.2)
			# check_count += 1
		else:
			print('Parachute Found\nTurning Around')
			para_pwr = PARA_PWR + add_pwr
			motor.move(para_pwr, -para_pwr, T_ROTATE)
			check_count += 1
	
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

		red_area = detect_para()      

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
			red_area = detect_para()
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
			control_num = 'Parachute is on the way'
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

	return isDistant_para, check_count

if __name__ == '__main__':
<<<<<<< HEAD
	t_start = time.time()
	lat_land, lon_land = gps.location()
	red_area =  #赤色を検知
=======
	detect_para()
>>>>>>> 6640247e53b6ff8bfe1c6813d2e8d665aacbcf2f
