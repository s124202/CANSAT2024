import time
import math

import bme280
import bmx055

def land_main():
	time_start = time.time()
	time_timeout = 300

	#閾値設定
	LAND_PRESS_THD = 0.05
	LAND_GYR_THD = 20
	LAND_ACC_THD = 0.2
	LAND_JUDGE_COUNT = 5
	LAND_JUDGE_TIME = 1

	#気圧による着地判定
	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	while True:
		press_array.pop(0)
		time.sleep(LAND_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])
		if press_array[0] != 0 and press_array[1] != 0:
			delta_press = abs(press_array[0] - press_array[1])

			if delta_press < LAND_PRESS_THD:
				press_count += 1
			else:
				press_count = 0
		
		elif press_array[0] == 0 or press_array[1] == 0:
			print('Reading Press Again')
			press_count = 0
		
		print(press_array, press_count)
		
		if press_count == LAND_JUDGE_COUNT:
			print("Press OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break
	
	#角速度による着地判定
	gyro_count = 0

	while True:
		time.sleep(LAND_JUDGE_TIME)
		bmxData = bmx055.bmx055_read()
		gyro_x = math.fabs(bmxData[3])
		gyro_y = math.fabs(bmxData[4])
		gyro_z = math.fabs(bmxData[5])

		if gyro_x < LAND_GYR_THD and gyro_y < LAND_GYR_THD and gyro_z < LAND_GYR_THD:
			gyro_count += 1
		else:
			gyro_count = 0

		print(gyro_x, gyro_y, gyro_z, gyro_count)

		if gyro_count == LAND_JUDGE_COUNT:
			print("Gyro OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break
	
	#加速度(絶対値)による着地判定
	acc_count = 0
	acc_array = [0]
	bmxData = bmx055.bmx055_read()
	acc_abs = math.sqrt(bmx055[0]**2 + bmx055[1]**2 + bmx055[2]**2)
	acc_array.append(acc_abs)

	while True:
		acc_array.pop(0)
		time.sleep(LAND_JUDGE_TIME)
		bmxData = bmx055.bmx055_read()
		acc_abs = math.sqrt(bmx055[0]**2 + bmx055[1]**2 + bmx055[2]**2)
		acc_array.append(acc_abs)
		
		delta_acc = abs(acc_array[0] - acc_array[1])
		if delta_acc < LAND_ACC_THD:
			acc_count += 1
		else:
			acc_count = 0
		
		print(acc_array, acc_count)
		
		if acc_count == LAND_JUDGE_COUNT:
			print("Acceleration OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break

if __name__ == "__main__":
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	bmx055.bmx055_setup()

	try:
		land_main()

	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)