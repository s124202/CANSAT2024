#2024/08/07 生川

#
FIRST_TIME_SLEEP = 60

#放出
RELEASE_TIMEOUT = 180
RELEASE_PRESS_THD = 0.2
RELEASE_JUDGE_COUNT = 3
RELEASE_JUDGE_TIME = 1

#着地
LAND_TIMEOUT = 300
LAND_PRESS_THD = 0.05
LAND_ACC_THD = 0.2
LAND_JUDGE_COUNT = 3
LAND_JUDGE_TIME = 2

#パラ回避
PARA_THD_COVERED = 300000
PARA_SLEEP = 30
PARA_BLT_TIMEOUT = 120

#溶断
MELT_PIN = 17
MELT_TIME = 5.0

#走行
THD_DIRECTION = 5.0
T_CAL = 60

#PID
PID_LOOP_NUM = 5
PID_THD_DISTANCE_DEST = 5
PID_T_CAL = 30
PID_STUCK_JUDGE_THD_DISTANCE = 1.0

#モーター
RUN_PID_R = 30
RUN_PID_L = 20

RUN_FOLLOW_R = 30
RUN_FOLLOW_L = 20

RUN_STRAIGHT_R = 30
RUN_STRAIGHT_L = 20
RUN_CAL = 30
ROTATE_PWR = 30
THD_RED_RATIO = 20 #画面を占める赤色の割合の閾値

#目標地点
RUN_LAT  = 40.142282
RUN_LON = 139.987399

#Bluetoothアドレス
BLT_ADRESS = "B8:27:EB:B3:DE:30" #親機のアドレス