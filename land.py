#2024/08/07 生川

#standard
import time
import math

#src
import bme280
import bmx055
import gps

#const
from main_const import *


def detect():
	#-----press_check-----#
	#init
	time_start = time.time()
	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	#detect
	while True:
		press_array.pop(0)
		time.sleep(LAND_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])

		delta_press = abs(press_array[0] - press_array[1])
		if delta_press < LAND_PRESS_THD:
			press_count += 1
		else:
			press_count = 0

		print("press:", press_array, "count:", press_count)


		if press_count == LAND_JUDGE_COUNT:
			print("Press OK")
			break

		if time.time() - time_start > LAND_TIMEOUT:
			print("Press Timeout")
			break


	#-----acc_check-----#
	#init
	time_start = time.time()
	acc_count = 0
	acc_array = [0]
	bmxData = bmx055.bmx055_read()
	acc_abs = math.sqrt(bmxData[0]**2 + bmxData[1]**2 + bmxData[2]**2)
	acc_array.append(acc_abs)

	#detect
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

		print("acc:", acc_array, "count:", acc_count)


		if acc_count == LAND_JUDGE_COUNT:
			print("Acc OK")
			break

		if time.time() - time_start > LAND_TIMEOUT:
			print("Acc Timeout")
			break
	
	lat,lon = gps.location
	return lat,lon


if __name__ == '__main__':
	detect()