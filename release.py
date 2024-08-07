#2024/08/07 生川

import time
import bme280


def detect():
	time_start = time.time()

	RELEASE_PRESS_THD = 0.2
	RELEASE_JUDGE_COUNT = 3
	RELEASE_JUDGE_TIME = 1
	RELEASE_TIMEOUT = 100

	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	while True:
		press_array.pop(0)
		time.sleep(RELEASE_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])
		if press_array[0] != 0 and press_array[1] != 0:
			delta_press = press_array[1] - press_array[0]

			if delta_press > RELEASE_PRESS_THD:
				press_count += 1
			else:
				press_count = 0
				
		elif press_array[0] == 0 or press_array[1] == 0:
			print('Reading Press Again')
			press_count = 0

		print(press_array, press_count)

		if press_count == RELEASE_JUDGE_COUNT:
			print("Release Detected")
			break

		if time.time() - time_start > RELEASE_TIMEOUT:
			print("Release Timeout")
			break


if __name__ == "__main__":
	bme280.bme280_setup()
	bme280.bme280_calib_param()

	try:
		detect()

	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)