import cv2
import numpy as np
import take_photo
import save_photo

def detect_red(small_img):
	# HSV色空間に変換
	hsv = cv2.cvtColor(small_img, cv2.COLOR_BGR2HSV)

	# 赤色のHSVの値域1
	hsv_min = np.array([0,100,100])
	hsv_max = np.array([5,255,255])
	mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

	# 赤色のHSVの値域2
	hsv_min = np.array([174,100,100])
	hsv_max = np.array([179,255,255])
	mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

	mask = mask1 + mask2

	return mask

def mosaic(original_img, ratio):
	small_img = cv2.resize(original_img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
	
	return cv2.resize(small_img, original_img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def get_para_area(max_contour, para_img):
	try:
		# 輪郭の面積を計算
		area = cv2.contourArea(max_contour)
	except:
		area = 0

	return area

def get_center(mask, original_img):
	try:
		contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		# 最大の輪郭を抽出
		max_contour = max(contours, key = cv2.contourArea)

		# 最大輪郭の重心を求める
		# 重心の計算
		m = cv2.moments(max_contour)
		cx,cy= m['m10']/m['m00'] , m['m01']/m['m00']
		# print(f"Weight Center = ({cx}, {cy})")
		# 座標を四捨五入
		cx, cy = round(cx), round(cy)
		# 重心位置に x印を書く
		cv2.line(original_img, (cx-5,cy-5), (cx+5,cy+5), (0, 255, 0), 2)
		cv2.line(original_img, (cx+5,cy-5), (cx-5,cy+5), (0, 255, 0), 2)

		cv2.drawContours(original_img, [max_contour], -1, (0, 255, 0), thickness=2)

	except:
		max_contour = 0
		cx = 0
		cy = 0
	
	return original_img, max_contour, cx, cy

def get_angle(cx, cy, original_img):
	angle = 0
	# 重心から現在位置とゴールの相対角度を大まかに計算
	img_width = original_img.shape[1]
	quat_width = img_width / 5
	x0, x1, x2, x3, x4, x5 = 0, quat_width, quat_width*2, quat_width*3, quat_width*4, quat_width*5

	if x0 < cx <x1:
		angle = 1
	elif x1 < cx < x4:
		angle = 2
	elif x4 < cx < x5:
		angle = 3

	return angle

def get_area(max_contour, original_img):
	try:
		# 輪郭の面積を計算
		area = cv2.contourArea(max_contour)
		img_area = original_img.shape[0] * original_img.shape[1] #画像の縦横の積
		area_ratio = area / img_area * 100 #面積の割合を計算
		if area_ratio < 0.1:
			area_ratio = 0.0
		# print(f"Area ratio = {area_ratio:.1f}%")
	except:
		area_ratio = 0

	return area_ratio

def detect_para():
	path_all_para = 'photo/detect_para/'
	photoname = take_photo.Capture(path_all_para)
	para_img = cv2.imread(photoname)
	angle = 0

	#画像を圧縮
	small_img = mosaic(para_img, ratio=0.8)

	#赤色であると認識させる範囲の設定
	mask = detect_red(small_img)

	#圧縮した画像から重心と輪郭を求めて、画像に反映
	para_img, max_contour, cx, cy = get_center(mask, small_img)

	#赤色が占める割合を求める
	red_area = get_para_area(max_contour, para_img)

	return(red_area)

def detect_goal():
	#画像の撮影から「角度」と「占める割合」を求めるまでの一連の流れ
	path_all_photo = 'photo/detect_goal/'
	photoname = take_photo.Capture(path_all_photo)
	original_img = cv2.imread(photoname)

	#画像を圧縮
	small_img = mosaic(original_img, 0.8)
	
	mask = detect_red(small_img)

	original_img, max_contour, cx, cy = get_center(mask, small_img)

	#赤が占める割合を求める
	area_ratio = get_area(max_contour, original_img)

	#重心から現在位置とゴールの相対角度を大まかに計算
	angle = get_angle(cx, cy, original_img)

	#return area_ratio, angle
	return(area_ratio, angle)

if __name__ == '__main__':
	detect_para()