#2024/07/10　sato

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
print(f'red_area : {red_area}')

while True:
	if PARA_THD_COVERED < red_area:
		print("Parachute on top")
		motor.move(80, 80, 5)
	else:
		break

if red_area > 1000:
	print("Move Backwward")
	motor.move(70, 70, 3) #徐々に減速するはず
	#motor.motor_stop(0.2)
else:
	print("Move Forward")
	motor.move(-70, -70, 3) #徐々に減速するはず
	#motor.motor_stop(0.2)