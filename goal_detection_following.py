import cv2
import numpy as np

import motor
import red_detection

def get_largest_red_object(mask):
    # 最小領域の設定
    minarea = 300
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    if nlabels > 1:
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        center = centroids[largest_label]
        size = stats[largest_label,cv2.CC_STAT_AREA]
        if size > minarea:
            return center, size
        return None, None
    else:
        return None, None

def main():
	area_ratio = 0
	angle = 0
	isReach_goal = 0

	ROTATE_PWR = 30

	#追従走行の定数
	default_l = 26
	default_r= default_l + 3
	kp = 0.045
	kd = 0.01

	###-----画像誘導モードの範囲内にいた場合の処理-----###
	
	print('画像誘導を行います')
	area_ratio, angle = red_detection.detect_goal()
	print(area_ratio, angle)
	
	###-----撮像した画像の中にゴールが映っていた場合の処理-----###
	if 0 < area_ratio:
		# 追従走行
		old_center = [320,0]
		count = 0

		cap = cv2.VideoCapture(0)
		while(cap.isOpened()):
			# フレームを取得
			ret, frame = cap.read()
			frame = cv2.resize(frame, (640,320))
			frame = cv2.rotate(frame, cv2.ROTATE_180)
	
			# 赤色検出
			mask = red_detection.detect_red(frame)
	
			# 最大の赤色物体の中心を取得
			center, size = get_largest_red_object(mask)
	
			if center is None:
				center = old_center
				count += 1
			else:
				count = 0
			
			if size is None:
				size = 5000
			
			#PD制御
			mp = (int(center[0]) - 320) / 3.2   
			mp = mp * kp
	
			md = (center[0] - old_center[0]) * kd
	
			m = mp - md

			#ゴールの大きさによる速度調整
			if size < 1000:
				s = 0
			elif size < 20000:
				s = size / 2000 + 5
			else:
				motor.deceleration()
				print("arrived")
				isReach_goal = 1
				break
			
			#見失ったら停止
			if count == 60:
				print("no discover")
				motor.deceleration()
				break
			
			strength_l = default_l - s + m
			strength_r = default_r - s - m

			motor.move(strength_l, strength_r, 0.05)
	
			#print(old_center[0]-center[0])
			old_center = center    
			
		cap.release()
		cv2.destroyAllWindows()

	###-----撮像した画像の中にゴールが映っていない場合の処理-----###
	elif area_ratio == 0:
		print('Lost Goal')
		motor.motor_move(ROTATE_PWR, -ROTATE_PWR, 0.15)
		motor.motor_stop(0.5)
	
	###-----ゴールした場合の処理-----###
	if isReach_goal == 1:
		print('Goal')

	return isReach_goal

def main2():
	area_ratio = 0
	angle = 0
	isReach_goal = 0

	#追従走行の定数
	default_l = 26
	default_r= default_l + 3
	kp = 0.045
	kd = 0.01

	###-----画像誘導モードの範囲内にいた場合の処理-----###
	
	print('画像誘導を行います')
	area_ratio, angle = red_detection.detect_goal()
	print(area_ratio, angle)
	
	###-----撮像した画像の中にゴールが映っていた場合の処理-----###
	if 0 < area_ratio:
		# 追従走行
		old_center = [320,0]
		count = 0

		cap = cv2.VideoCapture(0)
		while(cap.isOpened()):
			# フレームを取得
			ret, frame = cap.read()
			frame = cv2.resize(frame, (640,320))
			frame = cv2.rotate(frame, cv2.ROTATE_180)
	
			# 赤色検出
			mask = red_detection.detect_red(frame)
	
			# 最大の赤色物体の中心を取得
			center, size = get_largest_red_object(mask)
	
			if center is None:
				center = old_center
				count += 1
			else:
				count = 0
			
			if size is None:
				size = 5000
			
			#PD制御
			mp = (int(center[0]) - 320) / 3.2   
			mp = mp * kp
	
			md = (center[0] - old_center[0]) * kd
	
			m = mp - md

			#ゴールの大きさによる速度調整
			if size < 1000:
				s = 0
			elif size < 20000:
				s = size / 2000 + 5
			else:
				motor.deceleration()
				print("arrived")
				isReach_goal = 1
				break
			
			#見失ったら停止
			if count == 60:
				print("no discover")
				motor.deceleration()
				break
			
			strength_l = default_l - s + m
			strength_r = default_r - s - m

			motor.move(strength_l, -strength_r, 0.05)
	
			#print(old_center[0]-center[0])
			old_center = center    
			
		cap.release()
		cv2.destroyAllWindows()

	###-----撮像した画像の中にゴールが映っていない場合の処理-----###
	elif area_ratio == 0:
		print('Lost Goal')
		motor.motor_move(30, 30, 0.2)
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