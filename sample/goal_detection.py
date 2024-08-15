#2024/08/07 生川

#src
import run_following_EM1
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
		
	elif (0 < area_ratio < THD_RED_RATIO) or (angle > 0):
		###-----ゴールが真正面にあるときの処理-----###
		if angle == 2:
			run_following_EM1.move_default(10, 10, 2)

		###------ゴールが真正面にないときの処理------###
		###-----目標角度を少しずらす-----###
		elif angle == 1:
			run_following_EM1.motor_move_default(-ROTATE_PWR, ROTATE_PWR, 0.13)
			run_following_EM1.motor_stop_default(0.5)

		elif angle == 3:
			run_following_EM1.motor_move_default(ROTATE_PWR, -ROTATE_PWR, 0.13)
			run_following_EM1.motor_stop_default(0.5)

		re_count = 1

	###-----撮像した画像の中にゴールが映っていない場合の処理-----###
	elif area_ratio == 0:
		print('Lost Goal')
		run_following_EM1.motor_move_default(10, -10, 3)
		run_following_EM1.motor_stop_default(0.5)
		re_count += 1
	
	###-----ゴールした場合の処理-----###
	if isReach_goal == 1:
		print('Goal')
		re_count = 0

	return isReach_goal, re_count

if __name__ == '__main__':
	run_following_EM1.setup()

	print("#####-----Goal Detect Sequence: Start-----#####")

	# while True:
	# 	isReach_goal = main()
		
	# 	if isReach_goal == 1:
	# 		break

	re_count = 1
	isReach_goal = 0

	while isReach_goal == 0:
		isReach_goal, re_count = main(re_count)
		print("count:", re_count)

		if re_count == 20 or re_count == 0:
			break
