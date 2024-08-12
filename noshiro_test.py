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
import avoid
import run
import goal_detection

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

	print("-----Finish 2_Land_sequence-----")
	time.sleep(1)


	#-----3_Melt_sequence-----#
	print("-----Start 3_Melt_sequence-----")

	melt.melt_down(MELT_PIN, MELT_TIME)

	print("-----Finish 3_Melt_sequence-----")
	time.sleep(1)


	#-----4_Avoid_sequence-----#
	print("-----Start 4_Avoid_sequence-----")

	avoid.main()

	print("-----Finish 4_Avoid_sequence-----")
	time.sleep(1)


	while re_count > 0:
		#-----5_Run_sequence-----#
		print("-----Start 5_Run_sequence-----")

		isReach_dest = 0
		while isReach_dest == 0:
			isReach_dest = run.run()

		print("-----Finish 5_Run_sequence-----")
		time.sleep(1)


		#-----6_Goal_sequence-----#
		print("-----Start 6_Goal_sequence-----")

		while isReach_goal == 0:
			isReach_goal, re_count = goal_detection.main(re_count)
			print("count:", re_count)

			if re_count == 20 or re_count == 0:
				break

		print("-----Finish 6_Goal_sequence-----")
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