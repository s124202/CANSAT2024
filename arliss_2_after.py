#2024/08/07 生川

#standard
import time
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
import blt_child
import run_pid_EM2
import run_following_EM2
import pid
import gps

#send
import send.mode3 as mode3
import send.send_11 as send

#const
from main_const import *


def setup():
	mode3.mode3_change()
	bmx055.bmx055_setup()
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	run_following_EM2.setup()


def mission():
	#const
	isReach_dest = 0
	isReach_goal = 0

	#-----2_Land_sequence-----#
	print("-----Start 2_Land_sequence-----")
	send.log("-----Start 2_Land_sequence-----")

	#land.detect()
	land.detect_csv()
	blt_child.main(102)

	print("-----Finish 2_Land_sequence-----")
	send.log("-----Finish 2_Land_sequence-----")
	time.sleep(1)

	for _ in range(300):
		lat_new, lon_new = gps.location()
		send.log("lat:" + str(lat_new) + "lon:" + str(lon_new))


	#-----3_Melt_sequence-----#
	print("-----Start 3_Melt_sequence-----")
	send.log("-----Start 3_Melt_sequence-----")

	melt.melt_down(MELT_TIME)
	blt_child.main(103)

	print("-----Finish 3_Melt_sequence-----")
	send.log("-----Finish 3_Melt_sequence-----")
	time.sleep(1)


	#-----4_Avoid_sequence-----#
	print("-----Start 4_Avoid_sequence-----")
	send.log("-----Start 4_Avoid_sequence-----")

	para_avoidance.para_child_main()

	print("-----Finish 4_Avoid_sequence-----")
	send.log("-----Finish 4_Avoid_sequence-----")
	time.sleep(1)
	

	#-----5_first_follow_sequence-----#
	print("-----Start 5_first_follow_sequence-----")
	send.log("-----Start 5_first_follow_sequence-----")

	check = run_following_EM2.main()

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
			temp,pres,hum,alt = bme280.bme280_read()
			print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
			writer2.writerows([[temp, pres, hum, alt]])

		f.close()
		f2.close()

	else:
		#-----6_second_follow_sequence-----#
		print("-----Start 6_second_follow_sequence-----")
		send.log("-----Start 6_second_follow_sequence-----")
	
		check = run_pid_EM2.main()
	
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
				temp,pres,hum,alt = bme280.bme280_read()
				print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
				writer2.writerows([[temp, pres, hum, alt]])

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
			temp,pres,hum,alt = bme280.bme280_read()
			print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
			writer2.writerows([[temp, pres, hum, alt]])

		f.close()
		f2.close()

		print("-----Finish extra_Run_sequence-----")
		send.log("-----Finish extra_Run_sequence-----")
		time.sleep(1)




if __name__ == '__main__':
	send.log("-----Start CO2_program_afterBLEon-----")

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
		send.log("-----Finish CO2_program-----")