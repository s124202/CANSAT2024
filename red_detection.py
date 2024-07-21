import cv2
import numpy as np

def detect_red(img):
	# HSV色空間に変換
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

def mosaic(img, ratio):
	small_img = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
	
	return cv2.resize(small_img, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def get_max_contour(mask, img):
	try:
		contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		#最大の輪郭を抽出
		max_contour = max(contours, key = cv2.contourArea)

		cv2.drawContours(img, [max_contour], -1, (0, 255, 0), thickness=2)

	except:
		max_contour = 0
	
	return img, max_contour

def get_para_area(max_contour):
	try:
		#輪郭の面積を計算
		area = cv2.contourArea(max_contour)
	except:
		area = 0

	return area

def get_center(mask, original_img):
	try:
		contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		#最大の輪郭を抽出
		max_contour = max(contours, key = cv2.contourArea)

		#最大輪郭の重心を求める
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
	#重心から現在位置とゴールの相対角度を大まかに計算
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
        #輪郭の面積を計算
        area = cv2.contourArea(max_contour)
        img_area = original_img.shape[0] * original_img.shape[1] #画像の縦横の積
        area_ratio = area / img_area * 100 #面積の割合を計算
        if area_ratio < 0.1:
            area_ratio = 0.0
        # print(f"Area ratio = {area_ratio:.1f}%")
    except:
        area_ratio = 0

    return area_ratio

#def get_larger_red_object(mask):
#	# 最小領域の設定
#	minarea = 50
#	nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
#	if nlabels > 1:
#		largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
#		center = centroids[largest_label]
#		size = stats[largest_label,cv2.CC_STAT_AREA]
#		if size > minarea:
#			return center, size
#		return None, 0
#	else:
#		return None, 0

def detect_para_movie():
	# カメラのキャプチャ
	cap = cv2.VideoCapture(0)

	while(cap.isOpened()):
		# フレームを取得
		ret, frame = cap.read()

		#カメラ表示を90度？回転
		frame = cv2.rotate(frame, cv2.ROTATE_180)

		#画像を圧縮
		frame = mosaic(frame, ratio=0.8)

		# 赤色検出
		mask = detect_red(frame)
		frame, max_contour = get_max_contour(mask, frame)
		red_area = get_para_area(max_contour)

		#リサイズ
		#frame = cv2.resize(frame, (640,640))
		#mask = cv2.resize(mask, (640, 640))

		#出力画面に赤色の面積を表示
		cv2.putText(frame, str(int(red_area)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

		# 結果表示
		cv2.imshow("Frame", frame)
		cv2.imshow("Mask", mask)

		# qキーが押されたら途中終了
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

def detect_para():
	# カメラのキャプチャ
	cap = cv2.VideoCapture(0)

	# フレームを取得
	ret, frame = cap.read()

	#カメラ表示を90度？回転
	frame = cv2.rotate(frame, cv2.ROTATE_180)

	#画像を圧縮
	frame = mosaic(frame, ratio=0.8)

	# 赤色検出
	mask = detect_red(frame)

	frame, max_contour = get_max_contour(mask, frame)

	red_area = get_para_area(max_contour)

	print(red_area)

def detect_goal_movie():
	# カメラのキャプチャ
	cap = cv2.VideoCapture(0)

	while(cap.isOpened()):
		# フレームを取得
		ret, frame = cap.read()

		frame = mosaic(frame, ratio=0.8)

		#frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)   #カメラ表示を90度回転
		frame = cv2.rotate(frame, cv2.ROTATE_180)

		# 赤色検出
		mask = detect_red(frame)

		original_img, max_contour, cx, cy = get_center(mask, frame)

		#赤が占める割合を求める
		area_ratio = get_area(max_contour, original_img)

		frame = cv2.resize(frame, (640,640))

		cv2.putText(frame, str(int(area_ratio)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

		# 結果表示
		cv2.imshow("Frame", frame)
		cv2.imshow("Mask", mask)

		# qキーが押されたら途中終了
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

def detect_goal():
	# カメラのキャプチャ
	cap = cv2.VideoCapture(0)

	# フレームを取得
	ret, frame = cap.read()

	#画像を圧縮
	frame = mosaic(frame, ratio=0.8)
	
	frame = cv2.rotate(frame, cv2.ROTATE_180)   #カメラ表示を90度回転

	frame = cv2.resize(frame, (640,640))

	# 赤色検出
	mask = detect_red(frame)

	original_img, max_contour, cx, cy = get_center(mask, frame)

	#赤が占める割合を求める
	area_ratio = get_area(max_contour, original_img)

	#重心から現在位置とゴールの相対角度を大まかに計算
	angle = get_angle(cx, cy, original_img)
	
	return area_ratio, angle

if __name__ == '__main__':
	detect_para_movie()