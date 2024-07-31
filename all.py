#2024/07/29 生川

#standard
import time

#src
import bme280
import bmx055
import run_test
import land
import motor
import para_avoid_alone
import goal_detection
import stuck
import melt
import blt_child

#send
import send.mode3 as mode3
import send.send_11 as send


def setup():
	mode3.mode3_change()
	bmx055.bmx055_setup()
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	motor.setup()


def main():
	#land sequence
	print("start land sequence")
	send.log("start land sequence")

	land.detect()

	print("end land sequence")
	send.log("end land sequence")

	time.sleep(1)


	#land wait
	# print("start land wait")
	# send.log("start land wait")

	# blt_child.main(0)

	# print("end land wait")
	# send.log("end land wait")


	#melt sequence
	print("start melt sequence")
	send.log("start melt sequence")

	#melt.melt_down(17,5)

	print("end melt sequence")
	send.log("end melt sequence")


	#para wait
	# print("start para wait")
	# send.log("start para wait")

	# blt_child.main(1)

	# print("end para wait")
	# send.log("end para wait")


	#para avoid sequence
	print("start para avoid sequence")
	send.log("start para avoid sequence")

	stuck.ue_jug()
	para_avoid_alone.main()

	print("end para avoid sequence")
	send.log("end para avoid sequence")

	time.sleep(1)


	#run start wait
	# print("start run wait")
	# send.log("start run wait")

	# blt_child.main(2)

	# print("end run wait")
	# send.log("end run wait")


	#gps run sequence
	print("start run sequence")
	send.log("start run sequence")

	run_test.main(35.9243193, 139.9124873)

	print("end run sequence")
	send.log("end run sequence")

	time.sleep(1)


	#goal detect sequence
	print("start goal detect sequence")
	send.log("start goal detect sequence")

	while True:
		isReach_goal = goal_detection.main()

		if isReach_goal == 1:
			break

	print("end goal detect sequence")
	send.log("end goal detect sequence")

	time.sleep(1)


if __name__ == '__main__':
	try:
		setup()

		time.sleep(1)

		print("start main program VOC")
		send.log("start main program VOC")
		main()
		print("end goal main program VOC")
		send.log("end goal main program VOC")
	except KeyboardInterrupt:
		print("stop!!!!")