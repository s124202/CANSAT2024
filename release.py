#2024/08/07 生川

#standard
import time
import csv

#src
import bme280

#const
from main_const import *


def detect():
    #init
	time_start = time.time()
	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

    #detect
	while True:
		press_array.pop(0)
		time.sleep(RELEASE_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])

		delta_press = press_array[1] - press_array[0]
		if delta_press > RELEASE_PRESS_THD:
			press_count += 1
		else:
			press_count = 0

		print("press:", press_array, "count:", press_count)


		if press_count == RELEASE_JUDGE_COUNT:
			break

		if time.time() - time_start > RELEASE_TIMEOUT:
			print("Release Timeout")
			break

def detect_csv():
	#init(csv)
	filename = "log/release_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	f = open(filename,"w")
	writer = csv.writer(f)

    #init
	time_start = time.time()
	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

    #detect
	while True:
		press_array.pop(0)
		time.sleep(RELEASE_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])

		delta_press = press_array[1] - press_array[0]
		if delta_press > RELEASE_PRESS_THD:
			press_count += 1
		else:
			press_count = 0

		print("press:", press_array, "count:", press_count)
		writer.writerows([[press_array,press_count]])


		if press_count == RELEASE_JUDGE_COUNT:
			break

		if time.time() - time_start > RELEASE_TIMEOUT:
			print("Release Timeout")
			break
	
	f.close()


if __name__ == "__main__":
	bme280.bme280_setup()
	bme280.bme280_calib_param()

	try:
		detect()

	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)