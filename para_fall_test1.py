import time

import para_avoidance
import motor
import stuck

motor.setup()

#print("Improving the rover's posture")
#stuck.correct_posture()

print("#####-----Parachute Avoid Sequence: Start-----#####")

print("Para Avoid Start")

check_count = 0 #パラ回避用のカウンター
red_area = 0
PARA_THD_COVERED = 255000

red_area = para_avoidance.detect_para()

while True:
	if red_area > PARA_THD_COVERED:
		print("Parachute on top")
		motor.move(80, 80, 5)
		break
	else:
		break

if red_area > 1000:
	print("Move Forwward")
	motor.move(60, 60, 5) #徐々に減速するはず
	#motor.motor_stop(0.2)
else:
	print("Move Backwward")
	motor.move(-60, -60, 5) #徐々に減速するはず
	#motor.motor_stop(0.2)