#2024/08/07 生川

#
FIRST_TIME_SLEEP = 10

#放出
RELEASE_TIMEOUT = 10
RELEASE_PRESS_THD = 0.2
RELEASE_JUDGE_COUNT = 8
RELEASE_JUDGE_TIME = 1

#着地
LAND_TIMEOUT = 900
LAND_PRESS_THD = 0.05
LAND_ACC_THD = 0.2
LAND_JUDGE_COUNT = 4
LAND_JUDGE_TIME = 2

#パラ回避
PARA_THD_COVERED = 300000
PARA_SLEEP = 600
PARA_BLT_TIMEOUT = 60

PARA_PWR_L = 60
PARA_PWR_R = 60
PARA_COVERED_PWR = 80

#溶断
MELT_TIME = 3.0

#走行
THD_DIRECTION = 5.0
T_CAL = 240
STUCK_JUDGE_THD_DISTANCE = 3.0
LOOP_NUM = 5

#PID
PID_LOOP_NUM = 5
PID_THD_DISTANCE_DEST = 5
PID_T_CAL = 30
PID_STUCK_JUDGE_THD_DISTANCE = 1.0

#モーター
RUN_PID_R = 60
RUN_PID_L = 60

RUN_FOLLOW_R = 60
RUN_FOLLOW_L = 60

RUN_STRAIGHT_R = 60
RUN_STRAIGHT_L = 60

RUN_CAL = 60
ROTATE_PWR = 60

#画像認識
THD_RED_RATIO = 55 #画面を占める赤色の割合の閾値

#目標地点
RUN_LAT  = 40.8694182
RUN_LON = -119.1055013

#Bluetooth通信
BLT_ADRESS = "B8:27:EB:F7:0B:E3" #子機のアドレス
