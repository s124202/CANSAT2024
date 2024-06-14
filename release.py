import time
import bme280

def release_main():
	#time_start = time.time()
	#time_timeout = 15

	
	
	release_press_thd = 
	release_judge_count = 
	release_judge_time = 

	press_array = [0]
	press_array.append(bme280.bme280_read()[1])
	while True:
		press_count = 0

		for i in range(5):
			press_array.pop(0)
			time.sleep(0.2)
			press_array.append(bme280.bme280_read()[1])
			print(press_array)
			press_gap = abs(press_array[0] - press_array[1])

			if press_gap < press_thd:
				press_count += 1
			else:
				break

		if press_count == 5:
			print("press_ok")
			break
		if time.time() - time_start > time_timeout:
			print("press_timeout")
			break



if __name__ == "__main__":
	bme280.bme280_setup()
	bme280.bme280_calib_param()

	try:
		land_main()

	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)