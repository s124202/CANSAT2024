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
T_RELEASE = 100


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
	print("-----1_Release_sequence start-----")

	#detect
	while True:
		#timeout
		if t_start - time.time() > T_RELEASE:
			print("Release_sequence timeout")
		
		

if __name__ == '__main__':
	try:
		print("-----Start setup-----")
		setup()
		print("-----Finish setup-----")

		time.sleep(1)
		
		print("-----Start mission-----")
		mission()
		print("-----Finish mission-----")

	except KeyboardInterrupt:
		print("-----Keyboard interrupt-----")