import gps
import bmx055
import motor
import red_detection

def main():
	area_ratio = 0
	angle = 0
	isReach_goal = 0

	ROTATE_PWR = 30

	###-----画像誘導モードの範囲内にいた場合の処理-----###
	
	print('画像誘導を行います')
	area_ratio, angle = red_detection.detect_goal()
	print(area_ratio, angle)
	
	###-----撮像した画像の中にゴールが映っていた場合の処理-----###
	if 0 < area_ratio:
	#追従走行ここにいれてー
		isReach_goal = 1
	###-----撮像した画像の中にゴールが映っていない場合の処理-----###
	elif area_ratio == 0:
		print('Lost Goal')
		motor.motor_move(ROTATE_PWR, -ROTATE_PWR, 0.15)
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
		isReach_goal = main()
		
		if isReach_goal == 1:
			break