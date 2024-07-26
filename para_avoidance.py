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
	LAT_DEST = 
	LON_DEST = 

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

	if red_area > 50:
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
	LAT_DEST = 
	LON_DEST = 

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

	if red_area > 50:
		print("Move Backwward")
		motor.motor_move(-40, -40, 2)
		#motor.motor_stop(0.2)

	else:
		print("Move Forward")
		motor.motor_move(40, 40, 2)
		#motor.motor_stop(0.2)
	
	while True:
		red_area = red_detection.detect_para()
		print(f'red_area : {red_area}')
		if red_area > 0:
			motor(30, -30, 0.3)
			motor.motor_stop(0.5)
			motor.motor_move(30, 30, 8)
		else:
			break
	
	print("Last Move Forwward")
	motor.motor_move(30, 30, 5)

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
			motor.motor_move(70, -70, 2)
		else:
			break

	if red_area > 50:
		print("Move Backwward")
		motor.motor_move(-40, 40, 2)
		#motor.motor_stop(0.2)

	else:
		print("Move Forward")
		motor.motor_move(40, -40, 2)
		#motor.motor_stop(0.2)
	
	while True:
		print('Starting Calibration')
		magx_off, magy_off = calibration.cal(40, 40, 30)
		lat_now, lon_now = gps.location()
		goal_info = gps_navigate.vincenty_inverse(lat_now, lon_now, lat2 = LAT_DEST, lon2 = LON_DEST)
		goal_azimuth = goal_info['azimuth1']
		theta_array = [0]*5
		PID.PID_adjust_direction(target_azimuth=goal_azimuth, magx_off=magx_off, magy_off=magy_off, theta_array=theta_array)
		red_area = red_detection.detect_para()
		print(f'red_area : {red_area}')
		if red_area > 0:
			motor(30, 30, 0.3)
			motor.motor_stop(0.5)
			motor.motor_move(30, -30, 8)
		else:
			break
	
	print("Last Move Forwward")
	motor.motor_move(30, -30, 5)

if __name__ == '__main__':
	gps.open_gps()
	motor.setup()
	bmx055.bmx055_setup()

	print("#####-----Parachute Avoid Sequence: Start-----#####")

	print("Para Avoid Start")
	
	main3()

	print("#####-----Parachute Avoid Sequence: Finish-----#####")