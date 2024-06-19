import time
import bme280

#気圧による放出判定
def release_main():
	time_start = time.time()
	time_timeout = 400
	
	release_press_thd = 0.3 
	release_judge_count = 5
	release_judge_time = 10

	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	while True:
		press_count = 0
		press_array.pop(0)
		time.sleep(release_judge_time)
		press_array.append(bme280.bme280_read()[1])
		print(press_array)
		if press_array[0] != 0 and press_array[1] != 0:
			delta_press = press_array[1] - press_array[0]

			if delta_press > release_press_thd:
				press_count += 1
			
			else:
				continue

		elif press_array[0] == 0 or press_array[1] == 0:
			print('Reading Press Again')
			continue

		if press_count == release_judge_count:
			print("press_ok")
			break

		if time.time() - time_start > time_timeout:
			print("press_timeout")
			break



if __name__ == "__main__":
	bme280.bme280_setup()
	bme280.bme280_calib_param()

	try:
		release_main()

	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)