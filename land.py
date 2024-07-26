#standard
import time
import math

import bme280
import bmx055

def detect():
	#const
	LAND_PRESS_THD = 0.05
	LAND_JUDGE_COUNT = 3
	LAND_JUDGE_TIME = 2
	LAND_ACC_THD = 0.2
	time_timeout = 300

	#init
	time_start = time.time()
	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	#気圧による着地判定
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

		print("press:", press_array, "count:", press_count)


		if press_count == LAND_JUDGE_COUNT:
			print("Press OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break

	#加速度(絶対値)による着地判定
	acc_count = 0
	acc_array = [0]
	bmxData = bmx055.bmx055_read()
	acc_abs = math.sqrt(bmxData[0]**2 + bmxData[1]**2 + bmxData[2]**2)
	acc_array.append(acc_abs)

	while True:
		acc_array.pop(0)
		time.sleep(LAND_JUDGE_TIME)
		bmxData = bmx055.bmx055_read()
		acc_abs = math.sqrt(bmxData[0]**2 + bmxData[1]**2 + bmxData[2]**2)
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

	print("land test finished")


if __name__ == '__main__':
	land()