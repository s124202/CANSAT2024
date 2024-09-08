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

#send
import send.mode3 as mode3
import send.send_11 as send

#const
from main_const import *


def setup():
	mode3.mode3_change()
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	run_following_EM2.setup()


def mission():
	#const
	isReach_dest = 0
	isReach_goal = 0


	#-----1_Release_sequence-----#
	print("-----Start 1_Release_sequence-----")
	send.log("-----Start 1_Release_sequence-----")

	#release.detect()
	release.detect_csv()

	print("-----Finish 1_Release_sequence-----")
	send.log("-----Finish 1_Release_sequence-----")
	time.sleep(1)


if __name__ == '__main__':
	send.log("-----Start CO2_program-----")

	try:
		print("####-----Start setup-----#####")
		setup()
		print("####-----Finish setup-----####")

		time.sleep(FIRST_TIME_SLEEP)

		print("####-----Start mission-----####")
		mission()
		print("####-----Finish mission-----####")

	except KeyboardInterrupt:
		print("####-----Keyboard interrupt-----####")

	finally:
		send.log("-----Finish CO2_program-----")