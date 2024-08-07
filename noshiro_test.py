#2024/08/07 生川

#standard
import time

#src
import bme280
import bmx055
import motor
import stuck

#seq
import release
import land
import melt

#send
import send.mode3 as mode3
import send.send_11 as send


#const
RELEASE_TIMEOUT = 100
RELEASE_PRESS_THD = 0.2
RELEASE_JUDGE_COUNT = 3
RELEASE_JUDGE_TIME = 1

LAND_TIMEOUT = 300
LAND_PRESS_THD = 0.05
LAND_ACC_THD = 0.2
LAND_JUDGE_COUNT = 3
LAND_JUDGE_TIME = 2

MELT_TIME = 5.0


def setup():
	mode3.mode3_change()
	bmx055.bmx055_setup()
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	motor.setup()


def mission():
	#clock setup
	t_start = time.time()

	#-----1_Release_sequence-----#
	print("-----Start 1_Release_sequence-----")

	release.detect()

	print("-----Finish 1_Release_sequence-----")


	#-----2_Land_sequence-----#
	print("-----Start 2_Land_sequence-----")

	land.detect()#landファイルの書き換えする！！！！

	print("-----Finish 2_Land_sequence-----")


	#-----3_Melt_sequence-----#
	print("-----Start 3_Melt_sequence-----")

	melt.melt_down(17,MELT_TIME)

	print("-----Finish 3_Melt_sequence-----")


	#-----4_Avoid_sequence-----#
	print("-----Start 4_Avoid_sequence-----")

	#どうするか佐藤と相談

	print("-----Finish 4_Avoid_sequence-----")


	#-----5_Run_sequence-----#
	print("-----Start 5_Run_sequence-----")

	#runファイル作ります
	#pid用
	#pid無し用

	print("-----Finish 5_Run_sequence-----")


	#-----6_Goal_sequence-----#
	print("-----Start 6_Goal_sequence-----")

	#どうするか佐藤と相談

	print("-----Finish 6_Goal_sequence-----")


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