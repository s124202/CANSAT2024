import time

import release
import land
import bme280
#import bmx055
import motor
import blt_adalt
import para_fall_test
import melt
import send.send1 as send



bme280.bme280_setup()
bme280.bme280_calib_param()
#bmx055.bmx055_setup()
#motor.setup()
#mode3.mode3_change()


#放出判定
release.release_main()
time.sleep(1)
#send.log("Release Detected")


#着地判定
land.land_main()
time.sleep(1)
#send.log("Land Detected")