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

def detect_red():
	# カメラのキャプチャ
	cap = cv2.VideoCapture(0)

	while(cap.isOpened()):
		# フレームを取得
		ret, frame = cap.read()

		# 赤色検出
		mask = detect_red(frame)

		frame, max_contour = get_max_contour(mask, frame)

		frame = cv2.resize(frame, (640,640))
		frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)   #カメラ表示を90度回転

		red_area = get_para_area(max_contour)

		cv2.putText(frame, str(int(red_area)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

		# 結果表示
		cv2.imshow("Frame", frame)
		cv2.imshow("Mask", mask)

		# qキーが押されたら途中終了
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_red()