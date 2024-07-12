import time

import release
import land
import bme280
import bmx055
import motor
import blt_child
import para_fall_test
import melt
import send.send as send
import send.mode3 as mode3

bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()
motor.setup()
mode3.mode3_change()

#放出判定
release.release_main()
time.sleep(1)

#放出判定確認
blt_child.main(0)
time.sleep(1)
send.log("release_check_ble")

#着地判定
land.land_main()
time.sleep(1)
send.log("Land Detected")

#着地判定確認
blt_child.main(1)
time.sleep(1)
send.log("land_check_ble")

#テグス溶断
send.log("melt start")
melt.melt_down(17,3)
time.sleep(1)
send.log("melt end")

#パラ回避
para_fall_test.para_child_main()
send.log("para_detect_end")