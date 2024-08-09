#2024/08/07 生川

#src
import motor
import red_detection

#const
from main_const import *


def main(re_count):
	area_ratio = 0
	angle = 0
	isReach_goal = 0

	###-----画像誘導モードの範囲内にいた場合の処理-----###
	
	print('画像誘導を行います')
	area_ratio, angle = red_detection.detect_goal()
	print(area_ratio, angle)
	
	###-----撮像した画像の中にゴールが映っていた場合の処理-----###
	if area_ratio >= THD_RED_RATIO:
		isReach_goal = 1
		re_count = 1
		
	elif (0 < area_ratio < THD_RED_RATIO) or (angle > 0):
		###-----ゴールが真正面にあるときの処理-----###
		if angle == 2:
			motor.move(20, 20, 0.1)

		###------ゴールが真正面にないときの処理------###
		###-----目標角度を少しずらす-----###
		elif angle == 1:
			motor.motor_move(-ROTATE_PWR, ROTATE_PWR, 0.15)
			motor.motor_stop(0.5)

		elif angle == 3:
			motor.motor_move(ROTATE_PWR, -ROTATE_PWR, 0.15)
			motor.motor_stop(0.5)

		re_count = 1

	###-----撮像した画像の中にゴールが映っていない場合の処理-----###
	elif area_ratio == 0:
		print('Lost Goal')
		motor.motor_move(25, -25, 0.15)
		motor.motor_stop(0.5)
		re_count += 1
	
	###-----ゴールした場合の処理-----###
	if isReach_goal == 1:
		print('Goal')
		re_count = 0

	return isReach_goal, re_count

if __name__ == '__main__':
	motor.setup()

	print("#####-----Goal Detect Sequence: Start-----#####")

	while True:
		isReach_goal = main()
		
		if isReach_goal == 1:
			break