import time
import bme280

def release_main():

	isRelease = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])
	press_array.pop(0)
	if press_array[0] != 0 and press_array[1] != 0:
		delta_press = press_array[1] - press_array[0]

		if delta_press > RELEASE_THD_PRESS:
			press_release_count += 1
			if press_release_count >= RELEASE_JUDGE_COUNT:
				isRelease = 1
		else:
			press_release_count = 0
	
	elif press_array[0] == 0 or press_array[1] == 0:
		print('Reading Press Again')
		delta_press = 0
		press_release_count = 0
	
	time.sleep(RELEASE_JUDGE_TIME)

	return latest_press, delta_press, press_release_count, isRelease

if __name__ == "__main__" :

	bme280.bme280_setup()
	bme280.bme280_calib_param()

	while True:
		try:
			latest_press, delta_press, press_release_count, isRelease = release_main(press_release_count = press_release_count, press_array = press_array)
			if isRelease == 1:
				print("release detected")
				break
		except KeyboardInterrupt:
			print('release_Interrupt')
			exit()