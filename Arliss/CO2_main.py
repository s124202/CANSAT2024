#2024/08/07 生川

#standard
import time
import csv
import math

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

#send
import send.mode3 as mode3
import send.send_11 as send


def setup():
	mode3.mode3_change()
	bmx055.bmx055_setup()
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	run_following_EM2.setup()


def mission():
	#const
	t_start = time.time()
	seq_num = 1
	isReach_dest = 0
	isReach_goal = 0

	#main
	while True:
		#----------1_Release_sequence----------#
		if seq_num == 1:
			#send
			print("-----Start 1_Release_sequence-----")
			send.log("-----Start 1_Release_sequence-----")

			#init(csv)
			filename = "log/release_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
			f = open(filename,"w")
			writer = csv.writer(f)

			#init(press)
			time_start = time.time()
			press_count = 0
			press_array = [0]
			press_array.append(bme280.bme280_read()[1])

			#detect
			while time.time() - time_start < RELEASE_TIMEOUT:
				press_array, press_count = release.press(press_array, press_count)

				print("press:", press_array, "count:", press_count)
				writer.writerows([[time.time() - t_start,press_array[0],press_array[1],press_count]])
				send.log(str(press_count))

				if press_count == RELEASE_JUDGE_COUNT:
					break

			else:
				print("-----Release Timeout-----")
				send.log("-----Release Timeout-----")

			#finish
			f.close()
			seq_num = 2

			#send
			print("-----Finish 1_Release_sequence-----")
			send.log("-----Finish 1_Release_sequence-----")

		time.sleep(1)

		#----------2_Land_sequence----------#
		if seq_num == 2:
			#send
			print("-----Start 2_Land_sequence-----")
			send.log("-----Start 2_Land_sequence-----")

			#-----press_check-----#
			#send
			print("----Start 2_1_PressCheck----")
			send.log("----Start 2_1_PressCheck----")

			#init(csv)
			filename = "log/land_press_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
			f = open(filename,"w")
			writer = csv.writer(f)

			#init(press)
			time_start = time.time()
			press_count = 0
			press_array = [0]
			press_array.append(bme280.bme280_read()[1])

			#detect
			while time.time() - time_start < LAND_TIMEOUT:
				press_array, press_count = land.press(press_array, press_count)

				print("press:", press_array, "count:", press_count)
				writer.writerows([[time.time() - t_start,press_array[0],press_array[1],press_count]])
				send.log(str(press_count))

				if press_count == LAND_JUDGE_COUNT:
					break

			else:
				print("-----Land Press Timeout-----")
				send.log("-----Land Press Timeout-----")

			#finish(csv)
			f.close()

			#send
			print("----Finish 2_1_PressCheck----")
			send.log("----Finish 2_1_PressCheck----")


			#-----acc_check-----#
			#send
			print("----Start 2_2_AccCheck----")
			send.log("----Start 2_2_AccCheck----")

			#init(csv)
			filename = "log/land_acc_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
			f = open(filename,"w")
			writer = csv.writer(f)

			#init(press)
			time_start = time.time()
			acc_count = 0
			acc_array = [0]
			bmxData = bmx055.bmx055_read()
			acc_abs = math.sqrt(bmxData[0]**2 + bmxData[1]**2 + bmxData[2]**2)
			acc_array.append(acc_abs)

			#detect
			while time.time() - time_start < LAND_TIMEOUT:
				acc_array, acc_count = land.acceleration(acc_array, acc_count)

				print("acc:", acc_array, "count:", acc_count)
				writer.writerows([[time.time() - t_start,acc_array[0],acc_array[1],acc_count]])
				send.log(str(acc_count))

				if acc_count == LAND_JUDGE_COUNT:
					break

			else:
				print("-----Land Acc Timeout-----")
				send.log("-----Land Acc Timeout-----")

			#finish(csv)
			f.close()

			#send
			print("----Finish 2_2_AccCheck----")
			send.log("----Finish 2_2_AccCheck----")

			#-----blt_connect-----#
			#send
			print("----blt connect waiting...----")
			send.log("----blt connect waiting...----")

			#connect
			situation = blt_child.main(102)
			if situation == 1:
				send.log("connect success")
			else:
				send.log("connect timeout")

			seq_num = 3

			#send
			print("-----Finish 2_Land_sequence-----")
			send.log("-----Finish 2_Land_sequence-----")

		time.sleep(1)

		#----------3_Melt_sequence----------#
		if seq_num == 3:
			#send
			print("-----Start 3_Melt_sequence-----")
			send.log("-----Start 3_Melt_sequence-----")

			melt.melt_down(MELT_TIME)

			#-----blt_connect-----#
			#send
			print("----blt connect waiting...----")
			send.log("----blt connect waiting...----")

			#connect
			blt_child.main(103)
			if situation == 1:
				send.log("connect success")
			else:
				send.log("connect timeout")

			seq_num = 4

			#send
			print("-----Finish 3_Melt_sequence-----")
			send.log("-----Finish 3_Melt_sequence-----")

		time.sleep(1)


	#-----4_Avoid_sequence-----#
	# print("-----Start 4_Avoid_sequence-----")
	# send.log("-----Start 4_Avoid_sequence-----")

	# para_avoidance.para_child_main()

	# print("-----Finish 4_Avoid_sequence-----")
	# send.log("-----Finish 4_Avoid_sequence-----")
	# time.sleep(1)
	

	# #-----5_first_follow_sequence-----#
	# print("-----Start 5_first_follow_sequence-----")
	# send.log("-----Start 5_first_follow_sequence-----")

	# check = run_following_EM2.main()

	# print("-----Finish 5_first_follow_sequence-----")
	# send.log("-----Finish 5_first_follow_sequence-----")
	# time.sleep(1)
	
	# if check == 1:
	# 	#自律誘導
	# 	#init
	# 	filename = "run_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	# 	f = open(filename,"w")
	# 	writer = csv.writer(f)

	# 	while isReach_dest == 0:
	# 		#isReach_dest = run.run(RUN_LAT,RUN_LON)
	# 		isReach_dest = run.run_csv(RUN_LAT,RUN_LON, writer)
	# 		temp,pres,hum,alt = bme280.bme280_read()
	# 		print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
	# 		writer.writerows([[temp, pres, hum, alt]])
		
	# 	f.close()

	# else:
	# 	#-----6_second_follow_sequence-----#
	# 	print("-----Start 6_second_follow_sequence-----")
	# 	send.log("-----Start 6_second_follow_sequence-----")
	
	# 	check = run_pid_EM2.main()
	
	# 	print("-----Finish 6_second_follow_sequence-----")
	# 	send.log("-----Finish 6_second_follow_sequence-----")
	# 	time.sleep(1)
	
	# 	if check == 1:
	# 		#自律誘導
	# 		#init
	# 		filename = "run_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	# 		f = open(filename,"w")
	# 		writer = csv.writer(f)

	# 		while isReach_dest == 0:
	# 			#isReach_dest = run.run(RUN_LAT,RUN_LON)
	# 			isReach_dest = run.run_csv(RUN_LAT,RUN_LON, writer)
	# 			temp,pres,hum,alt = bme280.bme280_read()
	# 			print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
	# 			writer.writerows([[temp, pres, hum, alt]])

	# 		f.close()


	# while True:
	# 	#-----6_Goal_sequence-----#
	# 	print("-----Start 6_Goal_sequence-----")
	# 	send.log("-----Start 6_Goal_sequence-----")
	# 	re_count = 1

	# 	while isReach_goal == 0:
	# 		isReach_goal, re_count = goal_detection.main(re_count)
	# 		print("count:", re_count)

	# 		if re_count == 20 or re_count == 0:
	# 			break

	# 	print("-----Finish 6_Goal_sequence-----")
	# 	send.log("-----Finish 6_Goal_sequence-----")
	# 	time.sleep(1)
	# 	if isReach_goal == 1:
	# 		break
		
	# 	#-----6_Run_sequence-----#
	# 	print("-----Start extra_Run_sequence-----")
	# 	send.log("-----Start extra_Run_sequence-----")

	# 	#init
	# 	filename = "run_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	# 	f = open(filename,"w")
	# 	writer = csv.writer(f)

	# 	while isReach_dest == 0:
	# 		#isReach_dest = run.run(RUN_LAT,RUN_LON)
	# 		isReach_dest = run.run_csv(RUN_LAT,RUN_LON, writer)
	# 		temp,pres,hum,alt = bme280.bme280_read()
	# 		print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
	# 		writer.writerows([[temp, pres, hum, alt]])

	# 	f.close()

	# 	print("-----Finish extra_Run_sequence-----")
	# 	send.log("-----Finish extra_Run_sequence-----")
	# 	time.sleep(1)


def delay_time(sleep):
	for i in range(sleep):
		print("cycle:", i)
		time.sleep(1)

		if i % 10 == 0:
			send.log(str(i))


if __name__ == '__main__':
	#const
	FIRST_TIME_SLEEP = 10

	RELEASE_TIMEOUT = 10
	RELEASE_JUDGE_COUNT = 3

	LAND_TIMEOUT = 120
	LAND_JUDGE_COUNT = 3

	MELT_TIME = 5


	send.log("-----Start CO2_program-----")

	try:
		print("####-----Start setup-----####")
		setup()
		print("####-----Finish setup-----####")

		print("####-----Start sleep-----####")
		delay_time(FIRST_TIME_SLEEP)
		print("####-----Finish sleep-----####")

		print("####-----Start mission-----####")
		mission()
		print("####-----Finish mission-----####")

	except KeyboardInterrupt:
		print("####-----Keyboard interrupt-----####")

	finally:
		send.log("-----Finish CO2_program-----")