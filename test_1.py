import time

import release
import land
import bme280
import bmx055
import motor
import blt_adalt
#import para_fall_test
import melt
import send.send1 as send
#import send.mode3 as mode3

bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()
motor.setup()
#mode3.mode3_change()

#放出判定
release.release_main()
time.sleep(1)
send.log("Release Detected")

#放出判定確認
blt_adalt.main(0)
time.sleep(1)
send.log("release_check_ble")

#着地判定
land.land_main()
time.sleep(1)
send.log("Land Detected")

#着地判定確認
blt_adalt.main(1)
time.sleep(1)
send.log("land_check_ble")

#テグス溶断
send.log("melt start")
print("melt start")
melt.melt_down(17,3)
time.sleep(1)
send.log("melt end")

#パラ回避
#para_fall_test.para_adalt_main()
#send.log("para avoiding finished")

#被追従準備


#自律走行開始(被追従)


#親機子機入れ替え(子機に変更)


#追従開始


#ゴール判定

