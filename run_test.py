#2024/07/30 生川

#standard
import time

#src
import motor
import calibration
import bmx055
import gps
import gps_navigate

#send
import send.mode3 as mode3


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


def setup():
	motor.setup()
	bmx055.bmx055_setup()
	mode3.mode3_change()


def run_calibration():
	magx_off, magy_off = calibration.cal(20,-20,40) 
	while magx_off == 0 and magy_off == 0:
		motor.motor_move(50, 50, 1)
		magx_off, magy_off = calibration.cal(20,-20,40) 
	
	return magx_off, magy_off


def get_param(magx_off, magy_off, lat_dest, lon_dest):
	lat_now, lon_now = gps.location()
	direction = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
	distance_to_dest, target_azimuth = direction["distance"], direction["azimuth1"]
	error_theta = get_theta_dest(target_azimuth, magx_off, magy_off)
	print("distance = ", distance_to_dest, "error = ", error_theta)

	return error_theta, distance_to_dest


def adjust_direction(magx_off, magy_off, lat_dest, lon_dest):
	#init
	t_out = 30
	t_start = time.time()

	while time.time() - t_start < t_out:
		error_theta, direction = get_param(magx_off, magy_off, lat_dest, lon_dest)

		if error_theta < -15:
			motor.move(20,-20,0.1)
		elif error_theta > 15:
			motor.move(-20,20,0.1)
		else:
			break

		time.sleep(0.3)
	
	print("finish adjust")


def run(lat_test, lon_test):
	#const
	THD_DIRECTION = 5.0
	T_CAL = 15
	isReach_dest = 0

	#cal
	magx_off, magy_off = run_calibration()

	#adjust direction
	adjust_direction(magx_off, magy_off, lat_test, lon_test)
	error_theta, direction = get_param(magx_off, magy_off, lat_test, lon_test)

	#init
	t_start = time.time()

	#move
	while time.time() - t_start < T_CAL:
		motor.move(20,20,1)
		error_theta, direction = get_param(magx_off, magy_off, lat_test, lon_test)

		if direction < THD_DIRECTION:
			isReach_dest = 1
			break

	return isReach_dest

def main(lat_test, lon_test):
	#const
	isReach_dest = 0
	try:
		while isReach_dest == 0:
			isReach_dest = run(lat_test, lon_test)

		print("end gps run")

	except KeyboardInterrupt:
		print("interrupt!")


if __name__ == "__main__":
	print("start setup")
	setup()

	#target
	#lat_test = 1
	#lon_test = 1

	lat_test,lon_test = gps.med()

	print("移動してください")
	time.sleep(20)
	print("start")
	time.sleep(5)

	print("main")
	main(lat_test, lon_test)