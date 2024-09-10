#2024/08/07 生川

#standard
import time
import board
import adafruit_sgp40
import csv

#src
import bme280
import bmx055

#seq
import release
import land
import melt
import para_avoidance
import run
import goal_detection
import blt_adalt
import run_pid_EM1
import run_following_EM1
import pid
import gps

#send
import send.mode3 as mode3
import send.send_10 as send

#const
from main_const import *


def setup():
	mode3.mode3_change()
	bmx055.bmx055_setup()
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	run_following_EM1.setup()


def mission():
	#const
	isReach_dest = 0
	isReach_goal = 0

	#setup_voc
	i2c = board.I2C() 
	sgp = adafruit_sgp40.SGP40(i2c)
	
	#-----2_Land_sequence-----#
	print("-----Start 2_Land_sequence-----")
	send.log("-----Start 2_Land_sequence-----")

	#lat,lon = land.detect()
	lat,lon = land.detect_csv()
	blt_adalt.main(102,300)

	print("-----Finish 2_Land_sequence-----")
	send.log("-----Finish 2_Land_sequence-----")
	time.sleep(1)

	for _ in range(20):
		lat_new, lon_new = gps.location()
		send.log("lat:" + str(lat_new) + "lon:" + str(lon_new))


	#-----3_Melt_sequence-----#
	print("-----Start 3_Melt_sequence-----")
	send.log("-----Start 3_Melt_sequence-----")

	blt_adalt.main(103,30)
	melt.melt_down(MELT_TIME)

	print("-----Finish 3_Melt_sequence-----")
	send.log("-----Finish 3_Melt_sequence-----")
	time.sleep(1)


	#-----4_Avoid_sequence-----#
	print("-----Start 4_Avoid_sequence-----")
	send.log("-----Start 4_Avoid_sequence-----")

	para_avoidance.para_adalt_main()

	print("-----Finish 4_Avoid_sequence-----")
	send.log("-----Finish 4_Avoid_sequence-----")
	time.sleep(1)
	

	#-----5_first_follow_sequence-----#
	print("-----Start 5_first_follow_sequence-----")
	send.log("-----Start 5_first_follow_sequence-----")

	check = run_pid_EM1.main(lat,lon)

	print("-----Finish 5_first_follow_sequence-----")
	send.log("-----Finish 5_first_follow_sequence-----")
	time.sleep(1)
	
	if check == 1:
		#自律誘導
		#init
		filename = "log/run_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
		f = open(filename,"w")
		writer = csv.writer(f)
		filename2 = "log/run_data2_" + time.strftime("%m%d-%H%M%S") + ".csv"
		f2 = open(filename2,"w")
		writer2 = csv.writer(f2)

		while isReach_dest == 0:
			isReach_dest = pid.drive(RUN_LON, RUN_LAT, writer)
			print("Raw Gas: ", sgp.raw)
			writer2.writerows([[sgp.raw]])

		f.close()
		f2.close()

	else:
		#-----6_second_follow_sequence-----#
		print("-----Start 6_second_follow_sequence-----")
		send.log("-----Start 6_second_follow_sequence-----")
	
		check = run_following_EM1.main()
	
		print("-----Finish 6_second_follow_sequence-----")
		send.log("-----Finish 6_second_follow_sequence-----")
		time.sleep(1)
	
		if check == 1:
			#自律誘導
			#init
			filename = "log/run_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
			f = open(filename,"w")
			writer = csv.writer(f)
			filename2 = "log/run_data2_" + time.strftime("%m%d-%H%M%S") + ".csv"
			f2 = open(filename2,"w")
			writer2 = csv.writer(f2)

			while isReach_dest == 0:
				isReach_dest = pid.drive(RUN_LON, RUN_LAT, writer)
				print("Raw Gas: ", sgp.raw)
				writer2.writerows([[sgp.raw]])

			f.close()
			f2.close()



	while True:
		#-----6_Goal_sequence-----#
		print("-----Start 6_Goal_sequence-----")
		send.log("-----Start 6_Goal_sequence-----")
		re_count = 1

		while isReach_goal == 0:
			isReach_goal, re_count = goal_detection.main(re_count)
			print("count:", re_count)

			if re_count == 20 or re_count == 0:
				break

		print("-----Finish 6_Goal_sequence-----")
		send.log("-----Finish 6_Goal_sequence-----")
		time.sleep(1)
		if isReach_goal == 1:
			break

		#-----6_Run_sequence-----#
		print("-----Start extra_Run_sequence-----")
		send.log("-----Start extra_Run_sequence-----")

		#自律誘導
		#init
		filename = "log/run_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
		f = open(filename,"w")
		writer = csv.writer(f)
		filename2 = "log/run_data2_" + time.strftime("%m%d-%H%M%S") + ".csv"
		f2 = open(filename2,"w")
		writer2 = csv.writer(f2)

		while isReach_dest == 0:
			isReach_dest = pid.drive(RUN_LON, RUN_LAT, writer)
			print("Raw Gas: ", sgp.raw)
			writer2.writerows([[sgp.raw]])

		f.close()
		f2.close()

		print("-----Finish extra_Run_sequence-----")
		send.log("-----Finish extra_Run_sequence-----")
		time.sleep(1)




if __name__ == '__main__':
	send.log("-----Start VOC_program_afterBLEon-----")

	try:
		print("####-----Start setup-----#####")
		setup()
		print("####-----Finish setup-----####")

		time.sleep(1)

		print("####-----Start mission-----####")
		mission()
		print("####-----Finish mission-----####")

	except KeyboardInterrupt:
		print("####-----Keyboard interrupt-----####")

	finally:
		send.log("-----Finish VOC_program-----")
