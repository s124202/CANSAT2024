import cv2
import numpy as np
import take_photo

def detect_purple(img):
	# HSV色空間に変換
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# 紫色のHSVの値域
	hsv_min = np.array([110,210,0])
	hsv_max = np.array([140,255,255])
	mask = cv2.inRange(hsv, hsv_min, hsv_max)

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

def detect_para():
	path_all_para = 'photo/detect_para/'
	photoname = take_photo.Capture(path_all_para)
	para_img = cv2.imread(photoname)

	#画像を圧縮
	small_img = mosaic(para_img, ratio=0.8)

	#赤色であると認識させる範囲の設定
	mask = detect_purple(small_img)

	#圧縮した画像から重心と輪郭を求めて、画像に反映
	para_img, max_contour, cx, cy = get_center(mask, small_img)

	#赤色が占める割合を求める
	purple_area = get_para_area(max_contour, para_img)

	return(purple_area)

def detect_para_test():
	path_all_para = 'photo/detect_para/'
	photoname = take_photo.Capture(path_all_para)
	para_img = cv2.imread(photoname)

	#画像を圧縮
	small_img = mosaic(para_img, ratio=0.8)

	#赤色であると認識させる範囲の設定
	mask = detect_purple(small_img)

	#圧縮した画像から重心と輪郭を求めて、画像に反映
	para_img, max_contour, cx, cy = get_center(mask, small_img)

	#赤色が占める割合を求める
	purple_area = get_para_area(max_contour, para_img)

	print(purple_area)

if __name__ == '__main__':
	detect_para_test()