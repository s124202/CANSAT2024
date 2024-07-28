import gps
import bmx055
import motor
import red_detection
import straight

def main():
	area_ratio = 0
	angle = 0
	isReach_goal = 0

	LITTLE_ROTATE_PWR = 20
	ROTATE_PWR = 30
	THD_RED_RATIO = 75 #画面を占める赤色の割合の閾値

	###-----画像誘導モードの範囲内にいた場合の処理-----###
	
	print('画像誘導を行います')
	area_ratio, angle = red_detection.detect_goal()
	print(area_ratio, angle)
	
	###-----撮像した画像の中にゴールが映っていた場合の処理-----###
	if area_ratio >= THD_RED_RATIO:
		isReach_goal = 1
		
	elif 0 < area_ratio < THD_RED_RATIO:
		###-----ゴールが真正面にあるときの処理-----###
		if angle == 2:
			###-----PID制御により前進-----###
			straight(motor_pwr = 30, move_time = 2)

		###------ゴールが真正面にないときの処理------###
		###-----目標角度を少しずらす-----###
		elif angle == 1:
			motor.motor_move(-LITTLE_ROTATE_PWR, LITTLE_ROTATE_PWR, 0.15)
			motor.motor_stop(0.5)

		elif angle == 3:
			motor.motor_move(LITTLE_ROTATE_PWR, -LITTLE_ROTATE_PWR, 0.15)
			motor.motor_stop(0.5)

	###-----撮像した画像の中にゴールが映っていない場合の処理-----###
	elif area_ratio == 0:
		print('Lost Goal')
		motor.motor_move(ROTATE_PWR, -ROTATE_PWR, 0.15)
		motor.motor_stop(0.5)
	
	###-----ゴールした場合の処理-----###
	if isReach_goal == 1:
		print('Goal')

	return isReach_goal

#PID直進が使えないとき
def main2():
	area_ratio = 0
	angle = 0
	isReach_goal = 0

	ROTATE_PWR = 20
	GO_STRAIGHT_PWR = 30
	THD_RED_RATIO = 75 #画面を占める赤色の割合の閾値

	###-----画像誘導モードの範囲内にいた場合の処理-----###
	
	print('画像誘導を行います')
	area_ratio, angle = red_detection.detect_goal()
	print(area_ratio, angle)
	
	###-----撮像した画像の中にゴールが映っていた場合の処理-----###
	if area_ratio >= THD_RED_RATIO:
		isReach_goal = 1
		
	elif 0 < area_ratio < THD_RED_RATIO:
		###-----ゴールが真正面にあるときの処理-----###
		if angle == 2:
			motor.motor_move(GO_STRAIGHT_PWR + 5, -GO_STRAIGHT_PWR, 2)

		###------ゴールが真正面にないときの処理------###
		###-----目標角度を少しずらす-----###
		elif angle == 1:
			motor.motor_move(-ROTATE_PWR, -ROTATE_PWR, 0.1)
			motor.motor_stop(0.5)

		elif angle == 3:
			motor.motor_move(ROTATE_PWR, ROTATE_PWR, 0.1)
			motor.motor_stop(0.5)

	###-----撮像した画像の中にゴールが映っていない場合の処理-----###
	elif area_ratio == 0:
		print('Lost Goal')
		motor.motor_move(ROTATE_PWR, ROTATE_PWR, 0.15)
		motor.motor_stop(0.5)
	
	###-----ゴールした場合の処理-----###
	if isReach_goal == 1:
		print('Goal')

	return isReach_goal

if __name__ == '__main__':
	gps.open_gps()
	motor.setup()
	bmx055.bmx055_setup()

	print("#####-----Goal Detect Sequence: Start-----#####")

	while True:
		isReach_goal = main2()
		
		if isReach_goal == 1:
			break