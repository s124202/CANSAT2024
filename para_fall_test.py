<<<<<<< HEAD
=======
#2024/07/10　sato

>>>>>>> 6640247e53b6ff8bfe1c6813d2e8d665aacbcf2f
import para_avoidance
import motor
import stuck

motor.setup()

<<<<<<< HEAD
print("Improving the rover's posture")
stuck.correct_posture()
=======
#print("Improving the rover's posture")
#stuck.correct_posture()
>>>>>>> 6640247e53b6ff8bfe1c6813d2e8d665aacbcf2f

print("#####-----Parachute Avoid Sequence: Start-----#####")

print("Para Avoid Start")

check_count = 0 #パラ回避用のカウンター
red_area = 0
<<<<<<< HEAD
PARA_THD_COVERED = 69120*0.7

red_area = para_avoidance.detect_red()

if red_area > PARA_THD_COVERED:
    print("Parachute on top")
    motor.move(80, 80, 5)
elif red_area == 0:
    print("Move Forwward")
    motor.move(60, 60, 5) #徐々に減速するはず
    #motor.motor_stop(0.2)
else:
    print("Move Backwward")
    motor.move(-60, -60, 5) #徐々に減速するはず
    #motor.motor_stop(0.2)
=======
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
>>>>>>> 6640247e53b6ff8bfe1c6813d2e8d665aacbcf2f
