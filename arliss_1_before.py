#2024/08/07 生川

#standard
import time

#src
import bme280

#seq
import release

#send
#import send.mode3 as mode3
#import send.send_10 as send

#const
from main_const import *


def setup():
	#mode3.mode3_change()
	bme280.bme280_setup()
	bme280.bme280_calib_param()

def mission():

	#-----1_Release_sequence-----#
	print("-----Start 1_Release_sequence-----")
	#send.log("-----Start 1_Release_sequence-----")

	#release.detect()
	release.detect_csv()

	print("-----Finish 1_Release_sequence-----")
	#send.log("-----Finish 1_Release_sequence-----")
	time.sleep(1)

if __name__ == '__main__':
	#send.log("-----Start VOC_program-----")

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

	#finally:
		#send.log("-----Finish VOC_program-----")