#2024/07/29 生川

#standard
import time

#src
import bme280
import bmx055
import pid_run_test
import land
import motor
import para_avoid_alone
import goal_detection
import stuck
import melt

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


	#melt sequence
	print("start melt sequence")
	send.log("start melt sequence")
	melt.melt_down(17,5)

	#para avoid sequence
	print("start para avoid sequence")
	send.log("start para avoid sequence")

	stuck.ue_jug()
	para_avoid_alone.main()

	print("end para avoid sequence")
	send.log("end para avoid sequence")

	time.sleep(1)

	stuck.ue_jug()
	##gps run sequence
	#print("start gps run sequence")
	#send.log("start gps run sequence")

	#pid_run_test.test(35.9243106, 139.912492)

	print("start run sequence")
	send.log("start run sequence")
	motor.move(28, 25, 3)

	print("end run sequence")
	send.log("end run sequence")

	stuck.ue_jug

	#print("end gps run sequence")
	#send.log("end gps run sequence")

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

		print("start main program CO2")
		send.log("start main program CO2")
		main()
		print("end goal main program CO2")
		send.log("end goal main program CO2")
	except KeyboardInterrupt:
		print("stop!!!!")