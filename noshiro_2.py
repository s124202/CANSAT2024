#2024/08/07 生川

#standard
import time

#src
import bme280
import bmx055
import motor

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

#const
from main_const import *


def setup():
	mode3.mode3_change()
	bmx055.bmx055_setup()
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	motor.setup()


def mission():
	#const
	isReach_dest = 0
	isReach_goal = 0
	re_count = 1

	#clock setup
	t_start = time.time()

	#-----1_Release_sequence-----#
	print("-----Start 1_Release_sequence-----")

	release.detect()

	print("-----Finish 1_Release_sequence-----")
	time.sleep(1)


	#-----2_Land_sequence-----#
	print("-----Start 2_Land_sequence-----")

	land.detect()
	blt_child.main(102)

	print("-----Finish 2_Land_sequence-----")
	time.sleep(1)


	#-----3_Melt_sequence-----#
	print("-----Start 3_Melt_sequence-----")

	melt.melt_down(MELT_TIME)
	blt_child.main(103)

	print("-----Finish 3_Melt_sequence-----")
	time.sleep(1)


	#-----4_Avoid_sequence-----#
	print("-----Start 4_Avoid_sequence-----")

	para_avoidance.para_child_main()

	print("-----Finish 4_Avoid_sequence-----")
	time.sleep(1)
	

	#-----5_first_follow_sequence-----#
	print("-----Start 5_first_follow_sequence-----")

	check = run_following_EM2.main()

	print("-----Finish 5_first_follow_sequence-----")
	time.sleep(1)
	
	if check == 1:
		#自律誘導
		while isReach_dest == 0:
			isReach_dest = run.run(35.9242707,139.9124209)
			
	if isReach_dest == 0:
		#-----6_second_follow_sequence-----#
		print("-----Start 6_second_follow_sequence-----")
	
		check = run_pid_EM2.main()
	
		print("-----Finish 6_second_follow_sequence-----")
		time.sleep(1)
	
		if check == 1:
			#自律誘導
			while isReach_dest == 0:
				isReach_dest = run.run(35.9242707,139.9124209)
	


	while True:
		#-----6_Goal_sequence-----#
		print("-----Start 6_Goal_sequence-----")
		re_count = 1

		while isReach_goal == 0:
			isReach_goal, re_count = goal_detection.main(re_count)
			print("count:", re_count)

			if re_count == 20 or re_count == 0:
				break

		print("-----Finish 6_Goal_sequence-----")
		time.sleep(1)
		if isReach_goal == 1:
			break
		
		#-----6_Run_sequence-----#
		print("-----Start extra_Run_sequence-----")

		while isReach_dest == 0:
			isReach_dest = run.run()

		print("-----Finish extra_Run_sequence-----")
		time.sleep(1)




if __name__ == '__main__':
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