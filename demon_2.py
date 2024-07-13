import time

import land
import bme280
#import bmx055
import motor
import blt_adalt
#import para_fall_test
import melt
import send.send2 as send

bme280.bme280_setup()
bme280.bme280_calib_param()
#bmx055.bmx055_setup()
motor.setup()

send.log("demon start")

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
#para_fall_test.para_child_main()