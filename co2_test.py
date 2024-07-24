#2024/7/23 生川

#standard
import time
import csv
from scd30_i2c import SCD30
import math

#src
import bme280
import bmx055
import co2_sensor as co2
import gps
import motor
import melt
import blt_sub

#send
import send.mode3 as mode3
import send.send_11 as send


def sensor():
	#start
	print("start sensor test")
	send.log("start sensor test_co2")

	time.sleep(1)

	#setup
	mode3.mode3_change()
	bmx055.bmx055_setup()
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	scd30 = SCD30()
	scd30.set_measurement_interval(2)
	scd30.start_periodic_measurement()
	filename = "co2_sensor_test_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	f = open(filename,"w")
	writer = csv.writer(f)

	#const
	TIME_THD = 10
	cycle = 1

	time.sleep(1)

	#main
	start_time = time.time()
	try:
		while time.time() - start_time < TIME_THD:
			temp, pres, hum, alt = bme280.bme280_read()
			accx, accy, accz, gyrx, gyry, gyrz, magx, magy, magz = bmx055.bmx055_read()
			m_co2 = co2.scd30_get()
			lat,lon = gps.test()

			#log
			send.log(str(cycle) + "," + str(lat) + "," + str(lon) + "," + str(temp) + str(pres) + "," + str(hum) + "," + str(alt) + "," + str(accx) + "," + str(accy) + "," + str(accz) + "," + str(gyrx) + "," + str(gyrz) + "," + str(magx) + "," + str(magy) + "," + str(magz) + "," + str(m_co2))
			print("cycle", cycle)
			print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
			print("accx:" + str(accx) + "\t" + "accy:" + str(accy) + "\t" + "accz:" + str(accz))
			print("gyrx:" + str(gyrx) + "\t" + "gyry:" + str(gyry) + "\t" + "gyrz:" + str(gyrz))
			print("magx:" + str(magx) + "\t" + "magy:" + str(magy) + "\t" + "magz:" + str(magz))
			print("co2:" + str(m_co2))
			print("lat:" + str(lat) + "\t" + "lon:" + str(lon))

			writer.writerows([[cycle, lat, lon, temp, pres, hum, alt, accx, accy, accz, gyrx, gyry, gyrz, magx, magy, magz, m_co2]])

			time.sleep(1)
			cycle += 1


	except KeyboardInterrupt:
		print("keyboard interrupt")
		send.log("keyboard interrupt")

	print("sensor test finished")
	send.log("sensor test finished")


def land():
	#start
	print("start land test")
	send.log("start land test")

	time.sleep(1)

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
	filename = "co2_land_test_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	f = open(filename,"w")
	writer = csv.writer(f)

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
		writer.writerows([[press_array, press_count]])


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
		writer.writerows([[bmxData, acc_array, acc_count]])
		
		if acc_count == LAND_JUDGE_COUNT:
			print("Acceleration OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break

	print("land test finished")
	send.log("land test finished")


def t_motor():
	print("start motor test")
	send.log("start motor test")
	motor.setup()
	time.sleep(20)
	motor.move(10, 10, 3)
	print("motor test finished")
	send.log("motor test finished")


if __name__ == '__main__':
	sensor()
	land()

	#melt
	print("start melt test")
	send.log("start melt test")
	melt.melt_down(meltPin=17, t_melt = 10.0)
	print("melt test finished")
	send.log("melt test finished")

	t_motor()

	print("start bluetooth test")
	send.log("start bluetooth test")
	blt_sub.blt()
	print("bluetooth test finished")
	send.log("bluetooth test finished")