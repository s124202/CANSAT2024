import motor
import red_detection

#PID直進が使えないとき（外）
def main():
	area_ratio = 0
	angle = 0
	isReach_goal = 0

	ROTATE_PWR = 30
	THD_RED_RATIO = 20 #画面を占める赤色の割合の閾値

	###-----画像誘導モードの範囲内にいた場合の処理-----###
	
	print('画像誘導を行います')
	area_ratio, angle = red_detection.detect_goal()
	print(area_ratio, angle)
	
	###-----撮像した画像の中にゴールが映っていた場合の処理-----###
	if area_ratio >= THD_RED_RATIO:
		isReach_goal = 1
		
	elif (0 < area_ratio < THD_RED_RATIO) or (angle > 0):
		###-----ゴールが真正面にあるときの処理-----###
		if angle == 2:
			motor.move(20, 24, 0.25)

		###------ゴールが真正面にないときの処理------###
		###-----目標角度を少しずらす-----###
		elif angle == 1:
			motor.motor_move(-ROTATE_PWR, ROTATE_PWR, 0.1)
			motor.motor_stop(0.5)

		elif angle == 3:
			motor.motor_move(ROTATE_PWR, -ROTATE_PWR, 0.1)
			motor.motor_stop(0.5)

	###-----撮像した画像の中にゴールが映っていない場合の処理-----###
	elif area_ratio == 0:
		print('Lost Goal')
		motor.motor_move(30, -30, 0.15)
		motor.motor_stop(0.5)
	
	###-----ゴールした場合の処理-----###
	if isReach_goal == 1:
		print('Goal')

	return isReach_goal

if __name__ == '__main__':
	motor.setup()

	print("#####-----Goal Detect Sequence: Start-----#####")

	while True:
		isReach_goal = main()
		
		if isReach_goal == 1:
			break