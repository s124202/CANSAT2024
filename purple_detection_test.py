import cv2
import numpy as np

def detect_purple(img):
	# HSV色空間に変換
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# 紫色のHSVの値域
	hsv_min = np.array([110,210,0])
	hsv_max = np.array([140,255,255])
	mask = cv2.inRange(hsv, hsv_min, hsv_max)

	return mask

def mosaic(img, ratio):
	small_img = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
	
	return cv2.resize(small_img, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def get_max_contour(mask, img):
	try:
		contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		# 最大の輪郭を抽出
		max_contour = max(contours, key = cv2.contourArea)

		cv2.drawContours(img, [max_contour], -1, (0, 255, 0), thickness=2)

	except:
		max_contour = 0
	
	return img, max_contour

def get_para_area(max_contour):
	try:
		# 輪郭の面積を計算
		area = cv2.contourArea(max_contour)
	except:
		area = 0

	return area

#def get_larger_purple_object(mask):
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

		# カメラ表示を180度回転
		frame = cv2.rotate(frame, cv2.ROTATE_180)

		# 画像を圧縮
		frame = mosaic(frame, ratio=0.8)

		# 赤色検出
		mask = detect_purple(frame)
		frame, max_contour = get_max_contour(mask, frame)
		purple_area = get_para_area(max_contour)

		# リサイズ
		#frame = cv2.resize(frame, (640,640))
		#mask = cv2.resize(mask, (640, 640))

		# 出力画面に赤色の面積を表示
		cv2.putText(frame, str(int(purple_area)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

		# 結果表示
		cv2.imshow("Frame", frame)
		cv2.imshow("Mask", mask)

		# qキーが押されたら途中終了
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	# カメラを閉じる
	cap.release()

	# すべてのウィンドウを閉じる
	cv2.destroyAllWindows()

def detect_para():
	# カメラのキャプチャ
	cap = cv2.VideoCapture(0)

	for i in range(5):
		# フレームを取得
		ret, frame = cap.read()

		# カメラ表示を180度回転
		frame = cv2.rotate(frame, cv2.ROTATE_180)

		# 画像を圧縮
		frame = mosaic(frame, ratio=0.8)

		# 赤色検出
		mask = detect_purple(frame)
		frame, max_contour = get_max_contour(mask, frame)
		purple_area = get_para_area(max_contour)

	# カメラを閉じる
	cap.release()

	return(purple_area)

if __name__ == '__main__':
	detect_para_movie()