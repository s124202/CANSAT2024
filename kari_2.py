import cv2
import numpy as np

# カメラのキャプチャを開始
cap = cv2.VideoCapture(0)

def nothing(x):
    pass

# ウィンドウを作成
cv2.namedWindow('frame')

while True:
    # フレームをキャプチャ
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640,320))
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    
    # フレームをHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # マウスのコールバック関数
    def show_hsv(event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            hsv_value = hsv[y, x]
            print(f'HSV: {hsv_value}')
    
    # マウスのコールバック関数を設定
    cv2.setMouseCallback('frame', show_hsv)
    
    # フレームを表示
    cv2.imshow('frame', frame)
    
    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# キャプチャを解放し、ウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()
